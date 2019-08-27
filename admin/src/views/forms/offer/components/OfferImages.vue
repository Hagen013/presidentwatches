<template>
    <div v-loading="loading">
        <el-row :gutter="20">
            <el-col :span="12">
                <h2 class="subtitle">
                    Главное изображение
                </h2>
                <el-upload
                    class="avatar-uploader"
                    :action="mainImageUploadUrl"
                    :multiple="false"
                    :show-file-list="false"
                    :auto-upload="false"
                    ref="mainUpload"
                    :on-change="handleMainImageFile"
                >
                    Заменить
                    <i class="el-icon-plus avatar-uploader-icon"></i>
                </el-upload>

                <div class="main-image">
                    <div class="main-image-controls">
                    </div>
                    <div class="main-image-wrap">
                        <img :src="mainImage">
                    </div>
                </div>
            </el-col>
            <el-col :span="12">
                <h2 class="subtitle">
                    Добавить новые
                </h2>
                <el-upload
                    action="#"
                    list-type="picture-card"
                    :auto-upload="false"
                    ref="newImages"
                    :on-change="handleUploadsChange"
                >
                    <i slot="default" class="el-icon-plus"></i>
                    <div slot="file" slot-scope="{file}">
                    <img
                        class="el-upload-list__item-thumbnail"
                        :src="file.url" alt=""
                    >
                    <span class="el-upload-list__item-actions">
                        <span
                        class="el-upload-list__item-preview"
                        @click="handlePictureCardPreview(file)"
                        >
                        <i class="el-icon-zoom-in"></i>
                        </span>
                        <span
                        v-if="!disabled"
                        class="el-upload-list__item-delete"
                        @click="handleRemove(file)"
                        >
                        <i class="el-icon-delete"></i>
                        </span>
                    </span>
                    </div>
                </el-upload>
                <h2 class="subtitle">
                    Дополнительные
                </h2>
                <div class="images-gallery">
                    <draggable v-model="images"
                        @change="reorderImages"
                    >
                        <transition-group type="transition" :name="!drag ? 'flip-list' : null">
                        <div class="image" v-for="image in images"
                            :key="image.id"
                        >
                            <span class="image-actions">
                                <span
                                    class="image-preview"
                                    @click="showImage(image)"
                                >
                                <i class="el-icon-zoom-in"></i>
                                </span>
                                <span
                                    class="image-delete"
                                    @click="handleImageRemove(image)"
                                >
                                <i class="el-icon-delete"></i>
                                </span>
                            </span>
                            <div class="image-wrap">
                                <img :src="image.thumbnail">
                            </div>
                        </div>
                        </transition-group>
                    </draggable>
                </div>
            </el-col>
        </el-row>
        <el-dialog :visible.sync="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="">
        </el-dialog>
    </div>
</template>

<script>
const equal = require('fast-deep-equal');
import draggable from 'vuedraggable'

import request from '@/utils/request'
import baseURL from '@/utils/baseUrl'


export default {
    name: 'OfferImages',
    data: () => ({
        mainImage: '',
        mainImageProxy: '',
        mainImageFile: null,
        images: [],
        imagesProxy: [],
        drag: false,
        hasChanged: false,
        mainImageUploadUrl: '',
        uploadFiles: [],
        uploadFilesProxy: [],
        ///
        dialogImageUrl: '',
        dialogVisible: false,
        disabled: false,
        ///
        mainImageResponseReceived: true,
        imagesResponseReceived: false,
        imagesUploadResponseReceived: false
    }),
    components: {
        'draggable': draggable
    },
    props: [
        'instance',
        'activeTab'
    ],
    computed: {
        loading() {
            return !(
                (this.mainImageResponseReceived) &&
                (this.imagesResponseReceived) &&
                (this.imagesUploadResponseReceived)
            )
        }
    },
    created() {
        if (this.activeTab === 'images') {
            this.initialize();
        }
    },
    methods: {
        initialize() {
            if (this.mainImage == '') {
                this.mainImage = this.instance.image;
                this.mainImageProxy = this.mainImage;
                this.mainImageResponseReceived = true;
                this.imagesUploadResponseReceived = true;
                this.uploadFilesProxy = this.uploadFiles.splice();
            }
            this.syncData();
        },
        syncData() {
            this.getImages();
        },
        getImages() {
            request.get(`/products/${this.instance.id}/images/`).then(
                response => {
                    this.handleSuccessfulGetResponse(response);
                },
                response => {
                    this.handleFailedGetResponse(response);
                }
            )
        },
        handleSuccessfulGetResponse(response) {
            this.images = response.data;
            this.imagesProxy = JSON.parse(JSON.stringify(this.images));
            this.imagesResponseReceived = true;
        },
        handleFailedGetResponse(response) {

        },
        checkStatus() {
            if ( (this.mainImage != this.mainImageProxy) || 
                 (!equal(this.images, this.imagesProxy)) || 
                 (!equal(this.uploadFiles, this.uploadFilesProxy))
                ) {
                this.hasChanged = true;
                this.$emit('change', this.hasChanged);
                console.log('hoy')
            }
        },
        handleMainImageFile(file, fileList) {
            this.mainImage = URL.createObjectURL(file.raw);
            this.mainImageFile = file;
            this.checkStatus();
        },
        handleRemove(file) {
            for (let i=0; i<this.$refs.newImages.uploadFiles.length; i++) {
                if (file.uid === this.$refs.newImages.uploadFiles[i].uid) {
                    this.$delete(this.$refs.newImages.uploadFiles, i);
                }
            }
        },
        handlePictureCardPreview(file) {
            this.dialogImageUrl = file.url;
            this.dialogVisible = true;
        },
        showImage(image) {
            this.dialogImageUrl = image.image;
            this.dialogVisible = true;
        },
        handleImageRemove(image) {
            for (let i=0; i<this.images.length; i++) {
                if (image.id === this.images[i].id) {
                    this.$delete(this.images, i);
                }
            }
        },
        handleUploadsChange() {
            this.uploadFiles = this.$refs.newImages.uploadFiles;
            this.checkStatus();
        },
        saveChanges() {
            if (this.mainImage != this.mainImageProxy) {
                this.updateMainImage();
            }
            if (!equal(this.images, this.imagesProxy)) {
                this.updateImages();
            }
            if (!equal(this.uploadFiles, this.uploadFilesProxy)) {
                this.uploadNewImages();
            }
        },
        updateMainImage() {
            let formData = new FormData();
            let options =   {headers: {'Content-Type': 'multipart/form-data'}};
            formData.append('image', this.mainImageFile.raw);

            this.mainImageResponseReceived = false;
            request.put(`/products/${this.instance.id}/image/`, formData, options).then(
                response => {
                    this.$notify({
                        title: 'Успешно',
                        message: 'Изображение обновлено',
                        type: 'success'
                    });
                    this.mainImageResponseReceived = true;
                    this.mainImageProxy = this.mainImage.splice();
                    this.checkStatus();
                },
                response => {

                }
            )
        },
        updateImages() {
            this.imagesResponseReceived = false;
            request.put(`/products/${this.instance.id}/images/`, this.images).then(
                response => {
                    this.$notify({
                        title: 'Успешно',
                        message: 'Изображения изменены',
                        type: 'success'
                    });
                    this.imagesProxy = JSON.parse(JSON.stringify(this.images));
                    this.imagesResponseReceived = true;
                    this.checkStatus();
                },
                response => {

                }
            )
        },
        uploadNewImages() {
            let options = {headers: {'Content-Type': 'multipart/form-data'}};
            let formData = new FormData();
            for (let i=0; i<this.uploadFiles.length; i++) {
                formData.append(`file[${i}]`, this.uploadFiles[i].raw);
            }

            this.imagesUploadResponseReceived = false;
            request.post(`/products/${this.instance.id}/images/upload/`, formData, options).then(
                response => {
                    this.$notify({
                        title: 'Успешно',
                        message: 'Изображения добавлены',
                        type: 'success'
                    });
                    this.uploadFilesProxy = JSON.parse(JSON.stringify(this.uploadFiles));
                    this.imagesUploadResponseReceived = true;
                    this.syncData();
                },
                response => {

                }
            )
        },
        reorderImages() {
            for (let i=0; i<this.images.length; i++) {
                this.images[i].order = i
            }
        },
        rollbackChanges() {
            this.syncData();
            this.hasChanged = false;
            this.$emit('change', this.hasChanged);
        }
    },
    watch: {
        activeTab() {
            if (this.activeTab == 'images') {
                this.initialize();
            }
        },
        images: {
            handler() {
                this.checkStatus();
            },
            deep: true
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .main-image-wrap {
        height: 400px;
        text-align: center;
        img {
            height: 100%;
            width: auto;
        }
    }
    .images-gallery {
        display: flex;
        flex-wrap: wrap;
    }
    .image {
        position: relative;
        display: inline-block;
        height: 146px;
        width: 146px;
        overflow: hidden;
        text-align: center;
        border: 1px solid #c0ccda;
        border-radius: 6px;
        margin-right: 8px;
        margin-bottom: 8px;
        transition: .3s;
        user-select: none;
        cursor: grab;
        &:hover {
            .image-actions {
                opacity: 1;
            }
        }
    }
    .image-wrap {
        display: flex;
        justify-content: center;
        height: 100%;
        width: 100%;
        overflow: hidden;
        img {
            height: 100%;
            width: auto;
        }
    }
    .image-preview {
        line-height: 1.8;
        cursor: pointer;
    }
    .image-delete {
        margin-left: 15px;
        line-height: 1.8;
        cursor: pointer;
    }
    .image-actions {
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        left: 0;
        top: 0;
        cursor: default;
        text-align: center;
        color: #fff;
        opacity: 0;
        font-size: 20px;
        background-color: rgba(0,0,0,.5);
        -webkit-transition: opacity .3s;
        transition: opacity .3s;
        will-change: opacity;
        z-index: 110;
        cursor: grab;
    }
</style>
