import os
import mock
import sys
from StringIO import StringIO

from django.contrib.gis.geos.error import GEOSException
from django.core.management import call_command
from django.test import TestCase
from django.core.management.base import CommandError

from geotrek.common.utils import almostequal
from geotrek.core.factories import PathFactory
from geotrek.infrastructure.factories import InfrastructureFactory
from geotrek.infrastructure.models import Infrastructure
from geotrek.authent.factories import StructureFactory


class InfrastructureCommandTest(TestCase):
    """
    There are 2 infrastructures in the file infrastructure.shp
    """
    def setUp(self):
        self.path = PathFactory.create()

    def test_load_infrastructure(self):
        output = StringIO()
        structure = StructureFactory.create(name='structure')
        filename = os.path.join(os.path.dirname(__file__), 'data', 'infrastructure.shp')
        call_command('loadinfrastructure', filename, type_default='label', name_default='name',
                     condition_default='condition', structure_default='structure',
                     description_default='description', year_default=2010, verbosity=2, stdout=output)
        self.assertIn('Infrastructures will be linked to %s' % structure, output.getvalue())
        self.assertIn('2 objects created.', output.getvalue())
        value = Infrastructure.objects.filter(name='name')
        self.assertEquals(2010, value[0].implantation_year)
        self.assertEquals(value.count(), 2)
        self.assertTrue(almostequal(value[0].geom.x, -436345.7048306435))
        self.assertTrue(almostequal(value[0].geom.y, 1176487.7429172313))
        self.assertTrue(almostequal(value[1].geom.x, -436345.5053471739))
        self.assertTrue(almostequal(value[1].geom.y, 1176480.9183338303))

    def test_load_infrastructure_multipoints(self):
        output = StringIO()
        structure = StructureFactory.create(name='structure')
        filename = os.path.join(os.path.dirname(__file__), 'data', 'infrastructure_good_multipoint.geojson')
        call_command('loadinfrastructure', filename, type_default='label', name_default='name',
                     condition_default='condition', structure_default='structure',
                     description_default='description', year_default=2010, verbosity=2, stdout=output)
        self.assertIn('Infrastructures will be linked to %s' % structure, output.getvalue())
        self.assertIn('1 objects created.', output.getvalue())
        value = Infrastructure.objects.first()
        self.assertEquals('name', value.name)
        self.assertEquals(2010, value.implantation_year)
        self.assertEquals(Infrastructure.objects.count(), 1)

    def test_load_infrastructure_bad_multipoints_error(self):
        output = StringIO()
        StructureFactory.create(name='structure')
        filename = os.path.join(os.path.dirname(__file__), 'data', 'infrastructure_bad_multipoint.geojson')
        with self.assertRaises(CommandError) as e:
            call_command('loadinfrastructure', filename, type_default='label', name_default='name',
                         condition_default='condition', structure_default='structure',
                         description_default='description', year_default=2010, verbosity=2, stdout=output)
        self.assertEqual('One of your geometry is a MultiPoint object with multiple points', e.exception.message)

    def test_load_infrastructure_with_fields_use_structure(self):
        output = StringIO()
        structure = StructureFactory.create(name='structure')
        filename = os.path.join(os.path.dirname(__file__), 'data', 'infrastructure.shp')
        call_command('loadinfrastructure', filename, type_field='label', name_field='name',
                     condition_field='condition', structure_default='structure', use_structure=True,
                     description_field='descriptio', year_field='year', verbosity=1, stdout=output)
        self.assertIn('Infrastructures will be linked to %s' % structure, output.getvalue())
        self.assertIn("InfrastructureType 'type (%s)' created" % structure, output.getvalue())
        self.assertIn("Condition Type 'condition (%s)' created" % structure, output.getvalue())
        value = Infrastructure.objects.all()
        names = [val.name for val in value]
        years = [val.implantation_year for val in value]
        self.assertIn('coucou', names)
        self.assertIn(2010, years)
        self.assertIn(2012, years)
        self.assertEquals(value.count(), 2)

    def test_load_infrastructure_with_fields(self):
        output = StringIO()
        structure = StructureFactory.create(name='structure')
        filename = os.path.join(os.path.dirname(__file__), 'data', 'infrastructure.shp')
        call_command('loadinfrastructure', filename, type_field='label', name_field='name',
                     condition_field='condition', structure_default='structure',
                     description_field='descriptio', year_field='year', verbosity=1, stdout=output)
        self.assertIn('Infrastructures will be linked to %s' % structure, output.getvalue())
        self.assertIn("InfrastructureType 'type' created", output.getvalue())
        self.assertIn("Condition Type 'condition' created", output.getvalue())
        value = Infrastructure.objects.all()
        names = [val.name for val in value]
        years = [val.implantation_year for val in value]
        self.assertIn('coucou', names)
        self.assertIn(2010, years)
        self.assertIn(2012, years)
        self.assertEquals(value.count(), 2)

    def test_no_file_fail(self):
        with self.assertRaises(CommandError) as cm:
            call_command('loadinfrastructure', 'toto.shp')
        self.assertEqual(cm.exception.message, "File does not exists at: toto.shp")

    def test_missing_defaults(self):
        StructureFactory.create(name='structure')
        filename = os.path.join(os.path.dirname(__file__), 'data', 'infrastructure.shp')
        output = StringIO()

        call_command('loadinfrastructure', filename, stdout=output)
        call_command('loadinfrastructure', filename, type_default='label', stdout=output)

        elements_to_check = ['type', 'name']
        self.assertEqual(output.getvalue().count("Field 'None' not found in data source."), 2)
        for element in elements_to_check:
            self.assertIn("Set it with --{0}-field, or set a default value with --{0}-default".format(element),
                          output.getvalue())

    def test_wrong_fields_fail(self):
        StructureFactory.create(name='structure')
        filename = os.path.join(os.path.dirname(__file__), 'data', 'infrastructure.shp')
        output = StringIO()
        call_command('loadinfrastructure', filename, type_field='wrong_type_field', stdout=output)
        call_command('loadinfrastructure', filename, type_default='label', name_field='wrong_name_field',
                     stdout=output)
        call_command('loadinfrastructure', filename, type_default='label', name_field='name',
                     condition_field='wrong_condition_field', stdout=output)
        call_command('loadinfrastructure', filename, type_default='label', name_field='name',
                     description_field='wrong_description_field', stdout=output)
        call_command('loadinfrastructure', filename, type_default='label', name_field='name',
                     year_field='wrong_implantation_year_field', stdout=output)
        call_command('loadinfrastructure', filename, type_default='label', name_field='name',
                     structure_field='wrong_structure_field', stdout=output)
        call_command('loadinfrastructure', filename, type_default='label', name_field='name',
                     eid_field='wrong_eid_field', stdout=output)
        call_command('loadinfrastructure', filename, type_default='label', name_field='name',
                     category_field='wrong_category_field', stdout=output)
        elements_to_check = ['wrong_type_field', 'wrong_name_field', 'wrong_condition_field',
                             'wrong_description_field', 'wrong_implantation_year_field', 'wrong_structure_field',
                             'wrong_eid_field', 'wrong_category_field']
        self.assertEqual(output.getvalue().count("set a default value"), 2)
        self.assertEqual(output.getvalue().count("Change your"), 6)
        for element in elements_to_check:
            self.assertIn("Field '{}' not found in data source".format(element),
                          output.getvalue())

    def test_line_fail_rolling_back(self):
        self.path.delete()
        StructureFactory.create(name='structure')
        filename = os.path.join(os.path.dirname(__file__), 'data', 'line.geojson')
        output = StringIO()
        with self.assertRaises(GEOSException):
            call_command('loadinfrastructure', filename, type_default='label', name_default='name',
                         stdout=output)
        self.assertIn('An error occured, rolling back operations.', output.getvalue())
        self.assertEqual(Infrastructure.objects.count(), 0)

    def test_update_same_eid(self):
        output = StringIO()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'infrastructure.shp')
        InfrastructureFactory(name="name", eid="eid_2")
        call_command('loadinfrastructure', filename, eid_field='eid', type_default='label',
                     name_default='name', verbosity=2, stdout=output)
        self.assertIn("Update : name with eid eid1", output.getvalue())
        self.assertEqual(Infrastructure.objects.count(), 2)

    def test_fail_import(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', 'infrastructure.shp')
        with mock.patch.dict(sys.modules, {'osgeo': None}):
            with self.assertRaises(CommandError) as e:
                call_command('loadinfrastructure', filename, verbosity=0)
            self.assertEqual('GDAL Python bindings are not available. Can not proceed.', e.exception.message)

    def test_fail_structure_default_do_not_exist(self):
        output = StringIO()
        filename = os.path.join(os.path.dirname(__file__), 'data', 'infrastructure.shp')
        call_command('loadinfrastructure', filename, type_default='label', name_default='name',
                     condition_default='condition', structure_default='wrong_structure_default',
                     description_default='description', year_default=2010, category_default='E', verbosity=0,
                     stdout=output)
        self.assertIn("Structure wrong_structure_default set in options doesn't exist", output.getvalue())
