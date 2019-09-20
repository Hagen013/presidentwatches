<template>
    <div class="payments" v-loading="loading">
        <el-row :gutter="20">
            <el-col :span="10">
                <ol class="info">
                    <li>
                        Оплата может осуществляться только зарегестрированными пользователями.
                    </li>
                    <li>
                        Если пользователь незарегестрирован - он будет зарегестрирован по указанному ниже Email, после чего на него придет
                        ссылка для опаты.
                    </li>
                </ol>
                <div class="summary">
                    <span>
                        Сумма к оплате:
                    </span>
                    <span>
                        {{instance.total_price}} ₽
                    </span>
                </div>
                <div class="field">
                    <div class="field-label">
                        Email:
                    </div>
                    <div class="field-value">
                        <el-input
                            v-model="email"
                        >
                        </el-input>
                    </div>
                </div>
                <div>
                    <el-button type="primary"
                        :disabled="!emailIsValid"
                        @click="createPayment"
                    >
                        Отправить платёж клиенту
                    </el-button>
                </div>
            </el-col>
            <el-col :span="10">
                <div class="history">
                    <div class="history-topbar">
                        <div class="history-title">
                            История платежей:
                        </div>
                        <el-button type="primary" icon="el-icon-refresh" circle
                            @click="getPaymentsList"
                        >
                        </el-button>
                    </div>
                    <ul class="history-list">
                        <li v-for="item in payments"
                            class="payment"
                            :key="item.id"
                        >
                            <el-card class="payment">
                                <div class="payment-header">
                                    <div class="payment-title">
                                        Платёж № {{item.id}}
                                    </div>
                                    <div class="payment-status" :class="item.status">
                                        {{item.status|statusFilter}}
                                    </div>
                                </div>
                                <div class="payment-body">
                                    <el-timeline>
                                        <el-timeline-item
                                        v-for="(activity, index) in item.activities"
                                        :key="index"
                                        :timestamp="activity.timestamp"
                                        :color="activity.color"
                                        >
                                        {{activity.content}}
                                        </el-timeline-item>
                                    </el-timeline>
                                </div>
                                <div class="payment-footer">
                                    <div class="payment-link">
                                        <a class="link" :href="item.confirmation_url" target="_blank">
                                            Ссылка
                                        </a>
                                    </div>
                                    <div class="payment-amount">
                                        {{item.amount}} ₽
                                    </div>
                                </div>
                            </el-card>
                        </li>
                    </ul>
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import api from '@/utils/request'
import { validateEmail } from '@/utils/validate'

export default {
    name: 'OrderPayments',
    data: () => ({
        loading: false,
        email: '',
        payments: []
    }),
    computed: {
        paymentIsAvailable() {
            return false
        },
        emailIsValid() {
            return validateEmail(this.email)
        }
    },
    props: [
        'instance',
        'activeTabName'
    ],
    created() {
        if (this.activeTabName === 'payments') {
            this.initialize();
        }
    },
    methods: {
        initialize() {
            this.loading = true;
            if (this.instance.customer.email.length > 0) {
                this.email = this.instance.customer.email;
            }
            this.getPaymentsList();
        },
        getPaymentsList() {
            this.loading = true;
            api.get('payments/', {params: {order: this.instance.id}}).then(
                response => {
                    let payments = response.data;
                    payments.forEach((payment) => {
                        payment.activities = [];
                        payment.activities.push({
                            content: 'Создан',
                            timestamp: this.formatDate(payment.created_at),
                            color: '#E4E7ED'
                        })
                        if (payment.status === 'pending') {

                        } else if (payment.status === 'success') {
                            payment.activities.push({
                                content: 'Оплачен',
                                timestamp: this.formatDate(payment.resolved_at),
                                color: '#3abb37'
                            })
                        } else if (payment.status === 'fail') {
                            payment.activities.push({
                                content: 'Ошибка',
                                timestamp: this.formatDate(payment.resolved_at),
                                color: '#f82c4b'
                            })
                        }
                    })
                    this.payments = response.data;
                    this.loading = false;
                },
                response => {

                }
            )
        },
        createPayment() {
            let payload = {
                email: this.email,
                user: this.instance.user,
                order: this.instance.id,
                phone: this.instance.customer.phone,
                name: this.instance.customer.name
            }
            this.loading = true;
            api.post(`/payments/create/`, payload).then(
                response => {
                    let payment = response.data.payment;
                    let user = response.data.user;

                    payment.activities = [];
                    payment.activities.push({
                        content: 'Создан',
                        timestamp: this.formatDate(payment.created_at),
                        color: '#E4E7ED'
                    })
                    this.payments.push(payment);

                    if (this.instance.user === null) {
                        this.updateUser(user);
                    }

                    this.loading = false;
                    this.$notify({
                        title: `Платеж № ${payment.id}`,
                        message: `успено отправлен на указанный адрес`,
                        type: 'success'
                    });
                },
                response => {
                    this.loading = false;
                }
            )
        },
        formatDate(datetime) {
            let date = new Date(datetime);
            return `
                ${date.getFullYear()}-${date.getMonth()}-${date.getDate()}  ${date.getHours()}:${date.getMinutes()}
            `
        },
        updateUser(user) {
            this.$emit('update-user', user);
        }
    },
    watch: {
        activeTabName() {
            if (this.activeTabName === 'payments') {
                this.initialize();
            }
        }
    },
    filters: {
        statusFilter(state) {
            if (state === 'pending') {
                return 'В ожидании'
            } else if (state === 'success') {
                return 'оплачен'
            } else {
                return 'Ошибка'
            }
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    ol {
        list-style: none;
    }
    ol li {
        counter-increment: my-awesome-counter;
    }
    ol li::before {
        content: counter(my-awesome-counter) ". ";
    }
    .info {
        max-width: 500px;
        line-height: 1.5;
        color: rgba(0,0,0,0.9);
        li {
            margin-bottom: 10px;
        }
    }
    .history-topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .history-title {
        font-weight: 600;
        font-size: 24px;
    }
    .history-list {
        list-style: none;
    }
    .field {
        display: flex;
        width: 100%;
        align-items: center;
        margin-bottom: 20px;
    }
    .field-label {
        margin-right: 10px;
    }
    .field-value {
        width: 350px;
    }
    .summary {
        margin-bottom: 20px;
    }
    .payment-header {
        display: flex;
        justify-content: space-between;
    }
    .payment-status {
        letter-spacing: 1px;
        text-transform: lowercase;
        font-size: 14px;
    }
    .payment-status.pending {
        color: #f57e39;
    }
    .payment-status.success {
        color: #3abb37;
    }
    .payment-status.fail {
        color: #fc152e;
    }
    .payment-amount {
        font-size: 24px;
        text-align: right;
        font-weight: 600;
    }
    .payment-footer {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }
    .link {
        text-transform: lowercase;
        color: #4c4dc1;
        text-decoration: underline;
    }
    .payment {
        margin-bottom: 10px;
    }
    .payment-body {
        padding: 20px 0px 10px 0px;
    }
</style>
