# 09 · Master Development Checklist

> Покрывает результат анализа **№29**.
> Чек-лист для команды разработки и QA. Пункт закрывается только при выполнении DoD фазы (`06-roadmap-plan.md` §21.9).
> Обозначения: **[A]** Dev A (Core), **[B]** Dev B (Visual/Integration), **[Q]** QA, **[A+B]** совместно.

---

## 0. Перед стартом (Gate 0)

- [ ] Заказчик утвердил ТЗ v2 (`docs/01…09`, Appendix A).
- [ ] Утверждены значения по умолчанию (A.19), пресеты структуры и сессий.
- [ ] Утверждён формат сдачи (§21.11). Видео-демонстрация **исключена**.
- [ ] Определены участники VAC-тестов (≥ 5, из них ≥ 2 без опыта работы с индикатором).
- [ ] Определены golden-отрезки (6 инструментов × 3 ТФ × 500 баров, фиксированные даты).
- [ ] Выбран эталонный тариф TradingView для замеров производительности и проверки лимитов.

## P0 · Foundations & Spikes

**Инфраструктура**
- [ ] [A] Репозиторий: `/src`, `/build`, `/dist`, `/tests`, `/docs`, `CHANGELOG.md`.
- [ ] [A] Build-скрипт: конкатенация по `targets`, подстановка версии, отчёт о размере.
- [ ] [A] Шаблон заголовка модуля: назначение, зависимости, публичные функции.
- [ ] [A] Соглашения по именованию (префиксы модулей, enums, UDT).

**Спайки**
- [ ] [A] S-1 HTF Feed: кортеж `[1]` + `lookahead_on`, смена HTF-бара, Bar Replay diff.
- [ ] [A] S-2 Глубина HTF-истории, fallback-пивоты.
- [ ] [B] S-3 Full render 450 объектов, rollback на тиках, стоимость инкремента.
- [ ] [B] S-4 Smart Labels: высота строки, abovebar/belowbar, коллизии.
- [ ] [B] S-5 `behind_chart`, `text_formatting`, размер текста в pt, `style_text_outline`, z-order.
- [ ] [B] S-6 Setup Path: lines vs polyline, `xloc.bar_time`, проекция в будущее.
- [ ] [A] S-7 Лимиты компиляции на синтетическом монолите.
- [ ] [A] S-8 Алерты: размер сообщения, Content-Type, троттлинг батча на M1.
- [ ] [B] S-9 Стоимость viewport-aware рендера.
- [ ] [A+B] Протокол спайков, обновлённые ADR (§4.13), обновлённый реестр рисков (§24).

**Ядро-каркас**
- [ ] [A] `02_types`: все enums (§8.2) и UDT (§8.3–8.4).
- [ ] [A] `01_config`: inputs по §14.4 с группами, inline, tooltip, `display.none`.
- [ ] [A] Display Profiles и правило ADR-09 (`mode.allows AND user.show`).
- [ ] [A] Пресеты структуры (Scalp / Intraday / Swing / Manual) и сессий (ICT NY / Original UTC / Custom).
- [ ] [A] Авто-HTF (§4.7) и валидация конфигурации (§14.4).
- [ ] [A] `03_registry_bus`: Registry с ёмкостями и вытеснением (§8.5), ключи (ADR-12).
- [ ] [A] Event Bus: `barEvents`, `history`, `lastByType`, ordinal, запрет эмиссии на неподтверждённом баре.
- [ ] [A] `10_data_engine`: ATR, геометрия, `isDispBar`, `volRatio` (+ авто-деградация), `isGapBar`, сессионные часы, тип графика.
- [ ] [A] Warm-up guard (§4.8).
- [ ] [B] Debug-таблица: effective config, размеры реестров, `isWarm`.
- [ ] [A] `log.info`-формат журнала событий (§19.1).

**QA**
- [ ] [Q] Ручная golden-разметка, два разметчика, decision log.
- [ ] [Q] Golden-журналы в формате `log.info` CSV.
- [ ] [Q] Синтетические сценарии (§27.3) подобраны на реальных отрезках.

## P1 · Structure Engine

- [ ] [A] Пивоты по правилу A.2 (internal и swing независимо).
- [ ] [A] HH/HL/LH/LL, EQH/EQL с `tolEQ` (A.3).
- [ ] [A] Автомат структуры (§7.1): UNDEFINED / BULLISH / BEARISH.
- [ ] [A] BOS / CHoCH / BOS initial, один пробой на пивот (A.4).
- [ ] [A] Break source Close / Wick.
- [ ] [A] Нога пробоя, `dispStrength`, `legHasFvg`, MSS.
- [ ] [A] Protected levels, weak high/low, опция CHoCH reference (A.5).
- [ ] [A] Флаг `shadowed` для дублей internal/swing.
- [ ] [A] События SWING, BOS, CHOCH с `causeId`.
- [ ] [A] Ассерты: один пробой на пивот, валидные переходы автомата.
- [ ] [Q] Golden diff ≥ 95% (AC-11), наборы длин 5 / 10 / 20 (AC-12).
- [ ] [Q] Bar Replay: 0 расхождений (AC-06, частично).

## P2 · Liquidity Engine

- [ ] [A] Уровни из swing-пивотов (major-кандидаты) и internal (minor, опц.).
- [ ] [A] EQ-кластеры: `liqTol`, `eqMaxBars`, touches, цена кластера, `LIQ_EQ`.
- [ ] [A] Key Levels: PDH/PDL, PWH/PWL (D/W-фиды по идиоме `[1]`), граница дня Exchange / NY midnight.
- [ ] [A] Session H/L → Key Levels (AH/AL, LOH/LOL, NYH/NYL), MOP.
- [ ] [A] `isMajor` (A.12), expiry.
- [ ] [A] Автомат уровня (§7.2): SWEPT (WICK / RECLAIM), PENDING_RECLAIM, TAKEN, EXPIRED, ARCHIVED.
- [ ] [A] Turtle Soup-классификация (A.13 п.6).
- [ ] [A] Несколько свипов на баре: порядок событий, приоритет важности.
- [ ] [A] События LIQ_*, KEYLEVEL_SET.
- [ ] [Q] Синтетика sweep / taken 100% (AC-14), golden ≥ 95%.
- [ ] [Q] Key Levels сверены с D/W-барами (AC-16).

## P3 · Zone Engine

- [ ] [A] Единая модель `Zone` (kind, state, геометрия, атрибуты качества).
- [ ] [A] OB: окно поиска, последняя противоположная свеча, fallback (A.7).
- [ ] [A] Режимы зоны Full / Body+Wick / Body. Опция «Extend to leg low».
- [ ] [A] Фильтры: размер (авто-Body), displacement, объём (авто-деградация), целостность.
- [ ] [A] Дедупликация OB internal/swing.
- [ ] [A] Lifecycle OB (§7.3), правила mitigation Touch / 50% / Full.
- [ ] [A] Конверсия BB / MB по флагу снятия ликвидности (A.8).
- [ ] [A] FVG: паттерн, размер, средняя свеча, сессионные гэпы, displacement-тег (A.10).
- [ ] [A] Lifecycle FVG (§7.4), fill rules, незаполненный остаток.
- [ ] [A] IFVG.
- [ ] [A] Strength (A.7 п.8), аннотация `htfContainerId`.
- [ ] [A] Вытеснение зон по политике §8.5.
- [ ] [A] События ZONE_*.
- [ ] [Q] OB-определение 100% (AC-17), FVG и гэпы (AC-18), ассерты lifecycle (AC-19), конверсия (AC-20), объём (AC-21).

## P4 · Context Engine

- [ ] [A] Dealing range: построение, DEVELOPING → ESTABLISHED → SUPERSEDED (A.14, §7.5).
- [ ] [A] `pd%`, PREMIUM / DISCOUNT / EQ с `eqBand`.
- [ ] [A] OTE-полоса и sweet spot для бычьего и медвежьего диапазона.
- [ ] [A] Сессии в таймзоне сессий с DST, пресеты, `minutesLeft` (A.15).
- [ ] [A] Отключение сессий на ТФ > 1H.
- [ ] [A] HTF bias, `htfReliable`, HTF2-подтверждение (A.16).
- [ ] [A] Режим RANGING / TRENDING (A.17), MARKET bias.
- [ ] [A] `MarketContext` (§8.3) на каждом подтверждённом баре.
- [ ] [A] Аннотация `pdLocation` для зон.
- [ ] [A] События RANGE_NEW, PD_ENTER, OTE_ENTER, SESSION_*, HTF_BIAS, REGIME.
- [ ] [Q] DST-кейсы (AC-23), формулы PD/OTE (AC-22), режимы (AC-24).

## P5 · HTF Feed

- [ ] [B] Один `request.security` на HTF: кортеж OHLCV + time + ATR подтверждённого бара.
- [ ] [B] Детекция закрытия HTF-бара, буфер HTF-баров.
- [ ] [B] Прогон Structure / Liquidity / Zone с TF slot = HTF1 (общий код).
- [ ] [B] HTF2-фид для bias (опц.).
- [ ] [B] Контроль глубины, ⚠ `HTF history low`, fallback S-2.
- [ ] [B] HTF ≤ chart TF → off + ⚠ (AC-26).
- [ ] [B] Бюджет `request.*`: ≤ 4 вызова в v1.0.
- [ ] [Q] History vs Bar Replay HTF-события 100% (AC-25), низкая история (AC-27).

## P6a · Visual Foundation

- [ ] [B] `60_visual_tokens`: палитры Standard и CVD, opacity, линии, типографика (§13).
- [ ] [B] Theme Resolver: Auto по яркости `chart.bg_color`, ручное переопределение.
- [ ] [B] Пулы box / line / label по z-слоям (§13.13).
- [ ] [B] `ViewHandle`, `renderHash`, dirty-check.
- [ ] [B] Full render на `barstate.islastconfirmedhistory`, инкремент на подтверждённом realtime-баре, live-слой на тиках.
- [ ] [B] Координаты: `xloc.bar_time` для истории, проекция вправо ≤ 25 баров.
- [ ] [B] Правый край зон — общая вертикаль `now + 5`.
- [ ] [B] Базовые рендереры: структура, уровни, зоны (по §13.8, §13.12).
- [ ] [B] `behind_chart` и прочее по итогам S-5.

## P6b · Visual Intelligence

- [ ] [B] Relevance Score: компоненты H/P/F/A/S/L/U, веса по видам (§16.2–16.3).
- [ ] [B] Маппинг R → класс → RenderSpec (§16.4), смещения по режимам.
- [ ] [B] Pinning объектов цепочки активного сетапа.
- [ ] [B] Конвейер Anti-Clutter (§15.2): фильтр режима, история, дистанция, слияние, кластеризация, HTF-доминирование, Nearest-N, бюджет, гистерезис.
- [ ] [B] TTL отработанных объектов по режимам.
- [ ] [B] Затухание структурных меток (AC-M14).
- [ ] [B] Smart Labels: якоря, коллизии (слияние / сдвиг / скрытие), стопка правых тегов (§14.7).
- [ ] [B] Уровни текста L0–L3, тултипы у всех меток.
- [ ] [B] Режимы Clean / Normal / Analysis / Debug / Custom по матрице §19.2.
- [ ] [B] Draw Budget Manager, ассерт превышения.
- [ ] [Q] VAC dry-run: VAC-1, 2, 3, 4, 6, 7, 17.

## P7 · Setup / Confluence / Signal / Risk

- [ ] [A] Автомат сетапа (§7.7), стадии UI (FORMING / READY / ACTIVE / DONE).
- [ ] [A] SWEEP_REVERSAL по A.18.
- [ ] [A] CONTINUATION по A.18.
- [ ] [A] Выбор POI (§9.4), альтернативный POI.
- [ ] [A] Конкуренция и замещение сетапов (§9.3).
- [ ] [A] Confluence: факторы, штрафы, clamp, грейды (§9.5), пресеты (§9.6).
- [ ] [A] `chain` и `chainText` строго из `causeId`.
- [ ] [A] Signal Engine: мин. грейд, сессионный фильтр, кулдаун, дедупликация.
- [ ] [A] Risk Engine: режимы SL и буферы, цели TP (§10.4–10.5), RR, проверки (§11.3).
- [ ] [A] TradePlan (DRAFT): все поля §10.2, `cancelRules`.
- [ ] [A] Execution Adapter: интерфейс, no-op.
- [ ] [A] Отслеживание TP/SL после входа с политикой §20.3 (для визуальных состояний).
- [ ] [A] Причины завершения (reason) и «почему нет сетапа» (guards).
- [ ] [Q] Цепочки (AC-28), инвалидация / экспирация / MISSED (AC-29), риск (AC-30), скоринг (AC-31), конкуренция (AC-32).

## P8 · Setup Composer · Dashboard · Ribbon · Gauge

- [ ] [B] Композиция сетапа: entry-зона, E / SL / TP-линии, reward/risk-боксы, карточка (§14.8).
- [ ] [B] Визуальные состояния композиции (FORMING … EXPIRED).
- [ ] [B] Price-scale markers (служебные plot'ы, опц.).
- [ ] [B] Dashboard Compact / Expanded (§14.5), схлопывание строк, тултипы.
- [ ] [B] Context Ribbon (§14.6), сегмент ⚠.
- [ ] [B] Range Gauge (§14.13).
- [ ] [B] Позиции панелей только в углах / по краям, проверка VAC-11.
- [ ] [B] Словарь текстов (EN), каркас для RU/ES.
- [ ] [Q] VAC-2, 9, 10, 11, 12.

## P9 · Alerts & Webhook

- [ ] [A] 15 `alertcondition()` с константными сообщениями (§12.7).
- [ ] [A] Батч-`alert()`: не более одного вызова на бар, только на закрытии бара.
- [ ] [A] Форматы Text / JSON, фильтры событий, мин. tier и грейд.
- [ ] [A] Сериализация по схеме v1 (§12.2–12.5): числа, `null`, экранирование, время.
- [ ] [A] `msg_id`, `build`, `cfg_hash`, `seq`.
- [ ] [A] SNAPSHOT-heartbeat.
- [ ] [A] Усечение по Tier при превышении размера (по итогам S-8).
- [ ] [Q] Тестовый приёмник с JSON Schema-валидацией (AC-33…AC-36), 24 ч на M1.

## P10 · Analysis & Debug Tooling

- [ ] [B] Setup Path: маркеры ①…⑨, стрелки, тултипы (§17.2).
- [ ] [B] Event Timeline в Dashboard Expanded.
- [ ] [B] Focus latest setup, Inspect at time (`input.time` с `confirm`).
- [ ] [B] Прошлые сетапы (до 10) с итогом.
- [ ] [B] Draw on Liquidity, альтернативный POI.
- [ ] [B] Debug: ID-аннотации, ghost-объекты с причиной, Budget table, effective config.
- [ ] [A] Debug: `log.info`-поток, ассерты `log.error`, «почему нет сетапа».
- [ ] [Q] VAC-15, журналы Normal == Debug (AC-09).

## P11 · QA, производительность, исправления

**Функциональность**
- [ ] [Q] AC-01…AC-40 по матрице §27.4.
- [ ] [Q] Golden-регрессия на всех отрезках.
- [ ] [Q] Repaint-аудит: Bar Replay ≥ 200 баров × 6 инструментов + запись живого рынка ≥ 1 сессии.
- [ ] [Q] Синтетические сценарии §27.3 — 100%.
- [ ] [Q] Нестандартные графики, нет объёма, низкая HTF-история, M1…MN.

**Визуал**
- [ ] [Q] VAC-1…VAC-20 (§28) с протоколами, ≥ 5 участников.
- [ ] [Q] Dark / Light / CVD / Grayscale.
- [ ] [Q] Устройства: 1920×1080, 1366×768, 4K, мобильное приложение.

**Производительность**
- [ ] [A+B] Pine Profiler: M15/5000 ≤ 3 с, H1/10000 ≤ 5 с, доли Logic / Visual (AC-03).
- [ ] [A+B] 20 000 баров: нет таймаутов, бюджеты соблюдены (AC-02).
- [ ] [A+B] Запас по размеру компиляции ≥ 20% (AC-01).

**Исправления**
- [ ] [A+B] Все дефекты Critical/High закрыты, Medium — закрыты или отложены с решением заказчика.
- [ ] [Q] QA-отчёт.

## P12 · Документация и релиз

- [ ] [A+B] README RU/EN: модули, режимы, словарь, Repaint Policy, алерты и пересоздание, webhook-схема, ограничения, FAQ.
- [ ] [A+B] Tooltips 100% inputs (AC-38).
- [ ] [A+B] CHANGELOG, версия `1.0.0`, версия схемы webhook `1.0`.
- [ ] [Q] Скриншоты: 6+ инструментов × Clean / Normal / Analysis × Dark / Light (+ CVD).
- [ ] [Q] Golden-журналы и QA-отчёт в `tests/`.
- [ ] [A] Описание пресетов и демонстрационных алертов.
- [ ] [A] Сборка `dist/SMC_Visualizer_Pro_v1.0.pine`, публикация invite-only, проверка формулировок (без обещаний доходности).
- [ ] ~~Видео-демонстрация~~ — исключено по решению заказчика.

## Сквозные проверки (на каждой фазе)

**Архитектура**
- [ ] Visual / Alert / Dashboard / Analytics не пишут в Registry и Event Bus (T-1).
- [ ] Relevance Score не используется в логике (ADR-11).
- [ ] Нет `varip`, `timenow`, `barstate.isrealtime` в логике. `lookahead_on` — только с `[1]` (§20.8).
- [ ] Логические изменения — только при `barstate.isconfirmed`.
- [ ] Новые пороги заданы в ATR или тиках, а не в процентах цены.
- [ ] Новые события добавлены в каталог §6.4 и таблицу соответствия webhook.

**Качество**
- [ ] Build проходит, размер под контролем.
- [ ] Golden-регрессия не ухудшилась.
- [ ] Ассерты Debug — 0 нарушений.
- [ ] Profiler-бюджеты не превышены.
- [ ] Изменения задокументированы (CHANGELOG, ADR при архитектурных решениях).

**UX**
- [ ] Новые визуальные элементы используют только токены §13.
- [ ] Каждый новый объект имеет tier, правила R и бюджет.
- [ ] Каждый смысл, переданный цветом, продублирован формой, символом или текстом.
- [ ] Новый input имеет tooltip, `display.none`, место в группе §14.4.

## Gate v2.0 (готовность к автоматизации, после v1.5)

- [ ] Outcome Tracker собрал ≥ 300 завершённых сетапов, монотонность «грейд → expectancy» проверена.
- [ ] Strategy-сборка совпадает с Outcome Tracker ≥ 99% по исходам.
- [ ] Спецификация Execution Gateway утверждена (§5.4–5.7).
- [ ] Risk Guard: сценарии отказов протестированы (пропуск, дубль, рассинхрон, kill switch).
- [ ] Shadow-режим 4 недели без инцидентов (§5.5).
- [ ] Юридическая проверка формулировок и модели распространения.
