"""
    Test custom django management commands
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """ Test Commands"""

    def test_wait_for_db_ready(self, patched_checked):
        """ Test waiting for db if db is ready. """
        patched_checked.return_value = True

        call_command('wait_for_db')

        patched_checked.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_delay(self, patched_sleep, patched_checked):
        """ waiting for db  when getting operational error."""
        patched_checked.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_checked.call_count, 6)
        patched_checked.assert_called_with(databases=['default'])
