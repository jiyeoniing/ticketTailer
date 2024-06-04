from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list),
    path('genres/', views.genre_list),
    path('genres/names/', views.genres_names),
    # path('create-movie/', views.create_movie),
    path('<int:movie_id>/', views.movie_detail),
    path('<int:movie_id>/likes/', views.movie_likes),
    path('<int:movie_id>/reviews/', views.review_create_list),
    path('<int:movie_id>/reviews/<int:review_id>/', views.review_detail_update_delete),
    path('reviews/<int:review_id>/likes/', views.review_likes, ),
    path('sorted/<str:sorted_name>/', views.movies_sorted), # 영화 목록 selected
    path('sorted/<str:sorted_name>/genre/<int:genre_id>/', views.movies_sorted_genre), # 영화 목록 selected
    path('algorithm/genre/', views.algorithm_genre), # 알고리즘 추천
    path('algorithm/review/', views.algorithm_review),
    path('algorithm/following/', views.algorithm_following),
    path('search/<str:search_name>/', views.search_movie)
]

