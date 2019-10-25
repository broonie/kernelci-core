# Copyright (C) 2019 Collabora Limited
# Author: Lakshmipathi G <lakshmipathi.ganapathi@collabora.com>
#
# This module is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

from kernelci import shell_cmd


def build(name, config, debos_path):

    for arch_type in config.arch_list:
        cmd = 'cd {debos_path} && \
debos \
-t architecture:{arch} -t suite:{name} -t basename:rootfs/{arch} \
-t extra_packages:"{extra_packages}" \
-t extra_packages_remove:"{extra_packages_remove}" \
-t extra_files_remove:"{extra_files_remove}" \
-t script:"{script}" \
rootfs.yaml'.format(
            debos_path=debos_path,
            arch=arch_type,
            name=config.debian_release,
            extra_packages=" ".join(config.extra_packages),
            extra_packages_remove=" ".join(config.extra_packages_remove),
            extra_files_remove=" ".join(config.extra_files_remove),
            script=config.script
            )
        shell_cmd(cmd, ret_code=True)
    return True