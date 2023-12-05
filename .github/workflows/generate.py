# *******************************************************************************
# Copyright (c) 2023 Eclipse Foundation and others.
# This program and the accompanying materials are made available
# under the terms of the MIT License
# which is available at https://spdx.org/licenses/MIT.html
# SPDX-License-Identifier: MIT
# *******************************************************************************

import sys
import json

import requests


def get_repo_status(token: str, owner: str, repo: str) -> (int, int):
    print(f"Checking repository {owner}/{repo}...")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    query = """query($org: String!, $repo: String!) {
        repository(owner: $org, name: $repo) {
            issues(first: 0, states: [OPEN]) {
                totalCount
            }
            pullRequests(first: 0, states: [OPEN]) {
                totalCount
            }
        }
    }"""

    query_total = """query($org: String!, $repo: String!) {
        repository(owner: $org, name: $repo) {
            issues(first: 0) {
                totalCount
            }
            pullRequests(first: 0) {
                totalCount
            }
        }
    }"""

    variables = {
        "org": owner,
        "repo": repo
    }

    response = requests.post("https://api.github.com/graphql", headers=headers, json={"query": query, "variables": variables})
    response_total = requests.post("https://api.github.com/graphql", headers=headers, json={"query": query_total, "variables": variables})

    data = response.json()["data"]["repository"]
    data_total = response_total.json()["data"]["repository"]

    if data is None:
        return 0, 0, 0, 0
    else:
        return (data.get("issues", {}).get("totalCount", 0), data.get("pullRequests", {}).get("totalCount", 0),
                data_total.get("issues", {}).get("totalCount", 0), data_total.get("pullRequests", {}).get("totalCount", 0))


def generate(token: str):

    with open("otterdog.json") as f:
        config = json.load(f)

    organizations = config["organizations"]

    EXTRA_DATA = './docs/orgs.yaml'
    NUM_ORGS = len(organizations)

    with open(EXTRA_DATA, "w") as extra:
        extra.write(f"count: {NUM_ORGS}")

    OUTPUT = './docs/orgs.csv'
    with open(OUTPUT, "w") as out:
        out.write("| Eclipse project | GitHub organization | Otterdog configuration | Dashboard | Open Issues | Open PRs | Total PRs |\n")
        out.write("| :-------------- | :------------------ | :--------------------- | :-------: | :---------: | :------: | :-------: |\n")

        openIssueSum = 0
        openPrSum = 0
        totalPrSum = 0

        for org in organizations:
            github_id = org["github_id"]
            eclipse_project = org["eclipse_project"]

            issueCount, prCount, totalIssueCount, totalPRCount = get_repo_status(token, github_id, ".eclipsefdn")

            openIssueSum += issueCount
            openPrSum += prCount
            totalPrSum += totalPRCount

            out.write(f"| [{eclipse_project}](https://projects.eclipse.org/projects/{eclipse_project}) "
                      f"| [{github_id}](https://github.com/{github_id}) "
                      f"| [{github_id}.jsonnet](https://github.com/{github_id}/.eclipsefdn/blob/main/otterdog/{github_id}.jsonnet) "
                      f"| [:link:](https://{github_id}.github.io/.eclipsefdn) "
                      f"| [{issueCount}](https://github.com/{github_id}/.eclipsefdn/issues) "
                      f"| [{prCount}](https://github.com/{github_id}/.eclipsefdn/pulls) "
                      f"| [{totalPRCount}](https://github.com/{github_id}/.eclipsefdn/pulls) |\n")
                      
        out.write(f"| Total | | | | {openIssueSum} | {openPrSum} | {totalPrSum} |\n")

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        print("Error: no token provided.")
        exit(1)

    generate(args[0])
    exit(0)
