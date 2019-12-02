<template>
    <div class="app-container">
        <div class="loading-screen" v-if="loading" v-loading="loading">
        </div>
        <div v-if="ready">
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
        sales: {},
        ready: false,
        loading: true,
        tableReceived: false,
        brandsReceived: false,
    }),
    computed: {
        responsesReceived() {
            return ( (this.tableReceived) && (this.brandsReceived) )
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
            this.sales = response.data;
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
        },
        saveChanges() {
        },
        rollbackChanges() {
        },
        checkChanges() {
        },
        handleInput(val, brand, group) {
        },
        handleChange(val, brand, group) {
        }
    },
    watch: {
        responsesReceived() {
            this.processData();
        },
        brands: {
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
</style>
