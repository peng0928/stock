import {createRouter, createWebHistory} from 'vue-router';

const routes = [
    {
        path: '/hello',
        name: 'Home',
        component: () => import('../components/HelloWorld.vue')
    }
];

const router = createRouter({
    history: createWebHistory(''),
    routes
});
export default router;
