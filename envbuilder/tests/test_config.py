from nose.tools import raises

from envbuilder.config import Config

def test_getitem():
    stub_config = { 'foo' : 'bar' }
    cfg = Config(config=stub_config)
    assert cfg['foo'] == stub_config['foo']

@raises(KeyError)
def test_getitem_keyerror():
    cfg = Config(config={'foo' : 'bar'})
    cfg['asdf']
