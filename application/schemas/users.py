from pydantic import BaseModel, EmailStr, Field

class UserCreateSchema(BaseModel):
    username: str = Field(max_length=32)
    email: EmailStr = Field(max_length=256)
    hashed_password: str = Field(max_length=256)