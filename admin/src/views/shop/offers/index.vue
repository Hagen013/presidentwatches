<template>
    <div class="app-container" v-loading="loading">

        <div class="pagination">
            <div class="pagination--page-size">
                <div class="field">
                    <div class="field-label">
                        Отображать по
                    </div>
                    <el-select v-model="pageSize"
                    >
                        <el-option
                            v-for="option in pageSizeOptions"
                            :key="option.value"
                            :label="option.label"
                            :value="option.value"
                        >
                        </el-option>
                    </el-select>
                </div>
            </div>
            <div class="pagination--info">
                <div class="pagination--current-count">
                    {{offset}} - {{currentCount}}
                </div>
                <span class="pagination--delimeter">из</span>
                <div class="pagination--total-count">
                    {{totalCount}}
                </div>
            </div>
            <div class="pagination--buttons">
                <el-button circle
                    :disabled="!hasPreviousPage"
                    @click="previousPage"
                >
                    <i class="el-icon-back"></i>
                </el-button>
                <el-button circle
                    :disabled="!hasNextPage"
                    @click="nextPage"
                >
                    <i class="el-icon-right"></i>
                </el-button>
            </div>
        </div>

        <div class="filters">
            <attribute-filter v-for="attribute in filterAttributes"
                :key="attribute.id"
                :attribute="attribute"
                :facetes="facetes"
                v-on:filter="addActiveFacetes"
                v-on:clear="clearActiveFacete"
            >
            </attribute-filter>
        </div>

        <table class="table">

            <tr class="table-heading">

                <th class="table-head">
                    <div class="table-label">
                    Изображение
                    </div>
                </th>

                <th class="table-head">
                    <div class="table-label">
                    Модель
                    </div>
                </th>

                <th class="table-head">
                    <div class="table-label">
                    Бренд
                    </div>
                </th>

                <th class="table-head">
                    <div class="table-label">
                    URL
                    </div>
                </th>

                <th class="table-head">
                    <div class="table-label">
                    Цена
                    </div>
                </th>

                <th class="table-head">
                    <div class="table-label">
                    Теги
                    </div>
                </th>

                <th class="table-head">
                    <div class="table-label">
                    В наличии
                    </div>
                </th>

            </tr>

            <tr class="table-row" v-for="item in items"
                :key="item.id"
            >
                <td class="table-cell">
                    <div class="table-container">
                        <div class="img-wrap">
                            <img :src="item.thumbnail">
                        </div>
                    </div>
                </td>

                <td class="table-cell">
                    <div class="table-container">
                        {{item.model}}
                    </div>
                </td>

                <td class="table-cell">
                    <div class="table-container">
                        {{item.brand}}
                    </div>
                </td>

                <td class="table-cell">
                    <a :href="item.absolute_url"
                        class="table__link"
                        target="_blank"
                    >
                        {{item.absolute_url}}
                    </a>
                </td>

                <td class="table-cell">
                    <div>
                        {{item._price}} ₽
                    </div>
                </td>

            </tr>

        </table>
    </div>
</template>

<script>
import request from '@/utils/request'
import AttributeFilter from './components/Filter'


export default {
    name: 'Offers',
    components: {
        'attribute-filter': AttributeFilter
    },
    data: () => ({
        apiUrl: '/products/',
        items: [],
        totalCount: 0,
        initialized: false,
        loading: false,
        offset: 0,
        limit: 100,
        pageSize: 100,
        pageSizeOptions: [
            {label: '50', value: 50},
            {label: '100', value: 100},
            {label: '200', value: 200}
        ],
        filters: {

        },
        filterAttributes: [],
        ordering: "id",
        activeFacetes: {

        }
    }),
    computed: {
        queryParams() {
            let params = {
                offset: this.offset,
                limit: this.limit,
                ordering: this.ordering
            }
            return params
        },
        currentCount() {
            return (this.offset + this.limit)
        },
        hasPreviousPage() {
            return this.offset > 0
        },
        hasNextPage() {
            return this.currentCount < this.totalCount;
        },
        facetes: {
            get() {
                return this.activeFacetes
            },
            set(value) {
                this.activeFacetes = value;
            } 
        }
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            this.getList();
            this.getFilters();
        },
        getList() {
            this.loading = true;
            let params = this.queryParams;
            for (let key in this.activeFacetes) {
                let values = this.activeFacetes[key];
                if (values.length > 0) {
                    values = values.join(',')
                    params[key] = values;
                }
            }
            request.get(this.apiUrl, {params: params}).then(
                response => {
                    this.handleSuccessfulGetListResponse(response);
                },
                response => {
                    this.handleFailedGetListResponse(response);
                }
            )
        },
        getFilters() {
            request.get('/eav/attributes/', {params: {is_filter: true}}).then(
                response => {
                    this.filterAttributes = response.data.results;
                },
                response => {
                    
                }
            )
        },
        handleSuccessfulGetListResponse(response) {
            this.items = response.data.results;
            this.totalCount = response.data.count;
            this.loading = false;
        },
        handleFailedGetListResponse(response) {
            this.loading = false;
        },
        previousPage() {
            this.offset -= this.pageSize;
        },
        nextPage() {
            this.offset += this.pageSize;
        },
        addActiveFacetes(payload) {
            console.log(payload);
            let key = payload.key;
            let values = payload.values;
            if (values.length > 0) {
                this.$set(this.activeFacetes, key, values);
            } else {
                this.$set(this.activeFacetes, key, []);
            }
            this.getList();
        },
        removeActiveFacetes(payload) {

        },
        clearActiveFacete(payload) {
            this.offset = 0;
            this.limit = this.pageSize;
            this.$set(this.activeFacetes, payload, []);
            this.getList();
        }
    },
    filters: {
    },
    watch: {
        queryParams: {
            handler: function() {
                this.getList();
            },
            deep: true
        },
        pageSize() {
            this.offset = 0;
            this.limit = this.pageSize;
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .img-wrap {
        height: 100px;
        width: 100px;
        text-align: center;
        img {
            height: 100%;
            width: auto;
        }
    }

    .field-label {
        display: inline-block;
        margin-right: 10px;
    }

    .pagination {
        display: flex;
        justify-content: flex-start;
    }

    .pagination--page-size {
        margin-right: 20px;
    }

    .pagination--delimeter {
        margin: 0px 10px;
    }

    .pagination--info {
        display: flex;
    }

    .pagination--info {
        margin-right: 20px;
    }

    .filters {
        margin: 10px 0px;
    }

</style>
