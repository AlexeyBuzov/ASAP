#!/usr/bin/env python

import subprocess
from pygit2 import Repository

branchName = Repository('.').head.shorthand
subprocess.call(["git", "push", "--force-with-lease", "origin", branchName])
