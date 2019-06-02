# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import click

from ..console import CONTEXT_SETTINGS
from ..test import test as test_command
from .start import start
from .stop import stop


@click.command(context_settings=CONTEXT_SETTINGS, short_help='Test an environment')
@click.argument('check')
@click.argument('env')
@click.option(
    '--agent',
    '-a',
    default='6',
    help=(
        'The agent build to use e.g. a Docker image like `datadog/agent:6.5.2`. For '
        'Docker environments you can use an integer corresponding to fields in the '
        'config (agent5, agent6, etc.)'
    ),
)
@click.option('--dev/--prod', help='Whether to use the latest version of a check or what is shipped')
@click.option('--base', is_flag=True, help='Whether to use the latest version of the base check or what is shipped')
@click.option(
    '--env-vars',
    '-e',
    multiple=True,
    help=(
        'ENV Variable that should be passed to the Agent container. '
        'Ex: -e DD_URL=app.datadoghq.com -e DD_API_KEY=123456'
    ),
)
@click.pass_context
def test(ctx, check, env, agent, dev, base, env_vars):
    """Test an environment."""
    ctx.invoke(start, check=check, env=env, agent=agent, dev=dev, base=base, env_vars=env_vars)

    try:
        ctx.invoke(test_command, checks=['{}:{}'.format(check, env)], e2e=True)
    finally:
        ctx.invoke(stop, check=check, env=env)
