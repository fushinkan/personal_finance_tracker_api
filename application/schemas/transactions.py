from pydantic import BaseModel, Field

from datetime import datetime

class TransactionsSchema(BaseModel):
    amount: float = Field(gt=0, description="The transaction amount must be greater than 0")
    category: str = Field(max_length=32, description="Transaction category")
    date: datetime | None = Field(None, description="Transaction datetime (default is current)")
    description: str | None = Field(max_length=512, description="Transaction description")