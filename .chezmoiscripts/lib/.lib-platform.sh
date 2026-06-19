#!/usr/bin/env bash
# .lib-platform.sh - Platform detection utilities
#
# Provides functions to detect the distribution, package manager,
# and init system for the current environment.
#
# Globals:
#   LAST_ERROR - Error message from last failed operation
# Exit codes:
#   0 (success), 1 (failure), 2 (invalid args), 127 (unknown/unsupported)

export LAST_ERROR="${LAST_ERROR:-}"

# Detects the Linux distribution.
#
# Uses /etc/os-release to determine the distribution ID.
# Returns lowercase distribution name.
#
# Outputs:
#   Distribution ID to stdout: "arch", "void", "unknown"
# Returns:
#   0 on success, 1 on failure
detect_distro() {
  LAST_ERROR=""

  if [[ -f /etc/os-release ]]; then
    local id
    id=$(grep -oP '^ID=\K\w+' /etc/os-release 2>/dev/null | tr '[:upper:]' '[:lower:]')
    if [[ -n "$id" ]]; then
      printf '%s\n' "$id"
      return 0
    fi
  fi

  LAST_ERROR="Failed to detect distribution from /etc/os-release"
  printf 'unknown\n'
  return 1
}

# Detects the package manager for the current distribution.
#
# Maps distribution to its package manager.
#
# Outputs:
#   Package manager name to stdout: "pacman", "xbps", "unsupported"
# Returns:
#   0 on success
get_pkg_manager() {
  local distro
  distro=$(detect_distro)

  case "$distro" in
  arch)
    printf 'pacman\n'
    ;;
  void)
    printf 'xbps\n'
    ;;
  *)
    printf 'unsupported\n'
    return 1
    ;;
  esac
}

# Detects the init system in use.
#
# Checks for systemd or runit indicators.
#
# Outputs:
#   Init system name to stdout: "systemd", "runit", "unsupported"
# Returns:
#   0 on success, 1 on unsupported
get_init_system() {
  LAST_ERROR=""

  if [[ -d /run/systemd/system ]]; then
    printf 'systemd\n'
    return 0
  elif command -v sv &>/dev/null && [[ -d /etc/sv ]]; then
    printf 'runit\n'
    return 0
  elif command -v openrc-init &>/dev/null; then
    printf 'openrc\n'
    return 0
  fi

  LAST_ERROR="No supported init system found (systemd, runit, openrc)"
  printf 'unsupported\n'
  return 1
}