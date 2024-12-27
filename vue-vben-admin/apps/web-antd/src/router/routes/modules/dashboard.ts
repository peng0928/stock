import type {RouteRecordRaw} from 'vue-router';

import {BasicLayout} from '#/layouts';
import {$t} from '#/locales';

const routes: RouteRecordRaw[] = [
  {
    component: BasicLayout,
    meta: {
      icon: 'lucide:layout-dashboard',
      order: -1,
      title: $t('page.dashboard.title'),
    },
    name: 'Dashboard',
    path: '/',
    children: [
      {
        name: 'Analytics',
        path: '/analytics',
        component: () => import('#/views/dashboard/analytics/index.vue'),
        meta: {
          affixTab: true,
          icon: 'lucide:area-chart',
          title: $t('page.dashboard.analytics'),
        },
      },
      {
        name: 'Workspace',
        path: '/workspace',
        component: () => import('#/views/dashboard/workspace/index.vue'),
        meta: {
          icon: 'carbon:workspace',
          title: $t('page.dashboard.workspace'),
        },
      },
      {
        name: '大盘',
        path: '/dp',
        component: () => import('#/views/dashboard/stockDp/index.vue'),
        meta: {
          icon: 'fxemoji:stockchart',
          title: '大盘',
        },
      },
      {
        name: '断板',
        path: '/duanban',
        component: () => import('#/views/dashboard/stockGdb/index.vue'),
        meta: {
          icon: 'lucide-lab:stairs-arrow-down-left',
          title: '断板',
        },
      },
      {
        name: '板块',
        path: '/bankuan',
        component: () => import('#/views/dashboard/bankuan/index.vue'),
        meta: {
          icon: 'proicons:component',
          title: '板块',
        },
      },{
        name: '个股',
        path: '/stock',
        component: () => import('#/views/dashboard/stock/index.vue'),
        meta: {
          icon: 'bytesize:lightning',
          title: '个股',
        },
      },
      {
        name: '异动',
        path: '/change',
        component: () => import('#/views/dashboard/stockChange/index.vue'),
        meta: {
          icon: 'lucide:trending-up',
          title: '异动',
        },
      },
    ],
  },
];

export default routes;
