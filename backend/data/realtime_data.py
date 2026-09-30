from __future__ import annotations

import re
from datetime import date
from html import unescape
from urllib.request import Request, urlopen


IMD_DISTRICT_RAINFALL_URL = (
    "https://mausam.imd.gov.in/responsive/rainfallinformation/rfi_district.inc.php"
)

_DISTRICT_RECORD = re.compile(
    r'"title"\s*:\s*"(?P<district>[^"]+)"\s*,\s*'
    r'"id"\s*:\s*"?(?P<district_id>\d+)"?.*?'
    r'"balloonText"\s*:\s*"(?P<balloon>[^"]+)"',
    re.DOTALL,
)
_RAINFALL_VALUES = re.compile(
    r"Date\s*:\s*(?P<date>\d{4}-\d{2}-\d{2}).*?"
    r"Departure\s*:\s*(?P<departure>-?\d+(?:\.\d+)?)%.*?"
    r"Actual\s*:\s*(?P<actual>-?\d+(?:\.\d+)?)\s*mm.*?"
    r"Normal\s*:\s*(?P<normal>-?\d+(?:\.\d+)?)\s*mm",
    re.DOTALL,
)


def normalize_district_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.casefold())


def parse_district_rainfall(page: str) -> list[dict]:
    observations = []
    for match in _DISTRICT_RECORD.finditer(page):
        balloon = unescape(match.group("balloon")).replace(r"\/", "/")
        values = _RAINFALL_VALUES.search(balloon)
        if not values:
            continue
        try:
            date.fromisoformat(values.group("date"))
        except ValueError:
            continue

        observations.append(
            {
                "district": unescape(match.group("district")).strip(),
                "report_date": values.group("date"),
                "actual_mm": float(values.group("actual")),
                "normal_mm": float(values.group("normal")),
                "departure_percent": float(values.group("departure")),
            }
        )
    return observations


def fetch_district_rainfall() -> list[dict]:
    request = Request(
        IMD_DISTRICT_RAINFALL_URL,
        headers={"User-Agent": "GARUDA risk assessment data client"},
    )
    with urlopen(request, timeout=15) as response:
        page = response.read().decode("utf-8", errors="replace")

    observations = parse_district_rainfall(page)
    if not observations:
        raise ValueError("The IMD district rainfall page returned no parseable observations")
    return observations