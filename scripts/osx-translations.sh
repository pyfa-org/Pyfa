#!/usr/bin/env bash
brew install gettext
find locale/ -type f -name "*.po" -exec msgen "{}" -o "{}" \;