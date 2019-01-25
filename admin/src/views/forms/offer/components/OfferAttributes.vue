<template>
    <div class="tab-content offer-attributes"
        v-loading="!dataIsReady"
    >
        <attttribute-field
            v-for="attribute in attributes"
            :key="attribute.id"
            :attribute="attribute"
            :options="attribute.value_set"
            :values="values"
            v-on:add-option="addActiveOption"
            v-on:remove-option="removeActiveOption"
            v-on:change-option="changeOption"
        >
        </attttribute-field>
    </div>
</template>

<script>
import Vue from 'vue'

import request from '@/utils/request'

import attributeField from '@/components/AttributeField'


export default {
    name: 'OfferAttributes',
    components: {
        'attttribute-field': attributeField
    },
    data: () => ({
        groups: [],
        attributes: [],
        values: [],
        eavAttributesResponseReceived: false,
        eavGroupsResponseReceived: false,
        eavInstanceResponseReceived: false,
        requestError: false,
        groupsApiUrl: '/eav/groups/',
        attributesApiUrl: '/eav/attributes/'
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

        },
        rollbackChanges() {

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
        processAttributes() {
            let attributes = this.attributes;
            for (let i=0; i<this.attributes.length; i++) {
                this.attributes[i].activeOptions = this.values.filter(function(value) {
                    return value.attribute === attributes[i].id
                })
            }
        },
        addActiveOption(option) {
            for (let i=0; i<this.attributes.length; i++) {
                if (this.attributes[i].id === option.attribute) {
                    this.attributes[i].activeOptions.push(option);
                    break
                } 
            }
        },
        removeActiveOption(option) {
            for (let i=0; i<this.attributes.length; i++) {
                if (this.attributes[i].id === option.attribute) {
                    for (let y=0; y<this.attributes[i].activeOptions.length; y++) {
                        let value = this.attributes[i].activeOptions[y];
                        if (value.id === option.id) {
                            console.log('triggered');
                            console.log(this.attributes[i].activeOptions.length);
                            let attribute = this.attributes[i];
                            attribute.activeOptions.splice(y,1);
                            Vue.set(this.attributes, i, attribute);
                            console.log(this.attributes[i].activeOptions.length);
                            this.$forceUpdate();
                            break
                        }
                    }
                    break
                }
            }
        },
        changeOption(option) {
            for (let i=0; i<this.attributes[i]; i++) {
                if (this.attribute[i].id === option.attribute) {
                    this.attributes[i].activeOptions = [option,]
                    break
                }
            }
        }
    },
    watch: {
        activeTab() {
            if (this.activeTab === 'attributes') {
                this.initialize();
            }
        },
        dataIsReady() {
            if (this.dataIsReady) {
                this.processAttributes();
            }
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .tab-content  {
        padding-top: 32px;
    }
</style>
