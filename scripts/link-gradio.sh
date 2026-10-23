#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="link"
TARGET_DIR=""
GRADIO_DIR="gradio"

usage() {
  cat <<'USAGE'
Usage: scripts/link-gradio.sh [--mode link|copy] TARGET_DIR [GRADIO_DIR]
       scripts/link-gradio.sh link|copy TARGET_DIR [GRADIO_DIR]

Create TARGET_DIR/gradio from GRADIO_DIR. In link mode, create a symlink and
fall back to copying if symlinking fails. In copy mode, copy GRADIO_DIR
directly. Relative paths are resolved from the repository root. GRADIO_DIR
defaults to gradio.
USAGE
}

resolve_path() {
  case "$1" in
    /*) printf '%s\n' "$1" ;;
    *) printf '%s\n' "${ROOT_DIR}/$1" ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for --mode." >&2
        usage >&2
        exit 2
      fi
      MODE="${2:-}"
      shift 2
      ;;
    --mode=*)
      MODE="${1#--mode=}"
      shift
      ;;
    link|copy)
      MODE="$1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [[ -z "${TARGET_DIR}" ]]; then
        TARGET_DIR="$1"
      elif [[ "${GRADIO_DIR}" == "gradio" ]]; then
        GRADIO_DIR="$1"
      else
        echo "Unexpected argument: $1" >&2
        usage >&2
        exit 2
      fi
      shift
      ;;
  esac
done

if [[ "${MODE}" != "link" && "${MODE}" != "copy" ]]; then
  echo "Unsupported mode: ${MODE}. Expected link or copy." >&2
  exit 2
fi

if [[ -z "${TARGET_DIR}" ]]; then
  echo "Missing required TARGET_DIR." >&2
  usage >&2
  exit 2
fi

TARGET_DIR="$(resolve_path "${TARGET_DIR}")"
GRADIO_DIR="$(resolve_path "${GRADIO_DIR}")"

if [[ ! -d "${GRADIO_DIR}" ]]; then
  echo "Missing gradio directory: ${GRADIO_DIR}" >&2
  exit 1
fi

mkdir -p "${TARGET_DIR}"

DEST="${TARGET_DIR}/gradio"
if [[ -e "${DEST}" || -L "${DEST}" ]]; then
  rm -rf "${DEST}"
fi

if [[ "${MODE}" == "copy" ]]; then
  cp -R "${GRADIO_DIR}" "${DEST}"
  echo "Copied ${GRADIO_DIR} to ${DEST}"
  exit 0
fi

LINK_TARGET="${GRADIO_DIR}"
if command -v realpath >/dev/null 2>&1; then
  LINK_TARGET="$(realpath --relative-to="${TARGET_DIR}" "${GRADIO_DIR}")"
fi

if ln -s "${LINK_TARGET}" "${DEST}"; then
  echo "Linked ${DEST} -> ${LINK_TARGET}"
else
  echo "Symlink failed; copying ${GRADIO_DIR} to ${DEST}" >&2
  cp -R "${GRADIO_DIR}" "${DEST}"
fi
