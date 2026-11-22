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
assert.equal(count(),7);
assert.match(controls['#count'].textContent,/групп: 6/);
controls['#protocol'].value = 'messages'; handlers.change(); assert.equal(count(),5);
controls['#currency'].value = 'USD'; handlers.change(); assert.equal(count(),1);
controls['#search'].value = 'no-such-resource'; handlers.input();
assert.equal(count(),0); assert.equal(controls['#empty'].hidden,false);
controls['#search'].value=''; controls['#currency'].value=''; controls['#protocol'].value='gemini';
handlers.change(); assert.equal(count(),2);
controls['#protocol'].value=''; handlers.reset(); assert.equal(count(),7);
console.log('OK: initial list, family count, protocol/currency combination, empty state, reset');
