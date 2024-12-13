<template xmlns="http://www.w3.org/1999/html">
  <a-layout class="layout">
    <a-layout-header>
      <div class="logo"/>
      <div class="flex justify-between">
        <a-menu
            v-model:selectedKeys="selectedKeys"
            theme="dark"
            mode="horizontal"
            :style="{ lineHeight: '64px' }"
        >
          <a-menu-item key="1">
            <router-link to="/">大盘</router-link>
          </a-menu-item>
          <a-menu-item key="2">
            <router-link to="/stock">个股</router-link>
          </a-menu-item>
          <a-menu-item key="3">
            <router-link to="/plate">板块</router-link>
          </a-menu-item>
          <a-menu-item key="4">
            <router-link to="/ztb">涨停板</router-link>
          </a-menu-item>
          <a-menu-item key="5">
            <router-link to="/duanban">昨日涨停板</router-link>
          </a-menu-item>
        </a-menu>
        <div class="text-right text-white flex">
          <a-tooltip placement="bottom" color="white" class="pr-5">
            <template #title>
              <div class="container text-right">
                <div class="text-red-500 flex justify-between">
                  <div>涨:</div>
                  <div>{{ stockZsData.shz_zs }}</div>
                </div>
                <div class="text-black flex justify-between">
                  <div>平:</div>
                  <div>{{ stockZsData.shz_ps }}</div>
                </div>
                <div class="text-green-500 flex justify-between">
                  <div>跌:</div>
                  <div>{{ stockZsData.shz_ds }}</div>
                </div>
                <div class="text-black flex justify-between">
                  <div>涨跌:</div>
                  <div :class="StyleColor(stockZsData.shz_zf)">{{ stockZsData.shz_zf }}</div>
                </div>
                <div class="text-black flex justify-between">
                  <div>涨幅:</div>
                  <div :class="StyleColor(stockZsData.shz_zfb)" class="pl-3">{{ stockZsData.shz_zfb }}%</div>
                </div>

              </div>
            </template>
            <div :class="StyleColor(stockZsData.shz_zf)">上证：<span>{{ stockZsData.shz }}</span></div>
          </a-tooltip>
          <a-tooltip placement="bottom" color="white">
            <template #title>
              <div class="container text-right">
                <div class="text-red-500 flex justify-between">
                  <div>涨:</div>
                  <div>{{ stockZsData.sz_zs }}</div>
                </div>
                <div class="text-black flex justify-between">
                  <div>平:</div>
                  <div>{{ stockZsData.sz_ps }}</div>
                </div>
                <div class="text-green-500 flex justify-between">
                  <div>跌:</div>
                  <div>{{ stockZsData.sz_ds }}</div>
                </div>
                <div class="text-black flex justify-between">
                  <div>涨跌:</div>
                  <div :class="StyleColor(stockZsData.sz_zf)">{{ stockZsData.sz_zf }}</div>
                </div>
                <div class="text-black flex justify-between">
                  <div>涨幅:</div>
                  <div :class="StyleColor(stockZsData.sz_zfb)" class="pl-3">{{ stockZsData.sz_zfb }}%</div>
                </div>

              </div>
            </template>
            <div :class="StyleColor(stockZsData.shz_zf)">深证：<span>{{ stockZsData.sz }}</span></div>
          </a-tooltip>
        </div>
      </div>
    </a-layout-header>
    <a-layout-content class="m-5">
      <div :style="{ background: '#fff', padding: '24px' }" class="min-h-max">
        <router-view/>
      </div>
    </a-layout-content>

    <a-layout-footer style="text-align: center" class="fixed bottom-0 w-full">
      Ant Design ©2018 Created by Ant UED
    </a-layout-footer>
  </a-layout>
</template>
<script setup>
import {computed, onUnmounted, ref, onMounted} from 'vue';
import {menuStore} from './stores/stock';
import {createFromIconfontCN} from "@ant-design/icons-vue";
import func from './stores/func';

const StyleColor = func.StyleColor;
const IconFont = createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/c/font_4766848_85as6e2e8rl.js',
});
const stockZsData = ref({})
const showPopover = ref(false)

const menuVal = menuStore();
const selectedKeys = computed({
  get() {
    return [menuVal.name];
  },
  set(value) {
    menuVal.update(value[0]);
  }
});
const sse = new EventSource('/api/stock/zs');

function stockZsSSE() {
  sse.onmessage = (event) => {
    stockZsData.value = JSON.parse(event.data);
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

}


onMounted(() => {
  stockZsSSE()
})
onUnmounted(() => {
  sse.close();

})
</script>
