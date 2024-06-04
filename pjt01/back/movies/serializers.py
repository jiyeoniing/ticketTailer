from rest_framework import serializers
from .models import Movie, Genre, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', ]

class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','nickname', 'username', 'followings', 'profile_img']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):

    # genres = GenreSerializer(many=True)

    genres = GenreSerializer(many=True, read_only=True )
    pick_users = UserAllSerializer(many=True, read_only=True)
    # pick_users = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=get_user_model().objects.all())
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'tagline', 'runtime', 'original_title', 'original_language',
            'original_country', 'overview', 'poster_path', 'backdrop_path',
            'popularity', 'vote_average', 'vote_count', 'release_date',
             'genres', 'pick_users', 'director', 'actors', 'trailer'
        ]

# 해당 movie에 해당하는 리뷰
class ReviewSerializer(serializers.ModelSerializer):

    class MovieTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id','title', 'poster_path')

    user = UserAllSerializer(read_only=True)
    movie = MovieTitleSerializer(read_only=True)
    like_users = UserSerializer(many=True, read_only=True)
    like_user_count = serializers.IntegerField(source='like_users.count', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

# 영화 상세페이지 => 해당 영화에 대한 리뷰들, 사용자가 찜한 영화들 나와야함.
class MovieDetailSerializer(serializers.ModelSerializer):

    class ReviewMovieDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = ('title','famous_line','content','watched_at','created_at','is_opened' ,'rating', )
            # fields = ('title','famous_line','content','watched_at','created_at' ,'rating', )
            read_only_fields = ('movie', 'user', 'like_users')

    reviews = ReviewSerializer(many=True, read_only=True)
    review_count = serializers.IntegerField(source='reviews.count', read_only=True)

    # genres = GenreSerializer(many=True)

    genres = GenreSerializer(many=True, read_only=True )
    # pick_users = UserAllSerializer(many=True, read_only=True)
    # isPicked = serializers.BooleanField(source=User)
    pick_users = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=get_user_model().objects.all())
    pick_user_count = serializers.IntegerField(source='pick_users.count', read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'tagline', 'runtime', 'original_title', 'original_language',
            'original_country', 'overview', 'poster_path', 'backdrop_path',
            'popularity', 'vote_average', 'vote_count', 'release_date',
             'genres', 'pick_users', 'director', 'actors', 'trailer','pick_user_count', 'reviews', 'review_count',
        ]
