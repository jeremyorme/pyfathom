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
	
pytest.main()
