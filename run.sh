#!/bin/sh

uv cache clean && uv tool uninstall omurtag && uv tool install .
