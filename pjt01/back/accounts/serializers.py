from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from movies.serializers import MovieDetailSerializer, ReviewSerializer
from communities.serializers import PostSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'nickname', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("비밀번호가 다릅니다.")

        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("이미 해당 아이디가 존재합니다.")

        if User.objects.filter(nickname=attrs['nickname']).exists():
            raise serializers.ValidationError("이미 해당 닉네임이 존재합니다.")

        try:
            validate_password(attrs['password'])
        except serializers.ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data['nickname']
        )
        return user

class MyInfoSerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(use_url=True)
    
    class Meta:
        model = User
        fields = ['nickname', 'profile_img', 'password']

    def update(self, instance, validated_data):
            # 사용자 정보 업데이트
            instance.nickname = validated_data.get('nickname', instance.nickname)
            
            # 프로필 이미지 업데이트
            profile_img = validated_data.get('profile_img')
            if profile_img is not None:
                instance.profile_img = profile_img
            
            # 비밀번호 업데이트
            password = validated_data.get('password')
            if password:
                instance.set_password(password)
            
            instance.save()
            return instance

# 프로필 페이지 => 내 정보, 팔로잉-팔로워 수, 내가 쓴 게시글 수, 댓글 수, 내가 쓴 게시글, 리뷰, 찜한 영화
class ProfileSerializer(serializers.ModelSerializer):
    following_count = serializers.IntegerField(source='followings.count', read_only=True)
    follower_count = serializers.IntegerField(source='followers.count', read_only=True)
    post_count = serializers.IntegerField(source='posts.count', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    posts = PostSerializer(many=True, read_only=True)
    picked_movies = MovieDetailSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)



    class Meta:
        model = User
        fields = [
            'nickname', 'username', 'profile_img', 
            'following_count', 'follower_count', 
            'post_count', 'comment_count', 
            'posts', 'reviews', 'picked_movies'
        ]
