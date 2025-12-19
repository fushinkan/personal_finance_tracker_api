from fastapi import APIRouter

router = APIRouter(prefix="/transactions", tags=["Transactions"])



@router.post("/new")
async def new_transaction_endpoint(transaction: ...):
    ...