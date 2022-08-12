import json
import os


class GeotrekParserTestMixin:
    def mock_json(self):
        filename = os.path.join('geotrek', self.app_label, 'tests', 'data', 'geotrek_parser_v2',
                                self.mock_json_order[self.mock_time])
        self.mock_time += 1
        with open(filename, 'r') as f:
            return json.load(f)

