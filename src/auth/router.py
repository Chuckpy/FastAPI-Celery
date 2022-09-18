from fastapi import APIRouter, HTTPException, Depends # , Header
from sqlalchemy.orm import Session
from . import authentication, services, schemas
from db.database import get_db



router = APIRouter(
    prefix="/auth",
    tags=["auth"],    
    responses={404: {"description": "Not found"}},
)


# @router.get("/") # TODO : example of user by authentication token
# async def read_root(Authorization : str = Header(default = None), db : Session = Depends(get_db)):
#     request_user = authentication.JWTAuthentication(Authorization, session = db)
#     if request_user.authenticate() :
#         return {"Hello": request_user.user.email}
#     return {"Hello": "Darn"}


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_users(db, skip=skip, limit=limit)

@router.post("/") # TODO : response models
def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user :
        raise HTTPException(status_code=401, detail="Email already registered")
    db_user = services.create_user(db=db, user=dict(user))
    user_dict = schemas.UserDisplay(**db_user.__dict__)    
    return dict(user_dict)

@router.post("/token", response_model = schemas.Token) # TODO : create auth token | response models
def create_auth_token(user : schemas.UserLogin, db : Session = Depends(get_db)):
    request_user = authentication.JWTAuthentication(login_payload = dict(user), session = db) 
    if request_user._valid:
        access_token = request_user.create_access_token()
        token = schemas.Token(access_token=access_token)        
        return token    
    raise HTTPException(status_code=401, detail="Wrong Password or email")
