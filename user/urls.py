from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import MyProfile, FollowerCRUD # RegisterUser

router = DefaultRouter()
router.register("follow", FollowerCRUD, basename="follow")

urlpatterns = [
    # path("api/register_user/", RegisterUser.as_view(), name="register_user")
    path("api/my-profile/", MyProfile.as_view(), name="my_profile")
]+ router.urls