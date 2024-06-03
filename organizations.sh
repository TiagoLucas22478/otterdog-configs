#!/usr/bin/env bash
set -euo pipefail

list_all() {
  local ORGS
  ORGS=($(jq -r ".organizations[].github_id" < otterdog.json | sort))
  printf '%s\n' "${ORGS[@]}"
}

list_all_projects() {
  local PROJECTS
  PROJECTS=($(jq -r ".organizations[].name" < otterdog.json | sort))
  printf '%s\n' "${PROJECTS[@]}"
}

list_with_customization() {
  local ORGS
  ORGS=($(find -name "*.jsonnet" -exec grep -H "local" {} \; | grep -v "local orgs" | cut -f 1 -d ":" | cut -f 3 -d "/" | uniq | sort))
  printf '%s\n' "${ORGS[@]}"
}

list_without_customization() {
  local ALL_ORGS CUSTOM_ORGS ORGS
  ALL_ORGS=$(jq -r ".organizations[].github_id" < otterdog.json | sort)
  CUSTOM_ORGS=$(find -name "*.jsonnet" -exec grep -H "local" {} \; | grep -v "local orgs" | cut -f 1 -d ":" | cut -f 3 -d "/" | uniq | sort)

  ORGS=($({ printf '%s\n' "${ALL_ORGS[@]}" "${CUSTOM_ORGS[@]}"; } | sort | uniq -u))
  printf '%s\n' "${ORGS[@]}"
}

usage() {
  local USAGE
  USAGE="
Usage: $(basename "${0}") [OPTIONS]

Options:
  -a      list all configured organizations
  -p      list all configured projects
  -c      list organizations with customizations
  -n      list organizations without customizations
  -h      show this help

"
  echo "$USAGE"
}

ACTION=""

while getopts "apcn" opt; do
    case "${opt}" in
        a)
            ACTION="list-all"
            ;;
        p)
            ACTION="list-all-projects"
            ;;
        c)
            ACTION="list-with-customization"
            ;;
        n)
            ACTION="list-without-customization"
            ;;
        *)
            usage
            exit 0
            ;;
    esac
done

if [ -z "$ACTION" ]; then
  usage
  exit 1
fi

shift $((OPTIND-1))

case $ACTION in
  "list-all") list_all ;;
  "list-all-projects") list_all_projects ;;
  "list-with-customization") list_with_customization ;;
  "list-without-customization") list_without_customization ;;
   *) exit 1 ;;
esac

