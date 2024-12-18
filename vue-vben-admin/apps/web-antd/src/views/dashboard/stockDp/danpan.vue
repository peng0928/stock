<script lang="ts" setup>
import {onMounted, ref} from 'vue';
import * as echarts from 'echarts';
import {
  EchartsUI,
  type EchartsUIType,
  useEcharts,
} from '@vben/plugins/echarts';

const chartRef = ref<EchartsUIType>();
const {renderEcharts} = useEcharts(chartRef);

const upColor = 'red';
const downColor = 'green';

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
    volumes: volumes
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
      const dataNum = parseFloat(data.values[i - j][1])
      sum += dataNum;
    }
    result.push(+(sum / dayCount).toFixed(3));
  }
  return result;
}

const rawData = ref([
  [
    "2004-01-02",
    10452.74,
    10409.85,
    10367.41,
    10554.96,
    168890000
  ],
  [
    "2004-01-05",
    10411.85,
    10544.07,
    10411.85,
    10575.92,
    221290000
  ],
  [
    "2004-01-06",
    10543.85,
    10538.66,
    10454.37,
    10584.07,
    191460000
  ],
  [
    "2004-01-07",
    10535.46,
    10529.03,
    10432,
    10587.55,
    225490000
  ],
  [
    "2004-01-08",
    10530.07,
    10592.44,
    10480.59,
    10651.99,
    237770000
  ],
  [
    "2004-01-09",
    10589.25,
    10458.89,
    10420.52,
    10603.48,
    223250000
  ],
  [
    "2004-01-12",
    10461.55,
    10485.18,
    10389.85,
    10543.03,
    197960000
  ],
  [
    "2004-01-13",
    10485.18,
    10427.18,
    10341.19,
    10539.25,
    197310000
  ],
  [
    "2004-01-14",
    10428.67,
    10538.37,
    10426.89,
    10573.85,
    186280000
  ],
  [
    "2004-01-15",
    10534.52,
    10553.85,
    10454.52,
    10639.03,
    260090000
  ],
  [
    "2004-01-16",
    10556.37,
    10600.51,
    10503.7,
    10666.88,
    254170000
  ],
  [
    "2004-01-20",
    10601.4,
    10528.66,
    10447.92,
    10676.96,
    224300000
  ],
  [
    "2004-01-21",
    10522.77,
    10623.62,
    10453.11,
    10665.7,
    214920000
  ],
  [
    "2004-01-22",
    10624.22,
    10623.18,
    10545.03,
    10717.4,
    219720000
  ],
  [
    "2004-01-23",
    10625.25,
    10568.29,
    10490.14,
    10691.77,
    234260000
  ],
  [
    "2004-01-26",
    10568,
    10702.51,
    10510.44,
    10725.18,
    186170000
  ],
  [
    "2004-01-27",
    10701.1,
    10609.92,
    10579.33,
    10748.81,
    206560000
  ],
  [
    "2004-01-28",
    10610.07,
    10468.37,
    10412.44,
    10703.25,
    247660000
  ],
  [
    "2004-01-29",
    10467.41,
    10510.29,
    10369.92,
    10611.56,
    273970000
  ],
  [
    "2004-01-30",
    10510.22,
    10488.07,
    10385.56,
    10551.03,
    208990000
  ],
  [
    "2004-02-02",
    10487.78,
    10499.18,
    10395.55,
    10614.44,
    224800000
  ],
  [
    "2004-02-03",
    10499.48,
    10505.18,
    10414.15,
    10571.48,
    183810000
  ],
  [
    "2004-02-04",
    10503.11,
    10470.74,
    10394.81,
    10567.85,
    227760000
  ],
  [
    "2004-02-05",
    10469.33,
    10495.55,
    10399.92,
    10566.37,
    187810000
  ],
  [
    "2004-02-06",
    10494.89,
    10593.03,
    10433.7,
    10634.81,
    182880000
  ],
  [
    "2004-02-09",
    10592,
    10579.03,
    10433.7,
    10634.81,
    160720000
  ],
  [
    "2004-02-10",
    10578.74,
    10613.85,
    10511.18,
    10667.03,
    160590000
  ],
  [
    "2004-02-11",
    10605.48,
    10737.7,
    10561.55,
    10779.4,
    277850000
  ],
  [
    "2004-02-12",
    10735.18,
    10694.07,
    10636.44,
    10775.03,
    197560000
  ],
  [
    "2004-02-13",
    10696.22,
    10627.85,
    10578.66,
    10755.47,
    208340000
  ],
  [
    "2004-02-17",
    10628.88,
    10714.88,
    10628.88,
    10762.07,
    169730000
  ],
  [
    "2004-02-18",
    10706.68,
    10671.99,
    10623.62,
    10764.36,
    164370000
  ],
  [
    "2004-02-19",
    10674.59,
    10664.73,
    10626.44,
    10794.95,
    219890000
  ],
  [
    "2004-02-20",
    10666.29,
    10619.03,
    10559.11,
    10722.77,
    220560000
  ],
  [
    "2004-02-23",
    10619.55,
    10609.62,
    10508.89,
    10711.84,
    229950000
  ],
  [
    "2004-02-24",
    10609.55,
    10566.37,
    10479.33,
    10681.4,
    225670000
  ],
]);

const StockKline = async () => {
  try {
    const response = await fetch('/stockApi/stock/kline', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // 设置请求体格式为 JSON
      },
      body: JSON.stringify({
        code: '1.000001'
      }),
    });
    // 解析响应数据
    const query = await response.json();
    rawData.value = query;
    var data = splitData(rawData.value);
    console.log(data, calculateMA(5, data));

    console.log(calculateMA(5, data));
    var option = {
      animation: false,
      legend: {
        data: ['日k', 'MA5', 'MA10', 'MA20', 'MA30'],
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
          label: {
            show: false // 不显示Y轴的刻度信息
          },
        },
        borderWidth: 1,
        borderColor: '#ccc',
        padding: 10,
        textStyle: {
          color: '#000'
        },
      },
      visualMap: {
        show: false,
        seriesIndex: 5,
        dimension: 2,
        pieces: [
          {
            value: 1,
            color: downColor
          },
          {
            value: -1,
            color: upColor
          }
        ]
      },
      grid: [
        {
          left: '10%',
          right: '8%',
          height: '50%'
        },
        {
          left: '10%',
          right: '8%',
          top: '80%',
          height: '15%'
        }
      ],
      xAxis: [
        {
          type: 'category',
          data: data.categoryData,
          boundaryGap: false,
          axisLine: {onZero: false},
          splitLine: {show: false},
          min: 'dataMin',
          max: 'dataMax',
          axisPointer: {
            z: 100
          }
        },
        {
          type: 'category',
          gridIndex: 1,
          data: data.categoryData,
          boundaryGap: false,
          axisLine: {onZero: false},
          axisTick: {show: false},
          splitLine: {show: false},
          axisLabel: {show: false},
          min: 'dataMin',
          max: 'dataMax'
        }
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
          gridIndex: 1,
          splitNumber: 2,
          axisLabel: {show: false},
          axisLine: {show: false},
          axisTick: {show: false},
          splitLine: {show: false}
        }
      ],
      dataZoom: [
        {
          type: 'inside',
          xAxisIndex: [0, 1],
          startValue: rawData.value.length - 60, // 展示后10个数据的索引
          endValue: rawData.value.length // 展示全部数据
        }
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
            borderColor0: undefined
          }
        },
        {
          name: 'MA5',
          type: 'line',
          data: calculateMA(5, data),
          smooth: true,
          symbol: "none",//无标记图案
          lineStyle: {
            width: 1,
            color: 'black'
          },
          itemStyle: {
            color: 'black' // 设置MA5点的颜色为红色
          }
        },
        {
          name: 'MA10',
          type: 'line',
          data: calculateMA(10, data),
          symbol: "none",//无标记图案
          smooth: true,
          lineStyle: {
            width: 1,
            color: '#9932CC'
          }, itemStyle: {
            color: '#9932CC' // 设置MA5点的颜色为红色
          }
        },
        {
          name: 'MA20',
          type: 'line',
          data: calculateMA(20, data),
          symbol: "none",//无标记图案
          smooth: true,
          lineStyle: {
            width: 1,
            color: '#FF8C00'
          }, itemStyle: {
            color: '#FF8C00' // 设置MA5点的颜色为红色
          }
        },
        {
          name: 'MA30',
          type: 'line',
          data: calculateMA(30, data),
          symbol: "none",//无标记图案
          smooth: true,
          lineStyle: {
            width: 1,
            color: '#4169E1'
          }, itemStyle: {
            color: '#4169E1' // 设置MA5点的颜色为红色
          }
        },
        {
          name: '成交量',
          type: 'bar',
          xAxisIndex: 1,
          yAxisIndex: 1,
          data: data.volumes
        }
      ], axisPointer: {
        link: [
          {
            xAxisIndex: 'all'
          }
        ],
        label: {
          backgroundColor: '#777'
        }
      },
    };
    renderEcharts(option);
  } catch (error) {
    console.log('There was an error!', error);
  }
};
var data = splitData(rawData.value);
var option = {
  animation: false,
  legend: {
    data: ['日k', 'MA5', 'MA10', 'MA20', 'MA30'],
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      label: {
        show: false // 不显示Y轴的刻度信息
      },
    },
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    textStyle: {
      color: '#000'
    },
  },
  visualMap: {
    show: false,
    seriesIndex: 5,
    dimension: 2,
    pieces: [
      {
        value: 1,
        color: downColor
      },
      {
        value: -1,
        color: upColor
      }
    ]
  },
  grid: [
    {
      left: '10%',
      right: '8%',
      height: '50%'
    },
    {
      left: '10%',
      right: '8%',
      top: '80%',
      height: '15%'
    }
  ],
  xAxis: [
    {
      type: 'category',
      data: data.categoryData,
      boundaryGap: false,
      axisLine: {onZero: false},
      splitLine: {show: false},
      min: 'dataMin',
      max: 'dataMax',
      axisPointer: {
        z: 100
      }
    },
    {
      type: 'category',
      gridIndex: 1,
      data: data.categoryData,
      boundaryGap: false,
      axisLine: {onZero: false},
      axisTick: {show: false},
      splitLine: {show: false},
      axisLabel: {show: false},
      min: 'dataMin',
      max: 'dataMax'
    }
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
      gridIndex: 1,
      splitNumber: 2,
      axisLabel: {show: false},
      axisLine: {show: false},
      axisTick: {show: false},
      splitLine: {show: false}
    }
  ],
  dataZoom: [
    {
      type: 'inside',
      xAxisIndex: [0, 1],
      startValue: rawData.length - 60, // 展示后10个数据的索引
      endValue: rawData.length // 展示全部数据
    }
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
        borderColor0: undefined
      }
    },
    {
      name: 'MA5',
      type: 'line',
      data: calculateMA(5, data),
      smooth: true,
      symbol: "none",//无标记图案
      lineStyle: {
        width: 1,
        color: 'black'
      },
      itemStyle: {
        color: 'black' // 设置MA5点的颜色为红色
      }
    },
    {
      name: 'MA10',
      type: 'line',
      data: calculateMA(10, data),
      symbol: "none",//无标记图案
      smooth: true,
      lineStyle: {
        width: 1,
        color: '#9932CC'
      }, itemStyle: {
        color: '#9932CC' // 设置MA5点的颜色为红色
      }
    },
    {
      name: 'MA20',
      type: 'line',
      data: calculateMA(20, data),
      symbol: "none",//无标记图案
      smooth: true,
      lineStyle: {
        width: 1,
        color: '#FF8C00'
      }, itemStyle: {
        color: '#FF8C00' // 设置MA5点的颜色为红色
      }
    },
    {
      name: 'MA30',
      type: 'line',
      data: calculateMA(30, data),
      symbol: "none",//无标记图案
      smooth: true,
      lineStyle: {
        width: 1,
        color: '#4169E1'
      }, itemStyle: {
        color: '#4169E1' // 设置MA5点的颜色为红色
      }
    },
    {
      name: '成交量',
      type: 'bar',
      xAxisIndex: 1,
      yAxisIndex: 1,
      data: data.volumes
    }
  ], axisPointer: {
    link: [
      {
        xAxisIndex: 'all'
      }
    ],
    label: {
      backgroundColor: '#777'
    }
  },
};

onMounted(() => {
  StockKline()
  // renderEcharts(option);
});
</script>

<template>
  <EchartsUI ref="chartRef" style="height: 350px"/>
</template>
