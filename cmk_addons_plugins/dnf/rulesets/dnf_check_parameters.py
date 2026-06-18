#!/usr/bin/env python3
"""Checkmk 2.4 rule specification for DNF Update Check"""

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    LevelDirection,
    SimpleLevels,
    ServiceState,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic, HostCondition


def _parameter_form_dnf():
    return Dictionary(
        title=Title("DNF Update Check"),
        elements={
            "reboot_req": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when a reboot is required"),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
                required=False,
            ),
            "normal": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("State when normal updates are available"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(1, 10)),
                ),
                required=False,
            ),
            "security": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("State when security updates are available"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(1, 1)),
                ),
                required=False,
            ),
            "last_update_time_diff": DictElement(
                parameter_form=Integer(
                    title=Title("Max Time since last run update (Default 60 days)"),
                    unit_symbol="days",
                    prefill=DefaultValue(60),
                ),
                required=False
            ),
            "last_update_state": DictElement(
                parameter_form=ServiceState(
                    title=Title("Change State based on last run update (default OK)"),
                    prefill=DefaultValue(ServiceState.OK),
                ),
                required=False,
            ),
        }
    )


rule_spec_dnf = CheckParameters(
    name="dnf",
    title=Title("DNF Update Check Parameters"),
    topic=Topic.OPERATING_SYSTEM,
    parameter_form=_parameter_form_dnf,
    condition=HostCondition(),
)
