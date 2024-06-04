<template>
  <div class="container">
    <h1>{{ isSignUp ? 'Sign Up' : 'Sign In' }}</h1>
    <ul class="links">
      <li>
        <a href="#" id="signin" @click.prevent="toggleSignUp(false)" :class="{ active: !isSignUp }">Sign In</a>
      </li>
      <li>
        <a href="#" id="signup" @click.prevent="toggleSignUp(true)" :class="{ active: isSignUp }">Sign Up</a>
      </li>
    </ul>

    <form @submit.prevent="handleSubmit">
      <div class="input__block" v-if="isSignUp">
        <input type="input" placeholder="닉네임을 입력하세요." class="input" v-model.trim="nickname"/>
      </div>
      <div class="input__block first-input__block">
        <input type="input" placeholder="아이디를 입력하세요." class="input" v-model.trim="username"/>
      </div>
      <div class="input__block">
        <input type="password" placeholder="비밀번호를 입력하세요." class="input" v-model.trim="password"/>
      </div>
      <div class="input__block" v-if="isSignUp">
        <input type="password" placeholder="비밀번호를 다시 입력하세요." class="input" v-model.trim="password2"/>
      </div>

      <button class="signin__btn">{{ isSignUp ? 'Sign Up' : 'Sign In' }}</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/accounts'

const store = useUserStore();
const username = ref('');
const password = ref('');
const password2 = ref('');
const nickname = ref('');
const isSignUp = ref(false);

const signIn = () => {
  const payload = {
    username: username.value,
    password: password.value
  };
  store.signIn(payload);
};

const signUp = () => {
  if (password.value !== password2.value) {
    alert("비밀번호가 다릅니다.");
    return;
  }
  if (password.value.length < 8 || password.value.length > 20) {
    alert("비밀번호가 유효하지 않습니다. 비밀번호는 8자 이상 20자 이하로 입력해주세요.");
    return;
  }
  const payload = {
    nickname: nickname.value,
    username: username.value,
    password: password.value,
    password2: password2.value,
  };
  store.signUp(payload);
};

const handleSubmit = () => {
  if (isSignUp.value) {
    signUp();
  } else {
    signIn();
  }
};

const toggleSignUp = (value) => {
  isSignUp.value = value;
};
</script>

<style scoped>
@font-face {
  font-family: 'WavvePADO-Regular';
  src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/2404@1.0/WavvePADO-Regular.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
}

body {
  font-family: 'WavvePADO-Regular';
  background: white;
}

.container {
  display: block;
  max-width: 680px;
  width: 80%;
  margin: 120px auto;
}

h1 {
  color: #e91e63;
  font-size: 48px;
  letter-spacing: -3px;
  text-align: center;
  margin: 120px 0 80px 0;
  transition: 0.2s linear;
  font-family: 'WavvePADO-Regular';
}


.links {
  display: flex;
  list-style-type: none;
  padding: 0;
  margin: 20px 0;
  font-family: 'WavvePADO-Regular';
}

.links li {
  margin-right: 20px; 
}

.links li:last-child {
  margin-right: 0; 
}

.links li:nth-child(2) {
  opacity: 0.6;
}

.links li:nth-child(2):hover {
  opacity: 1;
}

.links li:nth-child(3) {
  opacity: 0.6;
}

.links li:nth-child(3):hover {
  opacity: 1;
}

.links li a {
  text-decoration: none;
  color: #0f132a;
  font-weight: bolder;
  text-align: center;
  cursor: pointer;
}

.links li a.active {
  color: black;
}

form {
  width: 100%;
  max-width: 680px;
  margin: 40px auto 10px;
}

.input__block {
  margin: 20px auto;
  display: block;
  position: relative;
}

.input__block::before {
  display: none;
  content: "";
  position: absolute;
  top: -15px;
  left: 50px;
  display: block;
  width: 0;
  height: 0;
  background: transparent;
  border-left: 15px solid transparent;
  border-right: 15px solid transparent;
  transition: 0.2s linear;
}

.signup-input__block::before {
  left: 150px;
}

.input__block input {
  display: block;
  width: 90%;
  max-width: 680px;
  height: 50px;
  margin: 0 auto;
  border-radius: 8px;
  border: none;
  background: rgba(15, 19, 42, 0.1);
  color: rgba(15, 19, 42, 0.3);
  padding: 0 0 0 15px;
  font-size: 14px;
  font-family: 'Pretendard-Regular';
}

.input__block input:focus,
.input__block input:active {
  outline: none;
  border: none;
  color: rgba(15, 19, 42, 1);
}

.input__block input.hidden__nickname,
.input__block input.hidden__password {
  opacity: 0;
  display: none;
  transition: 0.2s linear;
}

.signin__btn {
  background: #e91e63;
  color: white;
  display: block;
  width: 92.5%;
  max-width: 680px;
  height: 50px;
  border-radius: 8px;
  margin: 0 auto;
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-family: 'WavvePADO-Regular';
  box-shadow: 0 15px 30px rgba(233, 30, 99, 0.36);
  transition: 0.2s linear;
}

.signin__btn:hover {
  box-shadow: 0 0 0 rgba(233, 30, 99, 0.0);
}

.separator {
  display: block;
}
</style>
