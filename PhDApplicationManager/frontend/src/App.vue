<template>
  <div id="app">
    <el-config-provider :locale="locale">
      <el-container class="layout-container">
        <el-header class="main-header">
          <div class="logo">
            <img src="./assets/logo.png" alt="Logo" class="logo-img" />
            <h1>PhD Application Manager</h1>
          </div>
          <div class="header-right">
            <el-badge :value="unreadNotifications" :max="99" class="notification-badge" v-if="unreadNotifications > 0">
              <el-button type="info" icon="Bell" circle @click="showNotifications"></el-button>
            </el-badge>
            <el-button type="info" icon="Bell" circle v-else @click="showNotifications"></el-button>
          </div>
        </el-header>
        
        <el-container>
          <el-aside width="240px" class="main-sidebar">
            <el-menu
              :default-active="activeMenu"
              class="sidebar-menu"
              background-color="#304156"
              text-color="#bfcbd9"
              active-text-color="#409EFF"
              router
            >
              <el-menu-item index="/">
                <el-icon><HomeFilled /></el-icon>
                <span>首页</span>
              </el-menu-item>
              
              <el-menu-item index="/schools">
                <el-icon><School /></el-icon>
                <span>学校</span>
              </el-menu-item>
              
              <el-menu-item index="/professors">
                <el-icon><User /></el-icon>
                <span>导师</span>
              </el-menu-item>
              
              <el-menu-item index="/applications">
                <el-icon><Document /></el-icon>
                <span>申请记录</span>
              </el-menu-item>
              
              <el-menu-item index="/emails">
                <el-icon><Message /></el-icon>
                <span>邮件</span>
              </el-menu-item>
              
              <el-menu-item index="/documents">
                <el-icon><Files /></el-icon>
                <span>文档</span>
              </el-menu-item>
              
              <el-menu-item index="/search">
                <el-icon><Search /></el-icon>
                <span>信息检索</span>
              </el-menu-item>
              
              <el-menu-item index="/settings">
                <el-icon><Setting /></el-icon>
                <span>设置</span>
              </el-menu-item>
            </el-menu>
          </el-aside>
          
          <el-container>
            <el-main class="main-content">
              <router-view v-slot="{ Component }">
                <transition name="fade" mode="out-in">
                  <component :is="Component" />
                </transition>
              </router-view>
            </el-main>
            
            <el-footer class="main-footer">
              PhD Application Manager &copy; {{ currentYear }} | 版本 1.0.0
            </el-footer>
          </el-container>
        </el-container>
      </el-container>
      
      <!-- 通知抽屉 -->
      <el-drawer
        v-model="notificationDrawer"
        title="通知"
        direction="rtl"
        size="30%"
      >
        <el-tabs v-model="notificationsTab">
          <el-tab-pane label="未读通知" name="unread">
            <el-empty description="没有未读通知" v-if="notifications.unread.length === 0"></el-empty>
            <el-scrollbar height="calc(100vh - 200px)" v-else>
              <div v-for="notification in notifications.unread" :key="notification.id" class="notification-item">
                <div class="notification-header">
                  <h3>{{ notification.title }}</h3>
                  <el-tag size="small" :type="getNotificationTagType(notification.type)">{{ notification.type }}</el-tag>
                </div>
                <p>{{ notification.content }}</p>
                <div class="notification-footer">
                  <span class="notification-time">{{ formatTime(notification.created_at) }}</span>
                  <el-button type="primary" size="small" @click="markNotificationAsRead(notification.id)">
                    标记为已读
                  </el-button>
                </div>
              </div>
            </el-scrollbar>
          </el-tab-pane>
          
          <el-tab-pane label="所有通知" name="all">
            <el-empty description="没有通知" v-if="notifications.all.length === 0"></el-empty>
            <el-scrollbar height="calc(100vh - 200px)" v-else>
              <div v-for="notification in notifications.all" :key="notification.id" class="notification-item" :class="{ 'read': notification.is_read }">
                <div class="notification-header">
                  <h3>{{ notification.title }}</h3>
                  <el-tag size="small" :type="getNotificationTagType(notification.type)">{{ notification.type }}</el-tag>
                </div>
                <p>{{ notification.content }}</p>
                <div class="notification-footer">
                  <span class="notification-time">{{ formatTime(notification.created_at) }}</span>
                  <el-button 
                    v-if="!notification.is_read" 
                    type="primary" 
                    size="small" 
                    @click="markNotificationAsRead(notification.id)"
                  >
                    标记为已读
                  </el-button>
                </div>
              </div>
            </el-scrollbar>
          </el-tab-pane>
        </el-tabs>
      </el-drawer>
    </el-config-provider>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { HomeFilled, School, User, Document, Message, Files, Search, Setting, Bell } from '@element-plus/icons'
import zhCn from 'element-plus/lib/locale/lang/zh-cn'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import moment from 'moment'

export default {
  name: 'App',
  components: {
    HomeFilled,
    School,
    User,
    Document,
    Message,
    Files,
    Search,
    Setting,
    Bell
  },
  setup() {
    const route = useRoute()
    const locale = ref(zhCn)
    const activeMenu = computed(() => route.path)
    const currentYear = new Date().getFullYear()
    
    // 通知相关
    const notificationDrawer = ref(false)
    const notificationsTab = ref('unread')
    const unreadNotifications = ref(0)
    const notifications = ref({
      unread: [],
      all: []
    })
    
    // 获取未读通知
    const fetchUnreadNotifications = async () => {
      try {
        const response = await axios.get('http://localhost:8000/notifications?is_read=false')
        notifications.value.unread = response.data
        unreadNotifications.value = response.data.length
      } catch (error) {
        console.error('获取未读通知失败', error)
      }
    }
    
    // 获取所有通知
    const fetchAllNotifications = async () => {
      try {
        const response = await axios.get('http://localhost:8000/notifications')
        notifications.value.all = response.data
      } catch (error) {
        console.error('获取所有通知失败', error)
      }
    }
    
    // 标记通知为已读
    const markNotificationAsRead = async (notificationId) => {
      try {
        await axios.put(`http://localhost:8000/notifications/${notificationId}/read`)
        // 更新通知列表
        fetchUnreadNotifications()
        fetchAllNotifications()
        ElMessage.success('已标记为已读')
      } catch (error) {
        console.error('标记通知失败', error)
        ElMessage.error('标记通知失败')
      }
    }
    
    // 显示通知抽屉
    const showNotifications = () => {
      notificationDrawer.value = true
      // 当打开通知抽屉时，获取所有通知
      fetchAllNotifications()
    }
    
    // 获取通知标签类型
    const getNotificationTagType = (type) => {
      const types = {
        '截止日期': 'danger',
        '邮件回复': 'success',
        '申请状态变更': 'warning'
      }
      return types[type] || 'info'
    }
    
    // 格式化时间
    const formatTime = (time) => {
      return moment(time).format('YYYY-MM-DD HH:mm')
    }
    
    // 定期检查截止日期
    const checkDeadlines = async () => {
      try {
        await axios.post('http://localhost:8000/notifications/check-deadlines')
        // 刷新未读通知
        fetchUnreadNotifications()
      } catch (error) {
        console.error('检查截止日期失败', error)
      }
    }
    
    // 组件挂载时获取通知
    onMounted(() => {
      fetchUnreadNotifications()
      // 每小时检查一次截止日期
      setInterval(checkDeadlines, 3600 * 1000)
      // 每10分钟刷新一次未读通知
      setInterval(fetchUnreadNotifications, 600 * 1000)
    })
    
    // 监听通知抽屉关闭
    watch(notificationDrawer, (newVal) => {
      if (!newVal) {
        // 当通知抽屉关闭时，重置标签页到未读通知
        notificationsTab.value = 'unread'
      }
    })
    
    return {
      locale,
      activeMenu,
      currentYear,
      notificationDrawer,
      notificationsTab,
      unreadNotifications,
      notifications,
      showNotifications,
      markNotificationAsRead,
      getNotificationTagType,
      formatTime
    }
  }
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.layout-container {
  height: 100vh;
}

.main-header {
  background-color: #ffffff;
  color: #333;
  line-height: 60px;
  display: flex;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
  position: relative;
  z-index: 10;
}

.logo {
  display: flex;
  align-items: center;
}

.logo-img {
  height: 40px;
  margin-right: 10px;
}

.header-right {
  display: flex;
  align-items: center;
}

.notification-badge {
  margin-right: 10px;
}

.main-sidebar {
  background-color: #304156;
  box-shadow: 2px 0 6px rgba(0,21,41,.35);
}

.sidebar-menu {
  border-right: none;
  height: 100%;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}

.main-footer {
  background-color: #ffffff;
  color: #666;
  text-align: center;
  line-height: 60px;
  font-size: 14px;
  box-shadow: 0 -1px 4px rgba(0,21,41,.08);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 通知样式 */
.notification-item {
  margin-bottom: 15px;
  padding: 15px;
  border-radius: 4px;
  background-color: #f8f8f8;
  border-left: 4px solid #409EFF;
}

.notification-item.read {
  border-left-color: #C0C4CC;
  opacity: 0.8;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.notification-header h3 {
  margin: 0;
  font-size: 16px;
}

.notification-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  font-size: 12px;
}

.notification-time {
  color: #909399;
}
</style> 