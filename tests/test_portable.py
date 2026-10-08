"""Isolated portability regression checks; no system services or desktop launched."""
import os
from pathlib import Path
import shutil
import shlex
import signal
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
        self.env['XDG_DATA_HOME']=str(self.home/'data with spaces')
        for shell in ('sh','bash','zsh'):
            for auto in ('set +a','set -a'):
                code=f'{auto}; . "{ROOT}/dot_config/n0-dots/environment.sh"; first="$PATH|$XDG_DATA_DIRS|$XCURSOR_PATH"; . "{ROOT}/dot_config/n0-dots/environment.sh"; [ "$first" = "$PATH|$XDG_DATA_DIRS|$XCURSOR_PATH" ] || exit 7; case $- in *a*) echo on;; *) echo off;; esac; printf "%s\\n" "$PATH" "$XDG_DATA_DIRS" "$QT_QPA_PLATFORMTHEME"'
                result=run([shell,'-c',code],self.env).stdout
                self.assertEqual(result.splitlines()[0], 'on' if auto=='set -a' else 'off')
                self.assertIn('/nix/var/nix/profiles/default/bin',result)
                self.assertIn('.nix-profile/share',result)
                self.assertIn('flatpak/exports/share',result)
                self.assertIn(str(self.home/'data with spaces/flatpak/exports/share'),result)
                self.assertTrue(result.endswith('gtk3\n'))
        # A late environment.d file must control PATH priority too; the loader
        # only deduplicates after loading, without imposing settings afterward.
        (conf/'environment.d/zz-local.conf').write_text('PATH=/opt/local:$PATH\nQT_QPA_PLATFORMTHEME=local-choice\n')
        for shell in ('sh','bash','zsh'):
            result=run([shell,'-c',f'. "{ROOT}/dot_config/n0-dots/environment.sh"; printf "%s\\n" "$PATH" "$QT_QPA_PLATFORMTHEME"'],self.env).stdout
            self.assertTrue(result.startswith('/opt/local:'))
            self.assertTrue(result.endswith('local-choice\n'))
        shutil.rmtree(conf)
        run(['sh','-c',f'. "{ROOT}/dot_config/n0-dots/environment.sh"'],self.env)
    def test_environment_empty_and_exports(self):
        conf = Path(self.env['XDG_CONFIG_HOME'])
        for populated in (False, True):
            if populated:
                (conf/'environment.d').mkdir(parents=True)
            for shell in ('sh', 'bash', 'zsh'):
                result = run([shell, '-c', f'. "{ROOT}/dot_config/n0-dots/environment.sh"'], self.env)
                self.assertEqual(result.stderr, '')
        # The loader must export new assignments, preserve lexical order and
        # restore Zsh options, even when no settings were inherited at login.
        (conf/'environment.d/10-first.conf').write_text('N0_VALUE=first\n')
        (conf/'environment.d/20-second.conf').write_text('N0_VALUE=$N0_VALUE:second\n')
        for shell in ('sh', 'bash', 'zsh'):
            result = run([shell, '-c', f'. "{ROOT}/dot_config/n0-dots/environment.sh"; /usr/bin/printenv N0_VALUE'], self.env)
            self.assertEqual(result.stdout, 'first:second\n')
        result = run(['zsh', '-c', f'setopt nomatch; . "{ROOT}/dot_config/n0-dots/environment.sh"; [[ -o nomatch ]]'], self.env)
        self.assertEqual(result.returncode, 0)

    def test_zsh_startup(self):
        conf = Path(self.env['XDG_CONFIG_HOME'])
        zdir = conf/'zsh'; zdir.mkdir(parents=True)
        shutil.copy(ROOT/'dot_zshenv', self.home/'.zshenv')
        for name in ('zshenv', 'zshrc'):
            shutil.copy(ROOT/f'dot_config/zsh/dot_{name}', zdir/f'.{name}')
        # Exercise real startup files without loading plugins or changing the
        # host's /etc/profile.d. This fixture models Void's login profile hook.
        shutil.copytree(ROOT/'dot_config/n0-dots', conf/'n0-dots')
        shutil.copytree(ROOT/'dot_config/environment.d', conf/'environment.d')
        (zdir/'conf.d').mkdir()
        shutil.copy(ROOT/'dot_config/zsh/conf.d/history.zsh', zdir/'conf.d/history.zsh')
        (zdir/'.zprofile').write_text('. "$XDG_CONFIG_HOME/n0-dots/environment.sh"\n')
        (conf/'environment.d/zz-count.conf').write_text('N0_LOADS=$((${N0_LOADS:-0} + 1))\n')
        env = dict(HOME=str(self.home), XDG_CONFIG_HOME=str(conf), PATH='/usr/bin:/bin', TERM='dumb')
        probe = """path+=("/opt/repeated" "/opt/repeated"); print -rl -- "${N0_LOADS:-0}" "$PATH" "$HISTFILE"; zsh -d -c 'print -r -- "${N0_LOADS:-0}"'"""
        for inherited in (False, True):
            if inherited: env['ZDOTDIR'] = str(zdir)
            for mode, loads in (('-c', 0), ('-ic', 1), ('-lc', 1), ('-lic', 2)):
                result = run(['zsh', '-d', mode, probe], env)
                self.assertEqual(result.stderr, '')
                lines = result.stdout.splitlines()
                self.assertEqual(lines[0], str(loads))
                self.assertEqual(lines[3], str(loads))  # child script never reloads desktop settings
                self.assertEqual(lines[1].split(':').count('/opt/repeated'), 1)
                self.assertIn(str(self.home/'.local/bin'), lines[1].split(':'))
                if 'i' in mode or mode == '-c':
                    self.assertEqual(lines[2], str(zdir/'.zsh_history'))

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
    @unittest.skipUnless(shutil.which('runsv') and shutil.which('sv'), 'requires runit tools')
    def test_runit_delayed_supervisor(self):
        # Real sv fails immediately before supervision exists, regardless of
        # -w. Model runsvdir's delayed discovery without touching host services.
        service = self.home/'sv/test'; service.mkdir(parents=True)
        (service/'run').write_text('#!/bin/sh\nexec sleep 60\n')
        (service/'run').chmod(0o755)
        (service/'down').touch()
        (self.home/'service').mkdir()
        lib = self.home/'runit.sh'
        lib.write_text((ROOT/'.chezmoiscripts/lib/.lib-runit.sh').read_text().replace('/etc/sv', str(self.home/'sv')).replace('/var/service', str(self.home/'service')))
        bin = self.home/'bin'; bin.mkdir()
        (bin/'sudo').write_text('#!/bin/sh\nexec "$@"\n'); (bin/'sudo').chmod(0o755)
        self.env['PATH'] = f'{bin}:/usr/bin:/bin'
        supervisor = subprocess.Popen(['sh', '-c', 'sleep 0.2; exec runsv "$1"', 'test-supervisor', str(service)], env=self.env, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            result = run(['bash', '-c', f'source {shlex.quote(str(lib))}; runit_enable_service test || {{ echo "$LAST_ERROR" >&2; exit 1; }}'], self.env, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(run(['sv', 'status', str(service)], self.env).stdout.startswith('run:'))
        finally:
            os.killpg(supervisor.pid, signal.SIGTERM)
            try:
                supervisor.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(supervisor.pid, signal.SIGKILL)
                supervisor.wait()

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
