import { defineConfig } from '@rsbuild/core';
import { pluginSass } from '@rsbuild/plugin-sass';

const assetPrefix = process.env.RSBUILD_BASE_URL;
const corsOrigin = process.env.RSBUILD_CORS_ORIGIN;
const hmrHost = process.env.RSBUILD_HMR_HOST;

// Docs: https://rsbuild.rs/config/
export default defineConfig({
  plugins: [pluginSass()],
  dev: {
    // Django serves the HTML, so hot-update assets must keep the Rsbuild origin.
    assetPrefix: assetPrefix || true,
    client: {
      ...(hmrHost ? { host: hmrHost } : {}),
      port: '<port>',
    },
    // Write files (including manifest.json) to disk so Django can read the manifest in dev too
    writeToDisk: (file) => file.endsWith('manifest.json'),
  },
  server: {
    port: 3000,
    strictPort: true,
    cors: corsOrigin ? { origin: corsOrigin } : true,
    headers: {
      'Cache-Control': 'no-store',
    },
  },
  output: {
    manifest: true,
  },
  tools: {
    rspack: {
      optimization: {
        runtimeChunk: 'single',
      },
    },
  },
});
