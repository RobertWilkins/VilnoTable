# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import parsenode , Ex

from bull import SUMMSTATOPTIONS , AVAILABLEVNAMES, \
          FACUNK_VNSET_TO_LOGNO, FACUNK_LOGNO_SET, \
          BOOLLOG, RESTRICT_SPELL_LOG, inflag_varnames, INFLAG_RESTRICTS, \
          MODELFOOTS, MODELFOOTS_ONLYIF, MODELFOOTS_SUBPOP


from bull2 import thingrelated_varnames_get, EQUAL_RESTRICT, \
            varnames_under_funk, varnames_under_m, varnames_under_r, \
            produce_facunk_node, UNIQUIZE_RESTRICT, UNIQUIZE_CAT


# INFLAG_RESTRICTS = {}   


#################################################


def variate_clarify(variator,colpath,rowpath) :
  path=colpath+rowpath
  if variator=="factorunk" : return variate_clarify_facunk(colpath,rowpath)
  if variator=="thisrowcat" :     ## repeat for col situ 
    rowreverse = rowpath[:] 
    rowreverse.reverse() 
    for e in rowreverse :
      if e.type=="cat" : return e 
    return None 
  if variator=="toprowlevel" :
    if len(rowpath)==0 : return None 
    e = rowpath[0] 
    if e.type in ["all","cat","restrict"] :
      return e 
    return None 
#end def variate_clarify

############################################


def variate_clarify_facunk(colpath,rowpath) :
  spell=set()
  path=colpath+rowpath
  for e in path :
    if e.type=="cat" : spell.add(e.text)
    if e.type=="srcreset" :
      if e.text in AVAILABLEVNAMES : spell.add(e.text)
    if e.type in SUMMSTATOPTIONS :     ## (mean,median,etc)
      if e.text2nd in AVAILABLEVNAMES : spell.add(e.text2nd) 
    if e.type=="restrict" :
      rspell=varnames_under_funk(e)
      spell.update(rspell)
  q=produce_facunk_node(spell)
  return q 
#end def variate_clarify_facunk


####################################################


# Oct 31 , need to have thingwant arg provided and use it, 
#   because thingwant can come from inside M-expr as well as n/% argument
def TABLESPELL(TPATH,ModelUsed,thingwantspec) :      # third argument new 
  collect=set()
  for e in TPATH :
    if e.type=="cat" : collect.add(e.text)
    if e.type=="restrict" :
      vnset=varnames_under_r(e) 
      collect.update(vnset)
    if e.type=="m_expr" :
      vnset=varnames_under_m(e) 
      collect.update(vnset) 
    if e.type in ("have","have?","nothave") and e.text2nd!=None :
      if e.text2nd not in inflag_varnames : raise Ex("notininflagvnvec") 
      v = inflag_varnames[e.text2nd]
      collect.add(v)
    # Oct 2010 : thingwant spec calculated BEFORE this function called , 
    # so depreciate following 7 lines 
    # if e.type in ("n","%") :
    #  if e.text2nd!=None and e.text2nd in THINGDEFN : 
    #    thingflag=e.text2nd 
    #  else thingflag=Nglobalsetting 
    #  if thingflag!=None : 
    #    vnset=thingrelated_varnames_get(thingflag)
    #    set_accumulate(collect,vnset)
    if e.type=="srcreset" : collect.add(e.text) 
    if e.type in ("mean","std","median","sum","min","max") and e.text2nd!=None :
        collect.add(e.text2nd)
  
  # Oct 2010 : 
  if thingwantspec!=None : 
    collect.update(thingrelated_varnames_get(thingwantspec)) 
  
  if ModelUsed!=None and ModelUsed.type=="m_expr" : 
    vnset=varnames_under_m(ModelUsed) 
    collect.update(vnset)

  ## addition to TABLESPELL(), November 2020
  if ModelUsed!=None and ModelUsed.type=="m_expr_ext" :
    collect.update(ModelUsed.under[0].input_vn)
  
  return collect 
#end def TABLESPELL




################################################

 


## slight modifications to this function, Nov 2020
## because MODELFOOTS is now Python dictionary, not list
def find_MSPEC(ROOFcr,OSPEC) :
  modelfootnum=None
  if OSPEC.refnum!=None : modelfootnum=OSPEC.refnum 
  else :
    for t in ROOFcr : 
      if t.type=="modelref" : modelfootnum=t.refnum
    ## change Nov 2020, comment this line out
    ## if modelfootnum==None and len(MODELFOOTS)==1 : modelfootnum=1 
    ## change Nov 2020, to try to reset if it is missing
    if modelfootnum==None and len(MODELFOOTS)==1 :
      modelfootnum=list(MODELFOOTS.keys())[0]
  if modelfootnum==None : raise Ex("modelfootnumnone")
  if modelfootnum not in MODELFOOTS : raise Ex("modelfootnumtwo")
  ## change Nov 2020, do not use modelfootnum-1 as index, it's a dictionary
  MSPEC=MODELFOOTS[modelfootnum]
  MSPEConlyif=MODELFOOTS_ONLYIF[modelfootnum]
  MSPECsubpop=MODELFOOTS_SUBPOP[modelfootnum]
  return MSPEC , MSPEConlyif , MSPECsubpop 
#end def find_MSPEC
## year 2020, proof=1











# find_M_O has been moved to moclarify module , Dec 22

##########################################################

##########################################################

def VECTOR_VARI_CLARIFY(VARIv,PATHc,PATHr) :
  RESv=[]
  CATv=[]
  for v in VARIv :
    result = variate_clarify(v,PATHc,PATHr)
    if result==None or result.type=="all" : continue 
    if result.type=="restrict" : RESv.append(result)
    if result.type=="cat" : CATv.append(result.text)
  RESv = UNIQUIZE_RESTRICT(RESv)
  CATv = UNIQUIZE_CAT(CATv)
  return CATv , RESv 
#end def VECTOR_VARI_CLARIFY

###################################################


