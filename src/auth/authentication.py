import jwt
import hashlib
from os import getenv
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from fastapi import HTTPException
from . import models, schemas, services



# def authenticate(db_user : models.User, user : schemas.UserLogin) :
#     """ This method compare the two hashes of the user on database
#     and the given user """
#     data = dict(user)    
#     # hashed = hashlib.md5(password.encode())
#     data["hashed_password"] = data.pop("password")    
#     encoded = jwt.encode(data, getenv("JWT_SECRET", None), algorithm=getenv("ALGORITHM", None))    
#     valid = True if db_user.hashed_password == encoded else False    
#     return valid
    
    
def hash_password(user:dict):    
    hashed = hashlib.md5(user.pop("password").encode())
    data = {
        "email" : user.get("email"), # Order matters a lot here
        "hashed_password" : hashed.hexdigest() # Removing the raw password to prevent future flaws
        }
    encoded = jwt.encode(data, getenv("JWT_SECRET", None), algorithm=getenv("ALGORITHM", None))    
    return encoded

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=getenv("JWT_EXPIRATION_MINUTES"))
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, getenv("JWT_SECRET", None), algorithm=getenv("ALGORITHM", None))
    return encoded_jwt
 

class AuthenticationFailed(HTTPException) :
    def __init__(self,
                status_code: int = 401,
                detail: Any = "Incorrect authentication credentials",
                headers: Optional[Dict[str, Any]] = None,
                                    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class AuthToken():
    """ This Object is made it to validate the Token. """
    def __init__(self, token : str ) :
        self.token = token
    
    def __call__(self):
        try :
            return jwt.decode(self.token, getenv("JWT_SECRET"), algorithms = [getenv("ALGORITHM")])
        except jwt.exceptions.InvalidSignatureError :
            raise AuthenticationFailed(detail="Token Authentication Failed")
        except jwt.exceptions.ExpiredSignatureError :
            raise AuthenticationFailed(detail="Token Expired")
        except jwt.exceptions.DecodeError:
            raise AuthenticationFailed(detail="Decode Token Error")


class JWTAuthentication(object):
    """
    An authentication plugin that authenticates requests through a JSON web
    token provided in a request header.
    """
    def __init__(self, auth_header : str = None, **kwargs ):        
        self.user_model =  models.User
        self.auth_header = auth_header
        self._valid = False # TODO : passed trough validation method
        self.login_payload = kwargs.get("login_payload", None)
        self.session = kwargs.get("session", None)

    def create_access_token(self):
        if self._valid :
            to_encode = self.login_payload
            expire = datetime.utcnow() + timedelta(minutes=int(getenv("JWT_EXPIRATION_MINUTES")))
            to_encode["exp"] = expire
            encoded_jwt = jwt.encode(to_encode, getenv("JWT_SECRET", None), algorithm=getenv("ALGORITHM", None))
            
            return encoded_jwt

        raise AuthenticationFailed(detail = "User not authenticated yet")

    def authenticate(self):

        if self.login_payload :
            hashed_password = hashlib.md5(self.login_payload.pop("password").encode())
            self.login_payload["hashed_password"] = hashed_password.hexdigest()            
            encoded = jwt.encode(self.login_payload, getenv("JWT_SECRET", None), algorithm=getenv("ALGORITHM", None))                
            db_user = services.get_user_by_email(self.session, self.login_payload["email"])            
            self._valid = True if db_user.hashed_password == encoded else False                           
            return self._valid

        if self.auth_header is None:
            return False

        raw_token = self.get_raw_token()
        if raw_token is None:
            return False

        validated_token = self.get_validated_token(raw_token)

        if self.get_user(validated_token) :            
            return True
        
        return False

    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        valid_token = AuthToken(raw_token)        
        return valid_token()

    def get_user(self, validated_token):        
        self.user = services.get_user_by_email(self.session, validated_token.get("email", None))
        return self.user

    def get_raw_token(self):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = self.auth_header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                ("Authorization header must contain two space-delimited values"),
                code="bad_authorization_header",
            )

        return parts[1]

