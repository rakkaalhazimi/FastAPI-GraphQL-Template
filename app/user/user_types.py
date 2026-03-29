from dataclasses import dataclass, fields
from typing import Optional

import strawberry


@dataclass
class UserPayload:
    id: int
    username: str
    email: str
    
    @classmethod
    def from_dict(cls, data):
        valid_keys = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in valid_keys})


@strawberry.type
class UserQL:
    id: strawberry.ID
    username: Optional[str] = None
    email: Optional[str] = None