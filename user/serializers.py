from hashlib import sha256
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from . models import User, FollowerTable

class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["username","password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create(
            username=validated_data['username'],
            password = make_password(validated_data['password'])
        )


class MyProfileSerializer(serializers.ModelSerializer):

    posts_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "private_status", "first_name", "last_name",
            "email","phone_number","birthday", "gender", "biography",
            "posts_count", "followers_count", "followings_count"]
        extra_kwargs = {
            "username": {
                "read_only": True
            }
        }

    def get_posts_count(self, obj):
        return obj.posts.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.followings.count()


class FollowerSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField()
    class Meta:
        model = FollowerTable
        fields = ["id","follower"]


class FollowingSerializer(serializers.ModelSerializer):
    following = serializers.StringRelatedField()
    class Meta:
        model = FollowerTable
        fields = ["id","following"]

class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowerTable
        fields = ["following"]

    def create(self, validated_data):
        follower = self.context["follower"]
        following = validated_data["following"]
        if following.private_status == True:
            return FollowerTable.objects.create(follower=follower, following=following, follow_status="p")
        return FollowerTable.objects.create(follower=follower, following=following, follow_status="a")
