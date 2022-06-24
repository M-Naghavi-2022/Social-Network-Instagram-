from rest_framework import serializers

from .models import *

class CommentLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = CommentLike
        exclude = ["comment"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    
    class Meta:
        model = PostComment
        exclude = ["post"]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def create(self, validated_data):
        user = self.context["user"]
        post = self.context["post"]
        return PostComment.objects.create(user=user, post=post, **validated_data)
    
    def get_likes_count(self, obj):
        return obj.comment_likes.count()

    def get_liked_by_user(self, obj):
        if obj.comment_likes.filter(user=self.context["user"]).exists():
            return True
        return False


class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = PostLike
        exclude = ["post"]


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    class Meta:
        model = PostInstagram
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def create(self, validated_data):
        user = self.context["user"]
        return PostInstagram.objects.create(user=user, **validated_data)

    def get_likes_count(self, obj):
        return obj.post_likes.count()

    def get_comments_count(self, obj):
        return obj.post_comments.count()

    def get_liked_by_user(self, obj):
        if obj.post_likes.filter(user=self.context["user"]).exists():
            return True
        return False


class PostEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostInstagram
        fields = ["caption"]