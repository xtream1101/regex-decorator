import re


class WithRe:

    def __init__(self, regex_str, callback, flags=0):
        self.regex = re.compile(regex_str, flags)
        self.callback = callback
        self.text = None
        self.find_all = None

    def _parse_matches(self, results):
        rdata = []

        def append_rdata(data):
            output = self._parse_result(data)
            if output is not None:
                rdata.append(output)

        if self.find_all is False:
            # Only care about the first match
            append_rdata(results)
        else:
            if results is not None:
                for result in results:
                    append_rdata(result)

        return rdata

    def _parse_result(self, result):
        rdata = None

        if result is not None:
            if len(result.groupdict().keys()) != 0:
                rdata = self.callback(self.text, **result.groupdict())
            else:
                rdata = self.callback(self.text, *result.groups())

        return rdata

    def parse(self, text, find_all=False):
        self.text = text
        self.find_all = find_all

        if self.find_all is True:
            parse_func = re.finditer
        else:
            parse_func = re.search

        matched = parse_func(self.regex, self.text)

        return self._parse_matches(matched)
