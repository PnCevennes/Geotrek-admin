import os
from unittest import mock, skipIf
from shutil import rmtree
from tempfile import mkdtemp
from io import StringIO
import requests
from requests import Response
import urllib

from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.utils import DatabaseError
from django.test.utils import override_settings
from django.template.exceptions import TemplateDoesNotExist

from geotrek.authent.tests.factories import StructureFactory
from geotrek.trekking.models import POI, Trek
from geotrek.common.models import Organism, FileType, Attachment
from geotrek.common.tests.mixins import GeotrekParserTestMixin
from geotrek.common.parsers import (
    ExcelParser, AttachmentParserMixin, TourInSoftParser, ValueImportError, DownloadImportError,
    TourismSystemParser, OpenSystemParser, GeotrekParser, GeotrekAggregatorParser
)
from geotrek.common.utils.testdata import get_dummy_img


class OrganismParser(ExcelParser):
    model = Organism
    fields = {'organism': 'nOm'}


class OrganismEidParser(ExcelParser):
    model = Organism
    fields = {'organism': 'nOm'}
    eid = 'organism'


class StructureExcelParser(ExcelParser):
    model = Organism
    fields = {
        'organism': 'nOm',
        'structure': 'structure'
    }
    eid = 'organism'


class OrganismNoMappingNoPartialParser(StructureExcelParser):
    field_options = {
        "structure": {"mapping": {"foo": "bar", "": "boo"}}
    }
    natural_keys = {
        "structure": "name"
    }


class OrganismNoMappingPartialParser(StructureExcelParser):
    field_options = {
        "structure": {"mapping": {"foo": "bar"}, "partial": True}
    }
    natural_keys = {
        "structure": "name"
    }


class OrganismNoNaturalKeysParser(StructureExcelParser):
    warn_on_missing_fields = True


class AttachmentParser(AttachmentParserMixin, OrganismEidParser):
    non_fields = {'attachments': 'photo'}


class WarnAttachmentParser(AttachmentParser):
    warn_on_missing_fields = True


class AttachmentLegendParser(AttachmentParser):

    def filter_attachments(self, src, val):
        (url, legend, author) = val.split(', ')
        return [(url, legend, author)]


class ParserTests(TestCase):
    def test_bad_parser_class(self):
        with self.assertRaisesRegex(CommandError, "Failed to import parser class 'DoesNotExist'"):
            call_command('import', 'geotrek.common.tests.test_parsers.DoesNotExist', '', verbosity=0)

    def test_bad_parser_file(self):
        with self.assertRaisesRegex(CommandError, "Failed to import parser file 'geotrek/common.py'"):
            call_command('import', 'geotrek.common.DoesNotExist', '', verbosity=0)

    def test_no_filename_no_url(self):
        with self.assertRaisesRegex(CommandError, "File path missing"):
            call_command('import', 'geotrek.common.tests.test_parsers.OrganismParser', '', verbosity=0)

    def test_bad_filename(self):
        with self.assertRaisesRegex(CommandError, "File does not exists at: find_me/I_am_not_there.shp"):
            call_command('import', 'geotrek.common.tests.test_parsers.OrganismParser', 'find_me/I_am_not_there.shp', verbosity=0)

    @override_settings(VAR_DIR=os.path.join(os.path.dirname(__file__), 'data'))
    def test_custom_parser(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'CustomParser', filename, verbosity=0)

    def test_progress(self):
        output = StringIO()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.OrganismParser', filename, verbosity=2, stdout=output)
        self.assertIn('(100%)', output.getvalue())

    def test_create(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.OrganismParser', filename, verbosity=0)
        self.assertEqual(Organism.objects.count(), 1)
        organism = Organism.objects.get()
        self.assertEqual(organism.organism, "2.0")

    def test_duplicate_without_eid(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.OrganismParser', filename, verbosity=0)
        call_command('import', 'geotrek.common.tests.test_parsers.OrganismParser', filename, verbosity=0)
        self.assertEqual(Organism.objects.count(), 2)

    def test_unmodified_with_eid(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.OrganismEidParser', filename, verbosity=0)
        call_command('import', 'geotrek.common.tests.test_parsers.OrganismEidParser', filename, verbosity=0)
        self.assertEqual(Organism.objects.count(), 1)

    def test_updated_with_eid(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        filename2 = os.path.join(os.path.dirname(__file__), 'data', 'organism2.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.OrganismEidParser', filename, verbosity=0)
        call_command('import', 'geotrek.common.tests.test_parsers.OrganismEidParser', filename2, verbosity=0)
        self.assertEqual(Organism.objects.count(), 2)
        organisms = Organism.objects.order_by('pk')
        self.assertEqual(organisms[0].organism, "2.0")
        self.assertEqual(organisms[1].organism, "Comité Hippolyte")

    def test_report_format_text(self):
        parser = OrganismParser()
        self.assertRegex(parser.report(), '0/0 lines imported.')
        self.assertNotRegex(parser.report(), r'<div id=\"collapse-\$celery_id\" class=\"collapse\">')

    def test_report_format_html(self):
        parser = OrganismParser()
        self.assertRegex(parser.report(output_format='html'),
                         r'<div id=\"collapse-\$celery_id\" class=\"collapse\">')

    def test_report_format_bad(self):
        parser = OrganismParser()
        with self.assertRaises(TemplateDoesNotExist):
            parser.report(output_format='toto')

    @mock.patch('geotrek.common.parsers.Parser.parse_row')
    def test_databaseerror_except(self, mock_parse_row):
        output = StringIO()
        mock_parse_row.side_effect = DatabaseError('foo bar')
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.OrganismEidParser', filename, verbosity=2, stdout=output)
        self.assertIn('foo bar', output.getvalue())

    def test_fk_not_in_natural_keys(self):
        output = StringIO()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism5.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.OrganismNoNaturalKeysParser', filename, verbosity=2, stdout=output)
        self.assertIn("Destination field 'structure' not in natural keys configuration", output.getvalue())

    def test_no_mapping_not_partial(self):
        output = StringIO()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism5.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.OrganismNoMappingNoPartialParser', filename, verbosity=2, stdout=output)
        self.assertIn("Bad value 'Structure' for field STRUCTURE. Should be in ['foo', '']", output.getvalue())

    def test_no_mapping_partial(self):
        output = StringIO()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism5.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.OrganismNoMappingPartialParser', filename, verbosity=2, stdout=output)
        self.assertIn("Bad value 'Structure' for field STRUCTURE. Should contain ['foo']", output.getvalue())


@override_settings(MEDIA_ROOT=mkdtemp('geotrek_test'))
class AttachmentParserTests(TestCase):
    def setUp(self):
        self.filetype = FileType.objects.create(type="Photographie")

    def tearDown(self):
        if os.path.exists(settings.MEDIA_ROOT):
            rmtree(settings.MEDIA_ROOT)

    @mock.patch('requests.get')
    def test_attachment(self, mocked):
        mocked.return_value.status_code = 200
        mocked.return_value.content = b''
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
        organism = Organism.objects.get()
        attachment = Attachment.objects.get()
        self.assertEqual(attachment.content_object, organism)
        self.assertEqual(attachment.attachment_file.name, 'paperclip/common_organism/{pk}/titi.png'.format(pk=organism.pk))
        self.assertEqual(attachment.filetype, self.filetype)
        self.assertTrue(os.path.exists(attachment.attachment_file.path), True)

    @mock.patch('requests.get')
    def test_attachment_connection_error(self, mocked):
        mocked.return_value.status_code = 200
        mocked.side_effect = requests.exceptions.ConnectionError("Error connection")
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        output = StringIO()
        output_3 = StringIO()
        call_command('import', 'geotrek.common.tests.test_parsers.WarnAttachmentParser', filename, verbosity=2,
                     stdout=output, stderr=output_3)
        self.assertFalse(Attachment.objects.exists())
        self.assertIn("Failed to load attachment: Error connection", output.getvalue())

    @mock.patch('requests.get')
    @override_settings(PAPERCLIP_MAX_BYTES_SIZE_IMAGE=20)
    def test_attachment_bigger_size(self, mocked):
        mocked.return_value.status_code = 200
        mocked.return_value.content = get_dummy_img()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)

        self.assertEqual(Attachment.objects.count(), 0)
        with override_settings(PAPERCLIP_MAX_BYTES_SIZE_IMAGE=86):
            # Dummy Image is of size 85
            call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
            self.assertEqual(Attachment.objects.count(), 1)

    @mock.patch('requests.get')
    @override_settings(PAPERCLIP_MIN_IMAGE_UPLOAD_WIDTH=6)
    def test_attachment_min_width(self, mocked):
        mocked.return_value.status_code = 200
        mocked.return_value.content = get_dummy_img()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)

        self.assertEqual(Attachment.objects.count(), 0)
        with override_settings(PAPERCLIP_MIN_IMAGE_UPLOAD_WIDTH=4):
            # Dummy Image is of size 85
            call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
            self.assertEqual(Attachment.objects.count(), 1)

    @mock.patch('requests.get')
    @override_settings(PAPERCLIP_MIN_IMAGE_UPLOAD_HEIGHT=6)
    def test_attachment_min_height(self, mocked):
        mocked.return_value.status_code = 200
        mocked.return_value.content = get_dummy_img()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)

        self.assertEqual(Attachment.objects.count(), 0)
        with override_settings(PAPERCLIP_MIN_IMAGE_UPLOAD_HEIGHT=4):
            # Dummy Image is of size 85
            call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
            self.assertEqual(Attachment.objects.count(), 1)

    @mock.patch('requests.get')
    def test_attachment_long_name(self, mocked):
        mocked.return_value.status_code = 200
        mocked.return_value.content = b''
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism3.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
        organism = Organism.objects.get()
        attachment = Attachment.objects.get()
        self.assertEqual(attachment.content_object, organism)
        self.assertEqual(attachment.attachment_file.name,
                         'paperclip/common_organism/{pk}/{ti}.png'.format(pk=organism.pk, ti='ti' * 64))
        self.assertEqual(attachment.filetype, self.filetype)
        self.assertTrue(os.path.exists(attachment.attachment_file.path), True)

    @mock.patch('requests.get')
    def test_attachment_long_legend(self, mocked):
        mocked.return_value.status_code = 200
        mocked.return_value.content = b''
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism4.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentLegendParser', filename, verbosity=0)
        organism = Organism.objects.get()
        attachment = Attachment.objects.get()
        self.assertEqual(attachment.content_object, organism)
        self.assertEqual(attachment.legend,
                         '{0}'.format(('Legend ' * 18).rstrip()))
        self.assertEqual(attachment.filetype, self.filetype)
        self.assertTrue(os.path.exists(attachment.attachment_file.path), True)

    @mock.patch('requests.get')
    def test_attachment_with_other_filetype_with_structure(self, mocked):
        """
        It will always take the one without structure first
        """
        structure = StructureFactory.create(name="Structure")
        FileType.objects.create(type="Photographie", structure=structure)
        mocked.return_value.status_code = 200
        mocked.return_value.content = b''
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
        organism = Organism.objects.get()
        attachment = Attachment.objects.get()
        self.assertEqual(attachment.content_object, organism)
        self.assertEqual(attachment.attachment_file.name, 'paperclip/common_organism/{pk}/titi.png'.format(pk=organism.pk))
        self.assertEqual(attachment.filetype, self.filetype)
        self.assertEqual(attachment.filetype.structure, None)
        self.assertTrue(os.path.exists(attachment.attachment_file.path), True)

    @mock.patch('requests.get')
    def test_attachment_with_no_filetype_photographie(self, mocked):
        self.filetype.delete()
        mocked.return_value.status_code = 200
        mocked.return_value.content = b''
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        with self.assertRaisesRegex(CommandError, "FileType 'Photographie' does not exists in Geotrek-Admin. Please add it"):
            call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)

    @mock.patch('requests.get')
    @mock.patch('requests.head')
    def test_attachment_not_updated(self, mocked_head, mocked_get):
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.content = b''
        mocked_head.return_value.status_code = 200
        mocked_head.return_value.headers = {'content-length': 0}
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
        self.assertEqual(mocked_get.call_count, 1)
        self.assertEqual(Attachment.objects.count(), 1)

    @mock.patch('requests.get')
    @mock.patch('requests.head')
    def test_attachment_not_updated_partially_changed(self, mocked_head, mocked_get):
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.content = b''
        mocked_head.return_value.status_code = 200
        mocked_head.return_value.headers = {'content-length': 0}
        filename_no_legend = os.path.join(os.path.dirname(__file__), 'data', 'attachment_no_legend.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename_no_legend, verbosity=0)
        attachment = Attachment.objects.get()
        self.assertEqual(attachment.legend, '')
        self.assertEqual(attachment.author, '')
        filename = os.path.join(os.path.dirname(__file__), 'data', 'attachment.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentLegendParser', filename, verbosity=0)
        self.assertEqual(mocked_get.call_count, 1)
        self.assertEqual(Attachment.objects.count(), 1)
        attachment.refresh_from_db()
        self.assertEqual(attachment.legend, 'legend')
        self.assertEqual(attachment.author, 'name')

    @mock.patch('requests.get')
    @mock.patch('requests.head')
    def test_attachment_updated_file_not_found(self, mocked_head, mocked_get):
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.content = b''
        mocked_head.return_value.status_code = 200
        mocked_head.return_value.headers = {'content-length': 0}
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
        attachment = Attachment.objects.get()
        os.remove(attachment.attachment_file.path)
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
        self.assertEqual(mocked_get.call_count, 2)
        self.assertEqual(Attachment.objects.count(), 1)

    @override_settings(PARSER_RETRY_SLEEP_TIME=0)
    @mock.patch('requests.get')
    @mock.patch('requests.head')
    def test_attachment_request_fail(self, mocked_head, mocked_get):
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.content = b''
        mocked_head.return_value.status_code = 503
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
        self.assertEqual(mocked_get.call_count, 1)
        self.assertEqual(mocked_head.call_count, 3)
        self.assertEqual(Attachment.objects.count(), 1)

    @mock.patch('requests.get')
    @mock.patch('requests.head')
    def test_attachment_request_except(self, mocked_head, mocked_get):
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.content = b''
        mocked_head.side_effect = DownloadImportError()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
        self.assertEqual(mocked_get.call_count, 1)
        self.assertEqual(mocked_head.call_count, 1)
        self.assertEqual(Attachment.objects.count(), 1)

    @mock.patch('requests.get')
    @mock.patch('geotrek.common.parsers.urlparse')
    def test_attachment_download_fail(self, mocked_urlparse, mocked_get):
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        mocked_get.side_effect = DownloadImportError("DownloadImportError")
        mocked_urlparse.return_value = urllib.parse.urlparse('ftp://test.url.com/organism.xls')
        output = StringIO()
        call_command('import', 'geotrek.common.tests.test_parsers.WarnAttachmentParser', filename, verbosity=2,
                     stdout=output)
        self.assertIn("Failed to load attachment: DownloadImportError", output.getvalue())
        self.assertEqual(mocked_get.call_count, 1)

    @mock.patch('requests.get')
    def test_attachment_no_content(self, mocked):
        """
        It will always take the one without structure first
        """
        def mocked_requests_get(*args, **kwargs):
            response = requests.Response()
            response.status_code = 200
            response._content = None
            return response

        # Mock GET
        mocked.side_effect = mocked_requests_get
        structure = StructureFactory.create(name="Structure")
        FileType.objects.create(type="Photographie", structure=structure)
        filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
        call_command('import', 'geotrek.common.tests.test_parsers.AttachmentParser', filename, verbosity=0)
        self.assertEqual(Attachment.objects.count(), 0)


class TourInSoftParserTests(TestCase):

    def test_attachment(self):
        class TestTourParser(TourInSoftParser):
            separator = '##'
            separator2 = '||'

            def __init__(self):
                self.model = Trek
                super().__init__()

        parser = TestTourParser()
        result = parser.filter_attachments('', 'a||b||c##||||##d||e||f')
        self.assertListEqual(result, [['a', 'b', 'c'], ['d', 'e', 'f']])

    def test_moyen_de_com_split_failure(self):
        class TestTourParser(TourInSoftParser):
            def __init__(self):
                self.model = Trek
                super().__init__()

        parser = TestTourParser()
        with self.assertRaises(ValueImportError):
            parser.filter_email('', 'Téléphone filaire|02 37 37 80 11#Instagram|#chateaudesenonches')
        with self.assertRaises(ValueImportError):
            parser.filter_website('', 'Mél|chateau.senonches@gmail.Com#Instagram|#chateaudesenonches')
        with self.assertRaises(ValueImportError):
            parser.filter_contact('', ('Mél|chateau.senonches@gmail.Com#Instagram|#chateaudesenonches', ''))


class TourismSystemParserTest(TestCase):
    @mock.patch('geotrek.common.parsers.HTTPBasicAuth')
    @mock.patch('requests.get')
    def test_attachment(self, mocked_get, mocked_auth):
        class TestTourismSystemParser(TourismSystemParser):
            def __init__(self):
                self.model = Trek
                self.filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
                self.filetype = FileType.objects.create(type="Photographie")
                self.login = "test"
                self.password = "test"
                super().__init__()

        def side_effect():
            response = Response()
            response.status_code = 200
            response._content = bytes('{\"metadata\": {\"total\": 1}, \"data\": [] }', 'utf-8')
            response.encoding = 'utf-8'
            return response

        mocked_auth.return_value = None
        mocked_get.return_value = side_effect()
        parser = TestTourismSystemParser()
        parser.parse()
        self.assertEqual(mocked_get.call_count, 1)
        self.assertEqual(mocked_auth.call_count, 1)


class OpenSystemParserTest(TestCase):
    @mock.patch('requests.get')
    def test_attachment(self, mocked_get):
        class TestOpenSystemParser(OpenSystemParser):
            def __init__(self):
                self.model = Trek
                self.filename = os.path.join(os.path.dirname(__file__), 'data', 'organism.xls')
                self.filetype = FileType.objects.create(type="Photographie")
                self.login = "test"
                self.password = "test"
                super().__init__()

        def side_effect():
            response = Response()
            response.status_code = 200
            response._content = bytes(
                "<?xml version=\"1.0\"?><Data><Resultat><Objets>[]</Objets></Resultat></Data>",
                'utf-8'
            )
            return response

        mocked_get.return_value = side_effect()
        parser = TestOpenSystemParser()
        parser.parse()
        self.assertEqual(mocked_get.call_count, 1)


class GeotrekTrekTestParser(GeotrekParser):
    url = "https://test.fr"
    model = Trek
    url_categories = {
        'foo_field': 'test'
    }


class GeotrekAggregatorTestParser(GeotrekAggregatorParser):
    pass


class GeotrekParserTest(TestCase):
    def setUp(self, *args, **kwargs):
        self.filetype = FileType.objects.create(type="Photographie")

    def test_improperly_configurated_categories(self):
        with self.assertRaisesRegex(ImproperlyConfigured, 'foo_field is not configured in categories_keys_api_v2'):
            call_command('import', 'geotrek.common.tests.test_parsers.GeotrekTrekTestParser', verbosity=2)


class GeotrekAggregatorParserTest(GeotrekParserTestMixin, TestCase):
    def setUp(self, *args, **kwargs):
        self.filetype = FileType.objects.create(type="Photographie")

    def test_geotrek_aggregator_no_file(self):
        with self.assertRaisesRegex(CommandError, "File does not exists at: config_aggregator_does_not_exist.json"):
            call_command('import', 'geotrek.common.tests.test_parsers.GeotrekAggregatorTestParser',
                         'config_aggregator_does_not_exist.json', verbosity=0)

    @skipIf(settings.TREKKING_TOPOLOGY_ENABLED, 'Test without dynamic segmentation only')
    @mock.patch('geotrek.common.parsers.importlib.import_module', return_value=mock.MagicMock())
    @mock.patch('django.template.loader.render_to_string')
    @mock.patch('requests.get')
    def test_geotrek_aggregator_no_data_to_import(self, mocked_get, mocked_render, mocked_import_module):
        def mocked_json():
            return {}

        def side_effect_render(file, context):
            return 'Render'

        mocked_get.json = mocked_json
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.content = b''
        mocked_render.side_effect = side_effect_render
        output = StringIO()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'geotrek_parser_v2',
                                'config_aggregator_no_data_to_import.json')
        call_command('import', 'geotrek.common.parsers.GeotrekAggregatorParser', filename=filename, verbosity=2,
                     stdout=output)
        stdout_parser = output.getvalue()
        self.assertIn('Render\n', stdout_parser)
        self.assertIn('0000: Trek (URL_1) (00%)', stdout_parser)
        self.assertIn('0000: InformationDesk (URL_1) (00%)', stdout_parser)
        self.assertIn('0000: Trek (URL_1) (00%)', stdout_parser)
        # Trek, POI, Service, InformationDesk, TouristicContent, TouristicEvent, Signage, Infrastructure
        self.assertEqual(8, mocked_import_module.call_count)

    @skipIf(not settings.TREKKING_TOPOLOGY_ENABLED, 'Test with dynamic segmentation only')
    def test_geotrek_aggregator_parser_model_dynamic_segmentation(self):
        output = StringIO()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'geotrek_parser_v2', 'config_aggregator_ds.json')
        call_command('import', 'geotrek.common.parsers.GeotrekAggregatorParser', filename=filename, verbosity=2,
                     stdout=output)
        string_parser = output.getvalue()
        self.assertIn("Services can't be imported with dynamic segmentation", string_parser)
        self.assertIn("POIs can't be imported with dynamic segmentation", string_parser)
        self.assertIn("Treks can't be imported with dynamic segmentation", string_parser)

    @skipIf(settings.TREKKING_TOPOLOGY_ENABLED, 'Test without dynamic segmentation only')
    @mock.patch('geotrek.common.parsers.importlib.import_module', return_value=mock.MagicMock())
    @mock.patch('django.template.loader.render_to_string')
    @mock.patch('requests.get')
    def test_geotrek_aggregator_parser_multiple_admin(self, mocked_get, mocked_render, mocked_import_module):
        def mocked_json():
            return {}

        def side_effect_render(file, context):
            return 'Render'

        mocked_get.json = mocked_json
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.content = b''
        mocked_render.side_effect = side_effect_render
        output = StringIO()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'geotrek_parser_v2',
                                'config_aggregator_multiple_admin.json')
        call_command('import', 'geotrek.common.parsers.GeotrekAggregatorParser', filename=filename, verbosity=2,
                     stdout=output)
        stdout_parser = output.getvalue()
        self.assertIn('Render\n', stdout_parser)
        self.assertIn('0000: Trek (URL_1) (00%)', stdout_parser)
        # "VTT", "Vélo"
        # "Trek", "Service", "POI"
        # "POI", "InformationDesk", "TouristicContent"
        self.assertEqual(8, mocked_import_module.call_count)

    @skipIf(settings.TREKKING_TOPOLOGY_ENABLED, 'Test without dynamic segmentation only')
    def test_geotrek_aggregator_parser_no_url(self):
        output = StringIO()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'geotrek_parser_v2', 'config_aggregator_no_url.json')
        call_command('import', 'geotrek.common.parsers.GeotrekAggregatorParser', filename=filename, verbosity=2,
                     stdout=output)
        string_parser = output.getvalue()

        self.assertIn('URL_1 has no url', string_parser)

    @skipIf(settings.TREKKING_TOPOLOGY_ENABLED, 'Test without dynamic segmentation only')
    @mock.patch('requests.get')
    @mock.patch('requests.head')
    @override_settings(MODELTRANSLATION_DEFAULT_LANGUAGE="fr")
    def test_geotrek_aggregator_parser(self, mocked_head, mocked_get):
        self.app_label = 'trekking'
        self.mock_time = 0
        self.mock_json_order = ['trek_difficulty.json',
                                'trek_route.json',
                                'trek_theme.json',
                                'trek_practice.json',
                                'trek_accessibility.json',
                                'trek_network.json',
                                'trek_label.json',
                                'trek_ids.json',
                                'trek.json',
                                'trek_children.json',
                                'poi_type.json',
                                'poi_ids.json',
                                'poi.json']

        # Mock GET
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json = self.mock_json
        mocked_get.return_value.content = b''
        mocked_head.return_value.status_code = 200

        output = StringIO()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'geotrek_parser_v2', 'config_aggregator.json')
        call_command('import', 'geotrek.common.parsers.GeotrekAggregatorParser', filename=filename, verbosity=2,
                     stdout=output)
        string_parser = output.getvalue()
        self.assertIn('0000: Trek (URL_1) (00%)', string_parser)
        self.assertIn('0000: POI (URL_1) (00%)', string_parser)
        self.assertIn('5/5 lines imported.', string_parser)
        self.assertIn('2/2 lines imported.', string_parser)
        self.assertEqual(Trek.objects.count(), 5)
        self.assertEqual(POI.objects.count(), 2)
