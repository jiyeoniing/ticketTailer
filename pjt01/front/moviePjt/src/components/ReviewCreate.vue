<template>
    <h1>리뷰 작성</h1>
    <div style="margin-top: 100px;">
        <form @submit.prevent="createReview" action="" method="get" class="review-form">
        <div class="form-group">
            <label for="title">제목 : </label>
            <input type="text" name="title" id="title" required v-model="title"/>
        </div>
        <div class="form-group">
            <label for="famouse-line">명대사 : </label>
            <input type="famouse-line" name="famouse-line" id="famouse-line" required v-model="famousLine"/>
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
            <input type="date" name="watched-at" id="watched-at" required v-model="watchedAt"/>
        </div>
        <div class="form-group">
            <label for="is_opened">공개 여부</label>
            <input type="checkbox" name="is_opened" id="is_opened" required v-model="isOpened"/>
        </div>

        <div class="form-group">
            <input type="submit" value="작성 완료" />
        </div>
        </form>
    </div>
  </template>
  
  <script setup>
  import axios from 'axios'
    import { ref } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    import { useMovieStore } from '@/stores/counter'
    import { useUserStore } from '@/stores/accounts'

// const props = defineProps({
//     movieId:Int16Array
// })

  const route = useRoute()
  const router = useRouter()
  const store = useMovieStore()
  const userStore = useUserStore()


  const title = ref(null)
  const famousLine = ref(null)
  const content = ref(null)
  const watchedAt = ref(null)
  const isOpened = ref(null)
  const rating = ref(null)


  console.log(route.params.movieId)

  const createReview = function () {
    axios({
        method:"POST",
        url: `${store.API_URL}/movies/${route.params.movieId}/reviews/`,
        headers: {
        Authorization : `Token ${userStore.token}`
        },
        data : {
            title:title.value,
            famous_line:famousLine.value,
            content:content.value,
            watched_at:watchedAt.value,
            is_opened:isOpened.value,
            rating:rating.value
        }
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