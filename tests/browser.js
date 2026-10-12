import { assert, fetchPage, runCase, Skip, withFrame } from './runner.js';

const cases = [];
const test = (name, action) => cases.push({ name, action });
const contentRoutes = ['About.html', 'privacy-policy.html'];

test('Runner distinguishes assertions, skips and timeouts (infrastructure only)', async () => {
  const pass = await runCase('success', () => {});
  const fail = await runCase('failure', () => { throw new Error('intentional'); });
  const skip = await runCase('skip', () => { throw new Skip('deferred'); });
  const timeout = await runCase('timeout', () => new Promise(() => {}), 15);
  assert([pass, fail, skip, timeout].map(result => result.status).join(',') ===
    'PASS,FAIL,SKIP,TIMEOUT', 'result classification failed');
});

test('Isolated fixture loads and is disposed (infrastructure only)', async signal => {
  await withFrame('<!doctype html><html lang="en"><body><main><h1>Fixture</h1></main></body></html>',
    320, signal, doc => assert(doc.querySelector('h1')?.textContent === 'Fixture', 'fixture unavailable'),
    { srcdoc: true });
  assert(!document.querySelector('#fixtures iframe'), 'fixture leaked');
});

test('Existing homepage is retrievable and its HTML link target resolves', async signal => {
  const doc = await fetchPage('../site/index.html', signal);
  assert(doc.title.trim(), 'missing title');
  const links = [...doc.querySelectorAll('body a[href]')];
  assert(links.length, 'no HTML navigation');
  for (const link of links) {
    const target = new URL(link.getAttribute('href'), new URL('../site/index.html', location.href));
    if (target.origin === location.origin) await fetchPage(target, signal);
  }
  // Do not require the existing redirect: WEB-02 replaces it, and audit.py reports it today.
});

test('About and Privacy navigation destinations agree', async signal => {
  const routes = [];
  for (const route of contentRoutes) {
    const doc = await fetchPage(`../site/${route}`, signal);
    routes.push([...doc.querySelectorAll('nav a[href]')].map(a => a.getAttribute('href')).sort());
  }
  assert(routes[0].length > 0, 'no navigation destinations');
  assert(JSON.stringify(routes[0]) === JSON.stringify(routes[1]), 'navigation differs');
});

for (const route of contentRoutes) {
  test(`${route}: HTML landmarks, working local links and contact`, async signal => {
    const url = new URL(`../site/${route}`, location.href);
    const doc = await fetchPage(url, signal);
    for (const tag of ['main', 'header', 'footer', 'h1']) {
      assert(doc.querySelectorAll(tag).length === 1, `expected one ${tag}`);
    }
    assert(doc.querySelector('a[href="mailto:b.lp.self@gmail.com"]'), 'contact missing');
    for (const link of doc.querySelectorAll('a[href]')) {
      const destination = new URL(link.getAttribute('href'), url);
      if (destination.origin !== location.origin) continue;
      const target = await fetchPage(destination, signal);
      if (destination.hash) {
        assert(target.getElementById(decodeURIComponent(destination.hash.slice(1))),
          `missing fragment ${destination.hash}`);
      }
    }
  });

  for (const width of [320, 768, 1440]) {
    test(`${route}: stylesheet and rendered width at ${width}px, scripts disabled`, async signal => {
      const path = `../site/${route}`;
      await fetchPage(path, signal); // An HTTP error page must not pass the frame load check.
      await withFrame(path, width, signal, (doc, win) => {
        assert(doc.querySelector('main'), 'page content missing');
        assert(doc.styleSheets.length > 0 && [...doc.styleSheets].some(sheet => sheet.cssRules.length),
          'stylesheet did not load');
        assert(win.getComputedStyle(doc.body).marginTop === '0px', 'site CSS not applied');
        assert(doc.documentElement.scrollWidth <= win.innerWidth + 1,
          `horizontal overflow: ${doc.documentElement.scrollWidth} > ${win.innerWidth}`);
        assert([...doc.querySelectorAll('nav a')].every(a => a.getClientRects().length > 0),
          'HTML navigation is hidden without JavaScript');
      });
    });
  }
}

for (const deferred of [
  'Production navigation state, link activation and repeated initialization',
  'Production Escape/focus and resize behavior',
  'Production media disabled, invalid and activated states',
  'Production playback error and timeout fallbacks with controlled adapters',
]) {
  test(deferred, () => { throw new Skip('WEB-04: production modules not implemented in WEB-01'); });
}

const results = [];
for (const { name, action } of cases) {
  document.getElementById('summary').textContent = `Running: ${name}`;
  const result = await runCase(name, action);
  results.push(result);
  const item = document.createElement('li');
  item.dataset.status = result.status;
  item.textContent = `${result.status}: ${name}${result.detail ? ` — ${result.detail}` : ''}`;
  document.getElementById('results').append(item);
}

const counts = Object.fromEntries(['PASS', 'FAIL', 'TIMEOUT', 'SKIP'].map(status =>
  [status, results.filter(result => result.status === status).length]));
const status = counts.FAIL || counts.TIMEOUT ? 'FAIL' : counts.SKIP ? 'BASELINE_WITH_SKIPS' : 'PASS';
window.browserReport = {
  status, counts, results, userAgent: navigator.userAgent, url: location.href,
  timestamp: new Date().toISOString(),
  scope: 'WEB-01 baseline; scripts disabled in real-page frames; manual and WEB-04 checks deferred',
};
document.getElementById('report').textContent = JSON.stringify(window.browserReport, null, 2);
document.getElementById('summary').textContent = `${status}: ${counts.PASS} pass, ${counts.FAIL} fail, ` +
  `${counts.TIMEOUT} timeout, ${counts.SKIP} skipped. This is foundation evidence, not release approval.`;
document.documentElement.dataset.testStatus = status;
clearTimeout(window.runnerWatchdog);
