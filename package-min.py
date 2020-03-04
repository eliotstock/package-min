# Copyright 2020 Eliot Stock
"""Package minimalist. Find unused packages on this Linux host so that you can remove them."""

import logging
import subprocess
import sys

_LOG = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def main() -> int:
    """Script entry point."""

    header_done = False

    # Get just the names of all the packages installed on the host.
    package_list = subprocess.check_output(['dpkg-query', '-f', "${Package}\n", '-W']).splitlines()

    _LOG.info(f'Analysing {len(package_list)} packages...')

    # For each package (usually about 2K)...
    for p in package_list:
        package = p.decode('utf-8')

        # Get a list of all reverse dependencies, that is, packages that depend on this package.
        rdepends_output = subprocess.check_output(['apt-cache', 'rdepends', package]).splitlines()

        # The first two lines of the output are headers. Every other line is a dependency.
        rdepends = max(len(rdepends_output) - 2, 0)

        if rdepends == 0:
            # Get some details for the package, then pull out the description from them.
            show_output = subprocess.check_output(['apt-cache', 'show', package]).splitlines()

            for line in show_output:
                line_str = line.decode('utf-8')

                if line_str.startswith('Description: '):
                    # Print the header only once we're sure we have at least one package to report.
                    if not header_done:
                        _LOG.info('The following packages are unused by any other package:')
                        header_done = True

                    _LOG.info(f"  {package}: {line_str.replace('Description: ', '')}")

    if not header_done:
        _LOG.info('All packages have at least one dependency')

if __name__ == '__main__':
    sys.exit(main())
