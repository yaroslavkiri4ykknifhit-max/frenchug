import { defineConfig } from 'astro/config';
export default defineConfig({site:process.env.SITE_URL || 'https://yaroslavkiri4ykknifhit-max.github.io',base:process.env.BASE_PATH || '/',output:'static',trailingSlash:'always',devToolbar:{enabled:false}});
