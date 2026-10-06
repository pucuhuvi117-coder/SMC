# 04 · Visual Design System

> Покрывает результат анализа **№13**.
> Документ — **единственный источник** визуальных решений. Рендереры не содержат «магических» цветов, прозрачностей и размеров: только токены отсюда (модуль `60_visual_tokens`).

---

## 13. Visual Design System

### 13.1 Принципы

| # | Принцип | Следствие |
|---|---|---|
| DS-1 | **Price Action First** | Свечи — самый контрастный элемент графика. Заливки зон всегда прозрачнее тел свечей. Ничего не рисуется поверх свечей непрозрачно |
| DS-2 | **Цвет = смысл** | Hue кодирует *направление* (bull / bear / neutral) и несколько *ролей* (ликвидность, сигнал, предупреждение, отработанное). Модули не получают «свой» цвет |
| DS-3 | **Форма = тип** | OB, FVG, S&D, Breaker различаются формой (заливка/контур/стиль границы), а не оттенком |
| DS-4 | **Прозрачность = состояние × релевантность** | Свежее и важное — плотнее, отработанное и далёкое — прозрачнее |
| DS-5 | **Толщина = таймфрейм и tier** | HTF и Tier 1 толще, LTF и Tier 3 тоньше |
| DS-6 | **Текст — только когда нужен** | Короткие метки (≤ 10 символов), подробности — в тултипе, Dashboard, Analysis Mode |
| DS-7 | **Не только цвет** | Каждый смысл, переданный цветом, дублируется формой, стилем линии, стрелкой или символом (доступность) |
| DS-8 | **Ограниченная палитра** | В Normal одновременно видны не более 5 hue: bull, bear, neutral, liquidity, signal (+ warning только в UI-панелях) |

### 13.2 Матрица визуального кодирования

| Канал | Что кодирует | Значения |
|---|---|---|
| **Hue** | Направление и роль | bull · bear · neutral · liquidity · signal · warning · mitigated · invalid |
| **Форма** | Тип сущности | линия (структура, уровни) · заливка+контур (OB) · заливка без контура (FVG) · контур без заливки (S&D) · пунктирный контур (Breaker/IFVG) · мягкий фон (PD, сессии) · композиция (Setup) |
| **Прозрачность** | Состояние × релевантность | шкала `op.*` / `fill.*` (§13.5) |
| **Стиль линии** | Степень подтверждения и роль | solid = подтверждённое/ключевое · dashed = структурный пробой, конверсия, проекция · dotted = второстепенное, середины (CE/EQ), снятое, формирующееся |
| **Толщина** | TF и tier | 1 px — LTF, Tier 2–3 · 2 px — HTF, Tier 1 (Entry/SL, HTF-уровни) |
| **Размер текста** | Tier и TF | tiny · small · normal (§13.7) |
| **Начертание** | Критичность | **bold** — только Tier 1 |
| **Символы** | Тип события и направление | ↑ ↓ ✕ ◆ ≡ ⚠ ✓ ⌛ ①–⑨ (§13.11) |
| **Позиция** | Время и роль | события — в точке события · теги уровней — у правого края · карточка сетапа — справа от последнего бара |

### 13.3 Цветовые токены

#### 13.3.1 Палитра Standard (по умолчанию)

| Токен | Dark | Light | Смысл и применение |
|---|---|---|---|
| `c.bull` | `#22AB94` | `#089981` | Бычье направление: BOS↑/CHoCH↑, бычьи OB/FVG/BB, Discount-тон, TP (reward) |
| `c.bear` | `#F7525F` | `#F23645` | Медвежье направление: BOS↓/CHoCH↓, медвежьи зоны, Premium-тон, SL (risk) |
| `c.neutral` | `#8C909C` | `#6B7080` | EQ, сессии, второстепенные линии, внутренняя структура |
| `c.liquidity` | `#E3B341` | `#A86F00` | Пулы ликвидности BSL/SSL, Key Levels, маркер свипа |
| `c.signal` | `#4C8DFF` | `#2962FF` | Сетап: entry-зона, entry-линия, OTE, карточка, Setup Path |
| `c.warning` | `#FF9F1A` | `#E65100` | Предупреждения ⚠ — **только** в Ribbon, Dashboard и карточке сетапа |
| `c.mitigated` | `#9C83D6` | `#7B5CC4` | Состояние «отработано» (mitigated OB) — приглушённо |
| `c.invalid` | `#5A5E6A` | `#B8BBC4` | Invalidated / expired / swept history — цвет, близкий к фону |
| `c.text` | `chart.fg_color` | `chart.fg_color` | Основной текст (адаптивно) |
| `c.text.muted` | `chart.fg_color` @ op 45 | `chart.fg_color` @ op 45 | Ключи Dashboard, второстепенные подписи |
| `c.panel.bg` | `#1E222D` | `#F0F3FA` | Фон Dashboard/Ribbon/карточек (с `fill.panel`) |
| `c.panel.border` | `#2A2E39` | `#D1D4DC` | Рамка панелей |

**Производные токены:**

| Токен | Определение | Комментарий |
|---|---|---|
| `c.reward` | = `c.bull` | TP-линии и reward-бокс. Конвенция Long/Short Position tool TradingView |
| `c.risk` | = `c.bear` | SL-линия, risk-бокс |
| `c.premium` | = `c.bear` @ `fill.wash` | Очень мягкий тон, по умолчанию выключен |
| `c.discount` | = `c.bull` @ `fill.wash` | То же |
| `c.breaker` | = hue **новой** полярности | Отличие формой: dashed-контур + тег `BB`. Отдельный hue не вводится (DS-2) |
| `c.htf` | = hue объекта, прозрачность −5…−8, толщина 2, тег `◆4H` | HTF — модификатор, а не цвет (§14.11) |
| `c.ltf` | = hue объекта, прозрачность +3…+5, толщина 1 | Модификатор |
| `c.session.asia/london/ny` | v0.2: собственные цвета из настроек (по умолчанию Asia `#7E57C2`, London `#2962FF`, NY `#FF9800`, прозрачность 86), рамка — тот же цвет плотнее | В v1-проекте сессии были нейтральными; на практике их почти не было видно, поэтому цвет вынесен в настройки |

> **Почему BSL/SSL не красные/зелёные** (в отличие от ТЗ §5.3): ликвидность — это *цель*, а не направление. Красный BSL над ценой читается как «сопротивление/медвежье» и противоречит смыслу (BSL — цель лонгов). Единый `c.liquidity` + тег `BSL`/`SSL` + позиция (над/под ценой) снимают противоречие.

#### 13.3.2 Палитра Color-blind safe (CVD, на базе Okabe–Ito)

| Токен | Dark | Light | Замена |
|---|---|---|---|
| `c.bull` | `#56B4E9` (sky blue) | `#0072B2` (blue) | вместо зелёного |
| `c.bear` | `#E69F00` (orange) | `#D55E00` (vermillion) | вместо красного |
| `c.liquidity` | `#D0D3DB` | `#3B3F4A` | высококонтрастный нейтральный + обязательные теги BSL/SSL |
| `c.signal` | `#CC79A7` (reddish purple) | `#AA3377` | отличим от blue/orange |
| `c.mitigated` | `#9C9EA6` | `#8A8C94` | серо-фиолетовый → серый |
| `c.warning` | `#F0E442` (dark) | `#9C6B00` (light) | — |
| прочие | как Standard | как Standard | — |

#### 13.3.3 Палитра Mono+ (v1.1, печать и максимальная доступность)

Все объекты — оттенки `c.neutral`/`c.text`. Направление — только стрелками ↑↓, стилем (bull — solid, bear — dashed) и позицией. Сигнал — `c.signal`. Используется для скриншотов в документации и для пользователей с тяжёлыми нарушениями цветовосприятия.

### 13.4 Адаптация темы

1. `Theme = Auto` (по умолч.): тема определяется по яркости `chart.bg_color` — `Y = 0.2126R + 0.7152G + 0.0722B` (0–255). `Y < 128` → Dark, иначе Light.
2. `Theme = Dark / Light` — ручное переопределение (например, для градиентного фона).
3. Текст всегда от `chart.fg_color` (с прозрачностью для muted), поэтому контраст с фоном гарантирован платформой.
4. Пользовательские цвета (input.color) допускаются только для `c.bull` / `c.bear` в группе Advanced. Остальные токены не настраиваются — это защищает семантику.

### 13.5 Шкала прозрачности

Значения — параметр `transp` Pine (0 = непрозрачно, 100 = невидимо).

> **v0.2 (после первого визуального теста):** шкала уплотнена — пользователи отметили, что зоны и сессии почти не видны. Действующие значения (Visibility = Standard): `op.strong` 10, `op.medium` 30, `op.soft` 50, `op.faint` 65; `fill.focus` 65, `fill.strong` 70, `fill.base` 76, `fill.light` 80, `fill.faint` 86, `fill.wash` 92, `fill.ghost` 95. Настройка **Visibility** сдвигает все значения: Subtle +8, Bold −12. Модуляция релевантностью: `+round((1 − R) × 6)`, потолок 94. Таблицы ниже — исходный проект v1, оставлены для истории решений.

**Линии и текст (`op.*`)**

| Токен | transp | Применение |
|---|---:|---|
| `op.solid` | 0 | Текст Tier 1, Entry/SL |
| `op.strong` | 15 | HTF Key Levels, swing BOS/CHoCH (последние), TP-линии |
| `op.medium` | 40 | Tier 2 линии, контуры свежих зон |
| `op.soft` | 65 | Tier 3 линии, контуры touched-зон, сессии |
| `op.faint` | 80 | Minor-ликвидность, старая структура, снятые уровни |

**Заливки (`fill.*`)**

| Токен | transp | Применение |
|---|---:|---|
| `fill.focus` | 70 | Entry-зона активного сетапа |
| `fill.strong` | 76 | HTF OB fresh |
| `fill.base` | 82 | LTF OB fresh |
| `fill.light` | 88 | FVG open, OB touched, Breaker |
| `fill.faint` | 92 | Mitigated, OTE-полоса, reward/risk-боксы сетапа |
| `fill.wash` | 96 | Premium/Discount, сессии |
| `fill.ghost` | 98 | Debug: скрытые объекты |
| `fill.panel` | 10 | Фон панелей (Dashboard, Ribbon, карточка) |

**Модуляция релевантностью (§16):** `transp_eff = min(base + round((1 − R) × 12), 97)`. Для HTF: `base − 5`.

### 13.6 Линии

| Токен | Стиль | Толщина | Применение |
|---|---|:---:|---|
| `ln.entry` | solid | 2 | Entry |
| `ln.sl` | solid | 2 | Stop Loss |
| `ln.tp` | dashed | 1 | TP1–TP3 |
| `ln.inv` | dotted | 1 | Инвалидация (если отличается от SL) |
| `ln.struct.swing` | dashed | 1 (HTF: 2) | BOS/CHoCH swing: от свинга до бара пробоя |
| `ln.struct.int` | dotted | 1 | BOS/CHoCH internal (Analysis) |
| `ln.liq.major` | solid | 1 (HTF/Key: 2) | Активная major-ликвидность |
| `ln.liq.minor` | dotted | 1 | Minor-ликвидность |
| `ln.liq.swept` | dotted | 1 | Снятая: обрывается на баре свипа, `op.faint` |
| `ln.liq.pending` | dashed | 1 | PENDING_RECLAIM |
| `ln.zone.mid` | dotted | 1 | CE FVG / mean threshold OB |
| `ln.range.eq` | dotted | 1 | Equilibrium |
| `ln.range.ote` | dotted | 1 | 0.705 внутри OTE-полосы |
| `ln.path` | dotted + стрелка | 1 | Setup Path (Analysis) |

Толщина 3+ не используется: на 4K и мобильных она создаёт визуальный «вес», конкурирующий со свечами.

### 13.7 Типографика

| Роль | Размер Pine | Начертание | Шрифт | Где |
|---|---|---|---|---|
| T1 — критичное | `size.small` | **bold** | default | Карточка сетапа (заголовок), HTF BOS/CHoCH, `SSL ✕` major |
| T2 — важное | `size.small` | regular | default | Swing BOS/CHoCH, теги зон и уровней Tier 2 |
| T3 — контекст | `size.tiny` | regular | default | Internal-структура, HH/HL/LH/LL, minor-теги, сессии |
| T4 — диагностика | `size.tiny` | regular | monospace | ID, состояния, R-оценки (Debug) |
| Dashboard: ключ | `size.tiny` (Compact) / `size.small` | regular, muted | default | MARKET, HTF, … |
| Dashboard: значение | `size.tiny` / `size.small` | **bold** | default | BULLISH, 8.4 / 10 |
| Dashboard: числа | `size.tiny` / `size.small` | regular | monospace | Цены, дистанции, RR |
| Ribbon | `size.tiny` / `size.small` | bold для значений | default | Одна строка |

`size.normal` и крупнее на графике **не используются** (крупный текст перекрывает свечи). Pine v6 позволяет задавать размер текста в пунктах, если это подтвердит спайк S-5. Тогда шкала: T1/T2 = 10 pt, T3/T4 = 8 pt, Dashboard = 9 pt.

### 13.8 Боксы: спецификация по сущностям

| Сущность | Заливка (fresh) | Контур | Стиль контура | Текст в боксе | Правый край |
|---|---|---|---|---|---|
| OB (LTF) | dir @ `fill.base` | dir @ `op.medium`, 1 px | solid | `OB` (tiny, верх-лево, dir @ op 20) | now + 5 баров |
| OB (HTF) | dir @ `fill.strong` | dir @ `op.strong`, 2 px | solid | `◆4H OB` (small, bold) | now + 5 |
| FVG | dir @ `fill.light` | нет | — | `FVG` (tiny) | now + 5 |
| IFVG | новый dir @ `fill.light` | новый dir @ `op.soft` | dashed | `IFVG` | now + 5 |
| Breaker | новый dir @ `fill.light` | новый dir @ `op.medium` | dashed | `BB` | now + 5 |
| Mitigation Block | новый dir @ `fill.faint` | новый dir @ `op.soft` | dotted | `MB` | now + 5 |
| Rejection Block | dir @ `fill.faint` | dir @ `op.soft` | solid | `RB` | now + 5 |
| S&D (v1.1) | нет | dir @ `op.medium` | dashed | `DBR` / `RBD` / `RBR` / `DBD` | now + 5 |
| VI / LV / BPR (v1.1) | dir @ `fill.faint` / нет / neutral @ `fill.light` | — / dir dotted / neutral solid | — | `VI` / `LV` / `BPR` | now + 5 |
| Premium / Discount | `c.premium` / `c.discount` @ `fill.wash` | нет | — | нет | граница диапазона |
| OTE-полоса | `c.signal` @ `fill.faint` | нет | — | `OTE` (tiny, справа) | now + 5 |
| Сессия (range box) | цвет сессии из настроек | тот же цвет, плотнее (текущая — solid, прошлые — dashed) | solid / dashed | название — **над** максимумом сессии (не на свечах) | конец сессии |
| Entry-зона сетапа | `c.signal` @ `fill.focus` | signal @ `op.medium` | solid | нет (карточка отдельно) | bar + 20 |
| Reward / Risk боксы | `c.reward` / `c.risk` @ `fill.faint` | нет | — | нет | bar + 20 |

**Внутренние отступы.** У боксов Pine нет padding. Текст выравнивается по верхнему левому углу (`text_halign = left`, `text_valign = top`), а для визуального отступа добавляется один неразрывный пробел в начале строки. Если высота бокса < 0.35 ATR, текст в боксе не выводится (тег уходит в тултип соседней метки или в Analysis).

### 13.9 Метки (labels)

| Тип метки | Стиль Pine | Позиция | Размер | Фон |
|---|---|---|---|---|
| Структурное событие (BOS/CHoCH) | текст без подложки (`style_label_none`) или `style_text_outline` | середина линии пробоя; над линией для ↑, под — для ↓ | T1/T2 | нет |
| Свинг (HH/HL/LH/LL) | текст без подложки | `yloc.abovebar` / `yloc.belowbar` бара пивота | T3 | нет |
| Свип | `style_label_up` / `down` (маленький) или текст `✕` | у тени бара свипа (`abovebar` / `belowbar`) | T1 (major) / T3 (minor) | `c.liquidity` @ 20 для major |
| Тег уровня | текст без подложки, `style_label_left` | правый край линии +1 бар | T2/T3 | нет |
| Карточка сетапа | `style_label_left` | справа от последнего бара, на уровне entry | T1 (заголовок) + T2 | `c.panel.bg` @ `fill.panel`, текст `c.text` |
| Маркер Setup Path | текст `①…⑨` | в точке события цепочки | T2 | нет |
| Debug-аннотация | `style_label_none`, monospace | рядом с объектом | T4 | нет |

**Правила:** все метки имеют `tooltip` с полной расшифровкой (§14.7). Текст метки — не более 2 строк и 24 символов в строке (карточка — до 3 строк).

### 13.10 Таблицы (Dashboard, Ribbon)

| Параметр | Dashboard | Ribbon |
|---|---|---|
| Позиция | `position.top_right` (настраиваемо) | `position.bottom_center` (настраиваемо: top_center) |
| Сетка | 2 колонки × 8–11 строк | 1 строка × 5–7 ячеек |
| Фон | `c.panel.bg` @ `fill.panel` | то же |
| Рамка | `frame_width = 1`, `c.panel.border` | то же |
| Внутренние границы | `border_width = 0` (чистый вид) | `border_width = 1`, `c.panel.border` как разделитель сегментов |
| Ширина ячеек | в % от ширины панели: ключ 5–6%, значение 8–10% (Compact); 7% / 12% (Expanded) | авто |
| Выравнивание | ключ — left, значение — left | center |
| «Padding» | не поддерживается → задаётся минимальными `width/height` ячеек (в % области графика) и ведущим пробелом | то же |
| Тултипы ячеек | Да: расшифровка и время события | Да |
| Обновление | только `barstate.islast`, таблица создаётся один раз | то же |

### 13.11 Иконография и сокращения

**Символы**

| Символ | Значение | ASCII-fallback |
|---|---|---|
| ↑ / ↓ | Направление (bull / bear) | `^` / `v` |
| ✕ | Снято (sweep) / инвалидировано | `x` |
| ◆ | HTF-объект (префикс ТФ) | `*` |
| ≡ | Равные уровни (EQ), с числом касаний: `≡3` | `=` |
| ✓ | Цель достигнута | `+` |
| ⌛ | Истёк срок | `~` |
| ⚠ | Предупреждение | `!` |
| ①…⑨ | Шаги Setup Path | `(1)…(9)` |
| ● | Точка входа (исполнение) | `o` |

**Словарь сокращений (единственно допустимые)**

| Сокр. | Полное | Сокр. | Полное |
|---|---|---|---|
| BOS | Break of Structure | OB | Order Block |
| CHoCH | Change of Character | BB | Breaker Block |
| MSS | Market Structure Shift (CHoCH + displacement + FVG) | MB | Mitigation Block |
| iBOS / iCHoCH | Internal BOS / CHoCH | RB | Rejection Block |
| HH / HL / LH / LL | Swing labels | FVG / IFVG | Fair Value Gap / Inverted FVG |
| EQH / EQL | Equal Highs / Lows | VI / LV / BPR | Volume Imbalance / Liquidity Void / Balanced Price Range |
| BSL / SSL | Buy-side / Sell-side Liquidity | CE | Consequent Encroachment (50% FVG) |
| PDH / PDL | Previous Day High / Low | EQ | Equilibrium |
| PWH / PWL | Previous Week High / Low | OTE | Optimal Trade Entry |
| AH / AL | Asia High / Low | KZ | Killzone |
| LOH / LOL | London High / Low | SB | Silver Bullet |
| NYH / NYL | New York AM High / Low | DBR / RBD / RBR / DBD | Supply/Demand patterns |
| MOP | NY Midnight Open | E / SL / TP1–3 / RR | Entry / Stop / Targets / Risk-Reward |

### 13.12 Каталог «сущность → визуал»

| Сущность | Форма | Hue | Плотность (fresh) | Линия | Метка | Tier по умолч. |
|---|---|---|---|---|---|:---:|
| HTF bias | Ribbon + Dashboard; на графике — HTF-уровни | bull/bear | — | — | `HTF ▲ BULL` | 1 |
| Swing BOS | линия от свинга до пробоя + метка | dir | `op.strong` | dashed 1 (HTF 2) | `BOS↑` | 1 (последний), 2 |
| Swing CHoCH / MSS | то же | dir | `op.strong` | dashed | `CHoCH↓` / `MSS↓` (bold) | 1 |
| Internal BOS/CHoCH | короткая линия | neutral (dir в стрелке) | `op.soft` | dotted | `iBOS↑` (tiny) | 3 |
| Swing labels | текст | neutral | `op.medium` | — | `HH` (tiny) | 3 |
| Major liquidity (BSL/SSL, EQ, Key) | линия до правого края | liquidity | `op.strong` | solid 1 / 2 (HTF, Key) | `BSL ≡3`, `◆PDH` | 1–2 |
| Minor liquidity | линия | liquidity | `op.faint` | dotted | без тега | 3 |
| Sweep | маркер у тени + обрыв линии | liquidity | `op.solid` (major) | — | `SSL ✕` | 1 |
| Taken (run) | обрыв линии без маркера | liquidity | `op.faint` | — | — | 3 |
| OB | бокс заливка+контур | dir | `fill.base` | solid | `OB` | 2 |
| FVG | бокс заливка без контура + CE | dir | `fill.light` | CE dotted | `FVG` | 2 |
| Breaker / MB / IFVG | бокс с dashed/dotted контуром | новый dir | `fill.light` / `fill.faint` | dashed / dotted | `BB` / `MB` / `IFVG` | 2 |
| S&D | только контур | dir | — | dashed | `DBR` | 3 |
| Dealing range | EQ-линия, OTE-полоса, риски границ, Gauge | neutral / signal | `fill.faint` | dotted | `EQ`, `OTE` | 2 |
| Premium / Discount | мягкий фон (опц.) | bear / bull | `fill.wash` | — | нет | 3 |
| Сессии | range box | neutral | `fill.wash` | dotted | `LON` | 3 |
| Setup | композиция (§14.8) | signal + reward/risk | `fill.focus` / `fill.faint` | entry/SL solid 2, TP dashed | карточка | 1 |

### 13.13 Z-порядок (снизу вверх)

1. `wash` — Premium/Discount, сессии.
2. `zones.htf` — HTF-зоны (крупные, фоновые).
3. `zones.ltf` — LTF-зоны (уточнение внутри HTF).
4. `range` — OTE-полоса, EQ.
5. `levels` — ликвидность, Key Levels.
6. `structure` — линии BOS/CHoCH.
7. `setup` — reward/risk/entry-боксы, линии Entry/SL/TP.
8. `labels` — все метки (последними, чтобы не перекрывались заливками).

Свечи — поверх всего (`behind_chart = true`). Порядок обеспечивается созданием пулов в этой последовательности (§4.9).

### 13.14 Макеты

**Normal Mode (тёмная тема), схематично** (`|` — свечи, Dashboard — см. §14.5):

```
┌───────────────────────────────────────────────────────────────── chart ──┐
│                                                     ┌─ DASHBOARD ──────┐ │
│ ═══════════════════════════════════════ ◆D PDH      │  §14.5           │ │
│ ─────────────────────────────────────── BSL =3      └──────────────────┘ │
│                                                                          │
│        |       BOS ^                        ┌─────────┐ - - TP2  3.2R    │
│      | | |  - - - - - - -                   │ reward  │ - - TP1  1.9R    │
│    | |   | |          |                     │         │                  │
│  | |       | |    |  | |   |   |            ├─────────┤ < LONG · A+ 8.4  │
│ |            |   | | |  | | | |  |          │  ENTRY  │   Sweep>CHoCH>   │
│ ····· EQ ····· | |  |    CHoCH ^ - - | |    ├─────────┤   FVG>OTE  RR3.2 │
│ ░░░░░ OTE ░░░░░░|░░░░░░░░░░░░░░░░░░░░░░░░░░ │  risk   │                  │
│                 |       [ FVG ·· CE ·· ]    └─────────┘ ── SL            │
│ ───────────────── SSL x                                                  │
│                                                                          │
│    ┌───────────────────────────────────────────────────────────────┐     │
│    │ HTF ^ BULL │ STR ^ BULL │ LON KZ │ DISC 36% │ SSL x │ LONG A+ │     │
│    └───────────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────────┘
```

Что видно за 3 секунды: HTF бычий (Ribbon, ◆PDH сверху как цель), структура развернулась вверх (CHoCH ^), SSL снята (x), цена в Discount/OTE, сетап LONG A+ с понятными Entry/SL/TP, цель — BSL =3 и PDH. Всё остальное скрыто приоритетом.

**Analysis Mode — тот же момент:** добавляются internal-структура (`iBOS`, tiny, dotted), HH/HL-метки, история снятой ликвидности (тусклые обрывки с ✕), маркеры цепочки `① SSL ✕ → ② disp → ③ CHoCH↑ → ④ FVG → ⑤ OTE → ⑥ E`, соединённые пунктирными стрелками, Event Timeline в Dashboard (Expanded).
