from argparse import ArgumentParser, BooleanOptionalAction, Namespace, _SubParsersAction
from logging import getLogger

logger = getLogger(__name__)


def add_subparser(subparsers: _SubParsersAction, **kwargs) -> None:
    from restrun.config.v1.target import GenerateTarget

    parser: ArgumentParser = subparsers.add_parser(
        "generate",
        description="Generate REST API clients.",
        help="Generate REST API clients.",
        **kwargs,
    )

    parser.add_argument(
        "--target",
        nargs="*",
        type=GenerateTarget,
        choices=list(GenerateTarget),
        default=[GenerateTarget.ALL],
        help="target to generate.",
    )

    parser.add_argument(
        "--format",
        action=BooleanOptionalAction,
        help="format generated code. default is [literal]true[/].",
    )

    parser.add_argument(
        "--lint",
        action=BooleanOptionalAction,
        help="lint generated code. default is [literal]true[/].",
    )

    parser.set_defaults(handler=generate_command)


def generate_command(space: "Namespace") -> None:
    from restrun import strcase
    from restrun.config import DEFAULT_CONFIG_FILE, get_path, load
    from restrun.config.v1.target import GenerateTarget, get_targets
    from restrun.generator.context.restrun_context import make_rustrun_context
    from restrun.writer import write_clients, write_resources

    targets = get_targets(space.target)
    config_path = get_path(space.config, DEFAULT_CONFIG_FILE)

    with open(config_path) as file:
        config = load(file)

    base_dir = config_path.parent / strcase.module_name(config.name)
    context = make_rustrun_context(base_dir, config)

    if GenerateTarget.RESOURCE in targets:
        write_resources(base_dir, config, context)

    if GenerateTarget.CLIENT in targets:
        write_clients(base_dir, config, context)

    if space.format if space.format is not None else config.format:
        from restrun.formatter.black import BlackFormatter
        from restrun.formatter.isort import IsortFormatter

        IsortFormatter().format(base_dir)
        BlackFormatter().format(base_dir)

    if space.lint if space.lint is not None else config.lint:
        from restrun.linter.ruff import RuffLinter

        RuffLinter().lint(base_dir)
