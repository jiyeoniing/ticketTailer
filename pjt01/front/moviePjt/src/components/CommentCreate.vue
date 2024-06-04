<template>
  <div style="margin-top: 100px;">
      <form @submit.prevent="createPost" class="post-form">
      <div class="form-group">
          <label for="title">제목 : </label>
          <input type="text" name="title" id="title" required v-model="title"/>
      </div>
      <div class="form-group">
          <label for="content">내용 : </label>
          <textarea id="content" name="content" v-model="content"></textarea>
      </div>

      <div class="form-group">
          <input type="submit" value="작성 완료" />
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
const userStore = useUserStore()

const title = ref('')
const content = ref('')
const post_img = ref('')
const data = ref(null)


const createPost = function () {
  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('content', content.value)
  if (post_img.value) {
    formData.append('post_img', post_img.value)
  }

  axios({
    method: "POST",
    url: `${userStore.API_URL}/communities/posts/`,
    headers: {
      Authorization: `Token ${userStore.token}`,
      'Content-Type': 'multipart/form-data'
    },
    data: formData
  })
  .then((response) => {
    console.log(response.data)
    router.push({ name: 'PostList' })
  })
  .catch(err => {
    console.log(err.response.data)
    console.log(err)
  })
}

const onFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (!file.type.startsWith('image/')) {
      alert('이미지 파일을 선택해주세요.')
      event.target.value = '' 
      return
    }
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