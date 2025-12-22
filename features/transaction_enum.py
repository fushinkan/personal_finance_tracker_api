from enum import Enum

class TransactionType(Enum):
    INCOME: str = "INCOME"
    EXPENSE: str = "EXPENSE"