import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    // 用户相关
    user: {
      name: '',
      email: '',
      settings: {
        emailNotifications: true,
        pushNotifications: true,
        colorTheme: 'light'
      }
    },
    
    // 数据相关
    schools: [],
    professors: [],
    applications: [],
    emails: [],
    documents: [],
    notifications: [],
    
    // UI相关
    loading: false,
    currentSchool: null,
    currentProfessor: null,
    currentApplication: null,
    searchResults: {}
  },
  
  mutations: {
    // 用户相关
    SET_USER(state, user) {
      state.user = user
    },
    UPDATE_USER_SETTINGS(state, settings) {
      state.user.settings = { ...state.user.settings, ...settings }
    },
    
    // 数据相关
    SET_SCHOOLS(state, schools) {
      state.schools = schools
    },
    SET_PROFESSORS(state, professors) {
      state.professors = professors
    },
    SET_APPLICATIONS(state, applications) {
      state.applications = applications
    },
    SET_EMAILS(state, emails) {
      state.emails = emails
    },
    SET_DOCUMENTS(state, documents) {
      state.documents = documents
    },
    SET_NOTIFICATIONS(state, notifications) {
      state.notifications = notifications
    },
    
    // 单项数据
    SET_CURRENT_SCHOOL(state, school) {
      state.currentSchool = school
    },
    SET_CURRENT_PROFESSOR(state, professor) {
      state.currentProfessor = professor
    },
    SET_CURRENT_APPLICATION(state, application) {
      state.currentApplication = application
    },
    
    // 搜索相关
    SET_SEARCH_RESULTS(state, results) {
      state.searchResults = results
    },
    
    // UI相关
    SET_LOADING(state, loading) {
      state.loading = loading
    }
  },
  
  actions: {
    // 学校相关
    async fetchSchools({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get('/schools')
        commit('SET_SCHOOLS', response.data)
      } catch (error) {
        console.error('获取学校列表失败', error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchSchoolById({ commit }, schoolId) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get(`/schools/${schoolId}`)
        commit('SET_CURRENT_SCHOOL', response.data)
        return response.data
      } catch (error) {
        console.error(`获取学校ID ${schoolId} 失败`, error)
        return null
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 导师相关
    async fetchProfessors({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get('/professors')
        commit('SET_PROFESSORS', response.data)
      } catch (error) {
        console.error('获取导师列表失败', error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchProfessorById({ commit }, professorId) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get(`/professors/${professorId}`)
        commit('SET_CURRENT_PROFESSOR', response.data)
        return response.data
      } catch (error) {
        console.error(`获取导师ID ${professorId} 失败`, error)
        return null
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 申请相关
    async fetchApplications({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get('/applications')
        commit('SET_APPLICATIONS', response.data)
      } catch (error) {
        console.error('获取申请列表失败', error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchApplicationById({ commit }, applicationId) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get(`/applications/${applicationId}`)
        commit('SET_CURRENT_APPLICATION', response.data)
        return response.data
      } catch (error) {
        console.error(`获取申请ID ${applicationId} 失败`, error)
        return null
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 邮件相关
    async fetchEmails({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get('/emails')
        commit('SET_EMAILS', response.data)
      } catch (error) {
        console.error('获取邮件列表失败', error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 文档相关
    async fetchDocuments({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get('/documents')
        commit('SET_DOCUMENTS', response.data)
      } catch (error) {
        console.error('获取文档列表失败', error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 通知相关
    async fetchNotifications({ commit }) {
      try {
        const response = await axios.get('/notifications')
        commit('SET_NOTIFICATIONS', response.data)
      } catch (error) {
        console.error('获取通知列表失败', error)
      }
    },
    
    // 搜索相关
    async searchSchools({ commit }, query) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get(`/search/school?school_name=${query}`)
        return response.data
      } catch (error) {
        console.error('搜索学校失败', error)
        return null
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async searchProfessors({ commit }, { name, school }) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get(`/search/professor?name=${name}${school ? `&school=${school}` : ''}`)
        return response.data
      } catch (error) {
        console.error('搜索导师失败', error)
        return null
      } finally {
        commit('SET_LOADING', false)
      }
    }
  },
  
  getters: {
    isLoading: state => state.loading,
    allSchools: state => state.schools,
    allProfessors: state => state.professors,
    allApplications: state => state.applications,
    allEmails: state => state.emails,
    allDocuments: state => state.documents,
    allNotifications: state => state.notifications,
    unreadNotifications: state => state.notifications.filter(n => !n.is_read),
    currentSchool: state => state.currentSchool,
    currentProfessor: state => state.currentProfessor,
    currentApplication: state => state.currentApplication
  },
  
  modules: {
    // 可以添加模块化的状态
  }
}) 