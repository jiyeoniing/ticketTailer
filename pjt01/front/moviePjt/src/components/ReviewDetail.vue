<template>
  <div class="review-container">
    <div class="review-author">
      <h6 style="font-family: 'JalnanGothic';">{{ review.user.nickname }}</h6>
    <div>
      <RouterLink :to="{ name: 'profile', params: { username: review.user.username } }">
      <img :src="review.user.profile_img ? `${API_URL}${review.user.profile_img}` : userStore.defaultImage" alt="profile_img">
      </RouterLink>
    </div>

    <RouterView/>
      
    </div>
    <div v-if="review.is_opened" class="review-card">
      <div class="review-header">
        <h5>{{ review.title }}</h5>
        <button @click="updateReview">수정하기</button>
      </div>
      <div class="review-body">
        <div class="review-meta">
          <p>평점: <span class="rating">{{ review.rating }}</span></p>
          <p>{{ review.created_at }}</p>
        </div>
        <p class="review-content">{{ review.content }}</p>
        <!-- <p class="review-fame">명언: {{ review.famous_line }}</p> -->
      </div>
      <div class="review-footer">
        <p>{{ like_user_count }}명이 좋아요를 눌렀어요!</p>
        <p @click.prevent="onLike(review.id)" class="like-button">
          <span v-if="isLike">👍 좋아요를 이미 눌렀어요</span>
          <span v-else>👍 좋아요 누르기</span>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
// import {ref} from 'vue'
import { onBeforeRouteLeave } from 'vue-router'
import { ref } from 'vue'
import axios from 'axios'
import { useMovieStore } from '@/stores/counter'
import router from '@/router'
import { useUserStore } from '@/stores/accounts'

const props = defineProps({
  review: Object,
  movieId: Number
})

const store = useMovieStore()
const userStore = useUserStore()
const isLike = ref(null)
const like_user_count = ref(props.review.like_user_count)
const reviewId = props.review.id
const review_username = ref(null)

// 리뷰 가져오기
axios({
  method: 'GET',
  url: `${store.API_URL}/movies/${props.movieId}/reviews/${reviewId}/`,
  headers: {
    Authorization: `Token ${userStore.token}`
  }
}).then((response) => {
  console.log(response.data)
  isLike.value = response.data.isLike
  review_username.value = response.data.data.user.username
}).catch((error) => console.log(error))

const onLike = (reviewId) => {
  axios({
    method: 'POST',
    url: `${store.API_URL}/movies/reviews/${reviewId}/likes/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  }).then((response) => {
    isLike.value = response.data.isLike
    like_user_count.value = response.data.like_user_count
  }).catch((error) => console.log(error))
}

const updateReview = () => {

  if ( review_username.value === userStore.userName ) {
  router.push({ name: 'ReviewUpdate', params: { movieId: props.movieId, reviewId: props.review.id } })
  } else {
    window.alert('작성자만 수정가능합니다.')
  }
}


// onBeforeRouteLeave((to, from) => {
//   if (to.name === "ReviewUpdate" && props.review.user.username !== userStore.userName) {
//     return router.push({name:from.name})
//   }

//   return true;

// })
</script>

<style scoped>

img {
  border-radius: 100%;
  size: 5px;
}
.review-container {
  display: flex;
  align-items: flex-start;
  margin: 20px auto;
  width: 100%;
  max-width: 1200px;
  padding: 0 20px;
  box-sizing: border-box;
}

.review-author {
  margin-right: 20px;
  min-width: 150px;
}

.review-card {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  box-sizing: border-box;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

.review-header h5 {
  margin: 0;
}

.review-header button {
  padding: 5px 10px;
  background-color:#007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.review-header button:hover {
  background-color: hsl(338, 90%, 55%);
}

.review-body {
  margin-bottom: 20px;
}

.review-meta {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-bottom: 10px;
}

.review-meta p {
  margin: 8px 0;
}

.review-content, .review-fame {
  margin-bottom: 10px;
}

.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #eee;
  padding-top: 10px;
}

.like-button {
  cursor: pointer;
}

.like-button span {
  display: block;
}

@media (max-width: 768px) {
  .review-container {
    flex-direction: column;
    align-items: stretch;
  }
  .review-author {
    margin-bottom: 20px;
  }
  .review-meta {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>

