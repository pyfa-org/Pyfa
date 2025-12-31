# The following is a build configuration for the PyOxidizer tool.
# It is used to build self-contained executables of Python applications.
# For more info, see: https://pyoxidizer.readthedocs.io/en/stable/

def make_exe():
    """
    Defines the executable that will be built.
    """
    dist = dists.get_python_distribution(
        python_version="3.11",
        flavor="standalone_static",
    )

    # Configure the Python interpreter.
    python_config = dist.make_python_config()
    python_config.run_module = "pyfa"
    # To run GUI apps on macOS, we need to run in a specific mode.
    python_config.macos_bundle_info_plist = {
        "CFBundleIdentifier": "org.pyfa.pyfa",
        "CFBundleName": "pyfa",
        "CFBundleExecutable": "pyfa",
    }


    # Create the executable definition.
    exe = dist.to_python_executable(
        name="pyfa",
        config=python_config,
    )

    # Add Python source files from the project.
    # We recursively glob for all .py files and add them.
    exe.add_python_resources(exe.find_python_resources(
        search_path=["."],
        exclude_matches=[
            "tests/*",
            "scripts/*",
            "_development/*",
            "dist_assets/*",
            "*.spec",
            "tox.ini",
        ]
    ))

    # Add data files. Based on `pyfa.spec`.
    exe.add_data_files([
        ("imgs", "imgs"),
        ("locale", "locale"),
        ("staticdata", "staticdata"),
        ("cacert.pem", "cacert.pem"),
        ("LICENSE", "LICENSE"),
        ("version.yml", "version.yml"),
    ])

    return exe

def make_install():
    """
    Defines what happens during `pyoxidizer install`.
    """
    install = default_install_maker()
    install.add_executable(make_exe())
    return install

# Register our targets. The `default=True` means `pyoxidizer build` will
# run the `install` target by default.
register_target("exe", make_exe)
register_target("install", make_install, default=True)
