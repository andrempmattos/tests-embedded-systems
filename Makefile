TARGET=tests-embedded-systems
CCS_WORKSPACE=$(HOME)/workspace_v7

DEV_CONFIG_FILE=targetConfigs/MSP430F6659.ccxml
IMG=Debug/$(TARGET).out

CC=$(HOME)/ti/ccsv7/eclipse/./ccstudio
FL=$(HOME)/ti/uniflash_6.2.0/deskdb/content/TICloudAgent/linux/ccs_base/DebugServer/bin/./DSLite


all:
	$(CC) -noSplash -data $(CCS_WORKSPACE) -application com.ti.ccstudio.apps.projectBuild -ccs.projects $(TARGET)

import:
	$(CC) -noSplash -data $(CCS_WORKSPACE) -application com.ti.ccstudio.apps.projectImport -ccs.overwrite -ccs.location .

flash:
	$(FL) flash -c $(DEV_CONFIG_FILE) -s VerifyAfterProgramLoad=2 -e -f -v "$(IMG)" -n 0 -u

clean:
	$(CC) -noSplash -data $(CCS_WORKSPACE) -application com.ti.ccstudio.apps.projectBuild -ccs.projects $(TARGET) -ccs.clean
