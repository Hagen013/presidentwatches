<template>
    <div class="crud">
        <div class="crud__controls">
            <div class="filters">
                <el-row>
                    <el-col :span="8">
                        <div class="grid-content">
                            <div class="filters__header"
                                @click="displayFilters = !displayFilters"
                            >
                                <div class="filters__title">
                                    Фильтры
                                </div>
                                <i class="filters__arrow el-icon-arrow-down"
                                    :class="{ 'is-active': displayFilters }"
                                >
                                </i>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="8">
                        <div class="grid-content">
                            <div class="placeholder">
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="8">
                        <div class="grid-content">
                            <div class="filters__buttons">
                                <el-button
                                    type="primary"
                                >
                                    Создать
                                </el-button>
                            </div>
                        </div>
                    </el-col>
                </el-row>
                <el-collapse-transition>
                    <div class="filters__content"
                        v-if="displayFilters"
                    >
                        <el-row>
                            <el-col :span="8">
                                <div class="grid-content">
                                    <el-input
                                        class="filters__search"
                                        placeholder="Поиск по имени"
                                        suffix-icon="el-icon-search"
                                    >
                                    </el-input>
                                </div>
                            </el-col>
                            <el-col :span="8"><div class="grid-content"></div></el-col>
                            <el-col :span="8"><div class="grid-content"></div></el-col>
                        </el-row>
                    </div>
                </el-collapse-transition>
            </div>
        </div>
        <div class="crud__content">
            <table class="table">
                <tr class="table__header">
                    <th class="table__head text_center">
                        ID
                    </th>
                    <th class="table__head text_left">
                        Название
                    </th>
                    <th class="table__head text_left">
                        Тип
                    </th>
                    <th class="table__head text_left">
                        Кол-во значений
                    </th>
                </tr>
                <tr class="table__row"
                    v-for="item in items"
                    :key="item.id"
                    @click="selectionRedirect(item)"
                >
                    <td class="table__cell text_center">
                        {{item.id}}
                    </td>
                    <td class="table__cell">
                        {{item.name}}
                    </td>
                    <td class="table__cell">
                        {{item.datatype|attributeDatatypeFilter}}
                    </td>
                    <td class="table__cell text_left">
                        {{item|countValuesFilter}}
                    </td>
                </tr>
            </table>
        </div>
    </div>
</template>

<script>
import request from '@/utils/request'

const attributeDatatypeMapping = {
    '1': 'Text',
    '2': 'Integer',
    '3': 'Float',
    '4': 'Bool',
    '5': 'Choice',
    '6': 'MultiChoice'
}

const countableAttributeDatatypes = [5,6]

export default {
    name: 'Attributes',
    data: () => ({
        apiUrl: '/eav/attributes/',
        items: [],
        pageSize: 100,
        offset: 0,
        limit: 100,
        totalCount: 0,
        displayFilters: false
    }),
    computed: {
        queryParams() {
            return {
                offset: this.offset,
                limit: this.limit
            }
        }
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            this.getList();
        },
        getList() {
            request.get(this.apiUrl, {params: this.queryParams}).then(
                response => {
                    this.handleSuccessfulListResponse(response);
                },
                response => {
                    this.handleFailedListResponse(response);
                }
            )
        },
        handleSuccessfulListResponse(response) {
            this.items = response.data['results'];
            this.totalCount = response.data['count'];
        },
        handleFailedListResponse(response) {
            console.log(response);
        },
        selectionRedirect(instance) {
            let path = `attributes/${instance.id}`;
            this.$router.push({path: path});
        }
    },
    filters: {
        attributeDatatypeFilter(value) {
            return attributeDatatypeMapping[String(value)]
        },
        countValuesFilter(instance) {
            if (countableAttributeDatatypes.indexOf(instance.datatype) !== -1) {
                return instance.value_set.length
            } else {
                return '...'
            }
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .crud__controls {
        padding: 16px;
    }
    .filters {
    }
    .filters__content {

    }
    .placeholder {
        height: 1px;
        width: 1px;
    }
    .filters__buttons {
        display: flex;
        justify-content: flex-end;
        padding: 0px 24px 0px 0px;
    }
</style>
