from fastapi import APIRouter, HTTPException, Request

router = APIRouter(
    prefix="/chatter",
    tags=["chatter"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def home(request: Request):
    print(request)
    return {"Hello" : "world!"}

