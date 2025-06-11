from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from rich import print as rprint


class SomeData(BaseModel):
    hi: str = "stringgg"


class Response[Data1, Data2, Data3](BaseModel):  # Auto creates a data type and you can pass to model
    data1: Data1
    data2: Data2
    data3: Data3


resp = Response[int, float, str](data1=1, data2=3.14, data3="hi")  # does not write type to json schema
rprint(resp)
rprint(Response.model_json_schema())
rprint(resp.model_dump())
resp2 = Response[list[int], dict[str, str], SomeData](data1=[1, 2, 3, 4, 5], data2={"a": "1", "b": "2"}, data3=SomeData(hi="hi"))
rprint(resp2)
rprint(resp2.model_dump())

# Does not work
# class BaseClass[TypeX](BaseModel):
#     X: TypeX

# class ChildClass[BaseClass[TypeX]](BaseClass):
#     pass
# Inherit from Generic, use the 3.9+ way

TypeX = TypeVar("TypeX")
TypeY = TypeVar("TypeY")
TypeZ = TypeVar("TypeZ")


class BaseClass(BaseModel, Generic[TypeX, TypeY]):
    x: TypeX
    y: TypeY


class ChildClass(BaseClass[TypeX, TypeY], Generic[TypeX, TypeY, TypeZ]):  # send the class with the new syntax
    z: TypeZ

    @classmethod
    def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:  # rename the class according to types
        return f"{params[0].__name__.title()}_{params[1].__name__.title()}_{params[2].__name__.title()}_ChildClass"


child = ChildClass[str, int, int](x="1", y=2, z=3)
rprint(child.model_dump())
rprint(child)
