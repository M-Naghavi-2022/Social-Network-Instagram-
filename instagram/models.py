from django.db import models
from user.models import Audit, User

class PostInstagram(Audit):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    img = models.ImageField(upload_to="postImages/")
    caption = models.CharField(max_length=2800, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.id} / {self.user} / {self.caption}'


class PostLike(Audit):
    post = models.ForeignKey(PostInstagram, on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['post', 'user'], name='unique post like')
    ]
    
    def __str__(self) -> str:
        return f'{self.post} / {self.user}'


class PostComment(Audit):
    post = models.ForeignKey(PostInstagram, on_delete=models.CASCADE, related_name='post_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commented_posts')
    text = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return f'{self.post} / {self.user}'


class CommentLike(Audit):
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='comment_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_comments')

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['comment', 'user'], name='unique comment like')
    ]
    
    def __str__(self) -> str:
        return f'{self.comment} / {self.user}'