<template>
    <div id="wrap">
      <MovieItem v-for="movie in random_movies" :key="movie.id" :movie="movie"/>
    </div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMovieStore } from '@/stores/counter'
import axios from 'axios'
import MovieItem from '@/components/MovieItem.vue';

const store = useMovieStore()
const random_movies = ref([])
const props = defineProps({
  randomName:String
})

onMounted(() => {
  console.log(props.randomName)
  getRandomMovies(props.randomName)
})

const getRandomMovies = function(randomName) {
  axios({
    method: 'GET',
    url: `${store.API_URL}/movies/algorithm/${randomName}`,
  }).then((response)=>{
    console.log(randomName)
    console.log(response.data[0].genres)
    random_movies.value = response.data.slice(0,10)
    // console.log(random_movies)
  }).catch(error => console.log(error))
}
</script>

<style scoped>
/* .main-img {
} */

#wrap{
    display: flex;
    flex-wrap: wrap;
    gap: 20px; 
    justify-content: space-between;
    position: relative;
}

.scroll-container {
    display: flex;
    overflow-x: auto;
    width: 80%;
    padding: 10px;
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 5px;
    white-space: nowrap;
}

.movie {
  min-width: 100px;
  height: 100px;
  margin-right: 10px;
  background-color: #007bff;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 5px;
  font-size: 24px;
  flex-shrink: 0;
} 


/* .item-box {
  text-align: center;
} */


</style>