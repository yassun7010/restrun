from argparse import ArgumentParser, Namespace, _SubParsersAction


def add_subparser(subparsers: _SubParsersAction, **kwargs) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "new",
        description="Create new [restrun]RESTRUN[/] project.",
        help="Create new RESTRUN project.",
        **kwargs,
    )

    parser.add_argument(
        "project",
        type=str,
        help="project name.",
    )

    parser.set_defaults(handler=new_command)


def new_command(space: Namespace) -> None:
    project_name = space.project
    print(f"Create a new RESTRUN project: {project_name}")
