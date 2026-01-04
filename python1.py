from typing import TypedDict


class User(TypedDict):
    id: int
    name: str
    active: bool


user: User = {
    "id": 1,
    "name": "Rajneesh",
    "active": True
}


print(user)

