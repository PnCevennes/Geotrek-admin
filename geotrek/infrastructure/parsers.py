from geotrek.common.parsers import GeotrekParser
from geotrek.infrastructure.models import Infrastructure


class GeotrekInfrastructureParser(GeotrekParser):
    """Geotrek parser for Infrastructure"""

    url = None
    model = Infrastructure
    constant_fields = {
        "published": True,
        "deleted": False
    }
    replace_fields = {
        "eid": "id",
        "geom": "geometry"
    }
    url_categories = {
        'condition': 'infrastructure_condition',
        'type': 'infrastructure_type',
    }
    categories_keys_api_v2 = {
        'condition': 'label',
        'type': 'label'
    }
    natural_keys = {
        'condition': 'label',
        'type': 'label'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_url = f"{self.url}/api/v2/infrastructure"
