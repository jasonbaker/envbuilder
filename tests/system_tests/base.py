from scripttest import TestFileEnvironment

class EnvbTest(object):
    env_file = ''
    def setUp(self):
        self.env = TestFileEnvironment('tmp')
        assert self.env_file
        self.env.writefile('.env', content=self.env_file)
