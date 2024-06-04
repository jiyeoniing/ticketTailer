from django.db import models
from django.conf import settings

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    recommend_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="recommended_posts", blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_img = models.ImageField(blank=True, upload_to='communities/', null=True)
    

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    parent_comments = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



