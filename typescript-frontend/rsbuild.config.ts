import { defineConfig } from '@rsbuild/core';

// Docs: https://rsbuild.rs/config/
export default defineConfig({
  dev: {
    // Write files (including manifest.json) to disk so Django can read the manifest in dev too
    writeToDisk: (file) => file.endsWith('manifest.json'),
  },
  server: {
    port: 3000,
    cors: true,
  },
  output: {
    manifest: true,
  },
});
