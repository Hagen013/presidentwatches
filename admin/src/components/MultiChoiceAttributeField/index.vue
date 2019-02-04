<template>
    <div class="attribute-field">
        <div class="attribute-field__title">
            {{attribute.name}}
        </div>
        <div class="attribute-field__input-box">
            <el-select v-model="searchQuery" filterable placeholder="Поиск"
                @change="addActiveOption"
            >
                <el-option
                    v-for="option in filteredOptions"
                    :key="option.id"
                    :label="option.value"
                    :value="option.value"
                    :disabled="option.disabled"
                >
                </el-option>
            </el-select>
        </div>
        <div class="attribute-field__tags">
            <el-tag
                v-for="option in active_options"
                :key="option.id"
                closable
                @close="removeActiveOption(option)"
            >
                {{option.value}}
            </el-tag>
        </div>
    </div>
</template>

<script>


export default {
    name: 'AttributeField',
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
        filteredOptions() {
            let activeMapping = this.attribute.activeOptions.map(function(option) {
                return option.id
            })
            let options = this.options.filter(function(option) {
                return activeMapping.indexOf(option.id) === -1
            })
            if (options.length === 0) {
                options.push({
                    value: 'Нет доступных значений',
                    id: null,
                    disabled: true
                })
            }
            return options
        }
    },
    methods: {
        addActiveOption(label) {
            for (let i=0; i<this.options.length; i++) {
                let option = this.options[i];
                if (option.value === label) {
                    this.$emit('add-option', option);
                    this.searchQuery = '';
                    break
                }
            }
        },
        removeActiveOption(option) {
            this.$emit('remove-option', option);
            this.$forceUpdate();
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
</style>
