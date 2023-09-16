from restrun.cli import App


def main() -> None:
    try:
        App.run()
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
