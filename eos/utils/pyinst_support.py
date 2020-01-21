"""
Slightly modified version of function taken from here:
https://github.com/pyinstaller/pyinstaller/issues/1905#issuecomment-525221546
"""


import pkgutil


def iterNamespace(name, path):
    """Pyinstaller-compatible namespace iteration.

    Yields the name of all modules found at a given Fully-qualified path.

    To have it running with pyinstaller, it requires to ensure a hook inject the
    "hidden" modules from your plugins folder inside the executable:

    - if your plugins are under the ``myappname/pluginfolder`` module
    - create a file ``specs/hook-<myappname.pluginfolder>.py``
    - content of this file should be:

        .. code-block:: python

            from PyInstaller.utils.hooks import collect_submodules
            hiddenimports = collect_submodules('<myappname.pluginfolder>')
    """
    prefix = name + "."
    for p in pkgutil.iter_modules(path, prefix):
        yield p[1]

    # special handling when the package is bundled with PyInstaller 3.5
    # See https://github.com/pyinstaller/pyinstaller/issues/1905#issuecomment-445787510
    toc = set()
    for importer in pkgutil.iter_importers(name.partition(".")[0]):
        if hasattr(importer, 'toc'):
            toc |= importer.toc
    for name in toc:
        if name.startswith(prefix):
            yield name
