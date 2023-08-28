from restrun import cli


def main() -> None:
    try:
        cli.App.run()
    except Exception:
        exit(1)


if __name__ == "__main__":
    main()
