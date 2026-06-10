<p align="center">
  <img src="assets/n0_dots-logo.svg" alt="n0_dots" width="400">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Arch-7C3AED?style=flat&logo=archlinux&logoColor=white&labelColor=1a1b26" alt="Arch">
  <img src="https://img.shields.io/badge/Niri-7C3AED?style=flat&logoColor=white&labelColor=1a1b26" alt="Niri">
  <img src="https://img.shields.io/badge/Noctalia_v5-A78BFA?style=flat&logoColor=white&labelColor=1a1b26" alt="Noctalia v5">
  <img src="https://img.shields.io/badge/Zsh-7C3AED?style=flat&logo=gnubash&logoColor=white&labelColor=1a1b26" alt="Zsh">
  <img src="https://img.shields.io/badge/Chezmoi-565f89?style=flat&logoColor=white&labelColor=1a1b26" alt="Chezmoi">
</p>

<br>

<p align="center">
  <img src="https://img.shields.io/badge/Quick_Start-7C3AED?style=for-the-badge" alt="Quick Start">
</p>

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

<br>

<p align="center">
  <img src="https://img.shields.io/badge/Daily_Operations-7C3AED?style=for-the-badge" alt="Daily Operations">
</p>

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

<br>

<p align="center">
  <img src="https://img.shields.io/badge/License-565f89?style=for-the-badge" alt="License">
</p>

GNU General Public License v3.0 — see <a href="LICENSE">LICENSE</a>.

<br>

<p align="center">
  <img src="https://img.shields.io/badge/--1a1b26?style=flat" alt="">
</p>
