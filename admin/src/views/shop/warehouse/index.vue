<template>
    <div class="form-container">
        <el-tabs v-model="activeName">
            <el-tab-pane label="Выгрузка" name="download">
                <download>
                </download>
            </el-tab-pane>
            <el-tab-pane label="Загрузка (старая)" name="upload">
                <upload>
                </upload>
            </el-tab-pane>
            <el-tab-pane label="Загрузка (новая)" name="upload-new">
                <upload-new>
                </upload-new>
            </el-tab-pane>
            <el-tab-pane label="+ Новые товары" name="create-list">
                <create-list>
                </create-list>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import baseUrl from '@/utils/baseUrl'
import api from '@/utils/request'
import NProgress from 'nprogress'

import Upload from './components/Upload.vue'
import Upload2 from './components/Upload2.vue'
import Download from './components/Download.vue'
import CreateList from './components/CreateList.vue'

export default {
    name: 'Warehouse',
    data: () => ({
        activeName: 'download'
    }),
    components: {
        'upload': Upload,
        'download': Download,
        'upload-new': Upload2,
        'create-list': CreateList
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
