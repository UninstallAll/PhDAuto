import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'

// 配置axios默认URL
axios.defaults.baseURL = 'http://localhost:8000'

// 创建Vue应用
const app = createApp(App)

// 使用插件
app.use(store)
app.use(router)
app.use(ElementPlus)

// 挂载应用
app.mount('#app') 