# n0_dots - Chezmoi Dotfiles

A chezmoi-managed dotfiles repository for Arch Linux systems featuring Niri Window Manager and Noctalia Shell

![Niri](https://img.shields.io/badge/Wayland-Niri-0078D7?logo=linux&logoColor=white)
![Shell](https://img.shields.io/badge/Shell-Zsh-81A1C1?logo=gnu-bash&logoColor=white)

## Features

- **Niri** - Scrollable-tiling Wayland compositor configuration
- **Zsh** - Shell configuration with sheldon plugin manager
- **Noctalia** - Integrated styling system
- **XDG compliant** - Follows XDG Base Directory specification

## Quick Start

### Install on Arch Linux

```bash
# Install chezmoi
sudo pacman -S chezmoi

# Initialize from this repository
chezmoi init --apply https://github.com/noeltz/n0_dots.git

# Or initialize without applying, then review
chezmoi init https://github.com/noeltz/n0_dots.git
chezmoi edit ~/.config/nvim/lua/plugins/example.lua
chezmoi apply
```

---

## Usage

### View Status

```bash
# See what files differ from the repository
chezmoi status

# See what would be changed (dry run)
chezmoi diff
```

### Apply Updates from Repository

```bash
# Pull latest changes and apply
chezmoi pull
chezmoi apply
```

### Contribute Changes Back

```bash
# Make a change to a dotfile
chezmoi edit ~/.zshrc

# Save and quit to apply the change

# Push changes back to the repository
chezmoi re-add ~/.zshrc
chezmoi source push
```

### Fork & Customize

1. Fork this repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/n0_dots.git`
3. Make customizations to files
4. Push to your fork: `git push origin main`
5. On your machines: `chezmoi init --apply https://github.com/YOUR_USERNAME/n0_dots.git`

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
| `run_onchange_after_80_wallpapers.sh` | When changed | Download wallpapers |
| `run_onchange_after_91-helium-browser.sh` | When changed | Configure Helium browser DRM |

---

## Directory Structure

```
n0_dots/
├── .chezmoiscripts/         # Installation and configuration scripts
│   ├── lib/                 # Shared library functions
│   │   ├── .lib-common.sh   # Core utilities (log, confirm, die)
│   │   ├── .lib-package_manager.sh
│   │   ├── .lib-chaotic_aur.sh
│   │   └── .lib-aur_helper.sh
│   └── run_once_*.sh*       # Installation hooks
├── .chezmoidata/            # Configuration data files
│   └── packages.toml          # Arch package lists
├── dot_config/              # ~/.config files
│   ├── niri/                # Niri compositor config
│   ├── nvim/                # Neovim configuration
│   ├── zsh/                 # Zsh configuration
│   └── matugen/             # Matugen templates
├── dot_zshenv               # ~/.zshenv
├── private_dot_local/       # ~/.local files (scripts)
└── Pictures/                # Wallpaper assets
```

---

## Useful Commands

```bash
# Edit dotfile source (preserves template syntax)
chezmoi edit ~/.config/niri/config.kdl

# List all managed files
chezmoi list

# Remove a dotfile from management
chezmoi remove ~/.config/nvim/init.lua

# Forget local changes (reset to repository state)
chezmoi forget ~/.zshrc

# Add untracked file
chezmoi add ~/.config/new-config/file.conf
```

---

## Template Variables

On first initialization, chezmoi prompts for AUR helper selection:

```
Which AUR helper would you like to use:
1. paru
2. yay
[Default: paru]
```

---

## License

MIT License - See [LICENSE](LICENSE) for details.
