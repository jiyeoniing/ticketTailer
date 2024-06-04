<template>
  <MovieTrailer :movie-trailer="movie.trailer"/>

  <!-- {{userStore.token}} -->

  <div class="container">

    <img class='movie-img' :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" alt="poster">
    

    <div class="movie-detail">
      <h1>{{ movie.title }}</h1>
      <h3 v-if="movie.tagline">{{ movie.tagline }}</h3>

      <div class="pick-container">
  
        <h4 >{{ pick_user_count }}명의 사용자가 "{{ movie.title }}" 를 찜했어요!</h4>
          <p @click.prevent="onPick(movie.id)" >
            <h4 v-if="isPicked">이미 찜했어요!💖</h4>
            <h4 v-else>나도 찜할래요! 🤍</h4>      
          </p>

      </div>

      <br>
      <h2 style="font-family: 'Pretendard-Regular';"> 평점 : {{ movie.vote_average }}</h2>
      <h4> 상영 시간 : {{ movie.runtime }}분</h4>
      <br>
      <hr>

      <h5>감독 : {{ movie.director }}</h5>
      <h5>배우 : {{ truncateActorNames(movie.actors, 8, 20) }}</h5>
      <h5>장르 : {{ genres }}</h5>
      <h5>개봉 : {{ movie.release_date }}</h5>
    </div>
  </div>

  <div class="container">
    <h5 v-if="movie.overview" style="font-size: 30px; margin: 50px 0px 100px 0px;">{{ movie.overview }}</h5>
  </div>

  <hr>
  <br>
  <div class="review">
    <h1 style="text-align: center;">리뷰</h1> 

    <div class="review-header">
      <!-- <div class="review-info"> -->
        <h5>{{ movie.review_count }}개의 리뷰</h5>
      <!-- </div> -->
      <!-- <div class="review-button"> -->
        <button @click.prevent="goReviewCreate(movie.id)">리뷰 작성 하러 가기</button>
      <!-- </div> -->
    </div>

    <div class="review-container">
      <ReviewDetail v-for="review in movie.reviews" :key="review.id" :review="review" :movie-id="movie.id"/>
    </div>


  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/counter'
import { useUserStore } from '@/stores/accounts'
import axios from 'axios'
import MovieTrailer from '@/components/MovieTrailer.vue'
import ReviewDetail from '@/components/ReviewDetail.vue'

const store = useMovieStore()
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()
const movieId = route.params.movieId

const movie = ref({})
const genres = ref(null)
const isPicked = ref(null)
const pick_user_count = ref(null)



  axios({
    method: 'GET',
    url: `${store.API_URL}/movies/${route.params.movieId}/`,
    headers: {
            Authorization: `Token ${userStore.token}`
        }
}).then((response) => {
  console.log(response.data)
    movie.value = response.data.data
    isPicked.value = response.data.isPicked
    pick_user_count.value = response.data.pick_user_count
}).catch((error) => console.log(error))



genres.value = computed(() => {
    return movie.value.genres.map(genre => genre.genre_name).join(', ')
})

const truncateActorNames = (actors, maxCount, maxLength) => {
    const actorArray = actors.split(', ')
    const truncatedNames = actorArray.slice(0, maxCount).map(actor => {
        if (actor.length <= maxLength) {
            return actor
        } else {
            return actor.slice(0, maxLength) + '...'
        }
    }).join(', ')
    return truncatedNames
}

const goReviewCreate = function (movieId) {
  console.log(2222222)
  console.log(1111111, userStore.isLogin)
  if (userStore.isLogin) {
    console.log(33333333)
    router.push({ name: 'ReviewCreate', params: { movieId } })
  } else {
    window.alert('로그인 후 이용가능합니다.')
  }
}

const onPick = function (movieId) {
    axios({
        method: 'POST',
        url: `${store.API_URL}/movies/${movieId}/likes/`,
        headers: {
            Authorization: `Token ${userStore.token}`
        }
    }).then((response) => {
        isPicked.value = response.data.isPicked
        pick_user_count.value = response.data.pick_user_count
    }).catch((error) => console.log(error))
}


</script>

<style scoped>
.container {
  display: flex;
  align-items: flex-start;
  gap: 60px;
}

.movie-img {
  margin-top: 50px;
  width: 400px;
}

.movie-detail {
  margin-top: 50px;
  display: flex;
  flex-direction: column;
}

h1 {
  font-family: 'WavvePADO-Regular';
  font-size: 70px;
}

h3 {
  font-family: 'JalnanGothic';
  font-size: 40px;
}

.review {
  margin: 60px;
  gap:60px;
  flex-direction: column;

}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 20px;
}

/* .review-header h5 {
  margin: 0;
} */

/* .review-info {
  flex: 1;
} */

.review-button {
  margin-left: 20px;
}
</style>
