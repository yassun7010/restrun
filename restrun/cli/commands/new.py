from argparse import ArgumentParser, Namespace, _SubParsersAction


def add_subparser(subparsers: _SubParsersAction, **kwargs) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "new",
        description="Create a new REST API client.",
        help="Create a new REST API client.",
        **kwargs,
    )

    parser.add_argument(
        "client",
        type=str,
        help="client name.",
    )

    parser.set_defaults(handler=new_command)


def new_command(space: Namespace) -> None:
    client_name = space.client
    print(f"Create a new REST API client: {client_name}")
