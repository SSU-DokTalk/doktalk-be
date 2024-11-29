from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, contains_eager

from app.dto.post import CreatePostReq
from app.dto.post_comment import CreatePostCommentReq
from app.model.User import User
from app.model.Post import Post
from app.model.PostComment import PostComment


def createPostService(user: User, post_data: CreatePostReq, db: Session) -> int:
    try:
        post = Post(user=user, data=post_data)
        db.add(post)
        db.commit()
        db.refresh(post)
    except IntegrityError:
        raise HTTPException(status_code=404)
    return post.id


def getPostService(post_id: int, db: Session):
    return (
        db.query(Post)
        .join(Post.user)
        .options(contains_eager(Post.user))
        .filter(Post.id == post_id)
        .first()
    )


def createPostCommentService(
    user: User, post_id: int, post_comment_data: CreatePostCommentReq, db: Session
) -> int:
    try:
        post_comment = PostComment(user=user, post_id=post_id, data=post_comment_data)
        db.add(post_comment)
        db.commit()
        db.refresh(post_comment)

        db.query(Post).filter(Post.id == post_id).update(
            {Post.comments_num: Post.comments_num + 1}
        )
        db.commit()

    except IntegrityError:
        raise HTTPException(status_code=404)
    return post_comment.id


def getPostCommentsService(post_id: int, db: Session):
    return (
        db.query(PostComment)
        .join(PostComment.user)
        .options(contains_eager(PostComment.user))
        .filter(PostComment.post_id == post_id)
        .all()
    )
