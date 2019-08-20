<template>
    <div class="filter"
        @click.self="toggleDropdown"
    >
        {{attribute.name}}
        <div class="filter-badge" v-if="hasActiveValues">
            {{activeValuesCount}}
        </div>
        <i class="filter-icon el-icon-arrow-down">
        </i>
        <div class="filter-dropdown" v-if="showDropdown"
            v-on-click-outside="hideDropdown"
        >
            <div class="filter-loader" v-if="!responseReceived">
                <i class="el-icon-loading"></i>
            </div>
            <div class="filter-content" v-else>
                <ul class="values-list">
                    <li class="value" v-for="value in sortedValues"
                        :key="value.id"
                    >
                        <el-checkbox v-model="value.active">
                            {{value.value}}
                            <div class="value-count">
                                {{value.doc_count}}
                            </div>
                        </el-checkbox>
                        
                    </li>
                </ul>

                <div class="filter-buttons">
                    <div class="filter-button filter-button-1">
                        СБРОСИТЬ
                    </div>
                    <div class="filter-button filter-button-2">
                        ПРИМЕНИТЬ
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
import request from '@/utils/request'


export default {
    name: 'AttributeFilter',
    data: () => ({
        showDropdown: false,
        responseReceived: false,
        values: []
    }),
    props: [
        'attribute'
    ],
    computed: {
        params() {
            return {
                key: this.attribute.key
            }
        },
        sortedValues() {
            return this.values.sort((a,b) => {
                return b.doc_count - a.doc_count
            })
        },
        activeValuesCount() {
            return this.sortedValues.filter((value) => {
                return value.active
            }).length
        },
        hasActiveValues() {
            return this.activeValuesCount > 0
        }
    },
    created() {
    },
    methods: {
        toggleDropdown() {
            this.showDropdown = !this.showDropdown;
            if (this.showDropdown) {
                this.responseReceived = false;
                this.getValuesList();
            }
        },
        hideDropdown() {
            this.showDropdown = false;
        },
        getValuesList() {
            request.get('/search/facetes/', {params: this.params}).then(
                response => {
                    this.handleSuccessfulGetResponse(response);
                },
                response => {
                    this.handleFailedGetResponse(response);
                }
            )
        },
        handleSuccessfulGetResponse(response) {
            let counts = response.data.counts;
            let values = response.data.values;
            let countsMap = {};

            counts.forEach((count) => {
                countsMap[count.key] = count.doc_count;
            })

            values.forEach((value) => {
                let count = countsMap[value.id];
                if (count === undefined) {
                    count = 0;
                }
                value.doc_count = count;
                value.active = false;
            })
            
            this.values = values;
            console.log(this.values)
            this.responseReceived = true;
        },
        handleFailedGetResponse(response) {
            console.log(response);
        },
        triggerFiltering() {

        }
    },
    filters: {
    },
    watch: {
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    $grey: #dcdcdc;
    $accent: #f6de32;

    .filter {
        position: relative;
        display: inline-block;
        user-select: none;
        cursor: pointer;
        height: 36px;
        margin-bottom: 10px;
        line-height: 36px;
        padding: 0px 10px;
        transition: .3s;
        margin-left: -1px;
        border: 1px solid rgba(0,0,0,.12);
        &:hover {
            background: rgba(0,0,0,.12);
        }
        &:first-of-type {
            border-radius: 4px 0px 0px 4px;
        }
    }
    .filter-dropdown {
        top: 36px;
        left: 0px;
        width: 300px;
        padding: 10px 0px;
        max-height: 500px;
        background: white;
        position: absolute;
        border-bottom: 1px solid rgba(0,0,0,.12);
        border-left: 1px solid rgba(0,0,0,.12);
        border-right: 1px solid rgba(0,0,0,.12);
        box-shadow: 0 9px 15px 0 rgba(0,0,0,0.15);
        z-index: 100;
        border-radius: 0px 0px 8px 8px;
    }
    .filter-icon {
        font-size: 12px;
        margin-left: 2px;
    }
    .filter-loader {
        display: flex;
        height: 100px;
        width: 100%;
        align-items: center;
        justify-content: center;
        font-size: 28px;
    }

    .values-list {
        margin: 0px;
        max-height: 444px;
        padding-bottom: 50px;
        overflow-y: scroll;
    }

    .value {
        list-style: none;
    }
    .el-checkbox {
        position: relative;
        padding: 0px 40px 0px 20px;
        width: 100% !important;
        transition-duration: .3s;
        transition-property: background;
        &:hover {
            background: rgba(0,0,0,0.15);
        }
    }
    .el-checkbox.is-checked {
        background: rgba(246,222,50,.2);
    }
    .value-count {
        position: absolute;
        top: 0px;
        right: 20px;
        height: 100%;
        display: flex;
        align-items: center;
    }

    .filter-buttons {
        position: absolute;
        display: flex;
        height: 46px;
        bottom: 0px;
        width: 100%;
        left: 0px;
        z-index: 100;
    }
    .filter-button {
        width: 50%;
        height: 46px;
        line-height: 46px;
        text-align: center;
    }
    .filter-button-1 {
        background: $grey;
        border-radius: 0px 0px 0px 8px;
        &:hover {
            background: darken($grey, 10);
        }
    }
    .filter-button-2 {
        border-radius: 0px 0px 8px 0px;
        background: $accent;
        &:hover {
            background: darken($accent, 10);
        }
    }
    .filter-badge {
        position: absolute;
        right: -3px;
        top: -7px;
        font-size: 12px;
        background: $accent;
        height: 20px;
        width: 20px;
        border-radius: 10px;
        text-align: center;
        line-height: 20px;
        z-index: 10;
    }
</style>
