import parse


class WithParse:

    def __init__(self, regex_str, callback):
        self.regex = parse.compile(regex_str)
        self.callback = callback
        self.text = None
        self.find_all = None

    def _parse_matches(self, results, **kwargs):
        rdata = []

        def append_rdata(data):
            output = self._parse_result(data, **kwargs)
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

    def _parse_result(self, result, **kwargs):
        rdata = None

        if result is not None:
            if len(result.named.keys()) != 0:
                rdata = self.callback(self.text, **result.named, **kwargs)
            else:
                rdata = self.callback(self.text, *result.fixed, **kwargs)

        return rdata

    def parse(self, text, find_all=False, **kwargs):
        """
        Return a list, even if empty
        """
        self.text = text
        self.find_all = find_all

        if self.find_all is True:
            parse_func = self.regex.findall
        else:
            parse_func = self.regex.search

        matches = parse_func(self.text)

        return self._parse_matches(matches, **kwargs)
