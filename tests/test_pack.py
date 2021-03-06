from typing import Optional
from unittest import TestCase

from validate_it import schema, Options, pack_value, ValidationError, to_dict


@schema
class A:
    a: int


@schema
class OptionalAutoPackDisabled:
    a: Optional[A]


@schema
class OptionalAutoPackEnabled:
    a: Optional[A] = Options(auto_pack=True, packer=pack_value)


class PackTestCase(TestCase):
    def test_pack(self):
        with self.assertRaises(ValidationError):
            OptionalAutoPackDisabled(a={'a': 1})

        OptionalAutoPackDisabled(a=A(a=1))
        OptionalAutoPackDisabled(a=None)
        OptionalAutoPackDisabled()

        OptionalAutoPackEnabled(a={'a': 1})
        OptionalAutoPackEnabled(a=None)
        OptionalAutoPackEnabled()

    def test_unpack(self):
        assert {'a': {'a': 1}} == to_dict(OptionalAutoPackDisabled(a=A(a=1)))
        assert {'a': {'a': 1}} == to_dict(OptionalAutoPackEnabled(a={'a': 1}))

        assert {} == to_dict(OptionalAutoPackEnabled(a=None))
        assert {} == to_dict(OptionalAutoPackEnabled())
