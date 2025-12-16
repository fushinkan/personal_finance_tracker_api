from enum import Enum

class TransactionType(Enum):
    INCOME: str = "income"
    EXPENSE: str = "expense"