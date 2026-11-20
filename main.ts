// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry is the X post itself. This program does one thing: it hands
// the post's address to the gate by copying POST.json from the repository
// root to the output directory, where the house reads it and fetches the
// post from X (first picture, then text) for the judge.
//
// It validates that POST.json is a JSON object with a url string before
// writing, so a placeholder or a broken file fails loudly here instead of
// silently passing an invalid entry to the gate.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and
// MAKEFUN_OUTPUT_DIR stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

function main(): void {
  const source = join(BOT_DIR, 'POST.json');
  const target = join(OUTPUT_DIR, 'POST.json');

  let raw: string;
  try {
    raw = readFileSync(source, 'utf8');
  } catch (err) {
    console.error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
    process.exit(1);
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    console.error(`POST.json is not valid JSON: ${(err as Error).message}`);
    process.exit(1);
  }

  const url = (parsed as { url: string }).url;
  if (!url.startsWith('https://x.com/') && !url.startsWith('https://twitter.com/')) {
    console.error('POST.json must be an object with a url string for an X post.');
    process.exit(1);
  }

  mkdirSync(OUTPUT_DIR, { recursive: true });
  writeFileSync(target, raw, 'utf8');
  console.log(`handed in ${url}`);
}

main();
