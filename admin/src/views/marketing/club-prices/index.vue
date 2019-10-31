<template>
    <div class="app-container" v-loading="ready">
        <div class="club-prices">
            <div class="table-controls">
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
                        {{brand.value}}
                        </div>
                    </td>
                    <td class="table-cell" v-for="key in brand.sales" :key="key">
                        <div class="table-container">
                            <el-input v-model="brand.sales[key]"
                                controls-position="right"
                                @change="tsoy"
                            >
                            </el-input>
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
    name: 'ClubPrices',
    data: () => ({
        brands: [],
        groups: [],
        groupsReceived: false,
        brandsReceived: false,
        ready: false
    }),
    computed: {
        loading() {
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
            for (let i=0; i<this.brands.length; i++) {
                this.brands[i].sales = {};
                for (let y=0; y<this.groups.length; y++) {
                    let sale = this.groups[y].sales[this.brands[i].value];
                    if (sale === undefined) {
                        sale = 0;
                    }
                    this.brands[i].sales[this.groups[y].id] = sale;
                }
            }
        },
        tsoy() {
            console.log('change')
        }
    },
    watch: {
        loading() {
            if (this.loading) {
                this.processData();
            }
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
</style>
