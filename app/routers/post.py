from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.routing import iscoroutinefunction_or_partial

from .. import models, oath2, schemas
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

# skip search and limit is a query parameter
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oath2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    # returns only posts without votes
    # posts = (
    #    db.query(models.Post)
    #    .filter(models.Post.title.contains(search))
    #    .limit(limit)
    #    .offset(skip)
    #    .all()
    # )
    # get all posts of the user currently logged in
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # results = db.query(models.Post)

    # by default sqlalchemy does a LEFT INNER JOIN while in PSQL by default is OUTER
    # results = (
    #    db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
    #    .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    #    .group_by(models.Post.id)
    # )
    # print raw SQL
    # print(results)
    # SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at, posts.owner_id AS posts_owner_id, count(votes.post_id) AS votes
    # FROM posts LEFT OUTER JOIN votes ON votes.post_id = posts.id GROUP BY posts.id
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oath2.get_current_user),
):

    # new_post = models.Post(
    #    title=post.title, content=post.content, published=post.published
    # )
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oath2.get_current_user),
):

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oath2.get_current_user),
):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform reqested action",
        )
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oath2.get_current_user),
):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    update_post = post_query.first()

    if not update_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exists",
        )

    if update_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform reqested action",
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
