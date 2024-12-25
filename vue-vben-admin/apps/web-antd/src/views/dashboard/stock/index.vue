<template>
  <div class="card-box min-h-screen p-4 md:p-6">
    <!-- 搜索栏优化 -->
    <div class="mx-auto mb-8 max-w-2xl">
      <InputSearch
        v-model:value="stockName"
        placeholder="请输入股票代码"
        class="w-full shadow-sm transition-shadow duration-300 hover:shadow-md"
        @search="Stock"
      >
        <template #enterButton>
          <a-button type="primary">查询</a-button>
        </template>
      </InputSearch>
    </div>

    <!-- 主要内容区域 -->
    <div class="flex flex-col gap-6 lg:flex-row">
      <!-- 左侧板块信息 -->
      <div
        class="w-full rounded-xl p-4 shadow-md transition-shadow duration-300 hover:shadow-lg lg:w-1/6"
      >
        <div
          v-if="stockPlate"
          class="no-scrollbar max-h-dvh space-y-4 overflow-y-auto text-center"
        >
          <div v-for="(item, index) in stockPlate" :key="index">
            <div
              class="m-4 h-32 rounded-lg hover:shadow-xl"
              :class="chgBgColor(item.rate)"
            >
              <p class="pt-5 text-xs font-medium">{{ item.code }}</p>
              <p class="text-lg font-medium">{{ item.name }}</p>
              <p class="text-xs font-semibold" :class="chgColor(item.rate)">
                ¥
                {{ item.end }}
              </p>
              <p class="text-xl font-semibold" :class="chgColor(item.rate)">
                {{ item.rate }}%
              </p>
            </div>
          </div>
        </div>
        <div v-else class="animate-pulse">
          <Skeleton active :paragraph="{ rows: 10 }" />
        </div>
      </div>

      <!-- 右侧股票详情 -->
      <div class="flex w-full flex-col rounded-xl p-4 shadow-md lg:w-5/6">
        <!-- 股票基本信息 -->
        <div v-if="stock.name">
          <div
            class="mb-4 flex flex-wrap items-center gap-x-8 gap-y-2 border-b pb-3 shadow-sm transition-all duration-300"
          >
            <div class="flex items-center gap-3">
              <h2 class="text-xl font-bold">{{ stock.name }}</h2>
              <span class="text-sm">{{ stock.code }}</span>
            </div>
            <div class="flex items-center gap-4">
              <div class="flex items-center gap-2">
                <span class="text-sm">现价</span>
                <span
                  :class="[
                    'text-lg font-bold',
                    stock.zx > stock.zuos ? 'text-red-600' : 'text-green-600',
                  ]"
                >
                  {{ stock.zx }}
                </span>
              </div>
              <div
                :class="[
                  'flex items-center gap-1',
                  stock.zx > stock.zuos ? 'text-red-600' : 'text-green-600',
                ]"
              >
                <span class="text-lg font-medium">{{ stock.zd }}</span>
                <span class="text-lg font-medium">({{ stock.zf }}%)</span>
                <IconifyIcon
                  :icon="
                    stock.zx > stock.zuos
                      ? 'mdi:arrow-up-thick'
                      : 'mdi:arrow-down-thick'
                  "
                  class="h-5 w-5"
                />
              </div>
            </div>
            <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm">
              <div class="flex items-center gap-2">
                <span class="">今开</span>
                <span
                  :class="
                    stock.jk > stock.zuos ? 'text-red-600' : 'text-green-600'
                  "
                  >{{ stock.jk }}</span
                >
              </div>
              <div class="flex items-center gap-2">
                <span class="">最高</span>
                <span
                  :class="
                    stock.max > stock.zuos ? 'text-red-600' : 'text-green-600'
                  "
                  >{{ stock.max }}</span
                >
              </div>
              <div class="flex items-center gap-2">
                <span class="">最低</span>
                <span
                  :class="
                    stock.min > stock.zuos ? 'text-red-600' : 'text-green-600'
                  "
                  >{{ stock.min }}</span
                >
              </div>
              <div class="flex items-center gap-2">
                <span class="">昨收</span>
                <span class="">{{ stock.zuos }}</span>
              </div>
            </div>
          </div>

          <!-- 股票详细数据 -->
          <div class="grid grid-cols-3 gap-2 sm:grid-cols-4 lg:grid-cols-10">
            <div
              v-for="(item, index) in stockInfo"
              :key="index"
              class="flex items-center justify-between text-nowrap rounded-md px-4 text-xs"
            >
              <span class="">{{ item.n1 }}</span>
              <span :class="stockColor(item.c1)">{{ stock[item.k1] }}</span>
            </div>
          </div>

          <div class="flex w-full flex-col gap-2 lg:flex-row">
            <div class="lg:w-3/4">
              <AnalysisChartsTabs :tabs="chartTabs" class="mt-5">
                <template #fs>
                  <myEcharts :cid="stock.cid" type="fs" />
                </template>
                <template #kline>
                  <myEcharts :cid="stock.cid" type="kline" />
                </template>
              </AnalysisChartsTabs>
            </div>
            <div class="mt-5 lg:w-1/4">11</div>
          </div>
        </div>
        <div v-else class="w-full animate-pulse">
          <Skeleton active :paragraph="{ rows: 1 }" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted, onBeforeUnmount, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import { useInputStore } from '../../../store/stock';
import func from '../../../store/func';
import { InputSearch, Skeleton } from 'ant-design-vue';
import { IconifyIcon } from '@vben/icons';

import {
  AnalysisChartCard,
  AnalysisChartsTabs,
  AnalysisOverview,
} from '@vben/common-ui';
import myEcharts from './echarts.vue';

const chartTabs: [] = [
  {
    label: '分时',
    value: 'fs',
  },
  {
    label: '日K',
    value: 'kline',
  },
];

const inputStore = useInputStore();
const stockName = computed({
  get() {
    return inputStore.name;
  },
  set(value) {
    inputStore.updateInputValue(value);
  },
});
const stockPlate = ref(null);
const stock = ref({
  chg: 0,
});
const stockInfo = ref([
  { n1: '最新', k1: 'zx', c1: true },
  { n1: '均价', k1: 'jj', c1: true },
  { n1: '涨幅', k1: 'zf', c1: true },
  { n1: '涨跌', k1: 'zd', c1: true },
  { n1: '总手', k1: 'zs', c1: false },
  { n1: '金额', k1: 'je', c1: false },
  { n1: '换手', k1: 'hs', c1: 'y' },
  { n1: '量比', k1: 'lb', c1: 'r' },
  { n1: '最高', k1: 'max', c1: true },
  { n1: '最低', k1: 'min', c1: false },
  { n1: '今开', k1: 'jk', c1: true },
  { n1: '昨收', k1: 'zuos', c1: 'blue' },
  { n1: '涨停', k1: 'zt', c1: 'r' },
  { n1: '跌停', k1: 'dt', c1: 'g' },
  { n1: '外盘', k1: 'wp', c1: 'r' },
  { n1: '内盘', k1: 'np', c1: 'g' },
  { n1: '流通市值', k1: 'float_market', c1: true },
  { n1: '市值', k1: 'market', c1: true },
  { n1: '市盈', k1: 'P_E', c1: true },
  { n1: '市净', k1: 'market_net', c1: true },
]);
const SSE = ref({
  get: undefined,
  trend: undefined,
  trend_data: undefined,
});

const chgColor = (chg = 0, v = 0) => {
  const va = chg ? chg : stock.value.chg;
  return va < v ? 'text-green-500' : 'text-red-500';
};
const chgBgColor = (chg = 0) => {
  const va = chg ? chg : stock.value.chg;
  return va < 0
    ? 'bg-green-300 hover:bg-green-400'
    : ' bg-red-300 hover:bg-red-400';
};
const stockColor = (e, chg = 0, v = 0) => {
  if (e === false) {
    return '';
  }
  if (e === 'r') {
    return 'text-red-500';
  }
  if (e === 'g') {
    return 'text-green-500';
  }
  if (e === 'blue') {
    return 'text-blue-500';
  }
  if (e === 'y') {
    return 'text-purple-500';
  }
  const va = chg ? chg : stock.value.zx;
  v = v ? v : stock.value.zuos;
  return va < v ? 'text-green-500' : 'text-red-500';
};
const StockGet = async (e = true) => {
  try {
    const response = await fetch('/stockApi/stock/get', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // 设置请求体格式为 JSON
      },
      body: JSON.stringify({
        code: stockName.value,
      }),
    });
    // 解析响应数据
    const query = await response.json();
    stock.value = query;
    if (e) {
      StockTrend();
    }
  } catch (error) {
    console.log('There was an error!', error);
  }
};
const StockTrend = async () => {
  const hy = stock.value.hy;
  const dp = stock.value.dp;
  try {
    const response = await fetch('/stockApi/stock/trend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // 设置请求体格式为 JSON
      },
      body: JSON.stringify({
        hy: hy,
        dp: dp,
        code: stockName.value,
      }),
    });
    // 解析响应数据
    const query = await response.json();
    query.sort((a, b) => {
      // 比较a和b的a属性
      if (a.rate < b.rate) {
        return 1; // 如果a.a小于b.a，则a应该排在b前面
      }
      if (a.rate > b.rate) {
        return -1; // 如果a.a大于b.a，则a应该排在b后面
      }
      return 0; // 如果a.a等于b.a，则a和b的顺序不变
    });
    stockPlate.value = query;
  } catch (error) {
    console.log('There was an error!', error);
  }
};
const Stock = async () => {
  stock.value = {};
  StockGet();
  closeSSE();
  StockGetSSE();
};

const closeSSE = () => {
  Object.entries(SSE.value).forEach(([key, value]) => {
    console.log(`Key: ${key}, Value: ${value}`);
    if (value !== undefined) {
      console.log('SSE正在关闭 =>', key);
      value.close();
    }
  });
};
function StockGetSSE() {
  const sse = new EventSource('/stockApi/stock/get/' + stockName.value);
  sse.onmessage = (event) => {
    stock.value = JSON.parse(event.data);
  };
  // 监听连接打开事件
  sse.onopen = (event) => {
    console.log('SSE连接已打开', event);
  };

  // 监听错误事件
  sse.onerror = (event) => {
    console.error('SSE连接发生错误', event);
    sse.close(); // 尝试关闭连接
  };
  SSE.value.get = sse;
}
onMounted(() => {});
onUnmounted(() => {
  closeSSE();
});
</script>
