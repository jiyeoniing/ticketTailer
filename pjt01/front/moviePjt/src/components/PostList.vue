<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6">
        <div class="post-list">
          <PostTitle v-for="post in posts" :key="post.id" :post="post" />
        </div>
      </div>
      <div class="col-md-6">
        <RouterView @updateCnt="updateCnt" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import PostTitle from '@/components/PostTitle.vue';
import { usePostStore } from '@/stores/communities';
import { useUserStore } from '@/stores/accounts';

const store = usePostStore();
const userStore = useUserStore();
const posts = ref([]);

const fetchPosts = () => {
  axios({
    method: 'GET',
    url: `${store.API_URL}/communities/posts/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  }).then((response) => {
    posts.value = response.data;
  }).catch((error) => console.log(error));
};

onMounted(() => {
  fetchPosts();
});

const updateCnt = (recommend_user_count, postId) => {
  const index = posts.value.findIndex((post) => post.id === postId);
  if (index !== -1) {
    posts.value[index].recommend_user_count = recommend_user_count;
  }
};
</script>

<style scoped>
.post-list {
  border-right: 1px solid #dee2e6;
  padding-right: 1rem;
}
</style>
