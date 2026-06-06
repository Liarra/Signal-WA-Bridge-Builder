"""Placeholder Matrix bot built on mautrix AppService."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

try:
    from mautrix.appservice import AppService
    from mautrix.types import EventType, MessageType
except ImportError:  # pragma: no cover - handled in runtime startup
    AppService = None  # type: ignore[assignment]
    EventType = None  # type: ignore[assignment]
    MessageType = None  # type: ignore[assignment]

COMMANDS = ("help", "create_bridged_pair", "bridge", "debug_info")


@dataclass(frozen=True)
class BotConfig:
    homeserver_url: str
    homeserver_domain: str
    appservice_token: str
    homeserver_token: str
    bot_localpart: str
    appservice_id: str
    listen_host: str = "0.0.0.0"
    listen_port: int = 8080


ENV_VAR_MAP = {
    "homeserver_url": "MATRIX_HOMESERVER_URL",
    "homeserver_domain": "MATRIX_HOMESERVER_DOMAIN",
    "appservice_token": "MATRIX_AS_TOKEN",
    "homeserver_token": "MATRIX_HS_TOKEN",
    "bot_localpart": "MATRIX_BOT_LOCALPART",
    "appservice_id": "MATRIX_APP_SERVICE_ID",
}


def get_placeholder_response(command: str) -> str:
    if command not in COMMANDS:
        raise ValueError(f"Unsupported command: {command}")
    return f"Placeholder: '{command}' command is not implemented yet."


def extract_command_from_message(body: str) -> str | None:
    stripped = body.strip()
    if not stripped:
        return None

    token = stripped.split(maxsplit=1)[0]
    if token.startswith("!"):
        token = token[1:]

    normalized = token.lower()
    if normalized in COMMANDS:
        return normalized
    return None


def load_config_from_env() -> BotConfig:
    values: dict[str, str] = {}
    missing: list[str] = []
    for field_name, env_name in ENV_VAR_MAP.items():
        value = os.getenv(env_name)
        if not value:
            missing.append(env_name)
        else:
            values[field_name] = value

    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    return BotConfig(
        homeserver_url=values["homeserver_url"],
        homeserver_domain=values["homeserver_domain"],
        appservice_token=values["appservice_token"],
        homeserver_token=values["homeserver_token"],
        bot_localpart=values["bot_localpart"],
        appservice_id=values["appservice_id"],
        listen_host=os.getenv("MATRIX_LISTEN_HOST", "0.0.0.0"),
        listen_port=int(os.getenv("MATRIX_LISTEN_PORT", "8080")),
    )


class PlaceholderMatrixBot:
    def __init__(self, appservice: Any):
        self.appservice = appservice

    async def handle_event(self, event: Any) -> str | None:
        if not self._is_text_message_event(event):
            return None

        body = getattr(getattr(event, "content", None), "body", "")
        command = extract_command_from_message(body)
        if command is None:
            return None

        response = get_placeholder_response(command)
        await self.appservice.intent.send_notice(event.room_id, response)
        return response

    def register(self) -> None:
        @self.appservice.matrix_event_handler
        async def on_matrix_event(event: Any) -> None:
            await self.handle_event(event)

        self._handler = on_matrix_event

    @staticmethod
    def _is_text_message_event(event: Any) -> bool:
        event_type = getattr(event, "type", None)
        if EventType is None:
            is_room_message = str(event_type) == "m.room.message"
        else:
            is_room_message = event_type == EventType.ROOM_MESSAGE or str(event_type) == "m.room.message"

        if not is_room_message:
            return False

        msgtype = getattr(getattr(event, "content", None), "msgtype", None)
        if MessageType is None:
            return str(msgtype) in {"m.text", "MessageType.TEXT"}
        return msgtype == MessageType.TEXT or str(msgtype) == "m.text"


def create_appservice(config: BotConfig) -> Any:
    if AppService is None:
        raise RuntimeError("mautrix is required. Install dependencies from requirements.txt")

    return AppService(
        server=config.homeserver_url,
        domain=config.homeserver_domain,
        as_token=config.appservice_token,
        hs_token=config.homeserver_token,
        bot_localpart=config.bot_localpart,
        id=config.appservice_id,
    )


def main() -> None:
    config = load_config_from_env()
    appservice = create_appservice(config)
    bot = PlaceholderMatrixBot(appservice)
    bot.register()
    appservice.start(host=config.listen_host, port=config.listen_port)


if __name__ == "__main__":
    main()
