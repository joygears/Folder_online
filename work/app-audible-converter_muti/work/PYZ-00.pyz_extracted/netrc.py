# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: netrc.py
"""An object-oriented interface to .netrc files."""
import os, shlex, stat
__all__ = [
 'netrc', 'NetrcParseError']

class NetrcParseError(Exception):
    __doc__ = 'Exception raised on syntax errors in the .netrc file.'

    def __init__(self, msg, filename=None, lineno=None):
        self.filename = filename
        self.lineno = lineno
        self.msg = msg
        Exception.__init__(self, msg)

    def __str__(self):
        return '%s (%s, line %s)' % (self.msg, self.filename, self.lineno)


class netrc:

    def __init__(self, file=None):
        default_netrc = file is None
        if file is None:
            try:
                file = os.path.join(os.environ['HOME'], '.netrc')
            except KeyError:
                raise OSError('Could not find .netrc: $HOME is not set')

        self.hosts = {}
        self.macros = {}
        with open(file) as (fp):
            self._parse(file, fp, default_netrc)

    def _parse(self, file, fp, default_netrc):
        lexer = shlex.shlex(fp)
        lexer.wordchars += '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        lexer.commenters = lexer.commenters.replace('#', '')
        while True:
            saved_lineno = lexer.lineno
            toplevel = tt = lexer.get_token()
            if not tt:
                break
            else:
                if tt[0] == '#':
                    if lexer.lineno == saved_lineno and len(tt) == 1:
                        lexer.instream.readline()
                        continue
                else:
                    if tt == 'machine':
                        entryname = lexer.get_token()
                    else:
                        if tt == 'default':
                            entryname = 'default'
                        else:
                            if tt == 'macdef':
                                entryname = lexer.get_token()
                                self.macros[entryname] = []
                                lexer.whitespace = ' \t'
                                while True:
                                    line = lexer.instream.readline()
                                    if not line or line == '\n':
                                        lexer.whitespace = ' \t\r\n'
                                        break
                                    self.macros[entryname].append(line)

                                continue
                            else:
                                raise NetrcParseError('bad toplevel token %r' % tt, file, lexer.lineno)
            login = ''
            account = password = None
            self.hosts[entryname] = {}
            while True:
                tt = lexer.get_token()
                if tt.startswith('#') or tt in frozenset({'', 'macdef', 'default', 'machine'}):
                    if password:
                        self.hosts[entryname] = (
                         login, account, password)
                        lexer.push_token(tt)
                        break
                    else:
                        raise NetrcParseError('malformed %s entry %s terminated by %s' % (
                         toplevel, entryname, repr(tt)), file, lexer.lineno)
                elif tt == 'login' or tt == 'user':
                    login = lexer.get_token()
                elif tt == 'account':
                    account = lexer.get_token()
                else:
                    if tt == 'password':
                        if os.name == 'posix':
                            if default_netrc:
                                prop = os.fstat(fp.fileno())
                                if prop.st_uid != os.getuid():
                                    import pwd
                                    try:
                                        fowner = pwd.getpwuid(prop.st_uid)[0]
                                    except KeyError:
                                        fowner = 'uid %s' % prop.st_uid

                                    try:
                                        user = pwd.getpwuid(os.getuid())[0]
                                    except KeyError:
                                        user = 'uid %s' % os.getuid()

                                    raise NetrcParseError('~/.netrc file owner (%s) does not match current user (%s)' % (
                                     fowner, user), file, lexer.lineno)
                                if prop.st_mode & (stat.S_IRWXG | stat.S_IRWXO):
                                    raise NetrcParseError('~/.netrc access too permissive: access permissions must restrict access to only the owner', file, lexer.lineno)
                        password = lexer.get_token()
                    else:
                        raise NetrcParseError('bad follower token %r' % tt, file, lexer.lineno)

    def authenticators(self, host):
        """Return a (user, account, password) tuple for given host."""
        if host in self.hosts:
            return self.hosts[host]
        else:
            if 'default' in self.hosts:
                return self.hosts['default']
            return

    def __repr__(self):
        """Dump the class data in the format of a .netrc file."""
        rep = ''
        for host in self.hosts.keys():
            attrs = self.hosts[host]
            rep += f"machine {host}\n\tlogin {attrs[0]}\n"
            if attrs[1]:
                rep += f"\taccount {attrs[1]}\n"
            rep += f"\tpassword {attrs[2]}\n"

        for macro in self.macros.keys():
            rep += f"macdef {macro}\n"
            for line in self.macros[macro]:
                rep += line

            rep += '\n'

        return rep


if __name__ == '__main__':
    print(netrc())