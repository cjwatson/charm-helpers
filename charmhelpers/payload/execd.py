#!/usr/bin/env python

import os
import sys
import subprocess
from charmhelpers.core import hookenv


def default_execd_dir():
    return os.path.join(os.environ['CHARM_DIR'],'exec.d')


def execd_module_paths(execd_dir=None):
    if not execd_dir:
        execd_dir = default_execd_dir()
    for subpath in os.listdir(execd_dir):
        module = os.path.join(execd_dir, subpath)
        if os.path.isdir(module):
            yield module


def execd_submodule_paths(submodule, execd_dir=None):
    for module_path in execd_module_paths(execd_dir):
        path = os.path.join(module_path, submodule)
        if os.access(path, os.X_OK) and os.path.isfile(path):
            yield path


def execd_run(submodule, execd_dir=None, die_on_error=False):
    for submodule_path in execd_submodule_paths(submodule, execd_dir):
        try:
            subprocess.check_call(submodule_path, shell=True)
        except subprocess.CalledProcessError as e:
            hookenv.log(e.output)
            if die_on_error:
                sys.exit(e.returncode)


def execd_preinstall(execd_dir=None):
    execd_run(execd_dir, 'charm-pre-install')