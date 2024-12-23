<template>
  <div class="card-box w-full p-5">
    <div class="p-1 flex gap-2">
      <Button @click="sortByADesc(1)"> 降序</Button>
      <Button @click="sortByADesc()"> 升序</Button>
    </div>
    <div class="flex flex-wrap p-0">
      <div v-for="(item, index) in plateData" :key="index"
           class="text-md hover:shadow-xl  border-border group w-1/3 cursor-pointer border-b border-r border-t py-3">
        <div class="rounded-lg">
          <div class="pl-3 truncate flex gap-4 text-lg">
            <div class="text-blue-500">{{ item.name }}</div>
            <div class="" :class="textColor(item.zf)">{{ item.zf }}%</div>
          </div>
        </div>
        <div class="pt-5 pb-5">
          <div class="table-responsive">
            <div class="overflow-x-auto">
              <table class="table-auto w-full sm:flex-col md:table">
                <thead>
                <tr>
                  <th></th>
                  <th>主</th>
                  <th>超</th>
                  <th>大</th>
                  <th>中</th>
                  <th>小</th>
                </tr>
                </thead>
                <tbody>
                <tr class="text-center">
                  <td>净额</td>
                  <td>{{ item.zlje }}</td>
                  <td>{{ item.jrcddje }}</td>
                  <td>{{ item.jrddje }}</td>
                  <td>{{ item.jrzdje }}</td>
                  <td>{{ item.jrxdje }}</td>
                </tr>
                <tr class="text-center">
                  <td>占比</td>
                  <td>{{ item.zljzb }}</td>
                  <td>{{ item.jrcddjzb }}</td>
                  <td>{{ item.jrddjzb }}</td>
                  <td>{{ item.jrzdjzb }}</td>
                  <td>{{ item.jrxdjzb }}</td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import {Button, Card, message, notification, Space} from 'ant-design-vue';
import {onMounted, ref} from "vue";
import {EllipsisText} from '@vben/common-ui';

const plateData = ref([])
const textColor = (chg = 0) => {
  return chg < 0 ? 'text-green-500 hover:text-green-600' : 'text-red-500 hover:text-red-600';
};
const chgBgColor = (chg = 0) => {
  if (chg === 0) {
    return 'bg-blue-200 hover:bg-blue-300'
  }
  return chg < 0 ? 'bg-green-200 hover:bg-green-300' : ' bg-red-200 hover:bg-red-300';
};
const StockPlateData = async () => {
  try {
    const response = await fetch('/stockApi/stock/bk', {
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

function sortByADesc(e = 0) {
  if (e === 0) {
    plateData.value = plateData.value.sort((a, b) => a.zf - b.zf);
  } else {
    plateData.value = plateData.value.sort((a, b) => b.zf - a.zf);
  }
}

onMounted(() => {
  StockPlateData();
})
</script>
