"""Normalize raw kbo-data output into SAVEX internal format."""

import re
from datetime import datetime

_TEAM_NAME_MAP: dict[str, str] = {
    "LG": "LG",
    "LG트윈스": "LG",
    "LG 트윈스": "LG",
    "KT": "KT",
    "KT위즈": "KT",
    "KT 위즈": "KT",
    "SSG": "SSG",
    "SSG랜더스": "SSG",
    "SSG 랜더스": "SSG",
    "NC": "NC",
    "NC다이노스": "NC",
    "NC 다이노스": "NC",
    "두산": "DOOSAN",
    "두산베어스": "DOOSAN",
    "두산 베어스": "DOOSAN",
    "DOOSAN": "DOOSAN",
    "KIA": "KIA",
    "KIA타이거즈": "KIA",
    "KIA 타이거즈": "KIA",
    "롯데": "LOTTE",
    "롯데자이언츠": "LOTTE",
    "롯데 자이언츠": "LOTTE",
    "LOTTE": "LOTTE",
    "삼성": "SAMSUNG",
    "삼성라이온즈": "SAMSUNG",
    "삼성 라이온즈": "SAMSUNG",
    "SAMSUNG": "SAMSUNG",
    "한화": "HANWHA",
    "한화이글스": "HANWHA",
    "한화 이글스": "HANWHA",
    "HANWHA": "HANWHA",
    "키움": "KIWOOM",
    "키움히어로즈": "KIWOOM",
    "키움 히어로즈": "KIWOOM",
    "KIWOOM": "KIWOOM",
}


def normalize_team_name(name: str) -> str:
    """Map any KBO team name variant to internal team ID."""
    if not name:
        return ""
    cleaned = name.strip()
    result = _TEAM_NAME_MAP.get(cleaned)
    if result:
        return result
    upper = cleaned.upper()
    for key, val in _TEAM_NAME_MAP.items():
        if key.upper() == upper:
            return val
    return cleaned.upper()


def normalize_player_name(name: str) -> str:
    """Strip whitespace and normalize Korean player names."""
    if not name:
        return ""
    return name.strip()


def normalize_game_date(value: str | None) -> str:
    """Convert various date formats to YYYY-MM-DD."""
    if not value:
        return ""
    value = str(value).strip()
    for fmt in ("%Y%m%d", "%Y-%m-%d", "%Y.%m.%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return value


def build_game_id(date: str, away_team: str, home_team: str) -> str:
    """Build a stable game ID from date and team IDs."""
    d = normalize_game_date(date).replace("-", "")
    a = normalize_team_name(away_team)
    h = normalize_team_name(home_team)
    return f"{d}_{a}_{h}"


def map_kbo_team_to_internal_id(name: str) -> str:
    """Alias for normalize_team_name; returns lowercase internal ID."""
    mapped = normalize_team_name(name)
    return {
        "LG": "lg",
        "KT": "kt",
        "SSG": "ssg",
        "NC": "nc",
        "DOOSAN": "doosan",
        "KIA": "kia",
        "LOTTE": "lotte",
        "SAMSUNG": "samsung",
        "HANWHA": "hanwha",
        "KIWOOM": "kiwoom",
    }.get(mapped, mapped.lower())
