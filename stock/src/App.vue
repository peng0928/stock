<template>
  <a-layout class="layout">
    <a-layout-header>
      <div class="logo"/>
      <a-menu
          v-model:selectedKeys="selectedKeys"
          theme="dark"
          mode="horizontal"
          :style="{ lineHeight: '64px' }"
      >
        <a-menu-item key="1">home</a-menu-item>

      </a-menu>
    </a-layout-header>
    <a-layout-content style="padding: 0 50px">
      <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>Home</a-breadcrumb-item>
        <a-breadcrumb-item>List</a-breadcrumb-item>
        <a-breadcrumb-item>App</a-breadcrumb-item>
      </a-breadcrumb>
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
import {ref} from 'vue';

const selectedKeys = ref(['2']);
</script>
