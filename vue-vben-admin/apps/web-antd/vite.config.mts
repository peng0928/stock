import { defineConfig } from '@vben/vite-config';

export default defineConfig(async () => {
  return {
    application: {},
    vite: {
      server: {
        proxy: {
          '/api': {
            changeOrigin: true,
            rewrite: (path) => path.replace(/^\/api/, ''),
            // mock代理目标地址
            target: 'http://localhost:5320/api',
            ws: true,
          },
           '/stockApi': {
            changeOrigin: true,
            rewrite: (path) => path.replace(/^\/stockApi/, ''),
            target: 'http://127.0.0.1:6888/api',
            ws: true,
          },
        },
      },
    },
  };
});
