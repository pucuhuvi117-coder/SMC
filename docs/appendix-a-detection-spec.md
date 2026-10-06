# Appendix A · Формальная спецификация детекторов

> Закрывает находки аудита **D-01…D-16**: каждое понятие SMC/ICT получает однозначное, проверяемое определение с параметрами и значениями по умолчанию.
> Определения даны **для бычьего случая**. Медвежий — зеркально (high ↔ low, > ↔ <, BSL ↔ SSL).
> Все проверки выполняются **на подтверждённом баре** `t`. Значения по умолчанию сведены в A.19.

---

## A.1 Обозначения и единицы

| Обозначение | Определение |
|---|---|
| `t` | Текущий подтверждённый бар |
| `o, h, l, c, v` | OHLCV бара |
| `VU` | Единица волатильности = `ATR(atrLen)` на баре оценки (по умолч. `atrLen = 14`) |
| `tick` | `syminfo.mintick` |
| `body` | `|c − o|` |
| `range` | `h − l` |
| `bodyRatio` | `body / max(range, tick)` |
| `TFms` | Длительность бара в мс (`timeframe.in_seconds() × 1000`) |
| `isGapBar(t)` | `time[t] − time[t−1] > 1.5 × TFms` **или** первый бар торговой сессии инструмента (для инструментов с сессиями) |

Все пороги вида «k × ATR» вычисляются в цене как `k × VU`.

## A.2 Свинги (пивоты)

- Пивот high длины `L` на баре `p` подтверждается на баре `p + L`, если:
  `h[p] > h[i]` для всех `i ∈ [p − L, p − 1]` (слева строго) **и** `h[p] ≥ h[i]` для всех `i ∈ [p + 1, p + L]` (справа нестрого).
  При равных максимумах это даёт ровно один пивот — самый левый.
- Два уровня структуры: **internal** (`Li`, по умолч. 3) и **swing** (`Ls`, по умолч. 10; пресеты Scalp 5/2, Intraday 10/3, Swing 20/5). Вычисляются независимо.
- Последовательность пивотов не обязана чередоваться (high, high возможны). Для меток сравнение идёт с предыдущим пивотом той же стороны.
- Если семантика `ta.pivothigh/pivotlow` не совпадает с правилом равенства, используется собственная реализация (проверка — спайк S-4/P1).

## A.3 Классификация свингов и EQ

- `tolEQ = eqTol × VU` (по умолч. `eqTol = 0.10`).
- Для нового пивота high с ценой `P` и предыдущим пивотом high `P₀` того же уровня:
  `P > P₀ + tolEQ` → **HH**; `P < P₀ − tolEQ` → **LH**; иначе → **EQH** (флаг равенства, метка `HH/LH` по знаку разницы + `≡`).
- Lows: **HL / LL / EQL** аналогично.
- «Significant» (режим меток): swing-уровень **и** (пивот был `ref` пробоя **или** якорем dealing range **или** уровнем, который сняли).

## A.4 Пробои структуры: BOS / CHoCH / MSS

| Элемент | Определение |
|---|---|
| `refHigh` | Последний подтверждённый, ещё не пробитый пивот high данного уровня |
| Источник пробоя | `Close` (по умолч.): `c[t] > refHigh.price`. `Wick`: `h[t] > refHigh.price` |
| Тип | `trend == BULLISH` → **BOS↑**. `trend == BEARISH` → **CHoCH↑**. `trend == UNDEFINED` → **BOS↑ initial** |
| После пробоя | `trend = BULLISH`, `refHigh.broken = true` (повторного пробоя этого пивота нет) |
| Нога пробоя | `origin` = бар с минимальным low на интервале `[refHigh.pivotBar, t]`. `legLow = l[origin]`, `legHigh = max(h[origin..t])` |
| `dispStrength` | `(legHigh − legLow) / VU` |
| `legHasFvg` | Внутри `[origin, t]` создан хотя бы один бычий FVG (A.10) |
| **MSS** | CHoCH, у которого `dispStrength ≥ kLeg` (по умолч. 1.5) **и** `legHasFvg` |
| Дубли уровней | Если на одном баре пробиты internal и swing одного направления, internal-событие эмитится с флагом `shadowed` и не рисуется в Clean/Normal |

## A.5 Strong / Weak, protected levels

- После **swing**-пробоя вверх: `protectedLow = legLow` (strong low — «защищённый» минимум, его пробой означает смену характера по строгому правилу). `weakHigh = max(h)` с момента пробоя (developing); после подтверждения следующего пивота high — фиксируется.
- Опция «CHoCH reference»: `Last swing` (по умолч., как в ТЗ §1.4: CHoCH↓ = закрытие ниже последнего swing low) или `Protected` (CHoCH↓ = закрытие ниже `protectedLow`).
- `protectedLow` используется Context (нижняя граница диапазона) и Setup (инвалидация CONTINUATION) в обоих режимах.

## A.6 Displacement

| Уровень | Определение | По умолч. |
|---|---|---|
| Бар | `isDispBar`: `body ≥ kBody × VU` **и** `bodyRatio ≥ minBodyRatio`, направление = `sign(c − o)` | `kBody = 1.0`, `minBodyRatio = 0.6` |
| Нога | `dispStrength` из A.4 | — |
| Событие `DISPLACEMENT` | Эмитится на баре `t`, если создан FVG, у которого средняя свеча `t−1` — `isDispBar` («displacement с imbalance») | — |
| Нормировка для скоринга | `min(1, dispStrength / 2.0)` | — |

## A.7 Order Block

**Рождение:** на событии бычьего пробоя (BOS↑/CHoCH↑) уровня из набора `obLevels` (по умолч. `swing`; опция `+internal`).

1. **Окно поиска** `W = [origin − nPre, d − 1]`, где `origin` — из A.4, `d` — первый бар после `origin` с `isDispBar` бычьего направления (если нет — первый бычий бар после `origin`; если и его нет — `t`). `nPre = 3`. Верхняя граница длины окна — `obMaxSearch` (по умолч. 30 баров).
2. **Свеча OB** = последняя (самая правая) медвежья свеча (`c < o`) в `W`.
3. Нет медвежьей свечи → свеча `origin` (fallback, `strength × 0.7`, флаг `fallback`).
4. **Зона** (`obZone`):
   - `Full`: `[l, h]` свечи OB;
   - `Body+Wick` (по умолч.): `[l, max(o, c)]`;
   - `Body`: `[min(o, c), max(o, c)]`.
   - Опция «Extend to leg low» (по умолч. off): `bottom = min(bottom, legLow)`.
5. **Фильтры:**
   - размер `top − bottom ∈ [obMin × VU, obMax × VU]` (0.25 / 3.0). Если больше `obMax` в режиме Full/Body+Wick → автоматически `Body`. Всё ещё больше → REJECTED;
   - `Require displacement` (по умолч. on): `dispStrength ≥ obDispMin` (1.0);
   - `Volume filter` (по умолч. off): `max(volRatio[d..t]) ≥ volMult` (1.5). Нет объёма → фильтр игнорируется + SYS_WARN `NO_VOLUME`;
   - целостность: если `min(l[j+1 .. t]) < bottom` (зона пробита до рождения) → REJECTED. Если `min(l[j+1 .. t]) ≤ top` → начальное состояние TOUCHED.
6. **Дедупликация:** OB с той же свечой от internal и swing → один объект (уровень = swing).
7. **Lifecycle (§7.3):**

| Переход | Условие (бычий OB) |
|---|---|
| → TOUCHED | `l[t] ≤ top` |
| → MITIGATED | Правило `Touch`: сразу при касании (без TOUCHED). `50%` (по умолч.): `l[t] ≤ mid`. `Full`: `l[t] ≤ bottom` и `c[t] ≥ bottom` |
| → BROKEN | `c[t] < bottom` |
| → EXPIRED | возраст > `obMaxAge` (500 баров) **или** расстояние до цены > `zoneMaxDist × VU` (20) |

8. **Strength** (для скоринга и визуала): `0.6 × min(1, dispStrength / 2.5) + 0.2 × min(1, size / VU / 1.5) + 0.2 × min(1, volRatio / 2)`. Без объёма вес объёма переносится на displacement.

## A.8 Breaker и Mitigation Block (конверсия пробитого OB)

Когда бычий OB `Z` переходит в BROKEN (`c[t] < Z.bottom`) и конверсия включена:

1. `extHigh` = последний подтверждённый **swing**-пивот high, сформированный до начала ноги `Z` (до `origin`).
2. `legMax` = максимум high от `origin` ноги `Z` до бара `t`.
3. `legMax > extHigh.price` (нога сняла внешнюю ликвидность — новый максимум) → **BREAKER** (медвежий).
   Иначе (нога не обновила максимум — несостоявшийся свинг) → **MITIGATION_BLOCK** (медвежий).
4. Новая зона: те же `top/bottom`, `dir = −1`, `state = FRESH`, `parentId = Z.id`. Событие `ZONE_CONVERTED`.
5. Breaker/MB проходят автомат OB. После их BROKEN — только INVALIDATED.

> Следствие: OB, рождённые swing-пробоем, при провале всегда становятся Breaker (их нога по определению обновила swing high). Mitigation Block возникает у OB internal-уровня, нога которых не дотянулась до внешнего максимума. Это соответствует ICT-различию «Breaker — со снятием ликвидности, Mitigation — без».

## A.9 Rejection Block (v1.1)

На подтверждённом swing-пивоте high (бар `p`): `upperWick = h − max(o, c)`. Если `upperWick ≥ 0.6 × range` **и** `upperWick ≥ 2 × body` → медвежий RB с зоной `[max(o, c), h]`. Lifecycle — как у OB, без конверсии.

## A.10 Fair Value Gap и IFVG

| Элемент | Определение (бычий) | По умолч. |
|---|---|---|
| Паттерн | На баре `t`: `l[t] > h[t−2]`. Зона: `bottom = h[t−2]`, `top = l[t]`, `mid (CE) = (top + bottom) / 2` | — |
| Размер | `top − bottom ≥ fvgMin × VU` | 0.30 |
| Средняя свеча | Опция «Require middle candle direction»: `c[t−1] > o[t−1]` | on |
| Сессионные гэпы | `Ignore session gaps`: паттерн игнорируется, если `isGapBar(t−1)` или `isGapBar(t)` | on |
| Displacement-тег | `isDispBar(t−1)` → `isDisplacementFvg` | — |
| → PARTIAL | `l[t] ≤ top` | — |
| → CE_REACHED | `l[t] ≤ mid` | — |
| → FILLED | `Wick far edge` (по умолч.): `l[t] ≤ bottom`. `Close far edge`: `c[t] ≤ bottom`. `CE`: `l[t] ≤ mid` | Wick |
| Незаполненный остаток | `unfilledTop = min(unfilledTop, l[t])`. Остаток = `[bottom, unfilledTop]` | — |
| → CONVERTED (IFVG) | `c[t] < bottom` и `IFVG` включён → новая медвежья зона `kind = IFVG` с геометрией исходного FVG | on |
| → EXPIRED | возраст > `fvgMaxAge` (300) или расстояние > `zoneMaxDist × VU` | — |

## A.11 VI, LV, BPR, Supply & Demand (v1.1)

| Вид | Определение (бычий) |
|---|---|
| **Volume Imbalance** | `min(o[t], c[t]) > max(o[t−1], c[t−1])` **и** `l[t] ≤ h[t−1]` (тени перекрываются, тела — нет). Зона `[max(o,c)[t−1], min(o,c)[t]]`, размер ≥ 0.10 VU |
| **Liquidity Void** | ≥ `lvBars` (3) подряд бычьих свечей с `bodyRatio ≥ 0.7`, суммарный диапазон ≥ `lvMin × VU` (3.0), перекрытие тел соседних свечей ≤ 30%. Зона `[l первой, h последней]`, визуально — только контур |
| **BPR** | Бычий FVG `A` и медвежий FVG `B` (или наоборот) с разницей рождения ≤ `bprBars` (20) и пересечением ≥ 0.10 VU. Зона = пересечение, `dir` = направление более позднего FVG |
| **Base (S&D)** | 1…`baseMax` (5) подряд свечей с `bodyRatio ≤ 0.5` и `range ≤ 1.0 × VU` |
| **Leg-in / Leg-out** | Свеча до и после базы с `bodyRatio ≥ 0.6` и `range ≥ 1.0 × VU` |
| **DBR / RBR** (demand) | leg-in вниз / вверх, leg-out вверх. Зона: `proximal = max(max(o, c))` базы, `distal = min(l)` базы |
| **RBD / DBD** (supply) | Зеркально |
| **Fresh** | Зона ни разу не касалась ценой после leg-out |

## A.12 Уровни ликвидности

| Элемент | Определение | По умолч. |
|---|---|---|
| Источники | Swing-пивоты (major-кандидаты), internal-пивоты (minor, опц.), EQ-кластеры, Key Levels, session H/L | swing + key |
| Уровень | BSL на цене пивота high, SSL — на low | — |
| EQ-кластер | Новый пивот той же стороны в пределах `tolLiq = liqTol × VU` от ACTIVE-уровня и не дальше `eqMaxBars` баров → `touches += 1`, цена уровня = **max** цен (BSL) / **min** (SSL). При `touches = 2` → событие `LIQ_EQ` | `liqTol = 0.15`, `eqMaxBars = 100` |
| Key Levels | PDH/PDL, PWH/PWL — из подтверждённых D/W-баров (идиома `[1]`); граница дня: `Exchange` (по умолч.) или `NY midnight`. AH/AL, LOH/LOL, NYH/NYL — high/low сессии на её закрытии. MOP — open бара 00:00 NY (референс, не ликвидность) | — |
| `isMajor` | `tfSlot ≠ CHART` **или** Key Level **или** `touches ≥ 2` **или** (swing-уровень **и** возраст ≥ `oldAge`) | `oldAge = 50` |
| Expiry | Расстояние > `liqMaxDist × VU` (20) или возраст > `liqMaxAge` (1000) | — |

## A.13 Свип и пробой ликвидности (BSL; SSL — зеркально)

Параметры: `maxSweepPen` (1.0 VU), `reclaimBars` (2), `tickBuf` (1 tick), `tsMinAge` (20), `tsWindow` (10).

| # | Условие на баре `t` для ACTIVE-уровня `P` | Результат |
|---|---|---|
| 1 | `h[t] > P + tickBuf`, `c[t] ≤ P`, `(h[t] − P) ≤ maxSweepPen × VU` | **SWEPT**, `sweepType = WICK`, `sweepExtreme = h[t]` |
| 2 | `c[t] > P` и `(h[t] − P) ≤ maxSweepPen × VU` | **PENDING_RECLAIM** с `pendingSince = t` |
| 3 | `(h[t] − P) > maxSweepPen × VU` (по high или close) | **TAKEN** (run — глубокое принятие цены) |
| 4 | Для PENDING_RECLAIM: в течение `reclaimBars` баров `c ≤ P` | **SWEPT**, `sweepType = RECLAIM`, `sweepExtreme = max(h)` за окно ожидания |
| 5 | Для PENDING_RECLAIM: за `reclaimBars` нет `c ≤ P`, или глубина превысила `maxSweepPen` | **TAKEN** |
| 6 | SWEPT-уровень с возрастом ≥ `tsMinAge` и в течение `tsWindow` баров — internal CHoCH↓ | атрибут `sweepType = TURTLE_SOUP` |

- Один бар может снять несколько уровней → несколько событий. Setup Engine использует самый важный (`isMajor`, затем HTF, затем touches).
- `penetrationAtr = (sweepExtreme − P) / VU`.
- Направление `LIQ_SWEPT.dir` для BSL = −1 (ожидаемая реакция вниз), для SSL = +1.

## A.14 Dealing Range, Premium/Discount, OTE

| Элемент | Определение | По умолч. |
|---|---|---|
| Источник | `Swing` (по умолч.) / `Internal` / `HTF1` | Swing |
| Построение (бычий) | На swing-пробое вверх: `low = protectedLow` (A.5), `high = max(h)` с `origin` (developing). Подтверждение пивота high после пробоя → `high` фиксируется, состояние ESTABLISHED | — |
| Перестройка | Следующий swing-пробой вверх → новый диапазон от нового `protectedLow`. CHoCH↓ → медвежий диапазон (`high = protectedHigh`, `low = min(l)` с origin) | — |
| `eq` | `(high + low) / 2` | — |
| `pd%` | `(c − low) / (high − low)`. Для отображения ограничивается `[−0.2, 1.2]` | — |
| Зоны | `pd% > 0.5 + eqBand` → PREMIUM. `pd% < 0.5 − eqBand` → DISCOUNT. Иначе — EQ | `eqBand = 0.02` |
| OTE (бычий диапазон, лонги) | Откат `r ∈ [oteLo, oteHi]` от high: цена ∈ `[high − oteHi × R, high − oteLo × R]` ⇔ `pd% ∈ [1 − oteHi, 1 − oteLo]` = `[0.21, 0.38]`. Sweet spot `1 − 0.705 = 0.295` | `oteLo = 0.62`, `oteHi = 0.79` (настраиваемо, напр. 0.618 / 0.786) |
| OTE (медвежий, шорты) | `pd% ∈ [oteLo, oteHi]` = `[0.62, 0.79]`, sweet 0.705 | — |

## A.15 Сессии и killzones

**Таймзона сессий** — `America/New_York` (DST автоматически через `time(timeframe.period, session, tz)`). Сессии отображаются на ТФ ≤ 1H. На старших ТФ — только Ribbon (по последнему LTF-времени) или отключены.

| Окно | ICT (NY) — по умолч. | Original (UTC) — пресет ТЗ v1 |
|---|---|---|
| Asia | 20:00–00:00 | 00:00–06:00 UTC |
| London KZ | 02:00–05:00 | 07:00–10:00 UTC |
| NY AM KZ | 07:00–10:00 | 12:00–15:00 UTC |
| London Close | 10:00–12:00 | — |
| NY PM | 13:30–16:00 | — |
| Silver Bullet | 03:00–04:00, 10:00–11:00, 14:00–15:00 | 10:00–11:00 NY |
| Judas window | первые 60 мин London KZ и NY AM KZ | первый час London/NY |

> В пресете Original UTC окна жёстко привязаны к UTC и **смещаются относительно Нью-Йорка/Лондона при DST**. Пресет сохранён для совместимости, по умолчанию не используется (D-07).

- Session high/low копятся на барах сессии, на её закрытии создаются Key Levels (AH/AL, LOH/LOL, NYH/NYL).
- `minutesLeft = (sessionEnd − time_close) / 60000`.

## A.16 HTF bias и MARKET bias

- `htfBias` = `trend` swing-структуры HTF1 на последнем закрытом HTF-баре. `UNDEFINED` → NEUTRAL.
- `htfReliable = (HTF-баров в буфере ≥ minHtfBars)`.
- HTF2 (опц.): подтверждение. Если `HTF2.trend ≠ htfBias`, Dashboard показывает `4H BULL · D BEAR` (warning-цвет), скоринг даёт половину балла за HTF.
- **MARKET:**
  1. `regime == RANGING` → **RANGING**;
  2. иначе, если `htfBias` неизвестен или ненадёжен → chart swing trend;
  3. иначе, если `htfBias == chart swing trend` → это направление;
  4. иначе → **MIXED**.

## A.17 Режим рынка

**RANGING**, если выполнено одно из условий:
- (a) с последнего swing-пробоя прошло ≥ `rangeBars` баров (по умолч. `8 × Ls`) **и** `pd% ∈ [0, 1]`;
- (b) два последних swing-события — CHoCH противоположных направлений в пределах `chopBars` (по умолч. `6 × Ls`).

Иначе — **TRENDING**.

## A.18 Модели сетапов (guards)

### SWEEP_REVERSAL (LONG; SHORT — зеркально)

| Стадия | Условие входа в стадию | Guard / таймаут |
|---|---|---|
| Контекст | Нет warm-up. Пресет Conservative: `htfBias ≠ BEAR` | — |
| SWEEP_SEEN | `LIQ_SWEPT` с `dir = +1` (снята SSL). `sweepExtreme = sweep low` | — |
| SHIFTED | В пределах `Nshift` баров после свипа — первый пробой вверх (internal или swing; CHoCH или BOS) с `dispStrength ≥ shiftDispMin`, нога которого начинается от свипа: `legLow ≤ sweepExtreme + 0.25 × VU` | `Nshift = 20`, `shiftDispMin = 1.0`. Нет сдвига → EXPIRED (`NO_SHIFT_IN_WINDOW`) |
| FORMING | POI выбран по §9.4 среди FVG/OB, рождённых ногой сдвига, и proximal POI ≤ `eq` нового диапазона (discount) | Нет POI → EXPIRED (`NO_POI`) или (`POI_IN_PREMIUM`) |
| READY | План: entry (§10.3), `SL = sweepExtreme − buffer`, цели (§10.5). `RR ≥ minRR`, SL в границах (§11.3), грейд ≥ `minGrade` | Не выполнено → остаётся FORMING до `expiryBars`, затем EXPIRED с причиной |
| TRIGGERED | Начиная с бара **после** READY: `l ≤ entry` | — |
| INVALIDATED | До входа: `c < sweepExtreme`, **или** swing CHoCH↓, **или** POI → BROKEN | — |
| MISSED | До входа: `h ≥ TP1` | — |
| EXPIRED | READY дольше `expiryBars` (30) или конец сессии (если «Require killzone») | — |
| TP / SL | После входа: `h ≥ TPn` → TPn_HIT; `l ≤ SL` → SL_HIT. Если TP и SL на одном баре — **SL первым** (§20.3) | — |

### CONTINUATION (LONG)

| Стадия | Условие | Guard |
|---|---|---|
| Контекст | Swing trend = BULLISH, `regime ≠ RANGING` (иначе штраф −0.5). Conservative: `htfBias == BULL` | — |
| BOS_SEEN | Swing BOS↑ (или internal BOS↑ при swing BULLISH) с `dispStrength ≥ 1.0` | — |
| FORMING | POI ноги BOS в discount диапазона, перестроенного этим BOS | Нет POI → EXPIRED |
| READY | `SL = protectedLow − buffer` (STRUCTURAL). Цели: weak high → следующая BSL → HTF BSL | Как у SWEEP_REVERSAL |
| INVALIDATED | `c < protectedLow` или CHoCH↓ (swing) или POI BROKEN | — |
| Бонус | Снятие internal-SSL на откате (до входа) → фактор SWEEP +1.0 | — |

## A.19 Параметры по умолчанию

| Параметр | По умолч. | Диапазон | Ед. |
|---|---:|---|---|
| `atrLen` | 14 | 5–200 | бары |
| `Ls` / `Li` (Intraday) | 10 / 3 | 2–50 / 2–20 | бары |
| Break source | Close | Close / Wick | — |
| `eqTol` | 0.10 | 0.02–0.5 | VU |
| `kLeg` (MSS) | 1.5 | 0.5–5 | VU |
| `kBody` / `minBodyRatio` | 1.0 / 0.6 | 0.3–3 / 0.3–0.95 | VU / доля |
| `obZone` | Body+Wick | Full / Body+Wick / Body | — |
| `nPre` / `obMaxSearch` | 3 / 30 | 0–10 / 5–100 | бары |
| `obMin` / `obMax` | 0.25 / 3.0 | 0–2 / 0.5–10 | VU |
| `obDispMin` | 1.0 | 0–5 | VU |
| `volMult` | 1.5 | 1–5 | × SMA(v, 20) |
| Mitigation rule | 50% | Touch / 50% / Full | — |
| `obMaxAge` / `fvgMaxAge` | 500 / 300 | 50–5000 | бары |
| `zoneMaxDist` / `liqMaxDist` | 20 / 20 | 5–100 | VU |
| `fvgMin` | 0.30 | 0–2 | VU |
| Fill rule | Wick far edge | Wick / Close / CE | — |
| `liqTol` / `eqMaxBars` | 0.15 / 100 | 0.02–0.5 / 10–1000 | VU / бары |
| `oldAge` | 50 | 10–500 | бары |
| `maxSweepPen` | 1.0 | 0.1–5 | VU |
| `reclaimBars` | 2 | 1–10 | бары |
| `tsMinAge` / `tsWindow` | 20 / 10 | 5–200 / 3–50 | бары |
| `liqMaxAge` | 1000 | 100–10000 | бары |
| `oteLo` / `oteHi` / sweet | 0.62 / 0.79 / 0.705 | 0.5–0.9 | доля |
| `eqBand` | 0.02 | 0–0.1 | доля |
| Session timezone | America/New_York | IANA | — |
| `minHtfBars` | 100 | 20–500 | HTF-бары |
| `rangeBars` / `chopBars` | 8 × Ls / 6 × Ls | — | бары |
| `Nshift` / `shiftDispMin` | 20 / 1.0 | 3–100 / 0–5 | бары / VU |
| `expiryBars` | 30 | 5–500 | бары |
| `minRR` | 2.0 | 0.5–10 | R |
| `maxSlAtr` / `minSlTicks` | 3.0 / 5 | 0.5–10 / 1–100 | VU / тики |
| SL buffer | 0.10 VU / 2 tick | — | — |
| Warm-up | `max(300, 20 × Ls)` | — | бары |
