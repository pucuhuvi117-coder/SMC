# SMC Visualizer Pro — архитектурное ТЗ v2.0

> **Статус:** разработка, alpha v0.2.0. Дата ревизии: 2026-10-06.
> **Платформа:** TradingView · Pine Script v6 · indicator (v1.x) → strategy + автоматизация через внешний шлюз (v2.0+).
> **Источник требований:** исходное ТЗ v1 — [`docs/00-source-tz-v1.md`](docs/00-source-tz-v1.md).

## Статус разработки

| Версия | Содержание | Состояние |
|---|---|---|
| 0.1.0 | Ядро, структура, ликвидность, зоны, контекст, визуальный слой, Ribbon, Dashboard, алерты | Компилируется и работает в TradingView |
| **0.2.0** | История на всём видимом графике, архив объектов, настройка Visibility, цвета сессий, подписи вне свечей | Собрана, синтаксис проверен офлайн, ждёт проверки в TradingView |
| 0.3.0 | HTF Feed (P5) | Следующая |
| 0.4.0 | Сетапы, скоринг, Entry/SL/TP (P7–P8) | План |

**Быстрый старт:** скопируйте `dist/SMC_Visualizer_Pro.pine` в Pine Editor → Add to chart. Чек-лист проверки — [`tests/README.md`](tests/README.md). Как устроен код — [`DEVELOPMENT.md`](DEVELOPMENT.md). Изменения — [`CHANGELOG.md`](CHANGELOG.md).

## Зачем этот пакет документов

ТЗ v1 — хороший каталог SMC/ICT-функций, но не спецификация системы. «Как написано» он даёт график-паутину, который нельзя без переписывания развить в стратегию и автоматизацию (см. аудит, [`docs/01-audit.md`](docs/01-audit.md)).

ТЗ v2 перестраивает проект вокруг трёх идей:

1. **Индикатор рассказывает историю движения цены.** Трейдер за секунды видит HTF bias, структуру, ликвидность, сетап и *почему* он появился: `Liquidity → Sweep → Displacement → CHoCH/BOS → OB/FVG → OTE → Entry → SL/TP`.
2. **Логика отделена от визуала.** Ядро вычисляет состояние и события. Visual Engine только отображает их и **никогда** не принимает торговых решений.
3. **Готовность к автоматизации с первого дня.** Setup → Signal → TradePlan → Risk → Execution — независимые слои с версионированными контрактами.

Главный UX-принцип: **«Не показывай всё, что умеет индикатор. Показывай то, что трейдеру действительно необходимо увидеть в данный момент»**. Режимы **Clean → Normal → Analysis → Debug** переключаются без изменения расчётов.

## Карта документов: 29 результатов анализа

| # | Результат | Документ |
|---:|---|---|
| 1 | Полный аудит существующего проекта | [01-audit.md §1](docs/01-audit.md#1-полный-аудит-существующего-проекта) |
| 2 | Список недостающих компонентов | [01-audit.md §2](docs/01-audit.md#2-список-недостающих-компонентов) |
| 3 | Список архитектурных изменений | [01-audit.md §3](docs/01-audit.md#3-список-архитектурных-изменений) |
| 4 | Новая архитектура SMC Visualizer Pro | [02-architecture.md §4](docs/02-architecture.md#4-новая-архитектура-smc-visualizer-pro) |
| 5 | Архитектура будущей автоматической торговли | [02-architecture.md §5](docs/02-architecture.md#5-архитектура-будущей-автоматической-торговли) |
| 6 | Event Model | [03-domain-models.md §6](docs/03-domain-models.md#6-event-model) |
| 7 | State Machine | [03-domain-models.md §7](docs/03-domain-models.md#7-state-machines) |
| 8 | Object Model | [03-domain-models.md §8](docs/03-domain-models.md#8-object-model) |
| 9 | Setup Model | [03-domain-models.md §9](docs/03-domain-models.md#9-setup-model) |
| 10 | TradePlan Model | [03-domain-models.md §10](docs/03-domain-models.md#10-tradeplan-model) |
| 11 | Risk Model | [03-domain-models.md §11](docs/03-domain-models.md#11-risk-model) |
| 12 | Webhook Model | [03-domain-models.md §12](docs/03-domain-models.md#12-webhook-model) |
| 13 | Visual Design System | [04-visual-design-system.md](docs/04-visual-design-system.md) |
| 14 | UX/UI Specification | [05-ux-ui-spec.md §14](docs/05-ux-ui-spec.md#14-uxui-specification) |
| 15 | Anti-Clutter System | [05-ux-ui-spec.md §15](docs/05-ux-ui-spec.md#15-anti-clutter-system) |
| 16 | Visual Priority System | [05-ux-ui-spec.md §16](docs/05-ux-ui-spec.md#16-visual-priority-system) |
| 17 | Analysis Mode | [05-ux-ui-spec.md §17](docs/05-ux-ui-spec.md#17-analysis-mode) |
| 18 | Clean Mode | [05-ux-ui-spec.md §18](docs/05-ux-ui-spec.md#18-clean-mode) |
| 19 | Debug Mode | [05-ux-ui-spec.md §19](docs/05-ux-ui-spec.md#19-debug-mode) |
| 20 | Backtesting-ready architecture | [02-architecture.md §20](docs/02-architecture.md#20-backtesting-ready-architecture) |
| 21 | Roadmap v1.0 → v2.0 → v3.0 (+ пошаговый план) | [06-roadmap-plan.md §21](docs/06-roadmap-plan.md#21-roadmap-v10--v20--v30) |
| 22 | Полный Dependency Graph | [06-roadmap-plan.md §22](docs/06-roadmap-plan.md#22-dependency-graph) |
| 23 | Critical Path | [06-roadmap-plan.md §23](docs/06-roadmap-plan.md#23-critical-path) |
| 24 | Technical Risks | [07-risks.md §24](docs/07-risks.md#24-technical-risks) |
| 25 | Automation Risks | [07-risks.md §25](docs/07-risks.md#25-automation-risks) |
| 26 | Visual/UX Risks | [07-risks.md §26](docs/07-risks.md#26-visual--ux-risks) |
| 27 | Acceptance Criteria | [08-acceptance-criteria.md §27](docs/08-acceptance-criteria.md#27-acceptance-criteria-функциональные-и-технические) |
| 28 | Visual Acceptance Criteria | [08-acceptance-criteria.md §28](docs/08-acceptance-criteria.md#28-visual-acceptance-criteria) |
| 29 | Master Development Checklist | [09-master-checklist.md](docs/09-master-checklist.md) |
| A | Формальные определения детекторов (BOS, OB, FVG, Sweep, OTE, сессии, сетапы) | [appendix-a-detection-spec.md](docs/appendix-a-detection-spec.md) |

## Ключевые решения (кратко)

| Решение | Где |
|---|---|
| Слои Data → Analytical Core → Decision → Risk → Execution. Visual / Alerts / Dashboard / Analytics — read-only подписчики Event Bus | §4.2–4.4 |
| Логика — только на подтверждённом баре. Визуал — один полный рендер на последнем подтверждённом историческом баре, затем инкременты | §4.5, ADR-02 |
| MTF — подтверждённые HTF-бары (`[1]` + `lookahead_on`) и **тот же код движков** | §4.7, ADR-03 |
| Тип и состояние объектов разделены; Breaker и Mitigation Block — исходы пробоя OB | §7.3, A.8 |
| Свип ≠ пробой: SWEPT (wick / reclaim) vs TAKEN, глубина в ATR | §7.2, A.13 |
| Сессии в `America/New_York` с DST | A.15, ADR-06 |
| Бюджет отрисовки по режимам. Relevance Score (визуал) ≠ Confluence Score (логика) | §4.10, §16, ADR-11 |
| Цвет = смысл, форма = тип, прозрачность = состояние × релевантность, толщина = TF / tier | §13 |
| Сетап — единая композиция Entry / SL / TP с карточкой `LONG · A+ 8.4 · Sweep → CHoCH → FVG → OTE` | §14.8 |
| Webhook: схема `smcvp.event` v1, один батч на бар, `msg_id`, `cfg_hash`, SNAPSHOT | §12 |
| Модульные исходники → монолитная сборка (IP invite-only) | §4.11, ADR-04 |

## Объём и сроки v1.0

≈ **60 человеко-дней**: 1 разработчик — около 12 недель; 2 разработчика — 42 рабочих дня по критическому пути (≈ 48 с буфером). MVP-срез — ≈ 42–45 ч/д. Детали — [`docs/06-roadmap-plan.md`](docs/06-roadmap-plan.md).

## Формат сдачи v1.0

Собранный `.pine`, модульные исходники, README RU/EN, CHANGELOG, скриншоты по режимам и темам, golden-журналы событий, QA-отчёт, описание пресетов и демонстрационных алертов. **Видео-демонстрация исключена** по решению заказчика.
