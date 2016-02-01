import re

import lxml.html
from lxml.cssselect import CSSSelector


__author__ = 'ivanenko.danil'

class BaseParser(object):
    """
    base clas for parsers, it saves selector in constructor
    """

    def __init__(self, selector):
        self.selector = selector

    def search(self, text):
        """
        get text and return result or empty string
        """
        pass


class RegexParser(BaseParser):
    """
    search text using regex selectors
    """

    def __init__(self, selector):
        super(RegexParser, self).__init__(selector)
        # compile regex pattern here, so we do not waist time later
        self.pattern = re.compile(self.selector)


    def search(self, text):
        match = self.pattern.search(text)
        if match:
            result = match.group(1)
        else:
            result = ""

        return result


class CSSParser(BaseParser):
    """
    search text using CSS selectors
    """

    def search(self, text):
        sel = CSSSelector(self.selector)
        # grrrr... not good idea to parse html for every selector
        tree = lxml.html.fromstring(text)
        results = sel(tree)
        if len(results) > 0:
            # exclude parent tag, we save only its content
            # also we record only first found tag, not all tags with selector
            res = (results[0].text or '') + "".join([lxml.html.tostring(child) for child in results[0]])
        else:
            res = ""

        return res

