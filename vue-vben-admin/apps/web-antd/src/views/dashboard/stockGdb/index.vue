<script lang="ts" setup>
import {onMounted, reactive, ref} from 'vue';

import type {VxeGridProps} from '#/adapter/vxe-table';

import {Button} from 'ant-design-vue';

import {useVbenVxeGrid} from '#/adapter/vxe-table';
import func from '../../../store/func';

const convertToChinese = func.convertToChinese;
const splitString = func.splitString;

interface RowType {
  category: string;
  color: string;
  id: string;
  price: string;
  productName: string;
  releaseDate: string;
}


/**
 * 获取示例表格数据
 */
async function getExampleTableApi() {

  try {
    const response = await fetch('/stockApi/stock/duanban', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // 设置请求体格式为 JSON
      },
      body: JSON.stringify({}),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    // const items = data.data.slice((page - 1) * pageSize, page * pageSize);
    gridApi.setGridOptions({data: data.data});
  } catch (error) {
    console.error('Fetching data failed:', error);
    throw error;
  }
}

const gridOptions: VxeGridProps<RowType> = {
  columns: [
    {title: '序号', type: 'seq', width: 50, fixed: 'left'},
    {field: 'code', title: '代码'},
    {field: 'name', title: '名称'},
    {field: 'details.chg', title: '今涨幅', slots: {default: 'jzd'}, sortable: true,},
    {field: 'zd', title: '涨幅', sortable: true, slots: {default: 'zd'}},
    {field: 'zxj', title: '现价', sortable: true, slots: {default: 'zxj'}},
    {field: 'zsz', title: '总市值', sortable: true, slots: {default: 'zsz'}},
    {field: 'fbjj', title: '封板基金', sortable: true, slots: {default: 'zxj'}},
    {field: 'fbt', title: '首板时间', slots: {default: 'fbt'}},
    {field: 'lbt', title: '最后封板时间', slots: {default: 'lbt'}},
    {field: 'zbcs', title: '炸板数', sortable: true},
    {field: 'zttj', title: '涨停统计', slots: {default: 'zttj'}},
    {field: 'lbs', title: '连扳数', sortable: true},
    {field: 'hy', title: '所属行业', fixed: 'right'},
  ],
  data: [],
  pagerConfig: {
    enabled: false,
  },
  sortConfig: {
    multiple: true,
  },
  height: 'auto',
  scrollY: {
    enabled: true,
    gt: 0,
  },
};
const [Grid, gridApi] = useVbenVxeGrid({
  gridOptions,
});

const ClassColor = (value = 0) => {
  if (value === 0) return 'text-red-500';
  return value > 0 ? 'text-red-500' : 'text-green-500';
};
const StyleColor = (value = 0, large = 0, color = 'red') => {
  if (value === 0) return '';
  return value >= large ? `text-${color}-500` : '';
};
onMounted(() => {
  getExampleTableApi();
});
</script>

<template>
  <div class="p-5 h-full">
    <Grid>
      <template #jzd="{ row }">
        <Tag>
             <span :class="ClassColor(row.details.chg)">
            {{ (parseFloat(row.details.chg)).toFixed(2) }}
          </span>
        </Tag>
      </template>
      <template #lbt="{ row }">
         <span>
           {{ splitString(row.lbt) }}
          </span>
      </template>
      <template #fbt="{ row }">
         <span>
           {{ splitString(row.fbt) }}
          </span>
      </template>
      <template #zttj="{ row }">
        <span :class="ClassColor()"> {{ row.zttj.ct }} </span>
        <span> / </span>
        <span :class="ClassColor()">{{ row.zttj.days }} </span>
      </template>
      <template #zd="{ row }">
         <span>
           {{  (parseFloat(row.zd)).toFixed(2) }}
          </span>
      </template>
      <template #fbjj="{ row }">
            <span>
            {{ convertToChinese(row.fbjj) }}
          </span>
      </template>
      <template #zsz="{ row }">
            <span>
            {{ convertToChinese(row.zsz) }}
          </span>
      </template>
      <template #zxj="{ row }">
            <span>
            {{ (row.zxj / 1000) }}
          </span>
      </template>
    </Grid>
  </div>
</template>
