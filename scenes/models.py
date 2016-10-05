from __future__ import unicode_literals
from django.db import models
from athanor.utils.time import utcnow


# Create your models here.


class Plot(models.Model):
    owner = models.ForeignKey('objects.ObjectDB', related_name='plots')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    type = models.CharField(max_length=40, blank=True, null=True)

    def display_plot(self, viewer):
        message = list()
        message.append(viewer.render.header('Plot ID %i: %s' % (self.id, self.title)))
        message.append('Runner: %s' % self.owner)
        message.append('Schedule: %s to %s' % (viewer.time.display(date=self.date_start),
                                               viewer.time.display(date=self.date_end)))
        message.append('Status: %s' % ('Running' if not self.status else 'Finished'))
        message.append(self.description)
        message.append(viewer.render.separator('Scenes'))
        scenes_table = viewer.render.make_table(['ID', 'Name', 'Date', 'Description,', 'Participants'],
                                                width=[3, 10, 10, 10, 30])
        for scene in self.scenes.all().order_by('date_created'):
            scenes_table.add_row(scene.id, scene.title, viewer.time.display(date=scene.date_created),
                                 scene.description, '')
        message.append(scenes_table)
        message.append(viewer.render.separator('Events'))
        events_table = viewer.render.make_table('ID', 'Name', 'Date', width=[3, 10, 10])
        for event in self.events.all().order_by('date_schedule'):
            events_table.add_row(event.id, event.title, viewer.time.display(date=event.date_schedule))
        message.append(events_table)
        message.append(viewer.render.footer())
        return "\n".join([unicode(line) for line in message])

    @property
    def recipients(self):
        return [char.character for char in self.participants]

    @property
    def participants(self):
        return Participant.objects.filter(scene__in=self.scenes).values_list('character', flat=True)

    @property
    def locations(self):
        return Pose.objects.filter(scene__in=self.scenes).values_list('location', flat=True).distinct()


class Scene(models.Model):
    owner = models.ForeignKey('objects.ObjectDB', related_name='scenes')
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField()
    date_finished = models.DateTimeField(null=True)
    plot = models.ForeignKey('Plot', null=True, related_name='scenes')
    status = models.SmallIntegerField(default=0, db_index=True)

    def display_scene(self, viewer):
        message = []
        message.append(viewer.render.header('Scene %i: %s' % (self.id, self.title)))
        message.append('Started: %s' % viewer.time.display(date=self.date_created))
        if self.date_finished:
            message.append('Finished: %s' % viewer.time.display(date=self.date_finished))
        message.append('Description: %s' % self.description)
        message.append('Owner: %s' % self.owner)
        message.append('Status: %s' % self.display_status())
        message.append(viewer.render.separator('Players'))
        player_table = viewer.render.make_table(['Name', 'Status', 'Poses'], width=[35, 30, 13])
        for participant in self.participants.order_by('character'):
            player_table.add_row(participant.character, '', participant.poses.exclude(ignore=True).count())
        message.append(player_table)
        message.append(viewer.render.footer())
        return "\n".join([unicode(line) for line in message])

    def display_status(self):
        if self.status == 0:
            return 'Active'
        if self.status == 1:
            return 'Paused'
        if self.status == 3:
            return 'Finished'

    def msg(self, text):
        for character in self.recipients:
            character.msg(text)

    @property
    def recipients(self):
        recip_list = list()
        if self.owner: recip_list.append(self.owner)
        recip_list += [char.character for char in self.participants]
        return set(recip_list)

    @property
    def locations(self):
        return self.poses.values_list('location', flat=True).distinct()

    @property
    def poses(self):
        return Pose.objects.filter(owner__scene=self)


class Participant(models.Model):
    character = models.ForeignKey('objects.ObjectDB', related_name='scenes')
    scene = models.ForeignKey('scenes.Scene', related_name='participants')

    class Meta:
        unique_together = (("character", "scene"),)


class Pose(models.Model):
    owner = models.ForeignKey('scenes.Participant', related_name='poses')
    ignore = models.BooleanField(default=False, db_index=True)
    date_made = models.DateTimeField(db_index=True)
    text = models.TextField(blank=True)
    location = models.ForeignKey('objects.ObjectDB', null=True, related_name='poses_here', on_delete=models.SET_NULL)

    def display_pose(self, viewer):
        message = []
        message.append(viewer.render.separator('%s Posed on %s' % (self.owner,
                                                                   viewer.time.display(date=self.date_made))))
        message.append(self.text)
        return "\n".join([unicode(line) for line in message])


class Event(models.Model):
    owner = models.ForeignKey('objects.ObjectDB', related_name='events')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    date_schedule = models.DateTimeField(db_index=True)
    plot = models.ForeignKey('Plot', null=True, related_name='events')
    interest = models.ManyToManyField('objects.ObjectDB')
    post = models.OneToOneField('bbs.Post', related_name='event', null=True)

    def display_event(self, viewer):
        message = []
        message.append(viewer.render.header('Event ID %i: %s' % (self.id, self.title)))
        message.append('Owner: %s' % self.owner)
        message.append(self.description)
        message.append(viewer.render.separator("Scheduled Time"))
        message.append('Blah')
        message.append(viewer.render.separator('Interested Characters'))
        interested = sorted(self.interest.all(), key=lambda char: char.key.lower())
        interest_table = viewer.render.make_table(['Name', 'Connected', 'Idle'])
        for char in interested:
            interest_table.add_row(char.key, char.time.last_or_conn_time(viewer), char.time.last_or_idle_time(viewer))
        message.append(interest_table)
        message.append(viewer.render.footer())
        return "\n".join([unicode(line) for line in message])

    def setup(self):
        from classes.scripts import SETTINGS
        board = SETTINGS('scene_board')
        if not board:
            return
        subject = '#%s: %s' % (self.id, self.title)
        text = self.post_text()
        new_post = board.make_post(character=self.owner, subject=subject, text=text)
        self.post = new_post
        self.save(update_fields=['post'])

    def post_text(self):
        message = list()
        message.append('|wTitle:|n %s' % (self.title))
        message.append('|wPosted By:|n %s' % self.owner)
        message.append('|wScheduled Time:|n %s' % self.date_schedule.strftime('%b %d %I:%M%p %Z'))
        message.append('-'*78)
        message.append(self.description)
        return '\n'.join(unicode(line) for line in message)

    def delete(self, *args, **kwargs):
        if self.post:
            self.post.delete()
        super(Event, self).delete(*args, **kwargs)

    def reschedule(self, new_time):
        self.date_schedule = new_time
        self.save(update_fields=['date_schedule'])
        self.update_post()

    def retitle(self, new_title):
        self.title = new_title
        self.save(update_fields=['title'])
        self.update_post()

    def update_post(self):
        if self.post:
            self.post.text = self.post_text()
            self.post.modify_date = utcnow()
            self.post.save(update_fields=['text', 'modify_date'])

class Pot(models.Model):
    owner = models.ForeignKey('objects.ObjectDB', related_name='pot_poses')
    location = models.ForeignKey('objects.ObjectDB', related_name='pot_poses_here')
    date_made = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)