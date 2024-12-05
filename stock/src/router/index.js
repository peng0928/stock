import {createRouter, createWebHistory} from 'vue-router';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../components/HelloWorld.vue'),
        meta: {
            title: '大盘'
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
