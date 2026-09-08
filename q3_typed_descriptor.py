"""
Question 3: Typed data descriptor with runtime type enforcement.

Typed(expected_type) is a data descriptor (defines both __get__ and
__set__) that:
  - stores expected_type at descriptor-creation time.
  - uses __set_name__ to learn the attribute name it was assigned to on
    the owning class, and derives a private storage name from it, so
    multiple Typed attributes on the same class never collide and no
    explicit string key has to be passed in by the user.
  - raises TypeError on assignment if the value isn't an instance of
    expected_type, using the exact message format requested.
"""


class Typed:
    def __init__(self, expected_type: type):
        self.expected_type = expected_type

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"Expected {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        setattr(instance, self.private_name, value)


if __name__ == "__main__":
    class Person:
        name = Typed(str)
        age = Typed(int)

    p = Person()
    p.name = "Christine"
    p.age = 30
    print(p.name, p.age)

    try:
        p.age = "thirty"
    except TypeError as e:
        print(f"Expected failure: {e}")