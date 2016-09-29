```
    !
   .-.
 __|=|__
(_/`-`\_)   This is Sir Json.
//\___/\\   Or Senior Json.
<>/   \<>
 \|_._|/    I can't decide.
  <_I_>
   |||      Either way, he's a fine fellow.
  /_|_\
 sr json
```

**ASCII credit**: _Joan G. Stark_

# srjson: self-referential json

**WARNING**: This is a WIP. Everything subject to ch-ch-ch-changes.

## tl;dr

srjson is json with self-referential tags. A small example:

```python
data = {
    "a": "<b>/bar",
    "b": "foo"
}

result = srjson.loads(data)

print (result)

# {
#     "a": "foo/bar",
#     "b": "foo"
# }
```

## ok;ib (ok, I'll bite)

A tag is any part of a string value that is enclosed in angle brackets. The
value within the tag is a lookup into the original json data. In the above
example, \<b\> is a lookup into data['b']. Here's another example:

```python
data = {
    "a": "<b.c>/bar",
    "b": {
        "c": "foo",
        "d": "baz"
    }
}

result = srjson.loads(data)

print (result)

# {
#     "a": "foo/bar",
#     "b": {
#         "c": "foo",
#         "d": "baz"
#     }
# }
```

You can use custom delimiters, rather than angle brackets. To use '%' instead:

```python
data = {
    "a": "%b%/bar",
    "b": "foo"
}

result = srjson.loads(data, delimiters=('%', '%'))

print (result)

# {
#     "a": "foo/bar",
#     "b": "foo"
# }

# or: srjson = SRJSON(delimiters=('%', '%'))
```

If a tag lookup doesn't reference a string value, then an error value is
returned:

```python
data = {
    "a": "<b>/bar",
    "b": {
        "c": "foo",
        "d": "baz"
    }
}

# {
#     "a": "|MISSING:b|/bar",
#     "b": {
#         "c": "foo",
#         "d": "baz"
#     }
# }
```

If the lookup value is a number, it is converted to a string:

```python
data = {
    "a": "<b>",
    "b": 1
}

# data = {
#     "a": "1",
#     "b": 1
# }
```

If the lookup value contains tags, those tags are also resolved, ad infinitum:

```python
data = {
    "a": "<b>",
    "b": "<c><d>",
    "c": "x",
    "d": "y"
}

# data = {
#     "a": "xy",
#     "b": "xy",
#     "c": "x",
#     "d": "y"
# }
```

Lookups can be into lists and dicts:

```python
data = {
    "a": "<b.c.0.x>/bar",
    "b": {
        "c": [
            {
                "x": "foo",
                "y": "baz"
            },
            "bar"
        ]
    }
}

# {
#     "a": "foo/bar",
#     "b": {
#         "c": [
#             {
#                 "x": "foo",
#                 "y": "baz"
#             },
#             "bar"
#         ]
#     }
# }
```

srjson only creates string values (this may change in the future):

```python
data = {
    "a": "<b>/bar",
    "b": 1
}

# {
#     "a": "1",
#     "b": 1
# }
```

srjson has two actions, #PASSWORD and #PROMPT. When encountering these, user
action is required to resolve values. srjson comes with a default resolver
for these two actions. For #PASSWORD:

```python
data = {
    "gmail": "<#PASSWORD>",
}

# user is prompted with "Enter password for 'gmail': ", after which:

# {
#     "a": "Somepassword1"
# }
```

For #PROMPT:

```python
data = {
    "name": {
        "first": "<#PROMPT>",
        "last": "<#PROMPT>"
    }
}

# user is prompted with "Enter value for 'name.first': ", after which:
# user is prompted with "Enter value for 'name.last': ", after which:

# data = {
#     "name": {
#         "first": "Jane",
#         "last": "Doe"
#     }
# }
```

You can write your own resolver and plug it in:

```python
srjson.loads(data, resolver=my_resolver)
```

See srjson.default_resolver for the required function signature.

srjson memorizes previous lookups by flattening the lookup paths:

```python
memo = {
    'mysite.password': 'hello'
}
```

A memo object of the above form can be passed in to loads:

```python
data = {
    "mysite": {
        "address": "www.foo.com",
        "pass": "<#PASSWORD>"
    }
}

srjson.loads(data, memo=memo)

# the #PASSWORD action will not need to be resolved, since the memo
# contains the value for the path:

# {
#     "mysite": {
#         "address": "www.foo.com",
#         "pass": "hello"
#     }
# }
```

## Considerations

 * srjson must always be valid json

## TODO

 * investigate [jsonpath_rw]() for replacing parser and path expressions
  * speed
  * simplicity
 * refactor resolvers so they are single functions per {action: resolver}
 * refactor SRJSON method args into generic **kwargs
