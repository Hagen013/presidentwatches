<template>
    <div class="form-container">
        <div class="orders">
            <div class="orders-controls">
                <el-row :gutter="20">
                    <el-col :span="8">
                        <el-input v-model="queryId"
                            placeholder="Номер заказа"
                        >
                        </el-input>
                    </el-col>
                    <el-col :span="8">
                        <el-input v-model="queryPhone"
                            placeholder="Номер телефона"
                        >
                        </el-input>
                    </el-col>
                    <el-col :span="8">
                        <el-input v-model="queryName"
                            placeholder="Имя клиента"
                        >
                        </el-input>
                    </el-col>
                </el-row>
            </div>
            <table class="table">
                <tr class="table-row">
                    <th class="table-head">
                        ID
                    </th>
                    <th class="table-head">
                        СОЗДАН
                    </th>
                    <th class="table-head">
                        КЛИЕНТ
                    </th>
                    <th class="table-head">
                        СТАТУС
                    </th>
                    <th class="table-head">
                        ДОСТАВКА
                    </th>
                    <th class="table-head">
                        ОПЛАТА
                    </th>
                </tr>
                <tr class="table-row"
                    v-for="order in orders"
                    :key="order.id"
                >
                    <td class="table-cell">
                        <div class="table-container">
                            {{order.id}}
                        </div>
                    </td> 
                    <td class="table-cell">
                        <div class="table-container">
                            23.06.2019
                        </div>
                    </td>
                    <td class="table-cell">
                        <div class="table-container">
                            Имя Фамилия Отчество
                        </div>
                    </td>
                    <td class="table-cell">
                        <div class="table-container">
                            Новый
                        </div>
                    </td>
                    <td class="table-cell">
                        <div class="table-container">
                            270 
                        </div>
                    </td>
                </tr>
            </table>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Orders',
    data: () => ({
        queryId: '',
        queryPhone: '',
        queryName: '',
        orders: [
            {'id': 1},
            {'id': 2}
        ]
    }),
    computed: {
    },
    methods: {

    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .orders {
        padding: 20px;
    }
    .orders-controls {
        margin-bottom: 30px;
    }
    .table-cell {
        height: 40px;
        border-top-color: rgba(0,0,0,.12);
        border-top: 1px solid rgba(0,0,0,.12);
    }
</style>
