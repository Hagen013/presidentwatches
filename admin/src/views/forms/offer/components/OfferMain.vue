<template>
    <div class="tab-content offer-main">
        <el-row :gutter="32">
            <el-col :span="12">
                <div class="sub-block">
                    <div class="subtitle">
                        Бренд и коллекция
                    </div>
                    <div class="field-block">
                        <div class="field">
                            <div class="field-label">
                                Бренд:
                            </div>
                            <div class="field-input-box"
                            >
                                <el-select
                                    v-model="instance.brand"
                                    filterable
                                    remote
                                    :remote-method="remoteBrands"
                                    :loading="!brandReceived"
                                    loading-text="Секунду..."
                                    @focus="getBrands"
                                >
                                    <el-option
                                        v-for="item in filteredBrands"
                                        :key="item.value"
                                        :label="item.value"
                                        :value="item.value"
                                    >
                                    </el-option>
                                </el-select>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Коллекция:
                            </div>
                            <div class="field-input-box">
                                <el-select
                                    v-model="instance.series"
                                    filterable
                                    remote
                                    :remote-method="remoteSeries"
                                    :loading="!seriesReceived"
                                    loading-text="Секунду..."
                                    @focus="getSeries"
                                >
                                    <el-option
                                        v-for="item in filteredSeries"
                                        :key="item.value"
                                        :label="item.value"
                                        :value="item.value"
                                    >
                                    </el-option>
                                </el-select>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="sub-block">
                    <div class="subtitle">
                        Цены:
                    </div>
                    <div class="field-block">
                        <div class="field">
                            <div class="field-label">
                                Цена:
                            </div>
                            <div class="field-input-box">
                                <el-input-number
                                    v-model="instance._price"
                                    controls-position="right"
                                    size="small"
                                    :min="0"
                                >
                                </el-input-number>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Цена до скидки:
                            </div>
                            <div class="field-input-box">
                                <el-input-number
                                    v-model="instance.old_price"
                                    controls-position="right"
                                    size="small"
                                    :min="0"
                                >
                                </el-input-number>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="sub-block">
                    <div class="subtitle">
                        Габариты:
                    </div>
                    <div class="field-block">
                        <div class="field">
                            <div class="field-label">
                                Длина:
                            </div>
                            <div class="field-input-box">
                                <el-input-number
                                    v-model="instance.height"
                                    controls-position="right"
                                    size="small"
                                    :min="0"
                                >
                                </el-input-number>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Ширина
                            </div>
                            <div class="field-input-box">
                                <el-input-number
                                    v-model="instance.width"
                                    controls-position="right"
                                    size="small"
                                    :min="0"
                                >
                                </el-input-number>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Толщина
                            </div>
                            <div class="field-input-box">
                                <el-input-number
                                    v-model="instance.thickness"
                                    controls-position="right"
                                    size="small"
                                    :min="0"
                                >
                                </el-input-number>
                            </div>
                        </div>
                    </div>
                    <div class="field-block">
                        <div class="field">
                            <div class="field-label">
                                Вес (гр):
                            </div>
                            <div class="field-input-box">
                                <el-input-number
                                    v-model="instance._weight"
                                    controls-position="right"
                                    size="small"
                                    :min="0"
                                >
                                </el-input-number>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="sub-block">
                    <div class="subtitle">
                        Метки:
                    </div>
                    <div class="tags">
                        <el-checkbox v-model="instance.is_in_stock">
                            В наличии
                        </el-checkbox>
                        <el-checkbox v-model="instance.is_bestseller">
                            Хит продаж
                        </el-checkbox>
                        <el-checkbox v-model="instance.is_new">
                            Новинка
                        </el-checkbox>
                        <el-checkbox v-model="instance.is_in_showcase">
                            Отображать в подборках
                        </el-checkbox>
                        <el-checkbox v-model="instance.is_published">
                            Опубликовано
                        </el-checkbox>
                        <el-checkbox v-model="instance.is_yml_offer">
                            Яндекс.Маркет
                        </el-checkbox>
                    </div>
                </div>
            </el-col>
            <el-col :span="12">
                <div class="img-wrap">
                    <img :src="instance.image">
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import request from '@/utils/request'
import fuzzy from 'fuzzysearch'

export default {
    name: 'OfferMain',
    data: () => ({
        // бренд
        availableBrands: [],
        filteredBrands: [],
        brandReceived: false,
        // серия
        availableSeries: [],
        filteredSeries: [],
        seriesReceived: false

    }),
    props: [
        'instance'
    ],
    computed: {
    },
    created() {

    },
    methods: {
        remoteBrands(query) {
            if (!this.brandReceived) {
                request.get('/eav/attributes/?search=Бренд').then(
                    response => {
                        this.availableBrands = response.data.results[0].value_set;
                        this.brandReceived = true;
                        if (query !== '') {
                            this.filteredBrands =  this.availableBrands.filter((value) => {
                                return value.value.toLowerCase().indexOf(query.toLowerCase()) > -1
                            })
                        } else {
                            this.filteredBrands =  this.availableBrands
                        }
                    },
                    response => {

                    }
                )
            } else {
                if (query !== '') {
                    this.filteredBrands = this.availableBrands.filter((value) => {
                        return value.value.toLowerCase().indexOf(query.toLowerCase()) > -1
                    })
                } else {
                    this.filteredBrands = this.availableBrands;
                }
            }
        },
        getBrands() {
            request.get('/eav/attributes/?search=Бренд').then(
                response => {
                    this.availableBrands = response.data.results[0].value_set;
                    this.filteredBrands = this.availableBrands;
                    this.brandReceived = true;
                },
                response => {

                }
            )
        },
        remoteSeries(query) {
            if (!this.brandReceived) {
                request.get('/eav/attributes/?search=Коллекция').then(
                    response => {
                        this.availableSeries = response.data.results[0].value_set;
                        this.seriesReceived = true;
                        if (query !== '') {
                            this.filteredSeries =  this.availableSeries.filter((value) => {
                                return value.value.toLowerCase().indexOf(query.toLowerCase()) > -1
                            })
                        } else {
                            this.filteredSeries =  this.availableSeries
                        }
                    },
                    response => {

                    }
                )
            } else {
                if (query !== '') {
                    this.filteredSeries = this.availableSeries.filter((value) => {
                        return value.value.toLowerCase().indexOf(query.toLowerCase()) > -1
                    })
                } else {
                    this.filteredSeries = this.availableSeries;
                }
            }
        },
        getSeries() {
            request.get('/eav/attributes/?search=Коллекция').then(
                response => {
                    this.availableSeries = response.data.results[0].value_set;
                    this.filteredSeries = this.availableSeries;
                    this.seriesReceived = true;
                },
                response => {

                }
            )
        },
    },
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .offer-main {
        padding-top: 16px;
    }
    .field {
        margin-right: 15px;
        margin-bottom: 15px;
    }
    .field-label {
        display: inline-block;
        margin-right: 10px;
    }
    .field-input-box {
        display: inline-block;
    }

    .field-block {
        display: flex;
        flex-wrap: wrap;
    }
    .sub-block {
        margin-bottom: 30px;
    }
    .subtitle {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .tags {
        padding-right: 30px;
        .el-checkbox {
            margin-bottom: 10px;
        }
    }
    .img-wrap {
        height: 500px;
        img {
            height: 100%;
            width: auto;
        }
    }
</style>
