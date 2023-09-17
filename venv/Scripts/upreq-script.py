#!"c:\users\camil\onedrive\área de trabalho\espaco-de-trabalho\backend-puc\venv\scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'upgrade-requirements==1.7.0','console_scripts','upreq'
__requires__ = 'upgrade-requirements==1.7.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('upgrade-requirements==1.7.0', 'console_scripts', 'upreq')()
    )
