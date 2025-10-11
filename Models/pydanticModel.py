from pydantic import BaseModel,Field,field_validator
from typing import List, Optional,Annotated

class Patient(BaseModel):
    