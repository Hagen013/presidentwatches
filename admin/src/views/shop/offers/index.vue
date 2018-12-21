<template>
    <div class="app-container">
        <div v-for="item in items"
            :key="item.id"
        >
            {{item['name']}}
        </div>
    </div>
</template>

<script>
import axios from 'axios'

const service = axios.create({
  baseURL: "http://localhost:8000/api/v0",
  timeout: 5000,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  }
})

export default {
    name: 'Offers',
    data: () => ({
        items: []
    }),
    computed: {
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            service.get('/products/').then(
                response => {
                    console.log(response);
                    this.items = response.data['results'];
                },
                response => {
                    console.log(response);
                }
            )
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
</style>
