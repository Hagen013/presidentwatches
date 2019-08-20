<template>
    <div class="filter"
        @click="toggleDropdown"
        v-on:click-outside="showDropdown=false"
    >
        {{attribute.name}}
        <i class="filter-icon el-icon-arrow-down">
        </i>
        <div class="filter-dropdown" v-if="showDropdown">
            tsoy
        </div>
    </div>
</template>

<script>
import request from '@/utils/request'


export default {
    name: 'Filter',
    data: () => ({
        showDropdown: false
    }),
    props: [
        'attribute'
    ],
    computed: {
    },
    created() {
    },
    methods: {
        toggleDropdown() {
            this.showDropdown = !this.showDropdown;
        }
    },
    filters: {
    },
    watch: {
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .filter {
        position: relative;
        display: inline-block;
        user-select: none;
        cursor: pointer;
        height: 36px;
        margin-bottom: 10px;
        line-height: 36px;
        padding: 0px 10px;
        transition: .3s;
        margin-left: -1px;
        border: 1px solid rgba(0,0,0,.12);
        &:hover {
            background: rgba(0,0,0,.12);
        }
        &:first-of-type {
            border-radius: 4px 0px 0px 4px;
        }
    }
    .filter-dropdown {
        top: 36px;
        left: 0px;
        width: 300px;
        padding: 10px;
        max-height: 200px;
        background: white;
        position: absolute;
        border-bottom: 1px solid rgba(0,0,0,.12);
        border-left: 1px solid rgba(0,0,0,.12);
        border-right: 1px solid rgba(0,0,0,.12);
        box-shadow: 0 9px 15px 0 rgba(0,0,0,0.15);
        z-index: 100;
    }
    .filter-icon {
        font-size: 12px;
        margin-left: 2px;
    }
</style>
