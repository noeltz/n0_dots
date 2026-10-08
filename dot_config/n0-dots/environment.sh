# POSIX shell environment loader; environment.d contains trusted shell assignments.
case $- in *a*) _n0_export=true;; *) _n0_export=false;; esac
set -a
XDG_CONFIG_HOME=${XDG_CONFIG_HOME:-$HOME/.config}
for _n0_file in "$XDG_CONFIG_HOME"/environment.d/*.conf; do
  [ ! -r "$_n0_file" ] || . "$_n0_file"
done
XDG_BIN_HOME=${XDG_BIN_HOME:-$HOME/.local/bin}
PATH=$XDG_BIN_HOME:${PATH:-/usr/local/bin:/usr/bin:/bin}
XDG_DATA_DIRS=${XDG_DATA_DIRS:-/usr/local/share:/usr/share}:$HOME/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share
# Deduplicate colon lists without word splitting, preserving paths with spaces.
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
PATH=$(_n0_dedup "$PATH")
XDG_DATA_DIRS=$(_n0_dedup "$XDG_DATA_DIRS")
XCURSOR_PATH=$(_n0_dedup "${XCURSOR_PATH:-/usr/share/icons}")
export PATH XDG_DATA_DIRS XCURSOR_PATH
[ "$_n0_export" = true ] || set +a
unset _n0_export _n0_file
unset -f _n0_dedup
