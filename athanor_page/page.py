from athanor.core.command import AthCommand
from athanor.utils.create import make_speech

class CmdPage(AthCommand):
    key = 'page'
    aliases = ['tell', 'reply']

    def main(self):
        if self.cmdstring.lower() == 'reply':
            self.reply()
            return
        if not self.args:
            self.error("What will you say?")
        if '=' in self.args:
            if not self.lhs:
                self.error("Who will you send to?")
                return
            if not self.lhs:
                self.error("What will you say?")
                return
            targets = list()
            for name in self.lhslist:
                try:
                    found = self.character.search_character(name)
                    targets.append(found)
                except ValueError as err:
                    self.error(str(err))
            text = self.rhs
        else:
            targets = self.character.page.last_to
            text = self.args

        online = [char for char in targets if hasattr(char, 'player')]
        print online
        for char in targets:
            if char not in online:
                self.error("%s is offline." % char)

        if not online:
            self.error("Nobody is listening...")

        online = set(online)

        speech = make_speech(self.character, text, mode='page', targets=online)
        self.character.page.send(online, speech)

    def reply(self):
        if not self.args:
            self.error("What will you say?")
            return
        targets = self.character.page.last_from
        online = [char for char in targets if hasattr(char, 'player')]
        if not online:
            self.error("Nobody is listening...")
            return

        speech = make_speech(self.character, self.args, mode='page', targets=online)
        online = set(online)
        self.character.page.send(online, speech)