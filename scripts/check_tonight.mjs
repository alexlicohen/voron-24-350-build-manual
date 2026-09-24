#!/usr/bin/env node
// Parity: the Tonight overlay's JS planner (docs/javascripts/tonight.js) must
// give the Python planner's answer (scripts/build_tonight.py) for every seeded
// device state the build wrote into docs/assets/tonight.json (`cases`).
// Run after a build: `node scripts/check_tonight.mjs` (exit 0 = parity).
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { isDeepStrictEqual } from 'node:util';

const repo = join(dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const planner = require(join(repo, 'docs/javascripts/tonight.js'));
const data = JSON.parse(readFileSync(join(repo, 'docs/assets/tonight.json'), 'utf8'));

let fails = 0;
if (!Array.isArray(data.cases) || data.cases.length === 0) {
  console.log('FAIL tonight.json has no cases');
  process.exit(1);
}
for (const c of data.cases) {
  const got = planner.planState(data, c.ticks, c.printed, c.kit_arrived).summary;
  if (isDeepStrictEqual(got, c.expect)) {
    const b = got.sections[0].buckets.map((x) => `${x.budget}:${x.items.length}/${x.total}m`).join(' ');
    console.log(`PASS ${c.name} — done ${got.done}, start ${got.start}, ${b}`);
  } else {
    fails++;
    console.log(`FAIL ${c.name}`);
    console.log('  python:', JSON.stringify(c.expect));
    console.log('  js:    ', JSON.stringify(got));
  }
}
console.log(`check_tonight: ${data.cases.length - fails}/${data.cases.length} cases match`);
process.exit(fails ? 1 : 0);
