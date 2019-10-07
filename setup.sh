#!/bin/bash
alias gitlog='git log --oneline --decorate --graph'
alias cmake_pandora='cmake -DCMAKE_MODULE_PATH=$ROOTSYS/etc/cmake -DPANDORA_MONITORING=ON -DPANDORA_EXAMPLE_CONTENT=OFF -DPANDORA_LAR_CONTENT=ON -DPANDORA_LC_CONTENT=OFF -DCMAKE_CXX_FLAGS="-std=c++17 -Wno-implicit-fallthrough" ..'
alias cmake_larreco='cmake -DCMAKE_MODULE_PATH="$MY_TEST_AREA/PandoraPFA/cmakemodules;$ROOTSYS/etc/cmake" -DPANDORA_MONITORING=ON -DPandoraSDK_DIR=$MY_TEST_AREA/PandoraPFA/ -DPandoraMonitoring_DIR=$MY_TEST_AREA/PandoraPFA/ -DLArContent_DIR=$MY_TEST_AREA/PandoraPFA/ -DCMAKE_CXX_FLAGS=-std=c++17 ..'
export GIT_EDITOR=vim

pandora_setup() {
export MY_TEST_AREA=`pwd`
git clone https://github.com/PandoraPFA/PandoraPFA.git
git clone https://github.com/PandoraPFA/LArReco.git
git clone https://github.com/PandoraPFA/LArMachineLearningData.git
cd PandoraPFA
mkdir build
cd build
cmake_pandora
make -j4 install
cd $MY_TEST_AREA
cd LArReco
mkdir build
cd build
cmake_larreco
make -j4 install
cd $MY_TEST_AREA
cd LArMachineLearningData
export FW_SEARCH_PATH=$FW_SEARCH_PATH:`pwd`
cd ../LArReco/settings
export FW_SEARCH_PATH=$FW_SEARCH_PATH:`pwd`
cd $MY_TEST_AREA
}
