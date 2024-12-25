<script lang="ts" setup>
import { onMounted, ref, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import {
  EchartsUI,
  type EchartsUIType,
  useEcharts,
} from '@vben/plugins/echarts';

const chartRef = ref<EchartsUIType>();
const { renderEcharts } = useEcharts(chartRef);

interface BasicOption {
  code: string;
}

interface Props {
  cid: BasicOption[];
  type: string;
}
const SSE = ref({
  kline: undefined,
});
defineOptions({
  name: 'AnalysisChartsTabs',
});

const props = withDefaults(defineProps<Props>(), {
  cid: () => [],
  type: () => '',
});
console.log('props.zsType', props.cid, props.type);
const upColor = 'red';
const downColor = 'green';
const option = ref();

function splitData(rawData) {
  let categoryData = [];
  let values = [];
  let volumes = [];
  for (let i = 0; i < rawData.length; i++) {
    categoryData.push(rawData[i].splice(0, 1)[0]);
    values.push(rawData[i]);
    volumes.push([i, rawData[i][4], rawData[i][0] > rawData[i][1] ? 1 : -1]);
  }
  return {
    categoryData: categoryData,
    values: values,
    volumes: volumes,
  };
}

function calculateMA(dayCount, data) {
  var result = [];
  for (var i = 0, len = data.values.length; i < len; i++) {
    if (i < dayCount) {
      result.push('-');
      continue;
    }
    var sum = 0;
    for (var j = 0; j < dayCount; j++) {
      const dataNum = parseFloat(data.values[i - j][1]);
      sum += dataNum;
    }
    result.push(+(sum / dayCount).toFixed(3));
  }
  return result;
}

const rawData = ref([]);

const SseFs = async () => {
  const sse = new EventSource('/stockApi/sse/data/fs');
  sse.onmessage = (event) => {
    const data = JSON.parse(event.data);
    rawData.value = data;
    FinitChart();
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
  SSE.value.kline = sse;
};

const SseTask = async () => {
  try {
    const response = await fetch('/stockApi/sse/kline/' + props.cid, {
      method: 'GET',
    });
  } catch (error) {
    console.log('There was an error!', error);
  }
};

function formatterTooltip(params: any) {
  let TooltipStr = '';
  const valueMap = {
    日k: 2,
    MA5: 1,
    MA10: 1,
    MA20: 1,
    MA30: 1,
    成交量: 1,
  };
  const title = params[0].name;
  for (let i = 0; i < params.length; i++) {
    const p = params[i];
    const seriesName = p.seriesName;
    let value = p.data[valueMap[seriesName]] || p.data || '';

    if (value && value !== '-') {
      try {
        value = parseFloat(value).toLocaleString();
      } catch (e) {
        value = '';
      }
      TooltipStr =
        TooltipStr +
        `
        <tr>
        <td>${p.marker}${p.seriesName}</td>
        <td class="text-base pl-8">${value}</td>
        </tr>`;
    }
  }
  return `<table class="tooltip-tab">
        <tr>
        <td  class="text-lg">
        ${title}
        </td>
        <tr>

        ${TooltipStr}
        </table>`;
}

const initxData = (klineData) => {
  const xData = [];
  for (let i = 0; i < klineData.length; i++) {
    xData[i] = klineData[i].datetime;
  }
  return xData;
};
const fsplitData = (jsonData) => {
  const hourData = [];
  const jdata = [];
  for (let i = 0; i < jsonData.length; i++) {
    hourData.push([
      i,
      jsonData[i].price,
      jsonData[i].increase,
      jsonData[i].cjl,
      jsonData[i].ratio,
      jsonData[i].amount,
      jsonData[i].datetime,
      jsonData[i].jj,
    ]);
    jdata.push([i, jsonData[i].jj]);
  }
  for (let i = 0; i < 242 - hourData.length; i++) {
    hourData.push([hourData.length + i, null, null, null, null, null, null]);
    jdata.push([jdata.length + i, null, null, null, null, null, null]);
  }

  return { data: hourData, jdata: jdata };
};
const formatNumber = (number) => {
  const n = parseInt(number);
  let s = (n / 100000000).toFixed(2);
  if (s < 1) {
    s = (n / 10000).toFixed(2);
    if (s < 1) {
      return `${n}`;
    } else {
      return `${s}万`;
    }
  } else {
    return `${s}亿`;
  }
};
const initCulomn = (klineData) => {
  const culomnColor = [];
  const culomnValue = [];
  culomnColor[0] = klineData[0].increase > 0 ? 1 : -1;
  culomnValue[0] = [0, klineData[0].cjl, -1];
  for (let i = 1; i < klineData.length; i++) {
    culomnColor[i] = klineData[i].price > klineData[i - 1].price ? 1 : -1;
    culomnValue[i] = [
      i,
      klineData[i].cjl,
      culomnColor[i],
      klineData[i].datetime,
    ];
  }
  for (let i = 0; i < 242 - culomnValue.length; i++) {
    culomnValue.push([
      culomnValue.length + i,
      null,
      null,
      null,
      null,
      null,
      null,
    ]);
  }
  return { color: culomnColor, data: culomnValue };
};
const FinitChart = () => {
  const data = rawData.value;
  const xdata = initxData(data);
  const result = fsplitData(data);
  const hourDa = result.data;
  const jdata = result.jdata;
  const culomn = initCulomn(data);
  const upcolor = '#FF0000'; //增长颜色
  const downColor = '#008000'; // 下跌颜色
  const optionData = {
    title: { text: '分时' },
    xAxis: [
      {
        type: 'category',
        data: xdata,
        boundaryGap: false,
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax',
        axisLine: { onZero: false },
      },
      // 柱状图
      {
        type: 'category',
        gridIndex: 1, //x 轴所在的 grid 的索引，默认位于第一个 grid。
        data: xdata,
        boundaryGap: false,
        axisLine: { onZero: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false },
        min: 'dataMin',
        max: 'dataMax',
      },
    ],
    yAxis: [
      {
        scale: true,
        splitArea: {
          show: true,
        },
      },
      {
        scale: true,
        gridIndex: 1, // y 轴所在的 grid 的索引，默认位于第一个 grid
        splitNumber: 2,
        axisLabel: { show: false },
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
      },
    ],
    series: [
      {
        type: 'line',
        data: hourDa,
        symbol: 'none', //无标记图案
        lineStyle: {
          width: 1,
          color: 'black',
        },
      },
      {
        type: 'line',
        data: jdata,
        symbol: 'none', //无标记图案
        lineStyle: {
          width: 1,
          color: '#d4a12f',
        },
      },
      {
        name: 'Volume',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: culomn.data,
      },
    ],
    grid: [
      {
        left: '10%',
        right: '10%',
        bottom: 200,
      },
      {
        left: '10%',
        right: '10%',
        height: 80,
        bottom: 80,
      },
    ],
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross', //十字准星指示器
      },
      borderWidth: 1,
      borderColor: '#ccc',
      padding: 10,
      textStyle: {
        color: '#000',
      },
      formatter: function (param) {
        param = param[0];
        const seriesName = param.seriesName;
        if (seriesName === 'Volume') {
          const res = formatNumber(param.data[1]);
          return [
            '时间: ' + param.data[3] + '<hr size=1 >',
            '成交量: ' + res + '<br/>',
          ].join('');
        } else {
          return [
            '时间: ' + param.data[6] + '<hr size=1 >',
            '价格: ' + param.data[1] + '<br/>',
            '均价: ' + param.data[7] + '<br/>',
            '涨跌额: ' + param.data[2] + '<br/>',
            '成交量: ' + formatNumber(param.data[3]) + '<br/>',
            '涨跌幅: ' + param.data[4] + '<br/>',
          ].join('');
        }
      },
    },
    visualMap: {
      type: 'piecewise',
      show: false, //不展示map，只应用对应颜色划分逻辑
      seriesIndex: 2, //指定取哪个系列的数据
      dimension: 2,
      // 定义每一段的颜色
      pieces: [
        {
          value: -1,
          color: downColor,
        },
        {
          value: 1,
          color: upcolor,
        },
      ],
    },
  };
  renderEcharts(optionData);
};

function initChart() {
  var data = splitData(rawData.value);
  option.value = {
    animation: false,
    legend: {
      data: ['日k', 'MA5', 'MA10', 'MA20', 'MA30'],
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          show: false, // 不显示Y轴的刻度信息
        },
      },
      borderWidth: 1,
      borderColor: '#ccc',
      padding: 10,
      textStyle: {
        color: '#000',
      },
      formatter: (params) => formatterTooltip(params),
    },
    visualMap: {
      show: false,
      seriesIndex: 5,
      dimension: 2,
      pieces: [
        {
          value: 1,
          color: downColor,
        },
        {
          value: -1,
          color: upColor,
        },
      ],
    },
    grid: [
      {
        left: '10%',
        right: '10%',
        height: '70%',
      },
      {
        left: '10%',
        right: '10%',
        top: '85%',
        height: '10%',
      },
    ],
    xAxis: [
      {
        type: 'category',
        data: data.categoryData,
        boundaryGap: false,
        axisLine: { onZero: false },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax',
        axisPointer: {
          z: 100,
        },
      },
      {
        type: 'category',
        gridIndex: 1,
        data: data.categoryData,
        boundaryGap: false,
        axisLine: { onZero: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false },
        min: 'dataMin',
        max: 'dataMax',
      },
    ],
    yAxis: [
      {
        scale: true,
        splitArea: {
          show: true,
        },
      },
      {
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        axisLabel: { show: false },
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
      },
    ],
    dataZoom: [
      {
        type: 'inside',
        xAxisIndex: [0, 1],
        startValue: rawData.value.length - 60, // 展示后10个数据的索引
        endValue: rawData.value.length, // 展示全部数据
        minValueSpan: 20,
      },
    ],
    series: [
      {
        name: '日k',
        type: 'candlestick',
        data: data.values,
        itemStyle: {
          color: upColor,
          color0: downColor,
          borderColor: undefined,
          borderColor0: undefined,
        },
      },
      {
        name: 'MA5',
        type: 'line',
        data: calculateMA(5, data),
        smooth: true,
        symbol: 'none', //无标记图案
        lineStyle: {
          width: 1,
          color: 'black',
        },
        itemStyle: {
          color: 'black', // 设置MA5点的颜色为红色
        },
      },
      {
        name: 'MA10',
        type: 'line',
        data: calculateMA(10, data),
        symbol: 'none', //无标记图案
        smooth: true,
        lineStyle: {
          width: 1,
          color: '#9932CC',
        },
        itemStyle: {
          color: '#9932CC', // 设置MA5点的颜色为红色
        },
      },
      {
        name: 'MA20',
        type: 'line',
        data: calculateMA(20, data),
        symbol: 'none', //无标记图案
        smooth: true,
        lineStyle: {
          width: 1,
          color: '#FF8C00',
        },
        itemStyle: {
          color: '#FF8C00', // 设置MA5点的颜色为红色
        },
      },
      {
        name: 'MA30',
        type: 'line',
        data: calculateMA(30, data),
        symbol: 'none', //无标记图案
        smooth: true,
        lineStyle: {
          width: 1,
          color: '#4169E1',
        },
        itemStyle: {
          color: '#4169E1', // 设置MA5点的颜色为红色
        },
      },
      {
        name: '成交量',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: data.volumes,
      },
    ],
    axisPointer: {
      link: [
        {
          xAxisIndex: 'all',
        },
      ],
      label: {
        backgroundColor: '#777',
      },
    },
  };
  renderEcharts(option.value);
}

const StockKline = async () => {
  try {
    const response = await fetch('/stockApi/sse/kline', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // 设置请求体格式为 JSON
      },
      body: JSON.stringify({
        code: props.cid,
      }),
    });
    // 解析响应数据
    const query = await response.json();
    rawData.value = query;
    initChart();
  } catch (error) {
    console.log('There was an error!', error);
  }
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
onMounted(() => {
  if (props.type === 'kline') {
    StockKline();
  }
  if (props.type === 'fs') {
    SseTask();
    SseFs();
  }
});
onUnmounted(() => {
  closeSSE();
});
</script>

<template>
  <EchartsUI ref="chartRef" style="height: 500px" />
</template>
