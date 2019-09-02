from future.utils import with_metaclass
from evennia.typeclasses.models import TypeclassBase
from modules.areas.models import AreaDB


class DefaultArea(with_metaclass(TypeclassBase, AreaDB)):
    pass