import glob
from argparse import ArgumentParser, Namespace
from enum import Enum
from logging import getLogger
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Annotated,
    Iterable,
    NotRequired,
    Type,
    TypedDict,
    cast,
)

from typer import Option

from restrun import strcase
from restrun.config import DEFAULT_CONFIG_FILENAME, Config, load
from restrun.core.request import (
    DeleteRequest,
    GetRequest,
    PatchRequest,
    PostRequest,
    PutRequest,
    Request,
    get_method,
)
from restrun.exception import DuplicateRequestTypeError, RequestURLInvalidError
from restrun.generator import (
    ClassInfo,
    find_classes_from_code,
    is_auto_generated,
)
from restrun.generator.context.resource import ResourceContext
from restrun.generator.context.restrun import RestrunContext
from restrun.generator.resource_module import ResourceModuleGenerator

if TYPE_CHECKING:
    from argparse import _SubParsersAction

logger = getLogger(__name__)


class GenerateTarget(Enum):
    ALL = "all"
    CLIENT = "client"
    RESOURCE = "resource"

    def __str__(self) -> str:
        return self.value


class GenerateArgs(TypedDict):
    target: NotRequired[
        Annotated[
            GenerateTarget | list[GenerateTarget],
            Option(default="all"),
        ]
    ]


def add_subparser(subparsers: "_SubParsersAction", **kwargs) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "generate",
        help="Generate REST API clients.",
        **kwargs,
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=Path(DEFAULT_CONFIG_FILENAME),
        help="Path to config file.",
    )

    parser.add_argument(
        "--target",
        nargs="*",
        type=GenerateTarget,
        choices=list(GenerateTarget),
        default=[GenerateTarget.ALL],
        help="Target to generate.",
    )

    parser.set_defaults(handler=generate_command)


def generate_command(space: Namespace) -> None:
    targets = get_targets(space.target)
    config_path: Path = space.config

    with open(config_path, "br") as file:
        config = load(file)

    base_dir = config_path.parent / strcase.module_name(config.name)
    context = make_rustrun_context(base_dir, config)

    resource_contexts = make_resource_contexts(base_dir, context)

    if GenerateTarget.RESOURCE in targets:
        write_resources(base_dir, context, resource_contexts)

    if GenerateTarget.CLIENT in targets:
        write_clients(base_dir, context)

    if config.format:
        from restrun.formatter.black import BlackFormatter

        BlackFormatter().format(base_dir)

    if config.lint:
        from restrun.linter.ruff import RuffLinter

        RuffLinter().lint(base_dir)


def get_targets(
    targets: Iterable[GenerateTarget],
) -> set[GenerateTarget]:
    for target in targets:
        if target == GenerateTarget.ALL:
            return set([t for t in GenerateTarget if t != GenerateTarget.ALL])

    return set(targets)


def make_resource_contexts(
    base_dir: Path, context: RestrunContext
) -> list[ResourceContext]:
    resource_contexts = []

    for resource_dir in (base_dir / "resources").iterdir():
        if not resource_dir.is_dir():
            continue

        resource_context = make_resource_context(resource_dir, context)
        if (resource_context) is not None:
            resource_contexts.append(resource_context)

    return resource_contexts


def make_resource_context(
    resource_dir: Path, context: RestrunContext
) -> ResourceContext | None:
    request_class_infos: dict[Type[Request], list[ClassInfo[Request]]] = {
        GetRequest: [],
        PostRequest: [],
        PutRequest: [],
        PatchRequest: [],
        DeleteRequest: [],
    }

    for request_file in resource_dir.iterdir():
        if (
            not request_file.is_file()
            or request_file.suffix != ".py"
            or request_file.name == "__init__.py"
        ):
            continue

        requests_map = find_classes_from_code(
            request_file,
            GetRequest,
            PostRequest,
            PutRequest,
            PatchRequest,
            DeleteRequest,
        )

        for request_type in [GetRequest, PostRequest, PutRequest, PatchRequest]:
            request_class_infos[request_type].extend(requests_map[request_type])
    resource_context = ResourceContext(name=resource_dir.name, url="", method_map={})
    for request_type, class_infos in request_class_infos.items():
        match len(class_infos):
            case 0:
                continue
            case 1:
                method = get_method(request_type)
                resource_context.method_map[method] = class_infos[0]  # type: ignore
            case _:
                raise DuplicateRequestTypeError(
                    get_method(request_type),
                    request_type.url,
                    class_infos,
                )
    urls = set(
        cast(ClassInfo[Request], request).class_type.url
        for request in resource_context.method_map.values()
    )

    match len(urls):
        case 0:
            return None
        case 1:
            return resource_context
        case _:
            raise RequestURLInvalidError(resource_context.methods)


def make_rustrun_context(base_dir: Path, config: Config) -> RestrunContext:
    client_mixins_dir = base_dir / "client" / "mixins"

    client_mixins: list[ClassInfo] = []
    real_client_mixins: list[ClassInfo] = []
    mock_client_mixins: list[ClassInfo] = []

    if client_mixins_dir.exists():
        from restrun.core.client import (
            RestrunClientMixin,
            RestrunMockClientMixin,
            RestrunRealClientMixin,
        )

        for pyfile in glob.glob(str(client_mixins_dir / "*.py")):
            pypath = Path(pyfile)

            mixins_map = find_classes_from_code(
                pypath,
                RestrunClientMixin,
                RestrunRealClientMixin,
                RestrunMockClientMixin,
            )
            client_mixins.extend(mixins_map[RestrunClientMixin])
            real_client_mixins.extend(mixins_map[RestrunRealClientMixin])
            mock_client_mixins.extend(mixins_map[RestrunMockClientMixin])

    return RestrunContext(
        config=config,
        client_prefix=config.name,
        client_mixins=client_mixins,
        real_client_mixins=real_client_mixins,
        mock_client_mixins=mock_client_mixins,
    )


def write_clients(base_dir: Path, context: RestrunContext) -> None:
    from restrun.generator.client import ClientGenerator
    from restrun.generator.client_mixins_module import ClientMixinsModuleGenerator
    from restrun.generator.client_module import ClientModuleGenerator
    from restrun.generator.mock_client import MockClientGenerator
    from restrun.generator.real_client import RealClientGenerator

    for filename, generator in [
        ("client.py", ClientGenerator()),
        ("real_client.py", RealClientGenerator()),
        ("mock_client.py", MockClientGenerator()),
        ("__init__.py", ClientModuleGenerator()),
        (Path("mixins") / "__init__.py", ClientMixinsModuleGenerator()),
    ]:
        filepath = base_dir / "client" / filename

        if not filepath.exists() or is_auto_generated(filepath):
            code = generator.generate(context)
            with open(filepath, "w") as file:
                file.write(code)


def write_resources(
    base_dir: Path,
    restrun_context: RestrunContext,
    resource_contexts: list[ResourceContext],
) -> None:
    from restrun.generator.resources_module import ResourcesModuleGenerator

    for resource_context in resource_contexts:
        code = ResourceModuleGenerator().generate(restrun_context, resource_context)
        with open(
            base_dir / "resources" / resource_context.name / "__init__.py", "w"
        ) as file:
            file.write(code)

    code = ResourcesModuleGenerator().generate(restrun_context)
    with open(base_dir / "resources" / "__init__.py", "w") as file:
        file.write(code)
