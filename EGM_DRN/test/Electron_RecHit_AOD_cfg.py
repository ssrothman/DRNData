import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from Configuration.ProcessModifiers.enableSonicTriton_cff import enableSonicTriton
process = cms.Process("Demo",enableSonicTriton)

process.load("HeterogeneousCore.SonicTriton.TritonService_cff")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.load("Configuration.StandardSequences.GeometryRecoDB_cff")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(5000) )
#process.options.numberOfThreads = cms.untracked.uint32(4)
#process.options.numberOfStreams = cms.untracked.uint32(8)
process.options.SkipEvent = cms.untracked.vstring('ProductNotFound')

process.TritonService.verbose = True
process.TritonService.fallback.verbose = True
process.TritonService.fallback.useDocker = False
process.TritonService.fallback.useGPU = False


process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)

options = VarParsing.VarParsing('standard')

options.register('inputFile',
        "~/",
        VarParsing.VarParsing.multiplicity.singleton,
        VarParsing.VarParsing.varType.string,
        "File containing a list of the EXACT location of the output file  (default = ~/)"
        )


options.parseArguments()
options.inputFile = 'root://eoscms//' + options.inputFile
print(options.inputFile)
process.source = cms.Source("PoolSource",
                                # replace 'myfile.root' with the source file you want to use
                                fileNames = cms.untracked.vstring(
#'root://cms-xrd-global.cern.ch///store/mc/RunIISummer19UL18RECO/DYJetsToEE_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/AODSIM/NoPUECAL4BX25_106X_upgrade2018_realistic_v11_Ecal4-v2/20000/D2F029DD-CACC-AA48-BC51-D1987DD92E26.root'
"file:testfile.root"
#'root://cms-xrd-global.cern.ch///store/mc/RunIISummer19UL18RECO/GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v2/10000/755C8490-4B61-E648-8984-4ED4CF3D3873.root'

                )
                            )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v11_Ecal5', '')


from CondCore.DBCommon.CondDBSetup_cfi import *
process.GlobalTag = cms.ESSource("PoolDBESSource",
                               CondDBSetup,
                               connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
                               globaltag = cms.string('106X_upgrade2018_realistic_v11_Ecal4'),
			       toGet = cms.VPSet(


                cms.PSet(record = cms.string("GBRDWrapperRcd"),
                        tag = cms.string("DoubleElectron_FlatPt-1To300_FlatPU0to70_ECAL5_106X_upgrade2018_realistic_v11_L1v1-v2"),
                        label = cms.untracked.string("pfscecal_EBCorrection_offline_v2"),
                        connect = cms.string("sqlite_file:DBFiles/correctedECALSampleDBFile_EB.db")
                        ),

                cms.PSet(record = cms.string("GBRDWrapperRcd"),
                        tag = cms.string("DoubleElectron_FlatPt-1To300_FlatPU0to70_ECAL5_106X_upgrade2018_realistic_v11_L1v1-v2"),
                        label = cms.untracked.string("pfscecal_EBUncertainty_offline_v2"),
                        connect = cms.string("sqlite_file:DBFiles/correctedECALSampleDBFile_EB.db")
                        ),


                cms.PSet(record = cms.string("GBRDWrapperRcd"),
                        tag = cms.string("DoubleElectron_FlatPt-1To300_FlatPU0to70_ECAL5_106X_upgrade2018_realistic_v11_L1v1-v2"),
                        label = cms.untracked.string("pfscecal_EECorrection_offline_v2"),
                        connect = cms.string("sqlite_file:DBFiles/correctedECALSampleDBFile_EE.db")
                        ),


                cms.PSet(record = cms.string("GBRDWrapperRcd"),
                        tag = cms.string("DoubleElectron_FlatPt-1To300_FlatPU0to70_ECAL5_106X_upgrade2018_realistic_v11_L1v1-v2"),
                        label = cms.untracked.string("pfscecal_EEUncertainty_offline_v2"),
                        connect = cms.string("sqlite_file:DBFiles/correctedECALSampleDBFile_EE.db")
                        )



                        )

                              )



process.DRNProducerEB = cms.EDProducer('SCEnergyCorrectorDRNProducer',
   correctorCfg = cms.PSet(
     ecalRecHitsEE = cms.InputTag('reducedEcalRecHitsEE'),
     ecalRecHitsEB = cms.InputTag('reducedEcalRecHitsEB'),
     rhoFastJet = cms.InputTag("fixedGridRhoAll"),
   ),
   inputSCs = cms.InputTag('particleFlowSuperClusterECAL','particleFlowSuperClusterECALBarrel'),
   Client = cms.PSet(
       mode = cms.string("Async"),
        preferredServer = cms.untracked.string(""),
        timeout = cms.untracked.uint32(10),
        modelName = cms.string("EGM_DRN"),
        modelVersion = cms.string(""),
        modelConfigPath = cms.FileInPath("DRNDeployment/EGM_DRN/data/models/{}/config.pbtxt".format('EGM_DRN')),
        verbose = cms.untracked.bool(True),
        allowedTries = cms.untracked.uint32(1),
        useSharedMemory = cms.untracked.bool(True),
        compression = cms.untracked.string(""),
    ),
 )


process.DRNProducerEE = cms.EDProducer('SCEnergyCorrectorDRNProducer',
   correctorCfg = cms.PSet(
     ecalRecHitsEE = cms.InputTag('reducedEcalRecHitsEE'),
     ecalRecHitsEB = cms.InputTag('reducedEcalRecHitsEB'),
     rhoFastJet = cms.InputTag("fixedGridRhoAll"),
   ),
   inputSCs = cms.InputTag('particleFlowSuperClusterECAL','particleFlowSuperClusterECALEndcapWithPreshower'),
   Client = cms.PSet(
        mode = cms.string("Async"),
        preferredServer = cms.untracked.string(""),
        timeout = cms.untracked.uint32(10),
        modelName = cms.string('EGM_DRN'),
        modelVersion = cms.string(""),
        modelConfigPath = cms.FileInPath("DRNDeployment/EGM_DRN/data/models/{}/config.pbtxt".format('EGM_DRN')),
        verbose = cms.untracked.bool(True),
        allowedTries = cms.untracked.uint32(1),
        useSharedMemory = cms.untracked.bool(True),
        compression = cms.untracked.string(""),
    ),
 )

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
dataFormat = DataFormat.AOD
switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V2_cff']

for idmod in my_id_modules:
        setupAllVIDIdsInModule(process, idmod, setupVIDElectronSelection)



process.nTuplelize = cms.EDAnalyzer('Electron_RecHit_NTuplizer3',
        vertexCollection = cms.InputTag('offlinePrimaryVertices'),
        rhoFastJet = cms.InputTag("fixedGridRhoFastjetAll"),
        pileupInfo = cms.InputTag("addPileupInfo"),
        electrons = cms.InputTag("gedGsfElectrons"),
        genParticles = cms.InputTag("genParticles"),
        #Cut Based Id
        eleLooseIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-loose"),
        eleMediumIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-medium"),
        eleTightIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-tight"),

        tracks = cms.InputTag("globalTracks"),
        SkipEvent = cms.untracked.vstring('ProductNotFound')
        )


'''
process.nTuplelize = cms.EDAnalyzer('Electron_RefinedRecHit_NTuplizer',
        rhoFastJet = cms.InputTag("fixedGridFastjetAll"),
        electrons = cms.InputTag("gedElectrons"),
        genParticles = cms.InputTag("genParticles"),
        eleMediumIdMap = cms.InputTag(""),
        eleTightIdMap = cms.InputTag("")
)
'''

process.TFileService = cms.Service("TFileService",
     fileName = cms.string("nTupleMC.root"),
      closeFileFast = cms.untracked.bool(True)
  )

process.load( "HLTrigger.Timer.FastTimerService_cfi" )

process.FastTimerService = cms.Service( "FastTimerService",
    dqmPath = cms.untracked.string( "timer" ),
    dqmModuleTimeRange = cms.untracked.double( 40.0 ),
    enableDQMbyPath = cms.untracked.bool( True ),
    writeJSONSummary = cms.untracked.bool( True ),
    dqmPathMemoryResolution = cms.untracked.double( 5000.0 ),
    enableDQM = cms.untracked.bool( True ),
    enableDQMbyModule = cms.untracked.bool( True ),
    dqmModuleMemoryRange = cms.untracked.double( 100000.0 ),
    dqmModuleMemoryResolution = cms.untracked.double( 500.0 ),
    dqmMemoryResolution = cms.untracked.double( 5000.0 ),
    enableDQMbyLumiSection = cms.untracked.bool( True ),
    dqmPathTimeResolution = cms.untracked.double( 0.5 ),
    printEventSummary = cms.untracked.bool( False ),
    dqmPathTimeRange = cms.untracked.double( 100.0 ),
    dqmTimeRange = cms.untracked.double( 2000.0 ),
    enableDQMTransitions = cms.untracked.bool( False ),
    dqmPathMemoryRange = cms.untracked.double( 1000000.0 ),
    dqmLumiSectionsRange = cms.untracked.uint32( 2500 ),
    enableDQMbyProcesses = cms.untracked.bool( True ),
    dqmMemoryRange = cms.untracked.double( 1000000.0 ),
    dqmTimeResolution = cms.untracked.double( 5.0 ),
    printRunSummary = cms.untracked.bool( False ),
    dqmModuleTimeResolution = cms.untracked.double( 0.2 ),
    printJobSummary = cms.untracked.bool( True ),
)

process.ThroughputService = cms.Service( "ThroughputService",
    dqmPath = cms.untracked.string( "throughput" ),
    eventRange = cms.untracked.uint32( 10000 ),
    timeRange = cms.untracked.double( 60000.0 ),
    printEventSummary = cms.untracked.bool( True ),
    eventResolution = cms.untracked.uint32( 100 ),
    enableDQM = cms.untracked.bool( True ),
    dqmPathByProcesses = cms.untracked.bool( True ),
    timeResolution = cms.untracked.double( 5.828 )
)

process.dqmOutput = cms.OutputModule("DQMRootOutputModule",
    fileName = cms.untracked.string("DQM.root")
)

#process.p = cms.Path(process.DRNProducerEB*process.egmGsfElectronIDSequence*process.nTuplelize)

process.p = cms.Path(process.DRNProducerEB*process.DRNProducerEE*process.egmGsfElectronIDSequence*process.nTuplelize)
#process.p = cms.Path(process.DRNProducerEB*process.DRNProducerEE)
