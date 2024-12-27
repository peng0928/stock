<script lang="ts" setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue';

import type { VxeGridProps } from '#/adapter/vxe-table';

import { Button } from 'ant-design-vue';

import { useVbenVxeGrid } from '#/adapter/vxe-table';
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
    const response = await fetch('/stockApi/change', {});

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    // const items = data.data.slice((page - 1) * pageSize, page * pageSize);
    gridApi.setGridOptions({ data: data });
  } catch (error) {
    console.error('Fetching data failed:', error);
    throw error;
  }
}

const gridOptions: VxeGridProps<RowType> = {
  columns: [
    { title: '序号', type: 'seq', width: 50, fixed: 'left' },
    { field: 'tm', title: '时间', sortable: true },
    { field: 'code', title: '代码' },
    { field: 'name', title: '名称' },
    { field: 'price', title: '价格', sortable: true },
    { field: 'zf', title: '涨幅', sortable: true },
  ],
  data: [],
  pagerConfig: {
    enabled: false,
  },
  sortConfig: {
    multiple: true,
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

let interval = null;
onMounted(() => {
  getExampleTableApi();
  interval = setInterval(() => {
    getExampleTableApi();
  }, 5000);
});
onUnmounted(() => {
  clearInterval(interval);
});
</script>

<template>
  <div class="h-full p-5">
    <Grid> </Grid>
  </div>
</template>
