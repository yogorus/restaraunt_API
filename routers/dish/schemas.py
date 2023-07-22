import re
from pydantic import BaseModel, constr, validator
from uuid import UUID

class SubmenuBaseModel(BaseModel):
    title: str
    description: str
    price: constr(strip_whitespace=True)  # type: ignore

    @validator('price')
    def validate_price(cls, value):
        pattern = r'(?!0[0-9])[0-9]+\.[0-9]{2}'
        if not re.match(pattern, value):
            raise ValueError("invalid float number")
        return value