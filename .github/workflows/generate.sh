#!/bin/bash

EXTRA_DATA='./docs/orgs.yaml'
NUM_ORGS=$(jq -c '.organizations[]' < otterdog.json | wc -l)
cat <<EOT > ${EXTRA_DATA}
count: ${NUM_ORGS}
EOT

OUTPUT='./docs/orgs.csv'
cat <<EOT > ${OUTPUT}
Eclipse project,GitHub organization,Otterdog configuration,GH Page
EOT

for org in $(jq -c '.organizations[]' < otterdog.json); do
  GITHUB_ID=$(echo $org | jq -r '.github_id')
  ECLIPSE_PROJECT=$(echo $org | jq -r '.eclipse_project')
  echo "[${ECLIPSE_PROJECT}](https://projects.eclipse.org/projects/${ECLIPSE_PROJECT}),[${GITHUB_ID}](https://github.com/${GITHUB_ID}),[${GITHUB_ID}.jsonnet](https://github.com/${GITHUB_ID}/.eclipsefdn/blob/main/otterdog/${GITHUB_ID}.jsonnet),[https://${GITHUB_ID}.github.io/.eclipsefdn](https://${GITHUB_ID}.github.io/.eclipsefdn)" >> ${OUTPUT}
done
