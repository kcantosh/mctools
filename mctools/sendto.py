#! /usr/bin/env python

import os
from os.path import basename, dirname, abspath, join, isfile
import argparse

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import subprocess


def sendto(server=False, project=False, folders=False):

    if not server:
        raise Exception('No remote server defined')

    conf_file = join(os.environ['HOME'], '.sendto.conf')
    if not isfile(conf_file):
        raise Exception("No config file found. Server names should be "
                        "set up with calculation directories "
                        "in {0}".format(conf_file))

    conf = ConfigParser()
    conf.read(conf_file)
    rundir = conf.get(server, 'rundir')

    # Use current directory if none provided
    if len(folders) == 0:
        folders = ['os.path.curdir']

    for calc in folders:
        calc = abspath(calc)
        # If project isn't given use name of directory two levels
        # above (Assumes structure /parents/PROJECTS/runs/RUNDIRS)
        if not project:
            project = basename(dirname(dirname(calc)))

    rsync_call = ['rsync', '-avzu', calc,
                  ':'.join((server, os.path.join(rundir,
                                                 project)))]
    subprocess.call(rsync_call)


def get_args():
    parser = argparse.ArgumentParser(
        description="Send calculations folder(s) to remote server"
        )
    parser.add_argument('server', type=str,
                        help="Server name from SSH config")
    parser.add_argument('-p', '--project', type=str, default=False,
                        help="Project ID (guess if not provided)")
    parser.add_argument('folders', type=str, nargs='*')
    args = parser.parse_args()
    return vars(args)


def main():
    args = get_args()
    sendto(**args)

if __name__ == '__main__':
    main()
