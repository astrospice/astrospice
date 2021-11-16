import spiceypy


class Body:
    """
    An individual body.

    Parameters
    ----------
    body : `int`, `str`
        Either the body ID code (integer) or the body name (string).
    """
    def __init__(self, body):
        if isinstance(body, int):
            self.id = body
        elif isinstance(body, str):
            self.name = body
        else:
            raise ValueError('body must be an int or str')

    def __repr__(self):
        return f'{super().__repr__()}, name={self.name}, id={self.id}'

    def __eq__(self, other):
        return isinstance(other, Body) and other.id == self.id

    @property
    def id(self):
        """Body ID code."""
        return self._id

    @id.setter
    def id(self, id):
        self._id = id
        try:
            self._name = spiceypy.bodc2n(id)
        except spiceytypes.SpiceyError:
            raise ValueError(f'id "{id}" not known by SPICE')

    @property
    def name(self):
        """Body name."""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        try:
            self._id = spiceypy.bodn2c(name)
        except spiceytypes.SpiceyError:
            raise ValueError(f'Body name "{name}" not known by SPICE')
