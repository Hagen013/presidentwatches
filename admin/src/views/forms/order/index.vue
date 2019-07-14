<template>
    <div class="app-container order"
        v-if="initialized"
        v-loading="loading"
    >
        <div class="order-topbar">
            <el-row :gutter="20">
                <el-col :span="24">
                    <el-button type="primary"
                        @click="redirectToOrdersList"
                    >
                        <el-icon class="el-icon-back">
                        </el-icon>
                        К списку заказов
                    </el-button>
                    <el-button>
                        Чек
                    </el-button>
                    <div class="order-id">
                        Заказ № {{instance.public_id}}
                    </div>
                    <el-button type="warning"
                        :disabled="!hasChanged"
                        @click="saveChanges"
                    >
                        Сохранить
                    </el-button>
                    <el-button type="danger"
                        :disabled="!hasChanged"
                        @click="rollbackChanges"
                    >
                        Отменить изменения
                    </el-button>
                    <el-button type="primary"
                        :disabled="true"
                    >
                        Уведомить клиента
                    </el-button>
                </el-col>
                <el-col :span="0">
                </el-col>
            </el-row>
        </div>
        <div class="order-main">
            <el-row :gutter="20">
                <el-col :span="10">
                    <div class="order-status">
                        <div class="field">
                            <div class="field-label">
                                Статус:
                            </div>
                            <div class="field-value-box">
                                <el-select v-model="instance.state">
                                    <el-option v-for="option in statusOptions"
                                        :key="option.value"
                                        :label="option.name"
                                        :value="option.value"
                                    >
                                    </el-option>
                                </el-select>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Служебные заметки:
                            </div>
                            <div class="field-value-box">
                                <el-input type="textarea"
                                    :rows="3"
                                    v-model="instance.manager_notes"
                                >
                                </el-input>
                            </div>
                        </div>
                    </div>
                    <div class="delimeter">
                    </div>
                    <div class="order-customer">
                        <div class="field">
                            <div class="field-label">
                                ФИО:
                            </div>
                            <div class="field-value-box">
                                <el-input
                                    v-model="instance.customer.name"
                                >
                                </el-input>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Телефон:
                            </div>
                            <div class="field-value-box">
                                <el-input
                                    v-model="instance.customer.phone"
                                >
                                </el-input>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                E-mail:
                            </div>
                            <div class="field-value-box">
                                <el-input
                                    v-model="instance.customer.email"
                                >
                                </el-input>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Пожелания
                            </div>
                            <div class="field-value-box">
                                <el-input type="textarea"
                                    :rows="3"
                                >
                                </el-input>
                            </div>
                        </div>
                    </div>
                    <div class="delimeter">
                    </div>
                    <div class="order-total">
                        <el-row :gutter="10">
                            <el-col :span="12">
                                <div class="field">
                                    <div class="field-label">
                                        Скидка:
                                    </div>
                                    <div class="field-value-box">
                                        <el-input type="numeric">
                                        </el-input>
                                    </div>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div class="field">
                                    <el-input
                                        placeholder="Промокод"
                                    >
                                    </el-input>
                                </div>
                            </el-col>
                        </el-row>
                        <el-row :gutter="10">
                            <el-col :span="12">
                                <div class="field">
                                    <div class="field-label">
                                        Стоимость доставки:
                                    </div>
                                    <div class="field-value-box">
                                        <el-input-number
                                            v-model="instance.delivery.price"
                                            :min="0"
                                            size="medium"
                                            controls-position="right"
                                        >
                                        </el-input-number>
                                    </div>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div class="field field-c-1">
                                    <el-checkbox label="Подлежит уточнению">
                                    </el-checkbox>
                                </div>
                            </el-col>
                        </el-row>
                        <el-row :gutter="10">
                            <el-col :span="12">
                                <div class="field">
                                    <div class="field-label">
                                        К оплате
                                    </div>
                                    <div class="field-value-box">
                                        <el-input
                                        >
                                        </el-input>
                                    </div>
                                </div>
                            </el-col>
                        </el-row>
                    </div>
                </el-col>
                <el-col :span="14">
                    <div class="order-cart">
                        <ul class="order-cart-list">
                            <li class="cart-item" v-for="(item, key) of instance.cart.items"
                                :key="item.pk"
                            >
                                <div class="cart-item-img-wrap">
                                    <img :src="item.image">
                                </div>

                                <div class="cart-item-name">
                                    <a class="cart-item-link"
                                        :href="item.url"
                                        target="_blank"
                                    >
                                        <div class="cart-item-vendor">
                                            {{item.brand}}
                                        </div>
                                        <div class="cart-item-model">
                                            {{item.model}}
                                        </div>
                                        <div class="cart-item-series">
                                            {{item.series}}
                                        </div>
                                    </a>

                                </div>

                                <div class="cart-item-calculate">
                                    <div class="cart-item-price">
                                        <el-input-number
                                            v-model="item.price"
                                            controls-position="right"
                                            size="small"
                                            :min=0
                                            @change="calculatePrices"
                                        >
                                        </el-input-number>
                                    </div>

                                    <div class="cart-item-multi">
                                        <el-icon class="el-icon-close">
                                        </el-icon>
                                    </div>

                                    <div class="cart-item-quantity">
                                        <el-input-number
                                            v-model="item.quantity"
                                            controls-position="right"
                                            size="small"
                                            :min="1"
                                            @change="calculatePrices"
                                        >
                                        </el-input-number>
                                    </div>

                                    <div class="cart-item-equal">
                                        =
                                    </div>

                                    <div class="cart-item-total">
                                        {{item.total_price}} ₽
                                    </div>
                                </div>

                            </li>
                        </ul>
                        <div class="field">
                            <div class="field-value-box">
                                <el-autocomplete 
                                    placeholder="Добавить товар"
                                    :trigger-on-focus="false">
                                </el-autocomplete>
                            </div>
                        </div>
                    </div>
                    <div class="delimeter">
                    </div>
                    <div class="order-location">
                        <div class="field">
                            <div class="field-label">
                                Регион
                            </div>
                            <div class="field-value-box">
                                <el-autocomplete
                                    placeholder="Выбрать"
                                >
                                </el-autocomplete>
                            </div>
                        </div>
                    </div>
                    <div class="delimeter">
                    </div>
                    <div class="order-delivery">
                        <div class="field">
                            <div class="field-label">
                                Доставка:
                            </div>
                            <div class="field-value-box">
                                <el-select
                                >
                                    <el-option v-for="service in deliveryServices"
                                        :key="service.value"
                                        :value="service.value"
                                    >
                                        {{service.name}}
                                    </el-option>
                                </el-select>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Пункт:
                            </div>
                            <div class="field-value-box">
                                <el-autocomplete
                                    placeholder="---"
                                >
                                </el-autocomplete>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Дата доставки:
                            </div>
                            <div class="field-value-box field-value-box-c-1">
                                <el-input
                                    class="field-value-c-1"
                                    placeholder="ДД.ММ.ГГГГ"
                                >
                                </el-input>
                                <el-button type="primary">
                                    Сегодня
                                </el-button>
                                <el-button type="primary">
                                    Завтра
                                </el-button>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                № отправления
                            </div>
                            <div class="field-value-box field-value-box-c-1">
                                <el-input
                                    class="field-value-c-2"
                                >
                                </el-input>
                                <el-button>
                                    №
                                </el-button>
                                <el-button>
                                    Ф-7
                                </el-button>
                                <el-button>
                                    Ф-112ЭП
                                </el-button>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Курьер:
                            </div>
                            <div class="field-value-box">
                                <el-select
                                >
                                    <el-option v-for="option in curierOptions"
                                        :key="option.value"
                                        :value="option.value"
                                    >
                                        {{option.name}}
                                    </el-option>
                                </el-select>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Статус доставки:
                            </div>
                            <div class="field-value-label">
                                <el-input
                                >
                                </el-input>
                            </div>
                        </div>
                    </div>
                    <div class="delimeter">
                    </div>
                    <div class="order-payment">
                        <div class="field">
                            <div class="field-label">
                                Способ оплаты
                            </div>
                            <div class="field-value-box">
                                <el-select
                                >
                                    <el-option v-for="option in paymentOptions"
                                        :key="option.value"
                                        :value="option.value"
                                    >
                                        {{option.name}}
                                    </el-option>
                                </el-select>
                            </div>
                        </div>
                        <el-row :span="10">
                            <el-col :span="12">
                                <div class="field">
                                    <div class="field-label">
                                        Оплачено
                                    </div>
                                    <div class="field-value-box">
                                        <el-input-number
                                            controls-position="right"
                                        >
                                        </el-input-number>
                                    </div>
                                    <el-checkbox label="Выставить счёт">
                                    </el-checkbox>
                                </div>
                            </el-col>
                        </el-row>
                    </div>
                    <div class="order-last-orders">
                    </div>
                </el-col>
            </el-row>
        </div>
        <div class="order-bottom">
        </div>
    </div>
</template>

<script>
import api from '@/utils/request'
import crudMixin from '@/components/mixins/crudMixin'


export default {
    name: 'Order',
    components: {
    },
    mixins: [crudMixin],
    data: () => ({
        listApiUrl: '/orders/',
        statusOptions: [
            {name: 'Новый', value: 1},
            {name: 'Недозвон', value: 2},
            {name: 'Недозвон 2', value: 3},
            {name: 'Доставка', value: 4},
            {name: 'Согласован', value: 5},
            {name: 'Выполнен', value: 6},
            {name: 'Отменен', value: 7},
            {name: 'Отменен: недозвон', value: 8},
            {name: 'Вручен', value: 9},
            {name: 'Отказ', value: 10}
        ],
        deliveryServices: [
            {name: 'Не выбрано', value: 'not_selected'},
            {name: 'Курьером', value: 'curier'},
            {name: 'Пункт самовывоза', value: 'delivery_points'},
            {name: 'Почтой России', value: 'rupost'}
        ],
        paymentOptions: [
            {name: 'Не выбрано', value: 'not_selected'},
            {name: 'Наличными', value: 'cash'},
            {name: 'Картой при получении', value: 'card_on_receipt'},
            {name: 'Картой онлайн', value: 'card'}
        ],
        curierOptions: [
            {name: '---', value: 'not_selected'},
            {name: 'tsoy', value: 'matsoy'}
        ]
    }),
    computed: {
    },
    created() {
    },
    methods: {
        redirectToOrdersList() {
            let path = '/orders/';
            this.$router.push({path: path});
        },
        calculatePrices() {
            let total_price = 0;
            for (let key in this.instance.cart.items) {
                let item = this.instance.cart.items[key];
                let quantity = item['quantity'];
                let price = item['price'];
                item['total_price'] = price * quantity;
                totalPrice += item['total_price'];
            }
            this.instance.cart.total_price = total_price;
        },
        setDeliveryDateToday() {

        },
        setDeliveryDateTommorrow() {
            
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>

    .field {
        display: flex;
        width: 100%;
        align-items: center;
        padding: 5px;
        margin-bottom: 10px;
    }
    .field-label {
        width: 100px;
        min-width: 100px;
        max-width: 100px;
        padding-right: 20px;
        text-align: right;
        font-size: 13px;
    }
    .field-value-box {
        flex-grow: 1;
        width: 100%;
    }

    .delimeter {
        width: 100%;
        height: 1px;
        border-bottom: dotted 2px grey;
    }

    .order-id {
        display: inline-block;
        margin: 0px 30px;
    }
    .order-status {
        margin-bottom: 30px;
    }
    .order-total {
        padding-top: 10px;
    }
    .order-main {
        margin-top: 20px;
    }
    .order-location {
        padding-top: 10px;
        margin-bottom: 20px;
    }
    .order-delivery {
        padding-top: 10px;
        margin-bottom: 20px;
    }
    .order-customer {
        padding-top: 10px;
        margin-bottom: 20px;
    }
    .order-payment {
        padding-top: 10px;
    }
    .order-bottom {
        margin-bottom: 100px;
    }

    .field-c-1 {
        display: flex;
        align-items: center;
        min-height: 50px;
    }
    .field-value-box-c-1 {
        display: flex;
    }
    .field-value-c-1 {
        width: 110px;
        margin-right: 10px;
    }
    .field-value-c-2 {
        width: 300px;
        margin-right: 10px;
    }

    // cart-item
    .order-cart {
        margin-bottom: 20px;
    }
    .order-cart-list {
        border: 1px solid #dcdcdc;
        border-radius: 4px;
    }
    .cart-item {
        height: 122px;
        padding: 10px;
        display: flex;
        list-style: none;
    }
    .cart-item-name {
        display: flex;
        align-items: center;
        width: 200px;
        overflow: hidden;
        padding: 0px 10px;
    }
    .cart-item-img-wrap {
        height: 102px;
        width: 102px;
        text-align: center;
        img {
            height: 100%;
            width: auto;
        }
    }
    .cart-item-link {
        display: block;
        height: 54px;
        margin-bottom: 8px;
        text-decoration: underline;
        color: #4c4dc1;
    }
    .cart-item-price {

    }
    .cart-item-calculate {
        display: flex;
        height: 100%;
        padding: 0px 20px 0px 0px;
        flex-grow: 1;
        align-items: center;
        justify-content: space-between;
    }
</style>
