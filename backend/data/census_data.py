from __future__ import annotations

import posixpath
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


CENSUS_WORKBOOK_PATH = Path(__file__).with_name("2011_population.xlsx")
_MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
_NAMESPACES = {"m": _MAIN_NS, "rel": _PACKAGE_REL_NS}
_DISTRICT_ALIASES = {
    "pauri garhwal": "garhwal",
    "tehri": "tehri garhwal",
    "ugarkashi": "uttarkashi",
}
_SUBDISTRICT_ALIASES = {
    "kapkote": "kapkot",
    "karnprayag": "karnaprayag",
}


def normalize_geography_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.casefold())


def _column_number(cell_reference: str) -> int:
    number = 0
    for character in cell_reference:
        if not character.isalpha():
            break
        number = number * 26 + ord(character.upper()) - ord("A") + 1
    return number


def _cell_text(cell: ET.Element, shared_strings: list[str]) -> str:
    value = cell.find(f"{{{_MAIN_NS}}}v")
    text = value.text if value is not None else ""
    if cell.attrib.get("t") == "s" and text:
        return shared_strings[int(text)].strip()
    return text.strip()


def load_census_subdistricts(
    workbook_path: str | Path = CENSUS_WORKBOOK_PATH,
) -> dict[tuple[str, str], dict]:
    with zipfile.ZipFile(workbook_path) as archive:
        shared_strings = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared_strings = [
                "".join(item.itertext()).strip()
                for item in shared_root.findall("m:si", _NAMESPACES)
            ]

        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        relationship_targets = {
            item.attrib["Id"]: item.attrib["Target"]
            for item in relationships.findall("rel:Relationship", _NAMESPACES)
        }
        sheet = workbook.find("m:sheets/m:sheet", _NAMESPACES)
        if sheet is None:
            raise ValueError("The Census workbook contains no worksheets")

        relationship_id = sheet.attrib[f"{{{_REL_NS}}}id"]
        target = relationship_targets[relationship_id]
        sheet_path = target.lstrip("/")
        if not sheet_path.startswith("xl/"):
            sheet_path = posixpath.normpath(posixpath.join("xl", sheet_path))
        worksheet = ET.fromstring(archive.read(sheet_path))

    rows = []
    for row in worksheet.findall(".//m:sheetData/m:row", _NAMESPACES):
        values = {
            _column_number(cell.attrib["r"]): _cell_text(cell, shared_strings)
            for cell in row.findall("m:c", _NAMESPACES)
        }
        if values.get(1, "").zfill(2) == "05":
            rows.append(values)

    district_names = {
        values.get(2, "").zfill(3): values.get(5, "")
        for values in rows
        if values.get(4) == "DISTRICT" and values.get(6) == "Total"
    }

    subdistricts = {}
    for values in rows:
        if values.get(4) != "SUB-DISTRICT" or values.get(6) != "Total":
            continue

        district_code = values.get(2, "").zfill(3)
        subdistrict_code = values.get(3, "").zfill(5)
        district = district_names.get(district_code)
        subdistrict = values.get(5, "")
        if not district or not subdistrict or not values.get(11, "").isdigit():
            continue

        subdistricts[(normalize_geography_name(district), normalize_geography_name(subdistrict))] = {
            "state_code": "05",
            "district_code": district_code,
            "subdistrict_code": subdistrict_code,
            "district": district,
            "subdistrict": subdistrict,
            "population": int(values[11]),
            "households": int(values[10]) if values.get(10, "").isdigit() else None,
            "inhabited_villages": int(values[7]) if values.get(7, "").isdigit() else None,
            "towns": int(values[9]) if values.get(9, "").isdigit() else None,
            "census_year": 2011,
        }

    if not subdistricts:
        raise ValueError("No Uttarakhand subdistrict population records found in the Census workbook")
    return subdistricts


def find_census_subdistrict(
    district: str,
    subdistrict: str,
    census_subdistricts: dict[tuple[str, str], dict],
) -> dict | None:
    district_name = _DISTRICT_ALIASES.get(district.casefold(), district)
    subdistrict_name = _SUBDISTRICT_ALIASES.get(subdistrict.casefold(), subdistrict)
    key = (normalize_geography_name(district_name), normalize_geography_name(subdistrict_name))
    return census_subdistricts.get(key)