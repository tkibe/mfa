# -*- coding: utf-8 -*-

"""Read the specified file and output the Multi-Factor Authentication (MFA)."""

import getpass
import os
import sys
from urllib import parse

from ansible.errors import AnsibleError
from ansible.parsing.vault import AnsibleVaultError
from ansible_vault import Vault
from passlib import totp
from texttable import Texttable

MFA_DEFAULT = f"{os.path.dirname(os.path.abspath(__file__))}/demo/example.yml"
MFA_FILE = os.environ.get("MFA_FILE", MFA_DEFAULT)


def main() -> None:
    """Decrypt with ansible-vault and output MFA."""
    if os.path.isfile(MFA_FILE) is False:
        print('Not exists "MFA_FILE".', file=sys.stderr)
        sys.exit()
    table = Texttable()
    lines = [["Name", "Code"]]

    try:
        vault = Vault(getpass.getpass(prompt="Vault password: "))
        yamls = vault.load(open(MFA_FILE).read())
        lists = list(map(lambda x, y: f"otpauth://totp/{x.strip()}?secret={y.strip()}", yamls.keys(), yamls.values()))
        for line in lists:
            totps = totp.TOTP.from_uri(line)
            lines.append([parse.urlparse(line).path[1:], str(totps.generate().token).rjust(6, "0")])
        table.set_cols_dtype(["t", "t"])
        table.add_rows(lines)
        print(table.draw(), file=sys.stdout)
    except (AnsibleError, AnsibleVaultError) as err:
        print(err, file=sys.stderr)


if __name__ == "__main__":
    main()
