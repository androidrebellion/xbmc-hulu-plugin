#!/usr/bin/python

import os
import re
import subprocess
import common

PID_RE = re.compile("hulupid=(.*)")

def hulu_decrypt(pid):
    gnash = common.settings['gnash_path']
    swf = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DecryptPid.swf")
    args = [gnash, "--render-mode", "0", "--once", "--verbose", "--param", "FlashVars=pid=%s" % pid, swf]
    output = subprocess.Popen(args, executable=gnash, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE).communicate()[0]
    match = PID_RE.search(output)
    if match:
        return match.group(1)
    else:
        return None