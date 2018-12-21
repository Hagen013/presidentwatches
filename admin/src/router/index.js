import Vue from 'vue'
import Router from 'vue-router'

// in development-env not use lazy-loading, because lazy-loading too many pages will cause webpack hot update too slow. so only in production use lazy-loading;
// detail: https://panjiachen.github.io/vue-element-admin-site/#/lazy-loading

Vue.use(Router)

/* Layout */
import Layout from '../views/layout/Layout'

/**
* hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
* alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
*                                if not set alwaysShow, only more than one route under the children
*                                it will becomes nested mode, otherwise not show the root menu
* redirect: noredirect           if `redirect:noredirect` will no redirect in the breadcrumb
* name:'router-name'             the name is used by <keep-alive> (must set!!!)
* meta : {
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
  }
**/
export const constantRouterMap = [
  { path: '/login', component: () => import('@/views/login/index'), hidden: true },
  { path: '/404', component: () => import('@/views/404'), hidden: true },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    name: 'Dashboard',
    children: [{
      path: 'dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: 'Главная', icon: 'home' }
    }]
  },

  {
    path: '/orders',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Orders',
        component: () => import('@/views/orders/index'),
        meta: { title: 'Заказы', icon: 'shopping-cart' }
      }
    ]
  },

  {
    path: '/shop',
    component: Layout,
    redirect: '/shop/offers',
    name: 'Каталог',
    meta: { title: 'Каталог', icon: 'dashboard' },
    children: [
      {
        path: 'offers',
        name: 'Offers',
        component: () => import('@/views/shop/offers/index'),
        meta: { title: 'Товары' }
      },
      {
        path: 'categories',
        name: 'Categories',
        component: () => import('@/views/shop/categories/index'),
        meta: { title: 'Категории' }
      },
      {
        path: 'products',
        name: 'Products',
        component: () => import('@/views/shop/products/index'),
        meta: { title: 'Модели' }
      },
      {
        path: 'warehouse',
        name: 'Warehouse',
        component: () => import('@/views/shop/warehouse/index'),
        meta: { title: 'Остатки' }
      },
      {
        path: 'categories/create',
        name: 'Category',
        hidden: true,
        component: () => import('@/views/forms/category'),
        meta: { title: 'Создать категорию' }
      },
      {
        path: 'categories/:id',
        name: 'Category',
        hidden: true,
        component: () => import('@/views/forms/category'),
        meta: { title: 'Редактирование категории' }
      },
    ]
  },

  {
    path: '/images',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Images',
        component: () => import('@/views/images/index'),
        meta: { title: 'Изображения', icon: 'insert_photo' }
      }
    ]
  },

  {
    path: '/users',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Users',
        component: () => import('@/views/users/index'),
        meta: { title: 'Пользователи', icon: 'user' }
      }
    ]
  },

  { path: '*', redirect: '/404', hidden: true }
]

export default new Router({
  // mode: 'history', //后端支持可开
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})
