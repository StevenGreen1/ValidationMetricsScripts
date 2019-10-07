# -*- coding: utf-8 -*-
import os
import re
import random
import dircache
import sys
import datetime

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ''


#===========================
# Input Variables
#===========================

settingsLocation = os.path.join(os.getcwd(), 'Settings')

eventsToRun = [
#                 { 'JobName': 'ProtoDUNE_RecoMetrics',
#                   'PandoraSettingsFiles': {'Master' : 'PandoraSettings_Master_ProtoDUNE.xml'},
#                   'EventType': "Beam_Cosmics",
#                   'EventsPerFile' : 50,
#                   'Momentum':  [2,3,6,7],
#                   'DetectorModel': 'ProtoDUNE-SP',
#                   'Sample': 'mcc12_Pndr',
#                   'LArSoftVersion': 'v08_30_02',
#                   'SpaceChargeEffect': ['SpaceCharge','NoSpaceCharge'],
#                   'AnalysisTag': 1
#                 }
                 { 'JobName': 'ProtoDUNE_RecoMetrics',
                   'PandoraSettingsFiles': {'Master' : 'PandoraSettings_Master_ProtoDUNE.xml'},
                   'EventType': "Beam_Cosmics",
                   'EventsPerFile' : 10,
                   'Momentum':  [1,2,3,6,7],
                   'DetectorModel': 'ProtoDUNE-SP',
                   'Sample': 'mcc11_Pndr',
                   'LArSoftVersion': 'larsoft_v07_13_00',
                   'SpaceChargeEffect': ['SpaceCharge','NoSpaceCharge'],
                   'AnalysisTag': 1
                 }
              ]

#===========================

now = datetime.datetime.now()
jobList = ''

for eventSelection in eventsToRun:
    jobName = eventSelection['JobName']
    eventType = eventSelection['EventType']
    detectorModel = eventSelection['DetectorModel']
    sample = eventSelection['Sample']
    larsoftVersion = eventSelection['LArSoftVersion']
    tag = eventSelection['AnalysisTag']
    pandoraSetttingsFiles = eventSelection['PandoraSettingsFiles']

    for momenta in eventSelection['Momentum']:
        for spaceChargeEffect in eventSelection['SpaceChargeEffect']:
            pndrPath = '/r06/dune/protoDUNE/' + sample + '/' + detectorModel + '/LArSoft_Version_' + larsoftVersion + '/' + eventType + '/' + str(momenta) + 'GeV/' + spaceChargeEffect + '/'
            pndrFormat = sample + '_' + detectorModel + '_LArSoft_Version_' + larsoftVersion + '_' + eventType + '_Momentum_' + str(momenta) + 'GeV_(.*?).pndr'

            settingsPath = '/r07/dune/sg568/LAr/Jobs/protoDUNE/' + str(now.year) + '/' + now.strftime("%B") + '/' + jobName + '/AnalysisTag' + str(tag) + '/' + sample + '/' + eventType + '/' + str(momenta) + 'GeV/' + spaceChargeEffect + '/PandoraSettings'
            rootFilePath = '/r07/dune/sg568/LAr/Jobs/protoDUNE/' + str(now.year) + '/' + now.strftime("%B") + '/' + jobName + '/AnalysisTag' + str(tag) + '/' + sample + '/' + eventType + '/' + str(momenta) + 'GeV/' + spaceChargeEffect + '/RootFiles'

            if not os.path.exists(settingsPath):
                os.makedirs(settingsPath)

            if not os.path.exists(rootFilePath):
                os.makedirs(rootFilePath)

            baseContent = {}

            for settingsName, settingsFile in pandoraSetttingsFiles.items():
                baseFile = os.path.join(settingsLocation, settingsFile)
                base = open(baseFile,'r')
                baseContent[settingsName] = base.read()
                base.close()

            fileDirectory = pndrPath
            allFilesInDirectory = dircache.listdir(fileDirectory)
            inputFileExt = 'pndr'

            allFiles = []
            allFiles.extend(allFilesInDirectory)
            allFiles[:] = [ item for item in allFiles if re.match('.*\.'+inputFileExt+'$',item.lower()) ]
            allFiles.sort()

            nFiles = 0
            if allFiles:
                nFiles = len(allFiles)

            for idx in range (nFiles):
                nextFile = allFiles.pop(0)
                matchObj = re.match(pndrFormat, nextFile, re.M|re.I)

                if matchObj:
                    identifier = matchObj.group(1)

                    newSettingsName = {}
                    for settingsName in pandoraSetttingsFiles:
                        newSettingsName[settingsName] = os.path.splitext(pandoraSetttingsFiles[settingsName])[0] + '_' + jobName + '_' + str(identifier) + '.xml'

                    for settingsName, settingsFileContent in baseContent.items():
                        newContent = settingsFileContent
                        settingsFullPath = os.path.join(settingsPath, newSettingsName[settingsName])

                        # This is where to modify the files
                        if settingsName == 'Master':
                            newSettingsName = 'PandoraSettings_Master_' + jobName + '_' + str(identifier) + '.xml'
                            settingsFullPath = os.path.join(settingsPath, newSettingsName)
                            rootFileFullPath = os.path.join(rootFilePath, jobName + '_Job_Number_' + str(identifier) + '.root')
                            rootFileFullPathHierarchy = os.path.join(rootFilePath, jobName + '_Hierarchy_Job_Number_' + str(identifier) + '.root')
                            newContent = re.sub('Validation.root', rootFileFullPath, newContent)
                            newContent = re.sub('ValidationHierarchy.root', rootFileFullPathHierarchy, newContent)
                            jobList += settingsFullPath + ' ' + os.path.join(pndrPath,nextFile)
                            jobList += '\n'

                        file = open(settingsFullPath,'w')
                        file.write(newContent)
                        file.close()

                        del newContent

runFilePath = os.getcwd()
file = open(runFilePath + '/CondorRunFile.txt','w')
file.write(jobList)
file.close()
