#######################################
# SHELDON (PLUGIN MANAGER)
#######################################
export ZSH_CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/oh-my-zsh"
mkdir -p "$ZSH_CACHE_DIR/completions"

autoload -Uz compinit
if [[ -n ${ZDOTDIR:-$HOME}/.zcompdump(#qN.mH+24) ]]; then
    compinit
else
    compinit -C
fi

eval "$(sheldon source)"

# Plugin-specific settings
ZSH_AUTOSUGGEST_STRATEGY=(history completion)
