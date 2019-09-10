<template>
    <div>
        <el-row>
            <el-col :span="12">
                <el-upload
                    ref="upload"
                    :multiple="false"
                    :on-change="clear"
                    action="https://jsonplaceholder.typicode.com/posts/"
                    :auto-upload="false"
                >
                <el-button slot="trigger" type="primary">
                    Выберите файл
                </el-button>
                <el-button style="margin-left: 10px;" type="success"
                    @click="submitUpload"
                    :disabled="loading"
                >
                    Загрузить на сервер
                </el-button>
                </el-upload>
                <div class="results" v-loading="taskInProgress">
                    <transition name="el-fade-in">
                    <div v-if="dataReceived">
                        <div class="results">
                            <div class="results-icon">
                                <i class="el-icon el-icon-check">
                                </i>
                            </div>
                            <div class="results-text">
                            Добавлено товаров: {{results.count}}
                            </div>
                        </div>
                        <div class="errors">
                            <div v-for="error in results.errors"
                                :key="error"
                            >
                                {{error}}
                            </div>
                        </div>
                    </div>
                    </transition>
                </div>
            </el-col>
            <el-col :span="12">
            </el-col>
        </el-row>
    </div>
</template>

<script>
import request from '@/utils/request'
import NProgress from 'nprogress'

export default {
    name: 'CreateList',
    data: () => ({
        loading: false,
        results: [],
        taskUUID: '',
        taskInProgress: false,
        uploadStatusTimer: null,
        taskUrl: '/tasks/warehouse/create-list/',
        dataReceived: false,
    }),
    computed: {
    },
    created() {
    },
    methods: {
        submitUpload() {
            this.results = [];
            let file = this.$refs.upload.uploadFiles[0].raw;
            let formData = new FormData()
            formData.append('file', file)
            NProgress.start()
            request.post(this.taskUrl, formData).then(
                response => {
                    this.handleSuccessfulResponse(response);
                },
                response => {
                    this.handleFailedResponse(response);
                }
            )
        },
        handleSuccessfulResponse(response) {
            this.taskUUID = response.data.uuid;
            this.taskInProgress = true;
        },
        handleFailedResponse(response) {
            NProgress.done();
        },
        getUploadStatus() {
            request.get(this.taskUrl, {params: {uuid: this.taskUUID}}).then(
                response => {
                    if (response.data.is_ready) {
                        this.taskInProgress = false;
                        this.results = response.data.results.results,
                        this.dataReceived = true;
                        NProgress.done()
                    }
                },
                response => {
                    this.taskInProgress = false;
                    NProgress.done();
                }
            )
        },
    },
    watch: {
        taskInProgress: {
            handler() {
                if (this.taskInProgress) {
                    this.uploadStatusTimer = setInterval(this.getUploadStatus, 2000);
                } else {
                    clearInterval(this.uploadStatusTimer);
                }
            }
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .errors {
        margin-top: 20px;
        max-height: 500px;
        overflow-y: scroll;
        color: red;
        margin-bottom: 50px;
    }
    .results {
        width: 100%;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .results-icon {
        color: #67C23A;
        height: 100px;
        width: 100px;
        border-radius: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 5px solid #67C23A;
        font-size: 30px;
        font-weight: 600;
        border-color: #67C23A;
        margin-bottom: 20px;
    }
</style>
