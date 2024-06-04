<template>
    <h1 style="margin-left: 60px; font-family: 'JalnanGothic';" v-if="genre_name">오늘의 영화 장르 추천!!
      <span style="color:hsl(338, 90%, 55%); font-family: 'JalnanGothic';">{{ genre_name }}</span>
    </h1>
  
    <div class="movie-list-container">
      <button class="scroll-button left" @click="scrollLeft">
        <i class="bi bi-chevron-left"></i>
      </button>
      <div class="movie-list" ref="movieList">
        <MainMovieItem v-for="movie in random_movies" :key="movie.id" :movie="movie" class="movie-item"/>
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
  import { useUserStore } from '@/stores/accounts'
  import axios from 'axios'
  import MainMovieItem from '@/components/MainMovieItem.vue'
  import 'bootstrap/dist/css/bootstrap.min.css'
  import 'bootstrap-icons/font/bootstrap-icons.css'
  
  const store = useMovieStore()
  const userStore = useUserStore()
  const random_movies = ref([])
  const genre_name = ref(null)
  const movieList = ref(null)
  const props = defineProps({
    randomName: String
  })
  
  onMounted(() => {
    console.log(props.randomName)
    getRandomMovies(props.randomName)
  })
  
  const getRandomMovies = function(randomName) {
    axios({
      method: 'GET',
      url: `${store.API_URL}/movies/algorithm/${randomName}/`,
    }).then((response) => {
      // random_movies.value = response.data.data.slice(0, 10)
      if (random_movies.value ) {
        random_movies.value = response.data.data.slice(0, 10)
        genre_name.value = response.data.genre_name
      } else {
        getRandomMovies(randomName)
      }
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
  