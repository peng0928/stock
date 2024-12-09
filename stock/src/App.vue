<template>
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
            <router-link to="/ztb">涨停版</router-link>
          </a-menu-item>
        </a-menu>
        <div class="text-right text-white flex">
          <div class="text-red-500">上证：{{ stockZsData.shz }}</div>
          <div class="pl-5">深证: {{ stockZsData.sz }}</div>
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

const IconFont = createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/c/font_4766848_85as6e2e8rl.js',
});
const stockZsData = ref({})

const menuVal = menuStore();
const selectedKeys = computed({
  get() {
    return [menuVal.name];
  },
  set(value) {
    menuVal.update(value[0]);
  }
});

function stockZsSSE() {
  const sse = new EventSource('/api/stock/zs');
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

  // 组件卸载时关闭SSE连接
  onUnmounted(() => {
    sse.close();
  });
}


onMounted(() => {
  stockZsSSE()
})
</script>
