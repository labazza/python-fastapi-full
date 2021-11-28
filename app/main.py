from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .config import Settings
from .database import engine
from .routers import auth, post, user, vote

# this will create the table defined via models.py
# if the table already exists will not modify it
# Since we have alembic we do not need it because will be done by the first alembic revision
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# where to allow my APIS from
# origins = [
#    "https://www.google.com",
#    "https://www.youtube.com",
# ]
# allow from everywhere
origins = ["*"]

# CORS https://fastapi.tiangolo.com/tutorial/cors/?h=cors
app.add_middleware(
    # Middlewre: Function that runs before every request
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # allow only specific http methods or headers
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
