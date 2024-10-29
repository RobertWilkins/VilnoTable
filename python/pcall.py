# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


import copy

from setup import Ex

# from bull import PCALLdirpath   , just use zdirectory instead 

from bull import KNOWNDSETS, PCALL, PCALLbegin, PCALLbegin_set , DIRREFS, \
    dsetname_Href, Href_to_fullfilename, Href_to_datref, zdirectory, \
    dd, ORIGDSETS, Ptask1, PHtask, THING_DSET, THING_KEYVARS, H_for_GST, \
    PCALL_filename, PCALL_mode, EXT_M2

from bull2 import DSET_PARITY, VNAMES_OF_DSET, produce_restrictnode_outcolconst, \
              dsetname, fullfilepath, datref_to_fullfilename, \
              construct_dirref_statement

from mo_external import gssMexternal 

from pcall4 import BEST_SORT_WAY, BEST_SORT_WAYc, inputrefs_as_tuple

from pcall2 import incomingdataset, RESTRICTIFY, PRESORT, MERGEIN0, \
            JOINBY1, READBY_DUO1, EASYCALC, NULLZEROFY, EMPTYDS0, EXP0, \
            SEL_DISTINCT0, SEL_DISTINCT1, SEL_N_0, SEL_MEAN1, SEL_MEDIAN1

from generateS import print_importst_S

## careful : DSET_PARITY not only patinfo , but **_aug1/2
## MERGEIN1 is in this file



#######################################################


def Hslot_attach(H1,dsetname) : 
  dsetname_Href[dsetname]=H1
#end def Hslot_attach


def Hslot(dsetname) :
  if dsetname not in dsetname_Href : raise Ex("hslot1")
  return dsetname_Href[dsetname]
#end def Hslot


def Hslot_fromoutside(dsetname) : 
  if dsetname not in dd : raise Ex("hslotoutsideunkdset")
  incomeobj=incomingdataset(dsetname,dd[dsetname].vnames,
                            dd[dsetname].ghost_inflag)
  PCALL.append(incomeobj)
  dsetname_Href[dsetname] = (len(PCALL)-1 , 0)
#end def Hslot_fromoutside



#####################################################

def do_early_PCALL() :
  ## do after PHtask/DSETMULTIRANGE but before building _AUG1
  for ds in ORIGDSETS : Hslot_fromoutside(ds)
  PCALLbegin_set(len(PCALL))
  ## build PATINFO_AUG1
  for t in Ptask1 :
    # PI=t[0]  this is wrong 
    # dsetname=t[1] this is wrong  Feb 9 bug fix follows 
    tstruct = Ptask1[t]
    PI = tstruct[0]
    dsetname = tstruct[1]
    
    H1=BUILD_PULLIN(PI)
    Hslot_attach(H1,dsetname)
  build_PATINFO_AUG2()
#end def do_early_PCALL






###################################################

def BUILD_PULLIN(PI) :
  ### ???
  ## setup_vnhere_vnpull(PI)
  return BUILD_PULLIN2(PI)
#end def BUILD_PULLIN

######################################

def BUILD_PULLIN2(PI) :
  H1 = Hslot(PI.dset)
  H1b = H1 
  VNcollect = PI.vnhere.copy()
  # Oct 2010 , make sure any link-status columns are retained 
  # Jan 2011 DSET_PARITY could return None
  # VNcollect.update( DSET_PARITY(PI.dset) )
  dp1 = DSET_PARITY(PI.dset) 
  if dp1!=None : VNcollect.update( dp1 )
  for PI2 in PI.under :
    VNcollect.update( DSET_PARITY(PI2.dset) )
  for PI2 in PI.under :
    H2 = BUILD_PULLIN2(PI2)
    bylistp = DSET_PARITY(PI2.dset)
    H1b = MERGEIN1(H1b,H2,bylist=bylistp,vnlist1=VNcollect,vnlist2=PI2.vnpull)
    VNcollect.update(PI2.vnpull)
  return H1b
#end def BUILD_PULLIN2


#############################################

def build_PATINFO_AUG2() :
  for t in PHtask :
    task = PHtask[t]
    dset = THING_DSET[t]
    aug1name = dset + "_aug1"
    aug2name = dset + "_aug2"
    thingkeyvars = THING_KEYVARS[t]
    Hprev = Hslot(aug1name)
    Ha = Hprev 
    othervn = set( VNAMES_OF_DSET(aug1name) )
    for v in task :
      PI , hasnode = task[v] 
      Ha = BUILD_PHAS(Hprev,PI,hasnode,thingkeyvars,v,othervn)
      Hprev = Ha 
      othervn.add(v)
    Hslot_attach(Ha,aug2name)
#end def build_PATINFO_AUG2



def BUILD_PHAS(H1,PI,boolexp,thingkeyvars,pathasname,othervn) :
  boolexp2 = boolexp.under[0]
  Hp = BUILD_PULLIN(PI)
  Hp2 = RESTRICTIFY(Hp,(boolexp2,))
  H2 = SEL_DISTINCT1(Hp2,thingkeyvars)
  H3 = MERGEIN1(H1,H2,bylist=thingkeyvars,inflagname=pathasname,vnlist1=othervn)
  if boolexp.text2nd=="nothas" :
    # March 8 bug fix , add argument for vncreate :
    # another March 8 bug fix , vnlist , add pathasname
    H3 = EASYCALC(H3,requestvec=((pathasname,"=","1","-",pathasname),),
                  vnlist=list(othervn)+[pathasname], 
                  vncreate=[] )
  return H3
#end def BUILD_PHAS

## above proof=1 , but fill in ??*3


###################################################



def NOTHAVE_PREP(H1,H2,MCAT,PCAT,PCATd,RESTRICTm,RESTRICTp,RESTRICTd,
                   thingkeyvars,EXPANDIFY_MAP) :
  MPCAT=MCAT+PCAT
  Hskel=JBY_MP(H1,H2,MCAT,PCAT,EXPANDIFY_MAP)
  H3=getN(H1,MPCAT,thingkeyvars,RESTRICTm,nameN="n_have")
  H4=getN(H2,PCAT,(),RESTRICTp,nameN="n_t")
  H5=getN(H2,PCATd,(),RESTRICTd,nameN="n_d")
  
  ### August change
  if len(MPCAT)==0 : H6=H3
  else :
    H6=MERGEIN1(Hskel,H3,MPCAT,vnlist2=["n_have"])
  H7=MERGEIN1(H6,H4,PCAT,vnlist1=MPCAT+["n_have"],vnlist2=["n_t"])
  H8=MERGEIN1(H7,H5,PCATd,vnlist1=MPCAT+["n_have","n_t"],vnlist2=["n_d"])
  
  H9=NULLZEROFY(H8,["n_have","n_t","n_d"])
  H10=EASYCALC(H9,requestvec=(("n_nothave","=","n_t","-","n_have"),
                              ("pct","=","100.0","*","n_nothave","/","n_d")      ),
                   vnlist=MPCAT+["n_have","n_t","n_d"] ,
                   vncreate=["n_nothave","pct"]  )
  return H10
#end def NOTHAVE_PREP



## august change
def JBY_MP(H1,H2,MCAT,PCAT,EXP_MAP) :
  if len(MCAT)==0 and len(PCAT)==0 : return EMPTYDS0()
  if len(MCAT)==0 : return EXPANDIFY1(H2,PCAT,EXP_MAP)
  if len(PCAT)==0 : return EXPANDIFY1(H1,MCAT,EXP_MAP)
  H1b=EXPANDIFY1(H1,MCAT,EXP_MAP)
  H2b=EXPANDIFY1(H2,PCAT,EXP_MAP)
  H3=JOINBY1(H1b,H2b,bylist=(),vnlist1=MCAT,vnlist2=PCAT)
  return H3
#end def JBY_MP


## august change
def EXPANDIFY1(H1,CATv,EXP_MAP) :
  CATnorm , CATexp = crossref_expmap(CATv,EXP_MAP)
  if len(CATv)==0 : return EMPTYDS0()
  if len(CATnorm)==0 : return EXP0(CATexp,EXP_MAP)
  if len(CATexp)==0 : return SEL_DISTINCT1(H1,CATnorm)
  H2=SEL_DISTINCT1(H1,CATnorm)
  H3=EXP0(CATexp,EXP_MAP)
  # bug fix Jan 16
  # H4=JOINBY1(H2,H3,vnlist1=CATnorm,vnlist2=CATexp)
  H4=JOINBY1(H2,H3,bylist=(),vnlist1=CATnorm,vnlist2=CATexp)
  return H4
#end def EXPANDIFY1



###########################################################

def crossref_expmap(CATv,emap) :
  CATreg = []
  CATex  = []
  for c in CATv :
    if c in emap : CATex.append(c) 
    else : CATreg.append(c)
  return CATreg , CATex 
#end def crossref_expmap

###########################################################


### BCAT is SUBPOP_CAT , ACAT is modelinput1 , ROWCAT2 is ROWCAT-BCAT 

def THISROW_PREP(H1,H2,BCAT,ACAT,thingkeyvars,ROWCAT,ROWCAT2,ROWRESTRICT,
               fRESTRICT,tRESTRICT,fCAT,tCAT) :
  BYBYCAT = set( BCAT+ROWCAT2 )
  Hskel = JBY_BRA(H1,H2,BCAT,ROWCAT2,ACAT)
  H3 = getN(H1,fCAT,thingkeyvars,fRESTRICT,nameN="n_f")
  H4 = getN(H2,tCAT,(),tRESTRICT,nameN="n_t")
  
  H5 = MERGEIN1(Hskel,H3,fCAT,vnlist1=BCAT+ROWCAT2+ACAT,vnlist2=["n_f"])
  H6 = MERGEIN1(H5,H4,tCAT,vnlist1=BCAT+ROWCAT2+ACAT+["n_f"],vnlist2=["n_t"])
  
  H7 = NULLZEROFY(H6,["n_f","n_t"])
  H8 = EASYCALC(H7,requestvec=(("n","=","n_t","-","n_f"),("thisrowq","=","0")),
                   vnlist=BCAT+ROWCAT2+ACAT+["n_f","n_t"] , 
                   vncreate=["n","thisrowq"]  )
  
  H9 = EASYCALC(H7,requestvec=(("n","=","n_f"),("thisrowq","=","1")),
                   vnlist=BCAT+ROWCAT2+ACAT+["n_f","n_t"]  ,
                   vncreate=["n","thisrowq"]  )
  
  H10 = READBY_DUO1(H8,H9,bylist=BYBYCAT,
                    vnlist1=["n","thisrowq"]+ACAT,vnlist2=["n","thisrowq"]+ACAT)
  
  return H10
#end def THISROW_PREP



## august change
def JBY_BRA(H1,H2,bylist1,CATv1,CATv2) :
  if len(bylist1+CATv1+CATv2)==0 : return EMPTYDS0()
  if len(CATv1)==0 : return SEL_DISTINCT1(H2,bylist1+CATv2)
  if len(CATv2)==0 : return SEL_DISTINCT1(H1,bylist1+CATv1)
  H3 = SEL_DISTINCT1(H1,bylist1+CATv1)
  H4 = SEL_DISTINCT1(H2,bylist1+CATv2)
  H5 = JOINBY1(H3,H4,bylist=bylist1,vnlist1=CATv1,vnlist2=CATv2)
  return H5
#end def JBY_BRA

## above page, modify(JBY_BRA) June 7


##########################################################


def getN(H1,CATv,thingkey,RESTRICTv,nameN="n") :
  tkey=thingkey
  if tkey==None : tkey=()
  bylist2a , bylist2b = BEST_SORT_WAYc( (CATv,tkey) )
  bylist2 = bylist2a + bylist2b
  H1b = RESTRICTIFY(H1,RESTRICTv)
  H2 = PRESORT(H1b,bylist2)
  if tkey!=() : H3 = SEL_DISTINCT0(H2,bylist2)
  else : H3 = H2 
  H4 = SEL_N_0(H3,bylist2a,nameN=nameN)
  return H4
#end def getN



def MERGEIN1(H1,H2,bylist,vnlist1=(),vnlist2=(),inflagname=None) :
  bylist2 = BEST_SORT_WAY(bylist)
  H3 = PRESORT(H1,bylist2)
  H4 = PRESORT(H2,bylist2)
  H5 = MERGEIN0(H3,H4,bylist2,vnlist1,vnlist2,inflagname)
  return H5
#end def MERGEIN1 



#######################################
### today is May 24 , typing below    <- must be May 24 2010 not 2011 ?!

# May 26 2011 : ADVMODEL_PREP does not need to be passed OUTPUTCOL_CONST, 
#    so remove that input argument in function call
### Feb 2021 , modify ADVMODEL_PREP() to call MAKE_GSS_EXT() or MAKE_GSS()
###
def ADVMODEL_PREP(Hprev,gssM,gssO) :
  ## Hprev = incoming ( typical or thisrow-prep or bridge-prep )
  gssM.bylist2 = BEST_SORT_WAY(gssM.bylist)
  gssO.bylist2 = gssM.bylist2
  gssO.sorted = gssM.bylist2
  ## Sept 27 , i think you will need this
  gssO.bylist = gssM.bylist2 
  Hgssprep = PRESORT(Hprev,gssM.bylist2)
  
  ## Jan 2021 , slight change here
  if gssM.__class__ == gssMexternal :
    Hresult = MAKE_GSS_EXT(Hgssprep,gssM,gssO)
  else :
    Hresult = MAKE_GSS(Hgssprep,gssM,gssO)
  
  # modification May 26 2011 : do not do restrict gsd, tableprint will handle that 
  return Hresult 
  # if OUTPUTCOL_CONST != {} :     May 26 , comment out this section 
  #   restrictnode = produce_restrictnode_outcolconst(OUTPUTCOL_CONST)
  #   Hresult2 = RESTRICTIFY(Hresult,(restrictnode,))
  # else : Hresult2=Hresult
  # return Hresult2
#end def ADVMODEL_PREP




#################################################

def MAKE_GSS_EXT(inputindex,gssM,gssO) :
  for i in range(len(PCALL)) :
    if PCALL[i].__class__ == gssMexternal and  \
       PCALL[i].seqno == gssM.seqno and  \
       PCALL[i].inputref == inputindex   :
      return ( i , gssO.out_seqno-1 )
  PROC = copy.deepcopy(EXT_M2[gssM.seqno-1])
  PROC.inputref = inputindex
  PROC.bylist = gssM.bylist
  PROC.bylist2 = gssM.bylist2
  for gso in PROC.OLIST :
    gso.Mref = PROC
    gso.bylist  = gssM.bylist2   ## frankly, not necessary
    gso.bylist2 = gssM.bylist2
    gso.sorted  = gssM.bylist2 
  PCALL.append(PROC)
  return ( len(PCALL)-1 , gssO.out_seqno-1 )
### end def MAKE_GSS_EXT()




#################################################


def MAKE_GSS(inputindex,gssM,gssO) :
  oclassname = gssO.__class__.__name__
  for i in range(len(PCALL)) :
    PROC = PCALL[i]
    if POSSIBLE_MATCH_M(PROC,gssM,inputindex) :
      for j in range(len(PROC.OLIST)) :
        ODSET = PROC.OLIST[j]
        if POSSIBLE_MATCH_O(ODSET,gssO) :
          UTP_UPDATE(ODSET,gssO)
          return (i,j)
      if (PROC.multallow[oclassname]==True) or (oclassname not in PROC.OLIST_TYPES) :
        ODSET = NEWDSETCALL(gssO)
        PROC.OLIST_TYPES.add(oclassname)
        PROC.OLIST.append(ODSET)
        j = len(PROC.OLIST)-1
        return (i,j)
  
  PROC = NEWPROCCALL(gssM)
  PROC.inputref = inputindex 
  ODSET = NEWDSETCALL(gssO)
  PROC.OLIST_TYPES.add(oclassname)
  PROC.OLIST.append(ODSET)
  PCALL.append(PROC)
  i = len(PCALL) - 1 
  return (i,0) 
#end def MAKE_GSS
### above proof=00


def POSSIBLE_MATCH_M(PCALLitem,newMobj,inputnum) :
  if PCALLitem.__class__.__name__ != newMobj.__class__.__name__ : return False
  if PCALLitem.inputref != inputnum : return False 
  for g in newMobj.__dict__.keys() :
    if g in ("OLIST","OLIST_TYPES","inputref") : continue 
    if g not in PCALLitem.__dict__.keys() : return  False   # (or RAISE)
    if newMobj.__dict__[g] != PCALLitem.__dict__[g] : return False 
  return True 
#end def POSSIBLE_MATCH_M


def POSSIBLE_MATCH_O(PCALLODSitem,newOobj) :
  if PCALLODSitem.__class__.__name__ != newOobj.__class__.__name__ : return False 
  for g in newOobj.__dict__.keys() :
    if g in ("utp_values","level","level1","level2","Mref") : continue 
    if g not in PCALLODSitem.__dict__.keys() : return False 
    if newOobj.__dict__[g] != PCALLODSitem.__dict__[g] : return False
  return True 
#end def POSSIBLE_MATCH_O


def UTP_UPDATE(ods,gssO) :
  if "utp_values" in ods.__dict__ :
    ods.utp_values.update(gssO.utp_values) 
#end def UTP_UPDATE

### above proof=00


def NEWPROCCALL(gssM) :
  obj = gssM.__class__()
  obj.OLIST = []
  obj.OLIST_TYPES = set()
  for g in gssM.__dict__.keys() :
    if g in ("OLIST","OLIST_TYPES") : continue 
    obj.__dict__[g] = copy.deepcopy(gssM.__dict__[g])
  return obj 
#end def NEWPROCCALL


def NEWDSETCALL(gssO) :
  obj = gssO.__class__() 
  obj.Mref = None 
  for g in gssO.__dict__.keys() :
    if g in ("Mref","level","level1","level2") : continue 
    obj.__dict__[g] = copy.deepcopy(gssO.__dict__[g])
  return obj 
#end def NEWDSETCALL


### above proof=00  but from napkins

##################################################



##########################################################




def getPCT(Hm,Hp,CAT1,CAT2,RESTRICT1,RESTRICT2,thingkeyvars) :
  H1=getN(Hm,CAT1,thingkeyvars,RESTRICT1,nameN="n")
  H2=getN(Hp,CAT2,(),RESTRICT2,nameN="n_d")
  H3=MERGEIN1(H1,H2,CAT2,vnlist1=CAT1+["n"],vnlist2=CAT2+["n_d"])
  H4=EASYCALC(H3,requestvec=(("pct","=","100.0","*","n","/","n_d"),),
              vnlist=CAT1+["n","n_d"],vncreate=["pct"] )
  return H4
#end def getPCT



def getAVGetc(H1,CATv,RESTRICTv,sourcevname,stat_choice) :
  H1b=RESTRICTIFY(H1,RESTRICTv)
  if stat_choice in ("mean","std","sum","min","max") :
    H2=SEL_MEAN1(H1b,CATv,sourcevname,stat_choice)
  elif stat_choice=="median" :
    H2=SEL_MEDIAN1(H1b,CATv,sourcevname)
  return H2
#end def getAVGetc




############################################################



def PCALL_abba_prep() :
  alreadyconvert = set() 
  incoming_convert = "" 
  STOR_CALL = [None]*len(PCALL)
  ABannotate = [ None ]*len(PCALL)
  for k in range(len(ABannotate)) : ABannotate[k] = ["",""]
  
  for k in range(PCALLbegin()) : 
    PROC = PCALL[k] 
    STOR_CALL[k] = KNOWNDSETS[PROC.datasetname].storage
  
  for k in range(PCALLbegin(),len(PCALL)) :
    if   PCALL[k].dom=="d" : STOR_CALL[k] = "vdt"
    elif PCALL[k].dom=="m" : STOR_CALL[k] = "asc"
  
  ###########
  
  for k in range(PCALLbegin(),len(PCALL)) :
    PROC = PCALL[k] 
    inputlist = inputrefs_as_tuple(PROC)
    for iref in inputlist :
      if iref in alreadyconvert : continue 
      (i1,i2) = iref 
      storenow = STOR_CALL[i1]
      cn3 = PCALL[i1].__class__.__name__ 
      if PROC.dom=="d" and storenow=="asc" :
        ABannotate[k][0] += print_ab( dsetname(iref) ) + "\n" 
        alreadyconvert.add(iref)
      if PROC.dom=="m" and storenow=="vdt" :
        if cn3 != "incomingdataset" :
          ABannotate[i1][1] += print_ba( dsetname(iref) ) + "\n" 
          alreadyconvert.add(iref)
        else :
          incoming_convert += print_ba( dsetname(iref) ) + "\n"
          alreadyconvert.add(iref)
  
  ############################
  
  for iref in H_for_GST :
    if iref in alreadyconvert : continue 
    (i1,i2) = iref 
    storenow = STOR_CALL[i1]
    cn3 = PCALL[i1].__class__.__name__ 
    if STOR_CALL[i1]=="vdt" and iref not in alreadyconvert :
      if cn3 != "incomingdataset" :
        ABannotate[i1][1] += print_ba( dsetname(iref) ) + "\n" 
        alreadyconvert.add(iref)
      else :
        incoming_convert += print_ba( dsetname(iref) ) + "\n"
        alreadyconvert.add(iref)
  
  
  
  return ABannotate , incoming_convert
  
#end def PCALL_abba_prep 


#############################################################
#############################################################
#############################################################

# May 2011 , substantial rewrite of finishPCALL to make more efficient 
# older versionn put in qcallfix.py to archive 
def finishPCALL() :
  global PCALL_filename , PCALL_mode  

  for k in range(PCALLbegin(),len(PCALL)) :
    PROC = PCALL[k]
    if PROC.dom=="d" : PROC.outputref = (k,0)
    elif PROC.dom=="m" :
      for i in range(len(PROC.OLIST)) : PROC.OLIST[i].outputref = (k,i)
  
  for k in range(PCALLbegin()) :
    PROC = PCALL[k] 
    dref = PROC.datasetname 
    Href_to_datref[(k,0)] = dref 
    Href_to_fullfilename[(k,0)] = datref_to_fullfilename(dref) 
  
  for k in range(PCALLbegin(),len(PCALL)) :
    PROC = PCALL[k]
    if PROC.dom=="m" :
      for i in range(len(PROC.OLIST)) :
        H = (k,i)
        s1 = "tmp_" + str(k) + "_" + str(i) 
        s2 = "z/" + s1 
        s3 = zdirectory + "/" + s1 + ".txt"
        Href_to_datref[H] = s2 
        Href_to_fullfilename[H] = s3
    elif PROC.dom=="d" :
      H=(k,0)
      s1 = "tmp_" + str(k) + "_0" 
      s2 = "z/" + s1 
      s3 = zdirectory + "/" + s1 + ".txt"
      Href_to_datref[H] = s2 
      Href_to_fullfilename[H] = s3
  
  
  ###########
  
  QCALL = [None]*len(PCALL)
  for k in range(PCALLbegin(),len(PCALL)) : QCALL[k]=PCALL[k].export()
  # remember .export() cannot do source() statements in S , do elsewhere 
  
  ABannotate , incoming_convert = PCALL_abba_prep()
  
  VDT_CALL = [] 
  VDT_CALL.append(construct_dirref_statement())
  if incoming_convert!="" :
    VDT_CALL.append(incoming_convert)
  S_CALL = []
  S_CALL.append(print_importst_S())
  
  for k in range(PCALLbegin(),len(PCALL)) :
    m=PCALL[k].dom
    if m=="d" :
      if ABannotate[k][0]!="" : VDT_CALL.append(ABannotate[k][0])
      VDT_CALL.append(QCALL[k])
      if ABannotate[k][1]!="" : VDT_CALL.append(ABannotate[k][1])
    if m=="m" :
      S_CALL.append(QCALL[k])
  
  VDT_CALL2 = "" 
  S_CALL2 = ""
  if len(VDT_CALL)>1 : 
    VDT_CALL2 =  "\n".join(VDT_CALL)
    filename = ( zdirectory + "/" +  "PCALL_script_0." + suffix_reformat("vdt")  )
    PCALL_filename.append(filename)
    PCALL_mode.append("vdt")
    file2 = open(filename,'w')
    file2.write(VDT_CALL2)
    file2.close()
    
  if len(S_CALL)>1 : 
    S_CALL2 = "\n".join(S_CALL)
    filename = ( zdirectory + "/" +  "PCALL_script_1." + suffix_reformat("s")  )
    PCALL_filename.append(filename)
    PCALL_mode.append("s") 
    file2 = open(filename,'w')
    file2.write(S_CALL2)
    file2.close()
  
#end def finishPCALL



##############################################################
###############################################################


def suffix_reformat(mode) :
  if mode=="vdt" : return "src"
  elif mode=="s" : return "s"
#end def suffix_reformat

#################################################


def print_ab(dref) :
  return  ( "convertfileformat asciitobinary(" + dref + "->" + dref + 
            ") colspecsinfirstrow ;"  )
#end def print_ab

def print_ba(dref) :
  return  ( "convertfileformat binarytoascii(" + dref + "->" + dref + 
            ") colspecsinfirstrow ;"  )
#end def print_ba

################################################

