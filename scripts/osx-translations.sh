#!/usr/bin/env bash
find locale/ -type f -name "*.po" -exec msgen "{}" -o "{}" \;
