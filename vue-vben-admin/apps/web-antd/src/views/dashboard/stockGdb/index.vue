<script lang="ts" setup>
import {onMounted, reactive, ref} from 'vue';
import XEUtils from 'xe-utils';
import type {VxeColumnPropTypes} from 'vxe-table';
import func from '../../../store/func';
import {VxeUI} from 'vxe-table';
import { preferencesManager } from '@vben/preferences';

VxeUI.setTheme(preferencesManager.state.theme.mode);

const loading = ref(true);
const columnConfig = {
  resizable: true
};
const convertToChinese = func.convertToChinese;
const splitString = func.splitString;

const tableData = reactive({
  data: [],
});

const StockGetduanban = async () => {
  try {
    const response = await fetch('/stockApi/stock/duanban', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // 设置请求体格式为 JSON
      },
      body: JSON.stringify({}),
    });
    // 解析响应数据
    const query = await response.json();
    loading.value = false;
    tableData.data = query.data;
  } catch (error) {
    console.log('There was an error!', error);
  }
};
const formatterNum: VxeColumnPropTypes.Formatter<RowVO> = ({cellValue}) => {
  return XEUtils.commafy(Number(cellValue), {digits: 2})
}

const ClassColor = (value = 0) => {
  if (value === 0) return 'text-red-500';
  return value > 0 ? 'text-red-500' : 'text-green-500';
};
const StyleColor = (value = 0, large = 0, color = 'red') => {
  if (value === 0) return '';
  return value >= large ? `text-${color}-500` : '';
};

onMounted(() => {
  StockGetduanban();
});

const sortNameMethod = ({row}) => {
  // 按名称长度进行排序
  return row.details.chg
}

</script>

<template>
  <div class="p-5">
    <div class="card-box w-full px-4 pb-5 pt-3">
      111
    </div>
    <div class="w-full pb-5 pt-3 mt-1">
      <vxe-table :data="tableData.data" :row-config="{isHover: true}" height="600"
                 :loading="loading" :column-config="columnConfig"
      >
        <vxe-column type="seq" width="auto" fixed="left"></vxe-column>
        <vxe-column field="code" title="代码" min-width="70"></vxe-column>
        <vxe-column field="name" title="名称" min-width="70">
          <template #default="{ row }">
            <span :class="ClassColor(row.details.chg)">
            {{ row.name }}
          </span>
          </template>
        </vxe-column>
        <vxe-column field="jzd" title="今涨幅" min-width="70" sortable :sort-by="sortNameMethod">
          <template #default="{ row }">
            <span :class="ClassColor(row.details.chg)">
            {{ (row.details.chg).toFixed(2) }}
          </span>
          </template>
        </vxe-column>
        <vxe-column field="zd" title="涨幅" min-width="70" :formatter="formatterNum"
                    sortable></vxe-column>
        <vxe-column field="zxj" title="现价" min-width="70" sortable></vxe-column>
        <vxe-column field="hs" title="换手" min-width="70" :formatter="formatterNum"
                    sortable></vxe-column>
        <vxe-column field="fbjj" title="封板基金" min-width="70" sortable>
          <template #default="{ row }">
            <span>
            {{ convertToChinese(row.fbjj) }}
          </span>
          </template>
        </vxe-column>
        <vxe-column field="fbt" title="首板时间" min-width="80">
          <template #default="{ row }">
          <span>
            {{ splitString(row.fbt) }}
          </span>
          </template>
        </vxe-column>
        <vxe-column field="lbt" title="最后封板时间" min-width="80">
          <template #default="{ row }">
         <span>
           {{ splitString(row.lbt) }}
          </span>
          </template>
        </vxe-column>
        <vxe-column field="zbcs" title="炸板数" min-width="70"></vxe-column>
        <vxe-column field="zttj" title="涨停统计" min-width="80">
          <template #default="{ row }">
            <span :class="ClassColor()"> {{ row.zttj.ct }} </span>
            <span> / </span>
            <span :class="ClassColor()">{{ row.zttj.days }} </span>
          </template>
        </vxe-column>
        <vxe-column field="lbs" title="连扳数" min-width="auto" sortable>
          <template #default="{ row }">
            <span :class="StyleColor((row.lbs).toFixed(2), 5)">
            {{ row.lbs }}
          </span>
          </template>
        </vxe-column>
        <vxe-column field="hy" title="所属行业" width="auto" fixed="right"></vxe-column>
      </vxe-table>
    </div>
  </div>
</template>

