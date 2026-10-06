# Changelog

Формат: [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/). Версии — SemVer. Схема webhook версионируется отдельно (docs §12).

## [0.1.0] — 2026-10-06 · Alpha «Structure · Liquidity · Zones»

Первая сборка по плану `docs/06-roadmap-plan.md`: фазы P0–P4 и ядро визуального слоя (P6a/P6b). **Не проверена компилятором TradingView** — только офлайн-проверка синтаксиса (pynescript) и lint проекта. Первая компиляция в TradingView — шаг 1 в `tests/README.md`.

### Добавлено
- **Сборка** (`build/build.py`): модули `src/*.pine` → `dist/SMC_Visualizer_Pro.pine`, версия и дата, отчёт о размере, lint (запрет `varip`/`timenow`, `lookahead_on` без `[1]`, отступы, неохраняемые циклы), опциональная проверка синтаксиса.
- **Ядро:** реестр объектов с ID, шина событий (очередь бара + кольцевая история), warm-up, журнал событий в Pine Logs (Debug).
- **Data Engine:** ATR как единица волатильности, displacement, межсессионные гэпы, относительный объём с авто-деградацией, сырые FVG-паттерны, пивоты, часы сессий (NY time + DST), PDH/PDL/PWH/PWL с подтверждённых D/W-баров.
- **Structure Engine** (A.2–A.5): internal и swing, HH/HL/LH/LL/EQH/EQL, BOS / CHoCH / MSS, первый пробой, Close/Wick, protected levels, ноги пробоя с displacement.
- **Liquidity Engine** (A.12–A.13): уровни из swing-пивотов, кластеры EQH/EQL, key levels (PDH/PDL, PWH/PWL, Asia/London/NY high/low), автомат ACTIVE → PENDING_RECLAIM → SWEPT / TAKEN, свипы wick / reclaim / turtle soup, major/minor.
- **Zone Engine** (A.7, A.8, A.10): OB с окном ноги и фильтрами (размер, displacement, объём, целостность), lifecycle Fresh → Touched → Mitigated → Broken, конверсия в Breaker / Mitigation Block, FVG с правилами заполнения и незаполненным остатком, IFVG.
- **Context Engine** (A.14, A.16, A.17): dealing range (developing/established), Premium/Discount/EQ, OTE, режим RANGING, снимок MarketContext.
- **Visual Engine:** токены дизайн-системы, авто-тема, палитры Standard и Color-blind safe, пулы объектов с отрисовкой только на последнем баре, Relevance Score, Nearest-N на сторону, окно дистанции, TTL, слияние перекрывающихся зон (`OB×2`, `+FVG`), Smart Labels для правых тегов, режимы Clean / Normal / Analysis / Debug / Custom.
- **Панели:** Context Ribbon, Dashboard (Compact/Expanded, лента событий в Analysis), Debug-таблица (бюджеты, реестры, здоровье данных), Range Gauge.
- **Алерты:** 11 `alertcondition()` по событиям шины (только на закрытии бара, не во время warm-up).

### Отклонения от спецификации (осознанные, временные)
- Рендер — «immediate mode» с пулами: каждый проход на последнем баре заново раскладывает объекты по пулам. Dirty-check по `renderHash` (§4.9) отложен до замеров Pine Profiler.
- `behind_chart` и жирный шрифт (`text_formatting`) не используются до технической проверки S-5: заливки и так прозрачнее свечей (PA-1).
- В Clean Dashboard скрыт строго по ADR-09 (режим — потолок видимости). Dashboard в «чистом» графике — через режим Custom. Уточнение к §18.1.
- Вид сессий «Background» отложен: доступны Range box и Off.
- HTF Feed (P5), сетапы (P7), батч-webhook JSON (P9), Setup Path и Inspect (P10) — следующие версии.
