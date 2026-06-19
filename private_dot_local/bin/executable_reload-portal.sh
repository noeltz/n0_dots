#!/usr/bin/env bash

dbus-update-activation-environment --all
if command -v systemctl &>/dev/null; then
  dbus-update-activation-environment --systemd --all
  systemctl --user import-environment QT_QPA_PLATFORMTHEME
fi

pkill -f xdg-desktop-portal
