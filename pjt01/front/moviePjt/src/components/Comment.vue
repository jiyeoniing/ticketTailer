<template>
  <div class="comment-box">
    <p>작성자 : {{ comment.user.nickname }}</p>
    <div v-if="flag"> 
      <p>댓글 : {{ content  }}</p> 
      <p>작성일자 : {{ created_at }}</p>
      <p>수정일자 : {{ updated_at }}</p>
      <button @click.prevent="onUpdate">댓글 수정</button>
    </div>
    <div v-else> 
      <label for="content">댓글 : </label>
          <textarea id="content" name="content" v-model="content"></textarea>
          <button @click.prevent="onUpdateCompleted()">수정 완료</button>
          <button @click.prevent="onDelete">댓글 삭제</button>
    </div>
    

  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/accounts'

const props = defineProps({
  comment:Object
})

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const flag = ref(true)

const content = ref(props.comment.content)
const created_at = ref(props.comment.created_at.slice(0,10))
const updated_at = ref(props.comment.updated_at.slice(0,10))
// const comment = ref(props.comment)

const onUpdate = function () {
  if (userStore.userName === props.comment.user.username){
    flag.value = false
  } else {
    window.alert('작성자만 수정할 수 있어요!')
  }

}

const onUpdateCompleted= function () {
  axios({
        method:"PUT",
        url: `${userStore.API_URL}/communities/${props.comment.post.id}/comments/${props.comment.id}/`,
        headers: {
        Authorization : `Token ${userStore.token}`
        },
        data:{
          content:content.value
        }
    }).then((response) => {
        console.log(response.data)
        flag.value=true

    }).catch(err => console.log(err))
  
}

const onDelete= function () {
  axios({
        method:"DELETE",
        url: `${userStore.API_URL}/communities/${props.comment.post.id}/comments/${props.comment.id}/`,
        headers: {
        Authorization : `Token ${userStore.token}`
        }
    }).then((response) => {
      console.log(11111)
      fetchData()
      // router.push({ name: 'PostDetail' }).catch(() => { })

      // router.push({'name':'PostDetail', params:{'postId':props.comment.post.id}})

    }).catch(err => console.log(err))
  
}

// fetchData 함수 정의
const fetchData = () => {
  axios({
    method: "GET",
    url: `${userStore.API_URL}/communities/${props.comment.post.id}/comments/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  }).then((response) => {
    window.location.href = '/detail/' + props.comment.post.id;
    // window.location.href = '/postDetail/' + props.comment.post.id;
    // router.push({'name':'PostDetail', params:{'postId':props.comment.post.id}})

    // 댓글 목록을 업데이트합니다.
    // props.comment = response.data 
  }).catch(err => console.log(err))
}

</script>

<style lang="scss" scoped>
.comment-box{
  text-align: left;
  padding-top: 5px;
  border: 1px solid black;
  // margin-bottom: 5px;
  margin: 10px;
}

p {
  margin-left: 10px;
}

button {
  margin-left: 10px;
  margin-bottom: 10px;
}

</style>