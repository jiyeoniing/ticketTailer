<template>
  <div>
    <div class="profile-section">
      <!-- 프로필 정보 -->
      <div class="profile-info" v-if="!showProfileUpdate">
        <div class="profile-image">
          <RouterLink :to="{ name: 'profile', params: { username: userInfo.username } }">
            <img :src="userInfo.profile_img ? `${userStore.API_URL}${userInfo.profile_img}` : userStore.defaultImage" alt="profile_img">
          </RouterLink>
        </div>
        <div class="user-info">
          <h2>{{ userInfo.nickname }}</h2>
          <h4>@{{ userInfo.username }}</h4>
          <h5>팔로잉 : {{ following_count }} / 팔로우 : {{ follower_count }} </h5>
          <div v-if="userInfo.username !== userStore.userName">
            <button @click.prevent="onFollow(userInfo.username)">follow</button>
          </div>
        </div>
      </div>

      <!-- 프로필 수정 폼 -->
      <div>
        <div v-if="userInfo.username === userStore.userName && !showProfileUpdate">
          <button @click.prevent="updateProfile">변경하기</button>
        </div>
        <ProfileUpdate v-if="showProfileUpdate" @close="updateClose" @updateComplete="handleUpdateComplete" :userInfo="userInfo"/>
      </div>
    </div>

    <!-- 내가 쓴 게시글 -->
    <div class="post-section">
      <h2>내가 쓴 게시글</h2>
      <div v-if="userInfo.posts && userInfo.posts.length">
        <ul> <div v-for="post in userInfo.posts" :key="post.id">
          <li><RouterLink :to="{ name: 'PostDetail', params: { postId: post.id } }">{{ post.title }}</RouterLink></li> 
        </div>
      </ul>
      </div>
      <div v-else>
        <p>작성된 게시글이 없습니다.</p>
      </div>
    </div>

    <!-- 내가 쓴 리뷰 -->
    <div class="review-section">
      <h2>내가 쓴 리뷰</h2>
      <div v-if="userInfo.reviews && userInfo.reviews.length">
        <div v-for="review in userInfo.reviews" :key="review.id">
          <h5>
            <ReviewCard  :review="review"/>
            <!-- {{ review.title }}<br>
            {{ review.famous_line }}<br>
            {{ review.content }}<br>
            {{ review.watched_at }}<br>
            {{ review.created_at }}<br>
            {{ review.rating }} -->
          </h5>
        </div>
      </div>
      <div v-else>
        <p>작성된 리뷰가 없습니다.</p>
      </div>
    </div>

    <!-- 내가 찜한 영화 -->
    <div class="picked-movies-section">
      <h2>내가 찜한 영화</h2>
      <div v-if="userInfo.picked_movies && userInfo.picked_movies.length">
        <div v-for="movie in userInfo.picked_movies" :key="movie.id" class="movie-item">
          <MovieItem :movie="movie"/>
        </div>
      </div>
      <div v-else>
        <p>찜한 영화가 없습니다.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/accounts'
import ProfileUpdate from '@/components/ProfileUpdate.vue'
import MovieItem from './MovieItem.vue'
import ReviewCard from '@/components/ReviewCard.vue'

const userStore = useUserStore()
const showProfileUpdate = ref(false)

const props = defineProps({
  userInfo: Object
})

const updateProfile = () => {
  showProfileUpdate.value = true
}

const updateClose = () => {
  showProfileUpdate.value = false
}

const handleUpdateComplete = () => {
  showProfileUpdate.value = false
  userStore.importMyInfo()
}

const following_count = ref(props.userInfo.following_count)
const follower_count = ref(props.userInfo.follower_count)

const onFollow = function(username) {
  axios({
    method: 'POST',
    url: `${userStore.API_URL}/accounts/${username}/follow/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  }).then((response) => {
    following_count.value = response.data.data.following_count
    follower_count.value = response.data.data.follower_count
  }).catch((error) => console.log(error))
}

onMounted(() => {
})

</script>

<style scoped>
.profile-section,
.post-section,
.review-section,
.picked-movies-section {
  margin-bottom: 40px;
}

.profile-info {
  display: flex;
  align-items: center;
}

.profile-image img {
  border-radius: 50%;
  width: 200px;
  height: 200px;
  object-fit: cover;
}

.user-info {
  margin-left: 20px;
}

.movie-item {
  margin-bottom: 10px;
}

h2 {
  font-size: 24px;
  font-family: 'JalnanGothic';
}

p {
  color: #999;
}
</style>
