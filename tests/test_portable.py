"""Isolated portability regression checks; no system services or desktop launched."""
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]

def run(cmd, env=None, check=True):
    return subprocess.run(cmd, text=True, capture_output=True, env=env, check=check)

class Portable(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='n0 tests ')
        self.home = Path(self.temp.name)
        self.env = dict(os.environ, HOME=str(self.home), XDG_CONFIG_HOME=str(self.home / 'custom config'))
        for key in ('XDG_DATA_DIRS', 'XCURSOR_PATH', 'XDG_RUNTIME_DIR', 'DBUS_SESSION_BUS_ADDRESS'):
            self.env.pop(key, None)
    def tearDown(self):
        self.temp.cleanup()
    def hardware(self, extra=':'):
        return run(['bash', '-c', f'source "{ROOT}/.chezmoiscripts/lib/.lib-platform.sh"; {extra}; resolve_machine || exit $?; echo "$IS_VM $IS_LAPTOP $HAS_BACKLIGHT $(detect_cpu_vendor)"'], self.env).stdout.strip()
    def test_hardware(self):
        sys = self.home / 'sys'; proc = self.home / 'proc'
        (sys / 'class/dmi/id').mkdir(parents=True); proc.mkdir()
        self.env.update(N0_SYS_ROOT=str(sys), N0_PROC_ROOT=str(proc))
        (proc/'cpuinfo').write_text('vendor_id : GenuineIntel\n')
        (sys/'hypervisor').mkdir()  # empty directory exists on physical Linux too
        (sys/'class/dmi/id/chassis_type').write_text('10\n')
        self.assertEqual(self.hardware(), 'false true false intel')  # laptop with no battery
        (sys/'class/dmi/id/chassis_type').write_text('3\n')
        self.assertEqual(self.hardware(), 'false false false intel')
        (proc/'cpuinfo').write_text('vendor_id : AuthenticAMD\n')
        self.assertEqual(self.hardware(), 'false false false amd')
        self.assertEqual(self.hardware('MACHINE_LAPTOP=on; MACHINE_BACKLIGHT=on'), 'false true true amd')
        (sys/'class/dmi/id/product_name').write_text('QEMU\n')
        self.assertEqual(self.hardware('MACHINE_LAPTOP=on; MACHINE_BACKLIGHT=on'), 'true false false amd')
        self.assertEqual(self.hardware('MACHINE_VM_GUEST=off; MACHINE_LAPTOP=on'), 'false true false amd')
        result=run(['bash','-c',f'source "{ROOT}/.chezmoiscripts/lib/.lib-platform.sh"; MACHINE_VM_GUEST=invalid; resolve_machine'],self.env,False)
        self.assertEqual(result.returncode,2)
    def test_environment(self):
        conf=Path(self.env['XDG_CONFIG_HOME']); shutil.copytree(ROOT/'dot_config/environment.d',conf/'environment.d')
        self.env['PATH']='/usr/bin:/bin:/nix/var/nix/profiles/default/bin:/usr/bin'
        for shell in ('sh','bash','zsh'):
            for auto in ('set +a','set -a'):
                code=f'{auto}; . "{ROOT}/dot_config/n0-dots/environment.sh"; first="$PATH|$XDG_DATA_DIRS|$XCURSOR_PATH"; . "{ROOT}/dot_config/n0-dots/environment.sh"; [ "$first" = "$PATH|$XDG_DATA_DIRS|$XCURSOR_PATH" ] || exit 7; case $- in *a*) echo on;; *) echo off;; esac; printf "%s\\n" "$PATH" "$XDG_DATA_DIRS" "$QT_QPA_PLATFORMTHEME"'
                result=run([shell,'-c',code],self.env).stdout
                self.assertEqual(result.splitlines()[0], 'on' if auto=='set -a' else 'off')
                self.assertIn('/nix/var/nix/profiles/default/bin',result)
                self.assertIn('.nix-profile/share',result)
                self.assertIn('flatpak/exports/share',result)
                self.assertTrue(result.endswith('gtk3\n'))
        shutil.rmtree(conf)
        run(['sh','-c',f'. "{ROOT}/dot_config/n0-dots/environment.sh"'],self.env)
    def test_session(self):
        # Read the actual generated greetd command and profile hook, then model
        # greetd sourcing the profile before executing a selected desktop entry.
        def render(name):
            return subprocess.run(
                ['chezmoi', '-S', str(ROOT), 'execute-template'],
                input=(ROOT/'.chezmoiscripts'/name).read_text(),
                text=True, capture_output=True, check=True,
            ).stdout
        login = render('run_onchange_after_04_login_manager.sh.tmpl')
        config = tomllib.loads('[terminal]\n' + login.split('[terminal]\n', 1)[1].split('\nEOF', 1)[0])
        command = shlex.split(config['default_session']['command'])
        self.assertNotIn('--cmd', command)
        self.assertIn('--remember-session', command)
        wrapper = shlex.split(command[command.index('--session-wrapper') + 1])
        self.assertEqual(wrapper, ['dbus-run-session', '--'])

        xdg = render('run_onchange_after_11-xdg-autostart.sh.tmpl')
        hook = xdg.split("sudo tee /etc/profile.d/xdg-environment.sh > /dev/null <<'EOF'\n", 1)[1].split('\nEOF', 1)[0]
        profile = self.home/'profile hook.sh'; profile.write_text(hook)
        conf = Path(self.env['XDG_CONFIG_HOME'])
        shutil.copytree(ROOT/'dot_config/environment.d', conf/'environment.d')
        shutil.copytree(ROOT/'dot_config/n0-dots', conf/'n0-dots')
        (conf/'environment.d/zz-session-test.conf').write_text('SESSION_TEST=loaded\n')
        bin = self.home/'bin'; bin.mkdir()
        bus = bin/'dbus-run-session'
        bus.write_text('#!/bin/sh\n[ "$1" = -- ] || exit 2\nshift\nexport DBUS_SESSION_BUS_ADDRESS=stub-session-bus\nexec "$@"\n')
        bus.chmod(0o755)
        self.env['PATH'] = f'{bin}:/usr/bin:/bin'
        for name in ('river', 'mangowc', 'future compositor'):
            session = bin/name
            session.write_text('#!/bin/sh\nprintf "%s\n" "${0##*/}" "$SESSION_TEST" "$XDG_CURRENT_DESKTOP" "$XDG_SESSION_DESKTOP" "$XDG_SESSION_TYPE" "$DBUS_SESSION_BUS_ADDRESS" "$QT_QPA_PLATFORMTHEME" "$@"\n')
            session.chmod(0o755)
            self.env.update(XDG_CURRENT_DESKTOP=name, XDG_SESSION_DESKTOP=name, XDG_SESSION_TYPE='wayland')
            result = run(['sh', '-c', '. "$1"; shift; exec "$@"', 'greetd-profile-test', str(profile), *wrapper, str(session), '--option', 'argument with spaces'], self.env).stdout.splitlines()
            self.assertEqual(result, [name, 'loaded', name, name, 'wayland', 'stub-session-bus', 'gtk3', '--option', 'argument with spaces'])
    def test_runit(self):
        # Redirect service roots into a sandbox, keeping helper logic unchanged.
        source=(ROOT/'.chezmoiscripts/lib/.lib-runit.sh').read_text().replace('/etc/sv',str(self.home/'sv')).replace('/var/service',str(self.home/'service'))
        lib=self.home/'runit.sh';lib.write_text(source)
        (self.home/'sv/test').mkdir(parents=True);(self.home/'service').mkdir()
        (self.home/'service/test').symlink_to(self.home/'sv/test')
        bin=self.home/'bin';bin.mkdir(); log=self.home/'calls';state=self.home/'state';state.write_text('run')
        (bin/'sudo').write_text('#!/bin/sh\nexec "$@"\n')
        (bin/'sv').write_text(f'''#!/bin/sh
printf '%s\\n' "$*" >> '{log}'
if [ "$1" = status ]; then printf '%s: test\\n' "$(cat '{state}')"; exit 0; fi
[ "${{FAIL_START:-}}" != 1 ] || exit 1
printf run > '{state}'
''')
        for f in bin.iterdir():f.chmod(0o755)
        self.env['PATH']=f'{bin}:/usr/bin:/bin'
        def enable(name='test',check=True):return run(['bash','-c',f'source "{lib}"; runit_enable_service {name}'],self.env,check)
        enable();self.assertNotIn('start',log.read_text())
        state.write_text('down');enable();self.assertIn('start',log.read_text());self.assertEqual(state.read_text(),'run')
        (self.home/'service/test').unlink();state.write_text('down');enable()
        self.assertTrue((self.home/'service/test').is_symlink())
        self.assertNotEqual(enable('missing',False).returncode,0)
        state.write_text('down');self.env['FAIL_START']='1';self.assertNotEqual(enable(check=False).returncode,0)
    def test_zram(self):
        template=(ROOT/'.chezmoiscripts/run_onchange_after_12-zram.sh.tmpl').read_text()
        rendered=subprocess.run(['chezmoi','-S',str(ROOT),'execute-template'],input=template,text=True,capture_output=True,check=True).stdout
        # Stub the common library and redirect absolute system paths into a sandbox.
        libdir=self.home/'source/.chezmoiscripts/lib';libdir.mkdir(parents=True)
        calls=self.home/'calls'
        (libdir/'.lib-common.sh').write_text(f"""
source '{ROOT}/.chezmoiscripts/lib/.lib-platform.sh'
request_sudo() {{ return 0; }}
die() {{ echo "$*" >&2; exit 1; }}
log() {{ :; }}
create_backup() {{ :; }}
write_system_config() {{ mkdir -p "$(dirname "$1")"; cat > "$1"; }}
enable_service() {{ echo enable >> '{calls}'; }}
""")
        bin=self.home/'bin';bin.mkdir()
        (bin/'sudo').write_text('#!/bin/sh\nexec "$@"\n')
        (bin/'swapon').write_text('#!/bin/sh\n[ "${ACTIVE:-}" != 1 ] || echo /dev/zram0\nexit 0\n')
        for file in bin.iterdir(): file.chmod(0o755)
        (self.home/'service').mkdir()
        script=self.home/'zram.sh'
        script.write_text(rendered.replace('/etc/sv',shlex.quote(str(self.home/'sv'))).replace('/var/service',shlex.quote(str(self.home/'service'))))
        self.env.update(CHEZMOI_SOURCE_DIR=str(self.home/'source'),PATH=f'{bin}:/usr/bin:/bin',ACTIVE='1')
        run(['bash',str(script)],self.env)
        self.assertFalse(calls.exists())
        self.assertIn('ZRAM_MAX_SIZE=8192',(self.home/'sv/zramen/conf').read_text())
        self.assertIn('zramen make', (self.home/'sv/zramen/run').read_text())
        # Executing guarded service with active swap must skip zramen itself.
        (bin/'pause').write_text('#!/bin/sh\nexit 0\n');(bin/'pause').chmod(0o755)
        run(['sh',str(self.home/'sv/zramen/run')],self.env)
        self.env['ACTIVE']='0';run(['bash',str(script)],self.env)
        self.assertEqual(calls.read_text().strip(),'enable')
        calls.unlink()
        script.write_text(script.read_text().replace('MACHINE_ZRAM=true','MACHINE_ZRAM=false'))
        run(['bash',str(script)],self.env);self.assertFalse(calls.exists())

    def test_templates_and_configs(self):
        for file in (ROOT/'dot_config/zsh/dot_zshenv', ROOT/'dot_config/zsh/dot_zshrc', ROOT/'dot_zshenv'):
            run(['zsh', '-n', str(file)])
        run(['sh','-n',str(ROOT/'dot_config/n0-dots/environment.sh')])
        for file in (ROOT/'.chezmoiscripts').glob('*.tmpl'):
            rendered=subprocess.run(['chezmoi','-S',str(ROOT),'execute-template'],input=file.read_text(),text=True,capture_output=True,check=True)
            subprocess.run(['bash','-n'],input=rendered.stdout,text=True,check=True)
        for file in ROOT.rglob('*.toml'):
            tomllib.loads(file.read_text())
        run(['umbriel','validate','-c',str(ROOT/'dot_config/umbriel/config.toml')])
        run(['niri','validate','-c',str(ROOT/'dot_config/niri/config.kdl')])

if __name__=='__main__':unittest.main(verbosity=2)
