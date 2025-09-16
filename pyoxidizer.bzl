def make_exe():
    dist = dists.get_python_distribution(
        python_version="3.11",
        flavor="standalone_static",
    )

    python_config = dist.make_python_config()
    python_config.run_command = "print('hello world')"


    exe = dist.to_python_executable(
        name="pyfa_minimal",
        config=python_config,
    )

    return exe

def make_install():
    install = default_install_maker()
    install.add_executable(make_exe())
    return install

register_target("exe", make_exe)
register_target("install", make_install, default=True)
