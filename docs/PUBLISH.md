# Публикация на TradingView

Тексты страниц скриптов (английский обязателен по правилам TradingView House Rules) и чек-лист релиза. Публикация — **invite-only** (ADR-04): код закрыт, доступ выдаётся по списку.

Правила формулировок: никаких обещаний доходности и процентов выигрыша. Оценка сетапа — «насколько полно собран сетап», а не вероятность. Статистика STATS — только по загруженной истории, без проскальзывания и комиссий. Ссылки на сторонние сайты, Telegram и контакты на странице скрипта запрещены.

---

## 1. SMC Visualizer Pro

**Title:** `SMC Visualizer Pro`

**Short description (≤ 160 chars):** Smart Money Concepts market map: structure, liquidity and sweeps, order blocks and FVG, premium/discount, sessions and the higher timeframe — without clutter.

**Description:**

> SMC Visualizer Pro draws the Smart Money Concepts picture of the market and keeps it readable. It shows what matters now and fades or hides the rest.
>
> **What it shows**
> • **Structure.** BOS, CHoCH and MSS for swing and internal structure. HH / HL / LH / LL and EQH / EQL swing labels. Strong / Weak High / Low on the current dealing range.
> • **Liquidity.** Buy-side and sell-side levels and equal highs / lows (≡N). Previous day and week highs and lows, session highs and lows.
> • **Sweeps.** A sweep (wick or reclaim, ✕) is kept apart from a level that was taken. Turtle-soup sweeps are classified.
> • **Zones.** Order blocks, Breaker and Mitigation blocks, fair value gaps and inversion FVG. Each zone follows its lifecycle (touched, mitigated, filled, broken) with a selectable mitigation and fill rule.
> • **Context.** Dealing range with premium / discount, equilibrium and the OTE band, plus a range gauge with the current location. Market regime (trending / ranging).
> • **Sessions.** Asia, London and New York AM killzones in New York time, with daylight saving.
> • **Higher timeframe.** HTF structure, order blocks, FVG and liquidity come from confirmed HTF bars only, so they do not repaint. The HTF is picked automatically or set manually.
> • **Panels.** A one-line Context Ribbon and a Dashboard with answers instead of numbers: market, HTF bias, structure, session, location, last liquidity event, nearest targets. In Analysis mode it adds an event timeline.
>
> **Display modes**
> Clean → Normal → Analysis → Debug. The mode sets a ceiling for how much is drawn; calculations never change between modes. Analysis adds internal structure, swing labels, displacement markers and history. Debug adds object IDs, relevance scores, a budget table and self-checks.
>
> **How it works**
> • All logic runs on confirmed bars. Drawing happens once on the last historical bar and once per closed realtime bar: nothing is redrawn between ticks, and scrolling or zooming does not re-run the script.
> • History is drawn over a window of the last N bars (default 1500), evenly spread over time.
> • Thresholds are in ATR, so the same settings work across instruments and timeframes.
>
> **Companion indicator**
> SMC Pro · Setups builds analytical trade setups on the same structure. Both indicators show a settings signature (cfg). Equal numbers mean the setups are built on exactly the markup this indicator draws.
>
> **Alerts**
> BOS / CHoCH, sweeps, order-block touch, FVG fill, session start, premium / discount change, OTE entry, HTF bias change and HTF structure breaks. Alerts fire on bar close.
>
> **Limitations**
> • The script is limited to 500 boxes, lines and labels, and each mode keeps within a budget.
> • No markup is drawn left of the history window.
> • Non-standard charts (Heikin Ashi, Renko, etc.) are flagged, because their prices are synthetic.
>
> This is an analysis tool. It does not place orders and does not predict prices.

---

## 2. SMC Pro · Setups

**Title:** `SMC Pro · Setups`

**Short description:** Analytical SMC setups — Sweep Reversal and Continuation — with entry, stop, targets, an explainable confluence score and a webhook message.

**Description:**

> SMC Pro · Setups turns the Smart Money Concepts structure into explicit, explainable setups. It is designed to run together with SMC Visualizer Pro and uses the same engine settings (check that the cfg number is equal in both).
>
> **Models**
> • **Sweep Reversal:** a liquidity sweep, then a CHoCH / MSS against it within N bars, then an FVG or order block of that leg in discount (long) or premium (short).
> • **Continuation:** a BOS with the trend, then an FVG or order block of the leg in discount / premium.
>
> **Lifecycle**
> FORMING → READY → ACTIVE → DONE. A setup is cancelled before the entry by a close beyond its invalidation level, an opposite swing CHoCH or a broken entry zone. Every setup that ends without a trade records its reason (no shift in window, RR too low, grade too low, …).
>
> **On the chart**
> • The entry zone is framed over the zone SMC Visualizer Pro draws.
> • Entry, stop and up to three targets (liquidity-based, or 1R / 2R / 3R), with reward and risk boxes.
> • A card with side, grade, score and the chain, e.g. "Sweep → CHoCH → FVG → OTE".
> • **Setup Path** numbers the sweep, the break, the zone and the entry: ① ② ③ ④.
> • Finished setups show their outcome.
>
> **Confluence score (0–10) and grade**
> Context (HTF bias, discount / premium, OTE), liquidity (sweep size, a target to draw on), structure (swing or internal, leg strength), POI (FVG ∩ OB, inside an HTF zone), killzone timing and RR. Penalties apply for an HTF zone against the trade and for ranging conditions. Grades: A+ ≥ 8, A ≥ 6.5, B ≥ 5. Presets: Balanced, Conservative, Aggressive.
> The score measures how complete a setup is. It is **not** a probability of success.
>
> **Panel and tools**
> • A setup panel shows the setup, its quality, plan and invalidation.
> • Statistics over the loaded history: setups that reached READY, closed trades by grade and model with the share won and average R. Entries are taken at the plan price, without slippage or fees.
> • **Inspect** explains the setup at a chosen time, or why there was none.
>
> **Alerts and webhook**
> Setup READY (any side, LONG or SHORT), TRIGGERED and INVALID. Or one "Any alert() function call" alert: one message per bar close, as readable text or a JSON envelope (smcvp.event v1) with the trade plan, for your own gateway or bot. Optional heartbeat snapshots.
>
> **Notes**
> • Logic runs on confirmed bars only. Alerts and the webhook fire on bar close.
> • Setups are analytical: nothing is executed.
> • Past statistics describe the loaded history only. They do not guarantee future results.

---

## 3. Чек-лист релиза

| # | Шаг | Где |
|---|---|---|
| 1 | Версия в `VERSION`, запись в `CHANGELOG.md`, `python3 build/build.py --check` без LINT и ошибок | репозиторий |
| 2 | Оба файла компилируются в TradingView без ошибок и предупреждений; время компиляции записано | `tests/README.md` |
| 3 | Чек-лист текущей версии пройден | `tests/README.md` |
| 4 | Скриншоты: 3+ инструмента × Clean / Normal / Analysis × тёмная / светлая тема (+ Color-blind safe) | для страницы скрипта |
| 5 | Тексты разделов 1 и 2 сверены с текущими функциями (новые функции добавлены, удалённые убраны) | этот файл |
| 6 | Publish → **Invite-only**, категория Indicators, теги: smc, smart money concepts, order blocks, fair value gap, liquidity, market structure | TradingView |
| 7 | Обновление существующей публикации — **Update** той же страницы, а не новый скрипт; в Release notes — краткий список из CHANGELOG | TradingView |
| 8 | Пользователям: пересохранить и пересоздать алерты (алерт работает с той версией, на которой создан) | Release notes |
