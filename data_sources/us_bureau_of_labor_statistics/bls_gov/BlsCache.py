import os


class BlsCache:
    @staticmethod
    def get_cache_directory() -> str:
        cache_directory: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cache'))
        return cache_directory
