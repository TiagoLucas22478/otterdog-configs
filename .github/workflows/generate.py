# *******************************************************************************
# Copyright (c) 2023 Eclipse Foundation and others.
# This program and the accompanying materials are made available
# under the terms of the MIT License
# which is available at https://spdx.org/licenses/MIT.html
# SPDX-License-Identifier: MIT
# *******************************************************************************

import sys
import json


def generate():

    with open("otterdog.json") as f:
        config = json.load(f)

    organizations = config["organizations"]

    EXTRA_DATA = './docs/orgs.yaml'
    NUM_ORGS = len(organizations)

    with open(EXTRA_DATA, "w") as extra:
        extra.write(f"count: {NUM_ORGS}")

    OUTPUT = './docs/orgs.csv'
    with open(OUTPUT, "w") as out:
        out.write("| Eclipse project | GitHub organization | Otterdog configuration | Dashboard |\n")
        out.write("| :-------------- | :------------------ | :--------------------- | :-------: |\n")

        for org in organizations:
            github_id = org["github_id"]
            name = org["name"]

            out.write(f"| [{name}](https://projects.eclipse.org/projects/{name}) "
                      f"| [{github_id}](https://github.com/{github_id}) "
                      f"| [{github_id}.jsonnet](https://github.com/{github_id}/.eclipsefdn/blob/main/otterdog/{github_id}.jsonnet) "
                      f"| [:link:](https://{github_id}.github.io/.eclipsefdn) |\n")


if __name__ == "__main__":
    generate()
    exit(0)
