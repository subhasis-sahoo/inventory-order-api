from datetime import datetime
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50,
        description="Product Name"        
    )
    description: str | None = Field(
        default=None,
        min_length=2,
        max_length=400,
        description="Product Description"
    )
    price: float = Field(
        gt=0,
        description="Price must be greater than 0"
    )
    stock: int = Field(
        ge=0,
        description="Stock can not be negative"
    )



class ProductUpdate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50,
        description="Product Name"        
    )
    description: str | None = Field(
        default=None,
        min_length=2,
        max_length=400,
        description="Product Description"
    )
    price: float = Field(
        gt=0,
        description="Price must be greater than 0"
    )
    stock: int = Field(
        ge=0,
        description="Stock can not be negative"
    )



class ProductPatch(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        description="Product Name"        
    )
    description: str | None = Field(
        default=None,
        min_length=2,
        max_length=400,
        description="Product Description"
    )
    price: float | None = Field(
        default=None,
        gt=0,
        description="Price must be greater than 0"
    )
    stock: int | None = Field(
        default=None,
        ge=0,
        description="Stock can not be negative"
    )    



class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class DeleteResponse(BaseModel):
    message: str