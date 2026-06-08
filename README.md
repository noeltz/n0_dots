# n0_dots - Chezmoi Dotfiles

A cross-platform dotfiles repository managed by [chezmoi](https://www.chezmoi.io/) for Arch Linux and Fedora systems.

## Features

- **Niri** - Scrollable-tiling Wayland compositor configuration
- **Zsh** - Shell configuration with sheldon plugin manager
- **Neovim** - LazyVim-based configuration
- **Matugen templates** - Color theming templates (for compatibility)
- **Noctalia v5** - Integrated styling system
- **XDG compliant** - Follows XDG Base Directory specification

## Quick Start

### Initial Installation (Fresh Arch Linux)

```bash
# Install chezmoi
sudo pacman -S chezmoi

# Initialize from this repository
chezmoi init --apply https://github.com/noeltz/n0_dots.git

# Or initialize without applying, then review
chezmoi init https://github.com/noeltz/n0_dots.git
chezmoi edit ~/.config/nvim/lua/plugins/example.lua  # Make customizations

# Apply all dotfiles
chezmoi apply
```

### Initial Installation (Fresh Fedora)

```bash
# Install chezmoi
sudo dnf install chezmoi

# Initialize from this repository
chezmoi init --apply https://github.com/noeltz/n0_dots.git
chezmoi apply
```

---

## Daily Usage

### Check Status

```bash
# See what files differ from the repository
chezmoi status

# See what would be changed (dry run)
chezmoi diff
```

### Apply Changes from Repository

```bash
# Pull latest changes and apply
chezmoi pull
chezmoi apply

# Or in one command
chezmoi source pull && chezmoi apply
```

### Push Local Changes to Repository

```bash
# Make a change to a dotfile
chezmoi edit ~/.zshrc

# The file opens in your editor with the source version
# Save and quit to apply the change

# Then push back to the repository
chezmoi re-add ~/.zshrc
chezmoi source push
```

---

## Workflow for Multiple Machines

This repository is designed for synchronization across multiple machines.

### Adding a New Machine

```bash
# On the new machine
chezmoi init https://github.com/noeltz/n0_dots.git
chezmoi apply
```

### Keeping Machines in Sync

```bash
# Before starting work on a machine - get latest
chezmoi pull
chezmoi apply

# After making changes - push them
chezmoi re-add               # Re-add all modified files to source
chezmoi source push          # Push to git repository
```

### Template Variables (One-time Setup)

On first initialization, chezmoi will prompt for AUR helper selection:

```
Which AUR helper would you like to use:
1. paru
2. yay
[Default: paru]
```

---

## Script Hooks

These scripts run automatically during `chezmoi apply`:

| Script | Trigger | Purpose |
|--------|---------|---------|
| `run_once_before_00-install-aur-helper.sh` | First apply | Install AUR helper and configure Chaotic-AUR |
| `run_once_after_04_login_manager.sh` | First apply | Configure Ly display manager |
| `run_once_after_10-systemd-service.sh` | First apply | Add systemd user services |
| `run_once_after_11-fonts_and_icons.sh` | First apply | Download and install fonts/icons |
| `run_once_after_20-gtk-settings.sh` | First apply | Apply GTK settings |
| `run_once_before_99-switch-shell.sh` | First apply | Switch default shell to zsh |
| `run_onchange_after_80_wallpapers.sh` | When wallpapers change | Download wallpapers |
| `run_onchange_after_91-helium-browser.sh` | When browser config changes | Configure Helium browser DRM |

---

## Directory Structure

```
n0_dots/
├── .chezmoicompiled/       # Compiled templates (auto-generated)
├── .chezmoiignore           # Files to ignore
├── .chezmoitemplates/       # Reusable template snippets
├── .chezmoiscripts/         # Installation and configuration scripts
│   ├── lib/                 # Shared library functions
│   │   ├── .lib-common.sh
│   │   ├── .lib-package_manager.sh
│   │   └── ...
│   └── run_once_*.sh*       # Installation hooks
├── .chezmoidata/            # Configuration data files
│   └── packages.toml        # Package lists
├── dot_config/              # ~/.config files
├── dot_zshenv               # ~/.zshenv
├── private_dot_local/       # ~/.local files (scripts, data)
└── Pictures/                # Wallpaper assets
```

---

## Useful Commands

```bash
# Edit dotfile in source (preserves chezmoi template syntax)
chezmoi edit ~/.config/niri/config.kdl

# Edit dotfile destination (no template processing)
chezmoi edit --destination ~/.config/niri/config.kdl

# Remove a dotfile from management
chezmoi remove ~/.config/ some/file

# List all managed files
chezmoi list

# Forget local changes (reset to repository state)
chezmoi forget ~/.zshrc

# Generate a simple bash script
chezmoi edit ~/.local/bin/executable_myscript.sh
```

---

## License

MIT License - See [LICENSE](LICENSE) for details.