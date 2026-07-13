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

A declarative, Void-Linux-only desktop setup managed with [chezmoi](https://chezmoi.io): Niri (Wayland) with the Noctalia shell, a dinit-supervised user session, Nix packages alongside XBPS, and libvirt virtualization.

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
| **Window Manager** | Niri (Wayland) with Noctalia theme |
| **Display Manager** | greetd + tuigreet (vt=7, `_greeter` user) |
| **Session Supervision** | User **dinit** instance spawned by niri, supervising pipewire, wireplumber, pipewire-pulse and noctalia — auto-restart, dependency ordering, per-service `dinitctl restart <name>` |
| **System Services** | runit services declaratively enabled/disabled via `services.toml` |
| **Logging** | socklog per-facility system logging (runit) |
| **Virtualization** | QEMU/KVM + libvirt host (virt-manager, virt-viewer, vsv; user added to `kvm`/`libvirt` groups) |
| **Backlight** | Brightness saved on change and restored across reboots (runit + inotify) |
| **Terminal** | Ghostty with shell integration |
| **Fonts** | Maple Mono Nerd Font, JetBrains Mono, Cascadia Code, Inter, Roboto, Noto Emoji |
| **Icons** | Papirus icon theme, Tabler icons |
| **GTK** | adw-gtk3-dark theme, Bibata cursor, dark color scheme |
| **Browser** | Helium (Chromium-based) with Widevine DRM |
| **Editor** | VSCodium with matugen dynamic theme |
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

- **System services — runit** (Void's init). Enabled via `services.toml` (`dbus`, `libvirtd`, `virtlockd`, `virtlogd`, `backlight`, …). Manage with `vsv` or `sv`.
- **User session services — dinit**. niri spawns a user dinit instance (`~/.local/bin/dinit-session`) pointed at `~/.config/dinit.d/`, which supervises pipewire, wireplumber, pipewire-pulse, noctalia and the `dbus-env` one-shot. Each is started explicitly so it is independently restartable: `dinitctl restart noctalia`. On niri exit, dinit gets SIGTERM and stops all session services.

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
| after | `11-xdg-autostart` | Disable unwanted XDG autostart entries |
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
