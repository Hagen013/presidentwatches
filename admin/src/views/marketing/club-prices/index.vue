<template>
    <div class="app-container">
        <div class="loading-screen" v-if="loading" v-loading="loading">
        </div>
        <div v-if="ready">
            <div class="club-prices">
                <div class="table-controls">
                    <el-button type="primary" @click="saveChanges" :disabled="!hasChanged">
                        Сохранить
                    </el-button>
                    <el-button type="danger" @click="rollbackChanges" :disabled="!hasChanged">
                        Отменить
                    </el-button>
                </div>
                <table class="table">
                    <tr class="table-heading">
                        <th class="table-head">
                            <div class="table-label">
                                Бренд
                            </div>
                        </th>
                        <th class="table-head" v-for="group in groups" :key="group.id">
                            <div class="table-label">
                                {{group.name}}
                            </div>
                        </th>
                    </tr>
                    <tr class="table-row" v-for="brand in brands" :key="brand.id">
                        <td class="table-cell">
                            <div class="table-container">
                            {{brand.value|brandFilter}}
                            </div>
                        </td>
                        <td class="table-cell" v-for="group in groups" :key="group.id">
                            <div class="input-box">
                                <input v-model="brand.sales[group.id]" type="number" :min="0" :max="100" class="input"
                                    @input="handleInput($event.target.value, brand, group)"
                                    @change="handleChange($event.target.value, brand, group)"
                                >
                                <span class="percentage">
                                    %
                                </span>
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</template>
<script>
import request from '@/utils/request'
const equal = require('fast-deep-equal');

export default {
    name: 'ClubPrices',
    data: () => ({
        brands: [],
        brandsProxy: [],
        groups: [],
        groupsReceived: false,
        brandsReceived: false,
        ready: false,
        hasChanged: false,
        loading: true
    }),
    computed: {
        responsesReceived() {
            return ((this.groupsReceived) && (this.brandsReceived))
        }
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            this.getList();
            this.getBrands();
        },
        getList() {
            request.get('/users/club-prices/').then(
                response => {
                    this.handleSuccessfulGetResponse(response);
                },
                response => {
                    this.handleFailedGetResponse(response);
                }
            )
        },
        handleSuccessfulGetResponse(response) {
            this.groups = response.data.results;
            this.groupsReceived = true;
        },
        handleFailedGetResponse(response) {
            
        },
        getBrands() {
            request.get('/eav/attributes/?key=vendor').then(
                response => {
                    this.handleSuccessfulBrandsResponse(response);
                },
                response => {
                    this.handleFailedBrandsResponse(response);
                }
            )
        },
        handleSuccessfulBrandsResponse(response) {
            this.brands = response.data.results[0].value_set.sort(function(a,b) {
                if(a.value < b.value) { return -1; }
                if(a.value > b.value) { return 1; }
                return 0;
            });
            this.brandsReceived = true;
        },
        handleFailedBrandsResponse(response) {
            
        },
        processData() {
            this.brands.unshift({
                'value': 'all',
            })
            for (let i=0; i<this.brands.length; i++) {
                this.brands[i].sales = {};
                for (let y=0; y<this.groups.length; y++) {
                    let sales = this.groups[y].sales;
                    let groupSale = sales[this.brands[i].value];
                    if (groupSale === undefined) {
                        groupSale = 0.00;
                    }
                    this.brands[i].sales[this.groups[y].id] = groupSale * 100;
                }
            }
            this.ready = true;
            this.brandsProxy = JSON.parse(JSON.stringify(this.brands));
            this.loading = false;
        },
        saveChanges() {
            this.loading = true;
            for (let i=0; i<this.groups.length; i++) {
                for (let y=0; y<this.brands.length; y++) {
                    let sale = this.brands[y].sales[this.groups[i].id];
                    sale = parseFloat(sale);
                    this.groups[i].sales[this.brands[y].value] = sale / 100;
                }
            }
            request.put('/users/club-prices/', this.groups).then(
                response => {
                    this.$notify({
                        title: 'Группы обновлены',
                        message: 'Клубные цены для групп пользователей успешно обновлены',
                        type: 'success'
                    });
                    this.brandsReceived = false;
                    this.groupsReceived = false;
                    this.getList();
                    this.getBrands();
                },
                response => {
                    this.$notify({
                        title: 'Произошла ошибка',
                        message: 'Во время сохранения на стороне сервера произошла ошибка',
                        type: 'error'
                    });
                    this.brandsReceived = false;
                    this.groupsReceived = false;
                    this.getList();
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
        handleInput(val, brand, group) {
            brand.sales[group.id] = val;
            this.checkChanges();
        },
        handleChange(val, brand, group) {
            val = parseInt(val);
            if (isNaN(val)) {
                brand.sales[group.id] = 0;
                this.$forceUpdate();
            }
        }
    },
    watch: {
        responsesReceived() {
            if (this.responsesReceived) {
                this.processData();
            }
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
</style>
