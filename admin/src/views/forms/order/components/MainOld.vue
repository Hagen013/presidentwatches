<template>
    <div class="app-container order"
        v-if="isReady"
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
                                    v-model="instance.client_notes"
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
                                        <div class="total-price">
                                            {{saleAmount}} ₽
                                        </div>
                                    </div>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div class="field">
                                    <el-input
                                        v-model="instance.sale.promocode"
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
                                            @change="calculatePrices"
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
                                    <div class="total-price">
                                        {{totalPrice}} ₽
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
                                <div class="cart-item-left">
                                    <div class="cart-item-img-wrap">
                                        <img :src="item.image">
                                    </div>
                                </div>
                                <div class="cart-item-right">
                                    <div class="cart-item-topbar">
                                        <a  class="cart-item-link" :href="item.url" target="_blank">
                                            {{item.brand}} {{item.model}} {{item.series}}
                                        </a>
                                        <div class="tsoy">{{item.brand}} {{item.model}} {{item.series}}</div>
                                    </div>
                                    <div class="cart-item-content">

                                        <div class="field field-nonmargin">
                                            <div class="field-label">
                                                Цена за 1 шт.
                                            </div>
                                            <div class="field-value-box">
                                                <el-input-number
                                                    v-model="item.price"
                                                    :min="0"
                                                    size="small"
                                                    controls-position="right"
                                                    @change="calculatePrices"
                                                >
                                                </el-input-number>
                                            </div>
                                        </div>

                                        <div class="field field-nonmargin">
                                            <div class="field-label">
                                                Кол-во
                                            </div>
                                            <div class="field-value-box">
                                                <el-input-number
                                                    v-model="item.quantity"
                                                    :min="0"
                                                    size="small"
                                                    controls-position="right"
                                                    @change="calculatePrices"
                                                >
                                                </el-input-number>
                                            </div>
                                        </div>


                                        <div class="field field-nonmargin">
                                            <div class="field-label">
                                                Скидка
                                            </div>
                                            <div class="field-value-box">
                                                <el-input-number
                                                    v-model="item.sale"
                                                    :min="0"
                                                    size="small"
                                                    controls-position="right"
                                                    @change="calculatePrices"
                                                >
                                                </el-input-number>
                                            </div>
                                        </div>

                                        <div class="field field-nonmargin">
                                            <div class="field-label">
                                                Итого:
                                            </div>
                                            <div class="field-value-box">
                                                <div class="total-price">
                                                {{item.total_price}} ₽
                                                </div>
                                            </div>
                                        </div>

                                        <div class="field field-nonmargin">
                                            <el-button type="danger"
                                                @click="triggerDelete(item)"
                                            >
                                                Удалить
                                            </el-button>
                                        </div>

                                    </div>
                                </div>

                            </li>
                        </ul>
                        <div class="field">
                            <div class="field-value-box">
                                <el-autocomplete 
                                    v-model="queryLine"
                                    placeholder="Добавить товар"
                                    :fetch-suggestions="querySearch"
                                    valueKey="name"
                                    :trigger-on-focus="false"
                                    @select="handleProductSelect"
                                    class="product-autocomplete"
                                >
                                </el-autocomplete>
                            </div>
                        </div>
                    </div>
                    <div class="delimeter">
                    </div>
                    <div class="order-location">
                        <el-row :gutter="10">
                            <el-col :span="12">
                                <div class="field">
                                    <div class="field-label">
                                        Регион
                                    </div>
                                    <div class="field-value-box">
                                        <el-input
                                            placeholder="Выбрать"
                                            v-model="instance.location.city.name"
                                        >
                                        </el-input>
                                    </div>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div class="field">
                                    <div class="field-value-box">
                                        <el-input
                                            placeholder="Адрес"
                                            v-model="instance.customer.address"
                                        >
                                        </el-input>
                                    </div>
                                </div>
                            </el-col>
                        </el-row>
                    </div>
                    <div class="delimeter">
                    </div>
                    <div class="order-delivery">
                        <el-row :gutter="10">
                            <el-col :span="12">
                                <div class="field field_full">
                                    <div class="field-label">
                                        Доставка:
                                    </div>
                                    <div class="field-value-box">
                                        <el-select
                                            v-model="instance.delivery.type"
                                        >
                                            <el-option v-for="service in deliveryServices"
                                                :key="service.value"
                                                :value="service.value"
                                                :label="service.name"
                                            >
                                            </el-option>
                                        </el-select>
                                    </div>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div class="field field_full" v-if="instance.delivery.type=='pvz'">
                                    <div class="field-label">
                                        Сервис:
                                    </div>
                                    <div class="field-value-box">
                                        <el-select
                                            v-model="instance.delivery.pvz_service"
                                        >
                                            <el-option v-for="service in pvzServices"
                                                :key="service.value"
                                                :value="service.value"
                                                :label="service.name"
                                            >
                                            </el-option>
                                        </el-select>
                                    </div>
                                </div>
                            </el-col>
                        </el-row>
                        <div class="field">
                            <div class="field-label">
                                Пункт:
                            </div>
                            <div class="field-value-box">
                                <el-input
                                    placeholder="---"
                                    v-model="instance.delivery.pvz_code"
                                >
                                </el-input>
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
                                    v-model="curier"
                                >
                                    <el-option v-for="option in curierOptions"
                                        :key="option.value"
                                        :value="option.value"
                                        :label="option.name"
                                    >
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
                                    v-model="instance.payment.type"
                                >
                                    <el-option v-for="option in paymentOptions"
                                        :key="option.value"
                                        :value="option.value"
                                        :label="option.name"
                                    >
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
        curier: 'not_selected',
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
            {name: 'Пункт самовывоза', value: 'pvz'},
            {name: 'Самовывоз', value: 'pickup'},
            {name: 'Почтой России', value: 'rupost'}
        ],
        pvzServices: [
            {name: 'СДЭК', value: 'sdek'},
            {name: 'PickPoint', value: 'pickpoint'},
            {name: 'Не выбрано', value: ''}
        ],
        paymentOptions: [
            {name: 'Не выбрано', value: 'not_selected'},
            {name: 'Наличными', value: 'cash'},
            {name: 'Картой при получении', value: 'card_offline'},
            {name: 'Картой онлайн', value: 'card_online'}
        ],
        curierOptions: [
            {name: '---', value: 'not_selected'},
        ],
        queryLine: ""
    }),
    computed: {
        isReady() {
            if (this.instanceId !== null) {
                return !(Object.keys(this.instance).length === 0);
            }
            return true
        },
        itemsPrice() {
            return this.instance.cart.total_price;
        },
        deliveryPrice() {
            return this.instance.delivery['price']
        },
        saleAmount() {
            return this.instance.cart.total_sale
        },
        totalPrice: {
            get() {
                return this.instance.total_price;
            },
            set(value) {
                value = parseInt(value);
                this.instance.total_price = value;
            }
        }
    },
    created() {
        this.notificationMessage = `Заказ успешно сохранен`;
    },
    methods: {
        redirectToOrdersList() {
            let path = '/orders/';
            this.$router.push({path: path});
        },
        calculatePrices() {
            let totalPrice = 0;
            let totalSale = 0;

            for (let key in this.instance.cart.items) {
                let item = this.instance.cart.items[key];
                let quantity = item['quantity'];
                let price = item['price'];
                let sale = item['sale']
                item['total_price'] = (price * quantity) - sale

                totalSale += sale;
                totalPrice += item['total_price'];
            }
            this.$set(this.instance.cart, 'total_price', totalPrice)
            this.$set(this.instance.cart, 'total_sale', totalSale)

            this.instance.total_price = totalPrice + this.instance.delivery['price'];

        },
        postInitialize() {
            this.notificationTitle = `${this.instance.public_id}`;
        },
        setDeliveryDateToday() {

        },
        setDeliveryDateTommorrow() {
            
        },
        querySearch(query, cb) {
            let lines = [{name: ''}];
            api.get('/search/', {params: {line: query}}).then(
                response => {
                    lines = response.data;
                    lines.forEach(function(item) {
                        item.name = item._source.name
                    })
                    cb(lines)
                },
                response => {

                }
            )
        },
        handleProductSelect(item) {
            let now = Date.now();
            this.queryLine = '';
            api.get(`/products/${item._source.id}/`).then(
                response => {
                    let product = response.data;
                    if (this.instance.cart.items[product.id] == undefined) {
                        let item = {
                            brand: product.brand,
                            image: product.image,
                            model: product.model,
                            pk: product.id,
                            base_price: product._price,
                            price: product._price,
                            quantity: 1,
                            series: product.series,
                            slug: product.slug,
                            total_price: product._price,
                            added_at: now,
                            url: product.url,
                            is_sale: false,
                            sale: 0

                        }
                        this.$set(this.instance.cart.items, product.id, item);
                        this.calculatePrices();
                    } else {
                        this.$notify({
                            title: 'Ошибка',
                            message: 'Данный товар уже есть в составе заказа',
                            type: 'error'
                        });
                    }
                },
                response => {

                }
            )
        },
        triggerDelete(item) {
            this.$confirm(`Удалить ${item.model}?`, 'Подвтерждение', {
                confirmButtonText: 'Да',
                cancelButtonText: 'Отмена',
                type: 'warning'
            }).then(() => {
                this.deleteFromCart(item);
            }).catch(() => {

            })
        },
        deleteFromCart(item) {
            let identifier = String(item.pk);
            this.$delete(this.instance.cart.items, identifier);
            this.$forceUpdate();
            this.calculatePrices();
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
        position: relative;
        padding: 10px;
        display: flex;
        list-style: none;
    }
    .product-autocomplete {
        width: 100%;
    }
    .field_full {
        width: 100%;
        .el-select {
            width: 100%;
        }
    }









    .total-price {
        font-size: 24px;
    }


    .cart-item-left {
        height: 100%;
        max-width: 100px;
    }
    .cart-item-right {
        position: relative;
        top: 0px;
        left: 0px;
        width: 100%;
    }
    .cart-item-img-wrap {
        height: 100px;
        width: 100px;
        text-align: center;
        img {
            height: 100%;
            width: auto;
        }
    }
    .cart-item-link {
        display: block; 
        padding: 5px;
        text-decoration: underline;
        color: #4c4dc1;
    }
    .cart-item-content {
        width: 100%;
        max-height: 100px;
        margin-top: 10px;
        padding: 5px;
        border-top: 1px solid #dcdcdc;
        display: flex;
        flex-wrap: wrap;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        .field {
            width: 240px;
            margin: 0px;
        }
    }
    .tsoy {
        margin-top: 4px;
        padding-left: 6px;
        font-size: 13x;
    }
</style>
