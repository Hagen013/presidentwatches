<template>
    <div class="app-container">
        <div class="filters">
            <el-input
                class="filters__search"
                placeholder="Поиск по модели"
                suffix-icon="el-icon-search"
            >
            </el-input>
        </div>
        <div class="gallery">
            <div v-for="item in items"
                class="item"
                :key="item.id"
            >
                <div class="item__img-wrap">
                    <img :src="formatImageUrl(item['image'])"
                        class="item__img"
                    >
                </div>
                <div class="item__info">
                    <div class="item__vendor">
                        {{formatItemName(item['name'])['vendor']}}
                    </div>
                    <div class="item__collection">
                        {{formatItemName(item['name'])['collection']}}
                    </div>
                    <div class="item__model">
                        {{formatItemName(item['name'])['model']}}
                    </div>
                    <div class="item__price">
                        {{item['_price']}} ₽
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

const service = axios.create({
  baseURL: "http://localhost:8000/api/v0",
  timeout: 5000,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  }
})

export default {
    name: 'Offers',
    data: () => ({
        items: []
    }),
    computed: {
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            service.get('/products/').then(
                response => {
                    console.log(response);
                    this.items = response.data['results'];
                },
                response => {
                    console.log(response);
                }
            )
        },
        formatImageUrl(url) {
            let formatedUrl = 'http://localhost:8000' + url;
            return formatedUrl
        },
        formatItemName(name) {
            let splitted = name.split(' ');
            console.log(splitted);
            return {
                'vendor': splitted[0],
                'collection': splitted[1],
                'model': splitted[2]
            }
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.gallery {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    padding: 32px;
}
.item {
    display: flex;
    justify-content: center;
    flex-direction: column;
    margin-bottom: 16px;
    background: white;
    width: 16%;
    box-shadow: 1px 2px 4px 1px rgba(0,0,0,0.15);
    border-radius: 4px;
}
.item__img-wrap {
    display: flex;
    justify-content: center;
    height: 231px;
    width: 100%;
}
.item__img {
    height: 100%;
    width: auto;
}
.item__info {
    padding: 16px 0px;
    text-align: center;
}
.item__vendor {
    width: 100%;
    height: 16px;
    font-size: 12px;
    font-weight: bold;
    font-style: normal;
    font-stretch: normal;
    line-height: 1.33;
    letter-spacing: 1px;
    text-align: center;
    color: #000000;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.item__collection {
    height: 16px;
    font-size: 14px;
    font-weight: normal;
    font-style: normal;
    font-stretch: normal;
    line-height: 1.14;
    letter-spacing: normal;
    text-align: center;
    color: #000000;
    text-align: center;
    margin-bottom: 3px;
}
.item__model {
    height: 14px;
    font-size: 12px;
    font-weight: normal;
    font-style: normal;
    font-stretch: normal;
    line-height: 1.17;
    letter-spacing: normal;
    text-align: center;
    color: #7f7f7f;
    margin-bottom: 9px;
}
.item__price {
    width: 100%;
    height: 24px;
    font-size: 18px;
    font-weight: normal;
    font-style: normal;
    font-stretch: normal;
    line-height: 1.33;
    letter-spacing: normal;
    text-align: center;
    color: #000000;
}
.filters {
    padding: 0px 32px;
}
.filters__search {
    max-width: 300px;
}
</style>
