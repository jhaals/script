#!/usr/bin/env python
# Created by Johan Haals <johan.haals@gmail.com>

import os
import sys
import commands
import time

""""
This script will scp your ~/.dotfiles to machines you connect to using ssh

INSTALL
    Copy this script to your .ssh/ folder

# put the lines below in your .ssh/config

Host *
   ServerAliveInterval 30
   NumberOfPasswordPrompts 1
   AddressFamily inet
   Compression yes
   ControlMaster auto
   ControlPath ~/.ssh/socket-%r@%h:%p
   ForwardAgent yes
   PermitLocalCommand yes
   LocalCommand python ~/.ssh/copy_dotfiles.py %r %h %p

"""

# Spawn another process
pid = os.fork()
if pid:
    # kill original
    os._exit(0)

try:
    user = sys.argv[1]
    host = sys.argv[2]
    port = sys.argv[3]
except IndexError:
    sys.exit()

# we don't want to add our configs to root
if user is 'root':
        sys.exit()

# Sleep 5 seconds before scp
time.sleep(5)

# copy only if socket exists
if os.path.exists(os.path.expanduser('~/.ssh/socket-%s@%s:%s') % (user, host, port)):
    # could be rsync instead of scp
    commands.getoutput('scp -P %s -r ~/.dotfiles/.* %s@%s:.' % (port, user, host))
