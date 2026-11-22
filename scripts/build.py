# SPDX-License-Identifier: MIT
"""Build the comparison page and readable catalog from the editorial JSON, offline."""
from pathlib import Path
import json
from html import escape as h
ROOT=Path(__file__).resolve().parents[1]
LABEL={'chat':'OpenAI Chat Completions','messages':'Anthropic Messages','responses':'OpenAI Responses','gemini':'Gemini native'}
def outputs():
 data=json.loads((ROOT/'data/providers.json').read_text()); providers=data['providers']
 md='# Карточки API · редакционный снимок\n\nПроверено 2026-11-23 (Asia/Shanghai). Это не рейтинг, не измерение и не подтверждение публикации поставщиков на сайте. Числовые цены не перепечатываются. [Методика](METHODOLOGY.md).\n\n'
 rows=''
 for p in providers:
  protocols=', '.join(LABEL[k] for k in p['protocols_documented'])
  md+=f'## {p["name"]}\n\n'
  for name,val in [('Официальный сайт',p['website']),('Документация',p['documentation']),('Публичные цены',p['pricing_url']),('Заявленные форматы',protocols),('Валюта',p['currency']),('Списание',p['billing']),('Ценовое свидетельство',p['price_evidence']),('Особенности цены',p['price_note']),('Ограничения',p['caveat']),('Группировка',p['group_note']),('Регион',p['region']),('Мониторинг',p['monitoring']),('Статус',p['status']),('Обнаружен / прочитан',p['discovered_at']+' / '+p['checked_at']+' (Asia/Shanghai)')]:md+=f'- **{name}:** {val}\n'
  md+='\n'
  rows+=f'''<tr data-protocols="{h(' '.join(p['protocols_documented']))}" data-currency="{h(p['currency'])}" data-group="{h(p['group'])}">
<td><a href="{h(p['website'])}">{h(p['name'])}</a><small>{h(p['group_note'])}</small></td>
<td>{h(protocols)}<small><a href="{h(p['documentation'])}">Источник: документация</a></small></td>
<td>{h(p['currency'])}<small>{h(p['billing'])}</small></td>
<td><a href="{h(p['pricing_url'])}">Публичная страница цен</a><small>{h(p['price_evidence'])} {h(p['price_note'])}</small></td>
<td>{h(p['caveat'])}<small>{h(p['region'])}</small></td>
<td><time datetime="{h(p['checked_at'])}">{h(p['checked_at'])}</time><small>Asia/Shanghai<br>Чтение источников, не API-тест.</small></td></tr>'''
 page='''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Сравнение API по публичной документации · Folkbench RU</title>
<meta name="description" content="Семь API-сайтов: форматы, валюта, тип списания, источники цен и ограничения. Редакционное сравнение без выдуманных рейтингов и доступности.">
<link rel="canonical" href="https://folkbench.github.io/relay-api-ru/"><link rel="stylesheet" href="style.css"><script src="filter.js" defer></script></head>
<body><header><nav aria-label="Связанные материалы"><a href="https://ru.folkbench.com/">Folkbench RU</a><a href="https://github.com/Folkbench/relay-api-ru">Репозиторий и методика</a><a href="https://github.com/Folkbench/awesome-ai-guide-ru">Руководства</a><a href="https://github.com/Folkbench/awesome-free-ai-ru">Бесплатные ресурсы</a></nav>
<p class="eyebrow">Открытый редакционный каталог · снимок 23 ноября 2026</p><h1>Выберите API по фактам,<br>а не по выдуманному месту</h1>
<p class="lead">Форматы, валюта, тип списания и источники цен для русскоязычных разработчиков. Семь сайтов, шесть редакционных групп. Связанные продукты не считаем независимыми конкурентами.</p></header>
<main><aside class="notice"><strong>Это не измеряемый рейтинг.</strong> Сопоставимых собственных тестов нескольких поставщиков пока нет. Не публикуем оценки, SLA, проценты доступности или скорость. Список по алфавиту. Документация отражает заявления поставщика, не гарантию качества.</aside>
<section aria-labelledby="filters-title"><h2 id="filters-title">Сузить выбор</h2><form id="filters"><label>Название или условие<input id="search" type="search" placeholder="Например: Beta или кэш"></label><label>Документированный формат<select id="protocol"><option value="">Все форматы</option><option value="chat">OpenAI Chat Completions</option><option value="messages">Anthropic Messages</option><option value="responses">OpenAI Responses</option><option value="gemini">Gemini native</option></select></label><label>Валюта<select id="currency"><option value="">Все валюты</option><option value="RUB">RUB</option><option value="USD">USD</option></select></label><button type="reset">Сбросить</button></form>
<p id="count" role="status" aria-live="polite">Показано сайтов: 7 · редакционных групп: 6</p><noscript><p>Фильтры требуют JavaScript. Все карточки ниже доступны без него.</p></noscript>
<div class="table-wrap" role="region" aria-label="Таблица сравнения API" tabindex="0"><table><caption>Что прямо указано в прочитанных публичных источниках</caption><thead><tr><th scope="col">Сайт / группа</th><th scope="col">Форматы</th><th scope="col">Валюта / списание</th><th scope="col">Свидетельство цены</th><th scope="col">Что проверить</th><th scope="col">Проверка</th></tr></thead><tbody>'''+rows+'''</tbody></table></div><p id="empty" hidden>Нет записей с такими условиями. Это не означает, что подходящего API не существует.</p></section>
<section class="explain"><h2>Как читать сравнение</h2><p>Неуказанный формат не объявляется неподдерживаемым. Совместимость зависит от пары «модель + метод», кэша и параметров. Числовые ставки намеренно не перепечатываются: разные каналы, цены «от», НДС и единицы нельзя сравнивать как одинаковые предложения. Откройте каталог поставщика перед оплатой.</p><p>PlusVibe API и GetVibe учитываются в одной редакционной группе. Это консервативная группировка, не аудит владения. Для остальных записей независимость владельцев также не подтверждалась.</p>
<h2>Каталог ≠ официальное включение</h2><p>Запись не означает сотрудничество, одобрение или публикацию на основном сайте. Мы не продаём API. Включение основано на открытых страницах; частные договорённости и переписка не публикуются.</p><p>База русского сайта остаётся единственным источником официального включения и актуальных измерений. Этот снимок не синхронизирован с базой и не объявляет официальное открытие сайта. Изменение JSON не меняет базу.</p>
<p><a class="action" href="https://ru.folkbench.com/submit/">Подать заявку на сайт</a> <a href="https://github.com/Folkbench/relay-api-ru/issues/new/choose">Предложить редакционное исправление</a></p><p>Не отправляйте API-ключи или приватные документы в Issue. Региональную доступность, оплату картой, идентичность модели и ответы поддержки мы не тестировали.</p></section></main>
<footer><p>Folkbench RU · <a href="https://github.com/Folkbench/relay-api-ru/blob/main/sources.json">Официальные источники и даты</a> · <a href="https://github.com/Folkbench/relay-api-ru/blob/main/METHODOLOGY.md">Методика</a> · <a href="https://github.com/Folkbench/relay-api-ru/blob/main/LICENSE.md">CC BY 4.0 для текстов · MIT для кода</a></p><p>Нет аналитических трекеров, запросов к API поставщиков и форм для секретов. Снимок обновляется редакцией вручную.</p></footer></body></html>'''
 return {'CATALOG.md':md,'docs/index.html':page}
if __name__=='__main__':
 for path,content in outputs().items():
  p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding='utf-8')
 print('Готово: карточки и страница собраны из data/providers.json')
