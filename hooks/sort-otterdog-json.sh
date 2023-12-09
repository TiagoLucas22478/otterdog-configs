#!/usr/bin/env bash

set -e

script_dir="$( cd "$(dirname "$0")" ; pwd -P )"
project_dir="$(dirname "${script_dir}")"

jq ".organizations |= sort_by(.name)" < "$project_dir"/otterdog.json > tmp.$$ && mv tmp.$$ "$project_dir"/otterdog.json || rm tmp.$$
