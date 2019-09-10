import pytest
from pyfathom import *

def test_single_pattern_match():
	c = classifier('/xyz/ is abc')
	assert str(c.classify('xyz')) == '<abc>xyz</abc>'
	
def test_single_pattern_two_matches():
	c = classifier('/xyz/ is abc')
	assert str(c.classify('xyz zyx xyz')) == '<abc>xyz</abc>zyx<abc>xyz</abc>'
	
def test_dual_pattern_match():
	c = classifier('/xyz/,/zyx/ is abc')
	assert str(c.classify('xyz zyx')) == '<abc>xyz zyx</abc>'
	
def test_dual_pattern_no_overlap():
	c = classifier('/xyz/,/xyz/ is abc')
	assert str(c.classify('xyz xyz xyz xyz')) == '<abc>xyz xyz</abc><abc>xyz xyz</abc>'
	
def test_no_match():
	c = classifier('/xyz/ is abc')
	assert str(c.classify('zyx')) == 'zyx'

def test_dual_pattern_end_missing():
	c = classifier('/xyz/,/xyz/ is abc')
	assert str(c.classify('xyz')) == 'xyz'
	
def test_single_type_match():
	k = '''
		/xyz/ is abc
		abc is def
	'''
	c = classifier(k)
	assert str(c.classify('xyz')) == '<abc><def>xyz</def></abc>'

def test_dual_type_match():
	k = '''
		/xyz/ is abc
		/zyx/ is foo
		abc,foo is def,bar
	'''
	c = classifier(k)
	assert str(c.classify('xyz zyx')) == '<abc><def>xyz</def></abc><foo><bar>zyx</bar></foo>'
	
def test_dual_type_match_single_is_type():
	k = '''
		/xyz/ is abc
		/zyx/ is foo
		abc,foo is ,bar
	'''
	c = classifier(k)
	assert str(c.classify('xyz zyx')) == '<abc>xyz</abc><foo><bar>zyx</bar></foo>'
	
def test_type_and_pattern_mix():
	k = '''
		/xyz/ is foo
		/abc/,foo,/cba/ is one,two,three
	'''
	c = classifier(k)
	assert str(c.classify('abc xyz cba')) == '<one>abc</one><foo><two>xyz</two></foo><three>cba</three>'
	
def test_zero_many_pattern_match_many():
	c = classifier('/these/,/\\w+/* is words')
	assert str(c.classify('these are some words')) == '<words>these are some words</words>'
	
def test_zero_many_pattern_match_zero():
	c = classifier('/these/,/\\w+/* is words')
	assert str(c.classify('these')) == '<words>these</words>'
	
def test_one_many_pattern_match_many():
	c = classifier('/these/,/\\w+/+ is words')
	assert str(c.classify('these are some words')) == '<words>these are some words</words>'
	
def test_one_many_pattern_match_one():
	c = classifier('/these/,/\\w+/+ is words')
	assert str(c.classify('these are')) == '<words>these are</words>'
	
def test_one_many_pattern_match_zero():
	c = classifier('/these/,/\\w+/+ is words')
	assert str(c.classify('these')) == 'these'
	
def test_zero_one_pattern_match_many():
	c = classifier('/these/,/\\w+/? is words')
	assert str(c.classify('these are some words')) == '<words>these are</words>some words'
	
def test_zero_one_pattern_match_one():
	c = classifier('/these/,/\\w+/? is words')
	assert str(c.classify('these are')) == '<words>these are</words>'
	
def test_zero_one_pattern_match_zero():
	c = classifier('/these/,/\\w+/? is words')
	assert str(c.classify('these')) == '<words>these</words>'
	
def test_lazy_zero_many_pattern_match_many():
	c = classifier('/\w+/*?,/abc/ is foo')
	assert str(c.classify('xyz xyz abc xyz')) == '<foo>xyz xyz abc</foo>xyz'
	
def test_lazy_zero_many_pattern_match_zero():
	c = classifier('/\w+/*?,/abc/ is foo')
	assert str(c.classify('abc xyz')) == '<foo>abc</foo>xyz'
	
def test_lazy_one_many_pattern_match_many():
	c = classifier('/\w+/+?,/abc/ is foo')
	assert str(c.classify('xyz xyz abc xyz')) == '<foo>xyz xyz abc</foo>xyz'
	
def test_lazy_one_many_pattern_match_zero():
	c = classifier('/\w+/+?,/abc/ is foo')
	assert str(c.classify('abc xyz')) == 'abc xyz'
	
def test_lazy_zero_many_dual_pattern_match_zero_many():
	c = classifier('/xyz/*?,/pqr/*?,/abc/ is foo')
	assert str(c.classify('pqr pqr abc xyz')) == '<foo>pqr pqr abc</foo>xyz'
	
def test_lazy_zero_many_dual_pattern_match_many_many():
	c = classifier('/xyz/*?,/pqr/*?,/abc/ is foo')
	assert str(c.classify('xyz xyz pqr pqr abc xyz')) == '<foo>xyz xyz pqr pqr abc</foo>xyz'

def test_lazy_zero_many_dual_pattern_match_many_zero():
	c = classifier('/xyz/*?,/pqr/*?,/abc/ is foo')
	assert str(c.classify('xyz xyz abc xyz')) == '<foo>xyz xyz abc</foo>xyz'

def test_lazy_zero_many_dual_pattern_match_zero_zero():
	c = classifier('/xyz/*?,/pqr/*?,/abc/ is foo')
	assert str(c.classify('abc xyz')) == '<foo>abc</foo>xyz'
	
def test_lazy_zero_many_dual_pattern_match_zero_many_not_start():
	c = classifier('/xyz/*?,/pqr/*?,/abc/ is foo')
	assert str(c.classify('zzz pqr pqr abc xyz')) == 'zzz<foo>pqr pqr abc</foo>xyz'
		
pytest.main()
