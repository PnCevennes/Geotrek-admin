from geotrek.common.parsers import GeotrekParser
from geotrek.signage.models import Signage


class GeotrekSignageParser(GeotrekParser):
    """Geotrek parser for Signage"""

    url = None
    model = Signage
    constant_fields = {
        "published": True,
        "deleted": False
    }
    replace_fields = {
        "eid": "id",
        "geom": "geometry"
    }
    url_categories = {
        'sealing': 'signage_sealing',
        'condition': 'infrastructure_condition',
        'type': 'signage_type',
    }
    categories_keys_api_v2 = {
        'condition': 'label',
        'sealing': 'label',
        'type': 'label'
    }
    natural_keys = {
        'condition': 'label',
        'sealing': 'label',
        'type': 'label'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_url = f"{self.url}/api/v2/signage"
