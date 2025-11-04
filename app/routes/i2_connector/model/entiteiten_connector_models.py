from pydantic import BaseModel
from typing import List

class EntiteitenDetailsData(BaseModel):
    type: int
    entiteit_ids: List[int]    