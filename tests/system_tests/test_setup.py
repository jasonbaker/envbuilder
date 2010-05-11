import os.path

from scripttest import TestFileEnvironment

def test_create_virtualenv():
    env = TestFileEnvironment('tmp')
    env_file = """\
            [project]
            parcels=[]
            """
    env.writefile('.env', content=env_file)
    result = env.run('envb setup')
    python_script = os.path.join('bin', 'python')
    assert python_script in result.files_created

