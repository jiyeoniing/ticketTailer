<template>
  <h1>리뷰 수정</h1>
  <div style="margin-top: 100px;">
      <form class="review-form">
      <div class="form-group">
          <label for="title">제목 :</label>
          <input type="text" name="title" id="title" required v-model="title"/>
      </div>
      <div class="form-group">
          <label for="famouse-line">명대사 : </label>
          <input type="famouse-line" name="famouse-line" id="famouse-line" required v-model="famous_line"/>
      </div>
      <div class="form-group">
          <label for="rating">평점 : </label>
          <input type="number" name="rating" id="rating" min="0" max="10" required v-model="rating"/>
      </div>
      <div class="form-group">
          <label for="content">리뷰 내용 : </label>
          <textarea id="content" name="content" v-model="content"></textarea>
      </div>
      <div class="form-group">
          <label for="watched-at">관람일</label>
          <input type="date" name="watched-at" id="watched-at" required v-model="watched_at"/>
      </div>
      <div class="form-group">
          <label for="is_opened">공개 여부</label>
          <input type="checkbox" name="is_opened" id="is_opened" required v-model="is_opened"/>
      </div>

      <div class="form-group">
          <input @click.prevent="goUpdate" type="submit" value="수정 완료" style="margin-bottom: 10px;"/>
          <input @click.prevent="goDelete" type="submit" value="삭제" />
      </div>
      </form>
  </div>
</template>

<script setup>
  import axios from 'axios'
  import { ref, onBeforeMount, onMounted} from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useMovieStore } from '@/stores/counter'
  import { useUserStore } from '@/stores/accounts'

const route = useRoute()
const router = useRouter()
const store = useMovieStore()
const userStore = useUserStore()

const title = ref('111')
const famous_line = ref(null)
const content = ref(null)
const watched_at = ref(null)
const is_opened = ref(null)
const rating = ref(null)

console.log(11, route.params.reviewId)
console.log(route.params)

onMounted(() => {
  console.log(1111, title.value)
  title.value = '582'

  axios({
      method:"GET",
      url: `${store.API_URL}/movies/${route.params.movieId}/reviews/${route.params.reviewId}/`,
      headers: {
      Authorization : `Token ${userStore.token}`
      }
  }).then((response) => {
      console.log(response.data)
      title.value=response.data.data.title
      famous_line.value = response.data.data.famous_line
      content.value=response.data.data.content
      watched_at.value =response.data.data.watched_at
      is_opened.value =response.data.data.is_opened
      rating.value=response.data.data.rating
      }).catch(err => console.log(err))


})


      // 수정 
  const goUpdate= function () {
    axios({
        method:"PUT",
        url: `${store.API_URL}/movies/${route.params.movieId}/reviews/${route.params.reviewId}/`,
        headers: {
        Authorization : `Token ${userStore.token}`
        },
        data : {
            title:title.value,
            famous_line:famous_line.value,
            content:content.value,
            watched_at:watched_at.value,
            is_opened:is_opened.value,
            rating:rating.value
        }
    }).then((response) => {
        console.log(response.data)
        router.push({name:'MovieDetail', params:{movieId:route.params.movieId}})
    }).catch(err => console.log(err))
  }

      // 삭제
  const goDelete = function () {
    axios({
        method:"DELETE",
        url: `${store.API_URL}/movies/${route.params.movieId}/reviews/${route.params.reviewId}/`,
        headers: {
        Authorization : `Token ${userStore.token}`
        },
      }).then((response) => {
          console.log(response.data)
          router.push({name:'MovieDetail', params:{movieId:route.params.movieId}})
      }).catch(err => console.log(err))
  }
</script>

<style scoped>

h1 {
  margin: 60px;
  font-size:60px;
  text-align: center;
  font-family: 'JalnanGothic';
}

.review-form {
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

.form-group-inline {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 15px;
}

.form-group-inline input[type="checkbox"] {
  margin-right: 10px;
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

.submit-form {
  display: flex;
  justify-content: flex-end;
}

.submit-form input[type="submit"] {
  padding: 10px 20px;
  font-size: 1rem;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-form input[type="submit"]:hover {
  background-color: #0056b3;
}



</style>