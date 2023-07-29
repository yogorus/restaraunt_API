import re
from pydantic import BaseModel, constr, field_validator, ConfigDict
from uuid import UUID


class DishBaseModel(BaseModel):
    title: str
    description: str
    price: constr(strip_whitespace=True)  # type: ignore

    @field_validator("price")
    def validate_price(cls, value):
        pattern = r"^(?!0[0-9])[0-9]+\.[0-9]{2}$"
        if not re.match(pattern, value):
            raise ValueError("invalid float number")
        return value

    model_config = ConfigDict(from_attributes=True)


class Dish(DishBaseModel):
    id: UUID
