from importlib import import_module

router_modules = [
    import_module(".remind", package=__name__),
]
