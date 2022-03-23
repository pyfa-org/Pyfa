APPIMAGETOOL:=appimagetool-x86_64.AppImage
APPIMAGETOOL_URL:=https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage

PYTHON_APPIMAGE=python3.8.12-cp38-cp38-manylinux2014_x86_64.AppImage
PYTHON_APPIMAGE_URL=https://github.com/niess/python-appimage/releases/download/python3.8/$(PYTHON_APPIMAGE)

DEPLOY_DIR=AppDir/opt/pyfa

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
PYFA_DIR:=$(realpath $(ROOT_DIR)/..)
EVE_DB:=$(DEPLOY_DIR)/eve.db

# Relative to Pyfa/ dir
PROJECT_FILES=README.md LICENSE eos graphs gui imgs locale scripts service staticdata utils version.yml config.py db_update.py pyfa.py
PROJECT_SOURCES=$(patsubst %, $(DEPLOY_DIR)/%, $(PROJECT_FILES))

# Just so the final appimage is rebuilt when these change
APPIMAGE_FILES=AppRun org.pyfa.pyfa.appdata.xml pyfa pyfa.desktop
APPIMAGE_SOURCES=$(patsubst %, $(ROOT_DIR)/%, $(APPIMAGE_FILES))


Pyfa-x86_64.AppImage: $(PROJECT_SOURCES) | $(APPIMAGETOOL) static deps $(EVE_DB)
	./$(APPIMAGETOOL) AppDir

$(EVE_DB): $(PYFA_DIR)/eos $(PYFA_DIR)/db_update.py deps
	AppDir/usr/bin/python -s $(DEPLOY_DIR)/db_update.py

.PHONY: deps
deps: $(DEPLOY_DIR) $(PYFA_DIR)/requirements.txt 
	AppDir/usr/bin/python -s -m pip install -U pip setuptools wheel
	AppDir/usr/bin/python -s -m pip install -r $(PYFA_DIR)/requirements.txt

.PHONY: static
static: $(DEPLOY_DIR) $(APPIMAGE_SOURCES)
	cp $(ROOT_DIR)/AppRun AppDir/
	cp $(ROOT_DIR)/pyfa.desktop AppDir/
	cp $(ROOT_DIR)/pyfa.desktop AppDir/usr/share/applications/
	cp $(ROOT_DIR)/org.pyfa.pyfa.appdata.xml AppDir/usr/share/metainfo/
	chmod +x $(ROOT_DIR)/pyfa && cp $(ROOT_DIR)/pyfa AppDir/usr/bin/

# Rule to copy generated PROJECT_SOURCES
$(DEPLOY_DIR)/%: $(PYFA_DIR)/% $(DEPLOY_DIR)
	cp -r $< $@

# Prepare Python base AppImage, stripping Python metadata
$(DEPLOY_DIR): $(PYTHON_APPIMAGE)
	./$(PYTHON_APPIMAGE) --appimage-extract
	mv squashfs-root AppDir
	rm AppDir/python*.desktop
	rm AppDir/usr/share/applications/*.desktop
	rm AppDir/usr/share/metainfo/*.appdata.xml
	mkdir -p $(DEPLOY_DIR)

$(PYTHON_APPIMAGE):
	curl -LO $(PYTHON_APPIMAGE_URL)
	chmod +x $(PYTHON_APPIMAGE)


$(APPIMAGETOOL): 
	curl -LO $(APPIMAGETOOL_URL)
	chmod +x $(APPIMAGETOOL)

clean:
	rm -rf AppDir

clean-all: clean
	rm -rf *.AppImage