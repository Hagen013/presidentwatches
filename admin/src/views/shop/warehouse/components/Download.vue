<template>
    <div class="download" v-loading="loading">
        <el-row :gutter="20">
            <el-col :span="8">
                <el-card>
                    <el-button type="primary"
                        @click="submit"
                        :disabled="taskInProgress"
                    >
                        Скачать файл
                        <el-icon class="el-icon-download">
                        </el-icon>
                    </el-button>
                </el-card>
            </el-col>
            <el-col :span="8">
            </el-col>
        </el-row>
    </div>
</template>

<script>
import baseUrl from '@/utils/baseUrl'
import request from '@/utils/request'
import NProgress from 'nprogress'

function downloadURI(uri, name) {
    let link = document.createElement("a");
    link.download = name;
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    link = null
}

export default {
    name: 'Download',
    data: () => ({
        loading: false,
        taskInProgress: false,
        uploadStatusTimer: null,
        uuid: '',
        filename: '',
        progress: 0,
        colors: [
          {color: '#f56c6c', percentage: 20},
          {color: '#e6a23c', percentage: 40},
          {color: '#5cb87a', percentage: 60},
          {color: '#1989fa', percentage: 80},
          {color: '#67C23A', percentage: 100}
        ],
    }),
    computed: {
    },
    created() {
        console.log(baseUrl)
    },
    methods: {
        submit() {
            NProgress.start()
            request.post('/tasks/warehouse/generate/').then(
                response => {
                    this.handleSuccessfulSubmitResponse(response);
                },
                response => {
                    this.handleFailedSubmitResponse(response);
                }
            )
            this.taskInProgress = true;
        },
        handleSuccessfulSubmitResponse(response) {
            this.taskInProgress = true;
            this.uuid = response.data.uuid
            this.filename = response.data.filename;
            console.log(this.filename);
        },
        handleFailedSubmitResponse(response) {
            this.taskInProgress = false;
        },
        getUploadStatus() {
            if (this.progress < 90) {
                this.progress += 10
            }
            request.get('/tasks/warehouse/generate/', {params: {uuid: this.uuid}}).then(
                response => {
                    this.handleSuccessfulGetResultsResponse(response);
                },
                response => {
                    this.hanldeFailedGetResultsResponse(response);
                }
            )
        },
        getResults() {
            document.location.assign(`${baseUrl}/tasks/warehouse/results/?filename=${this.filename}`)
        },
        handleSuccessfulGetResultsResponse(response) {
            if (response.data.is_ready) {
                this.getResults();
                this.taskInProgress = false;
                this.progress = 100;
                NProgress.done()
            }
        },
        hanldeFailedGetResultsResponse(response) {
            this.taskInProgress = false;
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
</style>
