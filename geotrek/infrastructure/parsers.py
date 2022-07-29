from geotrek.common.parsers import GeotrekParser
from geotrek.infrastructure.models import Infrastructure


class GeotrekInfrastructureParser(GeotrekParser):
    url = None
    model = Infrastructure
    constant_fields = {
        "published": True,
        "deleted": False
    }
    replace_fields = {
        "eid": "uuid"
    }
    url_categories = {
        'condition': '/api/v2/infrastructure_condition/',
        'type': '/api/v2/infrastructure_type/',
    }
    categories_keys_api_v2 = {
        'condition': 'label',
        'type': 'label'
    }
    natural_keys = {
        'condition': 'label',
        'type': 'label'
    }

    field_options = {
        "type": {"create": True}
    }

    def next_row(self):
        self.next_url = f"{self.url}/api/v2/infrastructure"
        return super().next_row()