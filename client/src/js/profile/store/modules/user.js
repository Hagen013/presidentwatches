import api from '@/api'

const user = {
  state: {
    id: null,
    username: "",
    first_name: "",
    last_name: "",
    patronymic: "",
    email: "",
    phone_number: "",
    sex: 1,
    birth_date: null
  },
  mutations: {
    SET_USER(state, payload) {
      for (let key in payload) {
        state[key] = payload[key];
      }
    },
    SET_USER_ID(state, payload) {
      state.id = payload;
    },
    set_first_name(state, payload) {
      state.first_name = payload;
    },
    set_last_name(state, payload) {
      state.last_name = payload;
    },
    set_patronymic(state, payload) {
      state.patronymic = payload;
    },
    set_email(state, payload) {
      state.email = payload;
    },
    set_phone_number(state, payload) {
      state.phone_number = payload;
    },
    set_sex(state, payload) {
      state.sex = payload
    },
    set_birth_date(state, payload) {
      state.birth_date = payload
    }
  },
  actions: {
    updateProfile({ commit, state, dispatch, }, payload) {
      api.put(`/users/${state.id}/`).then(
        response => {
          commit('SET_USER', response.data)
        },
        resonse => {

        }
      )
    }
  }
}

export default user
