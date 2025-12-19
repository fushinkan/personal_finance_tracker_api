from pydantic import BaseModel, Field

from datetime import datetime


class TransactionsSchema(BaseModel):
    amount: float
    category: str = Field(max_length=32)
    date: datetime
    description: str | None = Field(max_length=512)