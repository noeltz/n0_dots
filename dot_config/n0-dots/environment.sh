# Shared loading mechanism for the trusted shell assignments in environment.d.
# Keep environment settings in the .conf files, not in this loader.
_n0_load_environment() {
  case $- in *a*) _n0_export=true;; *) _n0_export=false;; esac
  # Native Zsh rejects unmatched globs. Keep POSIX behavior local to this call.
  if [ -n "${ZSH_VERSION:-}" ]; then emulate -L sh; fi
  set -a
  XDG_CONFIG_HOME=${XDG_CONFIG_HOME:-$HOME/.config}
  for _n0_file in "$XDG_CONFIG_HOME"/environment.d/*.conf; do
    [ ! -r "$_n0_file" ] || . "$_n0_file"
  done
  # Deduplicate colon lists without word splitting; first occurrence wins.
  _n0_dedup() (
    _n0_rest=$1 _n0_result=
    while :; do
      _n0_part=${_n0_rest%%:*}
      case :$_n0_result: in *:"$_n0_part":*) ;; *)
        if [ -n "$_n0_part" ]; then _n0_result=${_n0_result:+$_n0_result:}$_n0_part; fi;;
      esac
      case $_n0_rest in *:*) _n0_rest=${_n0_rest#*:};; *) break;; esac
    done
    printf '%s' "$_n0_result"
  )
  if [ "${PATH+x}" ]; then PATH=$(_n0_dedup "$PATH"); export PATH; fi
  if [ "${XDG_DATA_DIRS+x}" ]; then XDG_DATA_DIRS=$(_n0_dedup "$XDG_DATA_DIRS"); export XDG_DATA_DIRS; fi
  if [ "${XCURSOR_PATH+x}" ]; then XCURSOR_PATH=$(_n0_dedup "$XCURSOR_PATH"); export XCURSOR_PATH; fi
  [ "$_n0_export" = true ] || set +a
  unset _n0_export _n0_file
  unset -f _n0_dedup
}
_n0_load_environment
unset -f _n0_load_environment
