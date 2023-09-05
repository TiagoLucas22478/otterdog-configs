import sys
import json

from typing import Optional

import requests


def get_repo_status(token: Optional[str], owner: str, repo: str) -> (int, int):
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

    variables = {
        "org": owner,
        "repo": repo
    }

    response = requests.post("https://api.github.com/graphql", headers=headers, json={"query": query, "variables": variables})

    data = response.json()["data"]["repository"]
    return data["issues"]["totalCount"], data["pullRequests"]["totalCount"]


def generate(token: Optional[str]):

    with open("otterdog.json") as f:
        config = json.load(f)

    organizations = config["organizations"]

    EXTRA_DATA = './docs/orgs.yaml'
    NUM_ORGS = len(organizations)

    with open(EXTRA_DATA, "w") as extra:
        extra.write(f"count: {NUM_ORGS}")

    OUTPUT = './docs/orgs.csv'
    with open(OUTPUT, "w") as out:
        out.write("| Eclipse project | GitHub organization | Otterdog configuration | Dashboard | Open Issues | Open PRs |\n")
        out.write("| :-------------- | :------------------ | :--------------------- | :-------: | :---------: | :------: |\n")

        for org in organizations:
            github_id = org["github_id"]
            eclipse_project = org["eclipse_project"]

            issueCount, prCount = get_repo_status(token, github_id, ".eclipsefdn")

            out.write(f"| [{eclipse_project}](https://projects.eclipse.org/projects/{eclipse_project}) "
                      f"| [{github_id}](https://github.com/{github_id}) "
                      f"| [{github_id}.jsonnet](https://github.com/{github_id}/.eclipsefdn/blob/main/otterdog/{github_id}.jsonnet) "
                      f"| [:link:](https://{github_id}.github.io/.eclipsefdn) "
                      f"| [{issueCount}](https://github.com/{github_id}/.eclipsefdn/issues) "
                      f"| [{prCount}](https://github.com/{github_id}/.eclipsefdn/pulls) |\n")


if __name__ == "__main__":
    args = sys.argv[1:]
    arg_token = args[0] if len(args) > 0 else None
    generate(arg_token)
