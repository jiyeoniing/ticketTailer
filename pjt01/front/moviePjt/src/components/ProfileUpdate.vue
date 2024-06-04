<template>
  <div class="profile-update-container">
    <form @submit.prevent="updateMyInfo">
      <div class="image-upload">
        <img :src="previewImage" alt="profile_img" class="profile-img"/>
        <input type="file" @change="onFileChange" class="file-input"/>
      </div>

      <div class="form-group">
        <label for="nickname">닉네임 변경:</label>
        <input type="text" v-model="nickname" placeholder="닉네임" id="nickname" class="form-input"/>
      </div>

      <div class="form-group">
        <label for="password">비밀번호 변경:</label>
        <input type="password" v-model="password" placeholder="비밀번호" id="password" class="form-input"/>
      </div>

      <input type="submit" value="내 정보 변경하기" class="submit-btn">
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useUserStore } from '@/stores/accounts'

const props = defineProps({
  userInfo: Object
})

const emit = defineEmits(['close', 'updateComplete'])

const userStore = useUserStore()

const profile_img = ref(null)
const nickname = ref(props.userInfo.nickname)
const password = ref('')
const previewImage = ref(props.userInfo.profile_img ? `${userStore.API_URL}${props.userInfo.profile_img}` : userStore.defaultImage)

const onFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (!file.type.startsWith('image/')) {
      alert('이미지 파일을 선택해주세요.')
      event.target.value = '' // 파일 입력 리셋
      return
    }
    profile_img.value = file
    previewImage.value = URL.createObjectURL(file)
  }
}

const updateMyInfo = function () {
  userStore.updateMyInfo(profile_img.value, nickname.value, password.value)
  emit('updateComplete')
}

watch(() => props.userInfo, (newUserInfo) => {
  nickname.value = newUserInfo.nickname
  previewImage.value = newUserInfo.profile_img ? `${userStore.API_URL}${newUserInfo.profile_img}` : userStore.defaultImage
})
</script>

<style scoped>
.profile-update-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.profile-img {
  border-radius: 50%;
  width: 150px;
  height: 150px;
  object-fit: cover;
  margin-bottom: 10px;
}

.file-input {
  width: 80%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.form-group {
  width: 100%;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
  width: 80%;
}

.form-input {
  width: 80%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.submit-btn {
  width: 80%;
  padding: 10px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.submit-btn:hover {
  background-color: #0056b3;
}
</style>
