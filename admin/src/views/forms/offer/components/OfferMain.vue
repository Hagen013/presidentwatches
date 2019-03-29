<template>
    <div class="tab-content offer-main">
        <el-row :gutter="64">
            <el-col :span="12">
                <div class="input-box">
                    <div class="input-box__label">
                        Модель:
                    </div>
                    <el-input v-model="instance.model">
                    </el-input>
                </div>
                <div class="input-box">
                    <div class="input-box__label">
                        Базовая цена:
                    </div>
                    <el-input-number v-model="instance._price"
                        controls-position="right"
                    >
                    </el-input-number>
                </div>
                <div class="input-box">
                    <div class="input-box__label">
                        Старая цена:
                    </div>
                    <el-input-number v-model="instance.old_price"
                        controls-position="right"
                    >
                    </el-input-number>
                </div>
                <div class="input-box">
                    <div class="input-box__label">
                        Вес (гр):
                    </div>
                    <el-input-number v-model="instance._weight"
                        controls-position="right"
                    >
                    </el-input-number>
                </div>
                <div class="input-box">
                    <div class="input-box__label">
                        Длина:
                    </div>
                    <el-input-number v-model="instance.height"
                        controls-position="right"
                    >
                    </el-input-number>
                </div>
                <div class="input-box">
                    <div class="input-box__label">
                        Ширина:
                    </div>
                    <el-input-number v-model="instance.width"
                        controls-position="right"
                    >
                    </el-input-number>
                </div>
                <div class="input-box">
                    <div class="input-box__label">
                        Толщина:
                    </div>
                    <el-input-number v-model="instance.thickness"
                        controls-position="right"
                    >
                    </el-input-number>
                </div>
                <div class="input-box input-box_nonflex">
                    <el-checkbox v-model="instance.is_in_stock">
                        В наличии
                    </el-checkbox>
                    <el-checkbox v-model="instance.is_bestseller">
                        Хит продаж
                    </el-checkbox>
                    <el-checkbox v-model="instance.is_new">
                        Новинка
                    </el-checkbox>
                    <el-checkbox v-model="instance.is_sale">
                        Действует скидка
                    </el-checkbox>
                    <el-checkbox v-model="instance.is_in_showcase">
                        Отображать в подборках
                    </el-checkbox>
                </div>
                <div class="input-box">
                    <div class="input-box__label">
                        Рейтинг:
                    </div>
                    <el-input-number v-model="instance.scoring"
                        controls-position="right"
                    >
                    </el-input-number>
                </div>
                <div class="input-box">
                    <el-checkbox v-model="instance.is_published">
                        Страница в публичном доступе
                    </el-checkbox>
                </div>
                <div class="input-box">
                    <el-checkbox v-model="instance.is_yml_offer">
                        Яндекс.Маркет
                    </el-checkbox>
                </div>
                <div class="input-box">
                    <el-checkbox v-model="instance.is_in_stock">
                        В наличии в Магазине на Тульской
                    </el-checkbox>
                </div>
                <div class="input-box">
                    <div class="input-box">
                        Количество в остатсках
                    </div>
                    <el-input-number v-model="instance.quantity"
                        controls-position="right"
                    >
                    </el-input-number>
                </div>
            </el-col>
            <el-col :span="12">
                <div class="img-wrap">
                    <img
                        :src="instance.thumbnail"
                    >
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>


export default {
    name: 'OfferMain',
    data: () => ({
    }),
    props: [
        'instance'
    ],
    computed: {
    },
    created() {
    },
    methods: {
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .tab-content  {
        padding-top: 32px;
    }
    .input-box {
        display: flex;
        margin-bottom: 16px;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        label {
            margin-left: 0px;
            margin-right: 24px;
        }
    }
    .input-box_nonflex {
        display: block;
    }
    .input-box_vertical {
        flex-direction: column;
        .input-box__label {
            margin-right: 0px;
            margin-bottom: 8px;
        }
    }
    .input-box__label {
        margin-right: 16px;
    }
    .flex-start {
        justify-content: flex-start;
    }
</style>
