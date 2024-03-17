#!/usr/bin/env python

import sys
import subprocess

head = "HEAD~" + sys.argv[1]
subprocess.call(["git", "reset", "--soft", head])
