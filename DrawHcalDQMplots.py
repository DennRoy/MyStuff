import ROOT
import os
import sys

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

# e.g. Syntax: "python DrawHcalDQMplots.py 346559_HB_LED", to run on file "output/346559_HB_LED"

filename = "output/" + sys.argv[1]
rootFile = ROOT.TFile(filename, "read")
plotdir = "plots_"+filename.split("/")[-1]+"/"


def MkDir(name):
  if not os.path.isdir(name): os.system("mkdir "+name)

def MakePlot(hist, name, resize):
  c = ROOT.TCanvas()
  if resize and hist.ClassName()=="TPad": hist.SetPad(0.01,0.01,0.99,0.99)
  hist.Draw()
  c.SaveAs(name)
  del c
  
def GoThroughKeys(r, direc):
  MkDir(direc)
  keys = r.GetListOfKeys()
  for k in keys:
    kname = k.GetName()
    if k.GetClassName() == "TDirectoryFile":
      GoThroughKeys(r.GetDirectory(kname), direc+kname+"/")
    elif k.GetClassName() == "TCanvas":
      for p in r.Get(kname).GetListOfPrimitives():
        pname = p.GetName()
        MakePlot(r.Get(kname).GetPrimitive(pname), direc+pname+".png", True)
    else:
      MakePlot(r.Get(kname), direc+kname+".png", False)


GoThroughKeys(rootFile, plotdir)
print ("Done!")
exit()
