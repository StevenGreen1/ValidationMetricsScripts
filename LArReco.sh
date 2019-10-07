#!/bin/bash

source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh

setup gcc v7_3_0 -f Linux64bit+3.10-2.17
setup git v2_4_6 -f Linux64bit+3.10-2.17
setup python v2_7_13d -f Linux64bit+3.10-2.17

setup eigen v3_3_3
setup root v6_16_00 -f Linux64bit+3.10-2.17 -q e17:prof

export JOB_NAME="ProtoDUNE_RecoMetrics"
export MONTH="October"
export YEAR="2019"
export FW_SEARCH_PATH=${FW_SEARCH_PATH}:"/usera/sg568/LAr/Jobs/protoDUNE/${YEAR}/${MONTH}/${JOB_NAME}/Condor/LArReco/settings":"/usera/sg568/LAr/Jobs/protoDUNE/${YEAR}/${MONTH}/${JOB_NAME}/Condor/LArMachineLearningData"
export PD_GEOEMTRY="/usera/sg568/LAr/Jobs/protoDUNE/${YEAR}/${MONTH}/${JOB_NAME}/Condor/LArReco/geometry/PandoraGeometry_ProtoDUNE_MCC12.xml"

/usera/sg568/LAr/Jobs/protoDUNE/${YEAR}/${MONTH}/${JOB_NAME}/Condor/LArReco/bin/PandoraInterface -r Full -i $1 -e $2 -g ${PD_GEOEMTRY}

