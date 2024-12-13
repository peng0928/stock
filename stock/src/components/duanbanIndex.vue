<template>
  <div class="">
    <a-table :columns="columns" :data-source="data" :scroll="{ y: 600 }" :pagination="false" :showSorterTooltip="false"
             @change="onChange">
      <template #headerCell="{ column }">
        <template v-if="column.key === ''">
        <span>
          <smile-outlined/>
          Name
        </span>
        </template>
      </template>

      <template #bodyCell="{ column, record }">

        <template v-if="column.key === 'name'">
          <a-tooltip placement="bottom" color="white" class="pr-5">
            <template #title>
              <div class="container text-right">
                <div class="text-black flex justify-between w-32">
                  <div>总市值:</div>
                  <div>{{ (convertToChinese(record.zsz)) }}</div>
                </div>
                <div class="text-black flex justify-between w-32">
                  <div>成交额:</div>
                  <div>{{ (convertToChinese(record.cje)) }}</div>
                </div>
                <div class="text-black flex justify-between w-32">
                  <div>流通市值:</div>
                  <div>{{ (convertToChinese(record.ltsz)) }}</div>
                </div>
              </div>
            </template>
            <div>{{ record.name }}</div>
          </a-tooltip>
        </template>
        <template v-if="column.key === 'zd'">
          <span :class="ClassColor()">
            {{ (record.zd).toFixed(2) }}%
          </span>
        </template>
        <template v-if="column.key === 'jzd'">
          <span :class="ClassColor(record.details.chg)">
            {{ (record.details.chg).toFixed(2) }}%
          </span>
        </template>

        <template v-if="column.key === 'zxj'">
          <span :class="ClassColor()">
            {{ (parseFloat(record.zxj) / 1000).toFixed(2) }}
          </span>
        </template>
        <template v-if="column.key === 'cje'">
          <span>
            {{ (convertToChinese(record.cje)) }}
          </span>
        </template>
        <template v-if="column.key === 'ltsz'">
          <span>
            {{ (convertToChinese(record.ltsz)) }}
          </span>
        </template>
        <template v-if="column.key === 'zsz'">
          <span>
            {{ (convertToChinese(record.zsz)) }}
          </span>
        </template>
        <template v-if="column.key === 'fbjj'">
          <span>
            {{ (convertToChinese(record.fbjj)) }}
          </span>
        </template>
        <template v-if="column.key === 'hs'">
          <span :class="StyleColor((record.hs).toFixed(2), 10)">
            {{ (record.hs).toFixed(2) }}%
          </span>
        </template>
        <template v-if="column.key === 'zbcs'">
          <span :class="StyleColor((record.zbcs).toFixed(2), 3)">
            {{ record.zbcs }}
          </span>
        </template>
        <template v-if="column.key === 'lbs'">
          <span :class="StyleColor((record.lbs).toFixed(2), 5)">
            {{ record.lbs }}
          </span>
        </template>
        <template v-if="column.key === 'fbt'">
          <span>
            {{ splitString(record.fbt) }}
          </span>
        </template>
        <template v-if="column.key === 'lbt'">
          <span>
            {{ splitString(record.lbt) }}
          </span>
        </template>
        <template v-if="column.key === 'zttj'">
          <span :class="ClassColor()"> {{ record.zttj.ct }}  </span>
          <span> / </span>
          <span :class="ClassColor()">{{ record.zttj.days }} </span>
        </template>
      </template>
    </a-table>
  </div>
</template>
<script setup>
import {ref, computed, onMounted, onBeforeUnmount, onUnmounted} from 'vue'
import func from '../stores/func';

const convertToChinese = func.convertToChinese;
const splitString = func.splitString;

const columns = [
  {
    title: '序号',
    dataIndex: 'inx',
    key: 'inx',
    width: 80,
    sorter: (a, b) => a.inx - b.inx,
  },
  {
    title: '代码',
    key: 'code',
    dataIndex: 'code',
  },
  {
    title: '名称',
    key: 'name',
    dataIndex: 'name',

  }
  ,
  {
    title: '今涨跌幅',
    key: 'jzd',
    dataIndex: 'jzd',
    sorter: (a, b) => a.details.chg - b.details.chg,

  },
  {
    title: '涨跌幅',
    key: 'zd',
    dataIndex: 'zd',
    sorter: (a, b) => a.zd - b.zd,

  },
  {
    title: '最新价',
    key: 'zxj',
    dataIndex: 'zxj',
    sorter: (a, b) => a.zxj - b.zxj,

  },
  // {
  //   title: '成交额',
  //   key: 'cje',
  //   dataIndex: 'cje',
  //   sorter: (a, b) => a.cje - b.cje,
  // },
  // {
  //   title: '流通市值',
  //   key: 'ltsz',
  //   dataIndex: 'ltsz',
  //   sorter: (a, b) => a.ltsz - b.ltsz,
  // },
  // {
  //   title: '总市值',
  //   key: 'zsz',
  //   dataIndex: 'zsz',
  //   sorter: (a, b) => a.zsz - b.zsz,
  //
  // },
  {
    title: '换手率',
    key: 'hs',
    dataIndex: 'hs',
    sorter: (a, b) => a.hs - b.hs,
  },
  {
    title: '封板基金',
    key: 'fbjj',
    dataIndex: 'fbjj',
    sorter: (a, b) => a.fbjj - b.fbjj,
  },
  {
    title: '首板时间',
    key: 'fbt',
    dataIndex: 'fbt',

  },
  {
    title: '最后封板时间',
    key: 'lbt',
    dataIndex: 'lbt',

  },
  {
    title: '炸板次数',
    key: 'zbcs',
    dataIndex: 'zbcs',
    sorter: (a, b) => a.zbcs - b.zbcs,
  },
  {
    title: '涨停统计',
    key: 'zttj',
    dataIndex: 'zttj',

  },
  {
    title: '连扳数',
    key: 'lbs',
    dataIndex: 'lbs',
    sorter: (a, b) => a.lbs - b.lbs,
    filters: [
      {
        text: '1',
        value: '1',
      },
      {
        text: '2',
        value: '2',
      },
    ],
    filterMode: 'tree',
    filterSearch: true,
    onFilter: (value, record) => String(record.lbs).includes(value),
  },
  {
    title: '所属行业',
    key: 'hy',
    dataIndex: 'hy',

  }
];
const data = ref([])

const StockGetduanban = async () => {
  try {
    const response = await fetch('/api/stock/duanban', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // 设置请求体格式为 JSON
      },
      body: JSON.stringify({}),
    });
    // 解析响应数据
    const query = await response.json();
    data.value = query;
  } catch (error) {
    console.log('There was an error!', error);
  }
};

const ClassColor = (value = 0) => {
  if (value === 0) return 'text-red-500';
  return value > 0 ? 'text-red-500' : 'text-green-500';
};
const StyleColor = (value = 0, large = 0, color = 'red') => {
  if (value === 0) return '';
  return value >= large ? `text-${color}-500` : '';
};
const onChange = (pagination, filters, sorter, extra) => {
  console.log('params', extra.currentDataSource);
  const arr = extra.currentDataSource;
  const newList = arr.map((item, index) => {
    return {...item, inx: index + 1}; // 使用扩展运算符将索引添加到每个对象上
  });
  data.value = newList;
}

onMounted(() => {
  StockGetduanban();
})
</script>