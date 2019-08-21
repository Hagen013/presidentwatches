<template>
    <div class="upload">
        <div class="shop-controls">
            <el-row :gutter="20">
                <el-col :span="12">
                    <el-upload
                    class="upload-demo"
                    ref="upload"
                    :multiple="false"
                    :on-change="clear"
                    action="https://jsonplaceholder.typicode.com/posts/"
                    :auto-upload="false">
                    <el-button slot="trigger" type="primary">
                        Выберите файл
                    </el-button>
                    <el-button style="margin-left: 10px;" type="success" @click="submitUpload">
                        Загрузить на сервер
                    </el-button>
                    </el-upload>
                    <transition name="el-fade-in">
                    <div v-if="!resultsEmpty" class="not-found">
                        Не найдено товаров: {{notFound}}
                    </div>
                    </transition>
                </el-col>
                <el-col :span="12">
                    <transition name="el-fade-in">
                    <div class="results" v-if="showProgress">
                        <el-card>
                            <div slot="header" class="results-header">
                                <div class="results-title">
                                    {{resultsTitle}}
                                </div>
                                <div class="results-header-container">
                                <el-progress type="dashboard" :percentage="progress" :color="colors"></el-progress>
                                </div>
                            </div>
                            <div v-if="!resultsEmpty">
                                <el-table
                                    :data="results"
                                    style="width: 100%"
                                >
                                    <el-table-column
                                        prop="label"
                                        label="Изменилось"
                                    >
                                    </el-table-column>
                                    <el-table-column
                                        prop="quantity"
                                        label="Количество"
                                    >
                                    </el-table-column>
                                </el-table>
                            </div>
                        </el-card>
                    </div>
                    </transition>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
import baseUrl from '@/utils/baseUrl'
import api from '@/utils/request'
import NProgress from 'nprogress'

export default {
    name: 'Upload',
    data() {
      return {
        apiUploadUrl: '',
        fileList: [],
        taskInProgress: false,
        uploadStatusTimer: null,
        uuid: '',
        results: [],
        progress: 0,
        notFound: 0,
        colors: [
          {color: '#f56c6c', percentage: 20},
          {color: '#e6a23c', percentage: 40},
          {color: '#5cb87a', percentage: 60},
          {color: '#1989fa', percentage: 80},
          {color: '#67C23A', percentage: 100}
        ],
        showProgress: false
      };
    },
    computed: {
        resultsEmpty() {
            return this.results.length == 0
        },
        resultsTitle() {
            if (this.taskInProgress) {
                return 'Обработка...'
            } else if (!this.resultsEmpty) {
                return 'Готово'
            }
            return 'Произошла ошибка'
        }
    },
    created() {
        this.apiUploadUrl = baseUrl + '/tasks/uploads/warehouse2/'
    },
    methods: {
        submitUpload() {
            this.results = [];
            this.showProgress = false;
            this.progress = 0;
    
            let file = this.$refs.upload.uploadFiles[0].raw;
            let formData = new FormData()
            formData.append('file', file)
            NProgress.start()
            this.showProgress = true;

            api.post('/tasks/uploads/warehouse2/', formData).then(
                response => {
                    this.handleSuccessfulResponse(response);
                },
                response => {
                    this.handleFailedResponse(response);
                }
            )
        },
        handleSuccessfulResponse(response) {
            this.uuid = response.data.uuid;
            this.taskInProgress = true;
        },
        handleFailedResponse(response) {
            NProgress.done()
        },
        getUploadStatus() {
            if (this.progress < 90) {
                this.progress += 1
            }
            api.get('/tasks/uploads/warehouse2/', {params: {uuid: this.uuid}}).then(
                response => {
                    if (response.data.is_ready) {
                        this.taskInProgress = false;
                        this.results = response.data.results.results;
                        this.notFound = response.data.results.not_found;
                        NProgress.done()
                        this.progress = 100;
                        this.$refs.upload.uploadFiles.splice(0,1);
                    }
                },
                response => {
                    this.taskInProgress = false;
                    NProgress.done()
                }
            )
        },
        clear() {

        }
    },
    watch: {
        taskInProgress() {
            if (this.taskInProgress) {
                this.uploadStatusTimer = setInterval(this.getUploadStatus, 1000);
            } else {
                clearInterval(this.uploadStatusTimer);
            }
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .upload {
        padding-top: 20px
    }
    .shop-controls {
        padding: 0px;
    }
    .results-header {
        width: 100%;
    }
    .results-title {
        font-size: 24px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 20px;
    }
    .results-header-container {
        display: flex;
        justify-content: center;
        padding: 10px 0px;
    }
    .mini-table {
        width: 100%;
        border-collapse: collapse;
        td {
            color: rgb(96, 98, 102);
            padding: 12px;
            border-top: 1px solid rgb(128, 128, 128);
        }
    }
    .not-found {
        display: flex;
        justify-content: center;
        padding: 20px 0px;
        font-size: 24px;
        font-weight: 600;
        color: rgb(96, 98, 102);
    }
</style>
