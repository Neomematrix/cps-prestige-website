"""Build-contract checks; no network requests or real lead submissions."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]

class Contact(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.form = None
        self.fields = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'form' and attrs.get('id') == 'quote-form':
            self.form = attrs
        if tag in ('input', 'textarea', 'select') and attrs.get('name'):
            self.fields.add(attrs['name'])

class QuoteFormTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'dist').mkdir()
        for name in ('build.py', 'service-content.json', 'dist/main.js', 'dist/styles.css'):
            shutil.copy2(ROOT/name, self.root/name)

    def build(self, endpoint=None):
        env = {**os.environ, 'SITE_URL': 'https://website.invalid'}
        env.pop('QUOTE_FORM_URL', None)
        if endpoint is not None:
            env['QUOTE_FORM_URL'] = endpoint
        return subprocess.run([sys.executable, str(self.root/'build.py')],
                              env=env, capture_output=True, text=True)

    def test_unset_and_blank_use_email(self):
        for endpoint in (None, '', '   '):
            with self.subTest(endpoint=endpoint):
                self.assertEqual(self.build(endpoint).returncode, 0)
                text = (self.root/'dist/contact/index.html').read_text()
                self.assertNotIn('data-quote-endpoint', Contact(text).form)
                self.assertEqual(Contact(text).form['action'], 'mailto:cpsprestigeconstruction@gmail.com')
                self.assertIn('Prepare my quote request', text)
                self.assertIn('Review and send the email', text)
                self.assertIn('your email app', (self.root/'dist/privacy/index.html').read_text())

    def test_direct_post_and_privacy_then_clear(self):
        # Reserved invalid domain: test fixture only, never a deployed endpoint.
        endpoint = 'https://quote-handler.invalid/submit?form=cps&source=website'
        self.assertEqual(self.build(endpoint).returncode, 0)
        text = (self.root/'dist/contact/index.html').read_text()
        form = Contact(text)
        self.assertEqual(form.form['method'], 'post')
        self.assertEqual(form.form['action'], endpoint)
        self.assertEqual(form.form['data-quote-endpoint'], endpoint)
        self.assertEqual(form.fields, {'name', 'email', 'phone', 'location', 'service', 'message'})
        self.assertIn('Send my quote request', text)
        self.assertNotIn('Review and send the email', text)
        self.assertIn('&amp;source=website', text)
        privacy = (self.root/'dist/privacy/index.html').read_text()
        self.assertIn('quote-handler.invalid', privacy)
        self.assertIn('may store the submission', privacy)
        self.assertNotIn('does not store your form entries', privacy)
        self.assertEqual(self.build('').returncode, 0)
        self.assertNotIn('quote-handler.invalid', (self.root/'dist/contact/index.html').read_text())
        self.assertNotIn('quote-handler.invalid', (self.root/'dist/privacy/index.html').read_text())

    def test_invalid_endpoint_fails_build(self):
        for endpoint in ('http://quote-handler.invalid', '/submit', 'javascript:alert(1)',
                         'https://user:password@quote-handler.invalid',
                         'https://quote-handler.invalid/#fragment',
                         'https://quote-handler.invalid/has space', 'https://',
                         'https://quote-handler.invalid:bad', 'https://quote-handler.invalid\\evil'):
            with self.subTest(endpoint=endpoint):
                result = self.build(endpoint)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('QUOTE_FORM_URL must be', result.stderr)
                self.assertFalse((self.root/'dist/contact/index.html').exists())

if __name__ == '__main__':
    unittest.main()
