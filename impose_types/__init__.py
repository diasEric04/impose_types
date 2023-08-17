# flake8: noqa

from modules.classes.facades import DecoratorFacade
from modules.classes.factories import DecoratorFactory

decorator_facade = DecoratorFacade(DecoratorFactory, 'impose_types')
impose_types = decorator_facade.decorator
