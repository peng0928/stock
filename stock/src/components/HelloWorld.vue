<template>
  <div class="w-1/5  container mx-auto flex">
    <a-input-search v-model:value="stockName" placeholder="代码" @search="Stock">
      <template #enterButton>
        <a-button>查询</a-button>
      </template>
    </a-input-search>
    <div class="ml-3 mt-1">
      <a-switch v-model:checked="state.check" checked-children="开" un-checked-children="关" @change="doFunc"/>
    </div>
  </div>
  <div class="flex" v-if="stock.name">
    <div class="w-2/12">
      <div class="max-h-dvh overflow-y-auto no-scrollbar text-center pb-16">
        <div v-for="(item, index) in stockPlate" :key="index">
          <div class="m-4 h-32 rounded-lg" :class="chgBgColor(item.rate)">
            <p class="font-medium text-xs pt-5">{{ item.code }}</p>
            <p class="font-medium text-lg">{{ item.name }}</p>
            <p class="font-semibold text-xs" :class="chgColor(item.rate)">
              ¥
              {{ item.end }}
            </p>
            <p class="font-semibold text-xl" :class="chgColor(item.rate)">{{ item.rate }}%</p>
          </div>
        </div>
      </div>
    </div>
    <div class="w-10/12 m-4">
      <div class="text-lg font-medium flex">
        <p class="mr-2">{{ stock.name }}</p>
        <p>{{ stock.code }}</p>
        <p class="text-sm font-medium ml-3 pt-1">成交量：{{ stock.turnover }}</p>
        <p class="text-sm font-medium ml-3 pt-1">总市值：{{ stock.market }}</p>
        <p class="text-sm font-medium ml-3 pt-1">流通市值：{{ stock.float_market }}</p>
        <p class="text-sm font-medium ml-3 pt-1">市盈：{{ stock.P_E }}</p>
        <p class="text-sm font-medium ml-3 pt-1">市净：{{ stock.market_net }}</p>
      </div>
      <div class="text-lg font-medium flex">
        <p class="mr-2">开：{{ stock.now }}</p>
        <p class="ml-3" :class="chgColor(stock.max, stock.now)">高：{{ stock.max }}</p>
        <p class="ml-3" :class="chgColor(stock.min, stock.now)">低：{{ stock.min }}</p>
      </div>
      <div class="flex">
        <p class="font-semibold text-4xl ml-3" :class="chgColor()">{{ stock.end }}</p>
        <icon-font :type="chgIcon()" :style="{fontSize: '35px'}"/>
      </div>
      <div class="text-lg font-medium flex">
        <p class="font-semibold text-xl mr-2 ml-1" :class="chgColor()">{{ stock.cha }}</p>
        <p class="font-semibold text-xl" :class="chgColor()">{{ stock.chg }}%</p>
      </div>
      <div class="container mx-auto pt-10">
        <div id="main" class="" style="min-height: 60vh"></div>
      </div>
    </div>
  </div>
  <div v-else class="flex container mx-auto items-center justify-center pt-10">
    <icon-font type="icon-zanwuxinxi" :style="{fontSize: '350px'}"/>
  </div>
</template>


<script setup>
import {ref, computed, onMounted} from 'vue'
import {createFromIconfontCN} from '@ant-design/icons-vue';
import * as echarts from 'echarts';

const IconFont = createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/c/font_4766848_ljrh2ypfin.js',
});
const stockName = ref('002640')
const state = ref({
  check: true
})
const stockPlate = ref([])
const stockPlateTest = ref([])
const stock = ref({
  chg: 0
})
const timer = ref([]);

const chgColor = (chg = 0, v = 0) => {
  const va = chg ? chg : stock.value.chg
  return va < v ? 'text-green-500' : 'text-red-500';
};
const chgIcon = () => {
  return stock.value.chg < 0 ? 'icon-xiadie' : 'icon-shangzhang';
};
const chgBgColor = (chg = 0) => {
  const va = chg ? chg : stock.value.chg;
  return va < 0 ? ' bg-green-100 hover:bg-green-200' : ' bg-red-100 hover:bg-red-200';
};
const Stock = async () => {
  StockGet();
  doFunc();
};
const StockGet = async (e = true) => {
  try {
    const response = await fetch('/api/stock/get', {
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
      StockTrendData();
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
const StockTrendData = async () => {
  const title = stock.value.name;
  const dp = stock.value.cid;
  try {
    const response = await fetch('/api/stock/trend/data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // 设置请求体格式为 JSON
      },
      body: JSON.stringify({
        code: dp,
      }),
    });
    // 解析响应数据
    const query = await response.json();
    EchartMain(title, query.trends)
  } catch (error) {
    console.log('There was an error!', error);
  }
};
const doFunc = () => {
  const timeList = timer.value;
  if (stock.value.name) {
    for (let i = 0; i < timeList.length; i++) {
      clearTimeout(timeList[i]);
    }
  }
  if (state.value.check) {
    const tid = setInterval(() => {
      StockGet(false)
    }, 1000);
    timer.value.push(tid);
    const cid = setInterval(() => {
      StockTrendData()
    }, 1000);
    timer.value.push(cid);
    const pid = setInterval(() => {
      StockTrend()
    }, 10000);
    timer.value.push(pid);
  }
}
// ECHART

const formatNumber = (number) => {
  const n = parseInt(number);
  let s = (n / 100000000).toFixed(2);
  if (s < 1) {
    s = (n / 10000).toFixed(2)
    if (s < 1) {
        return `${n}`;
    } else {
      return `${s}万`;
    }
  } else {
    return `${s}亿`;
  }
};
const initxData = (klineData) => {
  const xData = [];
  for (let i = 0; i < klineData.length; i++) {
    xData[i] = klineData[i].datetime;
  }
  return xData
};
const splitData = (jsonData) => {
  const hourData = [];
  for (let i = 0; i < jsonData.length; i++) {
    hourData.push([
      i,
      jsonData[i].price,
      jsonData[i].increase,
      jsonData[i].cjl,
      jsonData[i].ratio,
      jsonData[i].amount,
      jsonData[i].datetime
    ]);
  }
  return hourData;
}
const initCulomn = (klineData) => {
  const culomnColor = [];
  const culomnValue = [];
  culomnColor[0] = klineData[0].increase > 0 ? 1 : -1;
  culomnValue[0] = [0, klineData[0].cjl, -1];
  for (let i = 1; i < klineData.length; i++) {
    culomnColor[i] = klineData[i].price > klineData[i - 1].price ? 1 : -1;
    culomnValue[i] = [i, klineData[i].cjl, culomnColor[i], klineData[i].datetime
    ];
  }
  return {color: culomnColor, data: culomnValue}
}
const EchartMain = (title, data) => {
  const chartDom = document.getElementById('main');
  const myChart = echarts.init(chartDom);
  var option;
  const xdata = initxData(data)
  const hourDa = splitData(data)
  const culomn = initCulomn(data)
  const upcolor = "#FF0000"; //增长颜色
  const downColor = "#008000"; // 下跌颜色
  option = {
    title: {text: title + "-分时图"},
    xAxis: [
      {
        type: "category",
        data: xdata,
        boundaryGap: false,
        axisLine: {onZero: false},
        splitLine: {show: false},
        min: "dataMin",
        max: "dataMax"
      },
      // 柱状图
      {
        type: "category",
        gridIndex: 1, //x 轴所在的 grid 的索引，默认位于第一个 grid。
        data: xdata,
        boundaryGap: false,
        axisLine: {onZero: false},
        axisTick: {show: false},
        splitLine: {show: false},
        axisLabel: {show: false},
        min: "dataMin",
        max: "dataMax"
      },
    ],
    yAxis: [
      {
        scale: true,
        splitArea: {
          show: true
        }
      },
      {
        scale: true,
        gridIndex: 1, // y 轴所在的 grid 的索引，默认位于第一个 grid
        splitNumber: 2,
        axisLabel: {show: false},
        axisLine: {show: false},
        axisTick: {show: false},
        splitLine: {show: false}
      },
    ],
    series: [
      {
        type: "line",
        data: hourDa,
        symbol: "none",//无标记图案
        lineStyle: {
          width: 1,
          color: 'black'
        }
      },
      {
        name: "Volume",
        type: "bar",
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: culomn.data
      },
    ],
    grid: [
      {
        left: "10%",
        right: "10%",
        height: "50%"
      },
      {
        left: "10%",
        right: "10%",
        top: "65%",
        height: "18%"
      }
    ],
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross" //十字准星指示器
      },
      borderWidth: 1,
      borderColor: "#ccc",
      padding: 10,
      textStyle: {
        color: "#000"
      },
      formatter: function (param) {
        param = param[0];
        const seriesName = param.seriesName;
        if (seriesName === "Volume") {
          const res = formatNumber(param.data[1]);
          return [
            "时间: " + param.data[3] + '<hr size=1 >',
            "成交量: " + res + "<br/>",
          ].join("");
        } else {
          return [
            "时间: " + param.data[6] + '<hr size=1 >',
            "价格: " + param.data[1] + "<br/>",
            "涨跌额: " + param.data[2] + "<br/>",
            "成交量: " + formatNumber(param.data[3]) + "<br/>",
            "涨跌幅: " + param.data[4] + "<br/>"
          ].join("");
        }
      }
    },
    visualMap: {
      type: "piecewise",
      show: false, //不展示map，只应用对应颜色划分逻辑
      seriesIndex: 1, //指定取哪个系列的数据
      dimension: 2,
      // 定义每一段的颜色
      pieces: [
        {
          value: -1,
          color: downColor
        },
        {
          value: 1,
          color: upcolor
        }
      ]
    },
  }
  myChart.setOption(option);

};
onMounted(() => {

})
</script>