# scripts/make_dummy_geojson.py
import json, random, math
from pathlib import Path

# 6 pretend ZIPs placed across the US (lon, lat centroids)
centers = [
    ("94105", "CA", -122.394, 37.789),  # SF
    ("90012", "CA", -118.243, 34.053),  # LA
    ("10001", "NY", -73.996, 40.750),   # NYC
    ("60607", "IL", -87.651, 41.875),   # Chicago
    ("75201", "TX", -96.801, 32.787),   # Dallas
    ("98101", "WA", -122.336, 47.610),  # Seattle
]

def rect(lon, lat, dlon=0.05, dlat=0.05):
    # simple rectangle (lon/lat degrees), not geodesically perfect but fine for demo
    return [
        [
            [lon - dlon, lat - dlat],
            [lon + dlon, lat - dlat],
            [lon + dlon, lat + dlat],
            [lon - dlon, lat + dlat],
            [lon - dlon, lat - dlat],
        ]
    ]

features = []
random.seed(42)
for zipcode, state, lon, lat in centers:
    # Make up plausible metrics
    zhvi = random.randint(250_000, 1_200_000)
    zori = random.randint(1200, 4500)
    rtp = min(max((12 * zori) / zhvi, 0.01), 0.15)  # clamp ~1–15%
    forecast_pct = round(random.uniform(-0.05, 0.10), 3)  # -5%..+10%

    feat = {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": rect(lon, lat)},
        "properties": {
            "zipcode": zipcode,
            "state": state,
            "zhvi": zhvi,
            "zori": zori,
            "rtp": rtp,
            "forecast_pct": forecast_pct,
            "as_of_price": "2025-10",
            "as_of_rent": "2025-10",
            "as_of_forecast": "2025-10",
        },
    }
    features.append(feat)

geo = {"type": "FeatureCollection", "features": features}

outdir = Path("data")
outdir.mkdir(parents=True, exist_ok=True)
(outdir / "zip_stats.geojson").write_text(json.dumps(geo))
print("Wrote data/zip_stats.geojson with", len(features), "features")
