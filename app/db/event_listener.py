from sqlalchemy import func, event

from app.model.User import User
from app.db.session import CommentBase, LikeBase, CommentLikeBase


@event.listens_for(User, "before_update", propagate=True)
def update_updated_at_only_for_specific_changes_user(mapper, connection, target):
    # 수정된 속성 이력을 가져옵니다.
    state = target.__dict__["_sa_instance_state"]
    followers_history = state.attrs["follower_num"].history
    followings_history = state.attrs["following_num"].history

    # comments_num이 아닌 다른 속성이 변경되었는지 확인
    if not (followers_history.has_changes() or followings_history.has_changes()):
        target.updated_at = func.now()
    else:
        # comments_num만 변경된 경우 updated_at 유지
        target.updated_at = state.attrs["updated_at"].loaded_value


@event.listens_for(CommentBase, "before_update", propagate=True)
def update_updated_at_only_for_specific_changes_commentbase(mapper, connection, target):
    # 수정된 속성 이력을 가져옵니다.
    state = target.__dict__["_sa_instance_state"]
    comments_history = state.attrs["comments_num"].history

    # comments_num이 아닌 다른 속성이 변경되었는지 확인
    if not comments_history.has_changes():
        target.updated_at = func.now()
    else:
        # comments_num만 변경된 경우 updated_at 유지
        target.updated_at = state.attrs["updated_at"].loaded_value


@event.listens_for(LikeBase, "before_update", propagate=True)
def update_updated_at_only_for_specific_changes_likebase(mapper, connection, target):
    # 수정된 속성 이력을 가져옵니다.
    state = target.__dict__["_sa_instance_state"]
    likes_history = state.attrs["likes_num"].history

    # likes_num이 아닌 다른 속성이 변경되었는지 확인
    if not likes_history.has_changes():
        target.updated_at = func.now()
    else:
        # likes_num만 변경된 경우 updated_at 유지
        target.updated_at = state.attrs["updated_at"].loaded_value


@event.listens_for(CommentLikeBase, "before_update", propagate=True)
def update_updated_at_only_for_specific_changes_commentlikebase(
    mapper, connection, target
):
    # 수정된 속성 이력을 가져옵니다.
    state = target.__dict__["_sa_instance_state"]
    comments_history = state.attrs["comments_num"].history
    likes_history = state.attrs["likes_num"].history

    # comments_num과 likes_num이 아닌 다른 속성이 변경되었는지 확인
    if not (comments_history.has_changes() or likes_history.has_changes()):
        target.updated_at = func.now()
    else:
        # comments_num 또는 likes_num만 변경된 경우 updated_at 유지
        target.updated_at = state.attrs["updated_at"].loaded_value
