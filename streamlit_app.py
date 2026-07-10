from __future__ import annotations

from html import escape

import streamlit as st


CAPACITY = {"EMEA": 80, "JAPAC": 40, "NAMER": 40}
REGIONS = tuple(CAPACITY.keys())

MONTHS = [
    {"key": "2026-07", "label": "Jul 2026", "long": "July 2026", "EMEA": 44, "JAPAC": 17, "NAMER": 20},
    {"key": "2026-08", "label": "Aug 2026", "long": "August 2026", "EMEA": 16, "JAPAC": 8, "NAMER": 5},
    {"key": "2026-09", "label": "Sep 2026", "long": "September 2026", "EMEA": 12, "JAPAC": 117, "NAMER": 3},
    {"key": "2026-10", "label": "Oct 2026", "long": "October 2026", "EMEA": 6, "JAPAC": 2, "NAMER": 0},
    {"key": "2026-11", "label": "Nov 2026", "long": "November 2026", "EMEA": 12, "JAPAC": 2, "NAMER": 62},
    {"key": "2026-12", "label": "Dec 2026", "long": "December 2026", "EMEA": 8, "JAPAC": 4, "NAMER": 10},
    {"key": "2027-01", "label": "Jan 2027", "long": "January 2027", "EMEA": 4, "JAPAC": 2, "NAMER": 2},
]

MIGRATIONS = [
    {"name": "Boudl", "count": 51, "region": "EMEA", "date": "Jul 2026", "month_key": "2026-07"},
    {"name": "Minor Hotels", "count": 108, "region": "JAPAC", "date": "Sep 2026", "month_key": "2026-09"},
    {"name": "Voyages", "count": 8, "region": "JAPAC", "date": "Oct 2026", "month_key": "2026-10"},
    {"name": "Vail", "count": 62, "region": "NAMER", "date": "Nov 2026", "month_key": "2026-11"},
    {"name": "Aramark", "count": 40, "region": "NAMER", "date": "Date TBC", "month_key": None},
]


def month_total(month: dict[str, int | str]) -> int:
    return sum(int(month[region]) for region in REGIONS)


def utilization(scheduled: int, region: str) -> float:
    return scheduled / CAPACITY[region] * 100


def state_for(percent: float) -> tuple[str, str]:
    if percent >= 90:
        return "critical", "At Capacity"
    if percent >= 70:
        return "warning", "Approaching"
    return "healthy", "Healthy"


def percent_label(percent: float) -> str:
    rounded = round(percent, 1)
    if rounded.is_integer():
        return f"{rounded:.0f}%"
    return f"{rounded:.1f}%"


def metrics() -> dict[str, object]:
    months = [{**month, "total": month_total(month)} for month in MONTHS]
    peak = max(months, key=lambda month: int(month["total"]))
    risk_months = [
        month
        for month in months
        if any(utilization(int(month[region]), region) >= 90 for region in REGIONS)
    ]
    return {
        "months": months,
        "total": sum(int(month["total"]) for month in months),
        "peak": peak,
        "risk_months": risk_months,
    }


def css() -> str:
    return """
    <style>
      .block-container {
        max-width: 1600px;
        padding-top: 1.25rem;
        padding-bottom: 2rem;
      }
      .dashboard {
        color: #17212b;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }
      .hero {
        display: grid;
        grid-template-columns: auto 1fr auto;
        gap: 1.5rem;
        align-items: center;
        padding: 1.35rem 1.5rem;
        border-bottom: 4px solid #c74634;
        border-radius: .75rem;
        background: #081522;
        color: white;
        box-shadow: 0 10px 26px rgba(8, 21, 34, .18);
      }
      .brand {
        padding-right: 1.3rem;
        border-right: 1px solid rgba(255, 255, 255, .22);
        color: #f15b4e;
        font-size: 1.45rem;
        font-weight: 850;
      }
      .hero h1 {
        margin: 0;
        font-size: clamp(1.45rem, 2.4vw, 2.15rem);
        line-height: 1.12;
      }
      .hero p {
        margin: .35rem 0 0;
        color: #b9c5cf;
      }
      .date-stamp {
        color: #d9e1e7;
        font-size: .85rem;
        text-align: right;
        white-space: nowrap;
      }
      .date-stamp strong {
        display: block;
        color: white;
        font-size: .75rem;
        letter-spacing: .08em;
        text-transform: uppercase;
      }
      .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: .9rem;
        margin-top: 1.25rem;
      }
      .kpi-card,
      .section,
      .brief-card,
      .migration-card {
        background: white;
        border: 1px solid #dfe5ea;
        border-radius: .75rem;
        box-shadow: 0 8px 24px rgba(8, 21, 34, .08);
      }
      .kpi-card {
        min-height: 7.5rem;
        padding: 1rem 1.1rem;
        border-left: 4px solid #17334c;
      }
      .kpi-card.risk {
        border-left-color: #c6382f;
      }
      .kpi-label {
        color: #667585;
        font-size: .75rem;
        font-weight: 800;
        letter-spacing: .06em;
        text-transform: uppercase;
      }
      .kpi-value {
        margin-top: .5rem;
        color: #0d2033;
        font-size: 2rem;
        line-height: 1;
        font-weight: 850;
      }
      .kpi-card.risk .kpi-value {
        color: #c6382f;
      }
      .kpi-note {
        margin-top: .5rem;
        color: #667585;
        font-size: .78rem;
      }
      .section {
        margin-top: 1.35rem;
        overflow: hidden;
      }
      .section-head {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        align-items: end;
        padding: 1rem 1.15rem .8rem;
        border-bottom: 1px solid #e5eaee;
        background: linear-gradient(180deg, #f8fafc, #fff);
      }
      .section-head h2 {
        margin: 0;
        color: #0d2033;
        font-size: 1.25rem;
      }
      .section-head p {
        margin: .25rem 0 0;
        color: #667585;
        font-size: .85rem;
      }
      .legend {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-end;
        gap: .8rem;
        color: #667585;
        font-size: .78rem;
      }
      .legend-item {
        display: inline-flex;
        align-items: center;
        gap: .35rem;
      }
      .dot {
        width: .55rem;
        height: .55rem;
        border-radius: 50%;
        background: #16845b;
      }
      .dot.warning { background: #b26a00; }
      .dot.critical { background: #c6382f; }
      .matrix-shell {
        overflow-x: auto;
      }
      .matrix {
        width: 100%;
        min-width: 1220px;
        border-collapse: separate;
        border-spacing: 0;
        table-layout: fixed;
      }
      .matrix th,
      .matrix td {
        border-right: 1px solid #dfe5ea;
        border-bottom: 1px solid #dfe5ea;
      }
      .matrix tr > *:last-child { border-right: 0; }
      .matrix tbody tr:last-child > * { border-bottom: 0; }
      .matrix thead th {
        height: 4.6rem;
        padding: .7rem .55rem;
        background: #f7f9fa;
        color: #0d2033;
        text-align: center;
        font-size: .82rem;
      }
      .matrix thead th:first-child,
      .matrix tbody th {
        position: sticky;
        left: 0;
        z-index: 2;
        width: 9rem;
        background: #eef2f4;
        text-align: left;
      }
      .matrix tbody th {
        padding: 1rem;
        color: #0d2033;
        font-size: .95rem;
      }
      .month-total,
      .region-note {
        display: block;
        margin-top: .2rem;
        color: #667585;
        font-size: .68rem;
        font-weight: 600;
      }
      .matrix td {
        height: 10.7rem;
        padding: .6rem;
        vertical-align: middle;
      }
      .util-card {
        min-height: 9.35rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 1px solid #dce7e1;
        border-radius: .55rem;
        background: #fbfdfc;
      }
      .util-card.warning {
        border-color: #f0d9af;
        background: #fffdf8;
      }
      .util-card.critical {
        border-color: #efc6c3;
        background: #fffafa;
        box-shadow: inset 0 3px 0 #c6382f;
      }
      .ring {
        --progress: 0;
        --state-color: #16845b;
        position: relative;
        width: 5rem;
        height: 5rem;
        display: grid;
        place-items: center;
        border-radius: 50%;
        background: conic-gradient(var(--state-color) calc(var(--progress) * 1%), #e3e9e6 0);
      }
      .warning .ring { --state-color: #b26a00; }
      .critical .ring { --state-color: #c6382f; }
      .ring::before {
        content: "";
        position: absolute;
        inset: .55rem;
        border-radius: 50%;
        background: white;
      }
      .ring-value {
        position: relative;
        z-index: 1;
        color: #0d2033;
        font-size: 1rem;
        font-weight: 850;
      }
      .critical .ring-value { color: #c6382f; }
      .scheduled {
        margin-top: .45rem;
        font-size: .78rem;
        font-weight: 800;
      }
      .status-label {
        margin-top: .35rem;
        padding: .18rem .45rem;
        border-radius: 999px;
        background: #e8f5ef;
        color: #11633f;
        font-size: .62rem;
        font-weight: 850;
        letter-spacing: .04em;
        text-transform: uppercase;
      }
      .warning .status-label {
        background: #fff3dc;
        color: #865000;
      }
      .critical .status-label {
        background: #fcebea;
        color: #9f2d27;
      }
      .migration-grid {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: .8rem;
        padding: 1rem 1.15rem 1.2rem;
      }
      .migration-card {
        min-height: 8.8rem;
        padding: .95rem;
        border-top: 3px solid #17334c;
      }
      .migration-card[data-region="EMEA"] { border-top-color: #16845b; }
      .migration-card[data-region="JAPAC"] { border-top-color: #2878a8; }
      .migration-card[data-region="NAMER"] { border-top-color: #c74634; }
      .migration-region {
        color: #667585;
        font-size: .7rem;
        font-weight: 850;
        letter-spacing: .07em;
        text-transform: uppercase;
      }
      .migration-name {
        margin-top: .55rem;
        color: #0d2033;
        font-size: 1.05rem;
        font-weight: 850;
      }
      .migration-count {
        margin-top: .2rem;
        font-size: .82rem;
        font-weight: 700;
      }
      .migration-date {
        display: inline-block;
        margin-top: .85rem;
        padding: .22rem .5rem;
        border-radius: .3rem;
        background: #edf1f4;
        color: #425363;
        font-size: .7rem;
        font-weight: 800;
      }
      .briefing-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 1.35rem;
      }
      .brief-card {
        padding: 1.1rem 1.25rem;
        border-left: 4px solid #17334c;
      }
      .brief-card.actions {
        border-left-color: #c74634;
      }
      .brief-card h2 {
        margin: 0 0 .8rem;
        color: #0d2033;
        font-size: 1.1rem;
      }
      .brief-card ul {
        display: grid;
        gap: .7rem;
        margin: 0;
        padding-left: 1.1rem;
        color: #3c4b58;
        line-height: 1.5;
      }
      .footer-note {
        margin-top: 1rem;
        padding-top: .8rem;
        border-top: 1px solid #dfe5ea;
        color: #667585;
        font-size: .72rem;
      }
      @media (max-width: 1100px) {
        .kpi-grid,
        .migration-grid,
        .briefing-grid {
          grid-template-columns: 1fr 1fr;
        }
      }
      @media (max-width: 760px) {
        .hero,
        .kpi-grid,
        .migration-grid,
        .briefing-grid {
          grid-template-columns: 1fr;
        }
        .brand {
          width: max-content;
          padding: 0;
          border: 0;
        }
        .date-stamp {
          text-align: left;
        }
      }
    </style>
    """


def render_header() -> str:
    return """
    <header class="hero">
      <div class="brand" aria-label="Oracle">ORACLE</div>
      <div>
        <h1>Resource Bandwidth Monthly Dashboard</h1>
        <p>Executive operations view across EMEA, JAPAC, and NAMER</p>
      </div>
      <div class="date-stamp"><strong>Reporting snapshot</strong>Data as of 12 May 2026</div>
    </header>
    """


def render_kpis(data: dict[str, object]) -> str:
    peak = data["peak"]
    risk_months = data["risk_months"]
    cards = [
        {
            "label": "Total projects scheduled",
            "value": f"{data['total']:,}",
            "note": "Across the seven-month planning horizon",
            "class": "",
        },
        {
            "label": "Peak month",
            "value": f"{peak['total']:,}",
            "note": f"{peak['label']} has the highest scheduled volume",
            "class": "",
        },
        {
            "label": "Risk months",
            "value": f"{len(risk_months):,}",
            "note": " and ".join(str(month["label"]) for month in risk_months),
            "class": "risk",
        },
        {
            "label": "Chain migrations",
            "value": f"{len(MIGRATIONS):,}",
            "note": "Major chain events tracked below",
            "class": "",
        },
    ]
    cards_html = "".join(
        f"""
        <article class="kpi-card {card['class']}">
          <div class="kpi-label">{escape(card['label'])}</div>
          <div class="kpi-value">{escape(card['value'])}</div>
          <div class="kpi-note">{escape(card['note'])}</div>
        </article>
        """
        for card in cards
    )
    return f'<section class="kpi-grid" aria-label="Executive KPI summary">{cards_html}</section>'


def render_matrix(data: dict[str, object]) -> str:
    header_cells = "".join(
        f"""
        <th scope="col">
          {escape(str(month['label']))}
          <span class="month-total">{int(month['total'])} projects total</span>
        </th>
        """
        for month in data["months"]
    )
    body_rows = []
    for region in REGIONS:
        cells = []
        for month in MONTHS:
            scheduled = int(month[region])
            pct = utilization(scheduled, region)
            state, label = state_for(pct)
            progress = min(pct, 100)
            aria = (
                f"{region}, {month['long']}: {scheduled} projects scheduled, "
                f"{percent_label(pct)} utilization, {label}"
            )
            cells.append(
                f"""
                <td>
                  <div class="util-card {state}" aria-label="{escape(aria)}">
                    <div class="ring" style="--progress:{progress:.2f}" aria-hidden="true">
                      <span class="ring-value">{percent_label(pct)}</span>
                    </div>
                    <div class="scheduled">{scheduled} scheduled</div>
                    <div class="status-label">{escape(label)}</div>
                  </div>
                </td>
                """
            )
        body_rows.append(
            f"""
            <tr>
              <th scope="row">
                {escape(region)}
                <span class="region-note">{CAPACITY[region]} monthly capacity</span>
              </th>
              {''.join(cells)}
            </tr>
            """
        )

    return f"""
    <section class="section" aria-labelledby="matrix-heading">
      <div class="section-head">
        <div>
          <h2 id="matrix-heading">Monthly Regional Utilization</h2>
          <p>Scheduled projects and utilization by region from July 2026 onward</p>
        </div>
        <div class="legend" aria-label="Utilization status legend">
          <span class="legend-item"><span class="dot"></span>Healthy</span>
          <span class="legend-item"><span class="dot warning"></span>Approaching capacity</span>
          <span class="legend-item"><span class="dot critical"></span>At or over capacity</span>
        </div>
      </div>
      <div class="matrix-shell" tabindex="0" aria-label="Scrollable monthly regional utilization table">
        <table class="matrix">
          <caption style="position:absolute;left:-10000px;">Monthly scheduled project volume and utilization percentage by region</caption>
          <thead>
            <tr>
              <th scope="col">Region</th>
              {header_cells}
            </tr>
          </thead>
          <tbody>{''.join(body_rows)}</tbody>
        </table>
      </div>
    </section>
    """


def render_migrations() -> str:
    cards = "".join(
        f"""
        <article class="migration-card" data-region="{escape(item['region'])}">
          <div class="migration-region">{escape(item['region'])}</div>
          <div class="migration-name">{escape(item['name'])}</div>
          <div class="migration-count">{int(item['count'])} hotels</div>
          <div class="migration-date">{escape(item['date'])}</div>
        </article>
        """
        for item in MIGRATIONS
    )
    return f"""
    <section class="section" aria-labelledby="migrations-heading">
      <div class="section-head">
        <div>
          <h2 id="migrations-heading">Major Chain Migrations</h2>
          <p>High-impact events tracked separately from monthly operating volume</p>
        </div>
      </div>
      <div class="migration-grid">{cards}</div>
    </section>
    """


def render_briefing(data: dict[str, object]) -> str:
    september = next(month for month in MONTHS if month["key"] == "2026-09")
    november = next(month for month in MONTHS if month["key"] == "2026-11")
    emea_peak = max(utilization(int(month["EMEA"]), "EMEA") for month in MONTHS)
    peak = data["peak"]
    peak_migrations = [
        migration for migration in MIGRATIONS if migration["month_key"] == peak["key"]
    ]
    peak_migration = max(peak_migrations, key=lambda migration: int(migration["count"]))

    insights = [
        f"{peak['long']} is the peak month at {peak['total']} projects, driven by {peak_migration['name']} in {peak_migration['region']}.",
        f"JAPAC reaches {percent_label(utilization(int(september['JAPAC']), 'JAPAC'))} utilization in September, while NAMER reaches {percent_label(utilization(int(november['NAMER']), 'NAMER'))} in November due to Vail.",
        f"EMEA remains stable across the period, with utilization peaking at {percent_label(emea_peak)} in July 2026.",
    ]
    actions = [
        "Shift discretionary work away from JAPAC in Sep 2026 and protect delivery capacity for Minor Hotels.",
        "Prepare overflow support for NAMER in Nov 2026 ahead of the Vail migration wave.",
        "Confirm timing for Aramark before assigning NAMER capacity to additional work.",
    ]
    insight_items = "".join(f"<li>{escape(item)}</li>" for item in insights)
    action_items = "".join(f"<li>{escape(item)}</li>" for item in actions)
    return f"""
    <section class="briefing-grid" aria-label="Executive briefing">
      <article class="brief-card">
        <h2>Executive Insights</h2>
        <ul>{insight_items}</ul>
      </article>
      <article class="brief-card actions">
        <h2>Recommended Actions</h2>
        <ul>{action_items}</ul>
      </article>
    </section>
    """


def main() -> None:
    st.set_page_config(
        page_title="Resource Bandwidth Monthly Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    data = metrics()
    dashboard_html = f"""
    {css()}
    <div class="dashboard">
      {render_header()}
      {render_kpis(data)}
      {render_matrix(data)}
      {render_migrations()}
      {render_briefing(data)}
      <div class="footer-note">Monthly resource planning view | Internal operations | Risk threshold: 90% utilization</div>
    </div>
    """
    st.html(dashboard_html)


if __name__ == "__main__":
    main()
