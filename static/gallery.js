'use strict';
// Flow-matching gallery. Everything shown comes from static/data/flow_gallery.json (built from the export manifests):
// nothing is inferred here. A method without a Sketchfab UID is shown as a still with its true status, never as a fake viewer.
(async function () {
  const root = document.querySelector('#flow-gallery');
  if (!root) return;
  let data;
  try { data = await (await fetch('static/data/flow_gallery.json', { cache: 'no-cache' })).json(); }
  catch (e) { root.querySelector('.fg-status').textContent = 'The gallery data could not be loaded.'; return; }
  const $ = s => root.querySelector(s);
  const ORDER = data.method_order, LABEL = data.method_labels;
  const objects = data.objects, byId = Object.fromEntries(objects.map(o => [o.id, o]));
  const state = { group: null, id: null, slot: { a: null, b: null }, loaded: { a: false, b: false, gt: false } };
  const SLOTS = ['a', 'b', 'gt'];                                   // gt: fixed ground-truth panel, never a selectable method
  const rec = s => s === 'gt' ? byId[state.id].gt : byId[state.id].methods[state.slot[s]];
  const nameOf = s => s === 'gt' ? 'Ground truth' : LABEL[state.slot[s]];
  const usable = m => m && (m.status === 'guided' || m.status === 'available' || m.status === 'not_guided_fallback' || m.status === 'geometry_only');
  const methodsOf = o => ORDER.filter(k => usable(o.methods[k]));
  const tag = m => m.status === 'not_guided_fallback' ? ' · NOT GUIDED fallback' : m.status === 'geometry_only' ? ' · geometry only' : '';

  // ---- filters and thumbnails
  const filters = $('.fg-filters');
  data.groups.forEach(g => { const b = document.createElement('button'); b.className = 'choice'; b.dataset.group = g.key; b.textContent = g.label;
    b.setAttribute('aria-pressed', 'false'); b.addEventListener('click', () => setGroup(g.key)); filters.appendChild(b); });
  function setGroup(key, keepObject) {
    state.group = key;
    filters.querySelectorAll('button').forEach(b => { const on = b.dataset.group === key; b.classList.toggle('active', on); b.setAttribute('aria-pressed', String(on)); });
    const picker = $('.fg-picker'); picker.innerHTML = '';
    objects.filter(o => o.group === key).forEach(o => { const b = document.createElement('button'); b.className = 'model-choice'; b.dataset.id = o.id;
      b.innerHTML = `<img src="${o.thumb}" alt="" loading="lazy"><span></span>`; b.querySelector('span').textContent = o.short_name || o.name;
      b.addEventListener('click', () => setObject(o.id)); picker.appendChild(b); });
    if (!keepObject) setObject(objects.find(o => o.group === key).id);
  }

  // ---- one viewer slot
  function slotEl(s) { return root.querySelector(`.fg-viewer[data-slot="${s}"]`); }
  function unload(s) { const el = slotEl(s), f = el.querySelector('iframe'); f.removeAttribute('src'); f.hidden = true; el.querySelector('.viewer-cover').hidden = false;
    el.querySelector('.fg-unload').hidden = true; state.loaded[s] = false; }
  function renderSlot(s) {
    const o = byId[state.id], k = state.slot[s], m = o.methods[k], el = slotEl(s);
    unload(s);
    const sel = el.querySelector('select'); sel.innerHTML = '';
    methodsOf(o).forEach(x => { const op = document.createElement('option'); op.value = x; op.textContent = LABEL[x] + tag(o.methods[x]); op.selected = x === k; sel.appendChild(op); });
    el.classList.toggle('ours', k === 'opera_combined');
    const cover = el.querySelector('.viewer-cover'), poster = cover.querySelector('img'), btn = cover.querySelector('.button'), note = cover.querySelector('p');
    poster.src = m.poster || o.thumb; poster.alt = `${o.name}: ${LABEL[k]}, still render`;
    const link = el.querySelector('.fg-link');
    if (m.sketchfab_uid) { btn.hidden = false; btn.textContent = 'Load interactive 3D ↗'; note.textContent = 'Loads a third-party viewer from Sketchfab.';
      link.hidden = false; link.href = `https://sketchfab.com/3d-models/${m.sketchfab_uid}`; link.textContent = 'Open on Sketchfab ↗'; }
    else { btn.hidden = true; note.textContent = m.pending_note || 'Interactive model not yet published; still render shown.';
      link.hidden = !o.native_gallery; link.href = o.native_gallery || '#'; link.textContent = 'Open in the research gallery ↗'; }
    el.querySelector('.fg-method-note').textContent = [m.note, m.frame_note].filter(Boolean).join(' ');
  }
  function load(s) {
    const o = byId[state.id], m = rec(s), el = slotEl(s); if (!m || !m.sketchfab_uid) return;
    const f = el.querySelector('iframe'); f.title = `${o.name} · ${nameOf(s)} · interactive 3D`;
    f.src = `https://sketchfab.com/models/${m.sketchfab_uid}/embed?autostart=1&ui_theme=dark&ui_infos=0&ui_watermark_link=0`;
    f.hidden = false; el.querySelector('.viewer-cover').hidden = true; el.querySelector('.fg-unload').hidden = false; state.loaded[s] = true;
  }
  SLOTS.forEach(s => { const el = slotEl(s);
    if (s !== 'gt') el.querySelector('select').addEventListener('change', e => { state.slot[s] = e.target.value; renderSlot(s); renderChips(); });
    el.querySelector('.viewer-cover .button').addEventListener('click', () => load(s));
    el.querySelector('.fg-unload').addEventListener('click', () => unload(s));
    el.querySelector('.fg-full').addEventListener('click', () => { const st = el.querySelector('.viewer-stage'); (st.requestFullscreen || st.webkitRequestFullscreen || (() => {})).call(st); }); });

  // ---- fixed ground-truth panel: the original author's public model, or a still of the reference scan; never a generated model or the input
  function renderGT() {
    const o = byId[state.id], m = o.gt, el = slotEl('gt'); unload('gt'); el.hidden = !m; if (!m) return;
    const cover = el.querySelector('.viewer-cover'), poster = cover.querySelector('img'), btn = cover.querySelector('.button'), note = cover.querySelector('p'), link = el.querySelector('.fg-link');
    poster.src = m.poster; poster.alt = `${o.name}: ground truth, still render of the reference scan`;
    if (m.sketchfab_uid) { btn.hidden = false; note.textContent = 'Loads the original model from its author’s Sketchfab page.';
      link.hidden = false; link.href = `https://sketchfab.com/3d-models/${m.sketchfab_uid}`; link.textContent = 'Original on Sketchfab ↗'; }
    else { btn.hidden = true; note.textContent = 'Still of the reference scan (no interactive ground truth is hosted here).';
      link.hidden = !m.source_url; link.href = m.source_url || '#'; link.textContent = 'Open the source record ↗'; }
    el.querySelector('.fg-method-note').textContent = m.rights || '';
  }

  // ---- "more comparisons": every method of the object with its true status
  function renderChips() {
    const o = byId[state.id], box = $('.fg-methods'); box.innerHTML = '';
    ORDER.forEach(k => { const m = o.methods[k]; if (!m) return; const b = document.createElement('button'); b.className = 'choice'; b.textContent = LABEL[k] + (usable(m) ? tag(m) : ` · ${m.status_label || 'not available'}`);
      if (!usable(m)) { b.disabled = true; b.title = m.note || ''; } else { b.classList.toggle('active', state.slot.b === k || state.slot.a === k);
        b.addEventListener('click', () => { const s = matchMedia('(max-width:760px)').matches ? 'a' : 'b'; state.slot[s] = k; renderSlot(s); renderChips(); }); }
      box.appendChild(b); });
  }

  function setObject(id) {
    const o = byId[id]; state.id = id; if (o.group !== state.group) setGroup(o.group, true);
    root.querySelectorAll('.fg-picker .model-choice').forEach(b => { const on = b.dataset.id === id; b.classList.toggle('active', on); b.setAttribute('aria-pressed', String(on)); });
    const lo = !!o.link_only; $('.fg-compare').classList.toggle('link-only', lo); $('.fg-more').hidden = lo;
    if (lo) { SLOTS.forEach(unload); $('.fg-input img').src = o.input; $('.fg-input img').alt = `${o.name}: input image`; $('.fg-name').textContent = o.name; $('.fg-credit').textContent = o.credit || '';
      const s2 = $('.fg-source'); s2.hidden = !o.source_url; s2.href = o.source_url || '#'; const n2 = $('.fg-native'); n2.hidden = false; n2.href = o.native_gallery;
      $('.fg-linkonly a').href = o.native_gallery; $('.fg-status').textContent = o.note || ''; state.userPicked = true; return; }
    const av = methodsOf(o); state.slot.a = av.includes(o.primary[0]) ? o.primary[0] : av[0]; state.slot.b = av.includes(o.primary[1]) ? o.primary[1] : (av[1] || av[0]);
    $('.fg-input img').src = o.input; $('.fg-input img').alt = `${o.name}: input image`;
    $('.fg-name').textContent = o.name; $('.fg-credit').textContent = o.credit || '';
    const src = $('.fg-source'); src.hidden = !o.source_url; src.href = o.source_url || '#';
    const nat = $('.fg-native'); nat.hidden = !o.native_gallery; nat.href = o.native_gallery || '#';
    $('.fg-status').textContent = o.note || '';
    renderSlot('a'); renderSlot('b'); renderGT(); renderChips();
    if (location.hash.startsWith('#flow/') || state.userPicked) history.replaceState(null, '', '#flow/' + id);
    state.userPicked = true;
  }
  const want = location.hash.startsWith('#flow/') ? location.hash.slice(6) : data.default_object;
  const first = byId[want] ? want : data.default_object;
  setGroup(byId[first].group, true); setObject(first);
  if (location.hash.startsWith('#flow/')) document.querySelector('#explore').scrollIntoView();
  window.__flowGallery = { state, data, load, unload, setObject };
})();

// Branch tabs (Flow matching / Diffusion) and approach tabs: generic [data-tabs] groups.
document.querySelectorAll('[data-tabs]').forEach(group => {
  const buttons = group.querySelectorAll('[data-tab]');
  buttons.forEach(b => b.addEventListener('click', () => {
    buttons.forEach(x => { const on = x === b; x.classList.toggle('active', on); x.setAttribute('aria-pressed', String(on)); });
    document.querySelectorAll(`[data-panel-of="${group.dataset.tabs}"]`).forEach(p => { p.hidden = p.dataset.panel !== b.dataset.tab; });
  }));
});

// Hero: the full abstract opens on demand (the short one stays visible).
(function () { const b = document.querySelector('#abstract-toggle'), p = document.querySelector('#abstract-full'); if (!b || !p) return;
  b.addEventListener('click', () => { p.hidden = !p.hidden; b.setAttribute('aria-expanded', String(!p.hidden)); b.textContent = p.hidden ? 'Full abstract' : 'Hide full abstract'; }); })();
