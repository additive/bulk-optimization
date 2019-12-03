class WrongInputError(ValueError):
    def __init__(self, message):
        super().__init__(message)
        print()
        print("Use argument `--help` to see how that lib works.")
        print("E.g.: python3 main.py --help")
        print()
