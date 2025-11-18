from pydantic import BaseModel
from typing import List

class DossiersDetailsData(BaseModel):
    dossier_ids: List[int]    