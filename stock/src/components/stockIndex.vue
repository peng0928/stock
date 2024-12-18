<template>
  <div class="w-1/5  container mx-auto flex">
    <a-input-search v-model:value="stockName" placeholder="代码" @search="Stock">
      <template #enterButton>
        <a-button>查询</a-button>
      </template>
    </a-input-search>
    <div class="ml-3 mt-1">
    </div>
  </div>
  <div class="flex" v-if="stock.name">
    <!--侧边板块-->
    <div class="w-2/12">
      <div v-if="stockPlate" class="max-h-dvh overflow-y-auto no-scrollbar text-center pb-16">
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
      <a-skeleton active v-else :paragraph="{ rows: 20 }"/>
    </div>
    <div class="w-screen m-4">
      <div class="text-lg font-medium flex h-1/4 ">
        <div class="w-1/4 m-4">
          <div class="flex">
            <p class="mr-2">{{ stock.name }}</p>
            <p>{{ stock.code }}</p>
            <div class="ml-3 flex items-center text-blue-500">
              <div class="pb-1">
                <icon-font type="icon-shijian" :style="{fontSize: '25px'}"/>
              </div>
              <div class="pl-1">
                {{ currentTime }}
              </div>
            </div>
          </div>
          <div class="text-lg font-light flex">
            <p class="mr-2" :class="chgColor(stock.max, stock.zuos)">开：{{ stock.now }}</p>
            <p class="ml-3" :class="chgColor(stock.max, stock.zuos)">高：{{ stock.max }}</p>
            <p class="ml-3" :class="chgColor(stock.min, stock.now)">低：{{ stock.min }}</p>
            <p class="ml-3 text-yellow-600">均价：{{ stock.jj }}</p>
          </div>
          <div class="flex">
            <p class="font-semibold text-4xl ml-3" :class="chgColor()">{{ try_toFixed(stock.end) }}</p>
            <icon-font :type="chgIcon()" :style="{fontSize: '35px'}"/>
          </div>
          <div class="text-lg font-medium flex">
            <p class="font-semibold text-xl mr-2 ml-1" :class="chgColor()">{{ stock.cha }}</p>
            <p class="font-semibold text-xl" :class="chgColor()">{{ stock.chg }}%</p>
          </div>
        </div>
        <div class="text-left font-light flex text-sm  w-3/4 h-20 m-4"
        >
          <div v-for="(item, index) in stockInfo" :key="index" class="grid grid-cols-5 gap-4 text-center m-4">
            <div class="text-nowrap relative">
              <div class="flex hover:font-bold">
                <div>{{ item.n1 }}:</div>
                <div :class="stockColor(item.c1)" class="pl-1">{{ stock[item.k1] }}</div>
              </div>
              <div class="flex absolute bottom-0 hover:font-bold">
                <div>{{ item.n2 }}:</div>
                <div :class="stockColor(item.c2)" class="pl-1">{{ stock[item.k2] }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="w-full flex h-3/5">
        <div id="main" class="w-10/12" style="min-height: 60vh;">
          <div>
            <div class="mx-auto mt-5 w-full max-w-sm rounded-md  p-4" v-if="!echartsDataFlags">
              <a-skeleton active :paragraph="{ rows: 6 }"/>
            </div>
          </div>
        </div>
        <div class="w-2/12 pt-16 right-0">
          <div v-if="stock.md">
            <div class="p-2 mx-2 border-2 border-blue-200 rounded-lg font-light text-xs h-2/5"
                 :class="borderColor()">
              <div class="text-center">
                <span>五档</span>
              </div>
              <div v-for="(item, index) in stock.md" :key="index" v-if="stock.md">
                <div class="flex whitespace-nowrap hover:font-bold">
                  <div class="w-1/3">{{ item[0] }}</div>
                  <div class="ml-4 mr-4 w-1/3" :class="stockColor('',item[1])">{{ item[1] }}</div>
                  <div :class="indexColor(index)" class="w-1/3">{{ convertToChinese(item[2]) }}</div>
                </div>
                <div v-if="index===4">
                  <div class="flex">
                    <div class="h-1 bg-red-500" :style="calculatePercentage(1)"></div>
                    <div class="h-1 bg-green-500" :style="calculatePercentage()"></div>
                  </div>
                </div>
              </div>
              <div v-if="stockDetails.length">
                <div class="pt-3 pb-1">
                  <div class="flex flex-wrap sm:grid sm:grid-cols-4  bg-green-200 font-bold">
                    <div class="flex-grow sm:w-auto text-left">时间</div>
                    <div class="flex-grow sm:w-auto text-right">成交价</div>
                    <div class="flex-grow sm:w-auto text-right">手数</div>
                    <div class="flex-grow sm:w-auto text-right">笔数</div>
                  </div>
                </div>
                <div v-for="(item, index) in stockDetails.slice(-5).reverse()" :key="index">
                  <div class="flex flex-wrap sm:grid sm:grid-cols-4">
                    <div class="flex-grow sm:w-auto font-light text-left  hover:font-bold">{{ item[0] }}</div>
                    <div class="flex-grow sm:w-auto font-light text-right  hover:font-bold"
                         :class="stockColor('',item[1])">{{ item[1] }}
                    </div>
                    <div class="flex-grow sm:w-auto font-light text-right text-red-500  hover:font-bold">{{
                        item[2]
                      }}
                    </div>
                    <div class="flex-grow sm:w-auto font-light text-right text-red-500  hover:font-bold">{{
                        item[3]
                      }}
                    </div>
                  </div>
                </div>
                <div class="container text-center pt-1"><a>查看更多</a></div>
              </div>
            </div>
          </div>
          <div v-else class="h-2/5">
            <a-skeleton active/>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="flex container mx-auto items-center justify-center pt-10 ">
    <icon-font type="icon-zanwuxinxi" :style="{fontSize: '350px'}"/>
  </div>
</template>


<script setup>
import {ref, computed, onMounted, onBeforeUnmount, onUnmounted} from 'vue'
import {createFromIconfontCN} from '@ant-design/icons-vue';
import * as echarts from 'echarts';
import {useInputStore} from '../stores/stock';
import func from '../stores/func';

const convertToChinese = func.convertToChinese;
const try_toFixed = func.try_toFixed;
const IconFont = createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/c/font_4766848_85as6e2e8rl.js',
});
const inputStore = useInputStore();
const SSE = ref({
  get: undefined,
  trend: undefined,
  trend_data: undefined,
})

// 将 store 中的值映射为响应式数据
const stockName = computed({
  get() {
    return inputStore.name;
  },
  set(value) {
    inputStore.updateInputValue(value);
  }
});
const state = ref({
  check: false
})
const stockPlate = ref(false)
const echartsDataFlags = ref(false)
const stockDetails = ref([])
const stockPlateTest = ref([])
const stock = ref({
  chg: 0
})
const stockInfo = ref([
  {n1: "最新", k1: "zx", n2: "均价", k2: "jj", c1: true, c2: true},
  {n1: "涨幅", k1: "zf", n2: "涨跌", k2: 'zd', c1: true, c2: true},
  {n1: "总手", k1: "zs", n2: "金额", k2: 'je', c1: false, c2: false},
  {n1: "换手", k1: "hs", n2: "量比", k2: 'lb', c1: 'y', c2: 'r'},
  {n1: "最高", k1: "max", n2: "最低", k2: 'min', c1: true, c2: false},
  {n1: "今开", k1: "jk", n2: "昨收", k2: 'zuos', c1: true, c2: 'blue'},
  {n1: "涨停", k1: "zt", n2: "跌停", k2: 'dt', c1: 'r', c2: 'g'},
  {n1: "外盘", k1: "wp", n2: "内盘", k2: 'np', c1: 'r', c2: 'g'},
  {n1: "流通市值", k1: "float_market", n2: "市值", k2: 'market', c1: true, c2: true},
  {n1: "市盈", k1: "P_E", n2: "市净", k2: 'market_net', c1: true, c2: true},

]);
const timer = ref([]);
const currentTime = ref(new Date().toLocaleTimeString());

const updateTime = () => {
  currentTime.value = new Date().toLocaleTimeString();
};
setInterval(updateTime, 100);

const chgColor = (chg = 0, v = 0) => {
  const va = chg ? chg : stock.value.chg
  return va < v ? 'text-green-500' : 'text-red-500';
};

function calculatePercentage(s = 0) {
  const arrList = stock.value.md;
  const arr = [];
  for (let i = 0; i < arrList.length; i++) {
    arr.push(arrList[i][2]);
  }
  const totalSum = arr.reduce((sum, value) => {
    if (value !== '-') return sum + value;
    return sum;
  }, 0);

  // 计算前5个元素的和，忽略'-'
  const firstHalfSum = arr.slice(0, 5).reduce((sum, value) => {
    if (value !== '-') return sum + value;
    return sum;
  }, 0);

  // 计算后5个元素的和，忽略'-'
  const secondHalfSum = arr.slice(5).reduce((sum, value) => {
    if (value !== '-') return sum + value;
    return sum;
  }, 0);

  // 计算前5个元素和后5个元素的和的总占比
  const first = parseInt(firstHalfSum / totalSum * 100);
  const second = parseInt(secondHalfSum / totalSum * 100);
  if (s === 0) {
    return 'width: ' + first + '%'

  } else {
    return 'width: ' + second + '%'
  }
}

const borderColor = (chg = 0, v = 0) => {
  const va = chg ? chg : stock.value.chg
  return va < v ? 'border-green-500' : 'border-red-500';
};
const indexColor = (e) => {
  if (e > 4) {
    return 'text-red-500'
  } else {
    return 'text-green-500'
  }
};
const stockColor = (e, chg = 0, v = 0) => {
  if (e === false) {
    return ''
  }
  if (e === 'r') {
    return 'text-red-500'
  }
  if (e === 'g') {
    return 'text-green-500'
  }
  if (e === 'blue') {
    return 'text-blue-500'
  }
  if (e === 'y') {
    return 'text-purple-500'
  }
  const va = chg ? chg : stock.value.zx
  v = v ? v : stock.value.zuos
  return va < v ? 'text-green-500' : 'text-red-500';
};
const chgIcon = () => {
  return stock.value.chg < 0 ? 'icon-xiadie' : 'icon-shangzhang';
};
const chgBgColor = (chg = 0) => {
  const va = chg ? chg : stock.value.chg;
  return va < 0 ? 'bg-green-100 hover:bg-green-200' : ' bg-red-100 hover:bg-red-200';
};
const Stock = async () => {
  // StockGet();
  // doFunc();
  stock.value = {};
  StockGet();
  closeSSE();
  StockGetSSE();
  StockTrendDataSSE();
  StockTrendSSE();
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

function StockGetSSE() {
  const sse = new EventSource('/api/stock/get/' + stockName.value);
  sse.onmessage = (event) => {
    stock.value = JSON.parse(event.data);
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
  SSE.value.get = sse;
}

async function StockTrendDataSSE() {
  const dp = stock.value.cid;
  if (dp) {
    const sse = new EventSource('/api/stock/trend/data/' + dp);
    sse.onmessage = (event) => {
      const query = JSON.parse(event.data);
      const title = stock.value.name;
      if (query.trends.length > 0) {
        echartsDataFlags.value = true;
      }
      console.log('echartsDataFlags', echartsDataFlags.value, query.trends)
      EchartMain(title, query.trends)
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

    SSE.value.trend_data = sse;
  } else {
    await new Promise(resolve => setTimeout(resolve, 500));
    StockTrendDataSSE()
  }
}

async function StockTrendSSE() {
  const hy = stock.value.hy;
  const dp = stock.value.dp;
  if (dp) {
    const sse = new EventSource('/api/stock/trend?' + 'hy=' + hy + '&dp=' + dp + '&code=' + stockName.value);
    sse.onmessage = (event) => {
      const query = JSON.parse(event.data);
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

    SSE.value.trend = sse;
  } else {
    await new Promise(resolve => setTimeout(resolve, 500));
    StockTrendSSE()
  }
}


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
      StockDetails();
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
    if (query.trends.length > 0) {
      echartsDataFlags.value = true;
    }
    console.log('echartsDataFlags', echartsDataFlags.value, query.trends)
    EchartMain(title, query.trends)
  } catch (error) {
    console.log('There was an error!', error);
  }
};
const StockDetails = async () => {
  const dp = stock.value.cid;
  try {
    const response = await fetch('/api/stock/details', {
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
    stockDetails.value = query;
  } catch (error) {
    console.log('There was an error!', error);
  }
};

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
    jdata.push([
      i,
      jsonData[i].jj,
    ]);
  }
  for (let i = 0; i < 242 - hourData.length; i++) {
    hourData.push([hourData.length + i, null, null, null, null, null, null])
    jdata.push([jdata.length + i, null, null, null, null, null, null])
  }

  return {data: hourData, jdata: jdata};
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
  for (let i = 0; i < 242 - culomnValue.length; i++) {
    culomnValue.push([culomnValue.length + i, null, null, null, null, null, null])
  }
  return {color: culomnColor, data: culomnValue}
}
const EchartMain = (title, data) => {
  const chartDom = document.getElementById('main');
  const myChart = echarts.init(chartDom);
  var option;
  const xdata = initxData(data);
  const result = splitData(data);
  const hourDa = result.data;
  const jdata = result.jdata;
  const culomn = initCulomn(data)
  const upcolor = "#FF0000"; //增长颜色
  const downColor = "#008000"; // 下跌颜色
  option = {
    title: {text: "分时"},
    xAxis: [
      {
        type: "category",
        data: xdata,
        boundaryGap: false,
        splitLine: {show: false},
        min: "dataMin",
        max: "dataMax",
        axisLine: {onZero: false},
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
        },
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
        },
      },
      {
        type: "line",
        data: jdata,
        symbol: "none",//无标记图案
        lineStyle: {
          width: 1,
          color: '#d4a12f'
        },
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
        left: '10%',
        right: '10%',
        bottom: 200
      },
      {
        left: '10%',
        right: '10%',
        height: 80,
        bottom: 80
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
            "均价: " + param.data[7] + "<br/>",
            "涨跌额: " + param.data[2] + "<br/>",
            "成交量: " + formatNumber(param.data[3]) + "<br/>",
            "涨跌幅: " + param.data[4] + "<br/>",
          ].join("");
        }
      }
    },
    visualMap: {
      type: "piecewise",
      show: false, //不展示map，只应用对应颜色划分逻辑
      seriesIndex: 2, //指定取哪个系列的数据
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
onUnmounted(() => {
  closeSSE();
})

</script>