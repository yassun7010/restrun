from restrun.generator.context import Context
from restrun.generator.mock_client import MockClientGenerator


class TestMockClientGenerator:
    def test_generate(self):
        locals = {}
        code = MockClientGenerator().generate(Context(client_prefix="My"))

        exec("class MyClient: pass\n" + code, None, locals)

        assert locals["MyMockClient"] is not None
