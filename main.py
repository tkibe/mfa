# -*- coding: utf-8 -*-

import sys
import os
import yaml
from passlib import totp
from urllib import parse
from texttable import Texttable

"""
Read the specified file and output the Multi-Factor Authentication (MFA).

e.g.)
    $ export MFA_FILE=~/bin/mfa/test/example.yml
    $ python ~/bin/mfa/main.py
"""

MFA_DEFAULT = f"{os.path.dirname(os.path.abspath(__file__))}/test/example.yml"
MFA_FILE = os.environ.get('MFA_FILE', MFA_DEFAULT)


def main():
    if os.path.isfile(MFA_FILE) is False:
        print('Not exists "MFA_FILE".')
        sys.exit()
    table = Texttable()
    lines = [['Name', 'Code']]
    with open(MFA_FILE, 'r+') as f:
        try:
            yamls = yaml.load(f, Loader=yaml.SafeLoader)
            lists = list(map(
                lambda x, y: f"otpauth://totp/{x.strip()}?secret={y.strip()}",
                yamls.keys(), yamls.values()))
            for line in lists:
                totps = totp.TOTP.from_uri(line)
                lines.append([
                    parse.urlparse(line).path[1:],
                    str(totps.generate().token).rjust(6, '0')
                ])
        except Exception:
            pass
    table.set_cols_dtype(['t', 't'])
    table.add_rows(lines)
    print(table.draw())


if __name__ == '__main__':
    main()
