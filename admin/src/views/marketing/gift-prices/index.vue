<template>
    <div class="app-container">
        <div class="loading-screen" v-if="loading" v-loading="loading">
        </div>
        <div v-if="ready" class="gift-prices">
            <div class="table-controls">
                <el-button type="primary" @click="saveChanges" :disabled="!hasChanged">
                    Сохранить
                </el-button>
                <el-button type="danger" @click="rollbackChanges" :disabled="!hasChanged">
                    Отменить
                </el-button>
            </div>
            <table class="table" style="max-width: 800px;">
                <tr class="table-heading">
                    <th class="table-head">
                        <div class="table-label">
                            Бренд
                        </div>
                    </th>
                    <th class="table-head">
                        <div class="table-label" style="padding-left: 40px;">
                            Скидка
                        </div>
                    </th>
                </tr>
                <tr v-for="brand in brands" :key="brand.id">
                    <td class="table-cell">
                        <div class="table-container">
                        {{brand.value}} {{brand.products_count}}
                        </div>
                    </td>
                    <td class="table-cell">
                        <div class="table-container">
                            <div class="input-box">
                                <input v-model="brand.sale" type="number" :min="0" :max="100" class="input"
                                    @input="handleInput($event.target.value, brand)"
                                    @change="handleChange($event.target.value, brand)"
                                >
                                <span class="percentage">
                                    %
                                </span>
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
const equal = require('fast-deep-equal');

export default {
    name: 'GiftPrices',
    data: () => ({
        brands: [],
        brandsProxy: [],
        sales: {},
        ready: false,
        loading: true,
        tableReceived: false,
        brandsReceived: false,
        hasChanged: false
    }),
    computed: {
        responsesReceived() {
            return ( (this.tableReceived) && (this.brandsReceived) )
        },
        sortedBrands() {
            
        }
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            this.getBrands();
            this.getTable();
        },
        getTable() {
            request.get('/cart/gift-prices/').then(
                response => {
                    this.handleSuccessfulGetResponse(response);
                },
                response => {
                    this.handleFailedGetResponse(response);
                }
            )
        },
        handleSuccessfulGetResponse(response) {
            this.sales = response.data.sales;
            this.tableReceived = true;
        },
        handleFailedGetResponse(response) {
        },
        getBrands() {
            request.get('/eav/counts/?attribute__key=vendor').then(
                response => {
                    this.handleSuccessfulBrandsResponse(response);
                },
                response => {
                    this.handleFailedBrandsResponse(response);
                }
            )
        },
        handleSuccessfulBrandsResponse(response) {
            this.brands = response.data.results.sort(function(a,b) {
                if(a.products_count < b.products_count) { return 1; }
                if(a.products_count > b.products_count) { return -1; }
                return 0;  
            })
            this.brandsReceived = true;
        },
        handleFailedBrandsResponse(response) {
        },
        processData() {
            for (let i=0; i<this.brands.length; i++) {
                let sale = this.sales[this.brands[i].value];
                if (sale === undefined) {
                    sale = 0.00;
                }
                this.brands[i].sale = Math.round(sale * 100);;
            }
            this.brandsProxy = JSON.parse(JSON.stringify(this.brands));
            this.ready = true;
            this.loading = false;
        },
        saveChanges() {
            this.loading = true;
            this.ready = false;
            let sales = {};
            
            for (let i=0; i<this.brands.length; i++) {
                let sale = parseFloat(this.brands[i].sale) / 100;
                if ( (sale > 0) && (sale < 1)) {
                    sales[this.brands[i].value] = sale;
                }
            }
            let data = {'sales': sales}
            request.post('/cart/gift-prices/', data).then(
                response => {
                    this.$notify({
                        title: 'Цены обновлены',
                        message: 'Подарочные цены для групп пользователей успешно обновлены',
                        type: 'success'
                    });
                    this.brandsReceived = false;
                    this.tableReceived = false;
                    this.getTable();
                    this.getBrands();
                },
                response => {
                    this.$notify({
                        title: 'Произошла ошибка',
                        message: 'Во время сохранения на стороне сервера произошла ошибка',
                        type: 'error'
                    });
                    this.brandsReceived = false;
                    this.tableReceived = false;
                    this.getTable();
                    this.getBrands();
                }
            )
        },
        rollbackChanges() {
            this.brands = JSON.parse(JSON.stringify(this.brandsProxy));
        },
        checkChanges() {
            this.hasChanged = !equal(this.brands, this.brandsProxy);
        },
        handleInput(val, brand) {
            brand.sale = val;
            this.checkChanges();
        },
        handleChange(val, brand) {
            val = parseInt(val);
            if (isNaN(val)) {
                brand.sale = 0;
                this.$forceUpdate();
            }
        }
    },
    watch: {
        responsesReceived() {
            this.processData();
        },
        brands: {
            handler() {
                if (this.ready) {
                    this.checkChanges();
                }
            },
            deep: true
        }
    },
    filters: {
        brandFilter(val) {
            if (val === 'all') {
                return 'Все бренды'
            } else {
                return val
            }
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .input-box {
        display: flex;
        align-items: center;
        padding: 0px 15px;
    }
    .input {
        width: 100%;
        height: 100%;
        max-height: 46px;
        padding: 7px 10px;
        border-radius: 4px;
        line-height: normal;
        line-height: inherit;
        border: 1px solid grey;
        margin-right: 5px;
    }
    .loading-screen {
        position: fixed;
        top: 0px;
        left: 0px;
        height: 100vh;
        width: 100%;
        z-index: 100;
    }
    .table-controls {
        margin-bottom: 20px;
    }
</style>
