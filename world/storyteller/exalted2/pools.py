from world.storyteller.pools import Pool as OldPool, WillpowerPool as OldWillpowerPool

# Define main types.


class Pool(OldPool):
    game_category = 'Exalted2'


class WillpowerPool(OldWillpowerPool):
    game_category = 'Exalted2'
    list_order = 20

class Virtue(Pool):
    main_category = 'Channel'


class EssencePool(Pool):
    component_name = 'Mote'
    component_plural = 'Motes'
    value_name = 'Essence'


class PersonalPool(EssencePool):
    value_name = 'Personal Essence'
    list_order = 0

class PeripheralPool(EssencePool):
    value_name = 'Peripheral Essence'
    list_order = 5

class ExtendedPool(PeripheralPool):
    value_name = 'Extended Peripheral Essence'
    list_order = 10

class OverdrivePool(EssencePool):
    value_name = 'Overdrive Peripheral Essence'
    list_order = 15

    def calculate_overdrive(self, owner):
        pass

    def initialize_max(self, owner):
        pool_calc = self.calculate_overdrive(owner)
        return sorted([0,pool_calc,25])[1]

class Limit(Pool):
    value_name = 'Limit'
    main_category = 'Track'

    def initialize_max(self, owner):
        return 10

# Solars


class SolarPersonal(PersonalPool):

    def initialize_max(self, owner):
        return 0

class SolarPeripheral(PeripheralPool):

    def initialize_max(self, owner):
        return 0

class SolarExtended(ExtendedPool):

    def initialize_max(self, owner):
        return 0

class SolarOverdrive(OverdrivePool):

    def initialize_max(self, owner):
        return 0

# Abyssals


class AbyssalPersonal(SolarPersonal):
    pass


class AbyssalPeripheral(SolarPeripheral):
    pass


class AbyssalExtended(ExtendedPool):
    pass


class AbyssalOverdrive(OverdrivePool):
    pass


class Resonance(Limit):
    base_name = 'Resonance'

# Infernals


class InfernalPersonal(SolarPersonal):
    pass


class InfernalPeripheral(SolarPeripheral):
    pass


class InfernalExtended(ExtendedPool):
    pass


class InfernalOverdrive(OverdrivePool):
    pass