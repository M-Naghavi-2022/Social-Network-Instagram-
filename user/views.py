from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.decorators import action

from .models import *
from .serializers import *

class RegisterUser(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = MyProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = MyProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowerCRUD(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["GET"], detail=False, url_path='followers_list')
    def followers_list(self, request):
        qs = request.user.followers.filter(follow_status='a')
        serializer = FollowerSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False, url_path='pending_follow_requests')
    def pending_follow_requests(self, request):
        qs = request.user.followers.filter(follow_status='p')
        serializer = FollowerSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False, url_path='followings_list')
    def followings_list(self, request):
        qs = request.user.followings.filter(follow_status='a')
        serializer = FollowingSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=["POST"], detail=False, url_path='send_follow_request')
    def send_follow_request(self, request):
        serializer = FollowRequestSerializer(data=request.data, context={"follower": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(serializer.errors)

    @action(methods=["GET"], detail=True, url_path="accept_follow_request")
    def accept_follow_request(self, request, pk=None):
        follow_req_obj = get_object_or_404(FollowerTable, pk=pk)
        if follow_req_obj.following != request.user:
            return Response(status=403)
        follow_req_obj.follow_status = "a"
        follow_req_obj.save()
        return Response(status=200)

    @action(methods=["GET"], detail=True, url_path="remove_follower")  
    def remove_follower(self, request, pk=None):
        follow_req_obj = get_object_or_404(FollowerTable, pk=pk)
        if follow_req_obj.following != request.user:
            return Response(status=403)
        follow_req_obj.delete()
        return Response(status=204)

    @action(methods=["GET"], detail=True, url_path="unfollow")  
    def unfollow(self, request, pk=None):
        follow_req_obj = get_object_or_404(FollowerTable, pk=pk)
        if follow_req_obj.follower != request.user:
            return Response(status=403)
        follow_req_obj.delete()
        return Response(status=204)