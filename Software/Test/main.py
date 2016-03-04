#!/bin/env python

import markdown

print(markdown.markdown("Hi\n=="))

for i in range(0, 10):
    print(i)

print(markdown.markdown("Hi\n--"))

