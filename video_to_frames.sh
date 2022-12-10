#!/bin/bash

mplayer -vf scale=-2:${2:-84} -vo png:outdir=frames $1 -nosound