import json

from restrun.config import Config


print(json.dumps(Config.model_json_schema(), indent=4))
