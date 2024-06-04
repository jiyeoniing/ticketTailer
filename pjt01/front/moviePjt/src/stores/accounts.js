import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

// default 이미지 경로 설정
import defaultImage from '@/assets/default_image.jpg'

export const useUserStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const userName = ref(null)
  const following_count = ref(null)
  const follower_count = ref(null)
  const post_count = ref(null)
  const comment_count = ref(null)
  const posts = ref(null)
  const pickedMovies = ref(null)
  const reviews = ref(null)
  const userInfo = ref([])
  // const isLogin = ref(false)

  const router = useRouter()
  const isLogin = computed(() => {
    return token.value !== null
  })
  
  const signUp = function (payload) {
    const { nickname, username, password, password2 } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: { nickname, username, password, password2 }
    })
    .then(() => {
      signIn({ username, password })
    })
    .catch((error) => {
      alert(error.response.data.error)
    })
  }

  const signIn = function (payload) {
    const { username, password } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: { username, password }
    })
    .then((response) => {
      userName.value = response.data.username
      token.value = response.data.token
      // isLogin.value = true
      router.push({ name: 'main' })
    })
    .catch((error) => {
      alert(error.response.data.error)
    })
  }

  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
      headers: { Authorization: `Token ${token.value}` }
    })
    .then(() => {
      token.value = null
      router.push({ name: 'main' })
    })
    .catch((error) => {
      console.error(error)
    })
  }

  const profile_img = ref(null)
  const nickname = ref('')
  const password = ref('')

  const importMyInfo = () => {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/my-info/`,
      headers: { Authorization: `Token ${token.value}` }
    })
    .then((response) => {
      profile_img.value = response.data.profile_img ? `${API_URL}${response.data.profile_img}` : defaultImage
      nickname.value = response.data.nickname
      password.value = response.data.password
      window.location.href='/profile/'+ userName.value;
      // router.push({ name: 'profile' })
    })
    .catch((error) => {
      console.error(error)
    })
  }

  const updateMyInfo = (profile_img, nickname, password) => {
    const formData = new FormData()
    formData.append('nickname', nickname)
    formData.append('password', password)
    if (profile_img instanceof File) {
      formData.append('profile_img', profile_img)
    }

    axios({
      method: 'put',
      url: `${API_URL}/accounts/my-info/`,
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Token ${token.value}`
      }
    })
    .then(() => {
      importMyInfo()
    })
    .catch((error) => {
      alert(error.response.data.error)
    })
  }

  const profile = (username) => {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/profile/${username}/`,
      headers: { Authorization: `Token ${token.value}` }
    })
    .then((response) => {
      console.log(response.data)
      profile_img.value = response.data.profile_img ? `${API_URL}${response.data.profile_img}` : defaultImage
      following_count.value = response.data.following_count
      follower_count.value = response.data.follower_count
      post_count.value = response.data.post_count
      comment_count.value = response.data.comment_count
      posts.value = response.data.posts
      pickedMovies.value = response.data.pickedMovies
      reviews.value = response.data.reviews
    }).catch((error) => {
      console.error(error)
    })
  }

  return { API_URL, userName, signUp, signIn, logOut, token, isLogin, importMyInfo, updateMyInfo, profile_img, nickname, password, profile, following_count, follower_count, post_count, comment_count, posts, pickedMovies, reviews, defaultImage }
}, { persist: true })
