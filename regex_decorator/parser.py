import os
import re
import parse
import logging

logger = logging.getLogger(__name__)


def _read_file(file_path):
    content = ''
    # Check if file exists
    if os.path.isfile(file_path) is False:
        logger.error("File {file} does not exist".format(file=file_path))
        return content

    with open(file_path) as f:
        content = f.readlines()
        # Strip out just the newline char at the end of line
        content = [l.rstrip('\n') for l in content]

    return content


class Parser():

    def __init__(self):
        self.listeners = []

    def listener(self, match_str, flags=0, parse_with='parse'):
        if parse_with == 're':
            parse_with = re
            compiled_regex = re.compile(match_str, flags)
        else:
            # Default parser
            parse_with = parse
            compiled_regex = parse.compile(match_str)

        def wrapper(func):
            self.listeners.append({'regex': compiled_regex,
                                   'func': func,
                                   'parse_with': parse_with,
                                   })
            logger.info("Registered listener '{func}' to regex '{str}'"
                        .format(func=func.__name__, str=match_str))
            return func

        return wrapper

    @classmethod
    def _call_func(cls, listener, matched_str, matched_data):
        """
        Try and return keyed args if possible
        """
        if listener['parse_with'] == re:
            # Use re
            if len(matched_data.groupdict().keys()) != 0:
                rdata = listener['func'](matched_str, **matched_data.groupdict())
            else:
                rdata = listener['func'](matched_str, *matched_data.groups())

        else:
            # Use parse
            if len(matched_data.named.keys()) != 0:
                rdata = listener['func'](matched_str, **matched_data.named)
            else:
                rdata = listener['func'](matched_str, *matched_data.fixed)

        return rdata

    def _base_parse(self, input_data, find_all=False):
        """
        All of the parsing is done ehre
        """
        orig_input = input_data
        if isinstance(input_data, str):
            input_data = [input_data]

        rdata = []
        # Check each string that was passed
        for test_string in input_data:
            # Check each listener for a match, if *_all, then always check all, else break after first match
            for listener in self.listeners:
                logger.debug("Test string '{str}' with regex '{regex}'"
                             .format(str=test_string, regex=listener['regex']))

                if listener['parse_with'] == re:
                    # Parse using re
                    if find_all is True:
                        parse_func = re.finditer
                    else:
                        parse_func = re.search

                    matched = parse_func(listener['regex'], str(test_string))

                else:
                    # Parse using parse
                    if find_all is True:
                        parse_func = listener['regex'].findall
                    else:
                        parse_func = listener['regex'].search

                    matched = parse_func(str(test_string))

                if matched:
                    if find_all is False:
                        # Match on first occurrence then stop
                        rdata.append(self._call_func(listener, test_string, matched))
                        # Move on to the next test_string if an array was passed
                        break

                    elif find_all is True and matched:
                        # Return every occurrence found in the string
                        for match in matched:
                            rdata.append(self._call_func(listener, test_string, match))

        if len(rdata) == 0:
            rdata = None

        elif isinstance(orig_input, str) and find_all is False:
            # If a single item was passed in, return a single item to be consistent
            rdata = rdata[0]

        return rdata

    def parse(self, input_data):
        """
        Find the first occurrence in a string
        If a list is passed in then the first occurrence in each item in that list
        """
        return self._base_parse(input_data, find_all=False)

    def parse_all(self, input_data):
        """
        Find all occurrences in a single string or in a list of strings
        """
        return self._base_parse(input_data, find_all=True)

    def parse_file(self, file_path):
        """
        Read in a file and parse each line for the first occurrence of a match
        """
        content = _read_file(file_path)
        rdata = self.parse(content)

        return rdata

    def parse_file_all(self, file_path):
        """
        Read in a file and parse each line for all occurrences of a match
        """
        content = _read_file(file_path)
        rdata = self.parse_all(content)

        return rdata
