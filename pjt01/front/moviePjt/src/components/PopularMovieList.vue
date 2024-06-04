<template>
    <h1 style="margin-left: 60px; font-family: 'JalnanGothic';">TOP 10 영화 </h1>
  
    <div class="movie-list-container">
      <button class="scroll-button left" @click="scrollLeft">
        <i class="bi bi-chevron-left"></i>
      </button>
      <div class="movie-list" ref="movieList">
        <MainMovieItem v-for="movie in popular_movies" :key="movie.id" :movie="movie" class="movie-item"/>
      </div>
      <button class="scroll-button right" @click="scrollRight">
        <i class="bi bi-chevron-right"></i>
      </button>
    </div>
    <br>
    <br>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useMovieStore } from '@/stores/counter'
  import axios from 'axios'
  import MainMovieItem from '@/components/MainMovieItem.vue'
  import 'bootstrap/dist/css/bootstrap.min.css'
  import 'bootstrap-icons/font/bootstrap-icons.css'
  
  const store = useMovieStore()
  const popular_movies = ref([])
  const movieList = ref(null)
  const props = defineProps({
    randomName: String
  })
  
  onMounted(() => {
    getPopularMovies('popular')
  })
  
  const getPopularMovies = function(popular) {
    axios({
      method: 'GET',
      url: `${store.API_URL}/movies/sorted/${popular}/`,
    }).then((response) => {

      // console.log(response.data)

      popular_movies.value = response.data.slice(0, 10)

    }).catch(error => console.log(error))
  }
  
  const scrollLeft = () => {
    movieList.value.scrollBy({
      left: -300,
      behavior: 'smooth'
    })
  }
  
  const scrollRight = () => {
    movieList.value.scrollBy({
      left: 300,
      behavior: 'smooth'
    })
  }
  </script>
  
  <style scoped>
  .movie-list-container {
    display: flex;
    align-items: center;
    position: relative;
  }
  
  .movie-list {
    overflow-x: auto;
    scroll-behavior: smooth;
    width: calc(100% - 80px); /* 양쪽 버튼의 너비를 뺀 나머지 */
    white-space: nowrap;
    padding: 0 50px; /* 버튼과의 간격 확보 */
  }
  
  .movie-item {
    display: inline-block;
    vertical-align: top;
  }
  
  .scroll-button {
    background: none; /* 배경색 제거 */
    border: none; /* 테두리 제거 */
    color: white;
    cursor: pointer;
    font-size: 24px;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    z-index: 1;
  }
  
  .scroll-button.left {
    left: 10px;
  }
  
  .scroll-button.right {
    right: 10px;
  }
  
  .scroll-button:hover {
    color: #000000; /* 호버 시 색상 변경 */
  }
  
  .movie-list::-webkit-scrollbar {
    display: none;
  }
  
  .movie-list {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
  </style>
  