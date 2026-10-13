// Test infrastructure. browser.js imports the actual production interaction modules.
export class Skip extends Error {}
export class Timeout extends Error {}

export function assert(condition, message) {
  if (!condition) throw new Error(message);
}

export async function runCase(name, action, milliseconds = 4000) {
  const controller = new AbortController();
  let timer;
  try {
    await Promise.race([
      Promise.resolve().then(() => action(controller.signal)),
      new Promise((_, reject) => {
        timer = setTimeout(() => reject(new Timeout(`exceeded ${milliseconds} ms`)), milliseconds);
      }),
    ]);
    return { name, status: 'PASS', detail: '' };
  } catch (error) {
    return {
      name,
      status: error instanceof Skip ? 'SKIP' : error instanceof Timeout ? 'TIMEOUT' : 'FAIL',
      detail: error.message || String(error),
    };
  } finally {
    clearTimeout(timer);
    controller.abort(); // Abort page loads/fetches and dispose timed-out fixtures.
  }
}

export async function fetchPage(path, signal) {
  const response = await fetch(path, { signal, cache: 'no-store' });
  assert(response.ok, `${path}: HTTP ${response.status}`);
  return new DOMParser().parseFromString(await response.text(), 'text/html');
}

export async function withFrame(source, width, signal, check, { srcdoc = false } = {}) {
  const frame = document.createElement('iframe');
  frame.title = 'Isolated browser test fixture';
  frame.width = String(width);
  // Page HTML runs without scripts. Fixture checks explicitly call imported production functions
  // against this document; page scripts never execute implicitly.
  frame.setAttribute('sandbox', 'allow-same-origin');
  const dispose = () => frame.remove();
  signal.addEventListener('abort', dispose, { once: true });
  try {
    if (!srcdoc) {
      // Fetch the exact HTML used by the frame, bypassing previously cached page revisions.
      const url = new URL(source, location.href);
      const doc = await fetchPage(url, signal);
      assert(!doc.querySelector('base'), 'site pages must use document-relative URLs');
      const base = doc.createElement('base');
      base.href = url.href;
      doc.head.prepend(base);
      // A no-store HTML fetch alone cannot invalidate the browser's stylesheet cache.
      // Give each fixture an unused CSS URL while still loading the actual HTTP stylesheet.
      for (const link of doc.querySelectorAll('link[rel~="stylesheet"][href]')) {
        const stylesheet = new URL(link.getAttribute('href'), url);
        assert(stylesheet.origin === url.origin, 'fixture stylesheet must be same-origin');
        stylesheet.searchParams.set('_webcheck', crypto.randomUUID());
        link.href = stylesheet.href;
      }
      source = '<!doctype html>' + doc.documentElement.outerHTML;
    }
    assert(!signal.aborted, 'fixture aborted before load');
    await new Promise((resolve, reject) => {
      frame.addEventListener('load', resolve, { once: true });
      frame.addEventListener('error', () => reject(new Error('frame load failed')), { once: true });
      signal.addEventListener('abort', () => reject(new Error('frame load aborted')), { once: true });
      frame.srcdoc = source;
      document.getElementById('fixtures').append(frame);
    });
    assert(!signal.aborted, 'fixture aborted');
    await check(frame.contentDocument, frame.contentWindow, frame);
  } finally {
    signal.removeEventListener('abort', dispose);
    dispose();
  }
}
