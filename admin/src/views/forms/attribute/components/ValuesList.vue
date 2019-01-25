<template>
    <div class="app-container"
    >
        <div class="values">
            <table class="table">
                <tr class="table__header"
                >
                    <th class="table__head text_left">
                        ID
                    </th>
                    <th class="table__head text_left">
                        Значение
                    </th>
                    <th class="tabel__head text_left">
                        Порядок
                    </th>
                </tr>
                <tr class="table__row"
                    v-for="item in attribute.value_set"
                    :key="item.id"
                >
                    <td class="table__cell">
                    {{item.id}}
                    </td>
                    <td class="table__cell">
                    {{item.value}}
                    </td>
                    <td class="table__cell">
                    {{item.order}}
                    </td>
                </tr>
            </table>
        </div>
    </div>
</template>

<script>
import request from '@/utils/request'

export default {
    name: 'Attribute',
    data: () => ({
    }),
    props: ['attribute'],
    computed: {
    },
    created() {
    },
    methods: {
        createInstance() {
        },
        selectionRedirect() {
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
</style>
