from pysistence import Expando
from nose.tools import raises

from envbuilder.config import Config

def test_getitem():
    stub_config = { 'foo' : 'bar' }
    cfg = Config(config=stub_config)
    assert cfg['foo'] == stub_config['foo']

@raises(KeyError)
def test_getitem_keyerror():
    cfg = Config(config={'foo' : 'bar'})
    # Force an error
    cfg['asdf']

def test_parcels():
    prj_config = {
        'project' : {
            'parcels' : ['foo', 'bar', 'asdf'],
            'foo' : {},
            'bar' : {},
            'asdf' : {}}}
    args = Expando(parcels=None)
    cfg = Config(prj_config, args=args)
    # Ordering isn't important, so sort the lists
    actual_parcels = sorted([parcel.name for parcel in cfg.parcels])
    expected_parcels = sorted(['foo', 'bar', 'asdf'])
    assert actual_parcels == expected_parcels
