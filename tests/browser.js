import { assert, fetchPage, runCase, Skip, withFrame } from './runner.js';

import { initNavigation } from '../site/site.js';
import { initMedia, createPlayer } from '../site/media.js';

const cases = [];
const test = (name, action) => cases.push({ name, action });
const contentRoutes = ['index.html', 'About.html', 'privacy-policy.html', 'medical-disclaimer.html'];

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

test('Real-page frames refresh HTML/CSS and preserve relative asset resolution', async signal => {
  let previousStyle;
  for (let attempt = 0; attempt < 2; attempt++) {
    await withFrame('../site/index.html', 375, signal, doc => {
      assert(doc.baseURI === new URL('../site/index.html', location.href).href, 'incorrect page base');
      assert(doc.querySelector('[data-navigation-toggle]'), 'current HTML missing');
      const style = new URL(doc.querySelector('link[rel="stylesheet"]').href);
      assert(style.pathname.endsWith('/site/site.css') && style.searchParams.has('_webcheck'),
        'stylesheet can reuse a stale cached revision');
      assert(style.href !== previousStyle, 'successive fixtures reused stylesheet cache key');
      previousStyle = style.href;
      assert(doc.querySelector('.hero-photo img').src.endsWith('/site/assets/hero-800.webp'),
        'relative image resolution changed');
    });
  }
  const missing = await runCase('missing real page', childSignal =>
    withFrame('../site/does-not-exist.html', 320, childSignal, () => {}));
  assert(missing.status === 'FAIL' && missing.detail.includes('HTTP 404'), 'HTTP errors became passing fixtures');
});

test('Landing homepage is retrievable and its HTML link target resolves', async signal => {
  const doc = await fetchPage('../site/index.html', signal);
  assert(doc.title.trim(), 'missing title');
  const links = [...doc.querySelectorAll('body a[href]')];
  assert(links.length, 'no HTML navigation');
  for (const link of links) {
    const target = new URL(link.getAttribute('href'), new URL('../site/index.html', location.href));
    if (target.origin === location.origin) await fetchPage(target, signal);
  }
  assert(!doc.querySelector('meta[http-equiv="refresh"]'), 'homepage redirects');
  assert(['home', 'benefits', 'demo', 'mission', 'features', 'download', 'team', 'contact']
    .every(id => doc.getElementById(id)), 'landing section missing');
});

test('All content pages share navigation labels, order and destinations', async signal => {
  const routes = [];
  for (const route of contentRoutes) {
    const doc = await fetchPage(`../site/${route}`, signal);
    routes.push([...doc.querySelectorAll('nav a[href]')].map(a => [a.textContent.trim(), a.getAttribute('href')]));
  }
  assert(routes[0].length > 0, 'no navigation destinations');
  assert(routes.every(links => JSON.stringify(links) === JSON.stringify(routes[0])), 'navigation differs');
});

for (const route of ['index.html', 'About.html']) {
  test(`${route}: WEB-03 product copy and availability in HTML`, async signal => {
    const doc = await fetchPage(`../site/${route}`, signal);
    const text = doc.querySelector('main').textContent;
    for (const phrase of ['Count Pace', 'seconds per count', 'zero counts',
      'while the app is open', 'planned and completed sets', 'do not measure recovery',
      'All current Android features are free', 'Android download link coming soon', 'Coming Soon']) {
      assert(text.includes(phrase), `missing product explanation: ${phrase}`);
    }
    assert(!text.includes('pilot release'), 'obsolete release claim');
    assert(!doc.querySelector('a[href*="play.google.com"], a[href*="apps.apple.com"]'),
      'unverified store action');
  });
}

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

  for (const width of [320, 375, 768, 1024, 1440]) {
    test(`${route}: stylesheet and rendered width at ${width}px, scripts disabled`, async signal => {
      const path = `../site/${route}`;
      await fetchPage(path, signal); // An HTTP error page must not pass the frame load check.
      await withFrame(path, width, signal, (doc, win) => {
        assert(doc.querySelector('main'), 'page content missing');
        assert(doc.styleSheets.length > 0 && [...doc.styleSheets].some(sheet => sheet.cssRules.length),
          'stylesheet did not load');
        assert(win.getComputedStyle(doc.body).marginTop === '0px', 'site CSS not applied');
        assert(doc.documentElement.scrollWidth <= win.innerWidth + 1,
          `horizontal overflow: ${doc.documentElement.scrollWidth} > ${win.innerWidth}; ${[...doc.body.querySelectorAll("*")].filter(n => n.getBoundingClientRect().right > win.innerWidth + 1).slice(0, 8).map(n => n.tagName + "." + n.className + ":" + Math.round(n.getBoundingClientRect().width)).join(", ")}`);
        assert([...doc.querySelectorAll('nav a')].every(a => a.getClientRects().length > 0),
          'HTML navigation is hidden without JavaScript');
      });
    });
  }
}

// Actual production controllers run against isolated, script-disabled documents.
const navigationFixture = `<!doctype html><html><body><header>
<button data-navigation-toggle hidden aria-controls="fixture-nav" aria-expanded="false">Menu</button>
<nav id="fixture-nav"><a href="#target">Target</a></nav></header><main id="target">Content</main></body></html>`;
function fakeMediaQuery() {
  const listeners = [];
  return { matches: false, addEventListener: (_, callback) => listeners.push(callback),
    resize(value) { this.matches = value; listeners.forEach(callback => callback()); },
    get count() { return listeners.length; } };
}
test('Production navigation state, native link activation and duplicate initialization', async signal => {
  await withFrame(navigationFixture, 320, signal, (doc, win) => {
    const query = fakeMediaQuery();
    const first = initNavigation(doc, { matchMedia: () => query });
    assert(initNavigation(doc, { matchMedia: () => query }) === first, 'duplicate controller');
    assert(query.count === 1, 'duplicate resize listener');
    const button = doc.querySelector('button'), nav = doc.querySelector('nav');
    assert(!button.hidden && nav.hidden && button.getAttribute('aria-expanded') === 'false', 'initial state');
    button.click();
    assert(!nav.hidden && button.getAttribute('aria-expanded') === 'true', 'open state');
    const click = new win.MouseEvent('click', { bubbles: true, cancelable: true });
    assert(nav.querySelector('a').dispatchEvent(click) && !click.defaultPrevented, 'native link cancelled');
    assert(nav.hidden, 'link did not close');
    button.click(); button.click();
    assert(nav.hidden, 'duplicate toggle effects');
  }, { srcdoc: true });
});
test('Production Escape/focus return and resize while focused', async signal => {
  await withFrame(navigationFixture, 320, signal, (doc, win) => {
    const query = fakeMediaQuery(); initNavigation(doc, { matchMedia: () => query });
    const button = doc.querySelector('button'), nav = doc.querySelector('nav'), link = nav.querySelector('a');
    button.click(); link.focus();
    link.dispatchEvent(new win.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
    assert(nav.hidden && doc.activeElement === button, 'Escape focus return');
    query.resize(true);
    assert(!nav.hidden && button.hidden && doc.activeElement === link, 'desktop hid focused button');
    query.resize(false);
    assert(nav.hidden && !button.hidden && doc.activeElement === button, 'mobile hid focused link');
  }, { srcdoc: true });
});
function mediaFixture(attributes = '') {
  return `<!doctype html><html><body><div data-media-provider="disabled" ${attributes}>
  <p>Demo coming soon</p></div><p id="description">Readable transcript of the walkthrough.</p></body></html>`;
}
function configure(element, provider = 'youtube', speech = false) {
  Object.assign(element.dataset, { mediaProvider: provider, mediaPoster: 'poster.png',
    mediaDescriptionId: 'description', mediaAccessibilityReviewed: 'true', mediaHasSpeech: String(speech) });
  if (provider === 'youtube') element.dataset.mediaId = 'abcdefghijk';
  else element.dataset.mediaSrc = 'demo.mp4';
}
const delay = milliseconds => new Promise(resolve => setTimeout(resolve, milliseconds));
test('Production disabled and invalid media retain inert readable placeholders', async signal => {
  for (const invalid of [null, 'provider', 'id', 'remotePoster', 'remoteSource', 'missingDescription',
    'hiddenDescription', 'review', 'speech', 'captions', 'youtubeCaptions', 'missingFile', 'probeError']) {
    await withFrame(mediaFixture(), 320, signal, async doc => {
      const element = doc.querySelector('[data-media-provider]');
      if (invalid) configure(element, invalid === 'remoteSource' || invalid === 'captions' ? 'self-hosted' : 'youtube');
      if (invalid === 'provider') element.dataset.mediaProvider = 'unknown';
      if (invalid === 'id') element.dataset.mediaId = 'bad';
      if (invalid === 'remotePoster') element.dataset.mediaPoster = 'https://example.com/poster.png';
      if (invalid === 'remoteSource') element.dataset.mediaSrc = '//example.com/demo.mp4';
      if (invalid === 'missingDescription') element.dataset.mediaDescriptionId = 'absent';
      if (invalid === 'hiddenDescription') doc.getElementById('description').hidden = true;
      if (invalid === 'review') element.dataset.mediaAccessibilityReviewed = 'false';
      if (invalid === 'speech') delete element.dataset.mediaHasSpeech;
      if (invalid === 'captions' || invalid === 'youtubeCaptions') element.dataset.mediaHasSpeech = 'true';
      let created = 0, probes = 0;
      assert(!await initMedia(element, { exists: async () => { probes++; if (invalid === 'probeError') throw new Error('missing'); return invalid !== 'missingFile'; },
        create: () => { created++; } }), `${invalid}: enabled invalid configuration`);
      assert(!element.querySelector('button, iframe, video') && !created, `${invalid}: active player`);
      if (!invalid) assert(!probes, 'disabled media issued a request');
      assert(element.textContent.includes('Demo coming soon'), 'placeholder erased');
    }, { srcdoc: true });
  }
});
test('Production media activation, idempotence, speech reviews and provider configurations', async signal => {
  for (const provider of ['youtube', 'self-hosted']) {
    await withFrame(mediaFixture(), 320, signal, async (doc, win) => {
      const element = doc.querySelector('[data-media-provider]'); configure(element, provider, true);
      element.dataset.mediaCaptionsReviewed = 'true';
      if (provider === 'self-hosted') element.dataset.mediaCaptionsSrc = 'captions.vtt';
      let created = 0, supplied, callbacks;
      const options = { exists: async () => true, create: (config, mount, handlers) => {
        created++; supplied = config; callbacks = handlers; return () => mount.replaceChildren();
      } };
      const task = initMedia(element, options);
      assert(task === initMedia(element, options), 'duplicate initialization');
      assert(await task && !created && element.querySelectorAll('button').length === 1, 'eager/duplicate player');
      const button = element.querySelector('button'); button.click();
      button.dispatchEvent(new win.MouseEvent('click'));
      assert(created === 1 && supplied.provider === provider, 'duplicate activation');
      if (provider === 'self-hosted') assert(supplied.captions.endsWith('/captions.vtt'), 'missing captions');
      callbacks.ready();
      assert(element.querySelector('[role="status"]').textContent.includes(provider === 'youtube' ? 'may still be blocked' : 'Demo ready'), 'readiness claim');
      callbacks.error();
      assert(!button.disabled && button.textContent === 'Retry demo', 'post-ready failure');
      assert(doc.getElementById('description').textContent.includes('Readable transcript'), 'lost transcript');
      assert(element.querySelector('a[href]')?.textContent.includes(provider === 'youtube' ? 'YouTube' : 'directly'), 'missing direct fallback');
    }, { srcdoc: true });
  }
});
test('Production blocked playback, thrown errors, timeout and explicit retry', async signal => {
  for (const failure of ['error', 'throw', 'timeout']) {
    await withFrame(mediaFixture(), 320, signal, async doc => {
      const element = doc.querySelector('[data-media-provider]'); configure(element);
      let callbacks, created = 0, disposed = 0;
      await initMedia(element, { exists: async () => true, timeout: 20,
        create: (_, mount, handlers) => {
          created++; callbacks = handlers;
          if (failure === 'throw') throw new Error('blocked');
          mount.append(doc.createElement('span'));
          return () => { disposed++; };
        } });
      const button = element.querySelector('button'); button.click();
      if (failure === 'error') callbacks.error();
      if (failure === 'timeout') await delay(40);
      assert(!button.disabled && element.querySelector('[role="status"]').textContent.includes('unavailable'), 'no failure fallback');
      assert(!element.querySelector('.media-player').children.length, 'failed player retained');
      assert(failure === 'throw' || disposed === 1, 'failed player not disposed');
      callbacks?.ready(); // Late events cannot undo failure.
      assert(!button.disabled, 'late callback revived player');
      button.click(); assert(created === 2, 'retry failed');
      if (failure !== 'throw') callbacks.error();
    }, { srcdoc: true });
  }
});
test('Production native video adapter keeps controls, reviewed captions and error fallback', async signal => {
  await withFrame(mediaFixture(), 320, signal, doc => {
    // Suppress media network calls while inspecting the actual adapter's DOM.
    const mount = doc.createElement('div');
    let errors = 0;
    const originalCreate = doc.createElement.bind(doc);
    doc.createElement = tag => {
      const node = originalCreate(tag);
      if (tag === 'video') node.play = async () => {}; // No network; inspect native DOM only.
      return node;
    };
    const remove = createPlayer({ provider: 'self-hosted', poster: '', src: '', captions: 'captions.vtt', description: {} },
      mount, { ready() {}, error() { errors++; } });
    const video = mount.querySelector('video');
    assert(video.controls && video.preload === 'none' && !video.autoplay, 'native controls/preload');
    const track = video.querySelector('track');
    assert(track.kind === 'captions' && track.default && track.srclang === 'en', 'caption attributes');
    track.dispatchEvent(new Event('error'));
    assert(errors === 1, 'caption error unhandled');
    video.dispatchEvent(new Event('error'));
    assert(errors === 2, 'native error unhandled');
    remove(); assert(!mount.children.length, 'adapter removal');
  }, { srcdoc: true });
});

test('Production YouTube adapter uses privacy-enhanced embed only on creation', async signal => {
  await withFrame(mediaFixture(), 320, signal, doc => {
    const mount = doc.createElement('div'); // Detached iframe never connects or contacts YouTube.
    const remove = createPlayer({ provider: 'youtube', id: 'abcdefghijk' }, mount,
      { ready() {}, error() {} });
    const iframe = mount.querySelector('iframe');
    assert(iframe.src === 'https://www.youtube-nocookie.com/embed/abcdefghijk?autoplay=1', 'wrong embed');
    assert(iframe.title && iframe.referrerPolicy === 'strict-origin-when-cross-origin', 'iframe accessibility/privacy');
    remove(); assert(!mount.children.length, 'iframe removal');
  }, { srcdoc: true });
});
for (const route of contentRoutes) {
  for (const width of [375, 1440]) {
    test(`${route}: persistent shared header at ${width}px`, async signal => {
      await withFrame(`../site/${route}`, width, signal, async (doc, win) => {
        initNavigation(doc);
        const header = doc.querySelector('header');
        win.scrollTo(0, 500);
        await new Promise(resolve => win.requestAnimationFrame(() => win.requestAnimationFrame(resolve)));
        assert(win.scrollY > 0, 'page did not scroll');
        assert(Math.abs(header.getBoundingClientRect().top) < 1, 'header left viewport');
        assert(header.getBoundingClientRect().height <= win.innerHeight / 2 + 1, 'header obscures content');
        const button = header.querySelector('button');
        if (width < 768) { button.click(); assert(!header.querySelector('nav').hidden, 'menu unavailable after scroll'); }
        else assert(!header.querySelector('nav').hidden, 'desktop navigation hidden');
        // Simulate closing the menu before jumping to content; targets clear the measured header.
        if (width < 768) button.click();
        const target = doc.querySelector(route === 'index.html' ? '#features' : 'main');
        target.scrollIntoView();
        await new Promise(resolve => win.requestAnimationFrame(resolve));
        assert(target.getBoundingClientRect().top >= header.getBoundingClientRect().bottom - 1,
          'anchor target hidden behind header');
      });
    });
  }
}
for (const route of contentRoutes) {
  test(`${route}: production enhancement on real mobile markup`, async signal => {
    await withFrame(`../site/${route}`, 375, signal, async doc => {
      initNavigation(doc);
      const button = doc.querySelector('[data-navigation-toggle]'), nav = doc.querySelector('nav');
      assert(!button.hidden && nav.hidden, 'production HTML failed to collapse');
      button.click(); assert(!nav.hidden, 'production HTML failed to expand');
      button.click(); assert(nav.hidden, 'production HTML failed to close');
      if (route === 'index.html') {
        const demo = doc.querySelector('[data-media-provider]');
        assert(!await initMedia(demo), 'real disabled demo enabled');
        assert(!demo.querySelector('button, video, iframe'), 'real disabled demo created player');
      }
    });
  });
}

// WEB-05 quality: real assets decode; enlarged text reflows on all content routes.
for (const route of contentRoutes) {
  test(`${route}: skip link, image decoding and 200% text reflow`, async signal => {
    await withFrame(`../site/${route}`, 320, signal, async (doc, win) => {
      const skip = doc.querySelector('.skip-link');
      assert(skip && doc.querySelector(skip.getAttribute('href')), 'skip target missing');
      skip.focus();
      assert(doc.activeElement === skip, 'skip link cannot receive focus');
      doc.documentElement.style.fontSize = '200%';
      await new Promise(resolve => win.requestAnimationFrame(() => win.requestAnimationFrame(resolve)));
      await Promise.all([...doc.images].map(async image => {
        image.loading = 'eager'; await image.decode();
        assert(image.naturalWidth > 0, `image did not decode: ${image.getAttribute('src')} (${image.currentSrc})`);
      }));
      assert(doc.documentElement.scrollWidth <= win.innerWidth + 1, 'overflow at 200% text');
    });
  });
}
test('WEB-05 sitemap, social image and 404 HTML contract', async signal => {
  const doc = await fetchPage('../site/404.html', signal);
  assert(doc.querySelector('meta[name="robots"]').content === 'noindex', '404 indexable');
  assert(!doc.querySelector('link[rel="canonical"]'), '404 canonical');
  for (const node of doc.querySelectorAll('[href], [src]')) {
    const value = node.getAttribute('href') || node.getAttribute('src');
    assert(value.startsWith('/') || value.startsWith('#') || value.startsWith('mailto:'), 'nested 404 relative resource');
  }
  const response = await fetch('../site/sitemap.xml', { signal, cache: 'no-store' });
  assert(response.ok, 'sitemap missing');
  const xml = new DOMParser().parseFromString(await response.text(), 'application/xml');
  assert(xml.querySelectorAll('loc').length === 4 && !xml.documentElement.textContent.includes('404.html'), 'sitemap routes');
  const image = new Image(); image.src = '../site/assets/social.png'; await image.decode();
  assert(image.naturalWidth === 1200 && image.naturalHeight === 630, 'social image dimensions');
});

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
  scope: 'WEB-05 quality and WEB-04 production interactions; four real pages with scripts disabled and enlarged text; nested 404 and manual accessibility/network checks remain separate',
};
document.getElementById('report').textContent = JSON.stringify(window.browserReport, null, 2);
document.getElementById('summary').textContent = `${status}: ${counts.PASS} pass, ${counts.FAIL} fail, ` +
  `${counts.TIMEOUT} timeout, ${counts.SKIP} skipped. This is layout evidence, not release approval.`;
document.documentElement.dataset.testStatus = status;
clearTimeout(window.runnerWatchdog);
