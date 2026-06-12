#!/usr/bin/env zsh

# Only load Starship in graphical sessions
if command -v starship &>/dev/null; then
    if [[ -n "$DISPLAY" ]] || [[ "$XDG_SESSION_TYPE" == "wayland" ]]; then
    eval "$(starship init zsh --print-full-init)"
    export STARSHIP_CACHE=$XDG_CACHE_HOME/starship
    export STARSHIP_CONFIG=$XDG_CONFIG_HOME/starship/starship.toml
    fi
fi
