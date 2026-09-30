"""Check generated metadata, sitemap coverage and local references."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent / 'dist'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.meta = {}
        self.links = []
        self.canonical = ''
        self.h1 = 0
        self.title = ''
        self.in_title = False
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta': self.meta[a.get('name', a.get('property'))] = a.get('content')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a['href']
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self.in_title = True
        for key in ('src', 'href'):
            if a.get(key, '').startswith('/'): self.links.append(a[key])
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.title += data

records = []
indexable = set()
for path in sorted(ROOT.rglob('index.html')):
    text = path.read_text()
    p = Page(text)
    assert p.h1 == 1, path
    assert p.title and p.meta.get('description') and p.canonical, path
    schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', text).group(1))
    assert any(item.get('@type') == 'GeneralContractor' for item in schema)
    for link in p.links:
        local = ROOT / urlsplit(link).path.lstrip('/')
        assert local.exists(), (path, link)
    if 'noindex' not in p.meta['robots']: indexable.add(p.canonical)
    records.append({'page':str(path.relative_to(ROOT)), 'title':p.title,
                    'description':p.meta['description'], 'robots':p.meta['robots'],
                    'schema_types':[item.get('@type') for item in schema]})
assert len({p['title'] for p in records}) == len(records)
assert len({p['description'] for p in records}) == len(records)
sitemap = ET.parse(ROOT / 'sitemap.xml')
locations = [e.text for e in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert len(locations) == len(set(locations))
assert set(locations) == indexable
origin = urlsplit(locations[0])
assert 'Sitemap: '+origin.scheme+'://'+origin.netloc+'/sitemap.xml' in (ROOT/'robots.txt').read_text()
project_text = (ROOT/'projects/index.html').read_text()
assert project_text.count('/assets/gallery-') == 10
for i in [6,7,8,11,17,19,20,21,23,24]:
    assert f'/assets/gallery-{i}-polished.webp' in project_text
report = {'validation':'passed','page_count':len(records),'sitemap_url_count':len(locations),
          'polished_gallery_images':10,'public_indexing':'Private review deployment; public domain launch required','pages':records}
(ROOT.parent/'seo-audit.json').write_text(json.dumps(report, indent=2)+'\n')
print(f'Passed: {len(records)} pages, {len(locations)} sitemap URLs, all local references, 10 polished gallery images.')
