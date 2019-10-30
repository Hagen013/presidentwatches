<template>
    <div class="form-container" v-loading="loading">
        <div class="list-view" v-if="responseReceived">
            <div class="list-view-filters">
                <el-row :gutter="20">
                    <el-col :span="8">
                        <el-input placeholder="Email"
                            v-model="filters.email"
                        >
                        </el-input>
                    </el-col>
                    <el-col :span="8">
                        <el-input placeholder="Номер телефона"
                            v-model="filters.phone"
                        >
                        </el-input>
                    </el-col>
                    <el-col :span="8">
                        <el-input placeholder="Имя"
                            v-model="filters.name"
                        >
                        </el-input>
                    </el-col> 
                </el-row>
            </div>
            <table class="table">
                <tr class="table-heading">

                    <th class="table-head">
                        <div class="table-label">
                        ID
                        </div>
                    </th>

                    <th class="table-head">
                        <div class="table-label">
                        Имя
                        </div>
                    </th>

                    <th class="table-head">
                        <div class="table-label">
                        Email
                        </div>
                    </th>

                </tr>
                <tr class="table-row" v-for="item in items"
                    :key="item.id"
                >

                    <td class="table-cell table-cell--colored">
                        <div class="table-container">
                            <div class="public_id">
                            {{item.id}}
                            </div>
                        </div>
                    </td>

                    <td class="table-cell table-cell--colored">
                        <div class="table-container">
                            <div class="public_id">
                            {{item.first_name}}
                            </div>
                        </div>
                    </td>

                    <td class="table-cell table-cell--colored">
                        <div class="table-container">
                            <div class="public_id">
                            {{item.email}}
                            </div>
                        </div>
                    </td>

                </tr>
            </table>
        </div>
    </div>
</template>
<script>
import request from '@/utils/request'

export default {
    name: 'Users',
    data: () => ({
        apiUrl: '/users/',
        items: [],
        loading: false,
        responseReceived: false,
        offset: 0,
        limit: 100,
        totalCount: 0,
        pageSizeOptions: [
            {label: '50', value: 50},
            {label: '100', value: 100},
            {label: '200', value: 200}
        ],
        filters: {
            email: '',
            phone: '',
            name: ''
        }
    }),
    computed: {
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            this.getList();
        },
        getList() {
            this.loading = true;
            this.responseReceived = false;
            request.get(this.apiUrl).then(
                response => {
                    this.handleSuccessfulGetResponse(response);
                },
                response => {
                    this.handleFailedGetResponse(response);
                } 
            )
        },
        handleSuccessfulGetResponse(response) {
            console.log(response);
            this.items = response.data.results;
            this.totalCount = response.data.count;
            this.loading = false;
            this.responseReceived = true;
        },
        handleFailedGetResponse(response) {
            this.loading = false;
            this.responseReceived = true;
        }
    },
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
</style>
