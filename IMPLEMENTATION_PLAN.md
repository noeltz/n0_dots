# Portable Void desktop setup: Umbriel default, Niri alternative

Implementation and rollout are separate. Evidence recorded 2026-10-08.
External prerequisite: publish a signed `xdg-desktop-portal-umbriel` package with
GTK4 share picker through `n0_void-repo`. Package creation is outside this work.
Snapshot/recovery automation and virtualization-host restructuring are excluded.

## Summary

- [x] Inspect bootstrap, services, sessions and upstream guidance — read existing scripts; checked Void power guidance and Umbriel portal interfaces/build installation paths.
- [x] Confirm Umbriel preferred, Niri alternative — default tuigreet command and remembered selector retained.
- [x] Automatic detection with local overrides — isolated tests and this laptop (`false true true` for VM/laptop/backlight).
- [x] Leave snapshots/recovery to separate work — no snapshot changes.
- [x] Running CPU matches installed firmware revision — Intel signature `0x406e3`, flags `0xc0`, both revisions `0xf0`.
- [x] Implement system services/hardware — rendered scripts and mocked service checks pass.
- [x] Shared environment/preferred session — sh/Bash/Zsh and wrapper stub checks pass.
- [x] Compositor-specific portal configuration — overrides implemented; ScreenCast spelling fixed; installed-interface validator supplied.
- [x] Portable display/lock defaults — both compositor validators pass without theme/local files; Virtual-1 widgets removed.
- [ ] Complete microcode diagnostics — read-only CPU/firmware/dracut/mitigation evidence complete; privileged booted-initramfs inspection pending.
- [x] README and automated checks — six isolated regression groups pass.
- [ ] Local migration and hardware acceptance — sudo requires interactive authentication; fresh-login/reboot/VM/physical checks pending.

## 1. Services and hardware

- [x] Reusable VM, laptop, backlight and CPU-vendor helpers — synthetic Intel/AMD, chassis-only laptop, desktop, QEMU and override cases pass. Empty `/sys/hypervisor` is not VM evidence.
- [x] Optional machine `vm_guest`, `laptop`, `backlight` auto/on/off and boolean `zram` default true — templates render with absent data; invalid values fail.
- [x] Render overrides and helper hashes; hash actual `.chezmoi.configFile` — all scripts render and Bash syntax passes.
- [x] Disable/stop acpid, preserve elogind policy — service declaration; no logind overrides or added event daemons.
- [x] Keep Noctalia locking and lock-before-suspend configured — idle lock retained, lock_before_suspend=true retained.
- [ ] Verify actual Noctalia lock-before-sleep integration — physical lid and suspend test pending; configuration alone is not proof.
- [x] TLP only on physical laptops with packaged defaults — detection and template implementation verified.
- [x] Backlight only when selected; unnecessary service disabled — shared selection and bounded device wait implemented.
- [x] Declare chrony/tlp/zramen and enable NetworkManager/chronyd/D-Bus/logging — TOML parses and templates render.
- [x] Disable standalone dhcpcd/wpa_supplicant/iwd and competing time daemons — service declarations inspected.
- [x] Start enabled-but-stopped required services and verify state — mocked healthy, stopped, missing and failed-start checks pass; healthy services never restarted.
- [x] Retain existing healthy NetworkManager/D-Bus — no migration restart, DNS drop-in waits for future start.
- [x] Zram zstd/50%/8192 MiB/32767; retain disk swap — mocked inactive/active/disabled provisioning checks pass; activation guard skips zramen with active swap.
- [x] Require selected essentials; retain optional package failure handling — selected firmware/TLP/backlight/zram prerequisites checked explicitly; optional desktop package handling unchanged.

## 2. Environment and sessions

- [x] POSIX sourceable loader, lexical trusted assignments, export-state restoration — sh/Bash/Zsh tests pass with export on/off.
- [x] Profile/Zsh/wrapper share loader; retire duplicate scanning/XDG PATH hook — source reviewed, profile migration removes old path hook with backup.
- [x] Idempotent PATH/data/cursor paths, Nix/Flatpak, spaces/custom XDG/empty home — repeated-loading tests pass.
- [x] Runtime directory belongs to PAM/elogind — Zsh creation/fallback removed; wrapper validates owner/mode and missing directory errors.
- [x] Shared Qt gtk3 choice — environment.d updated; Qt6-specific and competing compositor assignments removed.
- [x] n0-session defaults to start-umbriel; inherited bus reused — stub tests preserve spaced arguments and explicit Niri selection.
- [x] Tuigreet default/remembered session/argument boundaries/desktop identity — rendered TOML and wrapper tests; packaged session Exec commands inspected.
- [x] Keep post-Wayland dinit and D-Bus activation publication — both compositor startup configs retain dinit-session, dbus-env retained.

## 3. Portals, displays, locking

- [x] Prepare required XBPS portal installation when repository advertises signed package; no source fallback — bootstrap integration complete.
- [ ] Install supplied Umbriel portal package — unavailable prerequisite remains external.
- [x] Umbriel default=umbriel;gtk, ScreenCast/Screenshot Umbriel, GTK dialogs, keyring secrets — config implemented.
- [x] Retain Niri GNOME/GTK and correct ScreenCast case — config implemented.
- [x] Preserve session-bus portal activation; no portal supervision/kill/restart — inspected scripts/dinit config.
- [ ] Validate installed Umbriel registration/activation/share picker/executable paths — n0-portal-check prepared, missing package prevents completion.
- [x] Remove forced outputs/modes/positions — shared output tables/blocks removed.
- [x] Optional unmanaged local output files load last — ignore entries supplied; native validators pass with absent files.
- [x] Remove shared cursor workaround; document local settings — WLR variable removed and Umbriel hardware cursor enabled.
- [x] Remove Virtual-1 login/clock/grid/wallpaper overrides — TOML parses; normal locking/wallpaper retained.
- [x] Optional Niri generated theme — niri validate passes without noctalia.kdl.

## 4. Microcode and docs

- [x] Vendor-selected physical firmware; guests report host responsibility — detection/package templates and diagnostics implemented.
- [x] Current Intel signature/revision/running/dracut/mitigation inspection — read-only n0-microcode-check reports signature 0x406e3, flags 0xc0, installed/running 0xf0, early_microcode=yes in both firmware drop-ins, GDS warning.
- [ ] Inspect booted initramfs early payload and kernel logs with privileges — `/boot/initramfs-6.18.55_1.img` not readable; sudo -n requires password.
- [ ] AMD equivalence-table/patch matching on physical AMD hardware — diagnostics list firmware; hardware-specific matching pending.
- [x] Correct GDS interpretation documented with kernel reference — missing mitigation, not evidence of unloaded firmware.
- [x] Conditional normal xbps-reconfigure guidance; no live reload or automatic mitigation changes — no rebuild attempted without evidence.
- [ ] Rebuild affected installed initramfs only if privileged inspection finds missing/stale payload — conditional pending, not assumed necessary.
- [x] README preferred session/editor/terminal/service ownership/overrides/environment/portals/displays/script order/migration/troubleshooting/reboots/Btrfs separation updated.

## 5. Verification and rollout

- [x] All chezmoi script templates render, rendered Bash syntax and TOML parsing — tests/test_portable.py.
- [x] POSIX and Zsh environment execution — repeated-source tests across sh/Bash/Zsh.
- [x] Hardware detection and explicit overrides — chassis-only laptop, empty hypervisor directory, desktop, physical Intel/AMD, QEMU guest, invalid settings.
- [x] Loader empty home/custom XDG/space-containing paths/Nix/Flatpak/export state — isolated checks.
- [x] Wrapper default/Niri/arguments/bus reuse/runtime failures — stub checks, no desktop launched.
- [x] Service healthy/stopped/missing/failed starts — mocked commands, no real services changed.
- [x] Zram active changes/inactive activation/disabled preservation — mocked checks; guarded service run also tested with active swap.
- [x] Fresh compositor configs without generated/local files — umbriel validate and niri validate pass.
- [ ] All installed portal overrides match registration interfaces — checker confirms Niri GNOME/GTK/keyring interfaces and activation commands; only Umbriel registration and share picker are missing.
- [x] Complete chezmoi dry-run generated and reviewed — `chezmoi -S "$PWD" apply --dry-run --force --verbose` succeeds; output contains unrelated existing destination conflicts (Kitty/theme), so no broad apply performed.
- [x] Migration backups prepared in scripts — first-run .bak for greetd/profile/zram; README includes NetworkManager and service-link backup instructions.
- [ ] Perform privileged migration with working TTY and next-login greetd changes — pending interactive sudo; system and current desktop not changed.
- [ ] Clean 4 GB/two-core Void VM bootstrap: network/time/audio/user directories/Umbriel/Niri — no clean VM supplied.
- [ ] File dialogs/browser screen sharing in both sessions — package and fresh login pending.
- [ ] Laptop lid/suspend/resume/AC/lock-before-sleep/brightness — requires physical acceptance.
- [ ] External display connect/disconnect/docked behavior/mixed mode/scaling/lock input — hardware/session acceptance pending.
- [ ] Repeat real apply for idempotence; reboot services/zram/microcode — pending migration/reboot.

Implementation of code and isolated checks is complete. Rollout is incomplete.
Microcode diagnostics and portal runtime checks retain the limitations above.
