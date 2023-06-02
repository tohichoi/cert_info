#!/usr/bin/env python

import os
import subprocess
import re
import sys
import dateparser
from datetime import datetime, timezone

BASEDIR = './'
FILENAME_DER = 'signCert.der'
FILENAME_KEY = 'signPri.key'
VALID_OPT_NAME = set(['notBefore', 'notAfter'])
pat=re.compile(r'^([^=]+)=(.+)$')
def parse_line(line):
    m=re.search(pat, line)
    if m:
        return (m.group(1), m.group(2))
    return None


# def get_datetime(datestr):
#     return dateparser.parse(datestr).isoformat()
    
def get_info(path):
    # cmd = ['openssl', 'x509', '-nameopt', 'utf8', '-inform', 'der', '-in', os.path.join(path, FILENAME_DER), '-subject', '-dates']
    cmd = ['openssl', 'x509', '-nameopt', 'utf8', '-inform', 'der', '-in', os.path.join(path, FILENAME_DER), '-dates']

    output=''
    try:
        output=subprocess.check_output(cmd).decode("utf-8")
    except Exception as e:
        print(f'{path} : {e.args}')
        return

    keyval={}
    for line in output.split("\n"):
        val=parse_line(line)
        if val and val[0] in VALID_OPT_NAME:
            keyval[val[0]]=val[1]

    # print(os.path.basename(path))
    print(f'\n{path}')
    sd=dateparser.parse(keyval['notBefore'])
    ed=dateparser.parse(keyval['notAfter'])
    cd=datetime.now(timezone.utc)
    isvalid=cd >= sd and cd <= ed
    print(f'notBefore: {sd.isoformat()}')
    print(f'notAfter: {ed.isoformat()}')
    print(f"State: {'Valid' if isvalid else 'Expired'}")
    # subject
    # for tokens in keyval['subject'].split(','):
    #     m=re.search(pat, tokens.strip())
    #     print(f'{m.group(1)} = {m.group(2)}')

for dirpath, dirnames, filenames in os.walk(BASEDIR):
    if len(set(filenames).intersection(set([FILENAME_DER, FILENAME_KEY]))) == 2:
        # path = os.path.join(dirpath, dirpath)
        # print(path)
        path=dirpath
        get_info(path)
