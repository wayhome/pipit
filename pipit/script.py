#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

header_template = '''\
#!/usr/bin/env python
import os
import sys

join = os.path.join
bin_dir = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
target_dir = os.path.dirname(bin_dir)
base = os.path.dirname(target_dir)

sys.path[0:0] = [
{path}
]
'''

py_script_template = header_template + '''\

_interactive = True
if len(sys.argv) > 1:
    _options, _args = __import__("getopt").getopt(sys.argv[1:], 'ic:m:')
    _interactive = False
    for (_opt, _val) in _options:
        if _opt == '-i':
            _interactive = True
        elif _opt == '-c':
            exec(_val)
        elif _opt == '-m':
            sys.argv[1:] = _args
            _args = []
            __import__("runpy").run_module(
                _val, {{}}, "__main__", alter_sys=True)

    if _args:
        sys.argv[:] = _args
        __file__ = _args[0]
        del _options, _args
        with open(__file__, 'U') as __file__f:
            exec(compile(__file__f.read(), __file__, "exec"))

if _interactive:
    del _interactive
    __import__("code").interact(banner="", local=globals())
'''

script_template = header_template + '''\

import {module}


if __name__ == '__main__':
    sys.exit({function}())
'''


def gen_script(filename, content):
    with open(filename, "w") as f:
        f.write(content)
    os.chmod(filename, 0755)
