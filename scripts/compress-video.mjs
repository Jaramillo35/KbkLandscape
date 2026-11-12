// npm run video [-- <dir>]
// Compresses every .mp4/.mov in video-src/ (or <dir>) into public/assets/video/
// as a silent, web-ready H.264 file plus a WebP poster, and fails if any
// output is over 8 MB. Requires ffmpeg on PATH.
import { execFileSync } from 'node:child_process';
import { readdirSync, statSync, mkdirSync, unlinkSync, existsSync } from 'node:fs';
import { join, parse } from 'node:path';
import sharp from 'sharp';

const SRC = process.argv[2] || 'video-src';
const OUT = 'public/assets/video';
const LIMIT = 8 * 1024 * 1024;

if (!existsSync(SRC)) { console.error(`No ${SRC}/ folder. Put source clips there.`); process.exit(1); }
mkdirSync(OUT, { recursive: true });
const ff = (args) => execFileSync('ffmpeg', ['-loglevel', 'error', '-y', ...args], { stdio: 'inherit' });

let failed = false;
for (const f of readdirSync(SRC).filter((n) => /\.(mp4|mov|m4v|webm)$/i.test(n))) {
  const name = parse(f).name;
  const out = join(OUT, `${name}.mp4`);
  for (const crf of [26, 29, 32]) {
    ff(['-i', join(SRC, f), '-an', '-vf', "scale='min(1920,iw)':-2,format=yuv420p", '-c:v', 'libx264', '-preset', 'slow', '-crf', String(crf), '-movflags', '+faststart', out]);
    if (statSync(out).size <= LIMIT) break;
  }
  const png = join(OUT, `${name}.poster.png`);
  ff(['-i', out, '-frames:v', '1', png]);
  await sharp(png).webp({ quality: 72 }).toFile(join(OUT, `${name}.webp`));
  unlinkSync(png);
  const mb = statSync(out).size / 1048576;
  console.log(`${name}.mp4  ${mb.toFixed(2)} MB${mb > 8 ? '  OVER 8 MB' : ''}`);
  if (mb > 8) failed = true;
}
process.exit(failed ? 1 : 0);
