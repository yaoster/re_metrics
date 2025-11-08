PRD — ZIP-Level Housing Map MVP

1) Overview
Product: Single-page site with a short intro + an interactive US ZIP-code map that toggles 3 metrics:
Forecasted appreciation (12-month %)
Rent-to-price ratio (annual rent ÷ home price)
Current median home price
Audience: Small residential real-estate investors who want a fast way to compare markets.
Positioning: “A simple, transparent way to scan US ZIPs for opportunity.”

2) Problem & Goals
Problem: Investors waste hours piecing together prices, rents, and forecasts across sources. Tools are either too complex or not local enough.
Goal (MVP): Let users visually compare ZIPs in seconds, then hover/click for exact values.

3) Scope (MVP)
Minimal hero text (1–2 sentences) explaining purpose.
Choropleth map of ZIP polygons with:
Metric toggle (3 options)
Hover tooltip (ZIP, state, metric value, date)
Click drawer (adds the other two metrics for that ZIP)
Filters: optional State dropdown.
Attribution: “Home value & rent data © Zillow Research.” + data as-of date.
Auto-update: monthly pipeline to refresh datasets and redeploy.
Analytics: Plausible (or GA4) for page views, metric-toggle usage, outbound clicks.
Out of scope (MVP): accounts, saved views, exports, time-series animation, listings integration, paywall.

4) Data
ZHVI (median home value) by ZIP → current price.
ZORI (median rent) by ZIP → monthly rent.
Forecast: Zillow metro/ZIP forecast (if ZIP-level available; otherwise use nearest geography and display the coverage note).
Geometries: Census ZCTA shapes (match on 5-digit code; skip non-matches).
Derived fields
rent_to_price = 12 * zori / zhvi
as_of_month for each source (string “YYYY-MM”)
ZIP vs ZCTA policy: match when ZIP==ZCTA code; skip if missing; no imputation.

5) Functional Requirements
Load precomputed GeoJSON (≤ ~15 MB) with properties: zipcode, state, zhvi, zori, rtp, forecast_pct, as_of_price, as_of_rent, as_of_forecast.
Render choropleth by selected metric with quantile color bins (7 bins, clamped).
Tooltip shows metric value + ZIP; click opens drawer with all 3 metrics + “data as of” dates.
Footer shows attribution, methodology link, and last update.
Analytics events: metric_change, state_filter, zip_click.

6) UX Requirements
Layout: Above-the-fold hero text (≤120 chars), metric toggle (tabs or dropdown), big map, footer.
Legend: always visible; shows numeric bin edges + units.
Accessibility: WCAG-AA color contrast for legend labels; keyboard navigation to toggle metrics.
Mobile: map fills viewport; controls collapse into a compact header.

7) Non-functional
Perf: first map paint ≤ 3s on average broadband; p95 interaction latency ≤ 150ms.
Bundle: keep client payload small (serve static GeoJSON gzip’d).
Reliability: monthly pipeline retries on failure; manual rerun button (GitHub Actions).
Compliance: prominent Zillow attribution; no bulk download endpoint; show “as is” disclaimer.

8) Success Metrics
Activation: ≥60% visitors interact with the map (hover or click) per session.
Engagement: median time on page ≥ 60s; ≥30% use metric toggle.
Retention proxy: ≥15% returning visitors in 30 days.
SEO: indexable landing (H1, meta); CTR from organic ≥3% within 60 days.

9) Risks & Mitigations
Large GeoJSON → simplify shapes, or move to vector tiles later.
Sparse ZIP coverage → show subtle hatch/gray for missing areas; explain in Methodology.
Forecasts at non-ZIP geographies → display coverage note and nearest level used.

10) Launch Checklist
Data QA spot checks in 10 random ZIPs.
Legend units correct for each metric.
Attribution + “as of” visible.
Analytics firing across major paths/devices.
Lighthouse ≥ 80 performance on desktop.