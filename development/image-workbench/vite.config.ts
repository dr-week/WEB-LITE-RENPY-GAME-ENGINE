import { defineConfig } from 'vite'

const packages = 'C:/CODES/webframework/fast/packages'

export default defineConfig({
  resolve: {
    alias: [
      { find: '@zuari/dom', replacement: `${packages}/dom/src/index.ts` },
      { find: '@zuari/signals', replacement: `${packages}/signals/src/index.ts` },
      { find: '@zuari/glyphs/actions', replacement: `${packages}/glyphs/src/actions.ts` },
      { find: '@zuari/glyphs/icons', replacement: `${packages}/glyphs/src/icons.ts` },
      { find: '@zuari/glyphs/navigation', replacement: `${packages}/glyphs/src/navigation.ts` },
      { find: '@zuari/glyphs/base', replacement: `${packages}/glyphs/src/base.ts` },
      { find: '@zuari/theme', replacement: `${packages}/recipes/styles/aether.css` }
    ]
  },
  server: {
    host: '127.0.0.1',
    port: 1422,
    strictPort: true,
    fs: { allow: ['..', `${packages}`] }
  }
})
