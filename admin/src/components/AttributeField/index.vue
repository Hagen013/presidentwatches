<template>
    <div class="attribute-field">
        <div class="attribute-field__title">
            {{attribute.name}}
        </div>
        <div class="attrobite-field__multichoice"
            v-if="attribute.datatype===6"
        >
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
                    :key="option.value"
                    closable
                    @close="removeActiveOption(option)"
                >
                    {{option.value}}
                </el-tag>
            </div>
        </div>
        <div class="attribute-field__choice"
            v-else-if="attribute.datatype===5"
        >
            <div class="attribute-field__input-box">
                <el-select v-model="searchQuery" filterable placeholder="Поиск"
                    @change="handleOptionChange"
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
            let filteredOptions = this.options.slice();
            let activeOptionsMapping = this.active_options.map(function(option) {
                return option.id
            })
            for (let i=0; i<filteredOptions.length; i++) {
                if (activeOptionsMapping.indexOf(filteredOptions[i].id) !== -1) {
                    filteredOptions[i].disabled = true;
                } else {
                    filteredOptions[i].disabled = false;
                }
            }
            return filteredOptions
        }
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            if (this.attribute.datatype === 5) {
            }
        },
        handleOptionChange(option) {

        },
        removeActiveOption(option) {

        },
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
    },
    watch: {
        attribute: {
            handler() {
                console.log('handler triggered');
            },
            deep: true
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
</style>
