import os.path

from scripttest import TestFileEnvironment

from .base import EnvbTest

class TestCreateVenv(EnvbTest):
    env_file = """\
            [project]
            parcels=[]
            """
    def test(self):
        result = self.env.run('envb setup')
        python_script = os.path.join('bin', 'python')
        assert python_script in result.files_created

