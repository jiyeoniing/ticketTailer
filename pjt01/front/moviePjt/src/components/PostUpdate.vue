<template>
  <div style="margin-top: 100px;">
      <form class="post-form">
      <div class="form-group">
          <label for="title">제목 : </label>
          <input type="text" name="title" id="title" required v-model="title"/>
      </div>
      <div class="form-group">
          <label for="content">내용 : </label>
          <textarea id="content" name="content" v-model="content"></textarea>
      </div>
      <div class="form-group">
          <label for="post_img">사진 첨부</label>
          <input type="file" id="post_img" @change="onFileChange" />

      </div>

      <div class="form-group">
          <input style="margin-bottom: 10px;" type="submit" @click.prevent="goUpdate" value="수정 완료" />
          <input type="submit" @click.prevent="goDelete" value="삭제" />
      </div>
      </form>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/accounts'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()


const title = ref('')
const content = ref('')
const post_img = ref('')
const data = ref(null)

// 원래 게시글 가져오기
axios({ 
  method:'GET',
  url: `${userStore.API_URL}/communities/posts/${route.params.postId}/`,
  headers: {
    Authorization : `Token ${userStore.token}`
  }
}).then((response) => {
  console.log(response.data)

  title.value = response.data.data.title
  content.value = response.data.data.content
  post_img.value = response.data.post_img

}).catch((error)=> console.log(error))


const goUpdate = function () {

  axios({
      method:"PUT",
      url: `${userStore.API_URL}/communities/posts/${route.params.postId}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      },
      data : {
          title:title.value,
          content:content.value,
          post_img:post_img.value,
      }
  }).then((response) => {
      console.log(response.data)
      router.push({name:'PostList'})
  }).catch(err => {
    console.log(err)
  })
}

const goDelete = function () {

  axios({
      method:"DELETE",
      url: `${userStore.API_URL}/communities/posts/${route.params.postId}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      },
  }).then((response) => {
      console.log(response.data)
      router.push({name:'PostList'})
  }).catch(err => {
    console.log(err)
  })
}

const onFileChange = (event) => {
    const file = event.target.files[0]
    if (file) {
      post_img.value = file
    }
  }
  

</script>

<style scoped>
.post-form {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}


.form-group label {
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
}

.form-group textarea {
  resize: vertical;
  height: 100px;
}



</style>