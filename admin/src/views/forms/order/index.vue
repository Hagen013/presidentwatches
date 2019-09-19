<template>
    <div class="order-wrap" v-loading="loading">
        <div class="topbar">
            <el-button type="primary" size="medium"
                @click="redirectToOrdersList"
            >
                <el-icon class="el-icon-back">
                </el-icon>
                Назад
            </el-button>
            <div class="order-id">
                Заказ № 
                <transition name="el-fade-in">
                    <span v-if="isReady">
                    {{publidId}}
                    </span>
                </transition>
            </div>
            <el-button type="success" size="medium"
                :disabled="!hasChanged"
                @click="saveChanges"
            >
                <el-icon class="el-icon-check">
                </el-icon>
                Сохранить
            </el-button>
            <el-button type="danger" size="medium"
                :disabled="!hasChanged"
                @click="rollbackChanges"
            >
                <el-icon class="el-icon-refresh-right">
                </el-icon>
                Отменить изменения
            </el-button>
        </div>
        <el-tabs v-model="activeTabName" type="card">
            <el-tab-pane label="Заказ" name="main">
                <div v-if="isReady">
                    <order-main
                        :instance_proxy="instance"
                        :is_ready="isReady"
                        @change="handleMainChange"
                        ref="main"
                    >
                    </order-main>
                </div>
            </el-tab-pane>
            <el-tab-pane label="Трекинг доставки" name="tracking">
                <order-tracking
                    :instance="instance"
                    :is_ready="isReady"
                >
                </order-tracking>
            </el-tab-pane>
            <el-tab-pane label="Клиент" name="user">
                <order-user
                    :instance="instance"
                    :is_ready="isReady"
                >
                </order-user>
            </el-tab-pane>
            <el-tab-pane label="Оплата" name="payments">
                <div v-if="isReady">
                    <order-payments
                        :instance="instance"
                        :is_ready="isReady"
                        :activeTabName="activeTabName"
                        v-on:update-user="updateUser"
                    >
                    </order-payments>
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import api from '@/utils/request'

import OrderMain from './components/Main'
import OrderTracking from './components/Tracking'
import OrderUser from './components/User'
import OrderPayments from './components/Payments'

export default {
    name: 'Order',
    components: {
        'order-main': OrderMain,
        'order-tracking': OrderTracking,
        'order-user': OrderUser,
        'order-payments': OrderPayments
    },
    mixins: [],
    data: () => ({
        loading: true,
        activeTabName: 'main',
        instanceId: '',
        instance: null,
        hasChanged: false
    }),
    computed: {
        instanceApiEndpoint() {
            return `/orders/${this.instanceId}/`;
        },
        isReady() {
            if (this.instance !== null) {
                return true
            } else {
                return false
            }
        },
        publidId() {
            if (this.isReady) {
                return this.instance.public_id
            }
            return ''
        }
    },
    created() {
        this.instanceId = this.$route.params.id;
        this.initialize();
    },
    methods: {
        initialize() {
            this.getInstance();
        },
        redirectToOrdersList() {
            let path = '/orders/';
            this.$router.push({path: path});
        },
        getInstance() {
            this.loading = true;
            api.get(this.instanceApiEndpoint).then(
                response => {
                    this.instance = response.data;
                    this.loading = false;
                },
                response => {

                }
            )
        },
        saveChanges() {
            this.updateInstance();
        },
        rollbackChanges() {

        },
        updateInstance() {
            this.loading = true;
            let data = this.$refs.main.instance;
            api.put(`/orders/${data.id}/`, data).then(
                response => {
                    this.instance = response.data;
                    this.$refs.main.copyInstance();
                    this.loading = false;
                    this.$notify({
                        title: `${this.instance.public_id}`,
                        message: `Заказ успешно сохранен`,
                        type: 'success'
                    });
                },
                response => {
                    this.loading = false;
                }
            )
        },
        handleMainChange(payload) {
            this.hasChanged = payload;
        },
        updateUser(user) {
            this.getInstance();
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .order-wrap {
        margin-top: 10px;
        padding: 0px 10px;
    }
    .topbar {
        display: flex;
        align-items: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .order-id {
        margin: 0px 15px;
        min-width: 145px;
    }
</style>
