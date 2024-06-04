<template>
  <div class="card movie-card">
    <div class="card_box">
      <div class="front">
        <img class="movie-img" :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" alt="movie poster"  @click.prevent="goMovieDetail(movie.id)">
      </div>
      <div class="back">
        <img class="movie-back-img" :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" alt="movie poster back" @click.prevent="goMovieDetail(movie.id)">
        <div class="text-overlay"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/accounts';

const router = useRouter()
const userStore = useUserStore()

const props = defineProps({
  movie: Object
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
.movie-card {
  width: 300px; /* 너비를 두 배로 조정 */
  height: 400px; /* 높이도 두 배로 조정 */
  margin: 20px;
}

.card_box {
  width: 100%;
  height: 100%;
  transition: transform 0.5s;
  transform-style: preserve-3d;
  position: relative;
  cursor: pointer;
}

.card_box .front,
.card_box .back {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
}

.card_box .back {
  transform: rotateY(180deg);
}

.card:hover .card_box {
  transform: rotateY(180deg);
}

.movie-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.movie-back-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.5);
}

.text-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 24px;
}
</style>
