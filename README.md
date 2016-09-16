# Regex Decorator

This library allows you to place a decorator on a function which has a regex as an argument. Then when parsing text, if that regex is found it will run the function and optionally return data


## Install
```
$ pip3 install regex_decorator
```

## Example

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


@p.listener('my name is (\w+)', re.IGNORECASE)
def name(matched_str, value):
    return value


@p.listener('The answer is (\d+)', re.IGNORECASE)
def answer(matched_str, value):
    return value


@p.listener('foo (\d)', re.IGNORECASE)
def foo(matched_str, value):
    return value


@p.listener('What is (\d+) \+ (\d+)', re.IGNORECASE)
def add(matched_str, val1, val2):
    ans = int(val1) + int(val2)
    print(ans)


example1 = p.parse("My name is Eddy, and the answer is 42.")
print(example1)  # Returns: Eddy

example2 = p.parse_all("My name is Eddy, and the answer is 42.")
print(example2)  # Returns: ['Eddy', '42']

example3 = p.parse_file('test_strings.txt')
print(example3)  # Returns: ['1', '99', 'Eddy', '44']

example4 = p.parse_file_all('test_strings.txt')
print(example4)  # Returns: ['1', '99', 'Eddy', '44', '4']

# It does not always have to return something and all action can be completed in the function like so:
p.parse("what is 2 + 3")  # Prints: 5

# Reference here for more examples: https://github.com/xtream1101/regex-decorator/blob/master/test_parsing.py

```

## Run tests
Just run the command `pytest` in the root directory (may need to `pip3 install pytest`)
