class DecoratorFacade:
    def __init__(self, decorator_factory: type, which_decorator: str):
        self.factory = decorator_factory(which_decorator)
        self.__decorator = self.factory.get_decorator()

    @property
    def decorator(self):
        return self.__decorator
