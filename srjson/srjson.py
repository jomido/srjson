
#!/usr/bin/env python

import json

from .tokens import Token
from .tokenizer import tokenize
from .resolver import default_resolver

try:
    basestring
except NameError:
    basestring = (str, bytes)


def is_integer(s):

    try:
        int(s)
    except:
        return False

    return True


class SRJSON(object):

    def __init__(self, resolver=None, delimiters=('<', '>')):

        self.install = {}
        self.memo = {}
        self.resolver = resolver or default_resolver
        self.delimiters = delimiters

    def expand(self, s, parent_path='', delimiters=None):

        if parent_path in self.memo:
            return self.memo[parent_path]

        delimiters = delimiters or self.delimiters
        e = []
        tokens = tokenize(s, delimiters=delimiters)

        for token in tokens:

            if token.type == Token.action:
                value = self.resolver(token.value, parent_path)
                e.append(self.expand(value, parent_path, delimiters=delimiters))

            elif token.type == Token.lookup:

                path = token.value.split('.')
                value = self.install
                path_x = path[:]

                while path_x:

                    path_part = path_x.pop(0)

                    try:
                        if (is_integer(path_part)):
                            try:
                                value = value[int(path_part)]
                            except:
                                value = '|MISSING:{}|'.format(
                                    '.'.join(path + [path_part])
                                )
                                break
                        else:
                            value = value.get(path_part, {})
                    except:
                        value = '|MISSING:{}|'.format('.'.join(path))
                        break

                if isinstance(value, dict):
                    value = '|MISSING:{}|'.format('.'.join(path))
                    e.append(value)
                else:
                    e.append(self.expand(
                        str(value), '.'.join(path), delimiters=delimiters
                    ))

            else:

                e.append(token.value)

        result = ''.join(e)

        self.memo[parent_path] = result

        return result

    def build(self, o, path=None, delimiters=None):

        if isinstance(o, dict):

            d = {}

            for k, v in o.items():

                if path is None:
                    p = k
                else:
                    p = '.'.join([path, k])

                d[k] = self.build(v, p, delimiters=delimiters)

            return d

        elif isinstance(o, list):

            path = path or ''

            l = []

            for i, e in enumerate(o):

                if path is None:
                    path = str(i)
                else:
                    path = '.'.join([path, str(i)])

                l.append(self.build(e, path, delimiters=delimiters))

            return l

        elif isinstance(o, basestring):

            return self.expand(o, path, delimiters=delimiters)

        else:
            return o

    def loads(self, raw, memo=None, resolver=None, delimiters=None):

        data = json.loads(raw)

        self.install = data
        self.memo = memo or {}

        if resolver is None:
            resolver = default_resolver

        old_resolver = self.resolver
        self.resolver = resolver

        result = self.build(data, delimiters=delimiters)

        self.resolver = old_resolver

        return result


srjson = SRJSON()


def loads(raw, **kwargs):

    return srjson.loads(raw, **kwargs)


def main():

    # TODO
    raise Exception("Script tool not implemented.")
