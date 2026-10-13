// Optional playback, with no third-party request until explicit activation.
const initialized = new WeakMap();
function localURL(value, base) {
  if (!value || /^(?:[a-z][a-z\d+.-]*:|[\\/])/i.test(value) || value.includes('\\')) return null;
  const url = new URL(value, base);
  return url.origin === new URL(base).origin ? url.href : null;
}
export function mediaConfiguration(element) {
  const d = element.dataset;
  if (!['youtube', 'self-hosted'].includes(d.mediaProvider) ||
      d.mediaAccessibilityReviewed !== 'true' || !['true', 'false'].includes(d.mediaHasSpeech)) return null;
  const description = element.ownerDocument.getElementById(d.mediaDescriptionId);
  if (!description?.textContent.trim() || description.hidden || description.closest('[hidden]') ||
      !description.getClientRects().length ||
      element.ownerDocument.defaultView.getComputedStyle(description).visibility === 'hidden') return null;
  const base = element.ownerDocument.baseURI;
  const poster = localURL(d.mediaPoster, base);
  if (!poster) return null;
  const speech = d.mediaHasSpeech === 'true';
  if (speech && d.mediaCaptionsReviewed !== 'true') return null;
  if (d.mediaProvider === 'youtube') {
    if (!/^[\w-]{11}$/.test(d.mediaId || '') || d.mediaSrc) return null;
    return { provider: 'youtube', poster, id: d.mediaId, description };
  }
  const src = localURL(d.mediaSrc, base);
  const captions = localURL(d.mediaCaptionsSrc, base);
  if (!src || d.mediaId || (speech && !captions)) return null;
  return { provider: 'self-hosted', poster, src, captions, description };
}
export function createPlayer(config, mount, { ready, error }) {
  const doc = mount.ownerDocument;
  let player;
  if (config.provider === 'youtube') {
    player = doc.createElement('iframe');
    player.title = 'GoHealaX app walkthrough';
    player.src = `https://www.youtube-nocookie.com/embed/${config.id}?autoplay=1`;
    player.allow = 'autoplay; fullscreen';
    player.referrerPolicy = 'strict-origin-when-cross-origin';
    player.addEventListener('load', ready, { once: true });
  } else {
    player = doc.createElement('video');
    player.controls = true;
    player.preload = 'none';
    player.poster = config.poster;
    player.src = config.src;
    if (config.captions) {
      const track = doc.createElement('track');
      track.kind = 'captions'; track.srclang = 'en'; track.label = 'English';
      track.src = config.captions; track.default = true;
      track.addEventListener('error', error, { once: true });
      player.append(track);
    }
    player.addEventListener('loadeddata', ready, { once: true });
  }
  player.addEventListener('error', error, { once: true });
  mount.append(player);
  if (config.provider === 'self-hosted') player.play().catch(error);
  return () => player.remove();
}
export function initMedia(element, { create = createPlayer, timeout = 12000,
  exists = async url => (await fetch(url, { method: 'HEAD', cache: 'no-store' })).ok } = {}) {
  if (initialized.has(element)) return initialized.get(element);
  const task = setup();
  initialized.set(element, task);
  return task;
  async function setup() {
    const config = mediaConfiguration(element);
    if (!config) return false;
    try {
      const files = [config.poster, config.src, config.captions].filter(Boolean);
      if (!(await Promise.all(files.map(exists))).every(Boolean)) return false;
    } catch { return false; }
    const doc = element.ownerDocument;
    const button = doc.createElement('button');
    button.type = 'button'; button.className = 'button'; button.textContent = 'Play demo';
    const mount = doc.createElement('div'); mount.className = 'media-player';
    const status = doc.createElement('p'); status.setAttribute('role', 'status');
    const fallback = doc.createElement('p');
    fallback.textContent = 'If playback is unavailable, read the description below. ';
    const link = doc.createElement('a');
    link.href = config.src || `https://www.youtube.com/watch?v=${config.id}`;
    link.textContent = config.src ? 'Open video directly' : 'Open on YouTube';
    fallback.append(link);
    element.append(button, mount, status, fallback);
    let active = false, dispose, timer, generation = 0;
    button.addEventListener('click', () => {
      if (active) return;
      active = true; dispose = undefined; button.disabled = true;
      const attempt = ++generation;
      status.textContent = 'Loading demo…';
      const fail = () => {
        if (attempt !== generation || !active) return;
        ++generation; clearTimeout(timer); active = false;
        dispose?.(); mount.replaceChildren();
        button.disabled = false; button.textContent = 'Retry demo';
        status.textContent = 'Playback unavailable. Read the description or try again.';
      };
      timer = setTimeout(fail, timeout);
      try {
        dispose = create(config, mount, {
          error: fail,
          ready: () => {
            if (attempt !== generation) return;
            clearTimeout(timer);
            status.textContent = config.provider === 'youtube'
              ? 'Player loaded. Playback may still be blocked; the description remains available.'
              : 'Demo ready. The description remains available.';
          },
        });
        if (!active) { dispose?.(); mount.replaceChildren(); }
      } catch { fail(); }
    });
    return true;
  }
}
for (const element of document.querySelectorAll('[data-media-provider]')) initMedia(element);
