 #!/bin/bash
source $1 > /dev/null
source $2/oe-init-build-env build/$3 > /dev/null && devtool $4 $5 $6 $7 $8
