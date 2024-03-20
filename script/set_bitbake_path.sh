#!/bin/bash

DIR=$PWD

VAR1="main"
VAR2="sub"
VAR3="path"

if [ "$VAR1" = "$2" ]; then
    source $TOPSTDIR/poky/oe-init-build-env $TOPSTDIR/build/tcc8050-main
    echo "source $TOPSTDIR/poky/oe-init-build-env $TOPSTDIR/build/tcc8050-main"
elif [ "$VAR2" = "$2" ]; then
    source $TOPSTDIR/poky/oe-init-build-env $TOPSTDIR/build/tcc8050-sub
    echo "source $TOPSTDIR/poky/oe-init-build-env $TOPSTDIR/build/tcc8050-sub"
elif [ "$VAR3" = "$2" ]; then
	if [ -z "$1" ]; then
		export TOPSTDIR=$DIR
		export TOPSTPOKYDIR=$DIR/poky
		echo "export TOPSTDIR=$DIR"
	else
		export TOPSTDIR=$1
		export TOPSTPOKYDIR=$1/poky
		echo "export TOPSTDIR=$1"
	fi
else
    echo "$2 is not match !"
fi

echo "================================================================="
echo "TOPSTDIR=$TOPSTDIR"
echo "BUILDDIR=$BUILDDIR"

cd $DIR
