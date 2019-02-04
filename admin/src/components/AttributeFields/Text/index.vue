<template>
    <div class="attribute-field">
        <div class="attribute-field__title">
            {{attribute.name}}
        </div>
        <div class="attribute-field__input-box">
            <el-input
                v-model="proxyValue"
                placeholder="Не указано"
                type="textarea"
                :autosize="{ minRows: 1 }"
            >
            </el-input>
        </div>
    </div>
</template>

<script>


export default {
    name: 'TextField',
    data: () => ({
        initialValue: null
    }),
    props: [
        'attribute',
        'options',
        'active_options'
    ],
    mounted() {
        if (this.isDefined) {
            this.initialValue = JSON.parse(JSON.stringify(this.activeValue));
        } else {
            this.initialValue = {id: null, attribute: this.attribute.id};
        }
    },
    computed: {
        isDefined() {
            return this.active_options.length>0
        },
        activeValue() {
            if (this.isDefined) {
                return this.active_options[0] 
            }
            return {id: null, value: ''}
        },
        proxyValue: {
            get() {
                return this.activeValue.value
            },
            set(newValue) {
                let option = JSON.parse(JSON.stringify(this.initialValue));
                option.id = null;
                option.value = newValue;
                this.$emit('change', option)
            }
        }
    },
    methods: {
    }
}
</script>

<style scoped>
    .attribute-field {
        margin-bottom: 24px;
    }
    .attribute-field__title {
        margin-bottom: 8px;
    }
    .attribute-field__input-box {
        margin-bottom: 8px;
    }
    .el-tag {
        margin-right: 8px;
    }
    .el-select {
        width: 320px;
    }
</style>
