import re
from regex_decorator import Parser

p = Parser()


@p.listener('my name is (\w+)', re.IGNORECASE, parse_using='re')
def name(matched_str, value):
    return value


@p.listener('The answer is (\d+)', re.IGNORECASE, parse_using='re')
def answer(matched_str, value):
    return value


@p.listener('foo (\d)', re.IGNORECASE, parse_using='re')
def foo(matched_str, value):
    return value


@p.listener('foo (?P<foo>\w+) bar (?P<bar>\w+)', re.IGNORECASE, parse_using='re')
def this_that(matched_str, bar, foo):
    """
    Checks that even though the args are reversed, the data is collected correctly
    """
    return foo + '-' + bar


#
# Test p.parse()
#
def test_parse_1():
    """
    Simple word parse
    """
    assert p.parse('my name is Eddy') == 'Eddy'


def test_parse_2():
    """
    Simple number parse
    """
    assert p.parse('The answer is 42') == '42'


def test_parse_3():
    """
    Only parse the first thing found
    """
    assert p.parse('foo 1, foo 2, Foo 3') == '1'


def test_parse_4():
    """
    Dont match anything
    """
    assert p.parse('Dont match anything') is None


def test_parse_5():
    """
    Dont match anything
    """
    assert p.parse(['Dont match anything', 'stil, nothing']) is None


def test_parse_6():
    """
    Match only one thing
    Since we passed in an array, the single match will be returned in an array
    """
    assert p.parse(['Dont match anything', 'foo 3', 'jk, just match that last one :)']) == ['3']


def test_parse_7():
    """
    Parse the first thing found in each of the items in the array
    """
    assert p.parse(['Foo 1', 'foo 2', 'Foo 3 foo 4']) == ['1', '2', '3']


def test_parse_8():
    """
    This works as it should, only getting the first result, but test_parse_9() broke it
    """
    assert p.parse('The answer is 42 and foo 5') == '42'


def test_parse_9():
    """
    Bug found, if a string contains something that will match two different regex's it will return both
    That should not happen
    Fixed in 0.1.1
    """
    assert p.parse(['The answer is 42 and foo 5']) == ['42']


def test_parse_10():
    """
    When using named args, order should not matter
    """
    assert p.parse("foo this bar that") == 'this-that'


def test_parse_11():
    """
    When using named args, order should not matter
    """
    assert p.parse(["foo this bar that", "foo one bar two"]) == ['this-that', 'one-two']


#
# Test p.parse_all()
#
def test_parse_all_1():
    """
    return all instances found
    """
    assert p.parse_all('foo 1 and foo 2 and another foo 3') == ['1', '2', '3']


def test_parse_all_2():
    """
    Parse all instances in each item in the list
    """
    assert p.parse_all(['Foo 1', 'foo 2', 'Foo 3 foo 4']) == ['1', '2', '3', '4']


def test_parse_all_3():
    """
    return all instances found, from 2 different functions
    """
    assert p.parse_all('The answer is 42 as well as foo 3') == ['42', '3']


def test_parse_all_4():
    """
    return all instances found, from 2 different functions
    """
    assert p.parse_all(['The answer is 42 as well as foo 3']) == ['42', '3']


def test_parse_all_5():
    """
    When using named args, order should not matter
    """
    assert p.parse_all("foo this bar that as well as foo one bar two") == ['this-that', 'one-two']


#
# Test p.parse_file()
#
def test_parse_file_1():
    """
    return all instances found
    """
    assert p.parse_file('tests/test_strings.txt') == ['1', '99', 'Eddy', '44']


def test_parse_file_2():
    """
    Test when a file does not exist
    """
    assert p.parse_file('not_a_file.txt') is None


#
# Test p.parse_file_all()
#
def test_parse_file_all_1():
    """
    return all instances found
    """
    assert p.parse_file_all('tests/test_strings.txt') == ['1', '99', 'Eddy', '44', '4']
