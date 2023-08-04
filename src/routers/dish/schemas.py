import re
from uuid import UUID

from pydantic import BaseModel, ConfigDict, constr, field_validator


class DishBaseModel(BaseModel):
    """Base model for inputs"""

    title: str
    description: str
    price: constr(strip_whitespace=True)  # type: ignore

    @field_validator('price')
    def validate_price(self, value):
        """Validate price for 2 decimals"""
        pattern = r'^(?!0[0-9])[0-9]+\.[0-9]{2}$'
        if not re.match(pattern, value):
            raise ValueError('invalid float number')
        return value

    model_config = ConfigDict(from_attributes=True)


class Dish(DishBaseModel):
    """Base model for outputs"""

    id: UUID
