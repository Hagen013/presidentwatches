<template>
    <div class="app-container">
        <div class="placeholder"
            v-if="!responseReceived"
            v-loading="!responseReceived"
        >
        </div>
        <div class="filters">
            <el-row :gutter="20">
                <el-col :span="8">
                    <div class="grid-content">
                        <div class="filters__header"
                            @click="displayFilters = !displayFilters"
                        >
                            <div class="filters__title">
                                Фильтры
                            </div>
                            <i class="filters__arrow el-icon-arrow-down"
                                :class="{ 'is-active': displayFilters }"
                            >
                            </i>
                        </div>
                    </div>
                </el-col>
                <el-col :span="8">
                    <div class="grid-content">
                    </div>
                </el-col>
                <el-col :span="8">
                    <div class="grid-content">
                    </div>
                </el-col>
            </el-row>
            <el-collapse-transition>
                <div class="filters__content"
                    v-if="displayFilters"
                >
                    <div class="filters__item">
                        <el-input
                            class="filters__search"
                            placeholder="Поиск по модели"
                            suffix-icon="el-icon-search"
                            v-model="filterParams.model"
                        >
                        </el-input>
                    </div>
                    <div class="filters__item">
                        <div class="filters__item-label">
                            Наличие:
                        </div>
                        <el-select v-model="filterParams.availability.value">
                            <el-option
                                v-for="option in filterParams.availability.options"
                                :key="option.label"
                                :value="option.value"
                                :label="option.label"
                            >
                            </el-option>
                        </el-select>
                    </div>
                </div>
            </el-collapse-transition>
        </div>
        <div class="gallery__wrap"
        >
            <div class="gallery__controls">
                <div class="gallery__switches">
                    <el-switch
                        v-model="galleryMode"
                        active-text="Галлерея"
                        inactive-text="Таблица"
                    >
                    </el-switch>
                </div>
                <div class="pagination">
                    <div class="pagination__pagezise-label">
                        Отображать по:
                    </div>
                    <el-select v-model="pageSize" placeholder="Select"
                        @change="handlePageSizeChange"
                    >
                        <el-option
                            v-for="item in pageSizeOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        >
                        </el-option>
                    </el-select>
                    <div class="pagination__info">
                        <div class="pagination__current-count">
                            {{offset}} - {{currentCount}}
                        </div>
                        <span class="pagination__delimeter">из</span>
                        <div class="pagination__total-count">
                            {{totalCount}}
                        </div>
                        <div class="pagination__buttons">
                            <div class="pagination__button pagination__button_prev"
                                :class="{ 'pagination__button_disabled': !hasPreviousPage }"
                                :disabled="!hasPreviousPage"
                                @click="previousPage"
                            >
                                <i class="el-icon-arrow-left"></i>
                            </div>
                            <div class="pagination__button pagination__button_next"
                                :class="{ 'pagination__button_disabled': !hasNextPage }"
                                :disabled="!hasNextPage"
                                @click="nextPage"
                            >
                                <i class="el-icon-arrow-right"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <table class="table"
                v-if="!galleryMode"
            >
                <tr class="table__header">
                    <th class="table__head text_left">
                        Модель
                    </th>
                    <th class="table__head text_left">
                        Базовая цена
                    </th>
                    <th class="table__head text_left">
                        URL
                    </th>
                    <th class="table__head text_left">
                        В наличии
                    </th>
                </tr>
                <tr class="table__row"
                    v-for="item in items"
                    :key="item.id"
                    @click="handleRedirect(item)"
                >
                    <td class="table__cell">
                        {{item.model}}
                    </td>
                    <td class="table__cell">
                        {{item._price}} ₽
                    </td>
                    <td class="table__cell table__cell_url">
                        <a :href="item.absolute_url"
                            class="table__link"
                            target="_blank"
                        >
                            {{item.absolute_url}}
                        </a>
                    </td>
                    <td class="table__cell table__cell_icon">
                        {{item.is_in_stock|availAbilityFilter}}
                        <i class="el-icon-check table__icon"
                            v-if="item.is_in_stock===true"
                        >
                        </i>
                        <i class="el-icon-close table__icon"
                            v-else
                        >
                        </i>
                    </td>
                </tr>
            </table>
            <div class="gallery"
                v-if="galleryMode"
            >
                <div class="gallery-card"
                    v-for="item in items"
                    :key="item.id"
                >
                    <div class="gallery-card__img-wrap">
                        <img class="gallery-card__img"
                            :src="item.thumbnail"
                        >
                    </div>
                    <div class="gallery-card__info">
                        <div class="gallery-card__model">
                            {{item.model}}
                        </div>
                        <div class="gallery-card__price">
                            {{item._price}} ₽
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import request from '@/utils/request'


export default {
    name: 'Offers',
    data: () => ({
        apiUrl: '/products/',
        items: [],
        pageSize: 100,
        offset: 0,
        limit: 100,
        totalCount: 0,
        galleryMode: false,
        displayFilters: false,
        pageSizeOptions: [
            {label: '50', value: 50},
            {label: '100', value: 100},
            {label: '200', value: 200}
        ],
        filterParams: {
            model: '',
            availability: {
                value: null,
                options: [
                    {value: null, label: 'Не выбрано'},
                    {value: true, label: 'Есть'},
                    {value: false, label: 'Нет'}
                ]
            }
        },
        responseReceived: false
    }),
    computed: {
        queryParams() {
            return {
                offset: this.offset,
                limit: this.limit,
            }
        },
        currentCount() {
            return (this.offset + this.limit)
        },
        hasPreviousPage() {
            return this.offset > 0
        },
        hasNextPage() {
            return this.currentCount < this.totalCount;
        }
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            this.getList();
        },
        getList() {
            this.responseReceived = false;
            request.get(this.apiUrl, {params: this.queryParams}).then(
                response => {
                    this.handleSuccessfulGetListResponse(response);
                },
                response => {
                    this.handleFailedGetListResponse(response);
                }
            )
        },
        previousPage() {
            this.offset -= this.pageSize;
        },
        nextPage() {
            this.offset += this.pageSize;
        },
        handleRedirect(instance) {
            let path = `/shop/offers/${instance.id}`
            this.$router.push({path: path});
        },
        handlePageSizeChange() {
            this.offset = 0;
            this.limit = this.pageSize;
        },
        handleSuccessfulGetListResponse(response) {
            this.items = response.data['results'];
            this.totalCount = response.data['count'];
            this.responseReceived = true;
        },
        handleFailedGetListResponse(response) {
            this.responseReceived = true;
        },
        formatImageUrl(url) {
            let formatedUrl = 'http://localhost:8000' + url;
            return formatedUrl
        },
        formatItemName(name) {
            let splitted = name.split(' ');
            return {
                'vendor': splitted[0],
                'collection': splitted[1],
                'model': splitted[2]
            }
        }
    },
    filters: {
        availAbilityFilter(value) {
            if (value === 'true') {
                return 'Есть'
            }
            return 'Нет'
        }
    },
    watch: {
        queryParams: {
            handler: function() {
                this.getList();
            },
            deep: true
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.gallery {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    padding: 32px;
}
.item {
    display: flex;
    justify-content: center;
    flex-direction: column;
    margin-bottom: 16px;
    background: white;
    width: 16%;
    box-shadow: 1px 2px 4px 1px rgba(0,0,0,0.15);
    border-radius: 4px;
}
.item__img-wrap {
    display: flex;
    justify-content: center;
    height: 231px;
    width: 100%;
}
.item__img {
    height: 100%;
    width: auto;
}
.item__info {
    padding: 16px 0px;
    text-align: center;
}
.item__vendor {
    width: 100%;
    height: 16px;
    font-size: 12px;
    font-weight: bold;
    font-style: normal;
    font-stretch: normal;
    line-height: 1.33;
    letter-spacing: 1px;
    text-align: center;
    color: #000000;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.item__collection {
    height: 16px;
    font-size: 14px;
    font-weight: normal;
    font-style: normal;
    font-stretch: normal;
    line-height: 1.14;
    letter-spacing: normal;
    text-align: center;
    color: #000000;
    text-align: center;
    margin-bottom: 3px;
}
.item__model {
    height: 14px;
    font-size: 12px;
    font-weight: normal;
    font-style: normal;
    font-stretch: normal;
    line-height: 1.17;
    letter-spacing: normal;
    text-align: center;
    color: #7f7f7f;
    margin-bottom: 9px;
}
.item__price {
    width: 100%;
    height: 24px;
    font-size: 18px;
    font-weight: normal;
    font-style: normal;
    font-stretch: normal;
    line-height: 1.33;
    letter-spacing: normal;
    text-align: center;
    color: #000000;
}
.filters {
    padding: 0px 0px;
    padding-bottom: 32px;
    user-select: none;
}
.filters__search {
    max-width: 300px;
}
.filters__content {
}
.gallery__controls {
    padding-bottom: 16px;
    margin-bottom: 24px;
    border-bottom: 1px solid rgba(0,0,0,.12);
}
.table__link {
    color: blue;
}
.table__cell_icon {
    display: flex;
    align-items: center;
}
.table__icon {
    margin-left: 8px;
    margin-top: 2px;
}
.pagination {
    display: flex;
}
.gallery__switches {
    display: flex;
    justify-content: flex-end;
    padding-right: 32px;
}
.pagination {
    display: flex;
    align-items: center;
}
.pagination__delimeter {
    margin-right: 8px;
    margin-left: 8px;
}
.pagination__pagezise-label {
    margin-right: 24px;
}
.gallery__controls {
    display: flex;
    justify-content: space-between;
}
.pagination__info {
    display: flex;
    align-items: center;
    margin-left: 24px;
}
.gallery__switches {
    display: flex;
    align-items: center;
}
.pagination__buttons {
    display: flex;
    align-items: center;
    margin-left: 32px;
}
.pagination__button {
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    height: 30px;
    width: 30px;
    border-radius: 15px;
}
.pagination__button_disabled {
    cursor: default;
    color: rgba(0,0,0,.32);
}
.pagination__button_next {
    margin-left: 8px;
}
.pagination__button_prev {

}
.placeholder {
    position: fixed;
    top: 0px;
    left: 0px;
    height: 100vh;
    width: 100%;
    z-index: 10000;
}
.filters__item {
    margin-right: 24px;
}
.filters__content {
    display: flex;
}
.filters__item {
    display: flex;
    align-items: center;
}
.filters__item-label {
    margin-right: 8px;
}
.gallery-card {
    position: relative;
    overflow: hidden;
    width: 254px;
    margin-bottom: 16px;
    border-radius: 4px;
}
.gallery-card__info {
    padding: 16px;
}
.gallery-card__img-wrap {
    display: block;
    height: 282px;
    width: 100%;
    text-align: center;
}
.gallery-card__img {
    height: 100%;
    width: auto;
}
.gallery-card__model {
    font-size: 12px;
    color: #7f7f7f;
    margin-bottom: 9px;
}
.gallery {
    flex-wrap: wrap;
    flex-direction: row;
    display: flex;
    justify-content: space-between;
}
</style>
