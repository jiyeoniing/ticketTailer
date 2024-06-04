<template>
  <div class="profile">
    <div v-if="userInfo">
      <ProfileDetail :userInfo="userInfo"/>
    </div>
  </div>

  
</template>

<script setup>

import ProfileDetail from '@/components/ProfileDetail.vue';
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/accounts';
import axios from 'axios';

const userStore = useUserStore()
const route = useRoute()
const username = route.params.username
console.log(username)

const userInfo = ref([])
userInfo.value = userStore.profile(username)



onMounted(() => {
  axios({
      method: 'get',
      url: `${userStore.API_URL}/accounts/profile/${username}/`,
      headers: { Authorization: `Token ${userStore.token}` }
    })
    .then((response) => {
      console.log(response.data)
      userInfo.value = response.data
    }).catch((error) => {
      console.error(error)
    })

})
</script>




<style scoped>
.profile {
  margin: 100px;
}

/* h1 {
margin: 60px;
font-size:60px;
text-align: center;
font-family: 'JalnanGothic';
}

h3 {
  margin: 60px;
  font-size:60px;
  text-align: center;
  font-family: 'JalnanGothic';
}

img {
  border-radius: 100%;
  size: 10px;
}

h4 {
  font-size: 40px;
  font-family: 'WavvePADO-Regular';
} */


</style>
