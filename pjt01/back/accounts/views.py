from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import logout as auth_logout
from .serializers import CustomUserSerializer, MyInfoSerializer, ProfileSerializer


User = get_user_model()

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "해당 닉네임 또는 아이디가 이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    # user= User.objects.get(username=username)
    user = authenticate(username=username, password=password)
    # return Response({"message": "test"}, status=status.HTTP_200_OK)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)       
        return Response({"token": token.key, 'username':username}, status=status.HTTP_200_OK)        
    return Response({'error': '아이디 또는 비밀번호와 일치한 사용자가 없습니다.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()  
    auth_logout(request)
    return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_info(request):
    user = request.user
    
    if request.method == 'GET':
        serializer = MyInfoSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MyInfoSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response({'error':'해당 정보를 수정할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # elif request.method == 'POST':
    #     profile_img = request.FILES.get('profile_img')

    #     if profile_img:
    #         user.profile_img = profile_img
    #         user.save()
    #         return Response({"message": "Profile image updated successfully."}, status=status.HTTP_200_OK)
    #     return Response({"error": "프로필 이미지가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, username):
    try:
        person = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': '해당 사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.user != person:
        if person.followers.filter(pk=request.user.pk).exists():
            person.followers.remove(request.user)
            is_followed = False
        else:
            person.followers.add(request.user)
            is_followed = True
  
        data = {
            'is_followed': is_followed,
            'follower_count': person.followers.count(),
            'following_count': person.followings.count(),
        }
        return Response({'data':data})

    data = {
            'follower_count': person.followers.count(),
            'following_count': person.followings.count(),
        }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    try:
        user = User.objects.get(username=username)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': '해당 사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)