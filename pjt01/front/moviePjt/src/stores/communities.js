import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const usePostStore = defineStore('counter', () => {
  const posts = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  

  const getPostList = function() {
    axios({
      method:'GET',
      url: `${API_URL}/posts/`,

    }).then((response)=>{
      posts.value = response.data
    }).catch(error => console.log(error))
  }

  return {
    API_URL, getPostList, posts,
  }
})
