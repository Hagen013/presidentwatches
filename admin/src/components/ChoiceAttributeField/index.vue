<template>
    <div class="attribute-field">
        <div class="attribute-field__title">
            {{attribute.name}}
        </div>
        <div class="attribute-field__input-box">
            <el-select v-model="searchQuery" filterable
                @change="handleChange"
            >
                <el-option
                    v-for="option in options"
                    :key="option.id"
                    :label="option.value"
                    :value="option.value"
                >
                </el-option>
            </el-select>
        </div>
    </div>
</template>

<script>


export default {
    name: 'Choice',
    data: () => ({
        searchQuery: '',
        showDropdown: false
    }),
    props: [
        'attribute',
        'options',
        'active_options'
    ],
    computed: {
        proxyOptions() {
            let options = JSON.parse(JSON.stringify(this.options));
            options.push({
                value: 'Не выбрано',
                id: null,
                disabled: false
            })
            return options
        }
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            if (this.active_options.length===0) {
                this.searchQuery = 'Не выбрано';
            } else {
                this.searchQuery = this.active_options[0].value;
            }
        },
        handleChange(label) {
            for (let i=0; i<this.options.length; i++) {
                let option = this.options[i];
                if (option.value === label) {
                    this.$emit('change', option);
                    break
                }
            }
        },
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
