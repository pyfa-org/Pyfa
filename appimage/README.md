## Pyfa As AppImage

Needed for building:

- Linux distro, currently tested is Arch/Manjaro
- make, curl
- GTK3 libraries are needed (`gtk3` for Arch based, `libgtk-3-dev` for debian based)
- patience, first time building wxPython can take about 10 minutes 

Steps:

```sh
cd appimage
mkdir build
cd build
make -f ../Makefile 
```

If everything goes alright, build directory should contain `Pyfa-x86_64.AppImage`.

