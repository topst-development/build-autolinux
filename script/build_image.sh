#!/bin/bash
source $1 > /dev/null
source $2/oe-init-build-env build/$3 > /dev/null && bitbake $4 $5 $6 $7
