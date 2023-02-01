class stats:
    config = {}

    @classmethod
    def add(cls, **kwargs) -> None:
        """overwrites existing keys"""
        cls.config = {**cls.config, **kwargs}

    @classmethod
    def generate_message(cls):
        message = []
        for k, v in cls.config.items():
            if isinstance(v, float):
                message.append(f"{k}:{v:5.2f}")
            elif isinstance(v, int):
                message.append(f"{k}:{v:5d}")
            else:
                message.append(f"{k}:{v}")
        message = "   ".join(message)
        return message


class ConsolePrinter(stats):
    lenght_of_message = 0

    @classmethod
    def write(cls) -> None:
        print("\b" * cls.lenght_of_message, end="", flush=True)
        message = cls.generate_message()
        cls.lenght_of_message = len(message)
        print(message, end="")
