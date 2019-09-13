<template>
    <div class="payments">
        <el-row :gutter="20">
            <el-col :span="12">
                <div>
                    <el-input>
                    </el-input>
                </div>
                <div>
                    <span>
                        К оплате:
                    </span>
                    <span>
                        400 Р
                    </span>
                </div>
                <div>
                    <el-button type="primary"
                        :disabled="!paymentIsAvailable"
                    >
                        Отправить платёж клиенту
                    </el-button>
                </div>
            </el-col>
            <el-col :span="12">
                <div class="title">
                    История платежей
                </div>
                <el-button type="primary" icon="el-icon-refresh" circle></el-button>
            </el-col>
        </el-row>
    </div>
</template>

<script>


export default {
    name: 'OrderPayments',
    data: () => ({
        loading: false,
    }),
    computed: {
        paymentIsAvailable() {
            return false
        }
    },
    created() {
    },
    methods: {
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
</style>
