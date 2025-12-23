from pydantic import BaseModel, EmailStr, Field

class UserCreateSchema(BaseModel):
    username: str = Field(max_length=32)
    email: EmailStr = Field(max_length=256)
    password: str = Field(max_length=256)

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(max_length=256)
    password: str = Field(max_length=256)

class UserResponseSchema(BaseModel):
    id: int = Field(ge=1)
    username: str = Field(max_length=32)
    email: EmailStr = Field(max_length=256)