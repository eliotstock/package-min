# Copyright 2020 Eliot Stock
"""Package minimalist. Find unused packages on this Linux host so that you can remove them."""

import logging
import subprocess
import sys

_LOG = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def main() -> int:
    """Script entry point."""

    # args = parse_args()

    package_list = subprocess.check_output(['dpkg-query', '-f', "${Package}\n", '-W']).splitlines()

    _LOG.info('Found %d pacakges', len(package_list))

if __name__ == '__main__':
    sys.exit(main())
