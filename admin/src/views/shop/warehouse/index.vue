<template>
    <div class="form-container">
        <el-tabs v-model="activeName">
            <el-tab-pane label="Выгрузка" name="download">
                <download>
                </download>
            </el-tab-pane>
            <el-tab-pane label="Загрузка" name="upload">
                <upload>
                </upload>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import baseUrl from '@/utils/baseUrl'
import api from '@/utils/request'
import NProgress from 'nprogress'

import Upload from './components/Upload.vue'
import Download from './components/Download.vue'

export default {
    name: 'Warehouse',
    data: () => ({
        activeName: 'download'
    }),
    components: {
        'upload': Upload,
        'download': Download
    },
    computed: {
    },
    created() {
    },
    methods: {
    },
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .form-container {
        padding: 10px 20px;
    }
</style>
