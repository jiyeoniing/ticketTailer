import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMovieStore = defineStore('counter', () => {
  const movies = ref([])
  const genres = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  const getMovieList = function() {
    axios({
      method:'GET',
      url: `${API_URL}/movies/`,

    }).then((response)=>{
      movies.value = response.data
    }).catch(error => console.log(error))
  }

  const getGenreList = function() {
    axios({
      method: 'GET',
      url: `${API_URL}/movies/genres/`,

    }).then((response)=>{
      genres.value = response.data
    }).catch(error => console.log(error))
  }

  // 최신순new 인기순 평점순 정렬
  const sortedMovies = function(sortedName) {
    axios({
      method: 'GET',
      url: `${API_URL}/movies/sorted/${sortedName}/`,
    }).then((response)=>{
      console.log(sortedName)
      movies.value = response.data
    }).catch(error => console.log(error))
  }

  // 장르별 정렬 => 장르아이디 이용
  const sortedGenreMovies = function(sortedName, genreId) {
    if (genreId === null) {
      axios({
        method: 'GET',
        url: `${API_URL}/movies/sorted/${sortedName}/`,
      }).then((response)=>{
        console.log(genreId)
        movies.value = response.data
      }).catch(error => console.log(error))
    } else {
 
    axios({
      method: 'GET',
      url: `${API_URL}/movies/sorted/${sortedName}/genre/${genreId}/`,
    }).then((response)=>{
      console.log(genreId)
      movies.value = response.data
    }).catch(error => console.log(error)
      )}
  }

  // 영화 검색 후 보여주기
  const search_movie = ref([])
  const getSearchMovie = function(searchInput) {
    console.log(searchInput)
    axios({
      method: 'GET',
      url: `${API_URL}/movies/search/${searchInput}/`,
    }).then((response)=>{
      console.log(response)
      movies.value = [response.data]
    }).catch(error => console.log(error))
  }

  const genre_names = ref([])

  // 장르아이디들 받으면 장르 이름 출력
  const getGenreNames = function (genreIds) {
    axios({
      method: 'POST',
      url: `${API_URL}/movies/genres/names/`,
      data: {genreIds},
      headers: { 'Content-Type': 'application/json' } 
    })
      .then((response) => {
        console.log(response.data.genreNames)
        genre_names.value = response.data.genreNames
      })
      .catch((error) => console.log(error));
  };

  return {
    API_URL, getMovieList, movies, getGenreList, genres, 
    sortedMovies, sortedGenreMovies, genre_names, 
    getGenreNames, getSearchMovie, search_movie, 
  }
})
