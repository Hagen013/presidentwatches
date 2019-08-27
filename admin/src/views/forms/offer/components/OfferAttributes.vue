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
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value"
                                >
                                </el-option>
                            </el-select>
                            <div v-else-if="attribute.datatype==3">
                                <div class="switcher">
                                    <el-switch
                                        v-model="attribute.disabled"
                                        active-text="Не указывать"
                                        @change="handleNumericSwitch(attribute)"
                                    >
                                    </el-switch>
                                </div>
                                <el-input-number
                                    v-if="!attribute.disabled"
                                    v-model="attribute.active_values"
                                    controls-position="right"
                                >
                                </el-input-number>
                            </div>
                            <div v-else-if="attribute.datatype==2">
                                <div class="switcher">
                                    <el-switch
                                        v-model="attribute.disabled"
                                        active-text="Не указывать"
                                        @change="handleNumericSwitch(attribute)"
                                    >
                                    </el-switch>
                                </div>
                                <el-input-number
                                    v-if="!attribute.disabled"
                                    v-model="attribute.active_values"
                                    controls-position="right"
                                    @change="handleIntegerChange(attribute)"
                                >
                                </el-input-number>
                            </div>
                            <el-input placeholder="Не указано" 
                                v-if="attribute.datatype==1"
                                v-model="attribute.active_values"
                            >
                            </el-input>
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
            'Распродажа': true,
            'Новинка': true,
            'Бренд': true,
            'СССР': true,
            'Армейские': true,
            "Gold'n'Black": true
        },
        hasChanged: false,
        pending: false
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
            this.hasChanged = false;
            this.$emit('change', this.hasChanged);
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
                    let activeValues =  this.eavValues.filter((value) => {
                        return value.attribute === attribute.id;
                    })
                    if (attribute.datatype === 6) {
                        activeValues = activeValues.map((value) => {
                            return value.id
                        })
                        this.$set(attribute, 'active_values', activeValues);
                    } else if (attribute.datatype === 5) {
                        activeValues = activeValues.map((value) => {
                            return value.id
                        })
                        if (activeValues.length > 0) {
                            this.$set(attribute, 'active_values', activeValues[0]);
                        } else {
    
                        }
                    } else if (attribute.datatype === 4) {
                        let valueset = [
                            {label: 'Да', value: true},
                            {label: 'Нет', value: false},
                            {label: 'Не указано', value: null}
                        ];
                        this.$set(attribute, 'value_set', valueset);

                        if (activeValues.length > 0) {
                            this.$set(attribute, 'active_values', activeValues[0].value);
                        } else {
                            this.$set(attribute, 'active_values', null);
                        }
                    } else if ( (attribute.datatype === 3) || (attribute.datatype === 2) ) {
                        activeValues = activeValues.map((value) => {
                            return value.value
                        })
                        if (activeValues.length > 0) {
                            this.$set(attribute, 'disabled', false);
                            this.$set(attribute, 'active_values', activeValues[0]);
                        } else {
                            this.$set(attribute, 'disabled', true);
                            this.$set(attribute, 'active_values', null);
                        }
                    } else if (attribute.datatype === 1) {
                        if (activeValues.length > 0) {
                            this.$set(attribute, 'active_values', activeValues[0].value);
                        } else {
                            this.$set(attribute, 'active_values', "");
                        }
                    }
                    this.eavGroupsProxy = JSON.parse(JSON.stringify(this.eavGroups));
                })
            })

            this.dataProcessed = true
        },
        checkStatus() {
            this.hasChanged = !equal(this.eavGroups, this.eavGroupsProxy);
            this.$emit('change', this.hasChanged);
        },
        handleNumericSwitch(attribute) {
            if (attribute.disabled) {
                attribute.active_values = null;
            } else {
                attribute.active_values = 0;
            }
        },
        handleIntegerChange(attribute) {
            attribute.active_values = parseInt(attribute.active_values)
        },
        saveChanges() {
            let attributes = [];
            for (let i=0; i<this.eavGroups.length; i++) {
                for (let y=0; y<this.eavGroups[i].attribute_set.length; y++) {
                    let attribute = this.eavGroups[i].attribute_set[y];
                    let attributeProxy = this.eavGroupsProxy[i].attribute_set[y];
                    if (!equal(attribute, attributeProxy)) {
                        attributes.push({
                            id: attribute.id,
                            datatype: attribute.datatype,
                            values: attribute.active_values
                        })
                    }
                }
            }
            let data = {bulk: true, attributes: attributes};
            request.post(`/products/${this.instance.id}/values/`, data).then(
                response => {
                    this.handleSuccessfulSaveResponse(response);
                },
                response => {
                    this.handleFailedSaveResponse(response);
                }
            )
        },
        rollbackChanges() {
            this.dataProcessed = false;
            this.syncData();
        },
        handleSuccessfulSaveResponse(response) {
            this.dataProcessed = false;
            this.syncData();
            this.$notify({
                title: 'Сообщение',
                message: 'Атрибуты обновлены'
            });
        },
        handleFailedSaveResponse(response) {

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
        eavGroups: {
            handler() {
                if (this.dataProcessed) {
                    this.checkStatus();
                }
            },
            deep: true
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
    .switcher {
        margin-bottom: 10px;
    }
</style>
