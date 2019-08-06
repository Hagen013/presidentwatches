import request from '@/utils/request'
import { login } from '@/api/login'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { getRefreshToken, setRefreshToken, removeRefreshToken } from '@/utils/auth'


const state = {
  token: getToken,
  refreshToken: getRefreshToken,
  name: ''
}

const mutations = {

  SET_ACCESS_TOKEN(state, token) {
    state.token = token;
  },
  SET_REFRESH_TOKEN(state, token) {
    state.refreshToken = token;
  },
  SET_NAME(state, name) {
    state.name = name;
  }

}

const actions = {

  login({commit}, payload) {
    const { username, password } = payload
    return new Promise((resolve, reject) => {
      login({username: username.trim(), password: password}).then(response => {
        const { data } = response
        commit('SET_ACCESS_TOKEN', data.access)
        commit('SET_REFRESH_TOKEN', data.refresh)
        setToken(data.access);
        setRefreshToken(data.refresh);
        resolve()
      }).catch(error => {
        reject(error);
      })
    })
  },

  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      commit('SET_ACCESS_TOKEN', '')
      commit('SET_REFRESH_TOKEN', '')
      removeToken()
      removeRefreshToken()
      resolve()
    })
  }

}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}