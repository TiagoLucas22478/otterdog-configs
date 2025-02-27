#! /usr/bin/env python3
# *******************************************************************************
# Copyright (c) 2025 Eclipse Foundation and others.
# This program and the accompanying materials are made available
# under the terms of the MIT License
# which is available at https://spdx.org/licenses/MIT.html
# SPDX-License-Identifier: MIT
# *******************************************************************************

import os
import sys
import re
import subprocess


def process(file: str) -> None:
    if not os.path.exists(file):
        return

    with open(file, "r") as f:
        content = f.read()

    def replace(match: re.Match):
        path = match.group(1)
        indent = match.group(3)
        if indent is None:
            indent = 0
        else:
            indent = int(indent)

        result = subprocess.run(["pass", path], capture_output=True, text=True)
        replacement = result.stdout.strip()

        value = ""
        index = 0
        for line in replacement.split("\n"):
            if index == 0:
                value = line
            else:
                value = value + "\n" + (" " * indent) + line
            index = index + 1

        return value

    print(re.sub(r"{{([a-zA-Z0-9/\-_]+)(:([0-9]+))?}}", replace, content))


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        exit(1)

    process(sys.argv[1])
    exit(0)
