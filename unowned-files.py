# Copyright 2020 Eliot Stock
"""Unowned files. Find files on this host that are not owned by any package."""

import logging
import subprocess
import sys

_LOG = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def main() -> int:
    """Script entry point."""

    # Get just the names of all the packages installed on the host.
    package_list = subprocess.check_output(['dpkg-query', '-f', "${Package}\n", '-W']).splitlines()

    _LOG.info(f'Analysing {len(package_list)} packages...')

    # List of all files that are owned by a package.
    owned_files = []

    # List of packages for which we weren't able to find the files because of
    # dpkg-query throwing an error.
    package_errors = []

    # For each package (usually about 2K)...
    for p in package_list:
        package = p.decode('utf-8')

        # Get a list of all files owned by this package. This is the same as
        # reading /var/lib/dpkg/info/[package].list. However, this duplicates
        # the whole path up to each file.
        try:
            files_output = subprocess.check_output(['dpkg-query', '-L', package], stderr=subprocess.DEVNULL).splitlines()
        except subprocess.CalledProcessError:
            package_errors.append(p)

        # _LOG.info(f'Package {p} has {len(files_output)} files')

        owned_files.append(files_output)

    if package_errors:
        _LOG.warning(f'These packages had errors: {package_errors}')

    # Now list all files on the entire root filesystem, with some exclusions.
    # find / \( -path "$HOME" -o -path /proc -o -path /lost+found -o -path /.pki -o -path /media \) -prune -o -print -type f
    find_cmd = r'find / ( -path "$HOME" -o -path /proc -o -path /.pki -o -path /media ) -prune -o -print -type f'

    # _LOG.info(f'find_cmd token 1 (0-based): {find_cmd.split()[1]}')
    # _LOG.info(f'find_cmd token 2 (0-based): {find_cmd.split()[2]}')

    all_files = subprocess.check_output(find_cmd.split(), stderr=subprocess.DEVNULL).splitlines()

    _LOG.info(f'Host has {len(all_files)} files of interest')

    # TODO: Get the difference of all_files and owned_files, ie. the files that are not owned by any package.

if __name__ == '__main__':
    sys.exit(main())
