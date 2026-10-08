# Portable Void desktop setup: dynamic session selection

Implementation and rollout are separate. Evidence recorded 2026-10-08.

User correction: greetd must remain compositor-independent. The original planned
hardcoded Umbriel default and custom session wrapper are superseded. Tuigreet
selects installed desktop entries and wraps them with `dbus-run-session --`;
greetd's normal profile loading supplies the shared environment. Adding a
compositor never requires adding a case to a shared script.
The user has published `xdg-desktop-portal-umbriel` through `n0_void-repo`.
It is declared and required by bootstrap. Installation, registration/activation and
share-picker executable validation passed after update/reboot. End-to-end browser
sharing, picker interaction and alternative-session acceptance remain pending.
Snapshot/recovery automation and virtualization-host restructuring are excluded.

## Summary

- [x] Inspect bootstrap, services, sessions and upstream guidance — read existing scripts; checked Void power guidance and Umbriel portal interfaces/build installation paths.
- [x] Dynamic session selection — no default compositor command; installed desktop entries and remembered selector determine the session.
- [x] Automatic detection with local overrides — isolated tests and this laptop (`false true true` for VM/laptop/backlight).
- [x] Leave snapshots/recovery to separate work — no snapshot changes.
- [x] Running CPU matches installed firmware revision — Intel signature `0x406e3`, flags `0xc0`, both revisions `0xf0`.
- [x] Implement system services/hardware — rendered scripts and mocked service checks pass.
- [x] Shared environment/dynamic sessions — sh/Bash/Zsh and generic session launch checks pass.
- [x] Compositor-specific portal configuration — overrides implemented; ScreenCast spelling fixed; installed-interface validator supplied.
- [x] Portable display/lock defaults — both compositor validators pass without theme/local files; Virtual-1 widgets removed.
- [ ] Complete microcode diagnostics — read-only CPU/firmware/dracut/mitigation evidence complete; privileged booted-initramfs inspection pending.
- [x] README and automated checks — nine isolated regression groups pass.
- [ ] Local migration and hardware acceptance — sudo requires interactive authentication; fresh-login/reboot/VM/physical checks pending.

## 1. Services and hardware

- [x] Reusable VM, laptop, backlight and CPU-vendor helpers — synthetic Intel/AMD, chassis-only laptop, desktop, QEMU and override cases pass. Empty `/sys/hypervisor` is not VM evidence.
- [x] Optional machine `vm_guest`, `laptop`, `backlight` auto/on/off and boolean `zram` default true — templates render with absent data; invalid values fail.
- [x] Render overrides and helper hashes; hash actual `.chezmoi.configFile` — all scripts render and Bash syntax passes.
- [x] Disable/stop acpid, preserve elogind policy — service declaration; no logind overrides or added event daemons.
- [x] Keep Noctalia locking and lock-before-suspend configured — idle lock retained, lock_before_suspend=true retained.
- [x] Verify Noctalia lock-before-sleep registration — post-reboot elogind ListInhibitors reports noctalia, UID 1000, "Lock before sleep", delay mode. Physical lid/suspend timing acceptance remains pending.
- [x] TLP only on physical laptops with packaged defaults — detection and template implementation verified.
- [x] Backlight only when selected; unnecessary service disabled — shared selection and bounded device wait implemented.
- [x] Declare chrony/tlp/zramen and enable NetworkManager/chronyd/D-Bus/logging — TOML parses and templates render.
- [x] Disable standalone dhcpcd/wpa_supplicant/iwd and competing time daemons — service declarations inspected.
- [x] Start enabled-but-stopped required services and verify state — mocked healthy, stopped, missing and failed-start checks pass; real delayed-supervisor regression passes after fixing runsvdir discovery race; healthy services never restarted.
- [x] Retain existing healthy NetworkManager/D-Bus — no migration restart, DNS drop-in waits for future start.
- [x] Zram zstd/50%/8192 MiB/32767; retain disk swap — mocked inactive/active/disabled provisioning checks pass; activation guard skips zramen with active swap.
- [x] Require selected essentials; retain optional package failure handling — selected firmware/TLP/backlight/zram prerequisites checked explicitly; optional desktop package handling unchanged.

## 2. Environment and sessions

- [x] POSIX sourceable loader, lexical trusted assignments, export-state restoration — sh/Bash/Zsh tests pass with export on/off and absent/empty environment directories; Zsh options restored.
- [x] Keep settings in environment.d — PATH/Flatpak choices moved from loader into 05-path.conf; late local PATH/theme overrides and custom XDG_DATA_HOME verified.
- [x] Restore lightweight Zsh startup — native persistent PATH deduplication and history kept in .zshenv; root .zshenv explicitly delegates to relocated file; full loader runs only via profile/.zshrc, not for every child script.
- [x] Profile/Zsh share the generic loader; greetd uses normal profile loading — duplicate scanning/XDG PATH hook retired with backup.
- [x] Idempotent PATH/data/cursor paths, Nix/Flatpak, spaces/custom XDG/empty home — repeated-loading tests pass.
- [x] Runtime directory belongs to PAM/elogind — Zsh creation/fallback removed; runtime diagnostics documented. Custom wrapper validation removed with the wrapper.
- [x] Shared Qt gtk3 choice — environment.d updated; Qt6-specific and competing compositor assignments removed.
- [x] Remove n0-session and compositor dispatch — tuigreet wraps arbitrary session commands directly with dbus-run-session; no custom bus-reuse policy.
- [x] Tuigreet discovery/remembered session/argument boundaries — rendered config and generic launch tests; identity belongs to desktop entries/compositors.
- [x] Keep post-Wayland dinit and D-Bus activation publication — both compositor startup configs retain dinit-session, dbus-env retained.

## 3. Portals, displays, locking

- [x] Declare and require supplied XBPS portal package — packages_void.toml updated; availability gate removed; no source fallback.
- [x] Install supplied Umbriel portal package — xdg-desktop-portal-umbriel-20261008142455_1 installed from n0_void-repo; current package script completed successfully.
- [x] Umbriel default=umbriel;gtk, ScreenCast/Screenshot Umbriel, GTK dialogs, keyring secrets — config implemented.
- [x] Retain Niri GNOME/GTK and correct ScreenCast case — config implemented.
- [x] Preserve session-bus portal activation; no portal supervision/kill/restart — inspected scripts/dinit config.
- [x] Validate installed Umbriel registration/activation/share picker/executable paths — n0-portal-check passes; activated backend owns its bus name; compiled /usr/libexec/umbriel-share-picker path is correct; both binaries have no missing shared libraries.
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
- [x] README dynamic sessions/editor/terminal/service ownership/overrides/environment/portals/displays/script order/migration/troubleshooting/reboots/Btrfs separation updated.

## 5. Verification and rollout

- [x] All chezmoi script templates render, rendered Bash syntax and TOML parsing — tests/test_portable.py.
- [x] POSIX and Zsh environment execution — repeated-source tests across sh/Bash/Zsh; real Zsh noninteractive, interactive, login and interactive-login startup with and without inherited ZDOTDIR; child scripts inherit exports without reloading configs.
- [x] Hardware detection and explicit overrides — chassis-only laptop, empty hypervisor directory, desktop, physical Intel/AMD, QEMU guest, invalid settings.
- [x] Loader empty home/custom XDG/space-containing paths/Nix/Flatpak/export state — isolated checks.
- [x] Generic session commands and profile environment — arbitrary session stubs preserve spaced arguments and supplied identity; no desktop launched.
- [x] Service healthy/stopped/missing/failed starts — mocked commands, no real services changed.
- [x] Zram active changes/inactive activation/disabled preservation — mocked checks; guarded service run also tested with active swap.
- [x] Fresh compositor configs without generated/local files — umbriel validate and niri validate pass.
- [x] All installed portal overrides match registration interfaces — n0-portal-check now passes for Umbriel and Niri configurations. Niri end-to-end session acceptance is still pending.
- [x] Complete chezmoi dry-run generated and reviewed — `chezmoi -S "$PWD" apply --dry-run --force --verbose` succeeds; output contains unrelated existing destination conflicts (Kitty/theme), so no broad apply performed.
- [x] Migration backups prepared in scripts — first-run .bak for greetd/profile/zram; README includes NetworkManager and service-link backup instructions.
- [x] Complete privileged migration — recovery recheck confirms current greetd/service/profile/zram scripts completed at 13:23 UTC; shared profile hook and guarded zram run script installed; obsolete xdg-path.sh removed; fresh graphical environment correct.
- [ ] Clean 4 GB/two-core Void VM bootstrap: network/time/audio/user directories/Umbriel/Niri — no clean VM supplied.
- [ ] File dialogs/browser screen sharing in both sessions — package and fresh login pending.
- [ ] Laptop lid/suspend/resume/AC/lock-before-sleep/brightness — requires physical acceptance.
- [ ] External display connect/disconnect/docked behavior/mixed mode/scaling/lock input — hardware/session acceptance pending.
- [ ] Repeat real apply for idempotence; reboot services/zram/microcode — pending migration/reboot.

Implementation of code and isolated checks is complete. Rollout is incomplete.
Microcode diagnostics and portal runtime checks retain the limitations above.


## Post-reboot audit — 2026-10-08, current laptop

- [x] Latest user dotfiles deployed (ecae180); dynamic greetd configuration matches.
- [x] Active elogind Wayland session on tty7; runtime directory belongs to noeltz, mode 0700.
- [x] Exactly one main graphical session bus (dbus-run-session -> dbus-daemon and Umbriel), plus the expected separate accessibility bus. System bus responds.
- [x] Dinit pipewire, wireplumber, pipewire-pulse, noctalia and dbus-env all STARTED. Audio devices and default sink/source available.
- [x] D-Bus-activated portals receive the same session-bus address, wayland-0 and umbriel desktop identity. Activation publication works.
- [ ] Complete graphical environment exports: compositor/dinit/portal processes have unset EDITOR, XCURSOR_PATH, XDG_CONFIG_HOME/DATA_HOME/STATE_HOME and duplicated Flatpak entries. Current /etc/profile.d/xdg-environment.sh is the old non-exporting loop; obsolete xdg-path.sh remains. Directly sourcing deployed shared loader produces correct exports and deduplicated paths.
- [x] NetworkManager reports connected/full connectivity; chrony synchronized with normal leap state. TLP enabled on AC using packaged defaults. Backlight saved/current brightness both 716; device max 7142.
- [x] Expected required service links present; acpid/dhcpcd/standalone wpa_supplicant/iwd/time competitors absent. NetworkManager's D-Bus wpa_supplicant backend is running normally. Root-only sv supervision status is still uninspected.
- [x] Noctalia registers elogind delay inhibitor "Lock before sleep". Lid/suspend timing still needs a physical test.
- [x] Zram runtime uses zstd, 7.7 GiB (50% of 16204224 KiB RAM), priority 32767. Only zram swap is active; no disk swap was removed by this work. Managed activation-guard run script has not yet been installed.
- [x] Deployed Umbriel/Niri configs validate. Internal output uses preferred 1920x1080 at 60.020 Hz. Standard XDG user directories exist.
- [x] GTK FileChooser interface responds (version 4). Screenshot interface responds (version 2), actual capture not tested.
- [ ] Umbriel ScreenCast unavailable (frontend version 0); required backend registration/share picker/package still missing, including repository query.
- [x] Post-reboot Intel running and installed firmware remain 0xf0; dracut drop-ins enable early microcode. Privileged booted-initramfs inspection remains pending.
- [x] Reproduced and fixed immediate sv failure before new service supervision exists. A new nanoklogd link plus absent completed service-script state is consistent with this interrupting the last apply; exact user error output was not available.
- [ ] Run the corrected update/apply from a terminal with sudo, then log out/in and recheck graphical process environments and script state. No live services/session were restarted by this audit.


## Recovery recheck — 2026-10-08, 15:25 CEST

- [x] User updated to c5c2fd9 and rebooted. Current greetd/services/XDG/zram script hashes all have successful completed state.
- [x] Shared system profile hook installed; obsolete xdg-path.sh absent; guarded zram run installed.
- [x] Umbriel, dinit, Noctalia and D-Bus-activated portals export configured XDG config/data/state directories, Micro/Zed editor settings, gtk3 Qt theme and cursor paths. Flatpak entries appear once.
- [x] One main session bus; child services and portals share it and receive wayland-0/umbriel. Runtime directory ownership/mode correct. System bus and elogind inhibitor query respond.
- [x] Dinit audio/shell services STARTED; audio sink/source available; NetworkManager full connectivity; chrony synchronized; TLP enabled with packaged defaults; brightness saved/current both 716; logging processes running.
- [x] Competing acpid/dhcpcd/standalone wpa_supplicant/iwd/time-daemon links absent. NetworkManager's D-Bus wpa_supplicant backend remains expected.
- [x] Rebooted zram still zstd, 7.7 GiB, priority 32767. Running CPU revision still 0xf0.
- [x] Repeat dry-run has zero pending setup scripts. Three destination differences remain: Kitty's Noctalia theme include, browser MIME defaults, and Umbriel's optional include order (local output file before generated theme). Current local output file is absent; future local overrides should be last. Local differences were retained.
- [ ] Umbriel portal package/share picker still missing; screen-sharing acceptance remains blocked by the external prerequisite.
- [ ] Root-only current sv status and booted-initramfs payload inspection still need terminal sudo. Physical lid/suspend timing, external displays, alternative-session acceptance and clean VM tests remain pending.


## Umbriel portal package recheck — 2026-10-08, 16:53 CEST

- [x] xdg-desktop-portal-umbriel-20261008142455_1 installed from https://github.com/noeltz/n0_void-repo/releases/latest/download; package script completed at 14:50 UTC; user rebooted afterward.
- [x] Package supplies portal registration, D-Bus activation and /usr/libexec backend/share-picker executables. No missing shared-library dependencies. Compiled chooser path is /usr/libexec/umbriel-share-picker; no local chooser override exists.
- [x] n0-portal-check passes. Umbriel backend owns org.freedesktop.impl.portal.desktop.umbriel; owner resolves to the running backend PID.
- [x] Frontend ScreenCast version now 4 (previously 0), source flags 3 and cursor-mode flags 7. Screenshot version 2; GTK FileChooser version 4. Protocol presence/capabilities checked without opening capture or dialog prompts.
- [x] Backend/frontend/GTK portal share the graphical session bus, wayland-0, umbriel identity and correct exported environment. Runtime directory ownership/mode correct. Dinit services, networking, chrony and zram remain healthy.
- [ ] Actual browser capture, source-picker interaction, screenshot result, file-dialog interaction and Niri-session acceptance remain pending; installation/API checks do not establish successful end-to-end capture.
