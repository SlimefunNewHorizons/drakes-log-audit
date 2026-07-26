#!/usr/bin/env python3
"""Collect and summarize Minecraft logs without storing production data in Git."""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import quote
from urllib.request import Request, urlopen


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


COMPLAINT_WORDS = re.compile(
    r"\b(bug|buguead|no (anda|funciona|sirve|deja)|lag|tps|crash|ca[íi]d|"
    r"roto|perd[ií]|desaparec|lento|error|dupe|duplic|no me deja|imposible)\b",
    re.IGNORECASE,
)
CHAT_LINE = re.compile(r"\[[^\]]+\]\s+(?:\[[^\]]+\]\s*)?(?P<player>[^»]+)\s+»\s+(?P<message>.+)$")
TPS_LINE = re.compile(r"TPS from last 5s, 1m, 5m, 15m:\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)")
CRASH_CAUSE = re.compile(r"(?:Caused by:|Description:)\s*(.+)")
FILE_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")


@dataclass(frozen=True)
class Finding:
    kind: str
    source: str
    line: int
    text: str


def api_request(url: str, key: str) -> dict:
    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {key}",
            "Accept": "application/vnd.pterodactyl.v1+json",
            # Avoid Cloudflare rejecting Python's default User-Agent.
            "User-Agent": "DrakesLogAudit/1.0",
        },
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def download(url: str, destination: Path) -> None:
    with urlopen(url, timeout=60) as response:
        destination.write_bytes(response.read())


def parse_remote_date(value: str) -> date:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).date()


def date_from_name(path: Path) -> date | None:
    """Return the date encoded in rotated log and crash-report filenames."""
    match = FILE_DATE.search(path.name)
    return date.fromisoformat(match.group(1)) if match else None


def collect(args: argparse.Namespace) -> int:
    key = os.environ.get("PTERODACTYL_API_KEY") or Path(args.key_file).read_text(encoding="utf-8").strip()
    since = date.fromisoformat(args.since)
    destination = Path(args.output)
    destination.mkdir(parents=True, exist_ok=True)
    base = args.base_url.rstrip("/") + f"/api/client/servers/{args.server_id}"
    downloaded = 0
    for directory in ("/logs", "/crash-reports"):
        listing = api_request(f"{base}/files/list?directory={quote(directory, safe='')}", key)
        for item in listing.get("data", []):
            attributes = item["attributes"]
            name_date = date_from_name(Path(attributes["name"]))
            if (
                not attributes.get("is_file")
                or parse_remote_date(attributes["modified_at"]) < since
                or (name_date is not None and name_date < since)
            ):
                continue
            remote_path = f"{directory}/{attributes['name']}"
            signed = api_request(f"{base}/files/download?file={quote(remote_path, safe='')}", key)["attributes"]["url"]
            target = destination / directory.strip("/") / attributes["name"]
            target.parent.mkdir(parents=True, exist_ok=True)
            download(signed, target)
            downloaded += 1
    print(f"[SUCCESS] Downloaded {downloaded} files to {destination}")
    return 0


def read_lines(path: Path) -> Iterable[str]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as handle:
        yield from handle


def fingerprint(text: str) -> str:
    text = re.sub(r"\d+", "#", text)
    text = re.sub(r"\[[^\]]{8,}\]", "[... ]", text)
    return text[:220]


def audit(paths: Iterable[Path]) -> dict:
    errors: Counter[str] = Counter()
    warnings: Counter[str] = Counter()
    complaints: list[Finding] = []
    crashes: list[Finding] = []
    tps: list[tuple[str, float, float, float, float]] = []
    files = 0
    for path in paths:
        files += 1
        for line_number, raw in enumerate(read_lines(path), 1):
            line = raw.strip()
            if not line:
                continue
            lower = line.lower()
            if "[error]" in lower or "exception" in lower or "error occurred" in lower:
                errors[fingerprint(line)] += 1
            elif "[warn]" in lower or "warning" in lower:
                warnings[fingerprint(line)] += 1
            tps_match = TPS_LINE.search(line)
            if tps_match:
                tps.append((path.name, *(float(value) for value in tps_match.groups())))
            chat = CHAT_LINE.search(line)
            if chat and COMPLAINT_WORDS.search(chat.group("message")):
                complaints.append(Finding("player-feedback", path.name, line_number, f"{chat.group('player').strip()}: {chat.group('message')}"))
            if path.name.startswith("crash-"):
                cause = CRASH_CAUSE.search(line)
                if cause:
                    crashes.append(Finding("crash", path.name, line_number, cause.group(1)))
    return {
        "files": files,
        "errors": errors.most_common(25),
        "warnings": warnings.most_common(25),
        "complaints": [asdict(item) for item in complaints[:100]],
        "crashes": [asdict(item) for item in crashes[:100]],
        "tps": tps,
    }


def render_markdown(report: dict) -> str:
    lines = ["# Auditoría de logs", "", f"Archivos analizados: **{report['files']}**", ""]
    lines.extend(["## Crashes", ""])
    lines.extend([f"- `{item['source']}`: {item['text']}" for item in report["crashes"]] or ["- Sin causa extraída."])
    lines.extend(["", "## Errores recurrentes", ""])
    lines.extend([f"- {count}x `{text}`" for text, count in report["errors"]] or ["- Sin errores detectados."])
    lines.extend(["", "## Avisos recurrentes", ""])
    lines.extend([f"- {count}x `{text}`" for text, count in report["warnings"]] or ["- Sin avisos detectados."])
    lines.extend(["", "## Comentarios relevantes", ""])
    lines.extend([f"- `{item['source']}:{item['line']}` {item['text']}" for item in report["complaints"]] or ["- Sin reportes de jugadores detectados."])
    if report["tps"]:
        minimum = min(sample[2] for sample in report["tps"])
        lines.extend(["", "## TPS", "", f"- Mínimo observado de 1 minuto: **{minimum:.2f}**."])
    return "\n".join(lines) + "\n"


def analyze(args: argparse.Namespace) -> int:
    source = Path(args.input)
    paths = sorted(path for path in source.rglob("*") if path.is_file() and path.suffix in {".log", ".txt", ".gz"})
    if args.since:
        since = date.fromisoformat(args.since)
        paths = [path for path in paths if date_from_name(path) is None or date_from_name(path) >= since]
    report = audit(paths)
    markdown = render_markdown(report)
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(markdown, encoding="utf-8")
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(markdown)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    collect_parser = commands.add_parser("collect")
    collect_parser.add_argument("--base-url", required=True)
    collect_parser.add_argument("--server-id", required=True)
    collect_parser.add_argument("--key-file", required=True)
    collect_parser.add_argument("--since", required=True)
    collect_parser.add_argument("--output", required=True)
    collect_parser.set_defaults(handler=collect)
    analyze_parser = commands.add_parser("analyze")
    analyze_parser.add_argument("--input", required=True)
    analyze_parser.add_argument("--since", help="Ignore rotated files older than YYYY-MM-DD.")
    analyze_parser.add_argument("--report")
    analyze_parser.add_argument("--json")
    analyze_parser.set_defaults(handler=analyze)
    return parser


if __name__ == "__main__":
    arguments = build_parser().parse_args()
    sys.exit(arguments.handler(arguments))
