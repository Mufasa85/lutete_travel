import { defineConfig } from 'vite'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.dirname(fileURLToPath(import.meta.url))

/**
 * Copie le dossier statique `assets/` (scripts classiques + images) dans le
 * build. Les pages referencent ces fichiers avec des URL relatives
 * (`assets/rdc-map.js`, `assets/img/xxx.jpg`) : Vite ne les traite pas comme
 * des modules, il faut donc les copier tels quels a la racine du site.
 */
function copyStaticAssets() {
  return {
    name: 'lutete-copy-static-assets',
    apply: 'build',
    closeBundle() {
      const src = path.join(root, 'assets')
      const dest = path.join(root, 'dist', 'assets')
      if (!fs.existsSync(src)) return
      fs.rmSync(dest, { recursive: true, force: true })
      fs.cpSync(src, dest, { recursive: true })
    },
  }
}

export default defineConfig({
  // Le site est multi-pages (index / activite / province / lutete-travel) :
  // pas de fallback SPA, chaque page reste une entree de build.
  appType: 'mpa',

  plugins: [copyStaticAssets()],

  build: {
    // `assets/` est copie tel quel par le plugin : on evite donc d'y mettre
    // les assets hashtes par Vite pour ne pas melanger les deux.
    assetsDir: 'static',
    rollupOptions: {
      input: {
        index: path.join(root, 'index.html'),
        activite: path.join(root, 'activite.html'),
        province: path.join(root, 'province.html'),
        luteteTravel: path.join(root, 'lutete-travel.html'),
      },
    },
  },

  server: {
    port: 5173,
    open: false,
  },

  preview: {
    port: 4173,
    open: false,
  },
})
