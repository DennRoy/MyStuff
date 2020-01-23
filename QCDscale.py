###
### How to use: Run python script with samplename as argument.
### The name(s) have to be in the form "GluGluHToWWTo2L2NuPowheg_M125", not something else like "nanoLatino_GluGluHToWWTo2L2NuPowheg_M125__part0.root".
### Further below are hardcoded options on what years to run.
###

import ROOT
import os
import sys
import re

# OPTIONS
do2016 = True
do2017 = True
do2018 = True
doAll = True
nAODv6 = False
what = sys.argv[1]

#Options:
# GluGluHToWWTo2L2NuPowheg_M125
# VBFHToWWTo2L2NuPowheg_M125
# HZJ_HToWW_M125
# ggZH_HToWW_M125
# HWJ_HToWW_M125
# GluGluHToTauTau_M125
# VBFHToTauTau_M125
# HZJ_HToTauTau_M125
# HWJ_HToTauTau_M125
#
# GluGluHToWWTo2L2Nu_MX
# VBFHToWWTo2L2Nu_MX
# GluGluHToWWToLNuQQ_MX
# VBFHToWWToLNuQQ_MX

# Groups
if 'GluGluWWTo2L2Nu' in what:
  ifiles = ['GluGluWWTo2L2Nu_MCFM', 'GluGluToWWToENMN', 'GluGluToWWToENTN', 'GluGluToWWToMNEN', 'GluGluToWWToMNMN', 'GluGluToWWToMNTN', 'GluGluToWWToTNEN', 'GluGluToWWToTNMN', 'GluGluToWWToTNTN']
elif 'onlyHZJ_HToWW_M125' in what:
  ifiles = ['HZJ_HToWW_M125']
elif 'HZJ_HToWW_M125' in what:
  ifiles = ['HZJ_HToWW_M125', 'HZJ_HToWWTo2L2Nu_M125']
elif 'ggZH_HToWW_M125' in what:
  ifiles = ['ggZH_HToWW_M125', 'GluGluZH_HToWWTo2L2Nu_M125']
elif 'HWJ_HToWW_M125' in what:
  ifiles = ['HWplusJ_HToWW_M125', 'HWminusJ_HToWW_M125']
elif 'HWJ_HToTauTau_M125' in what:
  ifiles = ['HWplusJ_HToTauTau_M125', 'HWminusJ_HToTauTau_M125']
elif '125' not in what:
  ifiles = [what, what.replace("_M","_JHUGen698_M"), what.replace("_M","_JHUGen714_M")]
else:
  ifiles = [what]

#All gg
#ifiles = ['GluGluHToWWTo2L2NuPowheg_M125', 'ggZH_HToWW_M125', 'GluGluZH_HToWWTo2L2Nu_M125', 'GluGluHToTauTau_M125']
#All qqbar
#ifiles = ['VBFHToWWTo2L2NuPowheg_M125', 'HZJ_HToWW_M125', 'HWplusJ_HToWW_M125', 'HWminusJ_HToWW_M125', 'VBFHToTauTau_M125', 'HZJ_HToTauTau_M125', 'HWplusJ_HToTauTau_M125', 'HWminusJ_HToTauTau_M125']

path_t = []
allyears = []

if nAODv6:
  if do2016:
    path_t.append('/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer16_102X_nAODv5_Full2016v6/MCl1loose2016v6__MCCorr2016v6__l2loose__l2tightOR2016v6/')
    allyears.append(2016)
  if do2017:
    path_t.append('/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__l2loose__l2tightOR2017v6/')
    allyears.append(2017)
  if do2018:
    path_t.append('/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/')
    allyears.append(2018)
else:
  if do2016:
    path_t.append('/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer16_102X_nAODv4_Full2016v5/MCl1loose2016v5__MCCorr2016v5__l2loose__l2tightOR2016v5/')
    allyears.append(2016)
  if do2017:
    path_t.append('/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Fall2017_102X_nAODv4_Full2017v5/MCl1loose2017v5__MCCorr2017v5__l2loose__l2tightOR2017v5/')
    allyears.append(2017)
  if do2018:
    path_t.append('/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Autumn18_102X_nAODv5_Full2018v5/MCl1loose2018v5__MCCorr2018v5__l2loose__l2tightOR2018v5/')
    allyears.append(2018)

files_t = {2016:[], 2017:[], 2018:[]}

def getyear(path):
  for thisyear in [2016, 2017, 2018]:
    if str(thisyear) in path: return thisyear

filenameFormat = "nanoLatino_("
for i,ifile in enumerate(ifiles):
  filenameFormat = filenameFormat + ifile
  if i+1<len(ifiles): filenameFormat = filenameFormat + '|'
filenameFormat = filenameFormat + ')(_ext1|_ext2|)__part([0-9]+)\.root' # (_ext1|_ext2|)


for dirt in path_t:
  findir = os.listdir(dirt)
  for file_ in findir:
    pattern = re.match(filenameFormat, file_)
    if pattern is not None:
      files_t[getyear(dirt)].append(dirt+file_)
    #for ifile in ifiles:
    #  if file_.startswith('nanoLatino_'+ifile+'__part'): files_t.append(dirt+file_)

saved = []
alltotalyields = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
for year in allyears:
  print '=====',year,'====='
  if files_t[year]==[]:
    print "No files to go through!"
    continue
  else:
    print "Doing",len(files_t[year]),'files...'
    #print "2016:",len([alpha for alpha in files_t if '2016' in alpha]),";  2017:",len([alpha for alpha in files_t if '2017' in alpha]),";  2018:",len([alpha for alpha in files_t if '2018' in alpha])

  totalyields = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

  for num,file_ in enumerate(files_t[year]):
    print '====='
    print file_
    rootfile = ROOT.TFile(file_)

    treeruns = rootfile.Get('Runs')
    treeruns.GetEntry(0)
    LHESumw = [-999.0, -999.0, -999.0, -999.0, -999.0, -999.0, -999.0, -999.0, -999.0]
    SumwVar = 'LHEScaleSumw'
    try:
      LHESumw[0] = treeruns.GetLeaf(SumwVar).GetValue(0)
    except ReferenceError:
      SumwVar = 'LHEScaleSumw_'
    for i in range(9):
      LHESumw[i] = treeruns.GetLeaf(SumwVar).GetValue(i)
    print LHESumw

    tree = rootfile.Get('Events')
    entries = tree.GetEntries()
    yields = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    for i in range(entries):
      tree.GetEntry(i)
    
      # wwSel
      if not (tree.GetLeaf("Lepton_pdgId").GetValue(0)*tree.GetLeaf("Lepton_pdgId").GetValue(1) == -11*13): continue
      if not (tree.GetLeaf("mll").GetValue() > 12): continue
      if not (tree.GetLeaf("ptll").GetValue() > 30): continue
      if not (tree.GetLeaf("PuppiMET_pt").GetValue() > 20): continue
      if not (tree.GetLeaf("nLepton").GetValue() >= 2): continue
      if not (tree.GetLeaf("Lepton_pt").GetValue(0) > 20): continue
      if not (tree.GetLeaf("Lepton_pt").GetValue(1) > 10): continue
      if (tree.GetLeaf("nLepton").GetValue() >= 3):
        if not (tree.GetLeaf("Lepton_pt").GetValue(2) < 10): continue
      # wwSel end

      XS = tree.GetLeaf("XSWeight").GetValue()
      yields[9] += XS
      for j in range(9):
        yields[j] += (XS * tree.GetLeaf("LHEScaleWeight").GetValue(j))

    for i in range(10):
      scale = LHESumw[4]/LHESumw[i] if i<9 else 1.0
      #print scale, yields[i]
      totalyields[i] += (yields[i] * scale)

  for i in range(10):
    alltotalyields[i] += totalyields[i]
    

  if totalyields[4] != totalyields[9]:
    print 'nom != [4] :',totalyields[9],'!=',totalyields[4]
  else:
    print 'nom == [4]'
  if abs((totalyields[4]-totalyields[9])/totalyields[9])>0.0001: print 'WARNING! Fairly large difference (?)'

  print "Getting maximum difference between nominal and scaled (ignoring mu_f/mu_r = 0.5/2 and 2/0.5)" #... which are indicees 2 and 6
  final = 0.0
  print "Nominal:", totalyields[4]
  doThese = [0,1,3,5,7,8]
  for i in doThese:
    varyield = totalyields[i]/totalyields[4]
    print '  ['+str(i)+']  :',totalyields[i],' --> Variation:',varyield
    varyield = abs(1-varyield)*100
    if varyield>final:
      final=varyield
      theone=i
  print "For Input:",what,', year',year
  print "QCDscale uncertainty is %.3f" % final,"% (highest variation from LHEScaleWeight["+str(theone)+"])"
  saved.append("%.3f" % final)

if doAll:
  final = 0.0
  for i in doThese:
    varyield = alltotalyields[i]/alltotalyields[4]
    varyield = abs(1-varyield)*100
    if varyield>final:
      final=varyield
      theone=i
  print "QCDscale uncertainty for everything is %.3f" % final,"% (highest variation from LHEScaleWeight["+str(theone)+"])"

if len(saved)>1:
  print "Summary of individual years:"
  print saved
exit()
