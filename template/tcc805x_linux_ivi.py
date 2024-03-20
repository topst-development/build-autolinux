#!/usr/bin/python
import os

# Supported MACHINEs
Machines = ['tcc8050-main', 'tcc8050-sub', 'tcc8050-cr5']

# Manifests versions
Manifests = [['tcc8050_linux_ivi_tost_0.1.0.xml','2022/04/08']]

# Manifest URLs
ManifestsURL = 'ssh://git@github.com/topst-development/manifest.git'

MainImages = ['automotive-linux-platform-image']

SubImages = ['telechips-subcore-image']

MainBuildScript = 'poky/meta-telechips/meta-ivi/ivi-build.sh'

SubBuildScript = 'poky/meta-telechips/meta-subcore/subcore-build.sh'

MainFeatures = []

SubFeatures = []