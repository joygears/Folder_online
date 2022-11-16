# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: psutil\_psposix.py
"""Routines common to all posix systems."""
import glob, os, signal, sys, time
from ._common import memoize
from ._common import sdiskusage
from ._common import TimeoutExpired
from ._common import usage_percent
from ._compat import ChildProcessError
from ._compat import FileNotFoundError
from ._compat import InterruptedError
from ._compat import PermissionError
from ._compat import ProcessLookupError
from ._compat import PY3
from ._compat import unicode
if sys.version_info >= (3, 4):
    import enum
else:
    enum = None
__all__ = [
 'pid_exists', 'wait_pid', 'disk_usage', 'get_terminal_map']

def pid_exists(pid):
    """Check whether pid exists in the current process table."""
    if pid == 0:
        return True
    else:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True

        return True


if enum is not None and hasattr(signal, 'Signals'):
    Negsignal = enum.IntEnum('Negsignal', dict([(x.name, -x.value) for x in signal.Signals]))

    def negsig_to_enum(num):
        """Convert a negative signal value to an enum."""
        try:
            return Negsignal(num)
        except ValueError:
            return num


else:

    def negsig_to_enum(num):
        return num


def wait_pid(pid, timeout=None, proc_name=None, _waitpid=os.waitpid, _timer=getattr(time, 'monotonic', time.time), _min=min, _sleep=time.sleep, _pid_exists=pid_exists):
    """Wait for a process PID to terminate.

    If the process terminated normally by calling exit(3) or _exit(2),
    or by returning from main(), the return value is the positive integer
    passed to *exit().

    If it was terminated by a signal it returns the negated value of the
    signal which caused the termination (e.g. -SIGTERM).

    If PID is not a children of os.getpid() (current process) just
    wait until the process disappears and return None.

    If PID does not exist at all return None immediately.

    If *timeout* != None and process is still alive raise TimeoutExpired.
    timeout=0 is also possible (either return immediately or raise).
    """
    if pid <= 0:
        raise ValueError("can't wait for PID 0")
    interval = 0.0001
    flags = 0
    if timeout is not None:
        flags |= os.WNOHANG
        stop_at = _timer() + timeout

    def sleep(interval):
        if timeout is not None:
            if _timer() >= stop_at:
                raise TimeoutExpired(timeout, pid=pid, name=proc_name)
        _sleep(interval)
        return _min(interval * 2, 0.04)

    while True:
        try:
            retpid, status = os.waitpid(pid, flags)
        except InterruptedError:
            interval = sleep(interval)
        except ChildProcessError:
            while _pid_exists(pid):
                interval = sleep(interval)

            return

        if retpid == 0:
            interval = sleep(interval)
            continue
        else:
            if os.WIFEXITED(status):
                return os.WEXITSTATUS(status)
            if os.WIFSIGNALED(status):
                return negsig_to_enum(-os.WTERMSIG(status))
            raise ValueError('unknown process exit status %r' % status)


def disk_usage(path):
    """Return disk usage associated with path.
    Note: UNIX usually reserves 5% disk space which is not accessible
    by user. In this function "total" and "used" values reflect the
    total and used disk space whereas "free" and "percent" represent
    the "free" and "used percent" user disk space.
    """
    if PY3:
        st = os.statvfs(path)
    else:
        try:
            st = os.statvfs(path)
        except UnicodeEncodeError:
            if isinstance(path, unicode):
                try:
                    path = path.encode(sys.getfilesystemencoding())
                except UnicodeEncodeError:
                    pass

                st = os.statvfs(path)
            else:
                raise

    total = st.f_blocks * st.f_frsize
    avail_to_root = st.f_bfree * st.f_frsize
    avail_to_user = st.f_bavail * st.f_frsize
    used = total - avail_to_root
    total_user = used + avail_to_user
    usage_percent_user = usage_percent(used, total_user, round_=1)
    return sdiskusage(total=total,
      used=used,
      free=avail_to_user,
      percent=usage_percent_user)


@memoize
def get_terminal_map():
    """Get a map of device-id -> path as a dict.
    Used by Process.terminal()
    """
    ret = {}
    ls = glob.glob('/dev/tty*') + glob.glob('/dev/pts/*')
    for name in ls:
        assert name not in ret, name
        try:
            ret[os.stat(name).st_rdev] = name
        except FileNotFoundError:
            pass

    return ret