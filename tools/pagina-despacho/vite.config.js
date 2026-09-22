import { defineConfig } from 'vite'
import { viteSingleFile } from 'vite-plugin-singlefile'

// Un solo archivo: todo el CSS y el JS quedan dentro del HTML.
// ADR-020 §3 y §4: la pagina viaja sola y no hace NI UNA peticion de red.
export default defineConfig({
  plugins: [viteSingleFile({ removeViteModuleLoader: true })],
  build: {
    outDir: 'dist',
    assetsInlineLimit: 100000000,
    cssCodeSplit: false,
    reportCompressedSize: false,
    rollupOptions: { output: { inlineDynamicImports: true } },
  },
})
