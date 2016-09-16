import os
import re
import logging

logger = logging.getLogger(__name__)


class Parser():

    def __init__(self):
        self.listeners = []

    def listener(self, match_str, flags=0):

        def wrapper(func):
            self.listeners.append({'regex': re.compile(match_str, flags), 'func': func})
            logger.info('Registered listener "{func}" to regex "{str}"'.format(func=func.__name__, str=match_str))
            return func

        return wrapper

    def parse(self, input_data):
        """
        Find the first occurrence in a string
        If a list is passed in then the first occurrence in each item in that list
        """
        listed_passed_in = True
        if isinstance(input_data, str):
            listed_passed_in = False
            input_data = [input_data]

        rdata = []
        for test_string in input_data:
            for test in self.listeners:
                logger.debug("Test string '{str}' with regex '{regex}'".format(str=test_string, regex=test['regex']))
                matched = re.search(test['regex'], str(test_string))
                if matched:
                    rdata.append(test['func'](test_string, *matched.groups()))
                    # Move on to the next test_string
                    break

        if len(rdata) == 0:
            rdata = None

        elif listed_passed_in is False:
            # If a string was passed in, then return as a string, not a list
            rdata = rdata[0]

        return rdata

    def parse_all(self, input_data):
        """
        Find all occurrences in a single string or in a list of strings
        """
        if isinstance(input_data, str):
            input_data = [input_data]

        rdata = []
        for test_string in input_data:
            for test in self.listeners:
                logger.debug("Test string '{str}' with regex '{regex}'".format(str=test_string, regex=test['regex']))
                matches = re.findall(test['regex'], str(test_string))
                if len(matches) > 0:
                    if len(matches) == 1:
                        # Check if only a single instance was found,
                        #   else when the * is applied it would break up the string
                        matches = [matches]

                    for matched in matches:
                        rdata.append(test['func'](test_string, *matched))

        return rdata

    def parse_file(self, file_path):
        """
        Read in a file and parse each line for the first occurrence of a match
        """
        content = self._read_file(file_path)
        rdata = self.parse(content)

        return rdata

    def parse_file_all(self, file_path):
        """
        Read in a file and parse each line for all occurrences of a match
        """
        content = self._read_file(file_path)
        rdata = self.parse_all(content)

        return rdata

    def _read_file(self, file_path):
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
