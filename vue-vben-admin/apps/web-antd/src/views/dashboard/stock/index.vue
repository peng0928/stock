<template>
  <div class="p-5">
    <div class="card-box w-full">
      <div class="container mx-auto mt-5 flex w-2/5 p-3">
        <InputSearch
          v-model:value="stockName"
          placeholder="代码"
          @search="Stock"
        >
          <template #enterButton>
            <a-button>查询</a-button>
          </template>
        </InputSearch>
      </div>
      <div class="mt-5 flex flex-col p-3 lg:flex-row">
        <div class="mr-4 w-full lg:w-1/6">
          <div
            v-if="stockPlate"
            class="no-scrollbar max-h-dvh overflow-y-auto pb-16 text-center"
          >
            <div v-for="(item, index) in stockPlate" :key="index">
              <div class="m-4 h-32 rounded-lg" :class="chgBgColor(item.rate)">
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
          <div v-else>
            <Skeleton active :paragraph="{ rows: 10 }" />
          </div>
        </div>
        <div class="mr-4 w-full lg:w-5/6">
          <div class="flex flex-col p-3 lg:flex-row">
            <div class="w-full lg:w-1/6">
              <div class="flex">
                <p class="text-lg font-medium">{{ stock.name }}</p>
              </div>
              <div
                class="flex text-nowrap text-lg font-light"
                :class="chgColor(stock.zx, stock.zuos)"
              >
                <div class="">
                  {{ stock.zd }}
                </div>
                <div class="pb-1">
                  <IconifyIcon
                    :icon="
                      stock.zx > stock.zuos
                        ? 'mdi:arrow-up-thick'
                        : 'mdi:arrow-down-thick'
                    "
                    width="20"
                    height="25"
                    class="text-2xl"
                  >
                  </IconifyIcon>
                </div>
              </div>
            </div>

            <div
              class="text-md flex w-full truncate text-center sm:text-sm md:text-base lg:w-5/6 lg:text-sm"
            >
              <div class="flex w-full flex-wrap">
                <div
                  v-for="(item, index) in stockInfo"
                  :key="index"
                  class="flex w-1/6"
                >
                  <div class="max-w-full truncate text-nowrap">
                    <div class="flex">
                      <div>{{ item.n1 }}:</div>
                      <div :class="stockColor(item.c1)" class="pl-1">
                        {{ stock[item.k1] }}
                      </div>
                    </div>
                    <div class="flex">
                      <div>{{ item.n2 }}:</div>
                      <div :class="stockColor(item.c2)" class="pl-1">
                        {{ stock[item.k2] }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
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
  { n1: '最新', k1: 'zx', n2: '均价', k2: 'jj', c1: true, c2: true },
  { n1: '涨幅', k1: 'zf', n2: '涨跌', k2: 'zd', c1: true, c2: true },
  { n1: '总手', k1: 'zs', n2: '金额', k2: 'je', c1: false, c2: false },
  { n1: '换手', k1: 'hs', n2: '量比', k2: 'lb', c1: 'y', c2: 'r' },
  { n1: '最高', k1: 'max', n2: '最低', k2: 'min', c1: true, c2: false },
  { n1: '今开', k1: 'jk', n2: '昨收', k2: 'zuos', c1: true, c2: 'blue' },
  { n1: '涨停', k1: 'zt', n2: '跌停', k2: 'dt', c1: 'r', c2: 'g' },
  { n1: '外盘', k1: 'wp', n2: '内盘', k2: 'np', c1: 'r', c2: 'g' },
  {
    n1: '流通市值',
    k1: 'float_market',
    n2: '市值',
    k2: 'market',
    c1: true,
    c2: true,
  },
  { n1: '市盈', k1: 'P_E', n2: '市净', k2: 'market_net', c1: true, c2: true },
]);
const chgColor = (chg = 0, v = 0) => {
  const va = chg ? chg : stock.value.chg;
  return va < v ? 'text-green-500' : 'text-red-500';
};
const chgBgColor = (chg = 0) => {
  const va = chg ? chg : stock.value.chg;
  return va < 0
    ? 'bg-green-100 hover:bg-green-200'
    : ' bg-red-100 hover:bg-red-200';
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
    const response = await fetch('/api/stock/trend', {
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
};
onMounted(() => {});
onUnmounted(() => {});
</script>
