from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname' ]

# 게시글 작성, 전체 목록
class PostSerializer(serializers.ModelSerializer):

    post_img = serializers.ImageField(use_url=True, required=False)
    recommend_users = UserSerializer(many=True, read_only=True)
    recommend_user_count = serializers.IntegerField(source='recommend_users.count', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'recommend_users', 'user', 'title', 'content', 'created_at', 'post_img', 'recommend_user_count']

class PostTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ('id', 'title', )

# 댓글 작성, 댓글 목록
    
# 댓글 디테일 수정 삭제
class CommentSerializer(serializers.ModelSerializer):

    replies = serializers.SerializerMethodField()
    post = PostTitleSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'parent_comments', 'replies', 'created_at', 'updated_at']
        read_only_fields = [ 'user', 'created_at', 'update_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return None

# 게시글 수정, 삭제, 디테일
class PostDetailSerializer(serializers.ModelSerializer):

    post_img = serializers.ImageField(use_url=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    recommend_users = UserSerializer(many=True, read_only=True)
    recommend_user_count = serializers.IntegerField(source='recommend_users.count', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'recommend_users', 'user', 'title', 'content',
                   'created_at', 'post_img', 'recommend_user_count',
                   'comments', 'comment_count']
