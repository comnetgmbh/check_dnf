#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from pathlib import Path
from typing import Any

from cmk.base.cee.plugins.bakery.bakery_api.v1 import FileGenerator, OS, Plugin, register


def get_dnf_files(conf: Any) -> FileGenerator:
    """
    Simple bakery plugin generator for yum

    conf looks like: ('deploy', {'interval': 18060.0})

    """

    # default to no interval - will be filled if set in config
    interval = None
    # flag to decide if plugin should be deployed
    deploy_plugin = False

    if isinstance(conf, dict):
        deploy = conf.get('deploy')
        # backward compatible - first check if 'interval' is still used
        if deploy is None:
            if isinstance(conf.get('interval'), dict):
                try:
                    interval = int(conf.get('interval'))
                except (TypeError, ValueError):
                    interval = None
                deploy_plugin = True
        # existence of 'deploy' dict
        elif isinstance(deploy, dict):
            interval = deploy.get('interval')
            if interval is not None:
                try:
                    interval = int(interval)
                except (TypeError, ValueError):
                    interval = None
            deploy_plugin = True

        if deploy_plugin:
            # only makes sense on Linux so just create for that OS
            yield Plugin(
                base_os=OS.LINUX,
                source=Path('dnf'),
                interval=interval
            )


# register the bakery plugin with its arguments
register.bakery_plugin(
    name='dnf',
    files_function=get_dnf_files
)
