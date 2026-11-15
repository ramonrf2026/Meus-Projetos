// Renderiza a animação quadro a quadro (determinística) e gera um MP4 1080x1920.
// Uso: node render.mjs [saida.mp4] [fps]
//      node render.mjs --stills t1,t2,...   (salva PNGs 1080x1920 em ./stills)
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';

const here = path.dirname(fileURLToPath(import.meta.url));
const url = pathToFileURL(path.join(here, 'index.html')).href + '?record=1';
const args = process.argv.slice(2);

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(url);
await page.waitForFunction(() => window.__starlink);
const { W, H, TOTAL } = await page.evaluate(() => ({ ...window.__starlink }));

function ffmpeg(outArgs) {
  const p = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', `${W}x${H}`,
    ...outArgs], { stdio: ['pipe', 'inherit', 'inherit'] });
  return p;
}

if (args[0] === '--stills') {
  const dir = path.join(here, 'stills'); fs.mkdirSync(dir, { recursive: true });
  for (const t of args[1].split(',').map(Number)) {
    const b64 = await page.evaluate((t) => window.__starlink.frameB64(t), t);
    const out = path.join(dir, `t${String(t).padStart(5, '0')}.png`);
    await new Promise((res) => {
      const p = ffmpeg(['-r', '1', '-i', '-', '-vf', 'scale=iw*6:ih*6:flags=neighbor', '-frames:v', '1', out]);
      p.on('close', res); p.stdin.end(Buffer.from(b64, 'base64'));
    });
    console.log(out);
  }
} else {
  const out = path.resolve(args[0] || path.join(here, 'flamengo-9x16.mp4'));
  const fps = Number(args[1] || 30);
  const n = Math.round(TOTAL * fps);
  const p = ffmpeg(['-r', String(fps), '-i', '-', '-vf', 'scale=1080:1920:flags=neighbor',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]);
  const done = new Promise((res) => p.on('close', res));
  for (let i = 0; i < n; i++) {
    const b64 = await page.evaluate((t) => window.__starlink.frameB64(t), i / fps);
    if (!p.stdin.write(Buffer.from(b64, 'base64'))) await new Promise((r) => p.stdin.once('drain', r));
    if (i % (fps * 5) === 0) console.log(`quadro ${i}/${n}`);
  }
  p.stdin.end(); await done;
  console.log(`ok: ${out} (${TOTAL.toFixed(1)} s, ${fps} fps)`);
}
await browser.close();
