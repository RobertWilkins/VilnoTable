# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 

from setup import Ex, parsenode, subpopdenomobject

from bull import zdirectory, dd, AVAILABLEVNAMES, SD_VARIATORS, \
     DIRREFS, Href_to_fullfilename, Href_to_datref, \
     BOOLLOG, RESTRICT_SPELL_LOG, BOOLLOG_PH, \
     FACUNK_LOGNO_SET, FACUNK_VNSET_TO_LOGNO, \
     INFLAG_RESTRICTS, inflag_varnames, \
     THING_DSET, THING_KEYVARS, DSETS_USED_WITH_THINGS, \
     request_convert_ab, request_convert_ba


##########################################################

def fullfilepath(Href) :
  if Href not in Href_to_fullfilename : raise Ex("fullfilepath1")
  return Href_to_fullfilename[Href] 
#end def fullfilepath 

def dsetname(Href) :
  if Href not in Href_to_datref : raise Ex("dsetname1")
  return Href_to_datref[Href] 
#end def dsetname


def datref_to_fullfilename(dref) :
  g = dref.split("/")
  if len(g)!=2 : raise Ex("datreffullfilename1")
  dirref1 = g[0]
  shortdset = g[1]
  if dirref1=="z" : dir2 = zdirectory 
  else : 
    if dirref1 not in DIRREFS : raise Ex("datreffullfilename2")
    dir2 = DIRREFS[dirref1]
  s = dir2 + "/" + shortdset + ".txt" 
  return s 
#end def datref_to_fullfilename





#####################################################

def EQUAL_RESTRICT(p,b) :
  if ( p.type!=b.type or p.text!=b.text or p.text2nd!=b.text2nd or 
       p.literalrange!=b.literalrange or p.opvec!=b.opvec ) :
      return False 
  if len(p.under)!=len(b.under) : return False 
  for i in range(len(p.under)) :
    if EQUAL_RESTRICT(p.under[i],b.under[i])==False : return False 
  return True 
#end def EQUAL_RESTRICT



def DSET_PARITY(dref) :
  if dref not in dd : raise Ex("dsetparity1")
  return dd[dref].parity
#end def DSET_PARITY



def VNAMES_OF_DSET(ds) :
  if ds not in dd : return None
  return set(dd[ds].vnames)
#end def VNAMES_OF_DSET


def searchDSET(lookfor,lookin) :
  # lookin is a dsetname 
  if lookin not in dd : return None
  lookingfor2 = set(lookfor)
  return lookingfor2.issubset(dd[lookin].vnames)
#end def searchDSET

########################################################

def subpopdenom_node_to_obj(p) :
  sdobj = subpopdenomobject() 
  RESv=[]
  CATv=[]
  Vv=[]
  for u in p.under :
    if u.type=="restrict" : RESv.append(u)
    elif u.text in AVAILABLEVNAMES :
      if u.text not in CATv : CATv.append(u.text)
    elif u.text in SD_VARIATORS : 
      if u.text not in Vv : Vv.append(u.text)
    else : raise Ex("subdentoobj1")
  sdobj.RESTRICTv = UNIQUIZE_RESTRICT(RESv)
  sdobj.CATv = CATv 
  sdobj.VARIv = Vv 
  return sdobj 
#end def subpopdenom_node_to_obj



##############################################

def varnames_under_thas(p) :
  vnset1=thingrelated_varnames_get(p.text)
  ## above : include inflag_patinfo,site,patid
  vnset2=varnames_under_r(p.under[0])
  vnset3=vnset1.union(vnset2)
  return vnset3 
#end def varnames_under_thas


def thingrelated_varnames_get(thingspec) :
  dref = THING_DSET[thingspec]
  inflag_vn = inflag_varnames[dref]
  keyvars = THING_KEYVARS[thingspec]
  vnset = set()
  vnset.add(inflag_vn)
  vnset.update(keyvars)
  return vnset
#end def thingrelated_varnames_get


##########################################################
##########################################################


##################################

def varnames_under_funk(p) :
  collect=set()
  varnames_under_funk2(collect,p)
  return collect
#end def varnames_under_funk


def varnames_under_funk2(collect,p) :
  if p.type=="thinghas" : return 
  if p.type=="word" and p.text in AVAILABLEVNAMES :
    collect.add(p.text)
    return 
  if p.type in ("=range","=null") and p.text in AVAILABLEVNAMES :
    collect.add(p.text)
    return 
  for u in p.under :
    varnames_under_funk2(collect,u)
#end def varnames_under_funk2


####################################
####################################



def produce_facunk_node(spellVN) :
  spellVN = frozenset(spellVN)
  q1 = parsenode() 
  q1.type = "restrict" 
  q2 = parsenode() 
  q2.type = "and_expr" 
  if spellVN in FACUNK_VNSET_TO_LOGNO : 
    logno = FACUNK_VNSET_TO_LOGNO[spellVN]
    p = BOOLLOG[logno]
    return p
  else :
    for v in spellVN : 
      g = parsenode() 
      g.type="!=null" 
      g.text = v 
      q2.under.append(g) 
    if len(q2.under)==1 : q1.under.append(q2.under[0]) 
    else : q1.under.append(q2)
    BOOLLOG.append(q1)
    RESTRICT_SPELL_LOG.append(spellVN)
    q1.restrict_logno = len(BOOLLOG)-1 
    FACUNK_VNSET_TO_LOGNO[spellVN] = q1.restrict_logno
    FACUNK_LOGNO_SET.add(q1.restrict_logno)
    return q1 
#end def produce_facunk_node


## above , rewrite of fac-node fctn , June 15,June 18

###########################################################




def varnames_under_m(p) :
  collect=set()
  if p.type!="m_expr" : raise Ex("vnameundermmexpr")
  varnames_under_m2(collect,p) 
  return collect 
#end def varnames_under_m


def varnames_under_m2(collect,p) :
  if p.type=="subpop" or p.type=="onlyif" : return 
  if p.type=="word" and p.text in AVAILABLEVNAMES :
    collect.add(p.text)
  for u in p.under : varnames_under_m2(collect,u) 
#end def varnames_under_m2


###############################################


def varnames_under_r(p) :
  collect=set()
  varnames_under_r2(collect,p)
  return collect
#end def varnames_under_r


def varnames_under_r2(collect,p) :
  if p.type=="thinghas" : 
    collect.add(p.synthetic_vname)
    return 
  if p.type=="word" and p.text in AVAILABLEVNAMES :
    collect.add(p.text)
    return 
  if p.type in ("=range","=null") and p.text in AVAILABLEVNAMES :
    collect.add(p.text)
    return 
  for u in p.under :
    varnames_under_r2(collect,u)
#end def varnames_under_r2


##################################################



def INTERSECT_RES(RES1v,RES2v) :
  rlog1=set()
  rlog2=set()
  rlog3=set()
  rv=[]
  for r in RES1v : rlog1.add(r.restrict_logno)
  for r in RES2v : rlog2.add(r.restrict_logno)
  for r in RES2v :
    n = r.restrict_logno 
    if (n in rlog1) and (n in rlog2) and (n not in rlog3) :
      rv.append(r)
      rlog3.add(n)
  return rv 
#end def INTERSECT_RES



def UNION_RES(RES1v,RES2v) :
  rlog3=set()
  rv=[]
  RES3v=RES1v+RES2v 
  for r in RES3v : 
    n = r.restrict_logno 
    if n not in rlog3 : 
      rv.append(r) 
      rlog3.add(n)
  return rv 
#end def UNION_RES



def UNIQUIZE_RESTRICT(RESv) :
  rlog3=set()
  rv=[]
  for r in RESv : 
    n = r.restrict_logno 
    if n not in rlog3 : 
      rv.append(r) 
      rlog3.add(n)
  return rv 
#end def UNIQUIZE_RESTRICT



def FILTERSPELL_RES(RES1v,setVN) :
  rv1=[]
  rv2=[]
  for r in RES1v :
    resspell = RESTRICT_SPELL_LOG[r.restrict_logno]
    if IS_SUBSET_OF(resspell,setVN) : rv1.append(r)
    else : rv2.append(r)
  return (rv1,rv2)
#end def FILTERSPELL_RES




def COLLECTSPELL_RES(RESv) :
  vnset=set()
  for r in RESv :
    resspell = RESTRICT_SPELL_LOG[r.restrict_logno]
    vnset.update(resspell)
  return vnset
#end def COLLECTSPELL_RES



def UNIQUIZE_CAT(CATv) :
  cat3 = set()
  cv=[]
  for c in CATv :
    if c not in cat3 :
      cv.append(c)
      cat3.add(c)
  return cv
#end def UNIQUIZE_CAT


# set1.issubset(set2) == if set1 is subset of set2
def IS_SUBSET_OF(smallset,bigset) :
  return smallset.issubset(bigset)
#end def IS_SUBSET_OF

# def IS_SUBSET_OF(set1,set2) :
# for a in set1 :
#   if a not in set2 : return False 
# return True 
# #end def IS_SUBSET_OF


def UNION_CAT(CAT1v,CAT2v) :
  clog3=set()
  cv=[]
  CAT3v=CAT1v+CAT2v 
  for c in CAT3v : 
    if c not in clog3 : 
      cv.append(c) 
      clog3.add(c)
  return cv 
#end def UNION_CAT

def UNION_CAT_tup(vec_of_CATv) :
  clog3=set()
  cv=[]
  for subvec in vec_of_CATv :
    for c in subvec : 
      if c not in clog3 : 
        cv.append(c) 
        clog3.add(c)
  return cv 
#end def UNION_CAT_tup


def DIFF_CAT(CAT1v,CAT2v) :
  cv=[]
  for c in CAT1v :
    if c not in CAT2v : cv.append(c)
  return cv
#end def DIFF_CAT

def INTERSECT_CAT(CAT1v,CAT2v) :
  cv=[]
  for c in CAT1v :
    if c in CAT2v : cv.append(c)
  return cv
#end def INTERSECT_CAT


def FILTERSPELL_CAT(CAT1v,setVN) :
  cv1=[]
  cv2=[]
  for c in CAT1v :
    if c in setVN : cv1.append(c)
    else : cv2.append(c)
  return (cv1,cv2)
#end def FILTERSPELL_CAT


def DIFF_ASLIST(vec1,set2) :
  vec2 = []
  for v in vec1 :
    if v not in set2 : vec2.append(v)
  return vec2
#end def DIFF_ASLIST

######################################################


# OCTOBER 2010 :

def specialoptions_under_m(p) :
  collect=set()
  ## this change November 2020, for ext. stat. proc. , no special options
  if p.type=="m_expr_ext" : return collect
  if p.type!="m_expr" : raise Ex("specialoptunderm1")
  specialoptions_under_m2(collect,p) 
  return collect 
#end def specialoptions_under_m


def specialoptions_under_m2(collect,p) :
  if p.type=="subpop" or p.type=="onlyif" : return 
  if p.text in ("n","thisrow?") :  collect.add(p.text)
  for u in p.under : specialoptions_under_m2(collect,u) 
#end def specialoptions_under_m2


##########################################


def produce_catrange_restrict_node(vname,litvec) :
  q1 = parsenode() 
  q1.type = "restrict" 
  q2 = parsenode() 
  q2.type = "=range" 
  q2.text = vname 
  q2.literalrange = litvec 
  q1.under.append(q2) 
  
  found=False
  for i in range(len(BOOLLOG)) :
    b=BOOLLOG[i] 
    chk=EQUAL_RESTRICT(q1,b)
    if chk==True :
      q1.restrict_logno=i 
      found=True 
      break
  if found==False :
    BOOLLOG.append(q1) 
    RESTRICT_SPELL_LOG.append(set([vname]))
    q1.restrict_logno=len(BOOLLOG)-1 
  return q1 
#end def produce_catrange_restrict_node

####################################################

def produce_restrictnode_outcolconst(OUTPUTCOL_CONST) :
  if OUTPUTCOL_CONST==None or OUTPUTCOL_CONST=={} : raise Ex("resnodeoutcol1")
  spellVN = set()
  qq1 = parsenode() 
  qq1.type = "restrict" 
  qq2 = parsenode() 
  qq2.type = "and_expr" 
  for vn in OUTPUTCOL_CONST :
    spellVN.add(vn)
    litval = OUTPUTCOL_CONST[vn]
    q2 = parsenode() 
    q2.type = "==" 
    q3 = parsenode()
    q3.type = "word"
    q3.text = vn 
    q4 = parsenode()
    q4.text = litval 
    if "." in litval and litval[0] not in ("\"","\'") : 
           raise Ex("resnodeoutcolfloatnotallow") 
    if litval[0].isdigit() : q4.type="intliteral"
    elif litval[0] in ("\"","\'") : q4.type="strliteral"
    else : raise Ex("resnodeoutcoldtypeunk")
    q2.under.append(q3)
    q2.under.append(q4)
    qq2.under.append(q2)
  
  if len(qq2.under)>1 : qq1.under.append(qq2) 
  elif len(qq2.under)==1 : qq1.under.append(qq2.under[0])
  
  found=False
  for i in range(len(BOOLLOG)) :
    b=BOOLLOG[i] 
    chk=EQUAL_RESTRICT(qq1,b)
    if chk==True :
      qq1.restrict_logno=i 
      found=True 
      break
  if found==False :
    BOOLLOG.append(qq1) 
    RESTRICT_SPELL_LOG.append(spellVN)
    qq1.restrict_logno=len(BOOLLOG)-1 
  return qq1 
  
#end def produce_restrictnode_outcolconst


########################################################






def produce_equal_node(vname,litval) :
  q1 = parsenode() 
  q1.type = "restrict" 
  q2 = parsenode() 
  q2.type = "==" 
  q1.under.append(q2) 
  
  q3 = parsenode()
  q3.type = "word"
  q3.text = vname 
  
  q4 = parsenode()
  q4.text = litval 
  if "." in litval and litval[0] not in ("\"","\'") : 
         raise Ex("equalnodefloatnotallow") 
  if litval[0].isdigit() : q4.type="intliteral"
  elif litval[0] in ("\"","\'") : q4.type="strliteral"
  else : raise Ex("equalnodedtypeunk")
  
  q2.under.append(q3)
  q2.under.append(q4)
  
  found=False
  for i in range(len(BOOLLOG)) :
    b=BOOLLOG[i] 
    chk=EQUAL_RESTRICT(q1,b)
    if chk==True :
      q1.restrict_logno=i 
      found=True 
      break
  if found==False :
    BOOLLOG.append(q1) 
    RESTRICT_SPELL_LOG.append(set([vname]))
    q1.restrict_logno=len(BOOLLOG)-1 
  return q1 
#end def produce_equal_node


#####################################################

def inconsistent_dtypes(litvec) :
  seenINT , seenSTR , seenFLO = False , False , False
  for val in litvec :
    if val[0].isdigit() and "." not in val : seenINT=True 
    elif val[0]=="." and len(val)>=2 and val[1].isdigit() : seenFLO=True 
    elif val[0].isdigit() and "." in val : seenFLO=True 
    elif val[0] in ("\"","\'") : seenSTR=True 
    else : return True     # calling function treats as error 
  if seenFLO==True : return True   # if call this fctn , not expect float
  if seenINT==True and seenSTR==True : return True
  return False
#end def inconsistent_dtypes

######################################################

# careful - don't call too early - inflag_varnames must be ready
def SETUP_INFLAG_RESTRICTS() :
  global INFLAG_RESTRICTS
  # INFLAG_RESTRICTS = {}
  # dsets_todo = HAVE_NOTHAVE_DATASETS.copy()
  dsets_todo = set() 
  # dsets_todo.update( set( DSETS_USED_WITH_THINGS.keys() ) )
  # Feb 9 bug fix: do not forget _aug1 and _aug2 
  for ds in DSETS_USED_WITH_THINGS : 
    dsets_todo.update( (ds,ds+"_aug1",ds+"_aug2") )
  for dset in dsets_todo :
    vn = inflag_varnames[dset]
    q1=parsenode()
    q1.type="restrict"
    q2=parsenode()
    q2.type="=="  ## verify that format 
    q3=parsenode()
    q3.type="word"
    q3.text=vn
    q4=parsenode()
    q4.type="intliteral"
    q4.text="1"
    q1.under.append(q2)
    q2.under.append(q3)
    q2.under.append(q4)
    INFLAG_RESTRICTS[dset]=q1 
    # careful here , for patinfo, patinfo_aug1,patinfo_aug2, three equal restricts 
    # but bookkeeping here counts them as not equal -- careful    Feb 9
    BOOLLOG.append(q1)
    RESTRICT_SPELL_LOG.append(set([vn]))
    q1.restrict_logno=len(BOOLLOG)-1
#end def SETUP_INFLAG_RESTRICTS  


###########################################################

def construct_dirref_statement() :
  v=[]
  q = "\""
  for dirref1 in DIRREFS :
    s = dirref1 + "=" + q + DIRREFS[dirref1] + q 
    v.append(s) 
  s = "z=" + q + zdirectory + q
  v.append(s)
  st = "directoryref " + " ".join(v) + " ;\n"
  return st 
#end def construct_dirref_statement

#######################################################



def prepare_request_converts() :
  stuff = []
  for dref in request_convert_ab :
    if request_convert_ab[dref]=="waiting" :
      s = ( "convertfileformat asciitobinary(" + dref + "->" + dref + 
          ") colspecsinfirstrow ;\n" )
      stuff.append(s)
      request_convert_ab[dref]="sentout"
  for dref in request_convert_ba :
    if request_convert_ba[dref]=="waiting" :
      s = ( "convertfileformat binarytoascii(" + dref + "->" + dref + 
          ") colspecsinfirstrow ;\n" )
      stuff.append(s)
      request_convert_ba[dref]="sentout"
  return stuff 
#end def prepare_request_converts



def prepare_dirref_statements() :
  stuff = []
  for dirref in DIRREFS : 
    s = "directoryref " + dirref + "=\"" + DIRREFS[dirref] + "\"" + "  ;\n"
    stuff.append(s)
  return stuff 
#end def prepare_dirref_statements





