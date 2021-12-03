import os

from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import Permission
from django.test import TestCase

from geotrek.authent.tests.base import AuthentFixturesTest
from geotrek.infrastructure.tests.factories import InfrastructureMaintenanceDifficultyLevelFactory, InfrastructureTypeFactory, InfrastructureConditionFactory, InfrastructureUsageDifficultyLevelFactory
from geotrek.infrastructure.models import InfrastructureMaintenanceDifficultyLevel, InfrastructureType, InfrastructureCondition, InfrastructureUsageDifficultyLevel
from geotrek.authent.tests.factories import StructureFactory

from mapentity.tests.factories import SuperUserFactory, UserFactory


class InfrastructureTypeAdminNoBypassTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create(password='booh')
        self.client.login(username=self.user.username, password='booh')
        self.user.user_permissions.add(Permission.objects.get(codename='add_draft_path'))
        for perm in Permission.objects.exclude(codename='can_bypass_structure'):
            self.user.user_permissions.add(perm)
        self.user.is_staff = True
        self.user.save()
        p = self.user.profile
        structure = StructureFactory(name="This")
        p.structure = structure
        p.save()
        self.infra = InfrastructureTypeFactory.create(structure=structure)

    def login(self):
        success = self.client.login(username=self.user.username, password='booh')
        self.assertTrue(success)

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_infrastructuretype_changelist(self):
        self.login()
        changelist_url = reverse('admin:infrastructure_infrastructuretype_changelist')
        response = self.client.get(changelist_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, InfrastructureType.objects.get(pk=self.infra.pk).label)

    def test_infrastructuretype_can_be_change(self):
        self.login()
        change_url = reverse('admin:infrastructure_infrastructuretype_change', args=[self.infra.pk])
        response = self.client.post(change_url, {'label': 'coucou', 'type': 'A',
                                                 'pictogram': os.path.join(
                                                     settings.MEDIA_URL, self.infra.pictogram.name)})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(InfrastructureType.objects.get(pk=self.infra.pk).label, 'coucou')

        self.assertEqual(response.url, '/admin/infrastructure/infrastructuretype/')

    def test_infrastructuretype_cannot_be_change_not_same_structure(self):
        self.login()
        structure = StructureFactory(name="Other")
        infra = InfrastructureTypeFactory.create(structure=structure)
        change_url = reverse('admin:infrastructure_infrastructuretype_change', args=[infra.pk])
        response = self.client.get(change_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(InfrastructureType.objects.get(pk=self.infra.pk).label, self.infra.label)

        self.assertEqual(response.url, '/admin/')


class InfrastructureConditionAdminNoBypassTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create(password='booh')
        self.client.login(username=self.user.username, password='booh')
        self.user.user_permissions.add(Permission.objects.get(codename='add_draft_path'))
        for perm in Permission.objects.exclude(codename='can_bypass_structure'):
            self.user.user_permissions.add(perm)
        self.user.is_staff = True
        self.user.save()
        p = self.user.profile
        structure = StructureFactory(name="This")
        p.structure = structure
        p.save()
        self.infra = InfrastructureConditionFactory.create(structure=structure)

    def login(self):
        success = self.client.login(username=self.user.username, password='booh')
        self.assertTrue(success)

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_infrastructurecondition_changelist(self):
        self.login()
        changelist_url = reverse('admin:infrastructure_infrastructurecondition_changelist')
        response = self.client.get(changelist_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, InfrastructureCondition.objects.get(pk=self.infra.pk).label)

    def test_infrastructurecondition_can_be_change(self):
        self.login()
        change_url = reverse('admin:infrastructure_infrastructurecondition_change', args=[self.infra.pk])
        response = self.client.post(change_url, {'label': 'coucou', 'structure': StructureFactory.create().pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(InfrastructureCondition.objects.get(pk=self.infra.pk).label, 'coucou')

        self.assertEqual(response.url, '/admin/infrastructure/infrastructurecondition/')

    def test_infrastructurecondition_cannot_be_change_not_same_structure(self):
        self.login()
        structure = StructureFactory(name="Other")
        infra = InfrastructureConditionFactory.create(structure=structure)
        change_url = reverse('admin:infrastructure_infrastructurecondition_change', args=[infra.pk])
        response = self.client.get(change_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(InfrastructureCondition.objects.get(pk=self.infra.pk).label, self.infra.label)

        self.assertEqual(response.url, '/admin/')


class InfrastructureTypeAdminTest(AuthentFixturesTest):
    def setUp(self):
        self.user = SuperUserFactory.create(password='booh')
        self.infra = InfrastructureTypeFactory.create()

    def login(self):
        success = self.client.login(username=self.user.username, password='booh')
        self.assertTrue(success)

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_infrastructuretype_can_be_change(self):
        self.login()
        change_url = reverse('admin:infrastructure_infrastructuretype_change', args=[self.infra.pk])
        response = self.client.post(change_url, {'label': 'coucou', 'type': 'A',
                                                 'pictogram': os.path.join(
                                                     settings.MEDIA_URL, self.infra.pictogram.name)})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(InfrastructureType.objects.get(pk=self.infra.pk).label, 'coucou')

        self.assertEqual(response.url, '/admin/infrastructure/infrastructuretype/')

    def test_infrastructuretype_changelist(self):
        self.login()
        changelist_url = reverse('admin:infrastructure_infrastructuretype_changelist')
        response = self.client.get(changelist_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, InfrastructureType.objects.get(pk=self.infra.pk).label)


class InfrastructureConditionAdminTest(AuthentFixturesTest):
    def setUp(self):
        self.user = SuperUserFactory.create(password='booh')
        self.infra = InfrastructureConditionFactory.create()

    def login(self):
        success = self.client.login(username=self.user.username, password='booh')
        self.assertTrue(success)

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_infrastructurecondition_can_be_change(self):
        self.login()

        change_url = reverse('admin:infrastructure_infrastructurecondition_change', args=[self.infra.pk])
        response = self.client.post(change_url, {'label': 'coucou', 'structure': StructureFactory.create().pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(InfrastructureCondition.objects.get(pk=self.infra.pk).label, 'coucou')

        self.assertEqual(response.url, '/admin/infrastructure/infrastructurecondition/')

    def test_infrastructurecondition_changelist(self):
        self.login()
        changelist_url = reverse('admin:infrastructure_infrastructurecondition_changelist')
        response = self.client.get(changelist_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, InfrastructureCondition.objects.get(pk=self.infra.pk).label)


class InfrastructureUsageDifficultyAdminTest(AuthentFixturesTest):
    def setUp(self):
        self.user = SuperUserFactory.create(password='booh')
        self.level = InfrastructureUsageDifficultyLevelFactory(label='Medium', structure=StructureFactory(name="Ecorp"))

    def login(self):
        success = self.client.login(username=self.user.username, password='booh')
        self.assertTrue(success)

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_infrastructure_usage_difficulty_level_display_string(self):
        '''Test string formatting for usage difficulty levels'''
        self.assertEquals(str(self.level), "Medium (Ecorp)")

    def test_infrastructure_usage_difficulty_can_be_changed(self):
        '''Test admin update view for usage difficulty levels'''
        self.login()
        change_url = reverse('admin:infrastructure_infrastructureusagedifficultylevel_change', args=[self.level.pk])
        response = self.client.post(change_url, {'label': 'Easy'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(InfrastructureUsageDifficultyLevel.objects.get(pk=self.level.pk).label, 'Easy')

        self.assertEqual(response.url, '/admin/infrastructure/infrastructureusagedifficultylevel/')

    def test_infrastructurecondition_changelist(self):
        '''Test admin list view for usage difficulty levels'''
        self.login()
        changelist_url = reverse('admin:infrastructure_infrastructureusagedifficultylevel_changelist')
        response = self.client.get(changelist_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, InfrastructureUsageDifficultyLevel.objects.get(pk=self.level.pk).label)


class InfrastructureMaintenanceDifficultyAdminTest(AuthentFixturesTest):
    def setUp(self):
        self.user = SuperUserFactory.create(password='booh')
        self.level = InfrastructureMaintenanceDifficultyLevelFactory(label='Medium', structure=StructureFactory(name="Ecorp"))

    def login(self):
        success = self.client.login(username=self.user.username, password='booh')
        self.assertTrue(success)

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_infrastructure_maintenance_difficulty_level_display_string(self):
        '''Test string formatting for maintenance difficulty levels'''
        self.assertEquals(str(self.level), "Medium (Ecorp)")

    def test_infrastructure_maintenance_difficulty_can_be_changed(self):
        '''Test admin update view for maintenance difficulty levels'''
        self.login()
        change_url = reverse('admin:infrastructure_infrastructuremaintenancedifficultylevel_change', args=[self.level.pk])
        response = self.client.post(change_url, {'label': 'Easy'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(InfrastructureMaintenanceDifficultyLevel.objects.get(pk=self.level.pk).label, 'Easy')

        self.assertEqual(response.url, '/admin/infrastructure/infrastructuremaintenancedifficultylevel/')

    def test_infrastructurecondition_maintenance_difficulty_changelist(self):
        '''Test list view for maintenance difficulty levels'''
        self.login()
        changelist_url = reverse('admin:infrastructure_infrastructuremaintenancedifficultylevel_changelist')
        response = self.client.get(changelist_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, InfrastructureMaintenanceDifficultyLevel.objects.get(pk=self.level.pk).label)
