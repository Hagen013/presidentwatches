<template>
    <div class="attribute-field">
        <div class="attribute-field__title">
            {{attribute.name}}
        </div>
        <div class="attribute-field__switch">
            <el-switch v-model="bindValueProxy"
                active-text="активное значение"
            >
            </el-switch>
        </div>
        <div class="attribute-field__input-box">
            <el-checkbox
                v-model="proxyValue"
                :disabled="!bindValue"
            >
                Есть
            </el-checkbox>
        </div>
    </div>
</template>

<script>


export default {
    name: 'BoolField',
    data: () => ({
        initialValue: null,
        bindValue: false
    }),
    props: [
        'attribute',
        'options',
        'active_options'
    ],
    created() {
        if (this.isDefined) {
            this.bindValue = true;
            this.initialValue = JSON.parse(JSON.stringify(this.activeOption));
        } else {
            this.initialValue = {id: null, attribute: this.attribute.id, value: true};
        }
    },
    computed: {
        isDefined() {
            return this.active_options.length>0
        },
        bindValueProxy: {
            get() {
                return this.bindValue
            },
            set(value) {
                console.log('switch triggered');
                if (value === true) {
                    this.updateValue();
                } else {
                    console.log('clear triggered');
                    this.$emit('clear', this.attribute);
                }
                this.bindValue = value;
            }
        },
        activeOption: {
            get() {
                if (this.isDefined) {
                    return this.active_options[0]
                }
                return {id: null, value: false}
            },
            set(value) {
                if (this.isDefined && (this.activeOption.value === value)) {
                
                } else {
                    let option = JSON.parse(JSON.stringify(this.initialValue));
                    option.id = null;
                    option.value = value;
                    this.$emit('change', option);
                }
            }
        },
        proxyValue: {
            get() {
                return this.activeOption.value
            },
            set(value) {
                if (this.bindValue) {
                    this.activeOption = value;
                }
            }
        }
    },
    methods: {
        updateValue() {
            let option = JSON.parse(JSON.stringify(this.initialValue));
            option.id = null;
            this.$emit('change', option);
        }
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
    .attribute-field__switch {
        margin: 16px 0px;
    }
</style>
