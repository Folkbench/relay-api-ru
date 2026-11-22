// SPDX-License-Identifier: MIT
// Dependency-free DOM contract test, not a real-browser end-to-end test.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'docs/index.html'), 'utf8');
const rows = [...html.matchAll(/<tr data-protocols="([^"]+)" data-currency="([^"]+)" data-group="([^"]+)">([\s\S]*?)<\/tr>/g)].map(m => ({
  dataset: {protocols:m[1], currency:m[2], group:m[3]},
  textContent:m[4].replace(/<[^>]*>/g, ' '), hidden:false
}));
const handlers = {};
const controls = {
  '#filters': {addEventListener: (event, callback) => handlers[event] = callback},
  '#search': {value:''}, '#protocol': {value:''}, '#currency': {value:''},
  '#count': {textContent:''}, '#empty': {hidden:true}
};
const context = vm.createContext({document:{
  querySelector: selector => controls[selector], querySelectorAll: () => rows
}, setTimeout: callback => callback()});
vm.runInContext(fs.readFileSync(path.join(root,'docs/filter.js'),'utf8'), context);
const count = () => rows.filter(r => !r.hidden).length;
function expectResults(expected, groups) {
  assert.equal(count(), expected);
  assert.match(controls['#count'].textContent, new RegExp(`сайтов: ${expected} · редакционных групп: ${groups}`));
  assert.equal(controls['#empty'].hidden, expected !== 0);
  assert.equal(controls['#count'].textContent.includes('Нет записей с такими условиями.'), expected === 0);
}
expectResults(7,6);
controls['#search'].value='NeuroAPI'; handlers.input(); expectResults(1,1);
controls['#search'].value='no-such-resource'; handlers.input(); expectResults(0,0);
controls['#search'].value=''; controls['#protocol'].value='messages'; handlers.change(); expectResults(5,4);
controls['#currency'].value='RUB'; handlers.change(); expectResults(4,4);
controls['#protocol'].value='gemini'; controls['#currency'].value='USD';
handlers.change(); expectResults(0,0);
// Reset event is delivered before native controls reset; the deferred callback reads reset values.
controls['#search'].value=''; controls['#currency'].value=''; controls['#protocol'].value='';
handlers.reset(); expectResults(7,6);
assert.match(html, /<link rel="icon" href="favicon\.ico" type="image\/x-icon" sizes="32x32">/);
assert(html.indexOf('id="empty"') < html.indexOf('class="table-wrap"'), 'Empty hint must be above the wide comparison table');
assert.equal((html.match(/id="empty"/g)||[]).length, 1);
assert.match(html, /Это не измеряемый рейтинг/);
assert.match(html, /Сопоставимых собственных тестов нескольких поставщиков пока нет/);
console.log('OK: 7 sites/6 groups, NeuroAPI=1, search empty=0, Messages=5 + RUB=4, Gemini+USD=0, unified empty hints, reset=7, local favicon');
