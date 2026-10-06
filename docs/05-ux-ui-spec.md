# 05 · UX/UI Specification · Anti-Clutter · Visual Priority · Режимы отображения

> Покрывает результаты анализа **№14–19**.
> Главный UX-принцип: **«Не показывай всё, что умеет индикатор. Показывай то, что трейдеру действительно необходимо увидеть в данный момент».**
> Переход **Clean → Normal (Detailed) → Analysis → Debug** не меняет ни одного логического расчёта (ADR-09, T-1).

---

## 14. UX/UI Specification

### 14.1 Тринадцать вопросов трейдера → элементы интерфейса

| # | Вопрос | Основной ответ | Резерв / детали | Tier | Цель, сек |
|---|---|---|---|:---:|:---:|
| 1 | Какой HTF bias? | Ribbon `HTF ▲ BULL` | Dashboard `HTF 4H BULLISH`. На графике — ◆HTF-уровни | 1 | ≤ 2 |
| 2 | Какова структура? | Последняя swing-метка `CHoCH↑` / `BOS↑` на графике | Ribbon `STR ▲`, Dashboard `CHoCH ↑ · 12 bars` | 1 | ≤ 3 |
| 3 | Где ликвидность? | Линии BSL/SSL: ближайшие 2 major с каждой стороны + Key Levels | Dashboard `NEXT BSL 1.0921 (+1.8 ATR)` | 1–2 | ≤ 3 |
| 4 | Была ли она снята? | Маркер `SSL ✕` у тени, обрыв линии | Ribbon `SSL ✕` (в течение N баров) | 1 | ≤ 3 |
| 5 | Где ключевые OB/FVG? | Ближайшие зоны (≤ 2 на сторону), HTF-приоритет | Analysis — все | 2 | ≤ 5 |
| 6 | Premium или Discount? | Ribbon `DISC 36%` + EQ-линия | Range Gauge | 2 | ≤ 3 |
| 7 | Где цена в dealing range? | **Range Gauge** — вертикальная шкала справа от цены | Dashboard `LOCATION` | 2 | ≤ 3 |
| 8 | Какая сессия? | Ribbon `LON KZ 47m` | Range box сессии | 2 | ≤ 2 |
| 9 | Есть ли setup? | Композиция сетапа + Ribbon `LONG READY` | Dashboard `SETUP` | 1 | ≤ 2 |
| 10 | Почему он появился? | Строка цепочки в карточке `Sweep → CHoCH → FVG → OTE` | Тултип с разбором баллов. Analysis — Setup Path ①…⑥ | 1 | ≤ 10 |
| 11 | Где invalidation? | Линия SL/INV с меткой | Тултип: условие инвалидации | 1 | ≤ 3 |
| 12 | Где entry / SL / TP? | Композиция: entry-зона, линии E/SL/TP1–3 | Ценовые метки на шкале (опц.) | 1 | ≤ 3 |
| 13 | Насколько качественный setup? | Бейдж `A+ 8.4` в карточке | Dashboard `QUALITY 8.4 / 10 ▮▮▮▮▮▮▮▮▯▯` | 1 | ≤ 2 |

### 14.2 Информационная архитектура: четыре поверхности

| Поверхность | Отвечает на | Плотность | Всегда видна? |
|---|---|---|---|
| **Chart canvas** | *Где?* (пространство цены и времени) | Управляется приоритетом и режимом | Да |
| **Context Ribbon** | *Что в целом?* (одна строка) | 5–7 сегментов | Да (по умолч. во всех режимах, кроме Debug) |
| **Dashboard** | *Что именно и сколько?* | 8–11 строк | По умолчанию Compact. В Clean — выключен (заменён Ribbon) |
| **Тултипы** | *Почему? Подробности?* | Без ограничений | По наведению |

Плюс push-канал — алерты (§12.7).

### 14.3 Режимы (сводка; детали — §17–19)

| Режим | Для кого | Суть |
|---|---|---|
| **Clean** | Визуальный трейдер, исполнение | Минимум: bias, последний сдвиг, ближайшая ликвидность, ≤ 1 зона на сторону, активный сетап |
| **Normal** (Detailed, по умолч.) | Повседневный анализ | Ключевые зоны и уровни, последние события, Dashboard Compact |
| **Analysis** | Разбор, обучение, проверка логики | Internal-структура, история, Setup Path, Event Timeline, Focus/Inspect |
| **Debug** | Разработка, QA, поддержка | ID, состояния, R-оценки, ghost-объекты, бюджет, логи |
| **Custom** | Продвинутый пользователь | Потолок видимости = Analysis, всё решают тумблеры |

### 14.4 Панель настроек v1.0

Принципы: (1) профиль — первым; (2) «Логика» и «Отображение» внутри групп разделены подзаголовками; (3) короткие связанные поля — в одну строку (`inline`); (4) у каждого input есть `tooltip` со смыслом, единицами и значением по умолчанию; (5) все inputs с `display = display.none`; (6) режимы и пресеты — через `input.enum`.

```
⚙️ 0 · PROFILE
   Display Mode ................ [Normal ▼]   Clean / Normal / Analysis / Debug / Custom
   Theme ....................... [Auto ▼]     Auto / Dark / Light
   Palette ..................... [Standard ▼] Standard / Color-blind safe / Mono+ (v1.1)
   Chart text language ......... [EN ▼]       EN / RU / ES (тексты графика и дашборда)

🎨 1 · VISUAL EXPERIENCE   (тумблеры могут только СКРЫТЬ то, что разрешает режим — ADR-09)
   Smart Labels ................ [✓]    Label verbosity [Short ▼] Icons / Short / Full
   Auto Hide Old Objects ....... [✓]    History depth (bars) [1500]
   HTF Priority ................ [✓]
   Reduce Minor Liquidity ...... [✓]    Reduce Minor FVG [✓]    Reduce Minor OB [✓]
   Max zones per side .......... [2]
   Show Setup Path ............. [✓]    (действует в Analysis/Custom)
   Show Entry/SL/TP ............ [✓]    Price-scale markers [✗]
   Show Context Ribbon ......... [✓]    Position [Bottom Center ▼]
   Show Dashboard .............. [✓]    Position [Top Right ▼]  Size [Compact ▼]
   Adaptive Colors ............. [✓]    (модуляция прозрачности релевантностью)
   Dark/Light Theme Adaptation . [✓]
   Viewport-aware rendering .... [✗]    (advanced: пересчёт при прокрутке, AC-M16 в §15.1)

🏗 2 · STRUCTURE
   ── logic ──
   Structure preset ............ [Intraday ▼] Scalp 5/2 · Intraday 10/3 · Swing 20/5 · Manual
   Swing length ................ [10]   Internal length [3]        (Manual)
   Break confirmation .......... [Close ▼]   Close / Wick
   Equal H/L tolerance (×ATR) .. [0.10]
   Trend filter (scoring only) . [Off ▼]     Off / EMA 200 / Supertrend
   ── display ──
   Swing BOS/CHoCH [✓]   Internal structure [✓]   Swing labels [Significant ▼] Off/Significant/All

💧 3 · LIQUIDITY
   ── logic ──
   Max sweep penetration (×ATR)  [1.00]   Reclaim window (bars) [2]
   Old level age (bars) ........ [50]     Turtle soup window (bars) [10]
   Key levels: PDH/PDL [✓] PWH/PWL [✓] Session H/L [✓] Midnight open [✗]
   ── display ──
   BSL/SSL levels [✓]   Sweeps [✓]   Swept history [✓]   Levels per side [2]

🧱 4 · ORDER BLOCKS
   ── logic ──
   OB zone ..................... [Body+Wick ▼]  Full / Body+Wick / Body
   Require displacement ........ [✓]    Min displacement (×ATR) [1.0]
   Size min/max (×ATR) ......... [0.25] / [3.0]
   Volume filter ............... [✗]    Multiplier [1.5]   (авто-off без объёма)
   Mitigation rule ............. [50% ▼]  Touch / 50% / Full
   Breaker & Mitigation Block .. [✓]
   Rejection Blocks ............ [✗]    (v1.1)
   ── display ──
   Order Blocks [✓]   Midline [✓]   Mitigated [✓]

🟨 5 · FAIR VALUE GAPS
   ── logic ──
   Min size (×ATR) ............. [0.30]
   Fill rule ................... [Wick far edge ▼]  Wick far edge / Close far edge / CE
   Ignore session gaps ......... [✓]
   Inversion (IFVG) ............ [✓]
   VI [✗]  LV [✗]  BPR [✗]      (v1.1)
   ── display ──
   FVG [✓]   CE line [✓]   Shrink on fill [✓]

🎯 6 · DEALING RANGE
   Range source ................ [Swing ▼]  Swing / Internal / HTF1
   OTE band .................... [0.62] – [0.79]   Sweet spot [0.705]
   Allow developing range ...... [✓]
   ── display ──
   PD view [EQ + OTE ▼]  Off / EQ only / EQ + OTE / Full (wash)    Range gauge [✓]

⏰ 7 · SESSIONS
   Session timezone ............ [America/New_York]
   Preset ...................... [ICT (NY) ▼]   ICT (NY) / Original (UTC) / Custom
   Asia [✓] 2000-0000   London KZ [✓] 0200-0500   NY AM KZ [✓] 0700-1000
   London Close [✗] 1000-1200   NY PM [✗] 1330-1600   Silver Bullet [✗]   Judas window [✗]
   ── display ──
   Session view [Range box ▼]  Range box / Background / Off    Sessions shown [Current+3]

🌐 8 · MULTI-TIMEFRAME
   HTF1 ........................ [Auto ▼]  Auto / manual TF
   HTF2 (bias) ................. [Auto ▼]  Auto / manual / Off
   Min HTF bars ................ [100]
   ── display ──
   HTF structure [✓]   HTF OB [✓]   HTF FVG [✗]   HTF liquidity [✓]   Only unmitigated [✓]

🧩 9 · SETUPS (analytical)
   Setup engine ................ [✓]
   Models: Sweep Reversal [✓]  Continuation [✓]
   Scoring preset .............. [Balanced ▼]  Conservative / Balanced / Aggressive / Custom
   Require HTF alignment ....... [✗]    Require killzone [✗]
   Min grade to show ........... [B ▼]
   Entry [CE ▼]   SL [Beyond sweep ▼]   SL buffer (×ATR) [0.10]   (ticks) [2]
   Targets [Liquidity ▼]   Min RR [2.0]   Expiry (bars) [30]   Spread (ticks) [0]

🔔 10 · ALERTS
   Alert format ................ [Text ▼]   Text / JSON
   Events: Structure [✓]  Sweeps [✓]  Zone touch [✓]  FVG fill [✗]  Killzone [✗]
           PD/OTE [✗]  Setups [✓]  min grade [A ▼]   HTF bias [✓]
   Snapshot heartbeat (bars) ... [1]
   Sender token (optional) ..... [      ]

🛠 11 · ADVANCED
   ATR length [14]   Warm-up bars [auto]   Custom bull/bear colors [ ] [ ]
   Scoring weights (Custom preset) ...
   Debug: Show IDs [✗]  Ghost objects [✗]  Log events [✗]  Budget table [✗]
```

**Валидация (Config Resolver):** `internal < swing` (иначе swap + ⚠), `OTE low < high`, `size min < max`, HTF > chart TF (иначе авто или off + ⚠), окна сессий корректного формата. Ошибки конфигурации показываются в Ribbon (⚠ CONFIG) и в тултипе.

### 14.5 Dashboard

**Строки (Compact — первые 8, Expanded — все):**

| Строка | Пример значения | Цвет значения | Тултип |
|---|---|---|---|
| MARKET | `BULLISH` / `BEARISH` / `MIXED` / `RANGING` | bull / bear / warning / neutral | Как получен: HTF + swing + режим (A.16) |
| HTF | `4H BULLISH` (`⚠ low history`) | bull / bear | Последний HTF-сдвиг, время |
| SESSION | `LONDON KZ · 47m` / `ASIA` / `—` | neutral, KZ — bold | Окна сессий, таймзона |
| LOCATION | `DISCOUNT 36% · OTE` / `PREMIUM 71%` / `EQ` | bull / bear / neutral | Границы диапазона, состояние (developing/established) |
| LIQUIDITY | `SSL SWEPT · 3 bars` / `BSL TAKEN` / `—` | liquidity | Уровень, тег, глубина, тип свипа |
| STRUCTURE | `CHoCH ↑ · 12 bars` / `BOS ↓ · 4 bars` | bull / bear | Пробитый уровень, displacement |
| SETUP | `LONG — READY` / `SHORT — FORMING` / `— watching` | signal / muted | Модель, стадия, срок действия |
| QUALITY | `8.4 / 10 · A+  ▮▮▮▮▮▮▮▮▯▯` | грейд: A+ / A — signal, B — neutral, C — muted | Разбор факторов (§9.7) |
| TARGET *(Exp.)* | `BSL 1.0921 · 3.2R` | liquidity | Цели TP1–3 |
| INVALID *(Exp.)* | `1.0835 · close below` | bear | Условие инвалидации |
| ⚠ *(при наличии)* | `HTF FVG overhead` | warning | Список предупреждений |
| EVENTS *(Analysis)* | 5 последних событий: время, тип, цена | по типу | — |

**Правила:**
- Если сетапа нет, строки SETUP/QUALITY схлопываются в одну: `SETUP — watching SSL 1.0835`.
- В Compact используется `size.tiny`, ширина ≈ 14% области графика. В Expanded — `size.small`, ≈ 19%.
- Dashboard **никогда** не занимает правый-центральный край, где находятся последние свечи и карточка сетапа: допустимые позиции — углы. По умолчанию — top_right; если пользователь поставит middle_right, ⚠ в тултипе.
- Статистика («количество активных OB/FVG») — только в Debug (бюджет и реестр).

### 14.6 Context Ribbon

```
 HTF ▲ BULL │ STR ▲ BULL │ LON KZ 47m │ DISC 36% · OTE │ SSL ✕ 3b │ LONG READY A+
```

| Сегмент | Содержимое | Цвет | Скрывается, когда |
|---|---|---|---|
| HTF | ▲/▼/◆ + BULL/BEAR/— | bull/bear | HTF выключен |
| STR | ▲/▼ + BULL/BEAR/RANGE | bull/bear/neutral | — |
| SESSION | имя + минут до конца | neutral, KZ — bold | вне сессий |
| PD | PREM/DISC/EQ + % (+ OTE) | bear/bull/neutral | нет диапазона |
| LIQ | последнее SWEPT/TAKEN + «Nb назад» (≤ 20 баров) | liquidity | старше 20 баров |
| SETUP | направление + стадия + грейд | signal | нет сетапа (сегмент «—») |
| ⚠ | код предупреждения | warning | нет предупреждений |

Ribbon — главный носитель контекста в Clean Mode и на маленьких экранах. Позиция по умолчанию — bottom_center: внизу по центру обычно нет последних свечей и нет ценовой шкалы.

### 14.7 Smart Labels

**Цели:** не перекрывать свечи, не накладываться друг на друга, сокращаться и скрываться по значимости, единый стиль.

**Правила размещения:**

| Тип | Якорь | Почему не перекрывает свечи |
|---|---|---|
| Свинги, свипы | `yloc.abovebar` / `yloc.belowbar` бара события | Платформа ставит метку за пределами диапазона бара |
| BOS/CHoCH | середина горизонтального отрезка пробоя, сдвиг на 0.15 ATR от линии наружу | Отрезок проходит над/под свечами между свингом и пробоем |
| Теги уровней и зон | правый край (`now + 5` бара и дальше) | Справа от последнего бара свечей нет |
| Карточка сетапа | `bar_index + 3…25` (будущее) | Зона будущего свободна |
| Теги зон | внутри бокса (`box.text`) | Не накладываются на свечи (бокс позади свечей) |

**Разрешение коллизий** (на шаге Visual update):
1. Метки-кандидаты сортируются по приоритету: tier → Relevance Score → новизна.
2. Для каждой метки вычисляется прямоугольник занятости `LabelSlot` (бары × цена). Высота строки в ценах ≈ `k_label × ATR` (по умолчанию 0.35, настраивается в Advanced; при viewport-aware — по видимому диапазону цен).
3. Пересечение с уже размещённой меткой более высокого приоритета → (а) **слияние**, если метки на одном баре (`SSL ✕ · CHoCH↑`); (б) сдвиг на одну высоту строки наружу от цены (не более 2 сдвигов); (в) скрытие с переносом текста в тултип победившей метки.
4. **Стопка правых тегов**: теги уровней сортируются по цене. Если соседние ближе одной высоты строки, теги объединяются (`BSL ≡3 · ◆PDH`) или разносятся по оси X (+6 баров).

**Уровни детализации текста:**

| Уровень | Пример | Где |
|---|---|---|
| L0 Icons | `▲` · `✕` | Clean (minor), сильный zoom out |
| L1 Short (по умолч.) | `CHoCH↑` · `SSL ✕` · `OB` | Normal |
| L2 Standard | `CHoCH↑ 1.0873` · `◆4H OB` | Normal (Tier 1) |
| L3 Full | `MSS↑ swing · 1.8 ATR` | Analysis |
| Tooltip | полное описание: тип, уровень, время, цена, displacement, причина, ID (Debug) | Всегда |

### 14.8 Setup Visualization (композиция)

Сетап — **единая композиция**, визуально родственная инструменту Long/Short Position TradingView: трейдер узнаёт её без обучения.

```
                        x0 = бар READY          x1 = x0 + 20 баров (≤ 500)
                        │                       │
             ─ ─ ─ ─ ─ ─┼─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤ TP2 1.08655 · 3.2R    (dashed, reward)
                        │                       │
                        │     REWARD (fill.faint, c.reward)
             ─ ─ ─ ─ ─ ─┼─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤ TP1 1.08560 · 1.9R
                        │                       │
             ━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━┥ E 1.08421          ◀ LONG · A+ 8.4
                        │▓▓▓ ENTRY ZONE (POI) ▓▓│                     Sweep → CHoCH → FVG → OTE
                        │▓▓▓  fill.focus      ▓▓│                     RR 1:3.2 · SL 0.9 ATR
                        │     RISK (fill.faint, c.risk)
             ━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━┥ SL 1.08349 · INV close below 1.08361
```

**Элементы:**

| Элемент | Токены | Обязателен |
|---|---|:---:|
| Entry-зона (POI) | box `c.signal` @ `fill.focus`, контур `op.medium` | ✅ |
| Entry-линия | `ln.entry`, `c.signal` | ✅ |
| SL-линия | `ln.sl`, `c.risk` | ✅ |
| TP1…TP3 | `ln.tp`, `c.reward`, тег справа `TP1 · 1.9R` | ✅ (сколько есть) |
| Reward / Risk боксы | `fill.faint` | Normal+: ✅. Clean: только линии |
| Карточка | label, panel-фон: строка 1 **bold** `LONG · A+ 8.4`; строка 2 — цепочка; строка 3 — RR и SL в ATR | ✅ |
| Линия инвалидации | `ln.inv`, только если отличается от SL | опц. |

**Состояния композиции:**

| Стадия | Визуал |
|---|---|
| FORMING | Только контур POI (dashed, `c.signal` @ `op.soft`) + карточка muted `LONG — FORMING · Sweep → CHoCH`. Без SL/TP |
| READY | Полная композиция, заливки как в таблице |
| TRIGGERED / ACTIVE | Маркер `●` на баре входа. Композиция продолжается вправо. Достигнутые TP: `TP1 ✓`, линия → `op.faint` |
| TP2/TP3 / CLOSED (win) | Карточка `✓ +3.2R`, композиция → `op.faint`. Clean: скрыть через 10 баров, Normal: через 30 |
| SL / INVALIDATED | Композиция → `c.invalid` @ `fill.ghost`, карточка `✕ INVALID · close below 1.08361`. Clean: скрыть через 5 баров |
| EXPIRED / MISSED | Пунктирный серый контур, `⌛ EXPIRED` / `MISSED`. Clean: скрыть сразу |

**Ограничения:** одновременно на графике — не более 1 активной композиции на направление (Clean/Normal). Прошлые сетапы — только Analysis (до 10, в затухшем виде с итогом ✓/✕ — для обучения и проверки воспроизводимости).

### 14.9 Entry / SL / TP: требования к визуализации

| Требование | Реализация |
|---|---|
| Читаемость с первого взгляда | Entry и SL — толщина 2, solid. TP — 1, dashed. Подписи справа с ценой и R |
| Различимость без цвета | E — solid + `E`; SL — solid + `SL`; TP — dashed + `TP1`; INV — dotted + `INV` |
| Цены на ценовой шкале | Опция «Price-scale markers»: служебные plot'ы E/SL/TP с `display.price_scale` (значение `na`, когда сетапа нет) |
| v1.0 | Только для аналитических/демо-сетапов. Карточка содержит пометку `ANALYTICAL` в тултипе |
| v2.0 | Те же элементы, но из TradePlan (rev, состояние исполнения от шлюза — если вернётся через ручной ввод/вне Pine) |

### 14.10 Визуальные изменения состояний

| Объект | Состояние | Визуал |
|---|---|---|
| **OB** | Fresh | dir @ `fill.base`, контур solid `op.medium`, тег `OB` |
|  | Touched | `fill.light`, контур `op.soft` |
|  | Mitigated | hue → `c.mitigated`, `fill.faint`, контур dotted, тег `OB·m` (Analysis) |
|  | Broken → Breaker | новая зона: новый hue, `fill.light`, контур **dashed**, тег `BB` |
|  | Broken → Mitigation Block | новая зона: новый hue, `fill.faint`, контур dotted, тег `MB` |
|  | Invalidated | `c.invalid` @ `fill.ghost` → скрыть через TTL (Clean 0, Normal 10, Analysis 50 баров) |
|  | Expired | Скрыта (Debug — ghost) |
| **FVG** | Open | dir @ `fill.light`, CE dotted |
|  | Partial | Опция «Shrink on fill»: бокс сжимается до незаполненного остатка, заполненная часть → `fill.ghost` |
|  | CE reached | CE-линия → `op.faint` |
|  | Filled | Скрыта (Analysis — ghost 20 баров) |
|  | Inverted (IFVG) | Новая зона: новый hue, контур dashed, тег `IFVG` |
| **Liquidity** | Active major | solid, `op.strong`, тег `BSL ≡3` / `◆PDH` |
|  | Active minor | dotted, `op.faint`, без тега (Normal), скрыта (Clean) |
|  | Pending reclaim | dashed, тег `BSL ?` |
|  | Swept | линия обрывается на баре свипа, `op.faint` dotted, маркер `✕` + метка `BSL ✕` (major — T1 bold) |
|  | Taken | обрыв без маркера, `op.faint`. Clean — скрыть сразу |
| **Structure** | Последний swing BOS/CHoCH | `op.strong`, метка L2 |
|  | Предыдущие 1–2 | `op.soft`, метка L1 |
|  | Более старые | Скрыты (Clean/Normal), `op.faint` (Analysis) |
|  | Internal | dotted tiny, только Analysis (Normal — последний iCHoCH, если он часть сетапа) |
| **Dealing range** | Developing | EQ и границы dashed, тег `EQ~` |
|  | Established | EQ dotted, границы solid-риски |
| **Setup** | см. §14.8 | |

### 14.11 MTF Visual Language

| Атрибут | HTF | LTF (chart) |
|---|---|---|
| Толщина линий/контуров | 2 px | 1 px |
| Заливка зон | плотнее на 5–8 пунктов (`fill.strong`) | `fill.base` / `fill.light` |
| Контур зон | всегда есть, solid | у OB — тонкий, у FVG — нет |
| Метки | `size.small` **bold**, префикс `◆4H` | `size.small`/`tiny`, без префикса |
| Z-порядок | ниже LTF (фон-контекст) | поверх HTF (уточнение) |
| Правило вложенности | LTF-зона того же направления внутри HTF-зоны → в Clean/Normal LTF скрыта, HTF получает бейдж `+LTF` | В Analysis видны обе: LTF — «refinement» |
| HTF-события | метка `◆4H CHoCH↑` в точке закрытия HTF-бара (на LTF-графике) | — |
| HTF key levels | `◆D PDH`, `◆W PWL` — solid 2 px, `c.liquidity` | — |

Пользователь отличает HTF-объект от LTF по **трём** независимым признакам: толщина, ◆-префикс, плотность. Цвет для этого не используется.

### 14.12 Визуализация ликвидности

| Класс | Правило отбора | Визуал |
|---|---|---|
| **Major** | HTF-уровень, Key Level, EQ ≥ 2, swing-уровень возрастом ≥ `oldAge` | solid, `op.strong`, тег |
| **Minor** | internal-уровень, свежий одиночный swing | dotted, `op.faint`, без тега. «Reduce Minor Liquidity» → только 1 ближайший на сторону |
| **Swept** | состояние SWEPT | обрыв + `✕` + метка (major) |
| **Active** | ACTIVE и в окне видимости | чёткая линия до правого края |

**Ограничение плотности:** по умолчанию ≤ 2 major + 1 minor на сторону (Normal), ≤ 1 major на сторону + Key Levels (Clean).

**Draw on Liquidity (опция Analysis):** пунктирная стрелка `ln.path` от текущей цены к ближайшей major-цели в направлении bias. В Clean и Normal цель показывается текстом в Dashboard (`TARGET`).

### 14.13 Dealing Range UX

| PD view | Что рисуется |
|---|---|
| Off | Ничего (Ribbon/Dashboard по-прежнему показывают PD) |
| **EQ only** | EQ-линия dotted neutral + тег `EQ` |
| **EQ + OTE** (по умолч.) | + OTE-полоса `c.signal` @ `fill.faint` (только в «торговой» половине диапазона) + dotted-линия 0.705 |
| Full (wash) | + Premium/Discount фоном `fill.wash` в пределах диапазона (не на весь график) |

**Range Gauge.** Вертикальная шкала справа от последнего бара (x = bar + 2): линия от low до high диапазона, риски `0` / `EQ` / `1`, OTE-отрезок толще, треугольник `◀` на уровне текущей цены. Отвечает на вопрос 7 без заливки фона. Занимает 3 линии и 1 метку.

### 14.14 Сессии / Killzones UX

- **Range box** (по умолч.): прямоугольник от high до low сессии на её интервале. v0.2: цвет каждой сессии задаётся в настройках, рамка того же цвета плотнее (текущая — solid, прошлые — dashed), название `LON KZ` / `NY KZ` / `ASIA` — **над** максимумом сессии, чтобы не перекрывать свечи. Сам диапазон сессии — информация о ликвидности (AH/AL).
- **Background**: `bgcolor` только для *текущей* сессии и только `fill.wash`. Исторические сессии фоном не рисуются.
- **Silver Bullet**: узкий бокс высотой с диапазон окна, контур dashed, тег `SB`.
- **Judas window**: первые 60 минут KZ — dashed-подчёркивание range box (без отдельной заливки).
- Количество: Clean — только текущая, Normal — текущая + 3, Analysis — 20.

### 14.15 Accessibility

| Аспект | Решение |
|---|---|
| Дальтонизм (протан/дейтеран) | CVD-палитра (§13.3.2). В любой палитре направление дублируется стрелками ↑↓ и позицией (над/под ценой) |
| Тританопия | Signal (сине-фиолетовый) отличается от liquidity и формой (композиция/линии entry) |
| Низкий контраст / проекторы | Mono+ (v1.1). Текст всегда от `chart.fg_color` |
| Не только цвет | Все критичные смыслы дублируются стилем линии, символом и текстом (DS-7, §13.11) |
| Маленькие экраны и мобильное приложение | Dashboard Compact или выключен, Ribbon включён. Метки L1. Ширина ячеек таблиц — в % области |
| 4K / высокая плотность | Толщина ≤ 2 px, размеры текста — константы платформы, масштабируются системой |
| Много свечей / zoom out | Авто-сокращение меток до L0 при viewport-aware. Иначе History depth и бюджеты держат плотность (VAC-14) |
| Zoom in | Теги зон в боксах появляются, когда высота бокса ≥ 0.35 ATR (иначе тег уходит в тултип) |
| Когнитивная нагрузка | Режимы, Tier-иерархия, единый словарь сокращений, тултипы со смыслом |

### 14.16 UX Performance

| Правило | Реализация |
|---|---|
| Logical ≠ Visual update | §4.5: логика — на подтверждённых барах; визуал — один полный проход + инкременты |
| Не пересоздавать неизменившееся | `renderHash` в `ViewHandle`. Нет изменений → нет `set_*` |
| Object reuse | Пулы по слоям. `new` — только при росте пула до бюджета |
| Дешёвый live-слой | На тиках обновляются ≤ 10 объектов: Ribbon (PD %), Gauge-маркер цены, прогресс сетапа |
| Ранжирование только на баре закрытия | Relevance Score пересчитывается при подтверждении бара, не на тике (заодно убирает мерцание) |
| Без визуала на истории | Исторические бары рисуют ноль объектов |
| Профилирование | Pine Profiler: бюджет Visual ≤ 25% времени расчёта, Logic ≤ 70% |

### 14.17 Правила Price Action First

| # | Правило | Проверка |
|---|---|---|
| PA-1 | Ни одна заливка не плотнее `fill.focus` (transp 70) | Ревью токенов |
| PA-2 | Все drawings — позади свечей (`behind_chart`) | Визуальный тест |
| PA-3 | Метки не ставятся внутрь диапазона high–low свечи | §14.7, VAC-20 |
| PA-4 | Фоновые заливки (wash) по умолчанию выключены. Одновременно ≤ 1 wash-слой | Режимы |
| PA-5 | В Normal в видимой области ≤ 12 боксов, ≤ 14 линий уровней, ≤ 15 меток | VAC-1 |
| PA-6 | `barcolor` не используется ни в одном режиме, кроме опции Analysis «displacement candles» (только контурный маркер) | Ревью |
| PA-7 | Dashboard — только в углах, Compact по умолчанию | §14.5 |
| PA-8 | Будущее (справа от последнего бара) — для меток, тегов и сетапа | §14.7 |

---

## 15. Anti-Clutter System

### 15.1 Механизмы

| # | Механизм | Как работает | Параметр (по умолч.) |
|---|---|---|---|
| AC-M1 | **Глобальные лимиты** | Бюджет по категориям и режимам (§4.10) | таблица режимов |
| AC-M2 | **Nearest-N на сторону** | Для каждой категории — не более N объектов над ценой и N под ценой (ранжирование по R) | Clean 1, Normal 2, Analysis 6 |
| AC-M3 | **Окно дистанции** | Объекты дальше `Dmax × ATR` от цены не показываются (кроме HTF Key Levels и целей активного сетапа) | Clean 3, Normal 6, Analysis 12 ATR |
| AC-M4 | **Затухание по возрасту** | Freshness `F = 0.5^(age / halfLife)` уменьшает R, а значит плотность | halfLife 150 баров chart TF / 50 HTF-баров |
| AC-M5 | **Скрытие по состоянию** | Mitigated / Filled / Invalidated / Swept / Taken — TTL отображения по режиму | §14.10 |
| AC-M6 | **Слияние зон** | Зоны одного kind и направления с перекрытием ≥ 50% меньшей → одна визуальная зона (union), тег `OB×2`. FVG внутри OB того же направления → OB с бейджем `+FVG`, отдельный FVG-бокс не рисуется | overlap 0.5 |
| AC-M7 | **Кластеризация уровней** | Уровни ликвидности одной стороны ближе `0.15 × ATR` → одна линия с тегом `≡n` или объединённым тегом `BSL · ◆PDH` | 0.15 ATR |
| AC-M8 | **HTF-доминирование** | LTF-зона внутри HTF-зоны того же направления скрыта (Clean/Normal), HTF получает бейдж `+LTF` | HTF Priority ✓ |
| AC-M9 | **Активное важнее исторического** | Активные (FRESH/OPEN/ACTIVE) получают `A = 1`, исторические ≤ 0.4 | §16.2 |
| AC-M10 | **Бюджет меток + коллизии** | §14.7: слияние, сдвиг, скрытие в тултип | — |
| AC-M11 | **Дисциплина правого края** | Зоны и уровни заканчиваются на общей вертикали `now + 5`. Никаких бесконечных `extend.right` | 5 баров |
| AC-M12 | **Глубина истории** | Объекты, рождённые раньше `History depth` баров назад, не рисуются (кроме активных HTF-уровней) | Clean 500, Normal 1500, Analysis 5000 |
| AC-M13 | **Гистерезис** | Объект появляется при `R ≥ θ`, исчезает при `R < θ − 0.05`. Ранжирование — только на закрытии бара | δ = 0.05 |
| AC-M14 | **Затухание событий** | Метки BOS/CHoCH: последнее — L2, 2 предыдущих — L1 с `op.soft`, остальные скрыты (Clean/Normal) | 3 события |
| AC-M15 | **Pinning сетапа** | Объекты цепочки активного сетапа закреплены (R = max(R, 0.95)) — никогда не скрываются бюджетом | — |
| AC-M16 | **Visible range (v0.2, по умолчанию)** | Рисуется видимая часть графика. Окно делится на временные сегменты (до 6 × ~150 баров), каждый ранжирует объекты относительно своего close/ATR, поэтому плотность одинакова по всему экрану. Завершённые объекты берутся из архива. «Recent only» — поведение v0.1 | On |

### 15.2 Порядок применения (конвейер Visual update)

```
Registry snapshot
   → 1. Фильтр по режиму и тумблерам (ADR-09)
   → 2. Фильтр по глубине истории и окну дистанции (M3, M12)
   → 3. Визуальное слияние и кластеризация (M6, M7) → «визуальные объекты»
   → 4. HTF-доминирование (M8)
   → 5. Relevance Score каждого визуального объекта (§16) + pinning (M15)
   → 6. Ранжирование и отбор: Nearest-N на сторону (M2) → бюджет категории (M1)
   → 7. Гистерезис относительно предыдущего кадра (M13)
   → 8. Маппинг R → RenderSpec (прозрачность, толщина, текст) (§16.4)
   → 9. Раскладка меток (M10)
   → 10. Применение к пулам с dirty-check
```

### 15.3 Сводка лимитов по режимам

| Параметр | Clean | Normal | Analysis | Debug |
|---|---:|---:|---:|---:|
| Зон на сторону (на категорию) | 1 | 2 | 6 | все в бюджете |
| Major-ликвидность на сторону | 1 | 2 | 6 | все |
| Minor-ликвидность на сторону | 0 | 1 | 4 | все |
| Структурных событий с меткой | 1 | 3 | 15 | все |
| Окно дистанции, ATR | 3 | 6 | 12 | ∞ |
| Порог показа θ | 0.55 | 0.40 | 0.25 | 0 (ghost < 0.25) |
| TTL отработанного, баров | 0 | 10 | 50 | ∞ |
| Глубина истории, баров | 500 | 1500 | 5000 | вся |

---

## 16. Visual Priority System

### 16.1 Relevance Score

Для каждого визуального объекта `o`:

```
R(o) = Σ wᵢ(kind) · cᵢ(o)   /   Σ wᵢ(kind)          (0 ≤ R ≤ 1)
если o ∈ цепочке активного сетапа:  R = max(R, 0.95)   (pinning)
```

### 16.2 Компоненты (все нормированы в 0..1)

| Компонент | Обозн. | Формула / таблица |
|---|---|---|
| HTF relevance | H | chart TF 0.5 · HTF1 0.85 · HTF2 1.0 · Key Level D 0.9 · W 1.0 |
| Proximity | P | Внутри зоны / на уровне → 1. Иначе `max(0, 1 − d / Dmax)`, d — расстояние до ближайшей границы в ATR, Dmax по режиму (§15.3) |
| Freshness | F | `0.5^(age / halfLife)`, age — в барах соответствующего TF |
| Activity | A | FRESH/OPEN/ACTIVE 1.0 · TOUCHED/PARTIAL/PENDING 0.7 · CE_REACHED 0.6 · BREAKER/MB/IFVG (fresh) 0.8 · MITIGATED 0.4 · SWEPT/TAKEN 0.3 · FILLED/INVALIDATED 0.1 |
| Confirmation strength | S | Зоны: `min(1, dispStrength / 2.5)`·0.6 + `min(1, size/ATR / 1.5)`·0.2 + `min(1, volRatio / 2)`·0.2 (без объёма — веса перераспределяются). События: `min(1, disp / 2)` |
| Liquidity importance | L | Уровни: `0.4·isMajor + 0.3·min(1, (touches−1)/3) + 0.3·min(1, age/oldAge)`. Key Level → 1 |
| Setup relevance | U | В цепочке активного сетапа 1.0 · в кандидате (FORMING) 0.6 · иначе 0 |

### 16.3 Веса по видам

| Вид | H | P | F | A | S | L | U |
|---|---:|---:|---:|---:|---:|---:|---:|
| OB / BB / MB | 0.20 | 0.25 | 0.15 | 0.15 | 0.15 | — | 0.10 |
| FVG / IFVG | 0.15 | 0.30 | 0.20 | 0.15 | 0.10 | — | 0.10 |
| Уровень ликвидности | 0.20 | 0.25 | 0.05 | 0.15 | — | 0.25 | 0.10 |
| Структурное событие | 0.25 | 0.10 | 0.35 | — | 0.20 | — | 0.10 |
| Сессия | — | 0.20 | 0.60 | 0.20 | — | — | — |
| S&D / VI / LV / BPR | 0.15 | 0.30 | 0.25 | 0.15 | 0.15 | — | — |

### 16.4 Маппинг R → визуальные свойства

| Класс | R (Normal) | Показ | Прозрачность | Толщина | Метка |
|---|---|---|---|---|---|
| **Prominent** | ≥ 0.75 | ✅ | базовый токен | по TF (HTF 2) | L2 (Tier 1 — bold) |
| **Standard** | 0.55–0.75 | ✅ | база + 4 | по TF | L1 |
| **Subdued** | 0.40–0.55 | ✅ | база + 8, контур → dotted | 1 | нет (только тултип у соседей) |
| **Hidden** | < 0.40 | ❌ (Debug: ghost) | — | — | — |

**Смещения по режиму:** Clean — все границы +0.15 (Subdued фактически исключён). Analysis — −0.15. Debug — показываются все, скрытые — `fill.ghost` + подпись `R=0.32`.

**Сокращение метки:** если для метки нет места после 2 сдвигов (§14.7), уровень текста понижается на 1 (L2 → L1 → L0), затем метка скрывается.

### 16.5 Примеры расчёта

**HTF OB 4H, fresh, 1.5 ATR от цены, возраст 40 баров (halfLife 150), displacement 2.0 ATR, вне сетапа (Normal):**
H = 0.85, P = 1 − 1.5/6 = 0.75, F = 0.5^(40/150) ≈ 0.83, A = 1.0, S ≈ 0.6·0.8 + 0.2·0.67 + 0.2·0.75 ≈ 0.76, U = 0.
R = 0.20·0.85 + 0.25·0.75 + 0.15·0.83 + 0.15·1.0 + 0.15·0.76 + 0.10·0 ≈ 0.170 + 0.188 + 0.125 + 0.150 + 0.114 = **0.746 → Standard** (на границе с Prominent: при приближении цены ещё на 0.1 ATR объект станет Prominent, гистерезис не даст ему мигать на границе).

**LTF FVG, partial, 4 ATR от цены, возраст 200 баров, размер 0.5 ATR:**
H = 0.5, P = 0.33, F ≈ 0.40, A = 0.7, S ≈ 0.08 (displacement 0; size 0.5/1.5 = 0.33; вес объёма перераспределён на size), U = 0.
R = 0.15·0.5 + 0.30·0.33 + 0.20·0.40 + 0.15·0.7 + 0.10·0.08 ≈ 0.075 + 0.099 + 0.080 + 0.105 + 0.008 = **0.37 → Hidden** в Normal (θ = 0.40), Subdued в Analysis (θ = 0.25).

**Major SSL (EQL ×3), 0.8 ATR, возраст 60 баров, в цепочке активного сетапа:** pinning → **R = 0.95**, всегда видна.

### 16.6 Правила целостности

1. R вычисляется **только** в Visual Engine и **никогда** не читается ядром (ADR-11).
2. R не влияет на lifecycle объекта: скрытая зона продолжает жить и может стать POI сетапа (после этого её R поднимается pinning'ом).
3. При равенстве R: HTF > LTF → активное > историческое → ближе к цене → новее.

---

## 17. Analysis Mode

**Назначение:** позволить трейдеру **визуально воспроизвести логику** индикатора — увидеть цепочку `Liquidity → Sweep → Displacement → CHoCH/BOS → OB/FVG → Retracement → OTE → Entry → SL/TP` и понять, почему сетап появился (или не появился).

### 17.1 Что добавляется к Normal

| Элемент | Описание |
|---|---|
| Internal structure | `iBOS` / `iCHoCH` (dotted, tiny), HH/HL/LH/LL |
| История ликвидности | Снятые и забранные уровни за глубину истории (тусклые, с ✕) |
| Все зоны в окне 12 ATR | Включая mitigated (`c.mitigated`) и refinement внутри HTF |
| Displacement | Контурные маркеры над/под свечами ноги displacement (не `barcolor`) |
| **Setup Path** | Маркеры ①…⑨ в точках событий цепочки (§17.2) |
| **Event Timeline** | Dashboard Expanded + строки EVENTS (последние 8 событий) |
| Прошлые сетапы | До 10 затухших композиций с итогом ✓ / ✕ / ⌛ |
| Метки L3 | `MSS↑ swing · 1.8 ATR`, `SSL ✕ EQL×3 · 0.18 ATR` |
| Draw on Liquidity | Пунктирная стрелка к ближайшей major-цели |
| Альтернативный POI | Контур второго POI (dotted) с тегом `alt` |

### 17.2 Setup Path

```
   ④ FVG ──────► ⑤ OTE ─────► ⑥ E ● ─────► TP1 ✓
      ▲
   ③ CHoCH↑ (MSS)
      ▲
   ② disp 1.8 ATR
      ▲
   ① SSL ✕ (EQL×3)
```

- Маркеры — текстовые метки с номером шага в точке события (бар, цена).
- Соединения — `ln.path` (dotted, `c.signal` @ `op.soft`, стрелка на конце), от шага k к шагу k+1. Альтернатива (спайк S-6) — одна polyline на сетап.
- Номера и подписи берутся **только** из `Setup.chain` (§9.2), то есть из реальных `causeId`. Path не «досочиняет» логику.
- Тултип маркера: событие, время, цена, вклад в скоринг.

### 17.3 Focus / Inspect

- **Focus latest setup** (по умолч. в Analysis): объекты вне цепочки последнего сетапа приглушаются (+8 прозрачности), цепочка — в Prominent.
- **Inspect at time:** `input.time(..., confirm = true)` — пользователь кликает на график, выбирая момент. Analysis показывает сетап, ближайший к выбранному времени, его цепочку и разбор, а также «почему нет сетапа» (§19.1), если сетапа не было. Повторный выбор — через настройки.

### 17.4 Чего Analysis Mode **не** делает

Не меняет детекторы, пороги и скоринг. Не показывает Debug-информацию (ID, R, бюджеты). Не включает `barcolor`.

---

## 18. Clean Mode

**Назначение:** исполнение и быстрое чтение рынка. «Пять секунд на понимание».

### 18.1 Состав

| Показывается | Ограничение |
|---|---|
| HTF bias | Ribbon + ◆HTF Key Levels (≤ 2) |
| Последний swing BOS/CHoCH | 1 событие, метка L1 |
| Ключевая ликвидность | 1 major на сторону + ◆PDH/PDL (если в окне 3 ATR) |
| Снятая ликвидность | Только последний major-свип, ≤ 20 баров |
| Актуальные OB/FVG | 1 на сторону (после слияния и HTF-доминирования) |
| Dealing range | EQ only (OTE — только если есть активный сетап) |
| Сессия | Только Ribbon (range box текущей сессии — опционально) |
| Активный сетап | Композиция без reward/risk-боксов: entry-зона, E/SL/TP-линии, карточка |
| Context Ribbon | ✅ |
| Dashboard | ❌ (контекст несёт Ribbon; режим — потолок видимости, ADR-09. Для Dashboard на чистом графике — режим Custom) |

### 18.2 Не показывается

Internal-структура, HH/HL, minor-ликвидность, mitigated/filled/invalidated-объекты, история сессий, Premium/Discount-фон, S&D/VI/LV/BPR, прошлые сетапы, Setup Path, Debug.

### 18.3 Бюджет

≤ 13 боксов / 20 линий / 10 меток (§4.10). Ориентир по плотности — ≤ 8 одновременно видимых «смысловых» объектов при отсутствии сетапа.

### 18.4 Normal Mode (Detailed) — для сравнения

Normal = Clean + 2 зоны на сторону + 2 major + 1 minor уровень на сторону + 3 последних структурных события + OTE + range box сессий (текущая + 3) + reward/risk-боксы сетапа + Dashboard Compact + Range Gauge.

---

## 19. Debug Mode

**Назначение:** разработка, QA, поддержка пользователей. Не влияет на логику (T-1) и никогда не включён по умолчанию.

### 19.1 Возможности

| Функция | Описание |
|---|---|
| ID и состояния | Debug-аннотации у объектов: `#Z142 OB FRESH R=0.71`, monospace, tiny |
| Ghost-объекты | Скрытые приоритетом объекты рисуются `fill.ghost` с подписью `R` и причиной скрытия (`dist`, `budget`, `htf-dominated`, `merged→#Z140`) |
| Budget table | Таблица (позиция middle_left): использовано / бюджет по категориям; размеры реестров; событий на баре; HTF-баров в буфере; `isWarm` |
| Effective config | Эффективные значения после профиля (что разрешил режим, что скрыл пользователь) |
| `log.info` поток | CSV-строки событий: `key,type,dir,price,ref,cause,v1,v2,v3,s1` — для сравнения с golden-журналами (§27) |
| Ассерты (`log.error`) | Инварианты: `top > bottom`, нет дублей ID, допустимые переходы автоматов, бюджеты не превышены, нет событий на неподтверждённом баре |
| «Почему нет сетапа» | Для последнего свипа/сдвига: какой guard не прошёл (`NO_SHIFT_IN_WINDOW`, `POI_IN_PREMIUM`, `RR_BELOW_MIN`, `SL_TOO_WIDE`, `GRADE_BELOW_MIN`, `WARMUP`) |
| Data health | Объём (есть/нет), тип графика, HTF-глубина, авто-HTF, таймзона сессий |
| Профилирование | Инструкция: Pine Profiler, бюджеты времени по модулям (§14.16) |

### 19.2 Матрица режимов

| Элемент | Clean | Normal | Analysis | Debug |
|---|:---:|:---:|:---:|:---:|
| Context Ribbon | ✅ | ✅ | ✅ | ⬜ (заменён Debug-таблицей, опц.) |
| Dashboard | ⬜ | Compact | Expanded + Events | Expanded + Budget |
| HTF bias / ◆Key Levels | ✅ | ✅ | ✅ | ✅ |
| Swing BOS/CHoCH | последний | 3 последних | 15 | все |
| Internal structure | ❌ | ❌ (кроме цепочки сетапа) | ✅ | ✅ |
| Swing labels HH/HL | ❌ | ❌ | ✅ | ✅ |
| Major liquidity | 1/сторону | 2/сторону | 6/сторону | все |
| Minor liquidity | ❌ | 1/сторону | 4/сторону | все |
| Sweep markers | последний major | major + последние minor | все | все |
| OB / FVG | 1/сторону | 2/сторону | 6/сторону | все |
| Breaker / MB / IFVG | при R ≥ θ | ✅ | ✅ | ✅ |
| Mitigated / filled | ❌ | TTL 10 | TTL 50 | ghost |
| PD view | EQ only | EQ + OTE | EQ + OTE | Full |
| Range Gauge | ❌ | ✅ | ✅ | ✅ |
| Sessions | Ribbon | текущая + 3 | 20 | 30 |
| Active setup | без боксов R/R | полная композиция | полная + alt POI | полная + guards |
| Setup Path | ❌ | ❌ | ✅ | ✅ |
| Прошлые сетапы | ❌ | ❌ | до 10 | до 10 |
| Метки | L1 | L1/L2 | L3 | L3 + ID |
| Ghost / R / ID | ❌ | ❌ | ❌ | ✅ |
| `log.*` | ❌ | ❌ | ❌ | опц. |
