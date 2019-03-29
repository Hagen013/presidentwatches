<template>
    <div class="crud">
        <div class="crud__controls">
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
                        Кол-во атрибутов
                    </th>
                </tr>
                <tr class="table__row"
                    v-for="item in items"
                    :key="item.id"
                >
                    <td class="table__cell text_center">
                        {{item.id}}
                    </td>
                    <td class="table__cell">
                        {{item.name}}
                    </td>
                    <td class="table__cell">
                        {{item.attribute_set.length}}
                    </td>
                </tr>
            </table>
        </div>
    </div>
</template>

<script>
import request from '@/utils/request'


export default {
    name: 'AttributeGroups',
    data: () => ({
        apiUrl: '/eav/groups/',
        items: [],
        pageSize: 100,
        offset: 0,
        limit: 100,
        totalCount: 0,
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
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
</style>
