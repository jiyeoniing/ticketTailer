<template>
  <div>
    <MovieTrailerList random-name="genre"/>
    <hr>
    <PopularMovieList />
    <br>
    <RandomGenreList random-name="genre"/>

    <RandomReviewRating v-if="userStore.isLogin" random-name="review"/>  
    <RandomFollowing v-if="userStore.isLogin" random-name="following"/> 
 
    <div>
    <RandomGenreList v-if="!userStore.isLogin" random-name="genre"/>
    <h1 style="margin-left: 60px; font-family: 'JalnanGothic'; font-size: 34px" v-if="!userStore.isLogin" >
      로그인 해보세요! <span style="color:hsl(338, 90%, 55%); font-family: 'JalnanGothic';">취향에 맞는 영화</span>를 추천해줄게요!
    </h1>
    </div>


  </div>
</template>

<script setup>
import MovieTrailerList from '@/components/MovieTrailerList.vue';
import PopularMovieList from '@/components/PopularMovieList.vue';
import RandomFollowing from '@/components/RandomFollowing.vue';
import RandomGenreList from '@/components/RandomGenreList.vue';
import RandomReviewRating from '@/components/RandomReviewRating.vue';
import {useUserStore} from '@/stores/accounts';

const userStore = useUserStore()


// 알고리즘 추천 1:장르별 랜덤 추천, 2: 리뷰 작성 기반 내가 가장 많이 본 장르 추천, 3:팔로잉 유저가 찜한 영화 추천
</script>

<style scoped>
@font-face {
    font-family: 'WavvePADO-Regular';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/2404@1.0/WavvePADO-Regular.woff2') format('woff2');
    font-weight: normal;
    font-style: normal;
}

/* 상 우 하 좌 / 상 좌우 하 */

h1 {
  margin: 10px 0px 10px 80px;
  font-family: 'JalnanGothic';
  font-size: 60px;

}

h2 {
  margin: 10px 0px 10px 80px;
  font-family: 'JalnanGothic';
  font-size: 60px;

}
</style>