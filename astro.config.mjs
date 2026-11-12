import { defineConfig } from 'astro/config';
import relativeLinks from 'astro-relative-links';

// Static build for GitHub Pages. `format: 'file'` keeps the existing URLs
// (services.html, projects.html, about.html, contact.html, es/index.html).
export default defineConfig({
  site: 'https://kbklandscape.com',
  build: { format: 'preserve', inlineStylesheets: 'always' },
  integrations: [relativeLinks()],
  devToolbar: { enabled: false },
  server: { port: 4321 },
});
