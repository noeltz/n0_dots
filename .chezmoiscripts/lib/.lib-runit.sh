#!/usr/bin/env bash
# .lib-runit.sh - Runit service management
#
# Provides functions to manage runit services on Void Linux.
#
# Globals:
#   LAST_ERROR - Error message from last failed operation
# Exit codes:
#   0 (success), 1 (failure), 2 (invalid args), 127 (missing dependency)

export LAST_ERROR="${LAST_ERROR:-}"

# Enables a runit service.
#
# Creates symlink from /etc/sv/<service> to /var/service/<service>
# and starts the service.
#
# Arguments:
#   $1 - Service name (e.g., 'greetd', 'NetworkManager')
#   $2 - Scope: 'system' or 'user' (default: 'system')
# Globals:
#   LAST_ERROR - Set on failure
# Returns:
#   0 on success, 1 on failure, 2 on invalid args, 127 if sv not found
runit_enable_service() {
  local service="${1:-}"
  local scope="${2:-system}"

  LAST_ERROR=""

  if [[ -z "$service" ]]; then
    LAST_ERROR="runit_enable_service() requires a service argument"
    return 2
  fi

  if [[ "$scope" != "system" ]] && [[ "$scope" != "user" ]]; then
    LAST_ERROR="Invalid scope: $scope (must be 'system' or 'user')"
    return 2
  fi

  if ! command -v sv &>/dev/null; then
    LAST_ERROR="sv command not found (runit not installed)"
    return 127
  fi

  local service_dir="/etc/sv/${service}"
  local service_link="/var/service/${service}"

  if [[ "$scope" == "user" ]]; then
    service_dir="$HOME/.local/service/${service}"
    service_link="$HOME/.local/service/${service}"
  fi

  # Check if service exists
  if [[ ! -d "$service_dir" ]]; then
    LAST_ERROR="Service directory not found: $service_dir"
    return 1
  fi

  # Check if already enabled
  if [[ -L "$service_link" ]]; then
    return 0
  fi

  # Create symlink
  if ! sudo ln -s "$service_dir" "$service_link" 2>/dev/null; then
    LAST_ERROR="Failed to enable service: $service"
    return 1
  fi

  # Start the service (give it a moment)
  sleep 1

  if ! sudo sv up "$service" &>/dev/null; then
    LAST_ERROR="Service failed to start: $service"
    return 1
  fi

  return 0
}

# Disables a runit service.
#
# Removes symlink from /var/service/<service> and stops the service.
#
# Arguments:
#   $1 - Service name (e.g., 'bluetoothd')
#   $2 - Scope: 'system' or 'user' (default: 'system')
# Globals:
#   LAST_ERROR - Set on failure
# Returns:
#   0 on success (disabled or already disabled), 1 on failure, 2 on invalid args
runit_disable_service() {
  local service="${1:-}"
  local scope="${2:-system}"

  LAST_ERROR=""

  if [[ -z "$service" ]]; then
    LAST_ERROR="runit_disable_service() requires a service argument"
    return 2
  fi

  if [[ "$scope" != "system" ]] && [[ "$scope" != "user" ]]; then
    LAST_ERROR="Invalid scope: $scope (must be 'system' or 'user')"
    return 2
  fi

  if ! command -v sv &>/dev/null; then
    LAST_ERROR="sv command not found (runit not installed)"
    return 127
  fi

  local service_link="/var/service/${service}"

  if [[ "$scope" == "user" ]]; then
    service_link="$HOME/.local/service/${service}"
  fi

  # Check if service is enabled
  if [[ ! -L "$service_link" ]]; then
    return 0
  fi

  # Stop the service
  if sudo sv status "$service" 2>/dev/null | grep -q "^run:"; then
    if ! sudo sv down "$service" &>/dev/null; then
      LAST_ERROR="Failed to stop service: $service"
      return 1
    fi
  fi

  # Remove symlink (requires root — /var/service is root-owned)
  if ! sudo rm -f "$service_link" 2>/dev/null; then
    LAST_ERROR="Failed to remove service symlink: $service_link"
    return 1
  fi

  return 0
}

# Checks if a runit service is enabled.
#
# Arguments:
#   $1 - Service name
#   $2 - Scope: 'system' or 'user' (default: 'system')
# Returns:
#   0 if enabled, 1 if not enabled, 2 on invalid args
runit_service_enabled() {
  local service="${1:-}"
  local scope="${2:-system}"

  if [[ -z "$service" ]]; then
    return 2
  fi

  local service_link="/var/service/${service}"

  if [[ "$scope" == "user" ]]; then
    service_link="$HOME/.local/service/${service}"
  fi

  [[ -L "$service_link" ]]
}

# Checks if a runit service is running.
#
# Arguments:
#   $1 - Service name
# Returns:
#   0 if running, 1 if not running or invalid
runit_service_running() {
  local service="${1:-}"

  if [[ -z "$service" ]]; then
    return 1
  fi

  sv status "$service" 2>/dev/null | grep -q "^run:"
}