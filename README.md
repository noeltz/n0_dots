<p align="center">
  <img src="assets/n0_dots-logo.svg" alt="n0_dots" width="400">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Void_Linux-7C3AED?style=flat&logoColor=white&labelColor=1a1b26" alt="Void Linux">
  <img src="https://img.shields.io/badge/Niri-7C3AED?style=flat&logoColor=white&labelColor=1a1b26" alt="Niri">
  <img src="https://img.shields.io/badge/Noctalia_v5-A78BFA?style=flat&logoColor=white&labelColor=1a1b26" alt="Noctalia v5">
  <img src="https://img.shields.io/badge/Zsh-7C3AED?style=flat&logo=gnubash&logoColor=white&labelColor=1a1b26" alt="Zsh">
  <img src="https://img.shields.io/badge/Nix-7C3AED?style=flat&logo=nixos&logoColor=white&labelColor=1a1b26" alt="Nix">
  <img src="https://img.shields.io/badge/Chezmoi-565f89?style=flat&logoColor=white&labelColor=1a1b26" alt="Chezmoi">
</p>

<br>

<p align="center">
  <img src="https://img.shields.io/badge/Quick_Start-7C3AED?style=for-the-badge" alt="Quick Start">
</p>

A declarative, Void-Linux-only desktop setup managed with [chezmoi](https://chezmoi.io): Umbriel (preferred) or Niri (alternative), both Wayland, with the Noctalia shell, a dinit-supervised user session, Nix packages alongside XBPS, and libvirt virtualization.

```bash
sh -c "$(curl -fsLS https://get.chezmoi.io)" -- init --apply https://github.com/noeltz/n0_dots.git
```

Or step by step:

```bash
# Install chezmoi
sudo xbps-install -S chezmoi

# Clone and apply
chezmoi init --apply https://github.com/noeltz/n0_dots.git
```

<br>

<p align="center">
  <img src="https://img.shields.io/badge/What_This_Sets_Up-7C3AED?style=for-the-badge" alt="What This Sets Up">
</p>

| Category | What Gets Configured |
|----------|---------------------|
| **Repositories** | XBPS: nonfree, Noctalia, n0 (self-hosted) · Nix channel (nixpkgs-unstable) |
| **Packages** | ~133 Void (xbps) + Nix packages via `packages_void.toml` / `packages_nix.toml` |
| **Shell** | Zsh as default shell, Starship prompt, Sheldon plugin manager |
| **Window Manager** | Umbriel by default; Niri available in tuigreet |
| **Display Manager** | greetd + tuigreet (vt=7, `_greeter` user) |
| **Session Supervision** | User **dinit** instance spawned by either compositor, supervising pipewire, wireplumber, pipewire-pulse and noctalia — auto-restart, dependency ordering, per-service `dinitctl restart <name>` |
| **System Services** | runit services declaratively enabled/disabled via `services.toml` |
| **Logging** | socklog per-facility system logging (runit) |
| **Virtualization** | QEMU/KVM + libvirt host (virt-manager, virt-viewer, vsv; user added to `kvm`/`libvirt` groups) |
| **Backlight** | Brightness saved on change and restored across reboots (runit + inotify) |
| **Terminal** | Kitty with shell integration |
| **Fonts** | Maple Mono Nerd Font, JetBrains Mono, Cascadia Code, Inter, Roboto, Noto Emoji |
| **Icons** | Papirus icon theme, Tabler icons |
| **GTK** | adw-gtk3-dark theme, Bibata cursor, dark color scheme |
| **Browser** | Helium (Chromium-based) with Widevine DRM |
| **Editor** | Micro (`EDITOR`, `SUDO_EDITOR`); Zed (`VISUAL`), Neovim, Vim and VS Code also installed |
| **Developer Tools** | Git, GitHub CLI, Neovim, LazyGit, Yazi, Zoxide, FZF, ripgrep, Bat, Eza |
| **Maintenance** | `sysupdate` — update xbps + Nix + Flatpak, report services needing restart, reboot check |
| **XDG** | Full XDG Base Directory compliance, autostart management |
| **Secrets** | Proton Pass CLI integration (non-fatal if unavailable) |
| **Wallpapers** | Auto-downloaded from GitHub releases |

<br>

<p align="center">
  <img src="https://img.shields.io/badge/Typical_Use_Cases-7C3AED?style=for-the-badge" alt="Typical Use Cases">
</p>

### Initial Setup on a Fresh Void Install

```bash
sh -c "$(curl -fsLS https://get.chezmoi.io)" -- init --apply https://github.com/noeltz/n0_dots.git
```

This single command will:
1. Install chezmoi
2. Clone the repo
3. Apply all dotfiles and run setup scripts
4. Configure XBPS repositories (nonfree, Noctalia, n0), install all packages (xbps + Nix), fonts, icons, themes
5. Set up runit system services, the dinit user-session supervisor, backlight persistence, the libvirt host, greetd, shell, git, GitHub CLI and Proton Pass

### Pull Latest Changes and Apply

```bash
chezmoi update
```

This pulls the latest changes from the repo and applies them. Scripts run only when their source files change (hash-based detection).

### Update the System

```bash
sysupdate            # xbps + Nix + Flatpak; reports services needing restart and reboots
sysupdate -y         # non-interactive
```

### Preview Changes Before Applying

```bash
chezmoi git pull -- --autostash --rebase && chezmoi diff
```

Shows what would change without applying. If happy:

```bash
chezmoi apply
```

### Edit a Managed Dotfile

```bash
chezmoi edit ~/.config/niri/config.kdl
```

Opens the source file in your editor. With `--watch`, changes auto-apply on save:

```bash
chezmoi edit --watch ~/.config/niri/config.kdl
```

### Add a New Managed File

```bash
chezmoi add ~/.config/some-app/config.toml
```

### Commit and Push Local Changes

```bash
chezmoi git add --all && chezmoi git commit -m "update: description" && chezmoi git push
```

Or using chezmoi's built-in git wrapper:

```bash
chezmoi git add --all
chezmoi git commit -m "update: description"
chezmoi git push
```

### Check Status

```bash
chezmoi status
```

Shows which managed files have diverged from their source state.

### List All Managed Files

```bash
chezmoi list
```

### Resolve Merge Conflicts After Update

```bash
chezmoi merge ~/.config/niri/config.kdl
```

### Remove a Managed File

```bash
chezmoi forget ~/.local/bin/old-script.sh
```

<br>

<p align="center">
  <img src="https://img.shields.io/badge/How_It_Works-7C3AED?style=for-the-badge" alt="How It Works">
</p>

### Session & services

Two separate supervisors are in play:

- **System services — runit** (Void's init). Enabled via `services.toml` (`dbus`, `NetworkManager`, `chronyd`, logging, libvirt; hardware-selected `tlp` and `backlight`). Manage with `vsv` or `sv`.
- **User session services — dinit**. Either compositor spawns a user dinit instance (`~/.local/bin/dinit-session`) pointed at `~/.config/dinit.d/`, which supervises pipewire, wireplumber, pipewire-pulse, noctalia and the `dbus-env` one-shot. Each is started explicitly so it is independently restartable: `dinitctl restart noctalia`. On compositor exit, dinit gets SIGTERM and stops all session services.

### Script Execution Order

chezmoi runs scripts in a deterministic order:

```
1. run_before_ scripts (alphabetical)
2. Target state updates (files, directories, symlinks)
3. run_after_ scripts (alphabetical)
```

| Phase | Script | Purpose |
|-------|--------|---------|
| before | `00-configure-repos` | Configure Void XBPS repositories (nonfree, Noctalia, n0) + full system update |
| before | `10-install-package` | Install packages from `packages_void.toml` (xbps) + `packages_nix.toml` (nix-env) |
| before | `11-backlight-service` | Install the backlight-persistence runit service |
| before | `12-socklog-logging` | Provision socklog per-facility log directories |
| before | `13-system-fixes` | Void/runit service fixes (e.g. avahi chroot) |
| before | `20_wallpapers` | Download wallpapers from GitHub releases |
| before | `50_extra_packages` | Install packages outside the package manager |
| after | `04_login_manager` | Configure greetd display manager |
| after | `10-services` | Enable/disable runit system services |
| after | `11-fonts_and_icons` | Install Maple Mono, Papirus, Tabler |
| after | `11-xdg-autostart` | Configure XDG environment, initialize user directories, and disable unwanted autostart entries |
| after | `12-zram` | Provision zstd swap (50% RAM, maximum 8 GiB); preserve active swap |
| after | `15-virtualization` | Configure QEMU/KVM + libvirt host |
| after | `30-vscode-theme` | Install matugen VSCode theme |
| after | `80-init-proton-pass-cli` | Install and authenticate Proton Pass CLI |
| after | `81-init-github` | Authenticate GitHub CLI, configure git |
| after | `85-gtk-settings` | Apply GTK settings from `gtk.toml` |
| after | `91-helium-browser` | Configure Helium browser (Widevine, policies) |
| after | `99-switch-shell` | Switch default shell to zsh |
| after | `99-restart-notice` | Display restart notification |

`run_once_*` scripts execute once per machine; `run_onchange_*` re-run when their source hash changes.

### Data-Driven Configuration

Most configuration is declarative via `.chezmoidata/*.toml`:

| File | Controls |
|------|----------|
| `packages_void.toml`, `packages_nix.toml` | Void (xbps) and Nix package lists |
| `services.toml` | runit system services to enable/disable |
| `autostart.toml` | XDG autostart entries to disable |
| `gtk.toml` | GTK theme, fonts, cursor, Nautilus settings |

The dinit user-session service definitions live as plain files in `dot_config/dinit.d/` (→ `~/.config/dinit.d/`).

### Library Functions

Hidden library scripts in `.chezmoiscripts/lib/`:

| Library | Purpose |
|---------|---------|
| `.lib-common.sh` | Logging, sudo keepalive, config updates, service management, backups |
| `.lib-platform.sh` | Distribution, package-manager and init-system detection |
| `.lib-runit.sh` | Runit service enable/disable/stop |

<br>

<p align="center">
  <img src="https://img.shields.io/badge/Troubleshooting-7C3AED?style=for-the-badge" alt="Troubleshooting">
</p>

### "chezmoi: command not found"

Install chezmoi first:

```bash
sudo xbps-install -S chezmoi
```

### A dinit session service won't restart independently

Make sure no grouping `boot` target depends on the daemons (that causes restart cascades). Each session service must be explicitly activated by `dinit-session`; check with `dinitctl list`.

### Scripts re-run on every apply

Scripts with `run_once` in the name run only once. Scripts with `run_onchange` re-run when their source hash changes. If a script re-runs unexpectedly, check that the hash template is present:

```bash
head -5 .chezmoiscripts/run_onchange_after_*.sh.tmpl | grep run_onchange_hash
```

### View chezmoi debug output

```bash
chezmoi --verbose apply
```

### Reset to clean state

```bash
chezmoi purge
```

Removes the source directory and config. Re-init with:

```bash
chezmoi init --apply https://github.com/noeltz/n0_dots.git
```

<br>

<p align="center">
  <img src="https://img.shields.io/badge/License-565f89?style=for-the-badge" alt="License">
</p>

GNU General Public License v3.0 — see <a href="LICENSE">LICENSE</a>.

<br>

<p align="center">
  <img src="https://img.shields.io/badge/--1a1b26?style=flat" alt="">
</p>

## Portable desktop and machine settings

Umbriel is the default command in greetd/tuigreet. Use tuigreet's session selector
(F3) to choose Niri; `--remember-session` remembers an explicit choice. The
`n0-session` wrapper forwards arguments, loads the shared environment, assigns
Wayland desktop identity, and starts one D-Bus session bus unless one is inherited.
Either compositor starts `dinit-session` after Wayland is ready; its `dbus-env`
service publishes the real display and desktop identity for portal activation.
Changes to greetd, environment and portal selection take effect at the next login.

Detection uses VM CPU/DMI evidence, battery devices or portable chassis types,
and actual backlight devices. VM detection takes priority and disables physical
laptop services. Optional settings in your local chezmoi configuration require
no migration on existing machines:

```toml
[data.machine]
vm_guest = "auto"  # auto, on, off
laptop = "auto"    # auto, on, off (physical machines only)
backlight = "auto" # auto, on, off (physical machines only)
zram = true       # false leaves existing swap and configuration untouched
```

NetworkManager owns networking; standalone dhcpcd, wpa_supplicant and iwd runit
services are disabled. NetworkManager may still launch its own wireless backend.
Chronyd owns time sync. D-Bus and socklog/nanoklogd remain enabled. Required
services must start successfully; healthy services stay running. Elogind owns
lid and power-button events, with its normal suspend/docked-lid policy; acpid is
stopped to avoid competing handlers, as described in the
[Void handbook](https://docs.voidlinux.org/config/power-management.html).
Physical laptops use packaged TLP defaults. Backlight persistence runs only on
selected machines. Noctalia provides locking and has lock-before-suspend enabled;
verify lid-triggered locking before accepting a laptop migration.

Zram uses zstd, 50% of memory, a maximum of 8192 MiB, and priority 32767. Disk
swap is retained. Applying changes never restarts active zram; new settings need
a reboot. CPU firmware is required on physical Intel (`intel-ucode`) and AMD
(`linux-firmware-amd`) systems. VM microcode belongs to the host.

The POSIX loader at `~/.config/n0-dots/environment.sh` is shared by the system
profile hook, Zsh initialization and graphical wrapper. It sources trusted,
readable `$XDG_CONFIG_HOME/environment.d/*.conf` in lexical order, exports
assignments and preserves the shell's automatic-export state. Repeated loading
deduplicates PATH, XDG data and cursor paths, retaining Nix and Flatpak entries.
Qt uses `QT_QPA_PLATFORMTHEME=gtk3`. Local environment changes belong in a later
unmanaged file such as `environment.d/zz-local.conf`.
Elogind/PAM owns `XDG_RUNTIME_DIR`; shells never create or substitute it. The
wrapper requires a directory owned by the user with mode 0700.

Shared compositor settings use preferred display modes and automatic placement.
Optional unmanaged `~/.config/umbriel/outputs.local.toml` and
`~/.config/niri/outputs.local.kdl` load after generated theme settings. Niri's
theme include is optional before first generation. Machines needing a cursor
workaround can set `WLR_NO_HARDWARE_CURSORS=1` in their local environment file;
Umbriel also offers `hardware_cursor = false` under `[input.cursor]` in a local
included TOML file. Noctalia uses default login-box placement on detected outputs.

Umbriel's portal override selects Umbriel for ScreenCast/Screenshot, GTK for
file dialogs, and gnome-keyring for secrets; Niri retains GNOME/GTK selection.
The signed `xdg-desktop-portal-umbriel` package with GTK4 share picker must be
published through `n0_void-repo`. Bootstrap requires it when repository metadata
advertises it; until then it reports the missing prerequisite. There is no
source-build fallback. Run `n0-portal-check` after installation to inspect backend
interfaces, activation files and executable paths. Portals activate on the session
bus; apply does not supervise or kill portal processes. Browser screen sharing
and file-dialog acceptance remain pending until the package and fresh login.
See the [backend's supported interfaces](https://github.com/noctalia-dev/xdg-desktop-portal-umbriel).

## Migration and acceptance

Run `python3 tests/test_portable.py` from this repository for isolated checks.
Review `chezmoi apply --dry-run --verbose` before applying. A dry-run with
`--force` can render conflicts without a TTY; review those conflicts before any
real apply. Keep a working TTY available. Back up `/etc/greetd/config.toml`,
`/etc/profile.d/xdg-*.sh`, `/etc/sv/zramen/conf` and NetworkManager configuration
before migration, and record `/var/service` symlinks. Changed greetd/profile/zram
files preserve a `.bak` on first migration. Existing NetworkManager DNS changes
wait for the next service start rather than interrupting a healthy connection.
Bootstrap order is repositories, packages, backlight/logging/system fixes,
dotfiles, greetd, services, XDG profile setup, then zram and optional tools.
Existing Btrfs layouts and snapshot/recovery automation are separate from this
reproducible dotfiles setup.

Useful diagnostics:

```sh
sv status /var/service/{NetworkManager,dbus,chronyd,tlp,backlight,zramen}
nmcli general status; nmcli device status
chronyc tracking; chronyc sources
loginctl session-status; loginctl list-inhibitors
stat -c '%U %a %n' "$XDG_RUNTIME_DIR"
dinitctl list; dinitctl status dbus-env
n0-portal-check
xbps-query -f xdg-desktop-portal-umbriel
swapon --show; zramctl
n0-microcode-check
sudo lsinitrd "/boot/initramfs-$(uname -r).img"
```

On the inspected Intel i5-6200U, signature `0x406e3`, platform flags `0xc0`,
installed firmware and running CPU both report revision `0xf0`. Dracut's Intel
and AMD drop-ins enable early microcode. Booted initramfs payload inspection
still requires privileges. The kernel's `Vulnerable: No microcode` GDS status
means missing GDS mitigation, not proof that microcode failed to load; see the
[kernel documentation](https://www.kernel.org/doc/html/latest/admin-guide/hw-vuln/gather_data_sampling.html).
Only if inspection finds a missing/stale early payload, rebuild the affected
installed kernel with `sudo xbps-reconfigure -f linux<version>` and verify after
reboot. Never reload microcode live or automatically change AVX/mitigation
settings. A rebuild alone is not expected to remove the GDS warning.

Rollout requires a clean 4 GB/two-core Void VM, both compositor logins, networking,
time sync, audio, user directories, dialogs and screen sharing. On physical
laptops also verify lid closure, suspend/resume, AC changes, lock-before-sleep,
brightness persistence, external displays and docked operation. Check mixed
modes/scaling and a usable lock-screen password box. Repeat apply for idempotence,
and verify service selection, zram and microcode after reboot. Track unavailable
hardware and privileged checks as pending in `IMPLEMENTATION_PLAN.md`.
