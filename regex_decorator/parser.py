import os
import logging
from regex_decorator.with_re import WithRe
from regex_decorator.with_parse import WithParse

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

    def listener(self, match_str, flags=0, parse_using='parse'):

        def wrapper(func):
            if parse_using == 're':
                parse_with = WithRe(match_str, func, flags=flags)

            else:
                # Default parser
                parse_with = WithParse(match_str, func)

            self.listeners.append(parse_with)
            logger.info("Registered listener '{func}' to regex '{str}'"
                        .format(func=func.__name__, str=match_str))
            return func

        return wrapper

    def _base_parse(self, input_data, find_all=False, **kwargs):
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
                             .format(str=test_string, regex=listener.regex))

                matched_data = listener.parse(test_string, find_all=find_all, **kwargs)

                if len(matched_data) != 0:
                    rdata.extend(matched_data)
                    if find_all is False:
                        break

        if len(rdata) == 0:
            rdata = None

        elif isinstance(orig_input, str) and find_all is False:
            # If a single item was passed in, return a single item to be consistent
            rdata = rdata[0]

        return rdata

    def parse(self, input_data, **kwargs):
        """
        Find the first occurrence in a string
        If a list is passed in then the first occurrence in each item in that list
        """
        return self._base_parse(input_data, find_all=False, **kwargs)

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
