import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import fs from 'fs';
import path from 'path';
import { defineConfig, type Plugin } from 'vite';

function pruneStaleWebgameBundles(): Plugin {
  const emittedAssetFiles = new Set<string>();

  return {
    name: 'prune-stale-webgame-bundles',
    apply: 'build',
    buildStart() {
      emittedAssetFiles.clear();
    },
    generateBundle(_options, bundle) {
      for (const fileName of Object.keys(bundle)) {
        const normalized = fileName.replace(/\\/g, '/');
        if (normalized.startsWith('assets/') && normalized.indexOf('/', 7) === -1) {
          emittedAssetFiles.add(path.posix.basename(normalized));
        }
      }
    },
    closeBundle() {
      if (emittedAssetFiles.size === 0) return;

      const assetsDir = path.resolve(import.meta.dirname, '../webgame/assets');
      if (!fs.existsSync(assetsDir)) return;

      for (const entry of fs.readdirSync(assetsDir, { withFileTypes: true })) {
        if (!entry.isFile()) continue;
        if (!/\.(js|css|map)$/i.test(entry.name)) continue;
        if (!emittedAssetFiles.has(entry.name)) {
          fs.unlinkSync(path.join(assetsDir, entry.name));
        }
      }
    },
  };
}

export default defineConfig(() => {
  return {
    base: './',
    build: {
      outDir: '../webgame',
      emptyOutDir: false, // Don't wipe server/cname files if present
      rolldownOptions: {
        output: {
          manualChunks(id) {
            const normalized = id.replace(/\\/g, '/');
            if (!normalized.includes('/node_modules/')) return undefined;
            if (normalized.includes('/node_modules/three/')) return 'vendor-three';
            if (
              normalized.includes('/node_modules/@trystero-p2p/') ||
              normalized.includes('/node_modules/trystero/') ||
              normalized.includes('/node_modules/nostr-tools/') ||
              normalized.includes('/node_modules/@noble/') ||
              normalized.includes('nostr')
            ) {
              return 'vendor-p2p';
            }
            if (
              normalized.includes('/node_modules/react-dom/') ||
              normalized.includes('/node_modules/react/') ||
              normalized.includes('/node_modules/scheduler/')
            ) {
              return 'vendor-react';
            }
            if (normalized.includes('/node_modules/lucide-react/')) return 'vendor-icons';
            if (normalized.includes('/node_modules/@google/genai/')) return 'vendor-genai';
            return undefined;
          },
        },
      },
    },
    plugins: [react(), tailwindcss(), pruneStaleWebgameBundles()],
    resolve: {
      alias: {
        '@': path.resolve(import.meta.dirname, '.'),
      },
    },
    server: {
      // HMR is disabled in AI Studio via DISABLE_HMR env var.
      // Do not modify—file watching is disabled to prevent flickering during agent edits.
      hmr: process.env.DISABLE_HMR !== 'true',
      // Disable file watching when DISABLE_HMR is true to save CPU during agent edits.
      watch: process.env.DISABLE_HMR === 'true' ? null : {},
    },
  };
});
