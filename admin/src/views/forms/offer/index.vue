<template>
    <div class="app-container offer"
        v-if="initialized"
        v-loading="loading"
    >
        <div class="offer__controls">
            <el-button icon="el-icon-back"
                @click="back"
            >
                Назад
            </el-button>
            <el-button type="primary" icon="el-icon-check"
                :disabled="!hasChangedOverall"
                :plain="!hasChangedOverall"
                @click="saveChangesOverall"
            >
                Сохранить
            </el-button>
            <el-button type="warning"
                :disabled="!hasChangedOverall"
                :plain="!hasChangedOverall"
                @click="rollbackChangesOverall"
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
        <h1 class="title">
            {{instance.brand}} {{instance.series}} {{instance.model}}
        </h1>
        <el-tabs v-model="activeTabName">
            <el-tab-pane label="Основное" name="main">
                <offer-main
                    :instance=instance
                >
                </offer-main>
            </el-tab-pane>
            <el-tab-pane label="Изображения" name="images">
                <offer-images
                    :instance="instance"
                    :activeTab="activeTabName"
                    @change="handleImagesChange"
                    ref="images"
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
                    @change="handleAttributesChange"
                >
                </offer-attributes>
            </el-tab-pane>
            <el-tab-pane label="Комментарии" name="comments">
                <offer-comments
                    :instance="instance"
                    :activeTab="activeTabName"
                    ref="comments"
                >
                </offer-comments>
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
import offerComments from './components/OfferComments'


export default {
    name: 'Offer',
    mixins: [crudMixin],
    components: {
        'offer-main': offerMain,
        'offer-images': offerImages,
        'offer-seo': offerSeo,
        'offer-videos': offerVideos,
        'offer-description': offerDescription,
        'offer-attributes': offerAttributes,
        'offer-comments': offerComments
    },
    data: () => ({
        listApiUrl: '/products/',
        activeTabName: 'main',
        attributesHasChanged: false,
        imagesHasChanged: false
    }),
    computed: {
        hasChangedOverall() {
            return (
                this.hasChanged ||
                this.attributesHasChanged ||
                this.imagesHasChanged
            )
        }
    },
    methods: {
        handleAttributesChange(state) {
            this.attributesHasChanged = state;
        },
        handleImagesChange(state) {
            this.imagesHasChanged = state;
        },
        saveChangesOverall() {
            if (this.hasChanged) {
                this.saveChanges();
            }
            if (this.attributesHasChanged) {
                this.$refs.attributes.saveChanges();
            }
            if (this.imagesHasChanged) {
                this.$refs.images.saveChanges();
            }
        },
        rollbackChangesOverall() {
            if (this.hasChanged) {
                this.rollbackChanges();
            }
            if (this.attributesHasChanged) {
                this.$refs.attributes.rollbackChanges();
            }
            if (this.imagesHasChanged) {
                this.$refs.images.rollbackChanges();
            }
        },
        back() {
            this.$router.go(-1)
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .offer__controls {
        padding-bottom: 16px;
    }
</style>
