from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class ProductBase(BaseModel):
    name: str
    description: str
    price: Decimal
    category_id: int
    image_url: str | None = None
    available: bool = True
    inventory: int = Field(default=0, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    category_id: int | None = None
    image_url: str | None = None
    available: bool | None = None
    inventory: int | None = Field(default=None, ge=0)

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)