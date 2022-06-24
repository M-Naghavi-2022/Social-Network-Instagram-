from rest_framework import serializers

from . models import User, FollowerTable

# class RegisterSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = User
#         fields = ["username","password"]

    

class MyProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "private_status", "first_name", "last_name",
            "email","phone_number","birthday", "gender", "biography"]
        extra_kwargs = {
            "username": {
                "read_only": True
            }
        }


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