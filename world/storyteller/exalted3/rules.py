from __future__ import unicode_literals


# The ANCESTORS dictionary contains the top-level settings that will be used for Storyteller data. These ensure that
# every stat, pool, etc, will have all of the necessary properties.

ANCESTORS = {
    'stat': {
        'save_fields': ('_rating', '_favored', '_supernal', '_specialties')
    },
    'custom': {

    },
    'merit': {
        '_rating': 0,
        '_descripion': None,
        '_notes': None,
        'save_fields': ('_rating', '_description', '_notes')
    },
    'power': {
        '_rating': 1,
        'save_fields': ('_rating')
    },
    'pool': {

    },
    'template': {
        'charm_type': 'Unset',

    }

}

# PARENTs are the second level of settings used for Storyteller data. These 'inherit' from the 'ANCESTORS' and serve
# the same purpose, one level down. The 'parent' key of a STAT, POOL, or TEMPLATE is used to target this dictionary.

PARENTS = {
    'stat': {
        'physical': {
            'kind': 'Attribute',
            'category': 'Physical',
            'features_default': ('dot', 'roll', 'special'),
        },
        'social': {
            'kind': 'Attribute',
            'category': 'Social',
            'features_default': ('dot', 'roll', 'special'),
        },
        'mental': {
            'kind': 'Attribute',
            'category': 'Mental',
            'features_default': ('dot', 'roll', 'special'),
        },
        'ability': {
            'kind': 'Ability',
            'features_default': ('dot', 'roll', 'favor', 'supernal', 'special'),
            '_rating': 0,
        },
        'advantage': {
            'kind': 'Advantage',
            'features_default': ('dot', 'roll'),
        },
    },
    'custom': {
        'craft': {
            'kind': 'Ability',
            'category': 'Craft',
        },
        'style': {
            'kind': 'Ability',
            'category': 'Style',
        }
    },
    'merit': {
        'merit': {
            'kind': 'Merit',
        },
        'flaw': {
            'kind': 'Flaw',
        },
        'pact': {
            'kind': 'Pact',
        }
    },
    'pool': {
        'essence': {

        },
        'limit': {

        }
    },
    'template': {
        'exalt': {

        }
    },
}

# And finally, the Stats for Exalted 3rd Edition.

STATS = {
    # attributes!
    'strength': {
        'name': 'Strength',
        'parent': 'physical',
        'list_order': 1,
    },
    'dexterity': {
        'name': 'Dexterity',
        'parent': 'physical',
        'list_order': 2,
    },
    'stamina': {
        'name': 'Stamina',
        'parent': 'physical',
        'list_order': 3,
    },
    'charisma': {
        'name': 'Charisma',
        'parent': 'social',
        'list_order': 4,
    },
    'manipulation': {
        'name': 'Manipulation',
        'parent': 'social',
        'list_order': 5,
    },
    'appearance': {
        'name': 'Appearance',
        'parent': 'social',
        'list_order': 6,
    },
    'perception': {
        'name': 'Perception',
        'parent': 'mental',
        'list_order': 7,
    },
    'intelligence': {
        'name': 'Intelligence',
        'parent': 'mental',
        'list_order': 8,
    },
    'wits': {
        'name': 'Wits',
        'parent': 'mental',
        'list_order': 9,
    },

    #Abilities!
    'archery': {
        'name': 'Archery',
        'parent': 'ability',
        'list_order': 10,
    },
    'brawl': {
        'name': 'Brawl',
        'parent': 'ability',
        'list_order': 15,
    },
    'melee': {
        'name': 'Melee',
        'parent': 'ability',
        'list_order': 20,
    },
    'war': {
        'name': 'War',
        'parent': 'ability',
        'list_order': 25,
    },
    'thrown': {
        'name': 'Thrown',
        'parent': 'ability',
        'list_order': 30,
    },
    'bureaucracy': {
        'name': 'Bureaucracy',
        'parent': 'ability',
        'list_order': 35,
    },
    'linguistics': {
        'name': 'Linguistics',
        'parent': 'ability',
        'list_order': 40,
    },
    'ride': {
        'name': 'Ride',
        'parent': 'ability',
        'list_order': 45,
    },
    'sail': {
        'name': 'Sail',
        'parent': 'ability',
        'list_order': 50,
    },
    'socialize': {
        'name': 'Socialize',
        'parent': 'ability',
        'list_order': 55,

    },
    'athletics': {
        'name': 'Athletics',
        'parent': 'ability',
        'list_order': 60,
    },
    'awareness': {
        'name': 'Awareness',
        'parent': 'ability',
        'list_order': 65,
    },
    'dodge': {
        'name': 'Dodge',
        'parent': 'ability',
        'list_order': 70,
    },
    'larceny': {
        'name': 'Larceny',
        'parent': 'ability',
        'list_order': 75,
    },
    'stealth': {
        'name': 'Stealth',
        'parent': 'ability',
        'list_order': 80,
    },
    'craft': {
        'name': 'Craft',
        'parent': 'ability',
        'list_order': 85,
        'features_remove': ('dot', 'roll')
    },
    'investigation': {
        'name': 'Investigation',
        'parent': 'ability',
        'list_order': 90,
    },
    'lore': {
        'name': 'Lore',
        'parent': 'ability',
        'list_order': 95,
    },
    'medicine': {
        'name': 'Medicine',
        'parent': 'ability',
        'list_order': 100,
    },
    'occult': {
        'name': 'Occult',
        'parent': 'ability',
        'list_order': 105,
    },
    'integrity': {
        'name': 'Integrity',
        'parent': 'ability',
        'list_order': 110,
    },
    'performance': {
        'name': 'Performance',
        'parent': 'ability',
        'list_order': 115,
    },
    'presence': {
        'name': 'Presence',
        'parent': 'ability',
        'list_order': 120,
    },
    'resistance': {
        'name': 'Resistance',
        'parent': 'ability',
        'list_order': 125,
    },
    'survival': {
        'name': 'Survival',
        'parent': 'ability',
        'list_order': 130,
    },
    'martial_arts': {
        'name': 'Martial Arts',
        'parent': 'ability',
        'list_order': 13,
        'features_remove': ('dot', 'roll', 'favor')
    },

    # Advantages
    'essence': {
        'name': 'Essence',
        'parent': 'advantage',
    },
    'willpower': {
        'name': 'Willpower',
        'parent': 'advantage',
        '_rating': 5,
    }

}

POOLS = {
    'personal': {
        'name': 'Personal',
        'parent': 'essence',
        'unit': 'Motes of Personal Essence',
    },
    'peripheral': {
        'name': 'Peripheral',
        'parent': 'essence',
        'unit': 'Motes of Peripheral Essence',
    },
    'willpower': {
        'name': 'Willpower',
        'parent': 'essence',
        'unit': 'Points of Temporary Willpower',
    },
    'limit': {
        'name': 'Limit',
        'unit': 'Points of Limit',
        'parent': 'limit',
        'refresh': 'empty'
    },

}


def universal_willpower(character):
    return character.ndb.stats_dict['willpower']


def solar_personal(character):
    return character.ndb.stats_dict['essence']*3 + 10


def solar_peripheral(character):
    return character.ndb.stats_dict['essence']*7 + 26


def solar_limit(character):
    return 10


def abyssal_personal(character):
    return solar_personal(character)


def abyssal_peripheral(character):
    return solar_peripheral(character)


def abyssal_resonance(character):
    return 10


def terrestrial_personal(character):
    return character.ndb.stats_dict['essence'] + 11


def terrestrial_peripheral(character):
    return character.ndb.stats_dict['essence']*4 + 23


def terrestrial_limit(character):
    return 10


def lunar_personal(character):
    return character.ndb.stats_dict['essence'] + 15


def lunar_peripheral(character):
    return character.ndb.stats_dict['essence']*4 + 34


def lunar_limit(character):
    return 10


def sidereal_personal(character):
    return character.ndb.stats_dict['essence']*2 + 9


def sidereal_peripheral(character):
    return character.ndb.stats_dict['essence']*6 + 25


def sidereal_limit(character):
    return 10


def liminal_personal(character):
    return character.ndb.stats_dict['essence']*3 + 10


def liminal_peripheral(character):
    return character.ndb.stats_dict['essence']*4 + 23


def liminal_limit(character):
    return 10


TEMPLATES = {
    'mortal': {
        'name': 'Mortal',
        'parent': 'exalt',
        'list_order': 0,
        'pools': {'willpower': universal_willpower}
    },
    'solar': {
        'name': 'Solar',
        'parent': 'exalt',
        'list_order': 5,
        'pools': {'personal': solar_personal, 'peripheral': solar_peripheral, 'willpower': universal_willpower,
                  'limit': solar_limit},
        'charm_type': 'solar_charm',
        'info_defaults': {'Caste': None},
        'info_choices': {'Caste': ('Dawn', 'Zenith', 'Eclipse', 'Twilight', 'Night')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste',),
    },
    'abyssal': {
        'name': 'Abyssal',
        'parent': 'exalt',
        'list_order': 10,
        'pools': {'personal': abyssal_personal, 'peripheral': abyssal_peripheral, 'willpower': universal_willpower,
                  'resonance': abyssal_resonance},
        'charm_type': 'Abyssal',
        'info_defaults': {'Caste': None},
        'info_choices': {'Caste': ('Dusk', 'Midnight', 'Moonshadow', 'Daybreak', 'Day')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste',),
    },
    'lunar': {
        'name': 'Lunar',
        'parent': 'exalt',
        'list_order': 15,
        'pools': {'personal': lunar_personal, 'peripheral': lunar_peripheral, 'willpower': universal_willpower,
                  'limit': lunar_limit},
        'charm_type': 'Lunar',
        'info_defaults': {'Caste': None},
        'info_choices': {'Caste': ('Full Moon', 'Changing Moon', 'No Moon')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste',),
    },
    'terrestrial': {
        'name': 'Terrestrial',
        'parent': 'exalt',
        'list_order': 20,
        'pools': {'personal': terrestrial_personal, 'peripheral': terrestrial_peripheral,
                  'willpower': universal_willpower, 'limit': terrestrial_limit},
        'charm_type': 'Terrestrial',
        'info_defaults': {'Aspect': None},
        'info_choices': {'Aspect': ('Fire', 'Air', 'Water', 'Wood', 'Earth')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Aspect',),
    },
    'sidereal': {
        'name': 'Sidereal',
        'parent': 'exalt',
        'list_order': 25,
        'pools': {'personal': sidereal_personal, 'peripheral': sidereal_peripheral, 'willpower': universal_willpower,
                  'limit': sidereal_limit},
        'charm_type': 'Sidereal',
        'info_defaults': {'Caste': None},
        'info_choices': {'Caste': ('Journeys', 'Battles', 'Serenity', 'Secrets', 'Endings')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste',),
    },
    'liminimal': {
        'name': 'Liminal',
        'parent': 'exalt',
        'list_order': 30,
        'pools': {'personal': liminal_personal, 'peripheral': liminal_peripheral, 'willpower': universal_willpower,
                  'limit': liminal_limit},
        'charm_type': 'Liminal',
        'info_defaults': {'Aspect': None},
        'info_choices': {'Aspect': ('Blood', 'Breath', 'Flesh', 'Marrow', 'Soil')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Aspect',),
    },
}