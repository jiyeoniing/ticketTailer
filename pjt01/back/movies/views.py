import random
from collections import Counter
from django.db.models import Count
from collections import defaultdict
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import Genre, Movie, Review
from django.contrib.auth import get_user_model
from django.db.models import Max, Q
from .serializers import (
    MovieSerializer, 
    GenreSerializer, 
    ReviewSerializer,
    MovieDetailSerializer
    )

User = get_user_model()

token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0ZjM4ZDBmMTBlNjI4MTI0MWZmOGRlNjZkYThmODU5NiIsInN1YiI6IjY2M2Q5MTViYjQ0N2EzZWRkN2M3NmI3OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.bEskFkSb3luRGhVLTtHmJSazgi-Em2YA-mwd2eALSCA'
# token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3N2Q1OTA1NDJmYzc2NjIzMDAzNWU5MzEzY2U1NzU0MiIsInN1YiI6IjY2M2RhYmU3MThlODBmOWE2NmRhNTdlOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DL5e2A1e_rJrCjun2KotPUk16She8F82jd5SQYH4YsQ'  # Bearer 토큰이 필요한 경우
def create_genre(request):
    url = f'https://api.themoviedb.org/3/genre/movie/list?language=ko-KR'
    headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

    genres = requests.get(url, headers=headers).json().get('genres')
    for genre in genres:
        genre_id=genre.get('id')
        genre_name=genre.get('name')
        Genre.objects.create(id=genre_id,genre_name=genre_name)

    return JsonResponse({'message':'save okay!'})


def create_movie(request):
    same=['고질라 X 콩: 뉴 엠파이어', '혹성탈출: 새로운 시대', '고질라: 마이너스 원', 'Un père idéal', '쿵푸팬더 4', '블랙 로터스', 'Chief of Station', '듄: 파트 2', '고스트버스터즈: 오싹한 뉴욕', '킹 VS. 머신킹', '애비게일', '노 웨이 업', '너란 개념', '가필드 더 무비', '异兽战场', '혹성탈출: 반격의 서막', 'Hunt Club', 'Miraculous World : Paris, Les Aventures de Toxinelle et Griffe Noire', '파묘', 'Rebel Moon — 파트 2: 스카기버', '인투 더 월드', '챌린저스', '이매큘레이트', '마담 웹', '오펜하이머', '귀공자', '로드 하우스', '분노의 질주: 라이드 오어 다이', '시빌 워', '듄', '트리플 엑스', '혹성탈출: 종의 전쟁', '극장판 스파이 패밀리 코드 : 화이트', 'The Long Game', '바비', '외계+인 1부', '이프: 상상의 친구', '타로', '혹성탈출: 진화의 시작', '사옌 3: 사냥꾼', 'The Night They Came Home', 'Más que amor, frenesí', '삼총사: 밀라디', '데미지드', '데드풀', '매 트릭스', '더 배트맨', '약속의 네버랜드', '플래 시', '퓨리오사: 매드맥스 사가', '스타워즈 에피소드 4: 새로운 희망', '미션 투 베를린', '메이의 새빨간 비밀', '인터스텔라', ' 조커', '터미네이터', '고스 트버스터즈', '테넷', '아이언맨 2', '578 매그넘', '신부의 어머니', '토르: 라그나로크', '로건', '에이리언', '인사이드 아웃 2', '더 마블스', 'X', '인셉션', '2001 스페이스 오디세이', '캡틴 마블', '컨택트', '블랙 팬서', '펄프 픽션', '웡카', '원더 우먼', '버드 박스', 'Breathe', '공포의 보수', '엑스맨: 다 크 피닉스', '프레데터', '007 스펙터', '록키', '바빌론', '23 아이덴티티', '도니 다코', '그린 북', '에이리언: 커버넌트', '모비우스', '어메이징 메리', ' 세레니티', '비키퍼', '파이터', '콘  에어', 'Force of Nature: The Dry 2', '베이워치: SOS 해상 구조대', '슈퍼맨', '미저리', '닥터 스트레인지', '로보캅', '시민 케인', '그래비티', '택시 드라이버', '미셸 오바마의 비커밍', '케이트', '혹성탈출', '다크 시티', '사일런스', '저지 드레드', '스카페이스', '할로윈', '데드풀 2', '토탈 리콜', '베놈', '크립쇼', 'La mesita del comedor', '매드  맥스: 분노의 도로', '어벤져스: 인피니티 워', '스탠 바이 미', '레이디 버드', '베이비 드라이버', '살인병동', '데스 위시', '블레이드', '엔젤 하트', '로건 럭키', '세븐', '오멘', '나의 잘못', '스파이더맨: 홈커밍', '죠스', '스카이스크래퍼', '더 넌', '채피', '샤잠!', '저스티스 리그', 'After the Pandemic', '프레이', '가필드', 'Noche de Bodas', '얼 라이드', '아서', '차이나타운', ' 아쿠아맨', '크리드 2', '특수부대 비룡', '봉신연의: 조가풍운', '다운사이징', '링스', '어비스', '겟 아웃', '랜드 오브 배드', '노바디', '스피시즈', 'U 턴', '스팅', '그것: 두 번째 이야기', '브룩클린의 아이들', '그리스', '콩: 스컬 아일랜드', '위시', '나의 마더', '댐즐', 'Vina: Sebelum 7 Hari', '아메리칸', '굿 윌 헌팅', '코드네임: 에이전트 블랙', '콰이어트 플레이스', '서버비콘', '메트로폴리스', '크리에이터', 'Justice League: Crisis on Infinite Earths Part Two', '이블 데드 2', '스크루지', 'Megamind vs. the Doom Syndicate', '아이언맨 3', '브라이트', '인사이드 아웃', '가여운 것들', '토이 스토리', '블루스 브라더스', '쏘우 X', '우디 우드페커 캠프에 가다', '맨하탄', '디트로이트', '제너럴', '스크림 2', '페이크 러브', '라이온 킹', '더 록', '블랙 위도우', '홈즈 & 왓슨', '슈퍼 마리오 브라더스', '스턴트맨', '록키 4', '파이트 클럽', '더 보이', '좋은 친구들', '더 이퀄라이저 3', '원더 우먼 1984', '아기상어 극장판: 사이렌 스톤의 비밀', '미이라', '범블비', 'Oh, God! Book II', '스파이더맨: 노 웨이 홈', '크리드 3', '어벤져스: 엔드게임', '재키', '캅 랜드', ' 록키 5', '명탐정 필립', '프레데터스', '지오스톰', '스파이더맨: 어크로스 더 유니버스', '드라이', '엑스 마키나', '저스티스 리그: 크라이시스 온 인피닛 어스 파트 1', '오션스 8', '더 수어사이드 스쿼드', '허슬러', '더 그레이', '아이즈 와이드 셧', '헌트', 'Vermines', '핵소 고지', '블랙 팬서: 와칸다 포에버', '스크림', '디파티드', 'クラユカバ', '프리 가이', '그대들은 어떻게 살 것인가', '아메리칸 뷰티', 'El correo', '뉴 뮤턴트', '헬레이저', '러브 라이즈 블리딩', '언컷 젬스', '스리 아시', '윈드 리버', '오멘: 저주의 시작', '더 미니스트리 오브 언젠틀맨리 워페어', '존 윅 4', 'Aberrance', '프레데터 2', '엘리멘탈', '그것', '덤 앤 더머', '히트', '토이 스토리 4', '몽키맨', '고질라 VS. 콩', '프로메테우스', '코카인 베어', '엑스맨: 아포칼립스', '제미니 맨', '스타워즈 에피소드 6: 제다이의 귀환', '트루 로맨스', '네트', 'Vikings: Battle of Heirs', '더 레이오버', '악마와의 토크쇼', '아이리시맨', '로건의 탈출', '파고', '트랜스포머: 비스트의 서막', '레드 스패로', '이모티: 더 무비', '수어사이드 스쿼드', '아일랜드', '킹스맨: 퍼스트 에이전트', '포스가 엄마와 함께 하길', '파벨만스', '이매지너리', '배트맨 비긴즈', '위플래쉬', '크립쇼 2', '눈물을 만드는  사람', '허니문처럼', '유령 마을', '발신제한', '레디 오어 낫', '골드', '날개', '직쏘', '도망자 2', '컨테이젼', '델마', '솔라리스', '아바타: 물의 길', '셀: 인류 최후의 날', '대부 3', '포레스트 검프', '하이랜더', '보헤미안 랩소디', '로스트 보이', '호커스 포커스 2', '007 퀀텀 오브 솔러스', '슈퍼플라이', '터미네이터 제니시스', '브루클린', '나폴 레옹', '토르: 러브  앤 썬더', '코드 8: 파트 2', '길다', '장화신은 고양이: 끝내주는 모험', '백헤드', '아쿠아맨과 로스트 킹덤', '프리랜스', '패신저스', '플래툰', '이색지대', '프레스티지', '사채왕 페그', '슈렉 2', '블로커스', '007 어나더데이', '뱀파이어', '더 플랫폼', '블루 비틀', 'Thabo and the Rhino Chase', '써로게이트', 'Jade', 'Nightman', '싸이코', '하트 오브 더 헌터', 'Culpa tuya', '카사블랑카', '데드풀과 울버린', '그녀', '데이 제로: 최후의 날', '어벤져스', '더 이퀄라이저 2', '트위스터', '판의 미로: 오필리아와 세개의 열쇠', '헤더스', '더 서클', '쥬라기 월드: 도미니언', 'Arca de Noé', '아이언맨', '딥 워터', '미 션 임파서블: 데드 레코닝 PART ONE', '오무로가', 'Skal - Fight for Survival', '머시', '더 더트', '크레이지 리치 아시안', '인사이드 르윈', '톱 햇', '고 질라: 킹 오브 몬스터', '구혼 작전', '지구 최후의 날 2021', '바운드', '싱잉 넌', '스타 트렉: 비욘드', '노팅 힐', '캣 윌리엄스: 깨어 있거나 잠들었거나', '쇼생크 탈출', '터미네이터: 다크 페이트', 'Hunters', '이블 데드', '리스타트', '블레어 위치', '터스크', ' 톡 투 미', '프레디의 피자가게', '더 벨코 익스페리먼트', '다운 더 래빗 홀', '더 프레데터', '블랙 아담', '고질라', '갤럭시 퀘스트', '헬프', '엔칸토: 마법의 세계', '미션 임파서블: 폴아웃', '캡틴 아 메리카: 시빌 워', '화이트 칙스', '헝거게임: 노래하는 새와 뱀의 발라드', '파운더', '안나', '金瓶風月', 'Malicious', '라 리파', '해리 포터와 아즈카반의 죄수', 'Dark Shadows', 'IO', '60분', '주토피아', '더 포스트', '몬스터 주식회사', '제이슨 X', 'The OctoGames', '메가로돈 2', '우주전쟁', '트롤: 밴드 투게더', '북북서로  진로를 돌려라', '007 리빙 데이라이트', '해리 포터와 불의 잔', '복수의 사도', '캐리비안의 해적: 블랙펄의 저주', '필라델피아 스토리', '알리타: 배틀 엔젤', '존 오브 인터레스 트', '투모로우 워', '반지의 제왕: 반지 원정대', '인랜드 엠파이어', '탑건: 매버릭', '나니아 연대기: 사자, 마녀 그 리고 옷장', '코렐라인: 비밀의 문', '코코', '소시지 파티', 'Ruthless', '블랙 호크 다운', '싱 스트리트', '대부', '에이리언 3', '옥자', '해리 포터와 비밀의 방', '가디언즈 오브 갤럭시 Volume 3', '돈 룩 업', '씽2게더', '히든 피겨스', '레오', '1922', '블랙 위도우: 파이널 챕터', '헬보이', '가타카', '황야', '슈렉', 'Darkness of Man', '로그', '메이드 인 스웨덴', 'Rebel Moon — 파트 1: 불의 아이', '잇 컴스  앳 나잇', '10 jours encore sans maman', '슬립워커스', '007 살인 면허', '사마리탄', '더 게스트', '터미네이터 2: 심판의 날', '맨 인 블랙', '13일의 금요일', '메이즈 러너', ' 워 머신', '마이 걸', '캐시트럭', '과거로부터', '로우', '크래프트', 'Red Water', '아키라', '다크타워: 희망의 탑', 'Princezna zakletá v čase 2', '클루리스', '아이스 로드', '인어공주', '밀러스 걸', '내 친구 어둠', '뮤트', '올드 스쿨', '오두막', '모넬라', '웨이 다운', '이블 데드 라이즈', '익스트랙션', '해리 포터와 죽음의 성물 2', '더 저지', '바튼 아카데미', '어메이징 스파이더맨', '돼지와 뱀과 비둘기', '남부의 노래', '플라워 킬링 문', '맬리스', '맨 오브 스틸', '라푼젤', 'The Quantum Devil', '토이 스토리 2', '미  비포 유', '타이타닉', '해리 포터와 죽음의 성물 1', '블레이드 러너 2049', 'Balinsasayaw', '호텔 아르테미스', '밥 말리:  원 러브', '불릿 트레인 다운', '프롬 데이트', '거북이는 언제나 거기에 있어', '수퍼 소닉 2', '007 두번 산다', '사탄의 베이비시터', '더 킹: 헨리 5세', ' 알라딘', '더 넌 2', '가족의 탄생', '혹성탈출 3 - 제3의 인류', '혹성탈출 5 - 최후의 생존자', '슈퍼배드 4', '2012', '애프터', 'Gargoyles', '무비 43', ' 킹콩', '해리 포터와 불사조 기사단', '해리 포터와 혼혈왕자', 'Kalikot', '워 온 에브리원', '식스 센스', '라따뚜이', '쿵푸팬더', 'Where the Devil Roams', '컨저링', '야전병원 매쉬', '혹성탈출 2 - 지하도시의 음모', '닥터 슬립', '스크림 4G', 'Teen Witch', '더 퍼스트 퍼지', '애니멀 하우스의 악동들', '빅 히어로', '제국의 종말', '바스터즈: 거친 녀석들', '찰리와 초콜릿 공장', '퍼플 레인', '아바타', '더 웨일', 'Valle de sombras', '스파이더맨: 파 프롬 홈', '반지의 제왕: 왕의 귀환', '어카운턴트', '데몰리션 맨', '미션 임파서블', '덩케르크', '스루 마이 윈도 3: 너에게 머무는 시선', '365일: 오늘', '시티 오브  갓', ' 언프로스티드', '하울링', '에이리언 4', '매그놀리아', '스트레인저스', 'Plancha', '스파이더맨: 뉴 유니버스', 'I viaggiatori', '실크우드', 'A Haunting in Ravenwood', 'El Roomie', '킹스맨: 시크릿 에이전트', '빽 투 더 퓨쳐', '007 살인 번호', '바이러스', '호빗: 다섯 군대 전투', '라이프', '스티브 잡 스', '애프터 썬셋', '어벤져스: 에이지 오브 울트 론', '쾌락지구X', '죽어도 마인드혼', '나이트 헌터', '비틀쥬스', '대역전', '그레이의 50가지 그림자', '더 테러: 인디아 해즈 폴른', '에어 포스 원 다운', '람보', '로스트 인 더스트', 'The Re-Education of Molly Singer', '아라비아의 로렌스', '시티헌터', '스파 이더맨 3', '디스커버리', '트와일라잇', '아일린', 'Mercy Falls', '니모를 찾아서', '카 3:  새로운 도전', "Don't Look at the Demon", '"Mitchell"!', '회색 도시', '리프트: 비행기를 털어라', 'Gato Galáctico e o Feitiço do Tempo', '캐리비안의 해적: 세상의 끝에서', ' 파워 레인져스: 더 비기닝', '파리, 텍사스', '맨체스터 바이 더 씨', '뉴 라이프', '다키스트 마인드', '몬스터 호텔: 뒤바뀐 세계', '슈퍼배드', '리버스 엣지', '복면목사', '더 랍스터', '티탄', '하드 타겟', 'The Thundermans Return', '스파이더맨', '172 Days', '나이스 가이즈', '캐리비안의 해적: 낯선 조류', '사스콰치 선셋', '블랙폰', '프로메어 가로편', 'Lucy 2', '메가마인드', '헝거게임: 모킹제이', '콰이어트 플레이스: 첫째 날', '마거리트의 정리', '몰리스 게임', '테이큰 3', '나쁜 녀석들: 라이드 오어 다이', '닥터 스트레인지: 대혼돈의 멀티버스', '업그레이드', '반지의 제왕: 두 개의 탑', '곰돌이 푸: 피와 꿀 2', '십계', '석양의 무법자', '리얼 스틸', ' 겨울왕국 2', '퀸카로 살아남는 법: 더 뮤지 컬', 'The Five', '폴: 600미터', '더 이퀄라이저', '겨울왕국', '그린 마일', '로크', '공각기동대: 고스트 인 더  쉘', '백 투 블랙', '아웃브레이크', '사탄의 인형', '비커밍 본드', '天使を誘惑', 'Supermarsu 2', '싸일런트 러닝', '미라큘러스: 레이디버그와 블랙캣, 더  무비', 'Dear David', '바르셀로나 이비자 DJ', '그란 투리스모', '엑스칼리버', '뮬란', '신데렐라', '피스트 파이트', '더 울프 오브 월 스트리트', '메리다와 마법의 숲', '드레스메이커', '런닝 맨', '아리', '미시즈 해리스 파리에 가다', '리차드 쥬얼', '행오버', ' 익스트랙션 2', '스내치', '스트레이트 아웃 오브 컴턴', '공작 부인', '쿵푸팬더 3', '하울의 움직이는 성', '캐리비안의 해적: 망자의 함', '슬렌더 맨', '카 2', '쿠스코? 쿠스코!', '또 다른 365일', '아이스 에이지', '맨 다운', '공포의 묘지', '사랑도 통역이 되나요?', '톰과 제리', '아들의 여친 아빠의 여친', '샹치와 텐 링즈의 전설', '카사그란데 가족:  더 무 비', '애나벨: 인형의 주인', '아카디안', '컨저링 3: 악마가 시켰다', 'L.E.T.H.A.L. Ladies: Return to Savage Beach', '씬 레드 라인', '베놈 2: 렛 데어 비 카니지', '레전 드', '맘&대드', '루카', '불릿 트레인', '킹스맨: 골든 서클', '팜 스프링스', '퍼피 러브', '로렉스', 'La moglie di mio padre', '빌로우 허', '사랑의 걸작', '닌자터틀: 뮤턴트  대소동', '위키드', '브릭레이어', '니모나', '나우 유 씨 미: 마술사기단', 'La via della prostituzione', '프로듀서', ' 러브 액츄얼리', '라스트 홈', '데드 캠프 4', '오버로드', '다 큰 녀석들', '나를 찾아줘', '악이 도사리고 있을 때', '미니언즈 2', '50가지 그림자: 심연', '레고 배트맨 무비', '브레이킹 던 Part 1', '존 윅', '인디펜던스 데이', 'Red Right Hand', 'Emmanuelle 6', '원 라이프', '메이즈 러너: 스코치 트라이얼', ' 분노의 질주: 홉스 & 쇼', '오즈의 마법사', '시누이의 맛', '투씨', '샤잠! 신들의 분노', '애프터: 그 후', '나쁜 녀석들: 포에버', '야망의 함정', '도그맨', '미션 임파서블: 로그네이션', '앤트맨과 와스프: 퀀텀매니아', '땡스기빙', '에이리언 2', '데드 포 어 달러', '사운드 오브 프리덤', '테이큰', '타잔', '공주와 개구리', '이오 카피타노', '슈렉 포에버', '라이츠 아웃', '귀멸의 칼날 극장판: 무한열차편', '월•E', '외계+인 2부', '스타워즈 에피소드 7: 깨어난 포스', '마다가스카의 펭귄', '레퓨지', 'Rust', '귀멸의 칼날: 남매의 연', '하우스', '드림 시나리오', '월드워Z', '캐리', '신비한 동물들과 덤블도어의 비밀', '배트맨', '크리스틴', '헤라클레스', '쥬라기 월드: 폴른 킹덤', '셰이프 오브 워터: 사랑의 모양', '존 윅 2: 리로드', '콰이어트 플레이스 2', '스마일', "You Can't Run Forever", '유브 갓  메일', '레트리뷰션', '라이온 킹 2', '쿵푸팬더 2', '스크림 6']
    for page in range(46, 80):
        
        url = f'https://api.themoviedb.org/3/movie/popular?language=ko-KR&page={page}'
        headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

        response = requests.get(url, headers=headers).json().get('results')
        for li in response:
            title = li.get('title')
            id = li.get('id')
            if title in same:
                continue
            
            else:
                same.append(title)

                # DETAIL API
                detail_url = f'https://api.themoviedb.org/3/movie/{id}?language=ko-KR'
                headers = {
                        'Authorization': f'Bearer {token}',
                        'Content-Type': 'application/json'
                    }

                movie = requests.get(detail_url, headers=headers).json()
                
                # CREDIT API
                credit_url = f'https://api.themoviedb.org/3/movie/{id}/credits'
                headers = {
                        'Authorization': f'Bearer {token}',
                        'Content-Type': 'application/json'
                    }
                params = {
                        'language': 'ko-KR'
                    }

                credit = requests.get(credit_url, headers=headers, params=params).json()            


                genre_lst = []
                for genre in movie.get('genres'):
                    genre_id, created = Genre.objects.get_or_create(id=genre.get('id'), genre_name=genre.get('name'))
                    genre_lst.append(genre_id.pk)

                actor_lst = []
                director_lst = [] 
                # 크레딧의 known_for_department (역할) : Acting(배우), Directing(감독), name (이름) 가져오기
                for info in credit.get('cast') :

                    if info.get('known_for_department') == 'Acting' :
                        actor_lst.append(info.get('name'))
                    elif info.get('known_for_department') == 'Directing' :
                        director_lst.append(info.get('name'))

                if not genre_lst or not director_lst or not actor_lst:
                    continue  
                

                print(same)
                print(page)
                # Youtube api
                youtube_search_url = f'https://www.googleapis.com/youtube/v3/search'
                headers = {
                        # 'Authorization': f'Bearer {token}',
                        'Content-Type': 'application/json'
                    }
                params = {
                        'language': 'ko-KR',
                          'part':'snippet', 
                        #   'key':'AIzaSyCD4mx86jbNItmF61PAspdfl0PzwK0D7k0',
                        #   'key':'AIzaSyCPzrDA08VQ0RYPQ57wbUNjEm-TYfFSJ3c', 
                            # 'key': 'AIzaSyC4fSXuv2W4OHlbuNrWOoD9R4Yi9rdEXdM' ,
                            # 'key' : 'AIzaSyBzLmYyMCm4y2szadkdV-DU6N7_saeQDmQ',
                            'key':'AIzaSyD1pz77705JbW_awoKqKq5K_3Sih_q58zI',
                            'type': "video",
                            'q': title
                    }

                trailer_id = requests.get(youtube_search_url, headers=headers, params=params).json().get('items')[0].get('id').get('videoId')
                print(trailer_id)
                trailer_url = f'https://www.youtube.com/embed/{trailer_id}'

                save_data = {
                    'title': movie.get('title'),
                    'tagline': movie.get('tagline', ''),
                    'runtime': movie.get('runtime'),
                    'original_title': movie.get('original_title'),
                    'original_language': movie.get('original_language'),
                    'original_country': movie.get('production_countries')[0]['iso_3166_1'] if movie.get('production_countries') else '',
                    'overview': movie.get('overview', ''),
                    'poster_path': movie.get('poster_path'),
                    'backdrop_path': movie.get('backdrop_path'),
                    'popularity': movie.get('popularity'),
                    'vote_average': movie.get('vote_average'),
                    'vote_count': movie.get('vote_count'),
                    'release_date': movie.get('release_date'),
                    'video': movie.get('video'),
                    'genres' : genre_lst,
                    'director': ', '.join(director_lst),  # 리스트를 문자열로 변환
                    'actors': ', '.join(actor_lst),  # 리스트를 문자열로 변환
                    'trailer': trailer_url
                    
                }

                serializer = MovieSerializer(data=save_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
    
    return JsonResponse({'message': 'Movies saved successfully!'})

@api_view(['GET'])
def genre_list(request):
    genres = get_list_or_404(Genre)
    serializers = GenreSerializer(genres, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def movie_list(request):
    movies = get_list_or_404(Movie)
    serializers = MovieSerializer(movies, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    serializer = MovieDetailSerializer(movie)

    if not request.user.is_authenticated:
        print(11111)
        return Response({'data': serializer.data})
    
    else:

        if request.user.is_authenticated and (request.user in movie.pick_users.all()):
            isPicked = True

        else:
            isPicked = False
        cnt = movie.pick_users.count()
        return Response({'data': serializer.data, 'isPicked': isPicked,'pick_user_count':cnt })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_likes(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)

    # 영화 좋아요를 요청하는 유저
    user = request.user

    if user in movie.pick_users.all():
        movie.pick_users.remove(user)
        isPicked=False
    else:
        movie.pick_users.add(user)
        isPicked=True
    cnt = movie.pick_users.count()
    print(isPicked)
    return Response({'message':'success', 'isPicked': isPicked,'pick_user_count':cnt})

# 리뷰 가져오기, 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def review_create_list(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    else:
        reviews = Movie.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

# 리뷰 디테일 보기, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_detail_update_delete(request, movie_id, review_id):
    user = get_object_or_404(User, id=request.user.id)
    movie = get_object_or_404(Movie, pk=movie_id)
    review = get_object_or_404(Review, pk=review_id)

    isLike = False
    if request.user.is_authenticated and (request.user in review.like_users.all()):
        isLike = True

    # 해당 유저가 이 글을 작성한 유저여야 수정할수 있음.
    if review.user == request.user:

        if request.method == 'PUT':
            serializer = ReviewSerializer(review, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            
        elif request.method == 'DELETE':
            review.delete()
            return Response({'message': f'review {review_id} is deleted.'})

        else:
            serializer = ReviewSerializer(review)
            return Response({'data':serializer.data, 'isLike':isLike})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_likes(request, review_id):
    review = Review.objects.get(pk=review_id)

    # 리뷰 좋아요를 요청하는 유저
    user = request.user

    if user in review.like_users.all():
        review.like_users.remove(user)
        
        isLike = False
    else:
        review.like_users.add(user)
        isLike = True

    cnt = review.like_users.count()
    return Response({'message':'success', 'isLike':isLike, 'like_user_count':cnt})

@api_view(['GET'])
# 영화 목록 정렬 (1:최신순, 2:평점순, 3:인기순) # 영화검색 => VUE
def movies_sorted(request, sorted_name):
    if sorted_name == 'new':
        movies = Movie.objects.order_by('-release_date')

    elif sorted_name == 'vote-average':
        movies = Movie.objects.order_by('-vote_average')
    
    elif sorted_name== 'popular':
        movies= Movie.objects.order_by('-popularity')

    serializers = MovieSerializer(movies, many=True)
    return Response(serializers.data)

# 영화 목록 정렬 3:장르별 # 영화검색 => VUE
@api_view(['GET'])
def movies_sorted_genre(request,sorted_name, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)

    if sorted_name == 'new':
        movies = Movie.objects.filter(genres=genre).order_by('-release_date')

    elif sorted_name == 'vote-average':
        movies = Movie.objects.filter(genres=genre).order_by('-vote_average')
    
    elif sorted_name== 'popular':
        movies= Movie.objects.filter(genres=genre).order_by('-popularity')
    serializers = MovieSerializer(movies, many=True)
    return Response(serializers.data)


# 영화 알고리즘 추천 (1:장르별 랜덤 추천, 2: 리뷰 작성 기반 내가 가장 많이 본 장르 추천, 3:팔로잉 유저가 찜한 영화 추천)
@api_view(['GET'])
def algorithm_genre(request):
    genres = list(Genre.objects.all())
    genre_name = ''
    random.shuffle(genres) # 장르 랜덤으로 섞은 후

    if genres:
        selected_genre = genres[0] # 랜덤으로 1개 선택
        genre_name = selected_genre.genre_name
    else:
        return Response({"detail": "No genres available."}, status=status.HTTP_404_NOT_FOUND)
    
    print(selected_genre)
    movies = Movie.objects.filter(genres=selected_genre).order_by('-release_date')

    serializers = MovieSerializer(movies, many=True)
    return Response({'data':serializers.data, 'genre_name':genre_name, 'ranndom':'genre'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def algorithm_review(request):
    # 현재 로그인된 유저를 가져오기
    user = get_object_or_404(User, id=request.user.id)

    is_review = user.reviews.all()
    if not is_review:
        return Response({'message': '아직 작성한 리뷰가 없어요😥 재밌었던 영화 리뷰를 적어보세요!'})

    # 유저가 작성한 리뷰 중 평점이 6점 이상인 리뷰 가져오기
    reviews = user.reviews.filter(rating__gte=6)
    
    # 평점이 6점 이상인 리뷰가 없는 경우
    if not reviews.exists():
        return Response({'message': '평점이 높은 리뷰가 없네요😥 재밌었던 영화 리뷰를 적어보세요!'})
    
    # 평점이 6점 이상인 리뷰 중에서 평점이 가장 높은 리뷰 찾기
    max_rating_review = reviews.aggregate(Max('rating'))
    max_rating = max_rating_review['rating__max']
    highest_rated_reviews = reviews.filter(rating=max_rating)
    
    # 평점이 가장 높은 리뷰가 없는 경우
    if not highest_rated_reviews.exists():
        return Response({'message': '재밌었던 영화 리뷰를 적어보세요😊!'}, status=404)
    
    # 가장 높은 평점을 가진 리뷰 중 하나 선택
    highest_rated_review = highest_rated_reviews.first()
    highest_rated_movie = highest_rated_review.movie
    
    # 같은 장르를 가진 영화 찾기 (현재 영화 제외)
    genres = highest_rated_movie.genres.all()
    similar_genre_movies = Movie.objects.filter(genres__in=genres).exclude(id=highest_rated_movie.id).distinct()
    
    # 장르 이름 리스트 만들기
    genre_lst = [genre.genre_name for genre in genres]
    
    # 영화 데이터를 시리얼라이즈
    serializers = MovieSerializer(similar_genre_movies, many=True)
    
    return Response({
        'data': serializers.data, 
        'genres': genre_lst, 
        'highest_rated_movie': highest_rated_movie.title,
        'highest_rating': max_rating, 'random': 'review'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def algorithm_following(request):
    user = get_object_or_404(User, id=request.user.id)
    
    # 팔로잉한 유저들 가져오기
    following_users = user.followings.all()
    print(following_users)

    if not following_users:
        print(1)
        return Response({'message': '팔로잉한 유저가 없어요!😥 다른 유저를 팔로우하고 찜💗한 영화를 공유해봐요!'})

    # 팔로잉한 유저들의 picked_movies 장르 가져오기
    genre_counter = Counter()
    for following_user in following_users:
        picked_movies = following_user.picked_movies.all()
        for movie in picked_movies:
            for genre in movie.genres.all():
                genre_counter[genre.id] += 1

    # print(genre_counter)
    if not genre_counter:
        return Response({'message': '다양한 유저를 팔로우해봐요😀'}, status=404)

    # 가장 많이 겹치는 장르 찾기
    most_common_genre_id, _ = genre_counter.most_common(1)[0]
    most_common_genre = Genre.objects.get(id=most_common_genre_id)
    # print('genrename', most_common_genre.genre_name, most_common_genre)

    # 해당 장르의 영화 가져오기
    recommended_movies = Movie.objects.filter(genres=most_common_genre).distinct()

    # 영화 데이터를 시리얼라이즈
    serializers = MovieSerializer(recommended_movies, many=True)
    return Response({
        'data': serializers.data,
        'genre_name': most_common_genre.genre_name
    })

@api_view(['GET'])
# 영화 검색 후 영화 가져오기
def search_movie(request, search_name):
    try:
        movie = Movie.objects.get(title=search_name)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)
    
    except Movie.DoesNotExist:
        return Response({'message': '해당 영화를 찾을 수 없습니다.'}, status=404)



@api_view(['POST'])
def genres_names(request):
    genre_names = []
    if request.method == "POST":
        genre_ids = request.data.get('genreIds', [])
        print(genre_ids)
        for id in genre_ids:
            try :
                genre = Genre.objects.get(pk=id)
                genre_names.append(genre.genre_name)
            except ObjectDoesNotExist:
                return Response({'error': f'Genre with ID {id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'genreNames':genre_names})

