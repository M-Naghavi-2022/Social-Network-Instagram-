from django.db import router
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register("posts", PostView, basename="posts")
router.register("post_likes", PostLikeView, basename="post_likes")
router.register("post_comments", PostCommentView, basename="post_comments")
router.register("comment_likes", CommentLikeView, basename="comment_likes")

urlpatterns = [

] + router.urls