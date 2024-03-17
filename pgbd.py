#!/usr/bin/env python

import subprocess
from pygit2 import Repository

#git branch | sed -n -e 's/^\* \(.*\)/\1/p'
branchName = Repository('.').head.shorthand
subprocess.call(["git", "checkout", "main"])
subprocess.call(["git", "branch", "-D", branchName])
