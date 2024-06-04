<template>
  <div class="post-box p-4">
    <h6>작성자: {{ post_nickname }}</h6>
    <h5>제목: {{ post.title }}</h5>
    <p>내용: {{ post.content }}</p>
    <p>{{ created_at }}</p>
    <img :src="`${userStore.API_URL}${post_img}`" alt="post_img" class="img-fluid">
    <div>
      <p>{{ recommend_user_count }}명이 추천을 눌렀어요!</p>
      <div @click.prevent="onRecommend(post.id)" class="pointer">
        <p v-if="is_recommend">👍 추천을 취소할래요!</p>
        <p v-else>👍 추천하고 싶어요!</p>
      </div>
      <button @click.prevent="goUpdateLink(post.id)" class="btn btn-primary mt-2">수정하기</button>
    </div>
    <div class="comments-section border p-3 mt-4">
      <h4>댓글창</h4>
      <div class="d-flex align-items-center mb-3">
        <label for="comment" class="me-2">댓글 쓰기</label>
        <input type="text" id="comment" v-model="content" class="form-control" required minlength="2" maxlength="50" />
        <button @click="goCommentCreate(post.id)" class="btn btn-success ms-2">생성</button>
      </div>
      <div>
        <Comment v-for="comment in comments" :key="comment.id" :comment="comment"/>
      </div>
    </div>
  </div>
</template>

<script setup>
import Comment from '@/components/Comment.vue';
import { watch, ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/accounts';
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router';

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();
const post = ref({});
const post_img = ref(null);
const is_recommend = ref(null);
const created_at = ref(null);
const recommend_user_count = ref(null);
const post_username = ref(null);
const content = ref(null);
const comments = ref([]);
const emit = defineEmits(['updateCnt']);
const post_nickname = ref(null)

const fetchData = () => {
  axios({
    method: 'GET',
    url: `${userStore.API_URL}/communities/posts/${route.params.postId}/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  }).then((response) => {
    post.value = response.data.data;
    post_img.value = response.data.data.post_img;
    is_recommend.value = response.data.is_recommend;
    created_at.value = response.data.data.created_at.slice(0, 10);
    recommend_user_count.value = response.data.data.recommend_user_count;
    post_username.value = response.data.data.user.username;
    post_nickname.value = response.data.data.user.nickname
  }).catch((error) => console.log(error));

  axios({
    method: 'GET',
    url: `${userStore.API_URL}/communities/${route.params.postId}/comments/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  }).then((response) => {
    comments.value = response.data;
  }).catch(err => console.log(err));
};

onMounted(() => {
  fetchData();
});

const onRecommend = (postId) => {
  axios({
    method: 'POST',
    url: `${userStore.API_URL}/communities/${postId}/recommend/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  }).then((response) => {
    is_recommend.value = response.data.is_recommend;
    recommend_user_count.value = response.data.recommend_user_count;
    emit('updateCnt', recommend_user_count.value, postId);
  }).catch((error) => console.log(error));
};

const goUpdateLink = (postId) => {
  router.push({ name: 'PostUpdate', params: { postId } });
};

onBeforeRouteLeave((to, from) => {
  if (to.name === 'PostUpdate' && post_username.value !== userStore.userName) {
    return router.push({ name: from.name });
  }
  return true;
});

const goCommentCreate = (postId) => {
  axios({
    method: 'POST',
    url: `${userStore.API_URL}/communities/${postId}/comments/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    },
    data: { content: content.value }
  }).then((response) => {
    content.value = '';
    fetchData();
  }).catch(err => console.log(err));
};
</script>

<style scoped>
.post-box {
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
  background-color: #f8f9fa;
}

.comments-section {
  border-radius: 0.25rem;
  background-color: #fff;
}

.pointer {
  cursor: pointer;
}
</style>
