class console_stats:
    lenght_of_message = 0
    config = {}

    @classmethod
    def add(cls, **kwargs) -> None:
        cls.config = {**cls.config, **kwargs}

    @classmethod
    def write(cls) -> None:
        print("\b" * cls.lenght_of_message, end="", flush=True)
        message = []
        for k, v in cls.config.items():
            if isinstance(v, float):
                message.append(f"{k}:{v:.2f}")
            else:
                message.append(f"{k}:{v}")
        message = " ".join(message)
        cls.lenght_of_message = len(message)
        print(message, end="")
