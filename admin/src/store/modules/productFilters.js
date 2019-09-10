const state = {
  initialized: false,
  offset: null,
  limit: null,
  pageSize: null,
  facetes: null,
  modelSearch: null,
  booleanFilters: null,
  total_count: null
}

const mutations = {
  set(state, payload) {
    state.offset = payload.offset;
    state.limit = payload.limit;
    state.pageSize = payload.pageSize;
    state.facetes = payload.facetes;
    state.modelSearch = payload.modelSearch;
    state.booleanFilters = payload.booleanFilters;
    state.total_count = payload.total_count;
    state.initialized = true;
  }
}

const actions = {

}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}