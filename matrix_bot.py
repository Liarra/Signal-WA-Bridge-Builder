"""Placeholder Matrix bot command handler."""

from __future__ import annotations

import argparse

COMMANDS = ("help", "create_bridged_pair", "bridge", "debug_info")


def get_placeholder_response(command: str) -> str:
    """Return a placeholder response for a supported command."""
    if command not in COMMANDS:
        raise ValueError(f"Unsupported command: {command}")
    return f"Placeholder: '{command}' command is not implemented yet."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Placeholder Matrix bot")
    parser.add_argument("command", choices=COMMANDS, help="Command to execute")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    print(get_placeholder_response(args.command))


if __name__ == "__main__":
    main()
