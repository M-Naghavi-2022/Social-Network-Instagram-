from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class Audit(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    GENDER_CHOICES = [
        ("M","male"),
        ("F","female")
    ]
    phone_number = models.CharField(max_length=13, null=True, blank=True, validators=[RegexValidator(regex= r'^+\d{12}$', message='invalid phone number')])
    biography = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1 ,null=True, blank=True, choices=GENDER_CHOICES)
    private_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username


class FollowerTable(Audit):
    Follow_STATUS_CHOICES = [("a", "Accept"), ("p", "Pending")]
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    follow_status = models.CharField(max_length=1, choices=Follow_STATUS_CHOICES, default='p')

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['following', 'follower'], name='unique follower')
    ]
    
    def __str__(self) -> str:
        return f'{self.following} / {self.follower}'