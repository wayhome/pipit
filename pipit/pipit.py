# -*- coding: utf-8 -*-
import os
import sys
import shutil
import tempfile

from pip.download import PipSession
from pip.index import PackageFinder, FormatControl
from pip.req import InstallRequirement, RequirementSet
from pip.wheel import WheelBuilder, WheelCache, get_entrypoints, move_wheel_files

from .script import py_script_template, script_template, gen_script


class EditInstallRequirement(InstallRequirement):

    def archive(self, build_dir):
        if self.editable:
            return
        else:
            return InstallRequirement.archive(self, build_dir)


def build(index, download_dir):
    """build wheels for pipit"""
    target = os.path.join(os.getcwd(), "target")
    download_dir = download_dir or os.path.join(target, "download")
    wheel_download_dir = os.path.join(target, "wheels")
    bin_dir = os.path.join(target, "bin")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)
    try:
        tempdir = tempfile.mkdtemp()
        session = PipSession()
        requirement_set = _make_requirement_set(session, tempdir, download_dir,
                                                wheel_download_dir)
        finder = PackageFinder(find_links=[wheel_download_dir],
                               index_urls=[index],
                               session=session)
        builder = WheelBuilder(requirement_set, finder)
        builder.build()
        # _install_scripts(requirement_set, bin_dir)
        _install_wheels(requirement_set, target)
    finally:
        shutil.rmtree(tempdir, ignore_errors=True)


def _install_wheels(requirement_set, target):
    wheel_download_dir = os.path.join(target, "wheels")
    lib_dir = os.path.join(target, "lib")
    scheme = {'purelib': lib_dir, 'platlib': lib_dir}
    for req in requirement_set.requirements.values():
        if req.editable:
            pass
        else:
            move_wheel_files(req.name, req, wheel_download_dir, scheme=scheme)


def _make_requirement_set(session, tempdir, download_dir, wheel_download_dir):
    """
    construction a RequirementSet
    """
    format_control = FormatControl(set(), set())
    wheel_cache = WheelCache(os.path.join(tempdir, ".cache"), format_control)
    requirement_set = RequirementSet(
        build_dir=os.path.join(tempdir, 'build'),
        src_dir=os.path.join(tempdir, 'src'),
        ignore_installed=True,
        download_dir=download_dir,
        wheel_download_dir=wheel_download_dir,
        wheel_cache=wheel_cache,
        session=session,
    )
    try:
        requirement_set.add_requirement(
            EditInstallRequirement.from_editable("."),
        )
    except Exception as e:
        sys.exit(e)
    if os.path.exists("requirements.txt"):
        with open("requirements.txt") as f:
            for line in f:
                requirement_set.add_requirement(
                    InstallRequirement.from_line(line),
                )
    return requirement_set


def _project_info(requirement_set):
    """
    get project info from requirement_set
    :param requirement_set: `pip.req.RequirementSet`
    :return: (paths, entry_points): project sys.path's string and entry_points
    """
    paths = ["."]
    editable_req = None
    for req in requirement_set.requirements.values():
        if req.editable:
            editable_req = req
            continue
        else:
            path = os.path.join("target/wheels", req.link.filename)
            paths.append(path)
    path_strings = '\n'.join(["    join(base, '{path}'),".format(path=p)
                             for p in paths])
    entry_points_path = editable_req.egg_info_path("entry_points.txt")
    entry_points = get_entrypoints(entry_points_path)[0]
    return path_strings, entry_points


def _install_scripts(requirement_set, bin_dir):
    """
    install python interpreter and console_script into bin_dir
    """
    path_strings, entry_points = _project_info(requirement_set)
    # generate python interpreter
    content = py_script_template.format(path=path_strings)
    interpreter = os.path.join(bin_dir, "python")
    gen_script(interpreter, content)
    # generate console_scripts
    for name, entrypoint in entry_points.items():
        script_path = os.path.join(bin_dir, name)
        module = entrypoint.split(":")[0]
        function = entrypoint.replace(":", ".")
        content = script_template.format(path=path_strings, module=module,
                                         function=function)
        gen_script(script_path, content)


if __name__ == "__main__":
    build()
