# n0_dots

Chezmoi-managed dotfiles for Arch Linux with Niri Wayland compositor and Noctalia v5 shell.

![Niri](https://img.shields.io/badge/Wayland-Niri-0078D7?logo=linux&logoColor=white)
![Shell](https://img.shields.io/badge/Shell-Zsh-81A1C1?logo=gnu-bash&logoColor=white)
![Noctalia](https://img.shields.io/badge/Shell-Noctalia%20v5-7C3AED?logo=shell&logoColor=white)

## Quick Start

```bash
# One-liner — installs chezmoi, clones repo, and applies dotfiles
sh -c "$(curl -fsLS https://get.chezmoi.io)" -- init --apply noeltz
```

Or step by step:

```bash
# Install chezmoi
sudo pacman -S chezmoi

# Clone and apply
chezmoi init --apply noeltz
```

On first init you will be prompted to choose an AUR helper (paru or yay).

## Daily Operations

```bash
# Pull latest changes from repo and apply them
chezmoi update

# See what would change (dry run)
chezmoi diff

# Apply pending changes
chezmoi apply

# Check which files have diverged from source
chezmoi status

# Edit a managed dotfile (includes --watch to auto-apply on save)
chezmoi edit ~/.config/niri/config.kdl

# Add an untracked file to management
chezmoi add ~/.config/some-app/config.toml

# Update source state after manual editing
chezmoi re-add ~/.zshrc

# List all managed files
chezmoi list

# Resolve merge conflicts after update
chezmoi merge ~/.config/niri/config.kdl

# Forget a file (stop managing it locally)
chezmoi forget ~/.local/bin/old-script.sh
```

## Template Variables

On `chezmoi init` you will be prompted to select an AUR helper:

```
Which AUR helper would you like to use:
1. paru
2. yay
[Default: paru]
```

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).
