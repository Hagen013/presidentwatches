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
                    @change="handleSelectChange"
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
                    v-for="option in attribute.activeOptions"
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
        'values'
    ],
    computed: {
        filteredOptions() {
            console.log('triggered');
            let options = [];
            let activeValuesIdMapping = this.attribute.activeOptions.map((option) => option.id);
            options = this.options.slice();

            for (let i=0; i<this.options.length; i++) {
                if (activeValuesIdMapping.indexOf(this.options[i].id) !== -1 ) {
                    this.options[i].disabled = true;
                } else {
                    this.options[i].disabled = false;
                }
            }
            return options
        },
        activeOptions() {
            return this.attribute.activeOptions
        }
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            if (this.attribute.datatype === 5) {
                this.searchQuery = this.activeOptions[0].value
            }
        },
        removeActiveOption(option) {
            for (let i=0; i<this.attribute.activeOptions.length; i++) {
                let activeOption = this.attribute.activeOptions[i];
                if (activeOption.id === option.id) {
                    this.attribute.activeOptions.splice(i,1);
                    this.$forceUpdate();
                    break
                }
            }
            //this.$emit('remove-option', option);
        },
        handleSelectChange(label) {
            for (let i=0; i<this.options.length; i++) {
                let option = this.options[i];
                if (option.value === label) {
                    //this.$emit('add-option', option);
                    this.attribute.activeOptions.push(option);
                    this.searchQuery = '';
                    this.$forceUpdate();
                    break
                }
            }
        },
        handleOptionChange(label) {
            for (let i=0; i<this.options.length; i++) {
                let option = this.options[i];
                if (option.value === label) {
                    this.$emit('change-option', option);
                    break
                }
            }
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
