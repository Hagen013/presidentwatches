<template>
    <div class="form-container">
        <div class="shop-controls">
            <el-row :gutter="10">
                <el-col :span="12">
                    <el-upload
                    class="upload-demo"
                    ref="upload"
                    action="https://jsonplaceholder.typicode.com/posts/"
                    :auto-upload="false">
                    <el-button slot="trigger" size="small" type="primary">select file</el-button>
                    <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">upload to server</el-button>
                    <div class="el-upload__tip" slot="tip">jpg/png files with a size less than 500kb</div>
                    </el-upload>
                </el-col>
                <el-col :span="12">
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Warehouse',
    data() {
      return {
        fileList: []
      };
    },
    computed: {
        uploadisActive() {
            return false
        }
    },
    methods: {
        submitUpload() {
            
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .shop-controls {
        padding: 20px;
    }
</style>
