<template>

  <div class="video-container">
    <iframe class="video" id="youtube-video" width="600" height="500" :src="movieTrailer+'?enablejsapi=1&autoplay=1&mute=1&controls=0'" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    <!-- <iframe class="video" id="youtube-video" width="560" height="315" :src="movieTrailer+'?enablejsapi=1&autoplay=1&mute=1&controls=0&loop=1&playlist='+movieTrailerId" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe> -->
  </div>

<!-- https://www.youtube.com/embed/2fCh9mSH6gA?enablejsapi=1 -->

</template>

<script setup>
const props = defineProps({
  movieTrailer:String
})

// const movieTrailerId = props.movieTrailer.slice(30)
// console.log(movieTrailerId)

document.addEventListener('DOMContentLoaded', (event) => {
  var tag = document.createElement('script');
  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

  window.onYouTubeIframeAPIReady = function() {
    var player = new YT.Player('youtube-video', {
      events: {
        'onReady': onPlayerReady
      }
    });
  }

  function onPlayerReady(event) {
    event.target.mute(); // 음소거
    event.target.playVideo(); // 자동 재생
    event.target.setLoop(true); // 반복 재생 설정 (API에서 직접 지원하지 않지만 끝나면 다시 시작하도록 설정 가능)
  }
});


</script>

<style coped>
.trailer-size {
  width: 100px;
}

.video-container {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

.video {
  margin-top: 0px;
  width: 100%;
}
</style>