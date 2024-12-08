<template>
  <div class="grid grid-cols-5 gap-4 text-center pb-8">
    <div v-for="(item, index) in plateData" :key="index" class="text-sm ">
      <div class="rounded-lg h-28 flex text-nowrap" :class="chgBgColor(item.zf)">
        <div class="m-2 text-xs text-left w-1/3">
          <div>净额</div>
          <div>主: {{item.zlje}}</div>
          <div>超: {{item.jrcddje}}</div>
          <div>大: {{item.jrddje}}</div>
          <div>中: {{item.jrzdje}}</div>
          <div>小: {{item.jrxdje}}</div>
        </div>
        <div class="m-4 w-1/3">
          <div class="text-lg">{{ item.name }}</div>
          <div class="pt-3 text-lg" :class="textColor(item.zf)">涨幅: {{ item.zf }}</div>
        </div>
        <div class="m-2 text-xs w-1/3 text-right">
          <div>净占比</div>
          <div>{{item.zljzb}}</div>
          <div>{{item.jrcddjzb}}</div>
          <div>{{item.jrddjzb}}</div>
          <div>{{item.jrzdjzb}}</div>
          <div>{{item.jrxdjzb}}</div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>

import {ref} from "@vue/reactivity";
import {onMounted} from "vue";

const plateData = ref([])
const textColor = (chg = 0) => {
  return chg < 0 ? 'text-green-500 hover:text-green-600' : 'text-red-500 hover:text-red-600';
};
const chgBgColor = (chg = 0) => {
  return chg < 0 ? 'bg-green-200 hover:bg-green-300' : ' bg-red-200 hover:bg-red-300';
};
const StockPlateData = async () => {
  try {
    const response = await fetch('/api/stock/bk', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // 设置请求体格式为 JSON
      },
      body: JSON.stringify({}),
    });
    // 解析响应数据
    const query = await response.json();
    plateData.value = query;
  } catch (error) {
    console.log('There was an error!', error);
  }
};

onMounted(() => {
  StockPlateData();
})
</script>