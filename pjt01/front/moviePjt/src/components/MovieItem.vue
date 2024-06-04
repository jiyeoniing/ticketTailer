<template>
  <div class="card">
      <div class="card_box">
          <div class="front">
            <img class='movie-img' :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" alt="">
          </div>
          <div class="back">
            <img class='movie-back-img' :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" alt="">
            <div class="text-overlay" @click.prevent="goMovieDetail(movie.id)"><span class="detail-box">상세보기</span></div>        
          </div>
      </div>
  </div>

</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/accounts';

const router = useRouter()
const userStore = useUserStore()

const props = defineProps({
  movie:Object
})


const goMovieDetail = function (movieId) {
  console.log(1111111111111)
  console.log(userStore.isLogin)
  if (userStore.isLogin ){
    router.push({name:'MovieDetail', params:{'movieId':movieId}})
  
  } else {
    router.push({name:'OpenMovieDetail', params:{'movieId':movieId}})
  }
}
</script>

<style scoped>
.movie-img {
  width: 100%;
}

.movie-back-img {
  width: 100%;
  filter: brightness(0.5); /* 0.5는 이미지를 반으로 어둡게 만듭니다. 1보다 작은 값은 어둡게, 1보다 큰 값은 밝게 만듭니다. */
}

*{
    font-size: 20px;
    font-weight:200;
    font-family: 'JalnanGothic';
}

.card {
  margin: 10px;
  padding-bottom: 20px;
}

.card_box{
    width: 250px;
    height: 350px;
    background: #FED6E3;
    transition: .5s;
    transform-style: preserve-3d;
    cursor: pointer;
}
.card_box div{
    width: 100%;
    height: 100%;
    line-height: 350px;
    text-align: center;
    position: absolute;
    backface-visibility: hidden;
}
.back{
    transform: rotateY(180deg);
    color: #fff;
    position: relative;
}
.card:hover .card_box{
    transform: rotateY(180deg);  
}

.text-overlay {
    position: absolute;
    top: 50%; /* 이미지의 상단 중앙에 위치하도록 설정 */
    left: 50%; /* 이미지의 좌측 중앙에 위치하도록 설정 */
    transform: translate(-50%, -50%); /* 텍스트를 가운데로 정렬하기 위한 변환 */
    color: white; /* 텍스트 색상 설정 */
    font-size: 24px; /* 텍스트 크기 설정 */
    /* background-color: rgba(0, 0, 0, 0.5);  */ 
}

.detail-box {
  border: 2px solid white;
  padding: 10px 20px 10px ;
  border-radius: 5px; 
}
</style>