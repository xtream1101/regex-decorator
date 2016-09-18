# Regex Decorator

[![PyPI](https://img.shields.io/pypi/v/regex_decorator.svg)](https://pypi.python.org/pypi/regex_decorator)
[![PyPI](https://img.shields.io/pypi/l/regex_decorator.svg)](https://pypi.python.org/pypi/regex_decorator)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/ce0745991c4f49a0b9805d4cbeb10d2a)](https://www.codacy.com/app/eddy-hintze/regex-decorator?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xtream1101/regex-decorator&amp;utm_campaign=Badge_Coverage)

This library allows you to place a decorator on a function which has a regex as an argument. Then when parsing text, if that regex is found it will run the function and optionally return data


## Install
```
$ pip3 install regex_decorator
```

## Example

Can use `re` or `parse` in the decorator

Default for `parse_using` is `parse`

`@p.listener('my name is (\w+).', re.IGNORECASE, parse_using='re')`

`@p.listener('my name is (?P<name>\w+).', re.IGNORECASE, parse_using='re')`

`@p.listener('my name is {}.')`

`@p.listener('my name is {name}.')`

Both of the above will match `Eddy` with the input of `my name is Eddy.`

```python
# Content of test_strings.txt
# Foo 1
# Don't match this line
# maybe this line because the answer is 99
# Hi, my name is Eddy!
# the answer is 44, foo 4

import re
import logging
from regex_decorator import Parser

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

p = Parser()


@p.listener('my name is (\w+)', re.IGNORECASE, parse_using='re')
def name(matched_str, name):
    return name


@p.listener('The answer is (\d+)', re.IGNORECASE, parse_using='re')
def answer(matched_str, answer):
    return answer


@p.listener('foo (\d)', re.IGNORECASE, parse_using='re')
def foo(matched_str, value):
    return value


@p.listener('What is (?P<val1>\d+) \+ (?P<val2>\d+)', re.IGNORECASE, parse_using='re')
def add(matched_str, val2, val1):
    """
    When using named args in the regex `(?P<name>)`, the order of the args does not matter
    """
    ans = int(val1) + int(val2)
    print(val1, "+", val2, "=", ans)


example1 = p.parse("My name is Eddy, and the answer is 42.")
print(example1)  # Returns: Eddy

example2 = p.parse_all("My name is Eddy, and the answer is 42.")
print(example2)  # Returns: ['Eddy', '42']

example3 = p.parse_file('test_strings.txt')
print(example3)  # Returns: ['1', '99', 'Eddy', '44']

example4 = p.parse_file_all('test_strings.txt')
print(example4)  # Returns: ['1', '99', 'Eddy', '44', '4']

# It does not always have to return something and all action can be completed in the function like so:
p.parse("what is 2 + 3")  # Prints: 2 + 3 = 5

# Reference here for more examples: https://github.com/xtream1101/regex-decorator/blob/master/test_parsing.py

```

## Example Use case
Use it with a speach to text library and create custom home automation commands.
This example requires `speech_recognition`

`$ pip3 install speech_recognition`

```python
import re
import speech_recognition as sr
from regex_decorator import Parser

p = Parser()


@p.listener('Turn (?P<action>\w+) (?:my|the)?\s?(?P<item>.+)', re.IGNORECASE)
def on(matched_str, action, item):
    # Some home automation action here
    print("Turning", action, item)


# Try and say:
#   "Turn on living room lights"
#   "Turn off the living room lights"

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Google Speech Recognition
try:
    result = r.recognize_google(audio)
    print("Google Speech Recognition thinks you said " + result)
    p.parse(result)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
```

## Run tests
Just run the command `pytest` in the root directory (may need to `pip3 install pytest`)
