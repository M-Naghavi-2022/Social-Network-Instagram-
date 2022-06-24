from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.decorators import action

from .models import *
from .serializers import *

class PostView(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        qs = request.user.posts.all().order_by('-create_time')
        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors)

    def destroy(self, request, pk=None):
        post = get_object_or_404(PostInstagram, pk=pk)
        if post.user != request.user:
            return Response(status=403)
        post.delete()
        return Response(status=204)

    def update(self, request, pk=None):
        post = get_object_or_404(PostInstagram, pk=pk)
        if post.user != request.user:
            return Response(status=403)
        serializer = PostEditSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["GET"], detail=False, url_name='followings_posts')
    def followings_posts(self, request):
        qs = PostInstagram.objects.filter(user__followers__follower = request.user).order_by('-create_time')
        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)



class PostLikeView(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    
    @action(methods=["GET"], detail=True, url_name='post_likes_list')
    def post_likes_list(self, request, pk=None):
        post = get_object_or_404(PostInstagram, pk=pk)
        if (post.user == request.user) or\
        (post.user.followers.filter(follower=request.user).exists()) or\
        (post.user.private_status==False):
            qs = post.post_likes.order_by('-create_time')
            serializer = PostLikeSerializer(qs, many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)

    @action(methods=["GET"], detail=True, url_name='like_unlike_post')
    def like_unlike_post(self, request, pk=None):
        post = get_object_or_404(PostInstagram, pk=pk)
        if (post.user == request.user) or\
        (post.user.followers.filter(follower=request.user).exists()) or\
        (post.user.private_status==False):
            post_like = PostLike.objects.filter(post=post, user=request.user).first()
            if post_like:
                post_like.delete()
                return Response({"message":"post unliked"},status=status.HTTP_204_NO_CONTENT)
            else:
                PostLike.objects.create(post=post, user=request.user)
                return Response({"message":"post liked"},status=status.HTTP_201_CREATED)
        else:
            return Response(status=403)


class PostCommentView(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    
    @action(methods=["GET"], detail=True, url_name='post_comments_list')
    def post_comments_list(self, request, pk=None):
        post = get_object_or_404(PostInstagram, pk=pk)
        if (post.user == request.user) or\
        (post.user.followers.filter(follower=request.user).exists()) or\
        (post.user.private_status==False):
            qs = post.post_comments.order_by('-create_time')
            serializer = CommentSerializer(qs, many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)

    @action(methods=["POST"], detail=True, url_name='new_comment')
    def new_comment(self, request, pk=None):
        post = get_object_or_404(PostInstagram, pk=pk)
        if (post.user == request.user) or\
        (post.user.followers.filter(follower=request.user).exists()) or\
        (post.user.private_status==False):
            serializer = CommentSerializer(data=request.data, context={"user": request.user, "post":post})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        else:
            return Response(status=403)

    def destroy(self, request, pk=None):
        comment = get_object_or_404(PostComment, pk=pk)
        if (comment.user == request.user) or (comment.post.user == request.user):
            comment.delete()
            return Response(status=204)
        return Response(status=403)


class CommentLikeView(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    
    @action(methods=["GET"], detail=True, url_name='comment_likes_list')
    def comment_likes_list(self, request, pk=None):
        comment = get_object_or_404(PostComment, pk=pk)
        if (comment.user == request.user) or\
        (comment.post.user == request.user) or\
        (comment.post.user.followers.filter(follower=request.user).exists()) or\
        (comment.post.user.private_status==False):
            qs = comment.comment_likes.order_by('-create_time')
            serializer = CommentLikeSerializer(qs, many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)

    @action(methods=["GET"], detail=True, url_name='like_unlike_comment')
    def like_unlike_comment(self, request, pk=None):
        comment = get_object_or_404(PostComment, pk=pk)
        if (comment.user == request.user) or\
        (comment.post.user == request.user) or\
        (comment.post.user.followers.filter(follower=request.user).exists()) or\
        (comment.post.user.private_status==False):
            comment_like = CommentLike.objects.filter(comment=comment, user=request.user).first()
            if comment_like:
                comment_like.delete()
                return Response({"message":"comment unliked"},status=status.HTTP_204_NO_CONTENT)
            else:
                CommentLike.objects.create(comment=comment, user=request.user)
                return Response({"message":"comment liked"},status=status.HTTP_201_CREATED)
        else:
            return Response(status=403)