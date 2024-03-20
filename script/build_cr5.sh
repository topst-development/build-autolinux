#!/bin/bash

if [ ! -d ../cr5-bsp/sources/build/tcc805x/gcc ]; then
	pushd cr5-bsp/sources/build/tcc805x/gcc
	make $1
	popd
fi
