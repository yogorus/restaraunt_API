"""Pydantic models for dish"""
import re
from uuid import UUID

from pydantic import BaseModel, ConfigDict, constr, field_validator


def validate_price(value):
    """Check if data mathces the decimal pattern"""
    pattern = r'^(?!0[0-9])[0-9]+\.[0-9]{2}$'
    if not re.match(pattern, value):
        raise ValueError('invalid float number')
    return value


class DishBaseModel(BaseModel):
    """Base model for inputs"""

    id: UUID | None = None
    title: str
    description: str
    price: constr(strip_whitespace=True)  # type: ignore

    @field_validator('price')
    def validate_price(cls, value):
        """Validate  Price"""
        return validate_price(value)

    model_config = ConfigDict(from_attributes=True)


class DishForeignKey(DishBaseModel):
    """Dish schema to pass foreign key into it"""

    submenu_id: UUID


class Dish(DishForeignKey):
    """Base model for outputs"""

    id: UUID
