import asyncio
import unittest
from dataclasses import dataclass
from types import SimpleNamespace

from matrix_bot import (
    COMMANDS,
    PlaceholderMatrixBot,
    extract_command_from_message,
    get_placeholder_response,
)


class _FakeIntent:
    def __init__(self):
        self.notices = []

    async def send_notice(self, room_id, text):
        self.notices.append((room_id, text))


class _FakeAppService:
    def __init__(self):
        self.intent = _FakeIntent()
        self.registered_handler = None

    def matrix_event_handler(self, handler):
        self.registered_handler = handler
        return handler


@dataclass
class _FakeContent:
    body: str
    msgtype: str


@dataclass
class _FakeEvent:
    room_id: str
    type: str
    content: _FakeContent


class MatrixBotPlaceholderTests(unittest.TestCase):
    def test_all_required_commands_return_placeholder(self):
        for command in ("help", "create_bridged_pair", "bridge", "debug_info"):
            self.assertIn(command, COMMANDS)
            self.assertEqual(
                get_placeholder_response(command),
                f"Placeholder: '{command}' command is not implemented yet.",
            )

    def test_extract_command_from_message(self):
        self.assertEqual(extract_command_from_message("!help"), "help")
        self.assertEqual(extract_command_from_message("bridge now"), "bridge")
        self.assertEqual(extract_command_from_message("DEBUG_INFO details"), "debug_info")
        self.assertIsNone(extract_command_from_message("unknown"))

    def test_handle_event_sends_placeholder_notice_for_supported_command(self):
        appservice = _FakeAppService()
        bot = PlaceholderMatrixBot(appservice)

        event = _FakeEvent(
            room_id="!room:example.org",
            type="m.room.message",
            content=_FakeContent(body="!create_bridged_pair", msgtype="m.text"),
        )

        response = asyncio.run(bot.handle_event(event))

        self.assertEqual(
            response,
            "Placeholder: 'create_bridged_pair' command is not implemented yet.",
        )
        self.assertEqual(
            appservice.intent.notices,
            [("!room:example.org", response)],
        )

    def test_handle_event_ignores_non_command_messages(self):
        appservice = _FakeAppService()
        bot = PlaceholderMatrixBot(appservice)

        event = _FakeEvent(
            room_id="!room:example.org",
            type="m.room.message",
            content=_FakeContent(body="hello there", msgtype="m.text"),
        )

        response = asyncio.run(bot.handle_event(event))

        self.assertIsNone(response)
        self.assertEqual(appservice.intent.notices, [])

    def test_register_uses_appservice_event_handler(self):
        appservice = _FakeAppService()
        bot = PlaceholderMatrixBot(appservice)

        bot.register()

        self.assertIsNotNone(appservice.registered_handler)


if __name__ == "__main__":
    unittest.main()
