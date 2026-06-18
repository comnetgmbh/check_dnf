#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
from collections.abc import Mapping

from cmk.rulesets.v1 import (
    Help,
    Label,
    Title,
)

from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    DefaultValue,
    #    SingleChoice,
    #    SingleChoiceElement,
    #    Integer,
    #    InputHint,
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    FixedValue,
    TimeSpan,
    TimeMagnitude,
    #    SimpleLevels,
    String
)
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic, Title, Help

# default interval in seconds
DEFAULT_INTERVAL = 60.0

def _parameter_form_dnf_bakery() -> Dictionary:
    """
    definition of the parameter form for the DNF bakery plugin
    :return:
    """
    return Dictionary(
        title=Title('DNF Update Check'),
        help_text=Help('This will deploy the agent plugin <tt>DNF</tt>. This will activate the '
                       'check <tt>DNF</tt> on RedHat based hosts and monitor pending normal and security updates.'
                       ),
        elements={
            'deploy': DictElement(
                parameter_form=Dictionary(
                    title=Title('Deploy plugin'),
                    help_text=Help(
                        'Determines how the the <tt>DNF</tt> plugin will run on a deployed agent or disables it on an deployed agent'),
                    elements={
                        'interval': DictElement(
                            parameter_form=TimeSpan(
                                title=Title('Run asynchronously'),
                                label=Label('Interval for collecting data'),
                                help_text=Help(
                                    'Determines how often the plugin will run on a deployed agent.'),
                                displayed_magnitudes=[TimeMagnitude.SECOND,
                                                      TimeMagnitude.MINUTE,
                                                      TimeMagnitude.HOUR,
                                                      TimeMagnitude.DAY],
                                prefill=DefaultValue(DEFAULT_INTERVAL),
                            )
                        )
                    }
                ),
            )
        }
    )


rule_spec_dnf_bakery = AgentConfig(
    title=Title('DNF Update Check'),
    name='dnf',
    parameter_form=_parameter_form_dnf_bakery,
    topic=Topic.OPERATING_SYSTEM,
    help_text=Help('This will deploy the agent plugin <tt>DNF</tt> '
                   'for checking package update status.'),
)
