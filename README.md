<p align="center">
  <img src="assets/n0_dots-logo.svg" alt="n0_dots" width="400">
</p>

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
