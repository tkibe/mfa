# -*- coding: utf-8 -*-
"""Read the specified file and output the Multi-Factor Authentication (MFA)."""

import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from copy import deepcopy
from getpass import getpass
from urllib import parse

from ansible.errors import AnsibleError
from ansible.parsing.vault import AnsibleVaultError
from ansible_vault import Vault
from passlib import totp
from texttable import Texttable
from version import __version__  # pylint: disable=E0611

here = os.path.abspath(os.path.dirname(__file__))
MFA_FILE = os.environ.get("MFA_FILE", f"{here}/../example/demo.yml")


def output() -> int:
    """Decrypt with ansible-vault and output MFA."""
    if os.path.isfile(MFA_FILE) is False:
        print('Not exists "MFA_FILE".', file=sys.stderr)
        sys.exit()
    table = Texttable()
    lines = [["Name", "Code"]]
    try:
        vault = Vault(getpass(prompt="Vault password: "))
        yamls = vault.load(open(MFA_FILE).read())
        lists = list(map(lambda x, y: f"otpauth://totp/{x.strip()}?secret={y.strip()}", yamls.keys(), yamls.values()))
        for line in lists:
            totps = totp.TOTP.from_uri(line)
            lines.append([parse.urlparse(line).path[1:], str(totps.generate().token).rjust(6, "0")])
        table.set_cols_dtype(["t", "t"])
        table.add_rows(lines)
        print(table.draw())
    except (AnsibleError, AnsibleVaultError) as err:
        print(err, file=sys.stderr)
        return 1
    except TypeError as err:
        print(err, file=sys.stderr)
        return 1
    return 0


def _prompt_choices(message: str, answer: list, default: str) -> str:
    """Select prompt."""
    print(message)
    choices = "/".join(answer)
    confirm = input(f"{choices} ({default}): ")
    if confirm == "":
        confirm = default
    if confirm in answer:
        return confirm
    return _prompt_choices(message, answer, default)


def add() -> int:
    """MFA will be added."""
    try:
        vault = Vault(getpass(prompt="Vault password: "))
        yamls = vault.load(open(MFA_FILE).read())
        lines = [["Name", "Secret key"]]
        while True:
            # MFA name
            message = "Enter the name of the element to be added."
            print(message)
            name = input("Name: ")
            if name in yamls.keys():
                message = "The name you entered is already registered, do you want to overwrite it?"
                confirm = _prompt_choices(message, ["y", "n"], "n")
                if confirm == "n":
                    continue
            # secret key
            message = "Please enter your for a MFA secret key without echoing."
            print(message)
            secret = getpass("Secret key: ")
            # input confirmation
            message = "Do you want to confirm your input?"
            confirm = _prompt_choices(message, ["y", "n"], "n")
            lines.append([name, secret])
            if confirm == "y":
                table = Texttable()
                table.set_cols_dtype(["t", "t"])
                table.add_rows(lines)
                print(table.draw())
                message = "Do you want to save it?"
                confirm = _prompt_choices(message, ["y", "n"], "y")
                if confirm == "n":
                    lines.pop(-1)
                    continue
            # Add more MFA
            message = "Do you want to add more MFA?"
            confirm = _prompt_choices(message, ["y", "n"], "n")
            if confirm == "y":
                continue
            break
        lines.pop(0)
        for key, value in lines:
            yamls.update({key: value})
        with open(MFA_FILE, mode="wb") as fpobj:
            vault.dump(yamls, fpobj)
    except (AnsibleError, AnsibleVaultError) as err:
        print(err, file=sys.stderr)
        return 1
    except TypeError as err:
        print(err, file=sys.stderr)
        return 1
    return 0


def delete() -> int:
    """MFA will be deleted."""
    try:
        vault = Vault(getpass(prompt="Vault password: "))
        yamls = vault.load(open(MFA_FILE).read())
        print(yamls)
        table = Texttable()
        lines = [["Name", "Be delete"]]
        for item in list(yamls.keys()):
            lines.append([item, ""])
        while True:
            _table = deepcopy(table)
            _table.set_cols_dtype(["t", "t"])
            _table.set_cols_align(["l", "c"])
            _table.add_rows(lines)
            print(_table.draw())
            # MFA name
            message = "Enter the name to be deleted."
            print(message)
            name = input("Name: ")
            matched = False
            for idx, item in enumerate(lines):
                if item[0] == name:
                    matched = True
                    lines[idx] = [item[0], "Yes"]
                    break
            if not matched:
                # No matching
                message = "No matching name found."
                print(message)
                message = "Would you like to re-enter?"
                confirm = _prompt_choices(message, ["y", "n"], "y")
            else:
                # Delete more MFA
                message = "Do you want to delete more MFA?"
                confirm = _prompt_choices(message, ["y", "n"], "n")
            # Re-enter
            if confirm == "y":
                continue
            break
        # Confirm
        table.set_cols_dtype(["t", "t"])
        table.set_cols_align(["l", "c"])
        table.add_rows(lines)
        print(table.draw())
        message = "* Do you really want to deletes this MFA?"
        confirm = _prompt_choices(message, ["y", "n"], "n")
        if confirm == "n":
            return 0
        lines.pop(0)
        for item in lines:
            if item[1] != "Yes":
                continue
            del yamls[item[0]]
        with open(MFA_FILE, mode="wb") as fpobj:
            vault.dump(yamls, fpobj)
    except (AnsibleError, AnsibleVaultError) as err:
        print(err, file=sys.stderr)
        return 1
    except TypeError as err:
        print(err, file=sys.stderr)
        return 1
    return 0


def main() -> int:
    """args branching."""
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("-o", "--output", action="store_true", default=True, help="Output MFA list")
    parser.add_argument("-a", "--add", action="store_true", default=False, help="Add MFA")
    parser.add_argument("-d", "--delete", action="store_true", default=False, help="Delete MFA")
    parser.add_argument("-v", "--version", action="version", help="Show version", version=__version__)
    args = parser.parse_args()
    result = 0
    if args.add:
        result = add()
    elif args.delete:
        result = delete()
    elif args.output:
        result = output()
    return result


if __name__ == "__main__":
    sys.exit(main())
