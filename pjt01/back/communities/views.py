from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from django.contrib.auth import get_user_model
from .serializers import (
    PostDetailSerializer,
    PostSerializer,
    CommentSerializer,
    # ReplySerializer
    )


User = get_user_model()

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_list_create(request):
   
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        posts = get_list_or_404(Post)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    is_recommend = False
    if request.user in post.recommend_users.all():
        is_recommend=True

    # 해당 유저가 이 글을 작성한 유저여야 수정 삭제 할 수 있음.
    if post.user == request.user:

        if request.method == 'PUT':
            serializer = PostDetailSerializer(post, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            
        elif request.method == 'DELETE':
            post.delete()
            return Response({'message': f'review {post_id} is deleted.'})

    serializer = PostDetailSerializer(post)
    return Response({'data':serializer.data, 'is_recommend':is_recommend})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            parent_id = request.data.get('parent_comments') # 적어줘야해 parent_comments를,,,
            if parent_id:
                parent = get_object_or_404(Comment, id=parent_id)
                serializer.save(post=post, user=request.user, parent_comments=parent)
            else:
                serializer.save(post=post, user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    comments = Comment.objects.filter(post=post, parent_comments=None) # 최상위 댓글만 조회
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id)

    # 해당 유저가 댓글을 작성한 유저여야 수정 삭제 할 수 있음.
    if comment.user == request.user:

        if request.method == 'PUT':
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            
        elif request.method == 'DELETE':
            comment.delete()
            return Response({'message': f'{post_id}인 post의 {comment_id}번째 댓글이 is deleted.'})

    serializer = CommentSerializer(comment)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_recommend(request, post_id):
    user = get_object_or_404(User, id=request.user.id)
    post = get_object_or_404(Post, pk=post_id)
    if user in post.recommend_users.all():
        post.recommend_users.remove(user)
        is_recommend=False
    else:
        post.recommend_users.add(user)
        is_recommend=True
    cnt = post.recommend_users.count()


    return Response({'message':'success','is_recommend':is_recommend ,'recommend_user_count':cnt})