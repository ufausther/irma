import os
import re
from subprocess import Popen, PIPE

version = None
regex = re.compile(r'(detected|suspicion)\t(.*)\r')

def resultfromoutput(code, stdout):
    if code == 0:
        return "clean"
    elif code == 2 or code == 3:
        m = regex.search(stdout)
        if m:
            return m.group(2)
        else:
            return stdout
    else:
        return "Unknown retcode %d" % code

def get_version():
    global version
    p = Popen(["avp.com", "help"], stdout=PIPE)
    out, _ = p.communicate()
    # win fr charset to utf8
    res = out.decode("cp1252")
    if p.returncode == 0:
        version = res.splitlines()[0]
    else:
        version = "unknown"
    return

def get_scan_result(filename):
    p = Popen(["avp.com", "scan", "/i0", filename], stdout=PIPE)
    out, _ = p.communicate()
    # win fr charset to utf8
    res = out.decode("cp1252")
    retcode = p.returncode
    return resultfromoutput(retcode, res)


def scan(filename):
    res = {}
    if not version:
        get_version()
    res['version'] = version
    res['result'] = get_scan_result(filename)
    return res
