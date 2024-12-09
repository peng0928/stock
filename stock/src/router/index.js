import {createRouter, createWebHistory} from 'vue-router';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../components/HomeIndex.vue'),
        meta: {
            title: '大盘'
        },
    },
    {
        path: '/stock',
        name: 'stock',
        component: () => import('../components/stockIndex.vue'),
        meta: {
            title: '个股'
        },
    },
    {
        path: '/plate',
        name: 'plate',
        component: () => import('../components/plateIndex.vue'),
        meta: {
            title: '板块'
        },
    }, {
        path: '/ztb',
        name: 'ztb',
        component: () => import('../components/stockZtb.vue'),
        meta: {
            title: '涨停板'
        },
    }
];

const router = createRouter({
    history: createWebHistory(''),
    routes
});
router.beforeEach((to, from, next) => {
    if (to.meta.title) {
        document.title = to.meta.title;
    }
    next();
});
export default router;
