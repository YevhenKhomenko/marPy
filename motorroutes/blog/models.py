from django.db import models
from django.contrib.auth.models import User


class File:
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    content = models.FileField()


class Post:
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True)
    text = models.TextField(max_length=5000)

    class Meta:
        ordering = ['-date']


class Comment:
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    text = models.TextField(max_length=2000)
    post_link = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_link = models.ForeignKey('self', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
