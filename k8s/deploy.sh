#! /usr/bin/env bash
# *******************************************************************************
# Copyright (c) 2025 Eclipse Foundation and others.
# This program and the accompanying materials are made available
# under the terms of the MIT License
# which is available at https://spdx.org/licenses/MIT.html
# SPDX-License-Identifier: MIT
# *******************************************************************************

# Bash strict-mode
set -o nounset
set -o pipefail

IFS=$'\n\t'

ENVIRONMENT="${1:-production}"
NAMESPACE="foundation-internal-security-otterdog"

if ! [[ "${ENVIRONMENT}" =~ ^(production|staging)$ ]]; then
  echo "ERROR: can only deploy 'production' or 'staging'." >&2
  exit 1
fi

LOCAL_CONFIG="${HOME}/.cbi/config"

if [[ ! -f "${LOCAL_CONFIG}" ]] && [[ -z "${PASSWORD_STORE_DIR:-}" ]]; then
  echo "ERROR: File '$(readlink -f "${LOCAL_CONFIG}")' does not exists"
  echo "Create one to configure the location of the password store. Example:"
  echo '{"password-store": {"it-dir": "~/.password-store"}}' | jq '.'
fi
PASSWORD_STORE_DIR="$(jq -r '.["password-store"]["it-dir"]' "${LOCAL_CONFIG}")"
PASSWORD_STORE_DIR="$(readlink -f "${PASSWORD_STORE_DIR/#~\//${HOME}/}")"
export PASSWORD_STORE_DIR

echo "Deploying ${ENVIRONMENT} to namespace ${NAMESPACE}"

declare -a elements=("volume" "secret" "redis" "mongodb" "ghproxy" "otterdog")
for element in "${elements[@]}"
do
   FILE="${element}-${ENVIRONMENT}".yml
   echo "Applying ${FILE}"
   ./template.py "${FILE}" | kubectl apply -f -
done

echo "Done."