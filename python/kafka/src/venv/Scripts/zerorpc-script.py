#!E:\jyong\myApp\python\kafka\src\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'zerorpc==0.6.1','console_scripts','zerorpc'
__requires__ = 'zerorpc==0.6.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('zerorpc==0.6.1', 'console_scripts', 'zerorpc')()
    )
