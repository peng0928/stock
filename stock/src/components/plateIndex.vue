<template>
  <div class="flex">
    <div v-for="(item, index) in plateData" :key="index" class="text-sm w-1/6">
      <div>{{ item.name }}</div>
    </div>
  </div>

</template>

<script setup>

import {ref} from "@vue/reactivity";

const plateData = ref([
  {name: "文化传媒"},
  {name: "酿酒行业"},
  {name: "医疗服务"},
  {name: "游戏"},
  {name: "保险"},
  {name: "文化传媒"},
  {name: "酿酒行业"},
  {name: "医疗服务"},
  {name: "游戏"},
  {name: "保险"},
  {name: "文化传媒"},
  {name: "酿酒行业"},
  {name: "医疗服务"},
  {name: "游戏"},
  {name: "保险"},
])
</script>