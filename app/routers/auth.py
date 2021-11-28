from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from .. import database, models, oath2, schemas, utils

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    # in the frontend i need to use a "form" not a json body
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):

    user = (
        db.query(models.User)
        # this is a form in the API request Login User and it will store my user username in the field "username"
        .filter(models.User.email == user_credentials.username).first()
    )
    if not user:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # user.id is the data to be passed in the jwt payload
    access_token = oath2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
