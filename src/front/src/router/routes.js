
import { productName } from "../../package.json";


const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '',name:`${productName}`, component: () => import('pages/IndexPage.vue') }
      ,
      { path: '/calls', name:`Звонки -- ${productName}`,component: () => import('pages/BlindPages.vue')}
      ,
      { path: '/vocabulary', name:`Логический анализ -- ${productName}`,component: () => import('pages/BlindPages.vue')}
      ,
      { path: '/statistic', name:`Статистика -- ${productName}`,component: () => import('pages/StatisticsPages.vue')}
      ,
      { path: '/dash', name:`Дашборд -- ${productName}`,component: () => import('pages/DashboardPages.vue')}
      ,
      { path: '/sunBox', name:`sb -- ${productName}`,component: () => import('pages/sunBox.vue')}
    ]
  },

  // Always leave this as last one,
  // but you can also remove it 
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
