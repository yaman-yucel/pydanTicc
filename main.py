from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict
from rich import print as rprint


class User(BaseModel):
    id: int
    name: str = "Jane Doe"

    model_config = ConfigDict(strict=True, str_max_length=10, extra="allow")


User1 = User(id=5, location=100)  # extra is location
rprint(User.model_json_schema())
rprint(User1.model_dump_json())
rprint(User1.model_copy(deep=True))
rprint(User1.__pydantic_extra__)


class SomeConfig(BaseModel):
    config1: str | None = None
    model_config = ConfigDict(extra="forbid", revalidate_instances="always")  # extra forbid allow ignore # 'revalidate_instances = always never, sub only


# rprint(SomeConfig(config1="config", extra=False)) ERROR

# Nested Models OK


class Foo(BaseModel):
    count: int
    size: float | None = None


class Bar(BaseModel):
    apple: str = "x"
    banana: str = "y"


class Spam(BaseModel):
    foo: Foo
    bars: list[Bar]


m = Spam(foo={"count": 4}, bars=[{"apple": "x1"}, {"apple": "x2"}])
rprint(m)
rprint(Spam.model_json_schema())

# No validation
a = Spam.model_construct(foo=Foo.model_construct(count=5, size="asd"), bars=[Bar.model_construct(apple=5, banana=3)])  # wow, what can go wrong, just never use
rprint(a)
a.foo.count = "as"  # also modifiable
rprint(a)


class DataModel(BaseModel):
    number: int


class Response[Data1, Data2, Data3](BaseModel):  # Auto creates a data type and you can pass to model
    data1: Data1
    data2: Data2
    data3: Data3


resp = Response[int, float, str](data1=1, data2=3.14, data3="hi")  # does not write type to json schema
rprint(resp)
rprint(Response.model_json_schema())
rprint(resp.model_dump())
resp2 = Response[list[int], dict[str, str], Foo](data1=[1, 2, 3, 4, 5], data2={"a": "1", "b": "2"}, data3=Foo(count=5, size=1.1))
rprint(resp2)
rprint(resp2.model_dump())

# Does not work
# class BaseClass[TypeX](BaseModel):
#     X: TypeX

# class ChildClass[BaseClass[TypeX]](BaseClass):
#     pass
# Inherit from Generic, use the 3.9+ way

TypeX = TypeVar("TypeX")


class BaseClass(BaseModel, Generic[TypeX]):
    X: TypeX


class ChildClass(BaseClass[TypeX], Generic[TypeX]):  # send the class with the new syntax
    pass


child = ChildClass[int](X=1)
rprint(child.model_dump())
