// gta6-meme-x-01 entry program (Node 22+, standard library only).
//
// The entry is the X post itself: this repository's POST.json names the
// post's address, and the grader reads that file from the output directory.
// So this program does one job, carefully:
//
//   1. read POST.json from the bot directory (the repository root),
//   2. check it really is a JSON object whose "url" is the address of a
//      post on x.com or twitter.com (…/<handle>/status/<digits>),
//   3. copy the file, byte for byte, to POST.json in the output directory.
//
// A placeholder or malformed POST.json fails loudly (exit 1) instead of
// being handed in silently. The program touches nothing outside the bot
// and output directories, uses no network and no clock, and writes the
// same bytes on every run.

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// The address of one post: https://x.com/<handle>/status/<id>, the id in
// digits only; twitter.com is the same address on the older host name.
// The handle must be a real X handle (1-15 letters, digits or underscores):
// a looser pattern would wave through addresses no post can live at.
const POST_URL = /^https:\/\/(?:x\.com|twitter\.com)\/[A-Za-z0-9_]{1,15}\/status\/\d+\/?$/;

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

const sourcePath = join(BOT_DIR, 'POST.json');
let raw: Buffer;
try {
  raw = readFileSync(sourcePath);
} catch {
  fail(`POST.json could not be read from ${sourcePath}`);
}

let post: unknown;
try {
  post = JSON.parse(raw.toString('utf8'));
} catch {
  fail('POST.json is not valid JSON');
}

const url = (post as { url?: unknown } | null)?.url;
if (typeof url !== 'string' || !POST_URL.test(url)) {
  fail(
    'POST.json must name one X post as {"url": "https://x.com/<handle>/status/<id>"}; ' +
      `got ${JSON.stringify(url ?? null)}`,
  );
}

mkdirSync(OUTPUT_DIR, { recursive: true });
writeFileSync(join(OUTPUT_DIR, 'POST.json'), raw);
