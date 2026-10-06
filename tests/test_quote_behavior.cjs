const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../dist/main.js'), 'utf8');

function load(endpoint = '', valid = true) {
  const handlers = {};
  const values = new Map(Object.entries({name: 'Test & Visitor', email: 'test@example.invalid',
    phone: '', location: 'Atlanta', service: 'Other project', message: 'Kitchen\nLine two & more'}));
  const status = {textContent: ''};
  const form = {dataset: {quoteEndpoint: endpoint}, elements: {service: {value: ''}},
    reportValidity: () => valid, addEventListener: (name, fn) => {handlers[name] = fn;}};
  const location = {search: '?service=flooring-tile', href: 'https://website.invalid/contact/'};
  const document = {querySelector: selector => selector === '#quote-form' ? form :
    selector === '#form-status' ? status : null, addEventListener() {}};
  vm.runInNewContext(source, {document, location, URLSearchParams,
    FormData: class {get(key) {return values.get(key);}}});
  return {handlers, form, location, status};
}

test('email fallback prepares the complete encoded request and tells the visitor to send it', () => {
  const page = load();
  let prevented = false;
  page.handlers.submit({preventDefault() {prevented = true;}});
  assert.ok(prevented);
  assert.ok(page.location.href.startsWith('mailto:cpsprestigeconstruction@gmail.com?'));
  const query = new URLSearchParams(page.location.href.split('?')[1]);
  assert.equal(query.get('subject'), 'Website quote request: Other project');
  assert.equal(query.get('body'), 'Name: Test & Visitor\nEmail: test@example.invalid\nPhone: \nLocation: Atlanta\nService: Other project\n\nProject details:\nKitchen\nLine two & more');
  assert.match(page.status.textContent, /Review it and press Send/);
});

test('invalid email-mode fields do not open the email application', () => {
  const page = load('', false);
  page.handlers.submit({preventDefault() {}});
  assert.equal(page.location.href, 'https://website.invalid/contact/');
  assert.equal(page.status.textContent, '');
});

test('configured forms leave native POST and validation intact, without email or premature success', () => {
  const page = load('https://quote-handler.invalid/submit');
  assert.equal(page.handlers.submit, undefined);
  assert.equal(page.form.elements.service.value, 'Flooring & tile');
  assert.equal(page.location.href, 'https://website.invalid/contact/');
  assert.equal(page.status.textContent, '');
});
