# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import Ex

from bull import AVAILABLEVNAMES, THINGDEFNS, INFLAG_RESTRICTS, ONLYIFstack, \
   DSET2_OF_THING, KEYVARS_OF_THING, thingglobalsetting, \
   HAVE_NOTHAVE_DATASETS, DSETMULTIRANGE, defaultPIrange, \
   DENOMglobal, SUBPOPglobal, H_for_GST, \
   translateTHISROWCAT , translateSRC, \
   translateTHISROWCAT_reset, translateSRC_reset , \
   STATISTICS_WHERE    # this dict is new, July 2011

from bull2 import subpopdenom_node_to_obj, produce_catrange_restrict_node, \
   UNIQUIZE_CAT, UNIQUIZE_RESTRICT, FILTERSPELL_CAT, \
   FILTERSPELL_RES, COLLECTSPELL_RES, \
   UNION_RES, UNION_CAT, UNION_CAT_tup, INTERSECT_RES, INTERSECT_CAT, \
   DIFF_CAT, specialoptions_under_m, VNAMES_OF_DSET, searchDSET

from pneed_gst import prepGST_FIV
from pneedhelp import VECTOR_VARI_CLARIFY, find_MSPEC, TABLESPELL

from moclarify import find_M_O
from pcall2 import RESTRICTIFY

from sourcing1 import searchPI, hedgetrim, PULLINaddfreebies, \
               ANY_FREEBIES, DSET_castasPI

from pcall import BUILD_PULLIN, NOTHAVE_PREP, THISROW_PREP, \
     getN, getPCT, getAVGetc, ADVMODEL_PREP,  Hslot

# AVAILABLETHINGNAMES , THINGDEFNS instead

##################################################

# looks like ROOFcr not needed in bull.py
ROOFcr=None   # decide what file you put ROOFcr in ?

gssMcrap = []
gssOcrap = []

###################################################

def PROCESS_THIS_LEAF(p,L) :
  global gssMcrap
  global gssOcrap
  global ROOFcr 
  # global innermostrowcat , innermostrowcatNODE , continuousvarname_src
  ROOFcr = L
  
  
  
  thingwant=None
  thingdset=None
  thingkeyvars=None
  USETHINGDSET=None
  UsingTWOdsets=None
  NOTHAVE=False
  MSPEC=None
  OSPEC=None
  MSPEConlyif=None
  MSPECsubpop=None
  M_OPT=None
  
  ROOFc=[]
  ROOFr=[]
  
  CAT_FREQ = {}
  ROOFCAT = []
  ROOFRESTRICT = []
  ROWCAT = []
  ROWCAT2 = []
  ROWRESTRICT = []
  CAT_RNG = {}
  srcvname = None
  SUMMSTAT = None
  NOTHAVE = False
  havenothave_datasetname=None
  CAT_RNG_RESTRICT = {}
  specialops = None
  
  setPvnames=None
  
  stat_node=None
  stat_toomany=False
  
  # here lots of stuff set as None,{},[]
  
  for t in ROOFcr : 
   if t.c_r=="c" : ROOFc.append(t) 
   elif t.c_r=="r" : ROOFr.append(t) 
   if t.type=="m_expr" : 
     MSPEC=t 
     for e in t.under : 
       if e.type=="onlyif" : MSPEConlyif=e 
       ## June/July , change to use node/obj transform fctn 
       if e.type=="subpop" : MSPECsubpop=subpopdenom_node_to_obj(e) 
   if t.type=="o_expr" : 
     if stat_node!=None : stat_toomany=True
     stat_node = t
     OSPEC=t 
   if t.type=="cat" : ROOFCAT.append(t.text)
   if t.type=="restrict" : ROOFRESTRICT.append(t)
   if t.type=="cat" and t.literalrange!=None : CAT_RNG[t.text]=t.literalrange 
   if t.type=="srcreset" :
    if t.text in AVAILABLEVNAMES and srcvname==None :
       srcvname=t.text 
   if t.type in ("mean","std","median","sum","min","max") :
     if t.text2nd in AVAILABLEVNAMES : srcvname=t.text2nd 
   if t.type in ("n","%","mean","median","std","sum","min","max") :
     if stat_node!=None : stat_toomany=True
     stat_node = t
     SUMMSTAT=t.type 
   if t.type in ("n","%") :
    if t.text2nd in THINGDEFNS : thingwant=t.text2nd 
    elif thingglobalsetting()!=None : thingwant=thingglobalsetting() 
    if thingwant!=None :
      thingdset=DSET2_OF_THING[thingwant]
      thingkeyvars=KEYVARS_OF_THING[thingwant]
   if t.type=="nothave" : NOTHAVE=True 
   if t.type in ("nothave","have") and t.text2nd in HAVE_NOTHAVE_DATASETS :
     havenothave_datasetname = t.text2nd 
     # TABLESPELL() will put "inflag_a_labs" into spelling for vname search 
     # do not need restrict node in addition, only for vname search 
  
  for v in ROOFCAT : CAT_FREQ[v]=0 
  for v in ROOFCAT : CAT_FREQ[v]=CAT_FREQ[v]+1 
  ROOFCAT=UNIQUIZE_CAT(ROOFCAT)
  ROOFRESTRICT=UNIQUIZE_RESTRICT(ROOFRESTRICT) 
  
  #######################
  
  if OSPEC!=None and SUMMSTAT!=None : raise Ex("summary+advanced")
  
  #### July 2011, allow for PRINT-STAT feature, decide to abort or not abort :
  if stat_toomany==True : raise Ex("toomany_stats")
  if stat_node==None : return 

  if stat_node.c_r=="c" : ROOFw = ROOFr
  else : ROOFw = ROOFc
  go_nogo = crossref_statistic_ROOF(stat_node,ROOFw)
  if go_nogo==False : return    # do not do this statistic, no PCALL build

  
  ### this piece of code relocated June 7
  
  ROWCAT=[]
  ROWRESTRICT=[]
  for t in ROOFr :
    if t.type=="cat" : ROWCAT.append(t.text) 
    if t.type=="restrict" : ROWRESTRICT.append(t)
  ROWCAT=UNIQUIZE_CAT(ROWCAT)
  ROWRESTRICT=UNIQUIZE_RESTRICT(ROWRESTRICT)
  
  
  # Oct 2010 CATVNAME(=3 4 5)  -> restrict to produce and add to RESvectors
  for c in CAT_RNG :
    CAT_RNG_RESTRICT[c] = produce_catrange_restrict_node(c,CAT_RNG[c]) 
    ROOFRESTRICT = UNION_RES(ROOFRESTRICT,[CAT_RNG_RESTRICT[c]])
    if c in ROWCAT :
      ROWRESTRICT = UNION_RES(ROWRESTRICT,[CAT_RNG_RESTRICT[c]])  
  
  
  ##############################
  
  # for t in ROOFcr : print t.type + " " + t.text 
  # if OSPEC==None : print "ospec is none"
  # else : print ( OSPEC.type + " " + OSPEC.text ) 
  
  

  if OSPEC!=None and MSPEC==None :
    MSPEC , MSPEConlyif , MSPECsubpop = find_MSPEC(ROOFcr,OSPEC) 
    if MSPEC==None : raise Ex("mspeccannotfind")
  if MSPEC!=None :
    gssM , gssO = find_M_O(MSPEC,OSPEC)
  
  
  # Oct 2010 , thingwant setup , via MSPEC :
  if MSPEC!=None :
    specialops = specialoptions_under_m(MSPEC)  # return empty set , or "n","thisrow?"
    if "n" in specialops or "thisrow?" in specialops :
      if thingglobalsetting()!=None : thingwant=thingglobalsetting() 
      if thingwant!=None :
        thingdset=DSET2_OF_THING[thingwant]
        thingkeyvars=KEYVARS_OF_THING[thingwant]
  
  
  
  ############################################
  
  ### august addition 
  innermostrowcat=None
  innermostrowcatNODE=None
  PATHrow = ROOFr[:]
  PATHrow.reverse()
  for e in PATHrow :
    if e.type=="cat" :
      innermostrowcat = e.text
      innermostrowcatNODE = e 
      break
  continuousvarname_src = srcvname
  translateTHISROWCAT_reset(innermostrowcat)
  translateSRC_reset(srcvname)
  
  
  #################################################
  
  tspelling = TABLESPELL(ROOFcr,MSPEC,thingwant)
  if thingwant!=None :
    dmr=DSETMULTIRANGE[thingwant] 
    PIrange=dmr[0]
    thingdset=dmr[1] 
    setPvnames = VNAMES_OF_DSET(thingdset) 
    USETHINGDSET=searchDSET(lookfor=tspelling,lookin=thingdset)
    UsingTWOdsets = not USETHINGDSET 
    if USETHINGDSET==False :
      PIa , depth = searchPI(lookfor=[tspelling],lookin=PIrange)
      if PIa==None : raise Ex("vnamesearchfail")
      PIb = hedgetrim(foundPI=[PIa,depth],lookfor=[tspelling]) 
    else :
      PIb = DSET_castasPI(thingdset)
  else  :  ## thingwant is None 
    PIa , depth = searchPI(lookfor=[tspelling],lookin=defaultPIrange())
    if PIa==None : raise Ex("vnamesearchfail2")
    PIb = hedgetrim(foundPI=[PIa,depth],lookfor=[tspelling])
  freespell = ANY_FREEBIES(PIb)
  
  
  ########################################################
  
  ### june 7 modify this page (MSPEConlyif.under[0] and INFLAG_RESTRICTS )
  
  if MSPEConlyif!=None : ONLYstack2=UNION_RES(ONLYIFstack,[MSPEConlyif.under[0]])
  else : ONLYstack2=ONLYIFstack[:]
  ONLYIFmp , Junk = FILTERSPELL_RES(ONLYstack2,freespell)
  
  # fix this : WHAT IF setPvnames with thingwant==None ?
  if thingwant!=None :
    ONLYIFp  , Junk = FILTERSPELL_RES(ONLYIFmp,setPvnames)
  else :
    ONLYIFp = ONLYIFmp[:]
  
  
  if thingwant!=None and UsingTWOdsets==True : 
    ONLYIFmp.append(INFLAG_RESTRICTS[thingdset])
  
  needfreebies=COLLECTSPELL_RES(ONLYIFmp) 
  
  PULLINaddfreebies(PIb,needfreebies)
  
  if thingwant!=None :
    ROOFRESTRICTp , Junk = FILTERSPELL_RES(ROOFRESTRICT,setPvnames)
  else :
    ROOFRESTRICTp = ROOFRESTRICT[:]
  
  RESTRICTp2=UNION_RES(ONLYIFp,ROOFRESTRICTp)
  RESTRICTmp2=UNION_RES(ONLYIFmp,ROOFRESTRICT)
  
  if thingwant!=None :
    ROOFCATp , ROOFCATm = FILTERSPELL_CAT(ROOFCAT,setPvnames) 
  else :
    ROOFCATp = ROOFCAT[:]
    ROOFCATm = []
  
  
  ###########################################################
  
  if SUMMSTAT in ("n","%") :
   DENOM1=DENOMglobal()
   DEN1b_CAT = INTERSECT_CAT(DENOM1.CATv,ROOFCAT)
   DEN1b_RES = INTERSECT_RES(DENOM1.RESTRICTv,ROOFRESTRICT)
   DEN1c_CAT , DEN1c_RES = VECTOR_VARI_CLARIFY(DENOM1.VARIv,ROOFc,ROOFr)
   # Oct 2010 , don't let MP-level stuff sneak in , only P-level
   if UsingTWOdsets==True : 
     DEN1c_CAT , Junk = FILTERSPELL_CAT(DEN1c_CAT,setPvnames)
     DEN1c_RES , Junk = FILTERSPELL_RES(DEN1c_RES,setPvnames)
   DENOM_CAT = UNION_CAT(DEN1b_CAT,DEN1c_CAT)
   DENOM_RESTRICT = UNION_RES(DEN1b_RES,DEN1c_RES)
  
  if MSPEC!=None :
   if MSPECsubpop!=None :
     SUBPOP1=MSPECsubpop 
   else :
     SUBPOP1=SUBPOPglobal() 
   POP1b_CAT = INTERSECT_CAT(SUBPOP1.CATv,ROOFCAT)
   POP1b_RES = INTERSECT_RES(SUBPOP1.RESTRICTv,ROOFRESTRICT)
   POP1c_CAT , POP1c_RES = VECTOR_VARI_CLARIFY(SUBPOP1.VARIv,ROOFc,ROOFr)
   # Oct 2010 , don't let MP-level stuff sneak in , only P-level
   if UsingTWOdsets==True : 
     POP1c_CAT , Junk = FILTERSPELL_CAT(POP1c_CAT,setPvnames)
     POP1c_RES , Junk = FILTERSPELL_RES(POP1c_RES,setPvnames)
   SUBPOP_CAT = UNION_CAT(POP1b_CAT,POP1c_CAT)
   SUBPOP_RESTRICT = UNION_RES(POP1b_RES,POP1c_RES)
  
  # if .VARIv translates to something not at P-level : bad 
  
  RESTRICTmp = ONLYIFmp[:]
  RESTRICTp = ONLYIFp[:]
  if SUMMSTAT in ("n","%") :
    RESTRICTmp = UNION_RES(RESTRICTmp,DENOM_RESTRICT)
    RESTRICTp = UNION_RES(RESTRICTp,DENOM_RESTRICT)
  if MSPEC!=None :
    RESTRICTmp = UNION_RES(RESTRICTmp,SUBPOP_RESTRICT)
    RESTRICTp  = UNION_RES(RESTRICTp,SUBPOP_RESTRICT)
  
  
  ####################################################
  
  if MSPEC!=None :
    gssM.mo_clarify(MSPEC)   ## Sept 28 mo_clarify not mo_clarify1 
    gssO.mo_clarify1(OSPEC)
    gssM.bylist = set(SUBPOP_CAT)
    M_OPT = gssM.specialoption
    modelinput1 = list(gssM.normalinputvarnames)
    if M_OPT=="thisrow?" :
      gssM.bylist = set(SUBPOP_CAT+ROWCAT)
    # gssM.mo_clarify_post()
    gssO.mo_clarify_post(CAT_FREQ)
    OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST = gssO.returnPSAT(ROOFcr)
    statcolname = OSPEC.text
  
  
  ######################################
  
  
  if NOTHAVE==True :
    ## PNEED IS ALL SET :
    ## already have: ROOFCATp ROOFCATm DENOM_CAT DENOM_RESTRICT 
    ## already have: RESTRICTmp RESTRICTp RESTRICTmp2 RESTRICTp2 
    pass
  
  if M_OPT=="n_bridge" :
    ##  earlier you did modelinput1=gssM.normalinputvarnames()  
    if UsingTWOdsets==True :
      whatever = 77 
      # do this check later
      # if not All_Plevel_CATs(modelinput1,ROOFcr,setPvnames) : 
      #      raise Ex("mpmix:nbridge")
  
  if M_OPT=="thisrow?" :
    ## june 7 , calc of ROWCAT and ROWRESTRICT moved to earlier 
    ROWCAT2=DIFF_CAT(ROWCAT,SUBPOP_CAT)
    fRESTRICT=UNION_RES(ROWRESTRICT,RESTRICTmp)
    tRESTRICT=RESTRICTp
    fCAT=UNION_CAT_tup((SUBPOP_CAT,ROWCAT,modelinput1))
    tCAT=UNION_CAT_tup((SUBPOP_CAT,modelinput1))
    ## if not All_Plevel_CATs(modelinput1,ROOFcr,setPvnames) RAISE
  
  
  
  ############################################################
  
  if SUMMSTAT in ("n","%","mean","sum","std","min","max","median") :
    statcolname = SUMMSTAT
  if SUMMSTAT=="%" : statcolname="pct"
  if SUMMSTAT in ("n","%") and UsingTWOdsets==True and NOTHAVE==True :
    if SUMMSTAT=="n" : statcolname = "n_nothave"
    else : statcolname = "pct"
  
  if MSPEC!=None : statcolname = OSPEC.text
  
  if MSPEC==None : 
    OUTPUTCOL_CONST = {}
    OUTPUTCOL_ROOFINDEX = {}
    for i in range(len(ROOFcr)) :
      t=ROOFcr[i]
      if t.type=="cat" : OUTPUTCOL_ROOFINDEX[t.text]=i
  
  
  ######################################################
  ######################################################
  
  
  if thingwant!=None and UsingTWOdsets==True : 
    Hm=BUILD_PULLIN(PIb)
    Hp=Hslot(thingdset)
  if thingwant!=None and (not UsingTWOdsets==True) :
    Hm=Hslot(thingdset)
    Hp=Hm
  if thingwant==None :
    Hm=BUILD_PULLIN(PIb)
    Hp=Hm
  
  if MSPEC==None :
    if NOTHAVE and SUMMSTAT in ("n","%") and UsingTWOdsets==True :
      Hw=NOTHAVE_PREP(Hm,Hp,ROOFCATm,ROOFCATp,DENOM_CAT,
                      RESTRICTmp2,RESTRICTp2,RESTRICTp,thingkeyvars,CAT_RNG)
    elif SUMMSTAT=="n" :
      Hw=getN(Hm,ROOFCAT,thingkeyvars,RESTRICTmp2,nameN="n")
    elif SUMMSTAT=="%" :
      Hw=getPCT(Hm,Hp,ROOFCAT,DENOM_CAT,RESTRICTmp2,RESTRICTp,thingkeyvars)
    elif SUMMSTAT in ("median","mean","std","min","max","sum") :
      Hw=getAVGetc(Hm,ROOFCAT,RESTRICTmp2,srcvname,SUMMSTAT)
    else : raise Ex("whichsummstat")
    Hanal=Hw
  
  
  if MSPEC!=None :
    if M_OPT=="n_bridge" :
      Hw=getN(Hp,SUBPOP_CAT+modelinput1,(),RESTRICTp,nameN="n")
    elif M_OPT=="thisrow?" :
      Hw=THISROW_PREP(Hm,Hp,SUBPOP_CAT,modelinput1,thingkeyvars,
                      ROWCAT,ROWCAT2,ROWRESTRICT,fRESTRICT,tRESTRICT,fCAT,tCAT)
  
    # Oct 2010 , fix this :
    # else : Hw=Hm         , no that is wrong , missing RESTRICT !
    else : Hw = RESTRICTIFY(Hm,RESTRICTmp)
  
    # May 26 2011 : ADVMODEL_PREP no longer needs OUTPUTCOL_CONST as input parameter, take out
    Hanal = ADVMODEL_PREP(Hw,gssM,gssO)
    gssMcrap.append(gssM)
    gssOcrap.append(gssO)
    # Hanal = ADVMODEL_PREP(Hw,gssM,gssO,OUTPUTCOL_CONST)
  
  ############################
  
  H_for_GST.add(Hanal)
  # May 26 2011 , now prepGST_FIV needs OUTPUTCOL_CONST as input parameter as well, add it
  prepGST_FIV(ROOFcr,ROOFc,ROOFr,OUTPUTCOL_ROOFINDEX,statcolname,Hanal,OUTPUTCOL_CONST)
  
#end def PROCESS_THIS_LEAF






##########################################################
#### July 2011, add for the PRINT-STAT feature to turn off statistic for some cells
##########################################################



def crossref_statistic_ROOF(stat_node,ROOF) :
  stat1 = stat_node.mark1
  stat2 = stat_node.mark2 
  if stat2 in STATISTICS_WHERE : stat3 = stat2 
  elif stat1 in STATISTICS_WHERE : stat3 = stat1 
  else : return True   # go ahead and print statistic
  
  list_options = STATISTICS_WHERE[stat3]
  
  ROOF_set = set()
  for t in ROOF : ROOF_set.update((t.mark1,t.mark2))

  go_ahead = False 
  for option in list_options :
    if option.issubset(ROOF_set) : go_ahead=True
  return go_ahead








