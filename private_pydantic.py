from datetime import datetime
from random import randint
from typing import Any, ClassVar

from pydantic import BaseModel, PrivateAttr, RootModel
from rich import print as rprint


class TimeAwareModel(BaseModel):
    _processed_at: datetime = PrivateAttr(default_factory=datetime.now)
    _secret_value: str
    regular_value: str

    def model_post_init(self, context: Any) -> None:
        # this could also be done with `default_factory`:
        self._secret_value = randint(1, 5)


m = TimeAwareModel(regular_value="hi")
print(m._processed_at)  # not included in model_json_schema
# > 2032-01-02 03:04:05.000006
print(m._secret_value)  # not included in model_json_schema
# > 3
print(TimeAwareModel.model_json_schema())
print(m)


class myClass(RootModel[list[int]]):
    pass


class DemonstrateClassVar(BaseModel):
    x: ClassVar[int] = 1
    y: myClass
    _z: datetime = PrivateAttr(default_factory=datetime.now)
    _v: str
    regular_value: str

    def model_post_init(self, context: Any) -> None:
        # this could also be done with `default_factory`:
        self._v = randint(1, 5)


rprint(DemonstrateClassVar.model_json_schema())  # classvar, private, post_init not included
d = DemonstrateClassVar(x=5, y=[1, 2, 3, 4, 5], regular_value="hi")  # does not print x, _z, _v
rprint(d)  # prints y, regular
rprint(d.model_dump())  # y, regular as a dict
rprint(d._z)  # prints
rprint(d._v)  # prints 4
rprint(d.x)  # prints 1
rprint(DemonstrateClassVar._z)  # needs to be initialized to write date # ModelPrivateAttr(default=PydanticUndefined, default_factory=<built-in method now of type object at 0x7a04a56a7408>)
rprint(DemonstrateClassVar.x)  # prints 1

# d.x = 5 # error
DemonstrateClassVar.x = 5  # works sets both # regular class variable, carried through the class not instance
rprint(d.x)
rprint(DemonstrateClassVar.x)
