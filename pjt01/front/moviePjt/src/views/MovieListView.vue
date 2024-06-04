<template>
  <h1>전체 영화 목록</h1>

  <div id="movie-list">
    <select name="sorted" id="sorted-select" class="select-blank" v-model="sortedName" @click.prevent="sortedMovies(sortedName)">
        <option value="new" selected>최신순</option>
        <option value="popular">인기순</option>
        <option value="vote-average">평점순</option>
      </select> 

      <select name="genres" id="genre-select" v-if="store.genres" v-model="genreId" @click.prevent="sortedGenreMovies(sortedName, genreId)">
        <option value="null" selected>전체</option>
        <option v-for="genre in store.genres" :key="genre.id" :value="genre.id">{{genre.genre_name}}</option>    
      </select>
  
      <label for="site-search" style="margin-left: 15px; font-family: 'Pretendard-Regular'; font-size: 20px;"> 영화 제목 검색 : </label>
      <input type="search" id="site-search" name="q" v-model="searchInput" style="margin-left: 5px;" />  
      <button style="font-family: 'Pretendard-Regular'; font-size: 17px;" @click.prevent="getSearchMovie(searchInput)" >검색</button>
  </div>

      <div id="wrap">
        <MovieItem v-for="movie in store.movies" :key="movie.id" :movie="movie"/>
      </div>

  
 
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useMovieStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'
import MovieItem from '@/components/MovieItem.vue'

const sortedName = ref('popular')
const genreId = ref(null)
const store = useMovieStore()
const searchInput = ref(null)

onMounted(() => {
  store.getMovieList()
  store.getGenreList()
})

const sortedMovies = function(sortedName) {
  store.sortedMovies(sortedName)
}

const sortedGenreMovies = function(sortedName, genreId) {
  if (genreId === 'null') {
    store.sortedMovies(sortedName)
  } else {
  store.sortedGenreMovies(sortedName, genreId)
  }

}

const getSearchMovie = function(searchInput) {
  console.log(searchInput)
  store.getSearchMovie(searchInput)
}

</script>

<style scoped>

#movie-list {
  margin: 0px 60px 0px;
}

.select-blank {
  margin-left: 10px;
  margin-right: 10px;
  margin-bottom: 20px;

}

.select {
  margin: 10px;

}

h1 {
  margin: 60px;
  font-size:60px;
  text-align: center;
  font-family: 'JalnanGothic';
}

#wrap{
    display: flex;
    flex-wrap: wrap;
    gap: 20px; 
    justify-content: space-between;
    position: relative;
    margin: 20px 60px 40px;
}

option {
  font-family: 'Pretendard-Regular';
  font-size: 20px;
  margin : 20px;
}

select {
  font-family: 'Pretendard-Regular';
  font-size: 20px;
  margin : 10px;

}
</style>