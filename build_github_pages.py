"""Build and validate this website for a GitHub Pages project URL."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import os, re, subprocess, sys
import xml.etree.ElementTree as ET

root = Path(__file__).parent
url = os.environ.get('SITE_URL', 'https://neomematrix.github.io/cps-prestige-website').rstrip('/')
parsed = urlsplit(url)
assert parsed.scheme == 'https' and parsed.netloc, 'SITE_URL must be an HTTPS website URL'
base = parsed.path.rstrip('/')
subprocess.run([sys.executable, str(root/'build.py')], env={**os.environ, 'SITE_URL':url}, check=True)
for path in (root/'dist').rglob('*.html'):
    text = path.read_text()
    if base:
        text = re.sub(r'(\b(?:href|src|action)=[\"\'])/(?!/)', lambda m:m.group(1)+base+'/', text)
    path.write_text(text)
(root/'dist'/'.nojekyll').touch()
for path in (root/'dist').rglob('*.html'):
    text = path.read_text()
    assert 'chatgpt.site' not in text, path
    for link in re.findall(r'\b(?:href|src)=[\"\']([^\"\']+)', text):
        if not link.startswith('/'): continue
        local_path = urlsplit(link).path
        assert not base or local_path.startswith(base+'/'), (path, link)
        local = root/'dist'/unquote(local_path[len(base):].lstrip('/'))
        assert local.exists(), (path, link)
for loc in ET.parse(root/'dist'/'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
    assert loc.text.startswith(url+'/'), loc.text
    local = root/'dist'/unquote(loc.text[len(url):].lstrip('/'))/'index.html'
    assert local.exists(), local
assert 'Sitemap: '+url+'/sitemap.xml' in (root/'dist'/'robots.txt').read_text()
print('GitHub Pages build passed: links, assets, canonical domain and sitemap.')
