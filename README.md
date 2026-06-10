<p align="center">
  <strong style="font-size: 2.5em; font-family: system-ui, -apple-system, sans-serif; letter-spacing: -1px;">
    n<span style="display: inline-block; background: linear-gradient(135deg, #7C3AED, #A78BFA); color: white; padding: 0 8px; border-radius: 6px; font-weight: 900;">0_d</span>ots
  </strong>
  <br>
  <span style="color: #6B7280; font-size: 0.85em;">chezmoi · arch · niri · noctalia · zsh</span>
</p>

![Niri](https://img.shields.io/badge/Wayland-Niri-0078D7?logo=linux&logoColor=white)
![Shell](https://img.shields.io/badge/Shell-Zsh-81A1C1?logo=gnu-bash&logoColor=white)
![Noctalia](https://img.shields.io/badge/Shell-Noctalia%20v5-7C3AED?logo=shell&logoColor=white)

## Quick Start

```bash
# One-liner — installs chezmoi, clones repo, and applies dotfiles
sh -c "$(curl -fsLS https://get.chezmoi.io)" -- init --apply https://github.com/noeltz/n0_dots.git
```

Or step by step:

```bash
# Install chezmoi
sudo pacman -S chezmoi

# Clone and apply
chezmoi init --apply https://github.com/noeltz/n0_dots.git
```

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

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).
