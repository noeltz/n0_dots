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
# Handles both quoted (ID="void") and unquoted formats.
#
# Outputs:
#   Distribution ID to stdout: "void", "unknown"
# Returns:
#   0 on success, 1 on failure
detect_distro() {
  LAST_ERROR=""

  if [[ -f /etc/os-release ]]; then
    local id id_like
    id=$(awk -F= '/^ID=/{gsub(/["'"'"']/,"",$2); print tolower($2); exit}' /etc/os-release 2>/dev/null)

    case "$id" in
      void)
        printf '%s\n' "$id"
        return 0
        ;;
    esac

    id_like=$(awk -F= '/^ID_LIKE=/{gsub(/["'"'"']/,"",$2); print tolower($2); exit}' /etc/os-release 2>/dev/null)
    case "$id_like" in
      void)
        printf '%s\n' "$id_like"
        return 0
        ;;
    esac

    # Fallback: detect Void via its package manager
    if command -v xbps-install &>/dev/null; then
      printf 'void\n'
      return 0
    fi

    printf '%s\n' "$id"
    return 0
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
#   Package manager name to stdout: "xbps", "unsupported"
# Returns:
#   0 on success
get_pkg_manager() {
  local distro
  distro=$(detect_distro)

  case "$distro" in
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

# Roots may be replaced by isolated tests; production uses the real kernel files.
detect_vm() {
  local root="${N0_SYS_ROOT:-/sys}" proc="${N0_PROC_ROOT:-/proc}"
  [[ -s "$root/hypervisor/type" ]] && return 0
  grep -qw hypervisor "$proc/cpuinfo" 2>/dev/null && return 0
  grep -Eiq 'kvm|qemu|vmware|virtualbox|virtual machine|xen|bochs|parallels' \
    "$root/class/dmi/id/product_name" "$root/class/dmi/id/sys_vendor" 2>/dev/null
}
detect_laptop() {
  local root="${N0_SYS_ROOT:-/sys}" file chassis
  for file in "$root"/class/power_supply/*/type; do
    [[ -r "$file" ]] && [[ $(cat "$file") == Battery ]] && return 0
  done
  chassis=$(cat "$root/class/dmi/id/chassis_type" 2>/dev/null || true)
  case "$chassis" in 8|9|10|11|14|30|31|32) return 0;; esac
  return 1
}
detect_backlight() {
  local file
  for file in "${N0_SYS_ROOT:-/sys}"/class/backlight/*/max_brightness; do
    [[ -r "$file" ]] && return 0
  done
  return 1
}
detect_cpu_vendor() {
  awk '/vendor_id/ { if ($3 == "GenuineIntel") print "intel"; else if ($3 == "AuthenticAMD") print "amd"; else print "unknown"; exit }' "${N0_PROC_ROOT:-/proc}/cpuinfo"
}
machine_setting() {
  case "$1" in
    on) return 0;; off) return 1;; auto) "$2";;
    *) echo "Invalid machine setting: $1 (expected auto, on, off)" >&2; return 2;;
  esac
}
resolve_machine() {
  local value
  for value in "${MACHINE_VM_GUEST:-auto}" "${MACHINE_LAPTOP:-auto}" "${MACHINE_BACKLIGHT:-auto}"; do
    case "$value" in auto|on|off) ;; *) echo "Invalid machine setting: $value" >&2; return 2;; esac
  done
  IS_VM=false; IS_LAPTOP=false; HAS_BACKLIGHT=false
  if machine_setting "${MACHINE_VM_GUEST:-auto}" detect_vm; then IS_VM=true; fi
  if [[ $IS_VM == false ]]; then
    if machine_setting "${MACHINE_LAPTOP:-auto}" detect_laptop; then IS_LAPTOP=true; fi
    if machine_setting "${MACHINE_BACKLIGHT:-auto}" detect_backlight; then HAS_BACKLIGHT=true; fi
  fi
}
