<template>
  <div class="p-5">
    <div class="card-box w-full p-3">
      <div class="flex gap-2 p-1">
        <Button @click="sortByADesc(1)"> 降序</Button>
        <Button @click="sortByADesc()"> 升序</Button>
      </div>
      <div class="flex flex-wrap p-0">
        <div
          v-for="(item, index) in plateData"
          :key="index"
          class="text-md border-border group w-1/3 cursor-pointer border-b border-r border-t py-3 hover:shadow-xl"
        >
          <div class="rounded-lg">
            <div class="flex gap-4 truncate pl-3 text-lg">
              <div class="text-blue-500">{{ item.name }}</div>
              <div class="" :class="textColor(item.zf)">{{ item.zf }}%</div>
            </div>
          </div>
          <div class="pb-5 pt-5">
            <div class="table-responsive absolute hidden">
              <div class="overflow-x-auto">
                <table class="w-full table-auto sm:flex-col md:table">
                  <thead>
                    <tr>
                      <th>主</th>
                      <th>超</th>
                      <th>大</th>
                      <th>中</th>
                      <th>小</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="text-center">
                      <td :class="textColor(item.zljzb)">{{ item.zlje }}</td>
                      <td :class="textColor(item.jrcddj)">
                        {{ item.jrcddje }}
                      </td>
                      <td :class="textColor(item.jrdddj)">{{ item.jrddje }}</td>
                      <td :class="textColor(item.jrzdj)">{{ item.jrzdje }}</td>
                      <td :class="textColor(item.jrxddj)">{{ item.jrxdje }}</td>
                    </tr>
                    <tr class="text-center">
                      <td :class="textColor(item.zljzb)">{{ item.zljzb }}</td>
                      <td :class="textColor(item.jrcddjzb)">
                        {{ item.jrcddjzb }}
                      </td>
                      <td :class="textColor(item.jrdddjzb)">
                        {{ item.jrddjzb }}
                      </td>
                      <td :class="textColor(item.jrzdjzb)">
                        {{ item.jrzdjzb }}
                      </td>
                      <td :class="textColor(item.jrxddjzb)">
                        {{ item.jrxdjzb }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { Button, Card, message, notification, Space } from 'ant-design-vue';
import { onMounted, ref } from 'vue';
import { EllipsisText } from '@vben/common-ui';

const plateData = ref([]);
const textColor = (chg = 0) => {
  return chg < 0
    ? 'text-green-500 hover:text-green-600'
    : 'text-red-500 hover:text-red-600';
};
const chgBgColor = (chg = 0) => {
  if (chg === 0) {
    return 'bg-blue-200 hover:bg-blue-300';
  }
  return chg < 0
    ? 'bg-green-200 hover:bg-green-300'
    : ' bg-red-200 hover:bg-red-300';
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
    sortByADesc(1);
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
});
</script>
