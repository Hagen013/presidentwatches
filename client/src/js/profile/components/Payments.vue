<template>
    <div class="payments">
        <ul class="payments-list">
            <li class="payment" v-for="payment in payments"
                :key="payment.id"
            >
                <div class="payment-heading">
                    <div class="payment-title">
                        {{payment.description}}
                    </div>
                    <div class="payment-status" :class="payment.status">
                        {{payment.status|statusFilter}}
                    </div>
                </div>
                <div class="payment-body">
                </div>
                <div class="payment-footer">
                    <a class="payment-link button button_accent">
                        ОПЛАТИТЬ
                    </a>
                    <div class="payment-price">
                        <span class="price">
                            {{payment.amount}}
                        </span>
                    </div>
                </div>
            </li>
        </ul>
    </div>
</template>

<script>
import api from '@/api/'

export default {
    name: "Payments",
    data: () => ({
        loading: false,
        payments: []
    }),
    created() {
        if (this.ready) {
            this.initialize();
        }
    },
    computed: {
        userId() {
            return this.$store.state.user.id
        },
        ready() {
            return (this.userId !== null)
        }
    },
    methods: {
        initialize() {
            this.getPaymentsList();
        },
        getPaymentsList() {
            api.get('/payments/', {params: {user: this.userId}}).then(
                response => {
                    this.payments = response.data;
                },
                response => {

                }
            )
        }
    },
    watch: {
        ready() {
            this.initialize();
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