class UniqueIdentifierError(Exception):

    _value = None

    def __init__(self, value):
        self.value = "The value for {} must be unique and was not.".format(value)

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return self.__repr__()

    def get_value(self):
        return self._value

    def set_value(self, v):
        self._value = v

    def del_value(self):
        self._value = None

    value = property(get_value, set_value, del_value)
