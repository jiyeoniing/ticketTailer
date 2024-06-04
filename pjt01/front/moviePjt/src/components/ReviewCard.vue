<template>
    <div class="card">
      <div class="card_box">
        <div class="front">
          <img class='movie-img' :src="'https://image.tmdb.org/t/p/w500' + review.movie.poster_path" alt="">
        </div>
        <div class="back">
          <img class='movie-back-img' :src="'https://image.tmdb.org/t/p/w500' + review.movie.poster_path" alt="">
          <div class="text-overlay" @click.prevent="goMovieDetail(review.movie.id)">
            <span>
              <h5 style="font-size: 14px; margin-top: 50px;">제목 - {{ review.title }}</h5>
              <h3 style="font-size: 14px; margin-top: 10px;">내용 - {{ review.content }}</h3>
              <p style="font-size: 14px; ">나의 관람일 - {{ review.watched_at }}</p>
            </span>
          </div>        
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
    review:Object
  })
  
  const goMovieDetail = function (movieId) {
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
    filter: brightness(0.5);
  }
  
  .card {
    margin: 10px;
    padding-bottom: 20px;
  }
  
  .card_box {
    width: 250px;
    height: 380px; /* 카드의 높이를 증가시켰습니다. */
    background: #FED6E3;
    transition: .5s;
    transform-style: preserve-3d;
    cursor: pointer;
  }
  
  .card_box div {
    width: 100%;
    height: 100%;
    line-height: 350px;
    text-align: center;
    position: absolute;
    backface-visibility: hidden;
  }
  
  .back {
    transform: rotateY(180deg);
    color: #fff;
    position: relative;
  }
  
  .card:hover .card_box {
    transform: rotateY(180deg);  
  }
  
  .text-overlay {
    position: absolute;
    top: 50%; 
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 15px;
  }
  
  .detail-box {
    border: 2px solid white;
    padding: 10px 20px 10px ;
    border-radius: 5px; 
  }
  </style>
  