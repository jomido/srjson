
class Token(object):

    class lookup(object):
        pass

    class action(object):
        pass

    class string(object):
        pass

    def __init__(self, value, type):

        self.value = value
        self.type = type

    def __str__(self):

        return self.value

    def __repr__(self):

        return "Token<'{}', {}>".format(self.value, self.type.__name__)
