<template>
    <div class="tab-content offer-attributes"
        v-loading="!dataIsReady"
    >
        <div class="offer-attributes__attribute-wrap"
            v-for="attribute in attributes"
            :key="attribute.id"
        >
            <div class="offer-attributes__content"
                v-if="attributesInitialized"
            >
                <multi-choice
                    v-if="attribute.datatype===6"
                    :attribute="attribute"
                    :options="attribute.value_set"
                    :active_options="attribute.activeOptions"
                    v-on:add-option="addActiveOption"
                    v-on:remove-option="removeActiveOption"
                >
                </multi-choice>
                <choice
                    v-else-if="attribute.datatype===5"
                    :attribute="attribute"
                    :options="attribute.value_set"
                    :active_options="attribute.activeOptions"
                    @change="handleChoiceChange"
                >
                </choice>
                <text-field
                    v-else-if="attribute.datatype===1"
                    :attribute="attribute"
                    :options="attribute.value_set"
                    :active_options="attribute.activeOptions"
                    @change="handleValueChange"
                >
                </text-field>
                <integer-field
                    v-else-if="attribute.datatype===2"
                    :attribute="attribute"
                    :options="attribute.value_set"
                    :active_options="attribute.activeOptions"
                    v-on:clear="clearAttributeActiveValues"
                    @change="handleValueChange"
                >
                </integer-field>
                <float-field
                    v-else-if="attribute.datatype===3"
                    :attribute="attribute"
                    :options="attribute.value_set"
                    :active_options="attribute.activeOptions"
                    v-on:clear="clearAttributeActiveValues"
                    @change="handleValueChange"
                >
                </float-field>
                <bool-field
                    v-else-if="attribute.datatype===4"
                    :attribute="attribute"
                    :options="attribute.value_set"
                    :active_options="attribute.activeOptions"
                    v-on:clear="clearAttributeActiveValues"
                    @change="handleValueChange"
                >
                </bool-field>
            </div>
        </div>
    </div>
</template>

<script>
const equal = require('fast-deep-equal');

import {Vue} from '@/vue.js'
import request from '@/utils/request'

import TextField from '@/components/AttributeFields/Text'
import IntegerField from '@/components/AttributeFields/Integer'
import FloatField from '@/components/AttributeFields/Float'
import BoolField from '@/components/AttributeFields/Bool'
import ChoiceAttributeField from '@/components/ChoiceAttributeField'
import MultiChoiceAttributeField from '@/components/MultiChoiceAttributeField'


export default {
    name: 'OfferAttributes',
    components: {
        'multi-choice': MultiChoiceAttributeField,
        'choice': ChoiceAttributeField,
        'text-field': TextField,
        'integer-field': IntegerField,
        'float-field': FloatField,
        'bool-field': BoolField
    },
    data: () => ({
        groups: [],
        attributes: [],
        values: [],
        proxyAttributes: [],
        eavAttributesResponseReceived: false,
        eavGroupsResponseReceived: false,
        eavInstanceResponseReceived: false,
        requestError: false,
        groupsApiUrl: '/eav/groups/',
        attributesApiUrl: '/eav/attributes/',
        hasChanged: false,
        attributesInitialized: false
    }),
    props: [
        'instance',
        'activeTab'
    ],
    computed: {
        dataIsReady() {
            return (
                this.eavAttributesResponseReceived === true &&
                this.eavGroupsResponseReceived === true &&
                this.eavInstanceResponseReceived === true
            )
        },
        instanceValuesApiUrl() {
            return `/products/${this.instance['id']}/values/`
        },
        sortedAttributes() {
            let attributes = this.attributes.sort(function(a, b) {
                return a.order - b.order
            })
            return attributes
        }
    },
    created() {
        if (this.activeTab === 'attributes') {
            this.initialize();
        }
    },
    methods: {
        initialize() {
            this.getGroups();
            this.getAttributes();
            this.getInstanceValues();
        },
        saveChanges() {
            let params = {'bulk': true};
            let values = this.attributes.map(function(attribute) {
                return attribute.activeOptions
            });
            values = [].concat.apply([], values);
            this.eavInstanceResponseReceived = false;
            request.post(this.instanceValuesApiUrl, values, {params: params}).then(
                response => {
                    this.handleSuccessfulUpdateResponse(response);
                },
                response => {
                    this.handleFailedUpdateResponse(response);
                }
            )
        },
        rollbackChanges() {
            console.log('triggered');
            console.log(this.attributes);
            console.l
            this.attributes = JSON.parse(JSON.stringify(this.proxyAttributes));
            this.checkStatus();
        },
        getGroups() {
            request.get(this.groupsApiUrl).then(
                response => {
                    this.handleSuccessfulGetGroupsResponse(response);
                },
                response => {
                    this.handleFailedGetGroupsResponse(response);
                }
            )
        },
        getAttributes() {
            request.get(this.attributesApiUrl).then(
                response => {
                    this.handleSuccessfulGetAttributesResponse(response);
                },
                response => {
                    this.handleSuccessfulGetAttributesResponse(response);
                }
            )
        },
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
        handleSuccessfulGetGroupsResponse(response) {
            this.groups = response.data['results'];
            this.eavGroupsResponseReceived = true;
        },
        handleFailedGetGroupsResponse(response) {
            this.eavGroupsResponseReceived = true;
            this.requestError = true;
        },
        handleSuccessfulGetAttributesResponse(response) {
            this.attributes = response.data['results'];
            this.eavAttributesResponseReceived = true;
        },
        handleFailedGetAttributesResponse(response) {
            this.eavAttributesResponseReceived = true;
            this.requestError = true;
        },
        handleSuccessfulGetValuesResponse(response) {
            this.values = response.data['results'];
            this.eavInstanceResponseReceived = true;
        },
        handleFailedGetValuesResponse(response) {
            this.eavInstanceResponseReceived = true;
            this.requestError = true;
        },
        handleSuccessfulUpdateResponse(response) {
            this.values = response.data['results'];
            this.eavInstanceResponseReceived = true;
        },
        handleFailedUpdateResponse(response) {
            this.eavInstanceResponseReceived = true;
            this.requestError = true;
        },
        processAttributes() {
            let attributes = this.attributes;
            for (let i=0; i<this.attributes.length; i++) {
                this.attributes[i].activeOptions = this.values.filter(function(value) {
                    return value.attribute === attributes[i].id
                })
            }
            this.proxyAttributes = JSON.parse(JSON.stringify(this.attributes));
            this.attributesInitialized = true;
        },
        getAttributeByOption(option) {
            let attribute = null;
            let index = null;
            for (let i=0; i<this.attributes.length; i++) {
                if (this.attributes[i].id === option.attribute) {
                    attribute = JSON.parse(JSON.stringify(this.attributes[i]));
                    index = i;
                    break
                }
            }
            return {attribute: attribute, index: index}
        },
        addActiveOption(option) {
            let {attribute, index} = this.getAttributeByOption(option);
            attribute.activeOptions.push(option);
            this.$set(this.attributes, index, attribute);
        },
        removeActiveOption(option) {
            let {attribute, index} = this.getAttributeByOption(option);
            for (let i=0; i<attribute.activeOptions.length; i++) {
                let iterationOption = attribute.activeOptions[i];
                if (iterationOption.id === option.id) {
                    attribute.activeOptions.splice(i, 1);
                    this.$set(this.attributes, index, attribute)
                    break
                }
            }
        },
        handleChoiceChange(option) {
            let {attribute, index} = this.getAttributeByOption(option);
            attribute.activeOptions = [option,];
            this.$set(this.attributes, index, attribute);
        },
        handleValueChange(option) {
            let {attribute, index} = this.getAttributeByOption(option);
            attribute.activeOptions = [option,];
            this.$set(this.attributes, index, attribute);
        },
        clearAttributeActiveValues(attribute) {
            for (let i=0; i<this.attributes.length; i++) {
                if (attribute.id === this.attributes[i].id) {
                    let instance = JSON.parse(JSON.stringify(this.attributes[i]));
                    instance.activeOptions = [];
                    this.$set(this.attributes, i, instance);
                }
            }
        },
        checkStatus() {
            this.hasChanged = !equal(this.attributes, this.proxyAttributes);
            this.$emit('change', this.hasChanged);
        },
    },
    watch: {
        activeTab() {
            if (this.activeTab === 'attributes') {
                if (!this.dataIsReady) {
                    this.initialize();
                }
            }
        },
        dataIsReady() {
            if (this.dataIsReady) {
                this.processAttributes();
            }
        },
        attributes: {
            handler() {
                this.checkStatus();
            },
            deep: true
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .offer-attributes {
        padding-bottom: 100px;
    }
    .tab-content  {
        padding-top: 32px;
    }
    .attribute-field {
        margin-bottom: 24px;
    }
    .attribute-field__title {
        margin-bottom: 8px;
    }
    .attribute-field__input-box {
        margin-bottom: 8px;
    }
    .el-tag {
        margin-right: 8px;
    }
    .el-select {
        width: 320px;
    }
</style>
