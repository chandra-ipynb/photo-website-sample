#!/usr/bin/env python3
"""
VARIABLES / TERMINAL COMMAND
----------------------------
Run from this folder:
python3 update_site.py --studio "My Studio" --phone "+919999999999" --address "My full address"

Optional:
  --instagram "https://instagram.com/my_studio"
  --message "Hello, I want to book a photoshoot."
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("site-config.js")


def load_config() -> dict[str, str]:
    text = CONFIG_PATH.read_text(encoding="utf-8")
    match = re.search(r"window\.SITE_CONFIG\s*=\s*(\{.*\})\s*;", text, re.DOTALL)
    if not match:
        raise SystemExit(f"Could not read configuration from {CONFIG_PATH}")
    return json.loads(match.group(1))


def display_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 12 and digits.startswith("91"):
        return f"+91 {digits[2:7]} {digits[7:]}"
    return phone


def main() -> None:
    parser = argparse.ArgumentParser(description="Update the studio details used across the website.")
    parser.add_argument("--studio", help="Studio or business name")
    parser.add_argument("--phone", help="Phone with country code, e.g. +919945690520")
    parser.add_argument("--address", help="Full studio address")
    parser.add_argument("--instagram", help="Full Instagram profile URL")
    parser.add_argument("--message", help="Default WhatsApp enquiry message")
    args = parser.parse_args()

    changes = {
        "studio": args.studio,
        "phone": args.phone,
        "address": args.address,
        "instagram": args.instagram,
        "whatsappMessage": args.message,
    }
    if not any(value is not None for value in changes.values()):
        parser.error("provide at least one detail to change")

    config = load_config()
    config.update({key: value for key, value in changes.items() if value is not None})
    if args.phone:
        config["displayPhone"] = display_phone(args.phone)

    output = "window.SITE_CONFIG = " + json.dumps(config, ensure_ascii=False, indent=2) + ";\n"
    CONFIG_PATH.write_text(output, encoding="utf-8")
    print(f"Updated {CONFIG_PATH.name}")


if __name__ == "__main__":
    main()
