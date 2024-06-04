<template>
  <header>
    <nav v-if="!store.isLogin">
      <RouterLink :to="{name:'main'}" class="logo">TicketTailor</RouterLink>
      <RouterLink :to="{name:'MovieList'}" class="title-text">영화</RouterLink>
      <RouterLink :to="{name:'PostList'}" class="title-text">커뮤니티</RouterLink>
      <RouterLink :to="{name:'sign'}" class="title-text">로그인</RouterLink>
    </nav>
    <nav v-if="store.isLogin">
      <RouterLink :to="{name:'main'}" class="logo">TicketTailor</RouterLink>
      {{ store.userName }}님
      <RouterLink :to="{name:'MovieList'}" class="title-text">영화</RouterLink>
      <RouterLink :to="{name:'PostList'}" class="title-text">커뮤니티</RouterLink>
      <RouterLink :to="{name:'profile', params:{username:store.userName}}" class="title-text">프로필</RouterLink>
      <p @click.prevent="logOut" class="title-text" role="button">로그아웃</p>
    </nav>
  </header>

  <footer>

  </footer>

  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from './stores/accounts'

const store = useUserStore()
const logOut = function() {
  store.logOut()
}

</script>



<style scoped>


nav {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60px;
  background-color: #1c1a1a;
}

.logo {
  font-family: 'WavvePADO-Regular';
  color: hsl(338, 90%, 55%);
  text-decoration: none;
  font-size: x-large;
  margin-right: auto;
  margin-left: 20px;
}

.title-text {
  font-size: larger;
  font-family: 'JalnanGothic';
  color: white;
  text-decoration: none;
  /* padding: 5px 10px; */
  margin: 0 20px;
}

span {
  text-align: center;
  width: 4%;
  color: white;
  border-radius: 100%;
  background-color: red;
}

.title-text[role="button"] {
  cursor: pointer;
  color: white;
  text-decoration: none; 
}
</style>
