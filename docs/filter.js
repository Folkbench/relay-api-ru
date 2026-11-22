// SPDX-License-Identifier: MIT
'use strict';
const form = document.querySelector('#filters');
const search = document.querySelector('#search');
const protocol = document.querySelector('#protocol');
const currency = document.querySelector('#currency');
const rows = Array.from(document.querySelectorAll('tbody tr'));
function update() {
  const query = search.value.trim().toLocaleLowerCase('ru');
  const shown = rows.filter(row => {
    const match = (!query || row.textContent.toLocaleLowerCase('ru').includes(query)) &&
      (!protocol.value || row.dataset.protocols.split(' ').includes(protocol.value)) &&
      (!currency.value || row.dataset.currency === currency.value);
    row.hidden = !match;
    return match;
  });
  const groups = new Set(shown.map(row => row.dataset.group));
  const isEmpty = shown.length === 0;
  document.querySelector('#count').textContent = `Показано сайтов: ${shown.length} · редакционных групп: ${groups.size}` +
    (isEmpty ? ' · Нет записей с такими условиями.' : '');
  document.querySelector('#empty').hidden = !isEmpty;
}
form.addEventListener('input', update);
form.addEventListener('change', update);
form.addEventListener('submit', event => event.preventDefault());
form.addEventListener('reset', () => setTimeout(update, 0));
update();
