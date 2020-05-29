![Documents in English](https://img.shields.io/badge/document-en__US-brightgreen.svg)

# mfa

Tool to do Multi-Factor Authentication (MFA) in CLI.


## Required environment

* OS X, Linux
* Python 3.x

## Basic Setup

1. Download PC.

    ```bash
    $ git clone git@github.com:tkibe/mfa.git ~/bin/mfa
    ```

2. Install the Python packages CLI as follows:

    ```bash
    $ cd ~/bin/mfa
    $ pip install -r requirements.txt
    ```

    **_Note_**: If you're having permission issues on your system installing the CLI, please try the following command:

    ```bash
    $ sudo pip install -r requirements.txt
    ```


3. Simply setting the "MFA" name and secret. (YAML format)


    This example defines a key "Demo MFA One" with value MFA secret key, a key "Demo MFA Two" with value MFA secret key that is itself set of key/value pairs.
    ```bash
    e.g.)
    $ echo "Demo MFA One: z7EKrWNx2T86FcLrNyiRKSnXVawe8kHx" >> test/example.yml
    $ echo "Demo MFA Two: jJNHhNBYujPFhKt4c3MC7Sk7QuTd53S8" >> test/example.yml
    ```

4. To run this tool, you need to set valid environment variable "MFA_FILE" beforehand.

    ```bash
    e.g.)
    $ export MFA_FILE=~/bin/mfa/test/example.yml
    ```

5. Can be executed when the setting is completed.

    Show one time password.
    ```bash
    $ python ~/bin/mfa/main.py
    ```

    It also feasible to narrow down the list.
    ```bash
    e.g.)
    $ python ~/bin/mfa/main.py | grep One
    | Demo MFA One  | xxxxxx |
    $ python ~/bin/mfa/main.py | grep Two
    | Demo MFA Two  | xxxxxx |
    ```

## Recommended settings

If you want to use it permanently, add the setting to `~/.bash_profile`.

```
$ echo "export MFA_FILE=~/bin/mfa/auth.yml" >> ~/.bash_profile
$ echo 'alias mfa="python ~/bin/mfa/main.py"' >> ~/.bash_profile
$ echo "<Your secret key>: xxxxxxxxxx" >> ~/bin/mfa/auth.yml
```