from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.post_list_create), # 게시글 생성 post 리스트 get
    path('posts/<int:post_id>/', views.post_detail),     # 게시글 수정 삭제 상세보기
    path('<int:post_id>/comments/', views.comment_list_create),  # 댓글 생성 댓글 리스트 get
    path('<int:post_id>/comments/<int:comment_id>/', views.comment_detail),         # 댓글 수정 삭제 상세보기
    path('<int:post_id>/recommend/', views.post_recommend), 
]
