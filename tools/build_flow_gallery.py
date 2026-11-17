#!/usr/bin/env python3
"""Build static/data/flow_gallery.json and static/images/flow/<id>/ from the Sketchfab export bundles (their manifest.json is the
single source: method status, Sketchfab UID, thumbnails, attribution). Nothing is invented here: a method that is not in a manifest
is not listed; a method without a UID is shown on the site as a still with its recorded status.
usage: build_flow_gallery.py <export dir> [<export dir> ...]      (run from the repo root; needs Pillow)"""
import json, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDER = ['stock', 'opera_combined', 'structure', 'material_only', 'reconviagen_v0.5', 'hi3dgen']      # GT is a fixed third panel (o['gt']), not a selectable method
# Era3D is a multiview-diffusion result: it is never listed in the flow-matching gallery, whatever the export manifest contains.
EXCLUDE = {'era3d'}
LABEL = {'stock': 'TRELLIS.2 (baseline)', 'opera_combined': 'OPERA Combined (ours)', 'structure': 'OPERA + Structure', 'material_only': 'OPERA + Material',
         'gt': 'Ground truth', 'reconviagen_v0.5': 'ReconViaGen v0.5', 'hi3dgen': 'Hi3DGen'}
GROUPS = [{'key': 'A', 'label': 'Fossils & Natural History'}, {'key': 'B', 'label': 'Insects · AntScan'}, {'key': 'C', 'label': 'Medical Anatomy'},
          {'key': 'D', 'label': 'Biological Specimens'}, {'key': 'E', 'label': 'Cultural Heritage'}]


def webp(src, dst, size, bg=None):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im = Image.open(src).convert('RGBA')
    if bg is not None:
        b = Image.new('RGBA', im.size, bg); b.alpha_composite(im); im = b.convert('RGB')
    im.thumbnail((size, size)); im.save(dst, 'WEBP', quality=88, method=6)
    return os.path.relpath(dst, ROOT)


objects, collection = [], None
for d in sys.argv[1:]:
    m = json.load(open(os.path.join(d, 'manifest.json'))); oid = m['object']; img = os.path.join(ROOT, 'static/images/flow', oid)
    collection = m.get('sketchfab_collection') or collection
    disp = next((os.path.join(d, f.split(' ')[0]) for f in m['input']['files'] if 'display' in f), None)
    o = {'id': oid, 'group': m.get('group', 'A'), 'name': m['name'], 'short_name': m.get('short_name', m['name']), 'credit': m.get('credit', ''),
         'source_url': m.get('source_url') or m.get('smithsonian_record'), 'native_gallery': m.get('native_gallery'), 'note': m.get('site_note', ''),
         'input': webp(disp, os.path.join(img, 'input.webp'), 900, (255, 255, 255, 255)), 'thumb': webp(disp, os.path.join(img, 'thumb.webp'), 220, (255, 255, 255, 255)),
         'primary': ['stock', 'opera_combined'], 'methods': {}, 'gt': None}
    for e in m['entries']:
        k = e['key']
        if k in EXCLUDE: continue
        st = e.get('site_status') or ('geometry_only' if k == 'hi3dgen' else 'not_guided_fallback' if e.get('guided') is False else 'guided' if k in ('structure', 'material_only', 'opera_combined') else 'available')
        uid = e.get('sketchfab_uid') if e.get('sketchfab_processing') == 'SUCCEEDED' else ''
        if str(e.get('permission', '')).startswith('UNRESOLVED-HOLD'):      # not certified as the linked gallery's version: listed, never displayed
            o['methods'][k] = {'status': 'held', 'status_label': 'not shown here', 'sketchfab_uid': '', 'note': 'Not shown: our stored output could not be matched to the version in the research gallery.'}; continue
        note = {'hi3dgen': 'Geometry only: this method outputs no texture.',
                'reconviagen_v0.5': 'Official release settings.', 'gt': 'Reference scan.'}.get(k, '')
        if k == 'gt' and uid: note = 'Original model on its author\'s Sketchfab page, in the author\'s own orientation.'
        if st == 'not_guided_fallback': note = 'Camera gate switched guidance off for this object: this is the unguided fallback, not a guided result.'
        pend = ''
        if not uid:
            perm = str(e.get('permission', ''))
            pend = ('Reference scan: shown as a still; see the source link for the original.' if k == 'gt'
                    else 'Not published interactively: the version shown in the linked research gallery could not be certified. Still render of our run shown.' if perm.startswith('UNRESOLVED')
                    else 'Interactive model not yet published; still render shown.')
        rec = {'status': st, 'sketchfab_uid': uid, 'poster': webp(os.path.join(d, e['thumbnail']), os.path.join(img, k.replace('.', '_') + '.webp'), 640, (244, 243, 239, 255)),
                           'note': note, 'frame_note': e.get('site_frame_note', ''), 'pending_note': pend, 'triangles': e.get('triangles')}
        if k == 'gt':      # true reference only: the original author's public model where one exists, otherwise a still of the study's GT scan
            rec.update(original_author_model=bool(uid), source_url=o['source_url'],
                       rights=('Shown through the original public Sketchfab model of its author.' if uid else 'Not hosted here: redistribution terms of the source scan are unresolved; still of the reference scan shown.'))
            o['gt'] = rec
        else:
            o['methods'][k] = rec
    if any(v['status'] == 'held' for v in o['methods'].values()):
        o['note'] = 'Selected example. Some methods are not shown for this object: our stored outputs could not be matched to the versions in the research gallery, which remains the reference for them.'
    objects.append(o)
# Objects of the owner's list whose original outputs are not on our storage: listed with their input image (from the cross-domain
# gallery) and a link to that gallery only. No viewer, no still of a model, nothing substituted.
LINK_ONLY = [
    ('ant_124', 'B', 'Eciton rapax (worker)', 'Army ant', 'AntScan micro-CT, specimen CASENT0744621 (CC BY 4.0).', 'https://doi.org/10.35097/xvug66q46ybwrx5n'),
    ('ant_4008', 'B', 'Parasyscia sp.', 'Parasyscia', 'AntScan micro-CT, specimen CASENT0877644 (CC BY 4.0).', 'https://doi.org/10.35097/puntaegngsg4xss9'),
    ('ant_392', 'B', 'Sphinctomyrmex stali', 'Sphinctomyrmex', 'AntScan micro-CT, specimen CASENT0790136 (CC BY 4.0).', 'https://doi.org/10.35097/gxfhjcpm31nrzjwm'),
    ('f7aa60639c60483f8e82fc182d2b0514', 'C', 'Occipital AVM', 'Occipital AVM', 'Model by jorgegonzalezcantero on Sketchfab (CC BY 4.0).', 'https://sketchfab.com/3d-models/occipital-avm-f7aa60639c60483f8e82fc182d2b0514'),
    ('e903b83694d5455da1d71c2943dd7bab', 'C', 'Tetralogy of Fallot with MAPCAs', 'Tetralogy of Fallot', 'Model by 3D Heart Project on Sketchfab (CC BY 4.0).', 'https://sketchfab.com/3d-models/tetralogy-of-fallot-with-mapcas-e903b83694d5455da1d71c2943dd7bab')]
have = {o['id'] for o in objects}
for oid, grp, name, short, credit, url in LINK_ONLY:
    if oid in have: continue
    img = f'static/images/flow/{oid}/input.webp'; assert os.path.isfile(os.path.join(ROOT, img)), img
    objects.append({'id': oid, 'group': grp, 'name': name, 'short_name': short, 'credit': credit, 'source_url': url, 'native_gallery': f'https://ood-results.vercel.app/#{oid}',
                    'input': img, 'thumb': img, 'primary': [], 'methods': {}, 'gt': None, 'link_only': True,
                    'note': 'Interactive models for this object are in the cross-domain results gallery (TRELLIS.2 and OPERA Combined, with ground truth); they are not hosted on this page yet.'})
ORDER_IDS = ['si02_mammuthus', 'si01_triceratops_view2', 'si25v2_a01_brachyceratops_montanensis_gilmo', 'ant_124', 'ant_4008', 'ant_392', 'ov13_10_lymphatic_system',
             'f7aa60639c60483f8e82fc182d2b0514', 'e903b83694d5455da1d71c2943dd7bab', 'si05_corallium', 'si25_17_subhyracodon_gidleyi_wood_1927', 'si25v2_c38_geochelone_carbonaria',
             'ov13_03_badge_of_the_black_prince', 'ov13_06_statue_of_liberty', 'ov13_02_armillary_sphere_1771']
objects.sort(key=lambda o: (o['group'], ORDER_IDS.index(o['id']) if o['id'] in ORDER_IDS else 99))
out = {'built_from': [os.path.basename(os.path.normpath(d)) for d in sys.argv[1:]], 'collection': collection, 'groups': [g for g in GROUPS if any(o['group'] == g['key'] for o in objects)],
       'method_order': ORDER, 'method_labels': LABEL, 'default_object': 'si02_mammuthus' if any(o['id'] == 'si02_mammuthus' for o in objects) else objects[0]['id'], 'objects': objects}
os.makedirs(os.path.join(ROOT, 'static/data'), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, 'static/data/flow_gallery.json'), 'w'), indent=1)
print(json.dumps({o['id']: {**{k: ('3D' if v['sketchfab_uid'] else 'still') for k, v in o['methods'].items()}, 'GT': ('3D original' if (o.get('gt') or {}).get('sketchfab_uid') else 'still' if o.get('gt') else 'none')} for o in objects}))
