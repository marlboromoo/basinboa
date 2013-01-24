#!/usr/bin/env bash

find ./ | grep -i pyc$ |xargs -i rm {}
