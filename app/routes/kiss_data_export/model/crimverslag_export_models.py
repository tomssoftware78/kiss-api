from pydantic import BaseModel
from typing import List

class CrimverslagIdList(BaseModel):
    ids: List[int] 