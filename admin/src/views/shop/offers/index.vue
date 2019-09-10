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

        <el-row class="search-inputs"
            :gutter="20"
        >
            <el-col
                :span="8"
            >
                <el-input
                    placeholder="Поиск по модели"
                    prefix-icon="el-icon-search"
                    v-model="modelSearchProxy"
                >
                </el-input>
            </el-col>
            <el-col :span="16">
                <div class="select-box">
                    <div class="select-box-label">
                        Наличие:
                    </div>
                    <div class="select-box-value">
                        <el-select
                            v-model="booleanFilters.is_in_stock"
                        >
                            <el-option v-for="option in availabilityOptions"
                                :key="option.label"
                                :label="option.label"
                                :value="option.value"
                            >
                            </el-option>
                        </el-select>
                    </div>
                </div>
                <div class="select-box">
                    <div class="select-box-label">
                        Есть на Тульской:
                    </div>
                    <div class="select-box-value">
                        <el-select
                            v-model="booleanFilters.is_in_store"
                        >
                            <el-option v-for="option in availabilityOptions"
                                :key="option.label"
                                :label="option.label"
                                :value="option.value"
                            >
                            </el-option>
                        </el-select>
                    </div>
                </div>
            </el-col>
        </el-row>

        <el-row>
            <div class="select-box">
                <div class="select-box-label">
                    Новинка:
                </div>
                <div class="select-box-value">
                    <el-select
                        v-model="booleanFilters.is_new"
                    >
                        <el-option v-for="option in availabilityOptions"
                            :key="option.label"
                            :label="option.label"
                            :value="option.value"
                        >
                        </el-option>
                    </el-select>
                </div>
            </div>
            <div class="select-box">
                <div class="select-box-label">
                    Фото:
                </div>
                <div class="select-box-value">
                    <el-select
                        v-model="booleanFilters.has_image"
                    >
                        <el-option v-for="option in imagesOptions"
                            :key="option.label"
                            :label="option.label"
                            :value="option.value"
                        >
                        </el-option>
                    </el-select>
                </div>
            </div>
        </el-row>



        <div class="filters">
            <attribute-filter v-for="attribute in filterAttributes"
                :key="attribute.id"
                :attribute="attribute"
                :facetes="facetes"
                v-on:filter="setActiveFacetes"
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

                <th class="table-head text-left">
                    <div class="table-label text-left">
                    Теги
                    </div>
                </th>

                <th class="table-head text-left">
                    <div class="table-label text-left">
                    В наличии
                    </div>
                </th>

            </tr>

            <tr class="table-row" v-for="item in items"
                :key="item.id"
                @click="select(item.id)"
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

                <td class="table-cell text-left">
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

                <td class="table-cell">
                    <div>
                    </div>
                </td>

                <td class="table-cell">
                    <div>
                        <div>
                            Онлайн: <span class="availability" :class="{ green : item.is_in_stock }">{{item.is_in_stock|boolean}}</span>
                        </div>
                        <div>
                            Оффлайн: <span class="availability" :class="{ green : item.is_in_store }">{{item.is_in_store|boolean}}</span>
                        </div>
                    </div>
                </td>

            </tr>

        </table>
    </div>
</template>

<script>
import request from '@/utils/request'
import AttributeFilter from './components/Filter'
import debounce from 'debounce'

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
        facetes: {
        },
        modelSearch: "",
        modelSearchProxy: "",
        availabilityOptions: [
            {label: '---', value: ''},
            {label: 'Да', value: 'true'},
            {label: 'Нет', value: 'false'}
        ],
        imagesOptions: [
            {label: '---', value: ''},
            {label: 'Есть', value: 'true'},
            {label: 'Без', value: 'false'}
        ],
        booleanFilters: {
            is_in_store: '',
            is_in_stock: '',
            is_new: '',
            has_image: '',
        }
    }),
    computed: {
        queryParams() {
            let params = {
                offset: this.offset,
                limit: this.limit,
                ordering: this.ordering
            }
            for (let key in this.facetes) {
                if ( (this.facetes[key] !== undefined) && (this.facetes[key].length > 0) ) {
                    params[key] = this.facetes[key].join(',');
                }
            }
            if (this.modelSearch.length > 0) {
                params['search'] = this.modelSearch;
            }
            if (this.booleanFilters.is_in_store !== '') {
                params['is_in_store'] = this.booleanFilters.is_in_store;
            }
            if (this.booleanFilters.is_in_stock !== '') {
                params['is_in_stock'] = this.booleanFilters.is_in_stock;
            }
            if (this.booleanFilters.is_new !== '') {
                params['is_new'] = this.booleanFilters.is_new;
            }
            if (this.booleanFilters.has_image !== '') {
                params['has_image'] = this.booleanFilters.has_image;
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
    },
    created() {
        this.initialize();
        let self = this;
    },
    methods: {
        initialize() {
            if (this.$store.state.productFilters.initialized) {
                let data = this.$store.state.productFilters;
                this.offset = data.offset;
                this.limit = data.limit;
                this.pageSize = data.pageSize;
                this.facetes = data.facetes;
                this.modelSearch = data.modelSearch;
                this.booleanFilters = data.booleanFilters;
                this.totalCount = data.total_count;
                this.initialized = true;
            }
            this.getList();
            this.getFilters();
        },
        getList() {
            this.loading = true;
            let params = this.queryParams;
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
        setActiveFacetes(payload) {
            let key = payload.key;
            let values = payload.values;
            this.$set(this.facetes, key, values);
            this.offset = 0;
        },
        clearActiveFacete(key) {
            this.$set(this.facetes, key, []);
            this.offset = 0;
        },
        select(pk) {
            this.$store.commit('productFilters/set', {
                offset: this.offset,
                limit: this.limit,
                pageSize: this.pageSize,
                facetes: this.facetes,
                modelSearch: this.modelSearch,
                booleanFilters: this.booleanFilters,
                total_count: this.totalCount
            });
            this.$router.push({path: `/shop/offers/${pk}/`})
        }
    },
    filters: {
        boolean(value) {
            if (value) {
                return 'да'
            } else {
                return 'нет'
            }
        }
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
        },
        modelSearchProxy: {
            handler: debounce(function(value) {
                this.modelSearch = this.modelSearchProxy;
            }, 500)
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

    .search-inputs {
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .table__link {
        padding: 20px 0px;
        color: blue;
    }

    .availability {
        color: red;
    }

    .availability.green {
        color:  #67C23A;
    }
    
    .table-label {
        padding: 0px;
    }

    .text-left {
        text-align: left !important;
    }

    .table-container {
        padding: 5px 0px;
    }

    .select-box {
        display: inline-block;
        margin-right: 20px;
    }

    .select-box-label {
        display: inline-block;
        margin-right: 10px;
    }

    .select-box-value {
        display: inline-block;
    }

</style>
