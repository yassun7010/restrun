import sys

from . import app


def main() -> None:
    try:
        app.run()

    except Exception:
        exit(1)

    finally:
        sys.stdout.flush()


if __name__ == "__main__":
    main()
