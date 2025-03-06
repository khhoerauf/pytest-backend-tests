import json
from os.path import dirname, join
from jsonschema import validate


class SchemaAssertions:

    def load_json_schema(self, filename):
        relative_path = join("support/schemas", filename)
        absolute_path = join(dirname(__file__), relative_path)

        try:
            with open(absolute_path) as schema_file:
                return json.load(schema_file)
        except ValueError:
            print("There is invalid schema json file : " + absolute_path)

    def assert_valid_schema(self, data, schema_file):
        schema = self.load_json_schema(schema_file)
        return validate(data, schema)
