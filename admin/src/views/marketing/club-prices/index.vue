<template>
    <div class="app-container" v-loading="loading">
        <div class="club-prices">
            <div class="table-controls">
            </div>
            <table class="table">
            </table>
        </div>
    </div>
</template>
<script>
export default {
    name: 'ClubPrices',
    data: () => ({
        loading: false,
    }),
    computed: {
    },
    methods: {
        getList() {
            
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
</style>
