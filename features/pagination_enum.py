from enum import Enum

class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"

class SortField(Enum):
    CREATED_AT = "created_at"
    DATE = "date"
    AMOUNT = "amount"
    UPDATED_AT = "updated_at"
    CATEGORY = "category"
    TRANSACTION_TYPE = "transaction_type"