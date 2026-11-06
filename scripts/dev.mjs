import { dev } from 'astro';
const args=process.argv.slice(2);
const value=(name,fallback)=>{const i=args.lastIndexOf(name);return i>=0&&args[i+1]&&!args[i+1].startsWith('--')?args[i+1]:fallback;};
// Run the official Astro API in the foreground for terminals and managed previews.
await dev({server:{host:value('--host','0.0.0.0'),port:Number(value('--port','4321'))},vite:{server:{strictPort:args.includes('--strictPort')}}});
