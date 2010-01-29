from envbuilder.config import Config

def test_getitem():
    stub_config = { 'foo' : 'bar' }
    cfg = Config(stub_config)
    assert cfg['foo'] == stub_config['foo']
