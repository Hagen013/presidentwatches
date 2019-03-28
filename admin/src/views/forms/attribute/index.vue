<template>
    <div class="app-container"
        v-loading="!initialized"
    >
        <div class="attribute-form">
            <h1 class="title">{{formTitle}}</h1>
            <div class="attribute-form__content">
                <el-tabs type="border-card">
                    <el-tab-pane label="Главное">
                        <el-row class="attribute-form__main">
                            <el-col :span="12">
                                <div class="grid-content">
                                    <div class="form__row">
                                        <div class="input-box">
                                            <span class="input-label">Название:</span>
                                            <el-input
                                                v-model="instance.name"
                                            >
                                            </el-input>
                                        </div>
                                    </div>
                                    <div class="form__row">
                                        <div class="input-box">
                                            <span class="input-label">Slug:</span>
                                            <el-input
                                                v-model="instance.slug"
                                            >
                                            </el-input>
                                        </div>
                                    </div>
                                    <div class="form__row">
                                        <div class="input-box">
                                            <span class="input-label">Тип атрибута:</span>
                                            <el-select v-model="instance.datatype">
                                                <el-option
                                                    v-for="option in datatypeOptions"
                                                    :key="option.value"
                                                    :label="option.label"
                                                    :value="option.value"
                                                >
                                                </el-option>
                                            </el-select>
                                        </div>
                                    </div>
                                    <div class="form__row">
                                        <div class="input-box">
                                            <span class="input-label">Порядок атрибута:</span>
                                             <el-input-number v-model="instance.order"
                                                controls-position="right"
                                                :min="0"
                                            >
                                            </el-input-number>
                                        </div>
                                    </div>
                                    <div class="form__row">
                                        <div class="input-box">
                                            <span class="input-label">Дата создания:</span>
                                            <el-input
                                                v-model="creationDate"
                                                :disabled="true"
                                            >
                                            </el-input>
                                        </div>
                                    </div>
                                    <div class="form__row">
                                        <div class="input-box">
                                            <span class="input-label">Дата последнего редактирование:</span>
                                            <el-input
                                                v-model="modificationDate"
                                                :disabled="true"
                                            >
                                            </el-input>
                                        </div>
                                    </div>
                                    <div class="input-box">
                                        <span class="input-label">Описание</span>
                                        <el-input
                                            type="textarea"
                                            :autosize="{ minRows: 4, maxRows: 16}"
                                        >
                                        </el-input>
                                    </div>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div class="grid-content col-2">
                                    <div class="form__row">
                                        <el-checkbox>Не отображать на странице товара</el-checkbox>
                                    </div>
                                    <div class="form__row">
                                        <el-checkbox>Фильтр</el-checkbox>
                                    </div>
                                    <div class="form__row">
                                        <el-checkbox>Не создавать автоматически новые опции</el-checkbox>
                                    </div>
                                </div>
                            </el-col>
                        </el-row>
                    </el-tab-pane>
                    <el-tab-pane label="Значения">
                        <values-list :attribute="instance">
                        </values-list>
                    </el-tab-pane>
                    <el-tab-pane label="Группы">
                    </el-tab-pane>
                </el-tabs>
            </div>
        </div>
    </div>
</template>

<script>
import request from '@/utils/request'
import formatTime from '@/utils/formatTime'

import valuesList from './components/ValuesList.vue'


export default {
    name: 'Attribute',
    components: {
        'values-list': valuesList
    },
    data: () => ({
        listApiUrl: '/eav/attributes/',
        initialized: false,
        instanceId: null,
        datatypeOptions: [
            {value: 1, label: 'Текстовый'},
            {value: 2, label: 'Целочисленный'},
            {value: 3, label: 'С плавающей запятой'},
            {value: 4, label: 'Булевый (да/нет)'},
            {value: 5, label: 'Choice'},
            {value: 6, label: 'MultiChoice'}
        ],
        instance: {
        }
    }),
    computed: {
        formTitle() {
            if (this.instanceID !== null) {
                if (this.initialized) {
                    return `Атрибут: ${this.instance.name}`
                }
                return 'Атрибут'
            }
            return 'Создать новый атрибут'
        },
        creationDate() {
            return formatTime(this.instance.created_at)
        },
        modificationDate() {
            return formatTime(this.instance.modified_at)
        }
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            let instanceID = this.$route.params.id;
            if (instanceID !== undefined) {
                this.instanceId = instanceID;
                this.getInstance();
            } else {
                this.initialized = true;
            }
        },
        getInstance() {
            let url = `${this.listApiUrl}${this.instanceId}/`;
            request.get(url).then(
                response => {
                    this.handleSuccessfulGetInstanceResponse(response);
                },
                response => {
                    this.handleFailedGetInstanceResponse(response);
                }
            )
        },
        handleSuccessfulGetInstanceResponse(response) {
            this.instance = response.data;
            this.initialized = true;
        },
        handleFailedGetInstanceResponse(response) {
            this.initialized = true;
        },
        handleSuccessfulUpdateInstanceResponse(response) {
        },
        handleFailedUpdateInstanceResponse(response) {
        },
        handleSuccessfulCreateInstanceResponse(response) {
        },
        handleFailedCreateInstanceResponse(response) {
        },
        handleSuccessfulDeleteInstanceResponse(response) {
        },
        handleFailedDeleteInstanceResponse(response) {
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .input-box {
        display: flex;
        align-items: center;
    }
    .input-label {
        margin-right: 16px;
    }
    .form__row {
        margin-bottom: 16px;
    }
    .col-2 {
        padding: 0px 0px 0px 16px;
    }
    .attribute-form__main {
        padding: 32px 0px 16px 0px;
    }
</style>
