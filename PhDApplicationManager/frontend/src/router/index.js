import { createRouter, createWebHistory } from 'vue-router'

// 导入视图组件
const Home = () => import('../views/Home.vue')
const SchoolList = () => import('../views/school/SchoolList.vue')
const SchoolDetail = () => import('../views/school/SchoolDetail.vue')
const ProfessorList = () => import('../views/professor/ProfessorList.vue')
const ProfessorDetail = () => import('../views/professor/ProfessorDetail.vue')
const ApplicationList = () => import('../views/application/ApplicationList.vue')
const ApplicationDetail = () => import('../views/application/ApplicationDetail.vue')
const EmailList = () => import('../views/email/EmailList.vue')
const EmailCompose = () => import('../views/email/EmailCompose.vue')
const DocumentList = () => import('../views/document/DocumentList.vue')
const Search = () => import('../views/search/Search.vue')
const Settings = () => import('../views/settings/Settings.vue')
const NotFound = () => import('../views/NotFound.vue')

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: '首页' }
  },
  {
    path: '/schools',
    name: 'SchoolList',
    component: SchoolList,
    meta: { title: '学校列表' }
  },
  {
    path: '/schools/:id',
    name: 'SchoolDetail',
    component: SchoolDetail,
    props: true,
    meta: { title: '学校详情' }
  },
  {
    path: '/professors',
    name: 'ProfessorList',
    component: ProfessorList,
    meta: { title: '导师列表' }
  },
  {
    path: '/professors/:id',
    name: 'ProfessorDetail',
    component: ProfessorDetail,
    props: true,
    meta: { title: '导师详情' }
  },
  {
    path: '/applications',
    name: 'ApplicationList',
    component: ApplicationList,
    meta: { title: '申请列表' }
  },
  {
    path: '/applications/:id',
    name: 'ApplicationDetail',
    component: ApplicationDetail,
    props: true,
    meta: { title: '申请详情' }
  },
  {
    path: '/emails',
    name: 'EmailList',
    component: EmailList,
    meta: { title: '邮件列表' }
  },
  {
    path: '/emails/compose',
    name: 'EmailCompose',
    component: EmailCompose,
    meta: { title: '撰写邮件' }
  },
  {
    path: '/documents',
    name: 'DocumentList',
    component: DocumentList,
    meta: { title: '文档列表' }
  },
  {
    path: '/search',
    name: 'Search',
    component: Search,
    meta: { title: '信息检索' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { title: '设置' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { title: '页面未找到' }
  }
]

// 创建路由
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 全局前置守卫 - 设置页面标题
router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - PhD Application Manager` : 'PhD Application Manager'
  next()
})

export default router 