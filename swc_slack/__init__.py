from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("swc-slack")
except PackageNotFoundError:
    # package is not installed
    pass
