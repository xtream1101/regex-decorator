import os
import re
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

    def listener(self, match_str, flags=0):

        def wrapper(func):
            self.listeners.append({'regex': re.compile(match_str, flags),
                                   'func': func
                                   })
            logger.info('Registered listener "{func}" to regex "{str}"'.format(func=func.__name__, str=match_str))
            return func

        return wrapper

    def _call_func(self, func, matched_str, matched_data):
        """
        Try and return keyed args if possible
        """
        if len(matched_data.groupdict().keys()) != 0:
            rdata = func(matched_str, **matched_data.groupdict())
        else:
            rdata = func(matched_str, *matched_data.groups())

        return rdata

    def _base_parse(self, input_data, re_func=re.search):
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
            for test in self.listeners:
                logger.debug("Test string '{str}' with regex '{regex}'".format(str=test_string, regex=test['regex']))
                matched = re_func(test['regex'], str(test_string))

                if matched:
                    if re_func.__name__ == 'search':
                        # Match on first occurrence then stop
                        rdata.append(self._call_func(test['func'], test_string, matched))
                        # Move on to the next test_string if an array was passed
                        break

                    elif re_func.__name__ == 'finditer' and matched:
                        # Return every occurrence found in the string
                        for match in matched:
                            rdata.append(self._call_func(test['func'], test_string, match))

        if len(rdata) == 0:
            rdata = None

        elif isinstance(orig_input, str) and re_func.__name__ == 'search':
            # If a single item was passed in, return a single item to be consistent
            rdata = rdata[0]

        return rdata

    def parse(self, input_data):
        """
        Find the first occurrence in a string
        If a list is passed in then the first occurrence in each item in that list
        """
        return self._base_parse(input_data)

    def parse_all(self, input_data, re_func=re.search):
        """
        Find all occurrences in a single string or in a list of strings
        """
        return self._base_parse(input_data, re_func=re.finditer)

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
