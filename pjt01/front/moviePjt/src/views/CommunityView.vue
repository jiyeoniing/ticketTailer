<template>
  <div class="container">
  <header>
    <nav>
      <CommunityMain />
      <div class="nav-links">
      <RouterLink class="nav-link" :to="{name:'PostList'}">게시글 목록</RouterLink>
      <span>  | </span>
      <RouterLink class="nav-link" :to="{name:'PostCreate'}">게시글 작성</RouterLink>
      </div>
    </nav>
  </header>
</div>

  <RouterView />
</template>

<script setup>
import CommunityMain from '@/components/CommunityMain.vue'

</script>

<style scoped>
.container {
  text-align: center;
  margin-top: 20px;
}

.nav-links {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px; /* 링크 사이의 간격을 설정합니다 */
}

.nav-link {
  font-size: 20px;
  text-decoration: none;
  color: #333;
}

.nav-link:hover {
  color: #007BFF;
  text-decoration: none; /* 링크에 밑줄이 생기지 않도록 합니다 */
}

span {
  font-size: 20px;
}

</style>