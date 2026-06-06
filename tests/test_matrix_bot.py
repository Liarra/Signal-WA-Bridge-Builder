import unittest

from matrix_bot import COMMANDS, get_placeholder_response


class MatrixBotPlaceholderTests(unittest.TestCase):
    def test_all_required_commands_return_placeholder(self):
        for command in ("help", "create_bridged_pair", "bridge", "debug_info"):
            self.assertIn(command, COMMANDS)
            self.assertEqual(
                get_placeholder_response(command),
                f"Placeholder: '{command}' command is not implemented yet.",
            )

    def test_unknown_command_raises_value_error(self):
        with self.assertRaises(ValueError):
            get_placeholder_response("unknown")


if __name__ == "__main__":
    unittest.main()
