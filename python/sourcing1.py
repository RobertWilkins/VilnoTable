# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


import copy 
from setup import ddobj, dsnode, Ex

# suppressDS in this file, not bull.py

from bull import KNOWNDSETS, dd,  ORIGDSETS, feedin, FEEDINvnames, \
       Ptask1, PHtask, DSETMULTIRANGE, defaultPIrange, defaultPIrange_reset, \
       THINGDEFNS,  THING_DSET,  THING_KEYVARS,  DSET2_OF_THING, \
       DSETS_USED_WITH_THINGS,  HAVE_NOTHAVE_DATASETS,  \
       BOOLLOG_PH, inflag_varnames, \
       dset_order_preview , dset_order_inlinevdt

from bull2 import varnames_under_thas , thingrelated_varnames_get,  \
         varnames_under_r , DIFF_ASLIST 


# suppressDS

# from ? import BUILD_PULLIN , build_PATINFO_AUG2
# from ? import SETUP_INFLAG_RESTRICTS , prep_for_BESTSORTWAY
# from ? import do_early_PCALL
## ddobj AND dsnode ?? i see a glitch -> nope , different purposes , no conflict
## ?? THINGDEFNS : check it 
##?? allhasnodes  : decide on spelling
# MISUSE_LINK_COLS


# June 2011 , instead of alphabetical order 
# ORIGDSETS must use reverse-age order 
def setup_ORIGDSETS() :
  global ORIGDSETS , dset_order_preview , dset_order_inlinevdt
  dset_prev2 = dset_order_preview[:]
  dset_inline2 = dset_order_inlinevdt[:]
  dset_prev2.reverse()
  dset_inline2.reverse()
  dset_inline3 = []
  for subvec in dset_inline2 :
    subvec2 = subvec[:]
    subvec2.reverse()
    for ds in subvec2 :
      if ds not in ORIGDSETS : ORIGDSETS.append(ds)
  for ds in dset_prev2 :
    if ds not in ORIGDSETS : ORIGDSETS.append(ds)





#########################################################
#########################################################

def PREPARE_SOURCING_PHAS() :
  global PHtask , DSETMULTIRANGE , Ptask1 , defaultPIrange
  global dd , ORIGDSETS , feedin , FEEDINvnames , DSET2_OF_THING
  #global-read BOOLLOG_PH KNOWNDSETS 
  
  allhasnodes = BOOLLOG_PH     # same thing, as it turns out 
  
  # June 2011 , change setup of ORIGDSETS 
  setup_ORIGDSETS() 

  for d1 in KNOWNDSETS :
    dd[d1] = ddobj()
    dd[d1].vnames = set(KNOWNDSETS[d1].vnames)
    dd[d1].parity = KNOWNDSETS[d1].parity
    # ORIGDSETS.append(d1)   ## when do you clarify best order inside ORIGDSETS??
  
  ## when do you clarify pecking order of ORIGDSETS ?
  ## also , when do you clarify pecking order of BEST-SORT-WAY ?
  
  for d1 in ORIGDSETS :
    feedin[d1]=[]
    if d1 in DSETS_USED_WITH_THINGS :
      feedin[ d1+"_aug1" ] = []
      feedin[ d1+"_aug2" ] = []
    for d2 in ORIGDSETS :
      # Dec 29 : bug fix , cannot feedin[d1]=d1 !!
      if dd[d2].parity!=None and d1!=d2 :
        parity2 = set(dd[d2].parity)
        if parity2.issubset(dd[d1].vnames) :
          feedin[d1].append(d2)
          # Oct 2010 , need pull in patinfo_aug1 and patinfo_aug2 as well
          if d2 in DSETS_USED_WITH_THINGS :
            feedin[d1].append( d2+"_aug1" )
            feedin[d1].append( d2+"_aug2" )
    if dd[d1].parity!=None : 
      FEEDINvnames.update(dd[d1].parity)
  
  ###########################
  
  # SETUP_INFLAG_RESTRICTS()  call elsewhere
  # prep_for_BESTSORTWAY()    call elsewhere
  
  for d in HAVE_NOTHAVE_DATASETS : make_immediate_inflag(d) 
  
  ###########################
  
  for t in THINGDEFNS : 
   # ?? tds = DSET_OF_THING[t]
   tds = THING_DSET[t]   # check spelling
   keyvars1 = THING_KEYVARS[t]
   make_immediate_inflag(tds)
   tds_aug1_name = tds + "_aug1"
   tds_aug2_name = tds + "_aug2"

   # Feb 9 bug fix , inflag_varnames for _aug1 & _aug2 
   inflagvname8 = make_inflag_vname(tds)
   inflag_varnames[tds_aug1_name] = inflagvname8 
   inflag_varnames[tds_aug2_name] = inflagvname8

   # newcolnames.clear() ?
   newcolnames = set() 
   PI1 = augment(root=tds,rangee=ORIGDSETS)
   # Jan 2011 , Ptask1 needs .vnpull+.vnhere ready , hence: 
   setup_vnhere_vnpull(PI1)
   Pdsets = set(PI1.top.dsetarray)
   Pvnames = PI1.top.vnall
   # simplePvnames = DIFF_SETS(Pvnames,FEEDINvnames)
   simplePvnames = Pvnames.difference(FEEDINvnames)
   MAKE_ROOTDATASET(PI1,tds_aug1_name)
   Ptask1[t] = [PI1,tds_aug1_name]
   notPdsets = DIFF_ASLIST(ORIGDSETS,Pdsets)
   SUPPRESS_VN(setDS=notPdsets,setVN=simplePvnames)
   M2 = notPdsets + [ tds_aug1_name ]
   nonP_PIs = augment(roots=notPdsets, rangee=M2)
   PHtask[t] = {}
  
   for hasnode in allhasnodes[t] :
    ## August 17 change varnames_under_thas , just spelling change
    vnamecollect = varnames_under_thas(hasnode)
    # IF_SUBSET_OF(vnamecollect,Pvnames) : raise
    if vnamecollect.issubset(Pvnames) : raise Ex("sourc8")
    ## August 17 change 
    ## nextvn = t + "_has_" + IntToString(hasnode.refnum)
    nextvn = hasnode.synthetic_vname
    newcolnames.add(nextvn)
    PIh , depth = searchPI(lookfor=[vnamecollect,tds_aug1_name],lookin=nonP_PIs)
    PIh2 = hedgetrim(foundPI=[PIh,depth],lookfor=[vnamecollect,tds_aug1_name])
    PHtask[t][nextvn] = [PIh2,hasnode]
    # this is a subtle error check, work on later :
    # if MISUSE_LINK_COLS(PIh2) : raise
  
   MAKE_SIMILARDATASET(newds=tds_aug2_name,oldds=tds_aug1_name,
                       morevn=newcolnames,vn_type="BOOL_0_1")
   DSET2_OF_THING[t] = tds_aug2_name
   M3 = notPdsets + [ tds_aug2_name ] 
   M3_PI_range = augment(roots=notPdsets,rangee=M3)
   DSETMULTIRANGE[t] = [ M3_PI_range , tds_aug2_name ]
   CANCEL_SUPPRESS_VN()
  
  ##################################
  
  ## prepare defaultPIrange
  # defaultPIrange=augment(roots=ORIGDSETS,rangee=ORIGDSETS)
  defaultPIrange_reset(augment(roots=ORIGDSETS,rangee=ORIGDSETS))
  
  ###########################################
  
  # do_early_PCALL()       call elsewhere
  
#end def PREPARE_SOURCING_PHAS



#####################################################################
#####################################################################


def augmentr(p,i) :
  if p.depth == i-1 :
   for d in feedin[p.dset] :
    if d in p.top.dsrange and d not in p.top.ds_how :
      q = dsnode()
      q.top = p.top 
      q.top.maxsofar = i 
      q.dset = d 
      q.depth = i 
      q.top.dsetarray.append(d) 
      q.top.ds[i].append(d) 
      q.top.ds_how[d] = p.top.ds_how[p.dset] + [d] 
      for v in dd[d].vnames :
       if v not in q.top.vnall :
        q.top.vnall.add(v) 
        q.top.vn[i].add(v)
        q.top.vn_how[v] = q.top.ds_how[d] 
      p.under.append(q)
  else :
   for u in p.under : augmentr(u,i)
#end def augmentr 

########################################

def augment2(rootdset,rangee) :
  p=dsnode()
  p.dset=rootdset
  p.depth=0
  p.top.maxsofar=0
  p.top.dsrange=rangee[:]
  p.top.dsetarray = [rootdset]
  p.top.ds_how[rootdset] = [rootdset] 
  p.top.ds = [ [rootdset] ]
  vns = copy.deepcopy(dd[rootdset].vnames)
  vns2 = copy.deepcopy(vns)
  p.top.vnall=vns
  p.top.vn= [ vns2 ]
  for v in vns : p.top.vn_how[v] = [rootdset]
  
  i=1 
  while True :
   p.top.ds.append([])
   p.top.vn.append(set())
   augmentr(p,i)
   if p.top.ds[-1] == [] :
    p.top.ds.pop()
    p.top.vn.pop()
    break 
   i = i + 1 
  
  return p 
#end def augment2 
 
##########################

def augment(root=None,roots=None,rangee=[]) :
  if roots != None :
   g = []
   for rds in roots : g.append(augment2(rds,rangee))
   return g
  if root != None : return augment2(root,rangee)
#end def augment 

###########################################

def searchPI(lookfor,lookin) :
  collectVN = lookfor[0]
  collectDS = set(lookfor[1:])
  m = 0 
  for p in lookin : 
   if p.top.maxsofar > m :  m =p.top.maxsofar 
  for dep in range(m+1) :
   for p in lookin :
    g = isitthere(p,dep,collectVN,collectDS)
    if g==True : return p,dep
  return None,None
#end def searchPI 


def isitthere(p,dep,vnames,dsets) :
  cannotdoit=False
  for d in dsets :
   if d in p.top.dsetarray :
    if len(p.top.ds_how[d]) <= dep + 1 : pass
    else : return False 
   else : return False
  for v in vnames :
   if v in p.top.vnall :
    if len(p.top.vn_how[v]) <= dep + 1 : pass
    else : return False
   else : return False
  return True 
#end def isitthere 
 
#############################################


def hedgetrim(foundPI,lookfor) :
  PI1 = foundPI[0] 
  depth1 = foundPI[1]
  needVN = lookfor[0] 
  needDS = set(lookfor[1:])
  p = PI1
  needDS2 = copy.deepcopy(needDS)
  for d in needDS :
   for d2 in p.top.ds_how[d] : needDS2.add(d2)
  for v in needVN : 
   for d2 in p.top.vn_how[v] : needDS2.add(d2)
  newrange = [] 
  for d in p.top.dsrange :
   if d in needDS2 : newrange.append(d) 
  
  PIsmall = augment(root=p.dset , rangee=newrange )
  if ( depth1 != PIsmall.top.maxsofar ) : raise Ex("hedgetrim1")
  if ( PIsmall.top.maxsofar != len(PIsmall.top.vn)-1 ) : raise Ex("hedgetrim2")
  vnvn = copy.deepcopy(PIsmall.top.vn)
  
  for i in range(depth1+1):
   for v in vnvn[i] :
    if v not in needVN :
     PIsmall.top.vn[i].remove(v)
     PIsmall.top.vnall.remove(v)
     del PIsmall.top.vn_how[v] 
  
  # Jan 2011
  setup_vnhere_vnpull(PIsmall)
  
  return PIsmall 
#end def hedgetrim



################################################################
################################################################



def setup_vnhere_vnpull(PI) :
  vnhere_map={}
  vnpull_map={}
  for d in PI.top.ds_how :
    vnhere_map[d]=set()
    vnpull_map[d]=set()
  for v in PI.top.vn_how :
    dsetpath = PI.top.vn_how[v]
    ds = dsetpath[-1]
    vnhere_map[ds].add(v)
    for d2 in dsetpath : vnpull_map[d2].add(v)
  distribute_vnhere_vnpull(PI,vnhere_map,vnpull_map)
#end def setup_vnhere_vnpull

##################


def distribute_vnhere_vnpull(p,vnheremap,vnpullmap) :
  p.vnhere = vnheremap[p.dset]
  p.vnpull = vnpullmap[p.dset]
  for u in p.under :
    distribute_vnhere_vnpull(u,vnheremap,vnpullmap)
#end def distribute_vnhere_vnpull

######################################


def PULLINaddfreebies(PI,wantedvnames) :
  wanted2 = wantedvnames.difference(PI.top.vnall)
  for d in PI.top.dsetarray :
    dpath=PI.top.ds_how[d]
    dep=len(dpath)-1
    getthese=wanted2.intersection(dd[d].vnames)
    for v in getthese : PI.top.vn_how[v]=dpath
    PI.top.vnall.update(getthese)
    PI.top.vn[dep].update(getthese)
    wanted2=wanted2.difference(getthese)
  
  # Jan 2011 , add this
  setup_vnhere_vnpull(PI)
  
#end def PULLINaddfreebies 

##############

def ANY_FREEBIES(PI) :
  forfree=set()
  for d in PI.top.dsetarray :
    forfree.update(dd[d].vnames)
  return forfree
#end def ANY_FREEBIES 

##################################################

def DSET_castasPI(dset) :
  PI = augment(root=dset,rangee=[dset])
  
  setup_vnhere_vnpull(PI)
  return PI
#end def DSET_castasPI






##################################################

suppressDS = None

def SUPPRESS_VN(setDS,setVN) :
  global suppressDS , dd
  for d in setDS :
    moveit=dd[d].vnames.intersection(setVN)
    dd[d].vnames=dd[d].vnames.difference(moveit)
    dd[d].hidden_vnames=moveit
  # suppressDS=setDS.copy()
  suppressDS = set(setDS)
#end def SUPPRESS_VN


def CANCEL_SUPPRESS_VN() :
  global suppressDS , dd 
  for d in suppressDS :
    dd[d].vnames.update(dd[d].hidden_vnames)
    dd[d].hidden_vnames=None
  suppressDS=None
#end def CANCEL_SUPPRESS_VN


###########################


def MAKE_ROOTDATASET(PI,dsetname) :
  global dd
  dd[dsetname]=ddobj()
  dd[dsetname].vnames=PI.top.vnall.copy()
  dd[dsetname].parity = dd[PI.dset].parity
#end def MAKE_ROOTDATASET



def MAKE_SIMILARDATASET(newds,oldds,morevn,vn_type) :
  global dd
  dd[newds]=ddobj()
  dd[newds].vnames=dd[oldds].vnames.copy()
  dd[newds].vnames.update(morevn)
  dd[newds].parity = dd[oldds].parity
#end def MAKE_SIMILARDATASET



def make_immediate_inflag(dsetname) :
  global inflag_varnames , dd 
  vn = make_inflag_vname(dsetname)   # cannot just do "inflag_"+  (/ to _) 
  inflag_varnames[dsetname] = vn 
  dd[dsetname].vnames.add(vn)
  dd[dsetname].ghost_inflag=vn
  ## do before connect to PCALL , so will carry forward
#end def make_immediate_inflag


def make_inflag_vname(dref) :   # assumes dirref does not have slash ( / ) 
  dref2 = dref
  i = dref.find("/")
  if i>0 and i<len(dref)-1 : dref2 = dref[:i] + "_" + dref[i+1:] 
  vn = "inflag_" + dref2 
  return vn 
#end def make_inflag_vname

##############################################################


#########################################################








