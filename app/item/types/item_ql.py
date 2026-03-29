from typing import Optional

import strawberry



@strawberry.type
class ItemQL:
    id: strawberry.ID
    name: str
    description: Optional[str]