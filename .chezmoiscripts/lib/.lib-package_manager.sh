#!/usr/bin/env bash
# .lib-package_manager.sh - Package installation and management
#
# Provides cross-distro package management for Arch Linux (pacman/AUR helpers)
# and Void Linux (xbps). Handles package existence checks, installation,
# and batch operations with automatic distro dispatch.
#
# Requires: .lib-platform.sh sourced for detect_distro()/get_pkg_manager()
#
# Globals:
#   LAST_ERROR - Error message from last failed operation
# Exit codes:
#   0 (success), 1 (failure), 2 (invalid args), 127 (missing dependency)

export LAST_ERROR="${LAST_ERROR:-}"

# Ensures platform detection is available.
# shellcheck source=/dev/null
_source_platform() {
  if ! command -v detect_distro &>/dev/null; then
    local lib_dir
    lib_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    source "$lib_dir/.lib-platform.sh"
  fi
}

# Detects available AUR helper (Arch Linux only).
#
# Checks for paru first, then yay.
#
# Globals:
#   LAST_ERROR - Set if no helper found
# Outputs:
#   AUR helper name to stdout: "paru" or "yay"
# Returns:
#   0 on success, 127 if not found
get_aur_helper() {
  local helper

  if command_exists paru; then
    helper="paru"
  elif command_exists yay; then
    helper="yay"
  else
    LAST_ERROR="No AUR helper found (paru or yay required)"
    return 127
  fi

  printf '%s\n' "$helper"
  return 0
}

# Checks if package is installed (cross-distro).
#
# Dispatches to pacman -Qi (Arch) or xbps-query (Void).
#
# Arguments:
#   $1 - Package name
# Globals:
#   LAST_ERROR - Set on failure
# Returns:
#   0 if installed, 1 if not, 2 on invalid args
package_exists() {
  local package_name="${1:-}"

  LAST_ERROR=""

  if [[ -z "$package_name" ]]; then
    LAST_ERROR="package_exists() requires package_name argument"
    return 2
  fi

  _source_platform
  local manager
  manager=$(get_pkg_manager)

  case "$manager" in
  pacman)
    pacman -Qi "$package_name" >/dev/null 2>&1
    ;;
  xbps)
    xbps-query "$package_name" >/dev/null 2>&1
    ;;
  *)
    LAST_ERROR="Unsupported package manager: $manager"
    return 127
    ;;
  esac
}

# Installs packages via AUR helper (Arch Linux).
#
# Internal function — use install_package() for cross-distro dispatch.
#
# Arguments:
#   $@ - Package names
# Globals:
#   LAST_ERROR - Set on failure
# Outputs:
#   SKIP messages to stderr via log() for already-installed packages
# Returns:
#   0 on success, 1 on failure, 2 on invalid args, 127 if no AUR helper
_install_package_pacman() {
  local -a packages_to_install=()
  local package_name

  LAST_ERROR=""

  declare -A _installed_lookup=()
  local _pkg
  local installed_pkgs

  if installed_pkgs="$({ pacman -Qq 2>/dev/null || true; })"; then
    while IFS= read -r _pkg; do
      _installed_lookup["$_pkg"]=1
    done <<<"$installed_pkgs"
  fi

  for package_name in "$@"; do
    if [[ -n "${_installed_lookup[$package_name]:-}" ]]; then
      log SKIP "${COLOR_GREEN}${package_name}${COLOR_RESET} exists"
    else
      packages_to_install+=("$package_name")
    fi
  done

  if [[ ${#packages_to_install[@]} -eq 0 ]]; then
    return 0
  fi

  local aur_helper

  if ! aur_helper="$(get_aur_helper)"; then
    return 127
  fi

  if ! "$aur_helper" -S --needed --noconfirm "${packages_to_install[@]}"; then
    LAST_ERROR="Failed to install packages with $aur_helper: ${packages_to_install[*]}"
    return 1
  fi

  return 0
}

# Installs packages via xbps-install (Void Linux).
#
# Internal function — use install_package() for cross-distro dispatch.
# Skips already-installed packages with SKIP log message.
#
# Arguments:
#   $@ - Package names
# Globals:
#   LAST_ERROR - Set on failure
# Outputs:
#   SKIP messages to stderr via log() for already-installed packages
# Returns:
#   0 on success, 1 on failure, 2 on invalid args
_install_package_xbps() {
  local -a packages_to_install=()
  local package_name

  LAST_ERROR=""

  for package_name in "$@"; do
    if xbps-query "$package_name" >/dev/null 2>&1; then
      log SKIP "${COLOR_GREEN}${package_name}${COLOR_RESET} exists"
    else
      packages_to_install+=("$package_name")
    fi
  done

  if [[ ${#packages_to_install[@]} -eq 0 ]]; then
    return 0
  fi

  log INFO "Installing: ${packages_to_install[*]}"
  if ! sudo xbps-install -y "${packages_to_install[@]}"; then
    LAST_ERROR="Failed to install packages with xbps-install: ${packages_to_install[*]}"
    return 1
  fi

  return 0
}

# Installs packages (cross-distro dispatch).
#
# Dispatches to pacman/AUR helper (Arch) or xbps-install (Void).
# Skips already-installed packages with SKIP log message.
#
# Arguments:
#   $@ - Package names
# Globals:
#   LAST_ERROR - Set on failure
# Outputs:
#   SKIP messages to stderr via log() for already-installed packages
# Returns:
#   0 on success, 1 on failure, 2 on invalid args, 127 if no package manager
install_package() {
  LAST_ERROR=""

  if [[ $# -eq 0 ]]; then
    LAST_ERROR="install_package() requires at least one package name"
    return 2
  fi

  _source_platform
  local manager
  manager=$(get_pkg_manager)

  case "$manager" in
  pacman)
    _install_package_pacman "$@"
    ;;
  xbps)
    _install_package_xbps "$@"
    ;;
  *)
    LAST_ERROR="Unsupported package manager: $manager"
    return 127
    ;;
  esac
}

# Installs a group of packages with a descriptive name.
#
# Arguments:
#   $1 - Group name (for logging)
#   $@ - Package names
# Globals:
#   LAST_ERROR - Set on failure
# Outputs:
#   STEP messages to stderr via log()
# Returns:
#   0 on success, 1 on failure, 2 on invalid args, 127 if no AUR helper
install_group() {
  local group_name="$1"
  shift

  if [[ $# -eq 0 ]]; then
    return 0
  fi

  log STEP "Installing $group_name packages"

  if ! install_package "$@"; then
    die "$LAST_ERROR"
  fi
}
