# Create a Pydantic model for the version information
from pydantic import BaseModel

class VersionResponse(BaseModel):
    tag: str
    commit: str