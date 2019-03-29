<template>
    <div class="app-container">
        <h1>{{title}}</h1>
        <el-tabs>
            <el-tab-pane label="Основное">
                <el-input placeholder="Название" v-model="instance.name">
                </el-input>
                <el-input placeholder="H1 (название на странице)" v-model="instance._title">
                </el-input>
            </el-tab-pane>
            <el-tab-pane label="Мета-теги">
                <el-input placeholder="Meta-title" v-model="instance._meta_title">
                </el-input>
                <el-input placeholder="Meta-keywords" v-model="instance._meta_keywords">
                </el-input>
                <el-input placeholder="Meta-description" v-model="instance._meta_description">
                </el-input>
            </el-tab-pane>
            <el-tab-pane label="Описание">
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import shopApi from '@/api/shop'

export default {
    name: 'Offers',
    data: () => ({
        instanceId: null,
        loading: false,
        instance: null
    }),
    created() {
        this.initialize();
    },
    computed: {
        editing() {
            return this.instanceId !== null
        },
        title() {
            if (this.editing) {
                return 'Редактирование категории'
            } else {
                return 'Создать категорию'
            }
        }
    },
    methods: {
        initialize() {
            let ID = this.$route.params.id;
            if (ID !== undefined) {
                this.instanceId = ID;
                this.loading = true;
                this.getInstance();
            }
        },
        getInstance() {
            shopApi.categories.get(this.instanceId).then(
                response => {
                    this.handleSuccessfulGetRespone(response);
                },
                response => {
                    this.handleFailedUpdateResponse(response);
                }
            )
        },
        updateInstance() {

        },
        deleteInstance() {

        },
        // Response handling start
        handleSuccessfulGetRespone(response) {
            this.loading = false;
            this.instance = response.data;
        },
        handleFailedGetResponse(response) {
            this.loading = false;
        },
        handleSuccessfulUpdateResponse(response) {
            this.loading = false;
        },
        handleFailedUpdateResponse(response) {
            this.loading = false;
        },
        handleSuccessfulDeleteResponse(response) {
             this.loading = false;
        },
        handleFailedDeleteResponse(response) {
            this.loading = false;
        },
        // Response handling end
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
</style>
