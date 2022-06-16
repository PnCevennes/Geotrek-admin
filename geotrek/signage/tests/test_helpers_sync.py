from io import StringIO
import os
from unittest.mock import patch

from django.test import TestCase

from geotrek.common.tests.factories import FakeSyncCommand
from geotrek.signage.tests.factories import SignageFactory
from geotrek.signage.helpers_sync import SyncRando


class SyncRandoTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.signage = SignageFactory.create(published=True)

    @patch('sys.stdout', new_callable=StringIO)
    def test_signage(self, mock_stdout):
        command = FakeSyncCommand()
        synchro = SyncRando(command)
        synchro.sync('en')
        self.assertTrue(os.path.exists(os.path.join('var', command.tmp_root, 'api', 'en', 'signages.geojson')))
        self.assertTrue(os.path.exists(os.path.join('var', command.tmp_root, 'static', 'signage', 'picto-signage.png')))
