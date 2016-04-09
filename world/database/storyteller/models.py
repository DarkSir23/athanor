from __future__ import unicode_literals
from decimal import Decimal
from django.db import models
from django.db.models import Q, Sum
from evennia.utils.ansi import ANSIString
from commands.library import partial_match, sanitize_string, dramatic_capitalize

from world.storyteller.exalted3.rules import EX3_RULES

RULES_DICT = {
    'ex3': EX3_RULES,

}

# Create your models here.

class Game(models.Model):
    key = models.CharField(max_length=20, db_index=True)
    ready = models.BooleanField(default=0)

    def setup_storyteller(self, force=False):
        if self.ready and not force:
            return
        rules = RULES_DICT[self.key]
        for k, v in rules['templates'].iteritems():
            obj, created =self.templates.get_or_create(key=k)
        for k, v in rules['stats'].iteritems():
            obj, created = self.stats.get_or_create(key=k)
        for k, v in rules['custom'].iteritems():
            obj, created = self.custom_stats.get_or_create(key=k)
        for k, v in rules['pools'].iteritems():
            obj, created = self.pools.get_or_create(key=k)
        for k, v in rules['merits'].iteritems():
            obj, created = self.merits.get_or_create(key=k)
        self.ready = True
        self.save()

    @property
    def rules(self):
        return RULES_DICT[self.key]


class Template(models.Model):
    key = models.CharField(max_length=40, db_index=True)
    game = models.ForeignKey('storyteller.Game', related_name='templates')

    class Meta:
        unique_together = (("key", "game"),)

    def __str__(self):
        return self.rules['name']

    @property
    def rules(self):
        return self.game.rules['templates'][self.key]


class CharacterTemplate(models.Model):
    template = models.ForeignKey('storyteller.Template', related_name='characters')
    character = models.OneToOneField('objects.ObjectDB', related_name='storyteller')
    base_sheet_colors = {'title': 'n', 'border': 'n', 'textfield': 'n', 'texthead': 'n', 'colon': 'n',
                         'section_name': 'n', '3_column_name': 'n', 'advantage_name': 'n', 'advantage_border': 'n',
                         'slash': 'n', 'statdot': 'n', 'statfill': 'n', 'statname': 'n', 'damagename': 'n',
                         'damagetotal': 'n', 'damagetotalnum': 'n'}

    class Meta:
        unique_together = (("template", "character"),)

    def setup_character(self):
        game = self.template.game
        game_stats = game.stats.all()
        rules = game.rules
        for stat in game_stats:
            obj, created = self.stats.get_or_create(stat=stat)
            if created:
                rating = rules['stats'][stat.key].get('start_rating', 0)
                if rating:
                    obj.rating = rating
                    obj.save()

        game_pools = game.pools.all()
        for pool in game_pools:
            obj, created = self.pools.get_or_create(pool=pool)

    def __str__(self):
        return self.rules['name']

    @property
    def game(self):
        return self.template.game

    @property
    def rules(self):
        return self.game.rules['templates'][self.template.key]

    @property
    def name(self):
        return self.rules['name']

    @property
    def list_order(self):
        return self.rules['list_order']

    @property
    def pool_dict(self):
        return self.rules['pools']

    @property
    def charm_type(self):
        return self.rules['charm_type']

    @property
    def info_defaults(self):
        return self.rules['info_defaults']

    @property
    def info_choices(self):
        return self.rules['info_choices']

    @property
    def extra_sheet_colors(self):
        return self.rules['extra_sheet_colors']

    @property
    def sheet_column_1(self):
        return self.rules['sheet_column_1']

    @property
    def sheet_column_2(self):
        return self.rules['sheet_column_2']

    @property
    def sheet_footer(self):
        return self.rules['sheet_footer']

    @property
    def info(self):
        info_defaults = self.rules['info_defaults']
        info_save = self.infos.all()
        save_dict = {info.info.kind.key: info.info.key for info in info_save}
        info_dict = dict()
        info_dict.update(info_defaults)
        info_dict.update(save_dict)
        return info_dict

    def get(self, field=None):
        if not field:
            return
        try:
            response = self.info[field]
        except KeyError:
            return None
        return response

    def set(self, field=None, value=None):
        if not field:
            raise KeyError("No field entered to set!")
        info_choices = self.rules['info_choices']
        info_fields = info_choices.keys()
        found_field = partial_match(field, info_fields)
        if not found_field:
            raise KeyError("Field '%s' not found." % field)
        info_save = self.infos.all()
        if not value:
            check = self.infos.filter(info__key=found_field)
            if check:
                check.delete()

        info_kind, created = self.game.infos.get_or_create(key=found_field)

        if found_field in info_choices:
            choices = info_choices[found_field]
            find_value = partial_match(value, choices)
            if not find_value:
                raise KeyError("'%s' is not a valid entry for %s. Choices are: %s" % (value, found_field,
                                                                                      ', '.join(choices)))
            final_value = find_value
        else:
            final_value = dramatic_capitalize(sanitize_string(value))
        info_set, created2 = info_kind.values.get_or_create(key=final_value)
        info_character, created3 = info_set.characters.get_or_create(character=self)


    def swap_template(self, key=None):
        if not key:
            raise ValueError("No template entered to swap to!")
        find_template = partial_match(key, self.template.game.templates.all())
        if not find_template:
            raise ValueError("Could not find a '%s' template." % key)
        self.template = find_template
        self.save()
        self.character.story.load()

    def stat(self, key):
        return self.stats.filter(stat__key=key).first()

    def specialties(self):
        return Specialty.objects.filter(Q(stat__character=self) | Q(custom__character=self))


class InfoKind(models.Model):
    key = models.CharField(max_length=40, db_index=True)
    game = models.ForeignKey('storyteller.Game', related_name='infos')

    class Meta:
        unique_together = (("key", "game"),)
        index_together = [['key', 'game'], ]

class Info(models.Model):
    kind = models.ForeignKey('storyteller.InfoKind', related_name='values')
    key = models.CharField(max_length=255, db_index=True)

    class Meta:
        unique_together = (("key", "kind"),)

    def __str__(self):
        return self.key

class CharacterInfo(models.Model):
    character = models.ForeignKey('storyteller.CharacterTemplate', related_name='infos')
    info = models.ForeignKey('storyteller.Info', related_name='characters')

    class Meta:
        unique_together = (('character','info'),)

    def __str__(self):
        return str(self.info)

class Stat(models.Model):
    key = models.CharField(max_length=40, db_index=True)
    game = models.ForeignKey('storyteller.Game', related_name='stats')

    class Meta:
        unique_together = (("key", "game"),)
        index_together = [['key', 'game'],]


class CharacterStat(models.Model):
    character = models.ForeignKey('storyteller.CharacterTemplate', related_name='stats')
    stat = models.ForeignKey('storyteller.Stat', related_name='characters')
    rating = models.SmallIntegerField(default=0, db_index=True)
    is_favored = models.BooleanField(default=False)
    is_asset = models.BooleanField(default=False)
    is_caste = models.BooleanField(default=False)
    is_supernal = models.BooleanField(default=False)
    features_default = ({'dot', 'roll', 'favor', 'supernal', 'caste', 'special'})

    class Meta:
        unique_together = (("character", "stat"),)
        index_together = [['character', 'stat'],]

    def __str__(self):
        return self.name

    def __int__(self):
        return self.rating

    def __add__(self, other):
        return int(self) + int(other)

    def __radd__(self, other):
        return int(self) + int(other)

    @property
    def game(self):
        return self.stat.game

    @property
    def rules(self):
        return self.character.game.rules['stats'][self.stat.key]

    @property
    def name(self):
        return self.rules['name']

    @property
    def kind(self):
        return self.rules['kind']

    @property
    def category(self):
        return self.rules['category']

    @property
    def list_order(self):
        return self.rules['list_order']

    @property
    def start_rating(self):
        return self.rules['start_rating']

    @property
    def features_add(self):
        return set(self.rules['features_add'])

    @property
    def features_remove(self):
        return set(self.rules['features_remove'])

    @property
    def features(self):
        features = self.features_default.union(self.features_add)
        return features.difference(self.features_remove)

    def display(self):
        return int(self) or self.is_favored or self.is_supernal or self.is_caste or self.is_asset

    def specialize(self, key=None, rating=None):
        if not key:
            raise ValueError("What will be your specialty?")
        key = dramatic_capitalize(key)
        if not rating:
            rating = 1
        try:
            rating = int(rating)
        except ValueError:
            raise ValueError("Enter a number!")
        if rating < 1:
            self.specialties.filter(key=key).delete()
        else:
            specialty, created = self.specialties.get_or_create(key=key)
            specialty.rating = rating
            specialty.save()


    def sheet_format(self, width=23, no_favored=False, fill_char='.', colors=None):
        if not colors:
            colors = {'statname': 'n', 'statfill': 'n', 'statdot': 'n'}
        display_name = ANSIString('{%s%s{n' % (colors['statname'], self))
        if self.is_supernal:
            fav_dot = ANSIString('{r*{n')
        elif self.is_caste:
            fav_dot = ANSIString('{r+{n')
        elif self.is_favored or self.is_asset:
            fav_dot = ANSIString('{r-{n')
        else:
            fav_dot = ANSIString(' ')
        if not no_favored:
            display_name = fav_dot + display_name
        if self.rating > width - len(display_name) - 1:
            dot_display = ANSIString('{%s%s{n' % (colors['statdot'], self.rating))
        else:
            dot_display = ANSIString('{%s%s{n' % (colors['statdot'], '*' * int(self)))
        fill_length = width - len(display_name) - len(dot_display)
        fill = ANSIString('{%s%s{n' % (colors['statfill'], fill_char * fill_length))
        return display_name + fill + dot_display


class Specialty(models.Model):
    stat = models.ForeignKey('storyteller.CharacterStat', null=True, related_name='specialties')
    custom = models.ForeignKey('storyteller.CharacterCustom', null=True, related_name='specialties')
    key = models.CharField(max_length=40, db_index=True)
    rating = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = (("stat", "key"), ('custom', 'key'),)

    def __str__(self):
        parent = self.stat or self.custom
        return '%s/%s' % (parent, self.key)

    def __int__(self):
        return self.rating

    def sheet_format(self, width=23, fill_char='.', colors=None):
        if not colors:
            colors = {'statname': 'n', 'statfill': 'n', 'statdot': 'n'}
        display_name = ANSIString('{%s%s{n' % (colors['statname'], self))
        if self.rating > width - len(display_name) - 1:
            dot_display = ANSIString('{%s%s{n' % (colors['statdot'], self.rating))
        else:
            dot_display = ANSIString('{%s%s{n' % (colors['statdot'], '*' * self.rating))
        fill_length = width - len(display_name) - len(dot_display)
        fill = ANSIString('{%s%s{n' % (colors['statfill'], fill_char * fill_length))
        return display_name + fill + dot_display

class CustomKind(models.Model):
    key = models.CharField(max_length=30, db_index=True)
    game = models.ForeignKey('storyteller.Game', related_name='custom_stats')

    class Meta:
        unique_together = (("key", 'game'),)


class CustomStat(models.Model):
    kind = models.ForeignKey('storyteller.CustomKind', related_name='custom_stats')
    key = models.CharField(max_length=40, db_index=True)

    class Meta:
        unique_together = (("key", 'kind'),)

    def __str__(self):
        return self.key


class CharacterCustom(models.Model):
    character = models.ForeignKey('storyteller.CharacterTemplate', related_name='customs')
    stat = models.ForeignKey('storyteller.CustomStat', related_name='characters')
    rating = models.SmallIntegerField(default=0, db_index=True)
    features = ({'special', 'dot', 'roll'})

    def __str__(self):
        return str(self.stat)

    def __int__(self):
        return self.rating

    def display(self):
        return self.rating

    @property
    def is_favored(self):
        return False

    @property
    def is_supernal(self):
        return False

    @property
    def is_caste(self):
        return False

    @property
    def game(self):
        return self.stat.kind.game

    @property
    def rules(self):
        return self.game.rules['custom'][self.stat.kind.key]

    def sheet_format(self, width=23, no_favored=False, fill_char='.', colors=None):
        if not colors:
            colors = {'statname': 'n', 'statfill': 'n', 'statdot': 'n'}
        display_name = ANSIString('{%s%s{n' % (colors['statname'], self))
        if self.is_supernal:
            fav_dot = ANSIString('{r*{n')
        elif self.is_caste:
            fav_dot = ANSIString('{r+{n')
        elif self.is_favored:
            fav_dot = ANSIString('{r-{n')
        else:
            fav_dot = ANSIString(' ')
        if not no_favored:
            display_name = fav_dot + display_name
        if self.rating > width - len(display_name) - 1:
            dot_display = ANSIString('{%s%s{n' % (colors['statdot'], self.rating))
        else:
            dot_display = ANSIString('{%s%s{n' % (colors['statdot'], '*' * self.rating))
        fill_length = width - len(display_name) - len(dot_display)
        fill = ANSIString('{%s%s{n' % (colors['statfill'], fill_char * fill_length))
        return display_name + fill + dot_display


class PowerKind(models.Model):
    game = models.ForeignKey('storyteller.Game', related_name='powers')
    key = models.CharField(max_length=30, db_index=True)

    class Meta:
        unique_together = (("key", "game", ),)

    def __str__(self):
        return self.key

class PowerCategory(models.Model):
    kind = models.ForeignKey('storyteller.PowerKind', related_name='categories')
    key = models.CharField(max_length=255, db_index=True)

    class Meta:
        unique_together = (("key", 'kind'),)

    def __str__(self):
        return self.key

class Power(models.Model):
    category = models.ForeignKey('storyteller.PowerCategory', related_name='powers')
    key = models.CharField(max_length=255, db_index=True)

    class Meta:
        unique_together = (("category", 'key'),)


class CharacterPower(models.Model):
    character = models.ForeignKey('storyteller.CharacterTemplate', related_name='powers')
    power = models.ForeignKey('storyteller.Power', related_name='characters')
    rating = models.SmallIntegerField(default=0, db_index=True)
    is_control = models.BooleanField(default=False)

    class Meta:
        unique_together = (("character", "power",),)

    def __str__(self):
        return self.power.key

    def __int__(self):
        return self.rating

    @property
    def game(self):
        return self.stat.kind.game

    @property
    def rules(self):
        return self.character.rules['powers'][self.power.kind.key]

    def sheet_format(self, width=23, colors=None, mode='stat'):
        if mode == 'stat':
            return self.stat_format(width, colors)
        if mode == 'word':
            return self.word_format(width, colors)

    def word_format(self, width, colors):
        if self.rating > 1:
            return '%s (%s)' % (self, self.rating)
        else:
            return str(self)

    def stat_format(self, width, colors):
        pass


class Pool(models.Model):
    game = models.ForeignKey('storyteller.Game', related_name='pools')
    key = models.CharField(max_length=70, db_index=True)

    class Meta:
        unique_together = (("game", "key",),)


class CharacterPool(models.Model):
    character = models.ForeignKey('storyteller.CharacterTemplate', related_name='pools')
    pool = models.ForeignKey('storyteller.Pool', related_name='pools')
    points = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = (("character", "pool",),)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.points

    @property
    def game(self):
        return self.pool.game

    @property
    def rules(self):
        return self.game.rules['pools'][self.pool.key]

    @property
    def name(self):
        return self.rules['name']

    @property
    def category(self):
        return self.rules['category']

    @property
    def list_order(self):
        return self.rules['list_order']

    @property
    def _func(self):
        return self.character.pool_dict.get(self.pool.key, None)

    @property
    def max(self):
        try:
            value = self._func(self.character.character.story)
            return value
        except TypeError:
            return 0

    @property
    def available(self):
        return min(self._points, self.max - self.total_commit)

    @property
    def total_commit(self):
        return sum(self._commits.values())

    def commit(self, reason=None, amount=None):
        if not reason:
            raise ValueError("Reason is empty!")
        try:
            value = int(amount)
        except ValueError:
            raise ValueError("Amount must be an integer.")
        if value < 1:
            raise ValueError("Commitments must be positive integers.")
        if value > self.available:
            raise ValueError("Cannot commit more than you have!")
        if reason.lower() in [key.lower() for key in self._commits.keys()]:
            raise ValueError("Commitments must be unique.")
        self._commits[reason] = value
        self.points -= value
        self.save(update_fields=['points'])
        return True

    def uncommit(self, reason=None):
        if not reason:
            raise ValueError("Reason is empty!")
        find_reason = partial_match(reason, self._commits.keys())
        if not find_reason:
            raise ValueError("Commitment not found.")
        self._commits.pop(find_reason)
        return True

    def fill(self, amount=None):
        try:
            value = int(amount)
        except ValueError:
            raise ValueError("Values must be integers.")
        if not value > 0:
            raise ValueError("Values must be positive.")
        self.points = min(self.points + value, self.max - self.total_commit)
        self.save(update_fields=['points'])
        return True

    def drain(self, amount=None):
        try:
            value = int(amount)
        except ValueError:
            raise ValueError("Values must be integers.")
        if not value > 0:
            raise ValueError("Values must be positive.")
        if value > self.points:
            raise ValueError("There aren't that many %s to spend!" % self.unit)
        self.points -= value
        self.save(update_fields=['points'])
        return True

    def refresh_pool(self):
        if self.refresh == 'max':
            self.points = self.max - self.total_commit
            return
        if self.refresh == 'empty':
            self.points = 0
            return

    def sheet_format(self, rjust=None, zfill=2):
        val_string = '%s/%s' % (str(self.points).zfill(zfill), str(self.max).zfill(zfill))
        if rjust:
            return '%s: %s' % (self.name.rjust(rjust), val_string)
        else:
            return '%s: %s' % (self.name, val_string)


class PoolCommits(models.Model):
    pool = models.ForeignKey('storyteller.CharacterPool', related_name='commitments')
    reason = models.CharField(max_length=150)
    amount = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = (("pool", "reason",),)


class MeritKind(models.Model):
    game = models.ForeignKey('storyteller.Game', related_name='merits')
    key = models.CharField(max_length=30, db_index=True)

    class Meta:
        unique_together = (("key", "game", ),)


class MeritCharacter(models.Model):
    character = models.ForeignKey('storyteller.CharacterTemplate', related_name='merits')
    kind = models.ForeignKey('storyteller.MeritKind', related_name='characters')
    key = models.CharField(max_length=120)
    context = models.CharField(max_length=120)
    rating = models.SmallIntegerField(default=0)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = (("character", "key", 'context', 'kind'),)

    def __str__(self):
        if self.context:
            return '%s: %s' % (self.key, self.context)
        else:
            return self.key

    def __int__(self):
        return self.rating

    @property
    def game(self):
        return self.pool.game

    @property
    def rules(self):
        return self.game.rules['merits'][self.pool.key]

    def sheet_format(self, width=23, fill_char='.', colors=None):
        if not colors:
            colors = {'statname': 'n', 'statfill': 'n', 'statdot': 'n'}
        display_name = ANSIString('{%s%s{n' % (colors['statname'], self))
        if self.rating > width - len(display_name) - 1:
            dot_display = ANSIString('{%s%s{n' % (colors['statdot'], self.rating))
        else:
            dot_display = ANSIString('{%s%s{n' % (colors['statdot'], '*' * self.rating))
        fill_length = width - len(display_name) - len(dot_display)
        fill = ANSIString('{%s%s{n' % (colors['statfill'], fill_char * fill_length))
        return display_name + fill + dot_display

class ExpKind(models.Model):
    game = models.ForeignKey('storyteller.Game', related_name='experiences')
    key = models.CharField(max_length=50, db_index=True)

    class Meta:
        unique_together = (("game", "key"),)

    @property
    def rules(self):
        return self.game.rules['experience'][self.key]

    def __str__(self):
        return self.rules['name']

    @property
    def list_order(self):
        return self.rules['list_order']

class ExpLink(models.Model):
    kind = models.ForeignKey('storyteller.ExpKind', related_name='exp_links')
    character = models.ForeignKey('storyteller.CharacterTemplate', related_name='exp_kinds')

    class Meta:
        unique_together = (("kind", "character"),)

    def __str__(self):
        return str(self.kind)

    def sheet_format(self, rjust=None):
        gained = self.gained()
        spent = self.spent()
        val_string = '%s/%i' % (str(int(gained + spent)).rjust(2), gained)
        if rjust:
            return '%s: %s' % (str(self).rjust(rjust), val_string)
        else:
            return '%s: %s' % (self, val_string)

    @property
    def list_order(self):
        return self.kind.list_order

    def spent(self):
        spent = self.entries.filter(amount__lt=0).aggregate(spent=Sum('amount'))
        num = spent['spent']
        if num is None:
            return Decimal(0.0)
        return num

    def gained(self):
        gained = self.entries.filter(amount__gt=0).aggregate(gained=Sum('amount'))
        num = gained['gained']
        if num is None:
            return Decimal(0.0)
        return num

    def available(self):
        available = self.entries.aggregate(available=Sum('amount'))
        num = available['available']
        if num is None:
            return Decimal(0.0)
        return num

class Exp(models.Model):
    link = models.ForeignKey('storyteller.ExpLink', related_name='entries')
    amount = models.DecimalField(default=0.0, db_index=True)
    reason = models.CharField(max_length=200)
    source = models.ForeignKey('communications.ObjectStub', null=True)
    date_awarded = models.DateTimeField()

    def __int__(self):
        return int(self.amount)

    def __str__(self):
        return self.reason