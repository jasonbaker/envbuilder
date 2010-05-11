import os.path

from scripttest import TestFileEnvironment

from .base import EnvbTest

python_script = os.path.join('bin', 'python')

class TestCreateVenv(EnvbTest):
    env_file = """\
            [project]
            parcels=[]
            """
    def test(self):
        result = self.env.run('envb setup')
        assert python_script in result.files_created


class TestNoCreateVenv(TestCreateVenv):
    def test(self):
        self.env.run('envb setup')
        result = self.env.run('envb setup -N')
        assert python_script not in result.files_updated
