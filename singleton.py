class Singleton:

    INSTANCE = None

    def __new__(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = super().__new__(cls)
        return cls.INSTANCE
