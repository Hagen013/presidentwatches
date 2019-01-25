<template>
    <div class="app-container offer"
        v-if="initialized"
        v-loading="loading"
    >
        <div class="offer__controls">
            <el-button type="primary" icon="el-icon-check"
                :disabled="!hasChanged"
                :plain="!hasChanged"
            >
                Сохранить
            </el-button>
            <el-button type="warning"
                :disabled="!hasChanged"
                :plain="!hasChanged"
            >
                Отменить изменения
            </el-button>
            <el-button type="danger"
                v-if="instanceId!==null"
                icon="el-icon-delete"
                @click="triggerDelete"
            >
                Удалить
            </el-button>
        </div>
        <el-tabs v-model="activeTabName">
            <el-tab-pane label="Основное" name="main">
                <offer-main
                    :instance=instance
                >
                </offer-main>
            </el-tab-pane>
            <el-tab-pane label="Изображения" name="images">
                <offer-images
                >
                </offer-images>
            </el-tab-pane>
            <el-tab-pane label="SEO информация" name="seo">
                <offer-seo
                >
                </offer-seo>
            </el-tab-pane>
            <el-tab-pane label="Видеообзоры" name="videoreviews">
                <offer-videos
                >
                </offer-videos>
            </el-tab-pane>
            <el-tab-pane label="Описание" name="description">
                <offer-description
                >
                </offer-description>
            </el-tab-pane>
            <el-tab-pane label="Атрибуты" name="attributes">
                <offer-attributes
                    :instance="instance"
                    :activeTab="activeTabName"
                    ref="attributes"
                    @chageStatus="changeAttributesStatus"
                >
                </offer-attributes>
            </el-tab-pane>
        </el-tabs>
        <el-dialog
            title="Подтверждение действия"
            :visible.sync="showDeleteDialog"
            width="30%"
        >
            <span>Вы уверены, что хотите удалить товар {{instance.model}}?</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="cancelDelete">
                    Отмена
                </el-button>
                <el-button type="danger" @click="deleteInstance">
                    Удалить
                </el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import request from '@/utils/request'
const equal = require('fast-deep-equal');

import crudMixin from '@/components/mixins/crudMixin'


import offerMain from './components/OfferMain'
import offerImages from './components/OfferImages'
import offerSeo from './components/OfferSeo'
import offerVideos from './components/OfferVideos'
import offerDescription from './components/OfferDescription'
import offerAttributes from './components/OfferAttributes'


export default {
    name: 'Offer',
    mixins: [crudMixin],
    components: {
        'offer-main': offerMain,
        'offer-images': offerImages,
        'offer-seo': offerSeo,
        'offer-videos': offerVideos,
        'offer-description': offerDescription,
        'offer-attributes': offerAttributes
    },
    data: () => ({
        listApiUrl: '/products/',
        activeTabName: 'main',
        attributesHasChanged: false
    }),
    methods: {
        changeAttributesStatus(state) {
            this.attributesHasChanged = state;
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .offer__controls {
        padding-bottom: 32px;
    }
</style>
