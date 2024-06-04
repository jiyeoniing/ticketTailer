<template>
    <MovieTrailer v-if="movie" :movie-trailer="movie.trailer"/>
</template>

<script setup>
import MovieTrailer from '@/components/MovieTrailer.vue'
import { ref, onMounted } from 'vue'
import { useMovieStore } from '@/stores/counter'
import axios from 'axios'

const store = useMovieStore()
const movie = ref([])


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
    console.log(response)
    movie.value = response.data.data[0]
    console.log(movie.value)
  }).catch(error => console.log(error))
}

</script>

<style coped>

</style>