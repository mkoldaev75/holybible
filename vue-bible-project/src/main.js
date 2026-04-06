import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './index.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: () => import('./components/BookList.vue') },
    { path: '/:bookDir', component: () => import('./components/ChapterList.vue'), props: true },
    { path: '/:bookDir/:chapter', component: () => import('./components/ChapterView.vue'), props: true },
  ],
  scrollBehavior() {
    return { top: 0 }
  }
})

createApp(App).use(router).mount('#app')
