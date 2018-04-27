import codecs, re

def mxp(text="", command="", hints=""):
    if text:
        return "|lc%s|lt%s|le" % (command, text)
    else:
        return "|lc%s|lt%s|le" % (command, command)

def re_color(match):
    return match.group('text')
    codes_text = match.group('codes')
    text = match.group('text')
    if not len(codes_text):
        return text

    codes = re.match(r'(?P<fg>.+?)(?:!(?P<bg>.+?))?',codes_text)

    if '<' in codes.group('fg'):
        pass

def re_pueblo(match):
    if match.group('command').startswith('send'):
        find = re.match(r'(?is)(?P<pre>send \\"(?P<com>.+?)\\)"', match.group('command'))
        return mxp(text=match.group('text'), command=find.group('com'))

    if match.group('command').startswith('a'):
        find = re.match(r'(?is)(?P<pre>a XCH_CMD=\\"(?P<com>.+?)\\)"', match.group('command'))
        return mxp(text=match.group('text'), command=find.group('com'))

    return match.group('text')

def re_newlines(match):
    return '\n'

def re_tabs(match):
    return '\t'

def process_penntext(text):
    if not len(text):
        return text
    text = re.sub(r'(?s)(?P<start>\002p(?P<command>.+?)\003)(?P<text>.+?)(?P<end>\002p\/\003)',re_pueblo,text)
    text = re.sub(r'(?s)(?P<start>\002c(?P<codes>.+?)\003)(?P<text>.+?)(?P<end>\002c\/\003)',re_color,text)
    text = re.sub(r'(?is)(?P<find>%r)',re_newlines,text)
    text = re.sub(r'(?is)(?P<find>%t)', re_tabs, text)
    return text


class read_penn(object):

    __slots__ = ['outdb', 'mush_data']

    def __init__(self, file):
        self.outdb = codecs.open(file, 'r', 'iso-8859-1')
        self.mush_data = {}
        self.parse_file()

    def parse_file(self):
        all_lines = self.outdb.readlines()
        del all_lines[-1]
        all_lines = [line.strip(u'\n') for line in all_lines]
        start_index = all_lines.index('!0')
        all_lines = all_lines[start_index:]
        all_dblines = list()
        for line_num, line_text in enumerate(all_lines):
            if re.match(r'\!\d+$', line_text):
                all_dblines.append(line_num)
        all_dblines = sorted(all_dblines)

        object_dict = dict()

        for count, entry in enumerate(all_dblines):

            dbref = all_lines[entry].replace(u'!', u'#')
            start_line = entry + 1
            try:
                end_line = all_dblines[count + 1]
            except IndexError:
                end_line = None

            object_dict[dbref] = all_lines[start_line:end_line]

        dbref_sort = sorted(object_dict.keys(), key=lambda dbref: int(dbref.strip('#')))

        for dbref in dbref_sort:
            self.parse_object(dbref, object_dict[dbref])


    def parse_object(self, dbref, lines):
        object_dbref = dbref
        object_name = None
        object_type = None
        object_parent = None
        object_location = None
        object_objid = None
        object_created = None
        object_exits = None
        object_owner = None
        object_flags = None
        object_powers = None

        attribute_start = list()
        for count, line in enumerate(lines):
            if line.startswith(u'attrcount '):
                attribute_start.append(count)

        attribute_start = attribute_start[0]

        main_lines = lines[:attribute_start]
        attribute_lines = lines[attribute_start:]

        for line in main_lines:
            subject, entry = line.split(u' ', 1)
            entry = entry.strip(u'"')

            if subject == u'name':
                object_name = entry
            if subject == u'location':
                object_location = entry
            if subject == u'exits':
                object_exits = entry
            if subject == u'parent':
                object_parent = entry
            if subject == u'type':
                object_type = int(entry)
            if subject == u'owner':
                object_owner = entry
            if subject == u'created':
                object_created = entry
                object_objid = u'%s:%s' % (object_dbref, entry)
            if subject == u'flags':
                object_flags = entry
            if subject == u'powers':
                object_powers = entry

        attributes = self.parse_attributes(attribute_lines)

        self.mush_data[object_dbref] = {u'name': object_name, u'type': object_type, u'location': object_location,
                                      u'parent': object_parent, u'objid': object_objid, u'created': object_created,
                                      u'exits': object_exits, u'owner': object_owner, u'flags': object_flags,
                                        u'attributes': attributes, u'powers': object_powers}

    def parse_attributes(self, attribute_lines):

        attributes = {}

        attribute_index = list()
        for count, entry in enumerate(attribute_lines):
            if entry.startswith(u' name "'):
                attribute_index.append(count)
        attribute_index = sorted(attribute_index)

        for count, entry in enumerate(attribute_index):
            name_line, name = attribute_lines[entry].strip(u' ').split(u' ', 1)
            try:
                end_line = attribute_index[count + 1]
            except IndexError:
                end_line = None
            value_lines = attribute_lines[entry+4:end_line]
            value = u'\n'.join(value_lines)
            value = value.strip(u' ')
            value = value.strip(u'\n')
            value_name, value = value.split(u' ', 1)
            value = value.strip(u'"')
            name = name.strip(u'"')
            attributes[name] = process_penntext(value)

        return attributes
