<template>
    <div class="filter"
        
    >
        <div class="filter-body"
            @click="toggleDropdown"
        >
            {{attribute.name}}
            <i class="filter-icon el-icon-arrow-down">
            </i>
            <div class="filter-badge" v-if="hasActiveValues">
                {{activeValuesCount}}
            </div>
        </div>
        <div class="filter-dropdown" v-if="showDropdown"
            v-on-click-outside="hideAndCheck"
            :style="{ left: dropdownOffset + 'px' }"
        >
            <div class="filter-loader" v-if="!responseReceived">
                <i class="el-icon-loading"></i>
            </div>
            <div class="filter-content" v-else>
                <div class="filter-input-box"
                    v-if="showSearch"
                >
                    <el-input
                        v-model="query"
                        suffix-icon="el-icon-search"
                        placeholder="Поиск"
                    >
                    </el-input>
                </div>
                <ul class="values-list"
                    :class="{ extended : showSearch }"
                >
                    <li class="value" v-for="value in sortedValues"
                        :key="value.id"
                    >
                        <el-checkbox v-model="value.active"
                            :disabled="value.disabled"
                        >
                            {{value.value}}
                            <div class="value-count">
                                {{value.doc_count}}
                            </div>
                        </el-checkbox>
                        
                    </li>
                </ul>

                <div class="filter-buttons">
                    <div class="filter-button filter-button-1"
                        @click="clearFiltering"
                    >
                        СБРОСИТЬ
                    </div>
                    <div class="filter-button filter-button-2"
                        @click="hideAndCheck"
                    >
                        ПРИМЕНИТЬ
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
import request from '@/utils/request'
import fuzzy from 'fuzzysearch'


export default {
    name: 'AttributeFilter',
    data: () => ({
        showDropdown: false,
        responseReceived: false,
        values: [],
        params: {},
        query: "",
    }),
    props: [
        'attribute',
        'facetes'
    ],
    created() {
        this.params = {key: this.attribute.key}
    },
    computed: {
        filteredValues() {
            return this.values.filter((value) => {
                return fuzzy(this.query.toLowerCase(), value.value.toLowerCase())
            })
        },
        sortedValues() {
            return this.filteredValues.sort((a,b) => {
                return b.doc_count - a.doc_count
            })
        },
        activeValues() {
            return this.sortedValues.filter((value) => {
                return value.active
            })
        },
        activeValuesCount() {
            if (!this.responseReceived) {
                let facetes = this.facetes[this.attribute.key];
                if (facetes === undefined) {
                    return 0
                } else {
                    return facetes.length
                }
            } else {
                return this.activeValues.length
            }
        },
        hasActiveValues() {
            return this.activeValuesCount > 0
        },
        showSearch() {
            return this.values.length > 11;
        },
        dropdownOffset() {
            let el = this.$el;
            let parent = el.parentNode;
            let offsetLeft = el.offsetLeft;
            let windowWidth = window.innerWidth;
            let dropdownWidth = 330;


            if (windowWidth - (offsetLeft + dropdownWidth) < dropdownWidth) {
                return (dropdownWidth - (windowWidth - (offsetLeft + dropdownWidth)) ) * -1
            }

            return 0
        }
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
            let params = {key: this.attribute.key, is_in_stock: false};
            let facetes =  JSON.parse(JSON.stringify(this.facetes));

            if (facetes[this.attribute.key] !== undefined) {
                delete facetes[this.attribute.key];
            }
            for (let key in facetes) {
                if ( (facetes[key] !== undefined) && (facetes[key].length > 0) ) {
                    let values = facetes[key];
                    values = values.filter((value) => {
                        return value !== 'none'
                    })
                    if (values.length > 0) {
                        values = values.join(',');
                        params[key] = values;
                    }
                }
            }
            request.get('/search/facetes/', {params: params}).then(
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
            let countsMap = {};
            let values = null;
            counts.forEach((count) => {
                countsMap[count.key] = count.doc_count;
            })

            if (this.values.length === 0) {
                values = response.data.values;
                if (this.attribute.name !== 'Бренд') {
                    values.unshift({
                        value: 'Не указано',
                        disabled: false,
                        active: false,
                        id: 'none'
                    })
                }
            } else {
                values = this.values;
            }
            values.forEach((value) => {
                let count = countsMap[value.id];
                if ( (count === undefined) && (value.value !== 'Не указано') ) {
                    count = 0;
                    value.doc_count = 0;
                    value.disabled = true;
                } else {
                    value.doc_count = count;
                    value.disabled = false;
                }
            })
            if (this.facetes[this.attribute.key] !== undefined) {
                values.forEach((value) => {
                    if (this.facetes[this.attribute.key].indexOf(value.id) !== -1) {
                        value.active = true;
                    }
                })
            }
            this.values = values;
            this.responseReceived = true;
        },
        handleFailedGetResponse(response) {
        },
        clearFiltering() {
            this.values.forEach((value) => {
                value.active = false;
            })
            this.$emit('clear', this.attribute.key);
            this.showDropdown = false;
        },
        triggerFiltering() {
            let values = this.activeValues.map((value) => {
                return value.id
            })
            this.$emit('filter', {key: this.attribute.key, values: values});
        },
        hideAndCheck() {
            this.triggerFiltering();
            this.showDropdown = false;
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
        transition: .3s;
        margin-left: -1px;
        border: 1px solid rgba(0,0,0,.12);
        &:first-of-type {
            border-radius: 4px 0px 0px 4px;
        }
    }
    .filter-body {
        padding: 0px 10px;
        transition: .3s;
        &:hover {
            background: rgba(0,0,0,.12);
        }
    }
    .filter-dropdown {
        top: 35px;
        left: 0px;
        width: 330px;
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
    }

    .values-list.extended {
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
    .filter-input-box {
        padding: 0px 10px;
        margin-bottom: 5px;
    }
</style>
