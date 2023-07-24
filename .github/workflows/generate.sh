#!/bin/bash

EXTRA_DATA='./docs/orgs.yaml'
NUM_ORGS=$(jq -c '.organizations[]' < otterdog.json | wc -l)
cat <<EOT > ${EXTRA_DATA}
count: ${NUM_ORGS}
EOT

OUTPUT='./docs/orgs.csv'
cat <<EOT > ${OUTPUT}
Eclipse project,GitHub organization,Otterdog configuration
EOT

for org in $(jq -c '.organizations[]' < otterdog.json); do
  GITHUB_ID=$(echo $org | jq -r '.github_id')
  ECLIPSE_PROJECT=$(echo $org | jq -r '.eclipse_project')
  echo "[${ECLIPSE_PROJECT}](https://projects.eclipse.org/projects/${ECLIPSE_PROJECT}),[${GITHUB_ID}](https://github.com/${GITHUB_ID}),[${GITHUB_ID}.jsonnet](https://github.com/${GITHUB_ID}/.eclipsefdn
done
