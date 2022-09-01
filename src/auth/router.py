from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from . import authentication, services, schemas
from db.database import get_db



router = APIRouter(
    prefix="/auth",
    tags=["auth"],    
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_root(Authorization : str = Header(default = None)):    
    user = authentication.JWTAuthentication(Authorization)    
    if user.authenticate() :
        return {"Hello": "World"}
    return {"Hello": "Darn"}


# TODO : uncomment this | rollback
# @router.get("/", response_model=list[schemas.User])
# async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return services.get_users(db, skip=skip, limit=limit)

@router.post("/") # TODO : response models
def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user :
        raise HTTPException(status_code=401, detail="Email already registered")
    db_user = services.create_user(db=db, user=dict(user))
    user_dict = schemas.UserDisplay(**db_user.__dict__)    
    return dict(user_dict)

@router.post("/token") # TODO : create auth token | response models
def create_auth_token(user : schemas.UserLogin, db : Session = Depends(get_db)):
    db_user = services.get_user_by_email(db,email=user.email)
    if db_user :
        if authentication.authenticate(db_user, user): # user is authenticated here
            return {"success": True}
        raise HTTPException(status_code=401, detail="Wrong Password or email")
    raise HTTPException(status_code=401, detail="User not Found")

