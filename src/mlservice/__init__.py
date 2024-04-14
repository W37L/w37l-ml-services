import importlib.metadata

try:
    __version__ = importlib.metadata.version(__package__) # type: ignore
except (NameError, importlib.metadata.PackageNotFoundError):
    __version__ = "dev"
