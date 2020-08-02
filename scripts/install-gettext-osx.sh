#!/usr/bin/env bash
gettext --version
HOMEBREW_NO_AUTO_UPDATE=1 brew install gettext
brew link --force gettext