#!/usr/bin/env bash
brew link --force gettext
find locale/ -type f -name "*.po" -exec msgen "{}" -o "{}" \;