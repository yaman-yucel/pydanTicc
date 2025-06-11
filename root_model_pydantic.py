from typing import Annotated

from pydantic import Field, RootModel, field_validator
from rich import print as rprint

Pets = RootModel[list[str]]  # declares list[str] in a pydantic way, data conversion, validation etc..
PetsByName = RootModel[dict[str, str]]


rprint(Pets(["dog", "cat"]))
rprint(Pets(["dog", "cat"]).model_dump_json())
rprint(Pets.model_validate(["dog", "cat"]))
rprint(Pets.model_json_schema())


rprint(PetsByName({"Otis": "dog", "Milo": "cat"}))
rprint(PetsByName({"Otis": "dog", "Milo": "cat"}).model_dump_json())
rprint(PetsByName.model_validate({"Otis": "dog", "Milo": "cat"}))


# class PetsV2(RootModel[list[str]]):  # never do, write class
#     def __iter__(self):
#         return iter(self.root)

#     def __getitem__(self, item):
#         return self.root[item]


class IntList(RootModel[list[int]]):
    pass


class GreetingMessage(RootModel[str]):
    pass


greet = GreetingMessage.model_validate("hello world")
rprint(greet)


class EvenNumbers(RootModel[list[int]]):  # adds even check functionality over list[int]
    @field_validator("root")
    def check_even(cls, v):
        if any(n % 2 for n in v):
            raise ValueError("All numbers must be even")
        return v


a = EvenNumbers.model_validate([2, 4, 6])  # ✅
# EvenNumbers.model_validate([1, 2])  ❌ Raises ValueError
rprint(a.model_dump_json())
rprint(EvenNumbers.model_json_schema())


class FewInts(RootModel[Annotated[list[int], Field(min_items=2, max_items=4, frozen=True)]]):
    pass


# try:
#     rprint(FewInts.model_validate([1, 2]))
# except Exception as e:
#     rprint(e)

# try:
#     rprint(FewInts.model_validate([1]))
# except Exception as e:
#     rprint(e)

try:
    a = FewInts.model_validate([1, 2, 3])
    a.root.append(5)
    rprint("hi")
except Exception as e:
    rprint(e)
print(FewInts.model_json_schema())
