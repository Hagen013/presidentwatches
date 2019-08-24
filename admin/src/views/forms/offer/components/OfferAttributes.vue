<template>
    <div class="tab-content offer-attributes"
        v-loading="!dataProcessed"
    >
        <div v-if="dataProcessed">

            <div class="group" v-for="group in eavGroups" :key="group.id">
                <div class="group-title">
                    {{group.name}}
                </div>
                <div class="group-attributes">
                    <div class="attribute" v-for="attribute in group.attribute_set" :key="attribute.id">
                        <div class="attribute-name">
                            {{attribute.name}}
                        </div>
                        <div class="attribute-field">
                            <el-select
                                v-if="attribute.datatype==6"
                                v-model="attribute.active_values"
                                multiple
                                filterable
                                placeholder="Выбрать"
                            >
                                <el-option
                                    v-for="item in attribute.value_set"
                                    :key="item.id"
                                    :label="item.value"
                                    :value="item.id"
                                >
                                </el-option>
                            </el-select>
                            <el-select v-else-if="attribute.datatype==5"
                                v-model="attribute.active_values"
                                filterable
                                placeholder="Выбрать"
                            >
                                <el-option
                                    v-for="item in attribute.value_set"
                                    :key="item.id"
                                    :label="item.value"
                                    :value="item.id"
                                >
                                </el-option>
                            </el-select>
                            <el-select v-else-if="attribute.datatype==4"
                                v-model="attribute.active_values"
                                filterable
                                placeholder="Выбрать"
                            >
                                <el-option
                                    v-for="item in attribute.value_set"
                                    :key="item.id"
                                    :label="item.value"
                                    :value="item.id"
                                >
                                </el-option>
                            </el-select>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
const equal = require('fast-deep-equal');

import request from '@/utils/request'


export default {
    name: 'OfferAttributes',
    data: () => ({
        //
        eavGroupsResponseReceived: false,
        eavGroups: [],
        //
        eavAttributesResponseReceived: false,
        eavAttributes: [],
        //
        eavValuesResponseReceived: false,
        eavValues: [],
        //
        dataProcessed: false,
        notEditable: {
            'Хит продаж': true,
            'Серия': true,
            'Распродажа': true,
            'Новинка': true,
            'Бренд': true,
            'Коллекция': true,
            'СССР': true,
            'Армейские': true,
            "Gold'n'Black": true
        }
    }),
    props: [
        'instance',
        'activeTab'
    ],
    computed: {
        dataIsReady() {
            return (
                this.eavGroupsResponseReceived === true &&
                this.eavAttributesResponseReceived === true &&
                this.eavValuesResponseReceived === true
            )
        },
        instanceValuesApiUrl() {
            return `/products/${this.instance['id']}/values/`
        }
    },
    created() {
        if (this.activeTab == 'attributes') {
            this.initialize();
        }
    },
    methods: {
        initialize() {
            this.syncData();
        },
        syncData() {
            this.eavGroupsResponseReceived = false;
            this.eavAttributesResponseReceived = false;
            this.eavValuesResponseReceived = false;
            this.dataProcessed = false;
            this.getGroups();
            this.getAttributes();
            this.getInstanceValues();
        },
        //------------------ГРУППЫ--------------------//
        getGroups() {
            request.get('/eav/groups/').then(
                response => {
                    this.handleSuccessfulGetGroupsResponse(response);
                },
                response => {
                    this.handleFailedGetGroupsResponse(response);
                }
            )
        },
        handleSuccessfulGetGroupsResponse(response) {
            this.eavGroups = response.data.results.sort((a,b) => {
                return a.order - b.order
            });
            this.eavGroupsResponseReceived = true;
        },
        handleFailedGetGroupsResponse(response) {
            this.eavGroupsResponseReceived = true;
        },
        //------------------ГРУППЫ КОНЕЦ----------------//

        //------------------АТТРИБУТЫ--------------------//
        getAttributes() {
            request.get('/eav/attributes/').then(
                response => {
                    this.handleSuccessfulGetAttributesResponse(response);
                },
                response => {
                    this.handleFailedGetAttributesResponse(response);
                }
            )
        },
        handleSuccessfulGetAttributesResponse(response) {
            this.eavAttributes = response.data.results;
            this.eavAttributesResponseReceived = true;
        },
        handleFailedGetAttributesResponse(response) {
            this.eavAttributesResponseReceived = true;
        },
        //------------------АТТРИБУТЫ КОНЕЦ----------------//

        //------------------VALUES--------------------//
        getInstanceValues() {
            request.get(this.instanceValuesApiUrl).then(
                response => {
                    this.handleSuccessfulGetValuesResponse(response);
                },
                response => {
                    this.handleFailedGetValuesResponse(response);
                }
            )
        },
        handleSuccessfulGetValuesResponse(response) {
            this.eavValues = response.data.results;
            this.eavValuesResponseReceived = true;
        },
        handleFailedGetValuesResponse(response) {
            this.eavValuesResponseReceived = true;
        },
        //------------------VALUES КОНЕЦ----------------//

        // ОБРАБОТКА
        processData() {
            let attributesMap = {};

            for (let i=0; i<this.eavAttributes.length; i++) {
                attributesMap[this.eavAttributes[i].id] = this.eavAttributes[i].value_set;
            }

            let nonGroupAttributes = this.eavAttributes.filter((attribute) => {
                return ( (attribute.group === null) && (this.notEditable[attribute.name] === undefined));
            })

            this.eavGroups.push({
                name: 'Прочие атрибуты',
                attribute_set: nonGroupAttributes
            })

            this.eavValues.forEach((value) => {
                value.label = value.value;
            })

            this.eavGroups.forEach((group) => {
                group.attribute_set.forEach((attribute) => {
                    attribute.value_set = attributesMap[attribute.id];
                    // attribute.active_values = this.eavValues.filter((value) => {
                    //     return value.attribute === attribute.id;
                    // })
                })
            })

            // for (let i=0; i<this.eavGroups.length; i++) {
            //     for (let y=0; y<this.eavGroups[i].attribute_set.length; y++) {
            //         this.eavGroups[i].attribute_set[y].active_values = [];
            //     }
            // }


            this.dataProcessed = true
        },
        tsoy() {
            console.log('hoy')
        }
    },
    watch: {
        activeTab() {
            if (this.activeTab == 'attributes') {
                this.initialize();
            }
        },
        dataIsReady() {
            if (this.dataIsReady) {
                this.processData();
            }
        },
        dataProcessed() {
            let self = this;
            setTimeout(function() {
                self.eavGroups.forEach((group) => {
                    group.attribute_set.forEach((attribute) => {
                        let activeValues = self.eavValues.filter((value) => {
                            return value.attribute === attribute.id;
                        })
                        activeValues.forEach((value) => {
                            attribute.active_values.push(value.id)
                        })
                    })
                })
            }, 0)
        }
    },
    filters: {
        length(values) {
            return values.length
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .offer-attributes {
        padding-top: 20px;
    }
    .group {
        margin-bottom: 30px;
    }
    .group-title {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 20px;
    }
    .attribute {
        display: inline-block;
        padding: 10px;
    }
    .group-attributes {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-start;
    }
    .attribute-name {
        font-size: 14px;
        margin-bottom: 5px;
    }
</style>
