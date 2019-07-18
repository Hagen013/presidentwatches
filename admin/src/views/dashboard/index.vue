<template>
    <div class="dashboard-container">
        <div class="view-placeholder">
            <div class="view-placeholder-container">
                Главная
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Dashboard',
    computed: {
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .view-placeholder {
        width: 100%;
        height: 90vh;
        padding: 20px;
    }
    .view-placeholder-container {
        height: 100%;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 32px;
        font-weight: 600;
        letter-spacing: 2px;
        border: 2px dotted grey;
        background: linear-gradient(45deg, rgba(0, 0, 0, 0) 49.9%, grey 49.9%, grey 60%, rgba(0, 0, 0, 0) 60% ), linear-gradient(45deg, green 10%, rgba(0, 0, 0, 0) 10% );
        background-size: 0.5em 0.5em;
        opacity: 0.3;
    }
</style>
