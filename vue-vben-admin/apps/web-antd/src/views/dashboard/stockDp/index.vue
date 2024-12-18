<script lang="ts" setup>
import {Card} from 'ant-design-vue';

import {
  AnalysisChartCard,
  AnalysisChartsTabs,
  AnalysisOverview,
} from '@vben/common-ui';
import dpanEcharts from './danpan.vue';

const chartTabs: TabOption[] = [
  {
    label: '上证',
    value: 'trends',
  },
  {
    label: '深证',
    value: 'visits',
  },
];
</script>

<template>
  <div class="p-5">
    <AnalysisChartsTabs :tabs="chartTabs" class="mt-5">
      <template #trends>
        <dpanEcharts/>
      </template>
<!--      <template #visits>-->
<!--&lt;!&ndash;        <AnalyticsVisits/>&ndash;&gt;-->
<!--      </template>-->
    </AnalysisChartsTabs>
  </div>
</template>
