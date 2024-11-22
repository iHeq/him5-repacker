#!/usr/bin/env python3

import argparse
import os
import logging as log
from fushigi import repacker  # Assuming repacker is defined in fushigi module

log.basicConfig(level=log.WARNING)  # Change to warning when finished

# Config

argparser = argparse.ArgumentParser(description='Repack folders into HIM5 HXP archives')
argparser.add_argument('folders', metavar='target', nargs='+', help='source folder to repack')
argparser.add_argument('--output', dest='output', default='./asset_dump', help='directory for output files, defaults to ./asset_dump')

args = argparser.parse_args()

# Body

def process_folder(path):
    log.info('Processing folder: ' + path)
    output_path = os.path.join(args.output, os.path.basename(path) + '.hxp')

    if os.path.exists(output_path):
        response = input('File %s already exists. Remove and re-pack? (y/N) ' % output_path)
        if response.lower() in ('y', 'yes'):
            os.remove(output_path)
        else:
            log.info('Skipping repack for %s' % path)
            return

    contents = sorted([os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])

    if contents:
        repacker.him5(contents, output_path)
        log.info('Successfully repacked %s into %s' % (path, output_path))
    else:
        log.warning('No files found in %s to repack' % path)

# Main loop

for path in args.folders:
    if os.path.isdir(path):
        process_folder(path)
    else:
        log.warning('%s is not a directory; skipping' % path)