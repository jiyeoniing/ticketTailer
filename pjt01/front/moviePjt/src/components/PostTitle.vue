<template>
  <div class="post-box p-3 mb-3">
    <h5>제목: {{ post.title }}</h5>
    <h6>작성자: {{ post.user.nickname }}</h6>
    <p>{{ post.recommend_user_count }}명 추천</p>
    <button @click.prevent="goDetailLink" class="btn btn-outline-primary btn-sm">상세보기</button>
    <p>작성 일자: {{ created_at }}</p>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/accounts';

const props = defineProps({
  post: Object
});

const userStore = useUserStore();
const created_at = props.post.created_at.slice(0, 10);
const router = useRouter();

const goDetailLink = () => {
  router.push({ name: 'PostDetail', params: { postId: props.post.id } });
};
</script>

<style scoped>
.post-box {
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
  background-color: #f8f9fa;
}
</style>
