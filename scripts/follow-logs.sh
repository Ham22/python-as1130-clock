#!/usr/bin/env bash

set -e

usage() {
  echo "Usage: $0 [--port port] [--debug] target-ip" 1>&2
  exit 1
}

PARAMS=""
while (( "$#" )); do
  case "${1}" in
    -p|--port)
      if [[ -n "${2}" ]] && [[ ${2:0:1} != "-" ]]; then
        PORT=${2}
        shift 2
      else
        echo "Error: Argument for ${1} is missing" 1>&2
        usage
      fi
      ;;
    -d|--debug)
      DEBUG=1
      shift
      ;;
    -*)
      echo "Error: Unsupported flag ${1}" 1>&2
      usage
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done

# set positional arguments in their proper place
eval set -- "$PARAMS"

IP_ADDRESS=${1}
PORT=${PORT:-22}
DEBUG=${DEBUG:-0}

if [[ -z ${IP_ADDRESS} ]]; then
  echo "Missing IP address" 1>&2
  usage
fi

USER_HOST="pi@${IP_ADDRESS}"
COMMON_OPTS=("-o" "LogLevel=error" "-o" "StrictHostKeyChecking=no")
SSH_OPTS=("${COMMON_OPTS[@]}" "-p" "${PORT}" "${USER_HOST}")
SCP_OPTS=("${COMMON_OPTS[@]}" "-P" "${PORT}")

follow_logs() {
  ssh "${SSH_OPTS[@]}" "sudo journalctl -fu clock"
}

follow_logs
