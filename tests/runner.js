// Test infrastructure only. Production interactions will be imported by browser.js in WEB-04.
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
  // Existing page baseline does not need scripts. WEB-04 module fixtures will explicitly import
  // production code, rather than implicitly running arbitrary page scripts in this frame.
  frame.setAttribute('sandbox', 'allow-same-origin');
  const dispose = () => frame.remove();
  signal.addEventListener('abort', dispose, { once: true });
  try {
    await new Promise((resolve, reject) => {
      frame.addEventListener('load', resolve, { once: true });
      frame.addEventListener('error', () => reject(new Error('frame load failed')), { once: true });
      signal.addEventListener('abort', () => reject(new Error('frame load aborted')), { once: true });
      if (srcdoc) frame.srcdoc = source;
      else frame.src = source;
      document.getElementById('fixtures').append(frame);
    });
    assert(!signal.aborted, 'fixture aborted');
    await check(frame.contentDocument, frame.contentWindow, frame);
  } finally {
    signal.removeEventListener('abort', dispose);
    dispose();
  }
}
