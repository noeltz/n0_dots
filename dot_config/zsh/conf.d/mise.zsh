# Mise (Environment manager for multiple languages)
if [[ -x "$(command -v mise)" ]]; then
  autoload -Uz _mise
  _mise() {
    unfunction _mise
    eval "$(mise activate zsh)"
    mise "$@"
  }
fi
