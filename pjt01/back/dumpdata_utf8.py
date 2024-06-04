import os
import django
from django.core.management import call_command

# Django 프로젝트의 설정을 환경 변수로 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviePjt.settings')

# Django 설정 및 데이터베이스 초기화
django.setup()

# # dumpdata 명령 실행
# with open('movies.json', 'w', encoding='utf-8') as f:
#     call_command('dumpdata', stdout=f, indent=2)

# 사용자 데이터 덤프 추가
with open('fixtures/users.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'accounts.User', stdout=f, indent=2)