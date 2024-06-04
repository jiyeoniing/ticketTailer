import { createRouter, createWebHistory } from 'vue-router'
import MainView from '../views/MainView.vue'
import ProfileView from '@/views/ProfileView.vue'
import SignView from '../views/SignView.vue'
import MovieListView from '@/views/MovieListView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import ReviewCreate from '@/components/ReviewCreate.vue'
import ReviewUpdate from '@/components/ReviewUpdate.vue'
import CommunityView from '@/views/CommunityView.vue'
import PostCreateView from '@/components/PostCreate.vue'
import PostListView from '@/components/PostList.vue'
import PostDetailView from '@/components/PostDetail.vue'
import PostUpdateView from '@/components/PostUpdate.vue'
import CommentCreate from '@/components/CommentCreate.vue'
import OpenMovieDetailView from '@/views/OpenMovieDetailView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView
    },
    {
      path: '/sign',
      name: 'sign',
      component: SignView
    },
    {
      path:'/MovieList',
      name: 'MovieList',
      component: MovieListView
    },
    {
      path:'/MovieDetail/:movieId',
      name:'MovieDetail',
      component:MovieDetailView,
    },
    {
      path:'/OpenMovieDetail/:movieId',
      name:'OpenMovieDetail',
      component:OpenMovieDetailView,
    },
    {
      path:'/:movieId/ReviewCreate',
      name:'ReviewCreate',
      component: ReviewCreate,
      props: true
    },
    {
      path:'/:movieId/ReviewUpdate/:reviewId',
      name:'ReviewUpdate',
      component: ReviewUpdate,
    },
    {
      path:'/profile/:username',
      name: 'profile',
      component: ProfileView
    },
    {
      path:'/community',
      name: 'community',
      component: CommunityView,
      children : [ {
        path:'',
        name: 'PostList',
        component: PostListView,
        children:[
          {
            path:'/detail/:postId',
            name:'PostDetail',
            component:PostDetailView,
            children:{
              path:'/CommentCreate/',
              name:'CommentCreate',
              component:CommentCreate
            }
          }
        ]
      },
      {
        path:'/PostCreate',
        name: 'PostCreate',
        component: PostCreateView,
      },
      {
        path:'/update/:postId',
        name: 'PostUpdate',
        component: PostUpdateView
      }]
  }

  ]
})

export default router
