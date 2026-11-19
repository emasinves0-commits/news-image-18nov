// Copies the pre-drawn poster (entry.png, produced by draw.py) into the output directory.
// Output dir: MAKEFUN_OUTPUT_DIR if set and non-empty, otherwise /output (created if missing).
import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const dest = join(outDir, 'entry.png');
try {
  mkdirSync(outDir, { recursive: true });
  copyFileSync(new URL('./entry.png', import.meta.url), dest);
} catch (err) {
  console.error(`error: failed to copy entry.png to ${dest}: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
}
console.log(`wrote ${dest}`);
