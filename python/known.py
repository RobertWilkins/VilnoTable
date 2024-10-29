# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 

from setup import knownobj, execute_at_shell , Ex

from bull import inline_vdt_log_filename, preview_vdt_dataset_filename, \
      KNOWNDSETS, DIRREFS, AVAILABLEVNAMES, DSETS_USED_WITH_THINGS, \
      KNOWNCLEVdense, KNOWNCLEVdense_VNAME, KNOWNCLEVdense_notdifficult, \
      KNOWNCLEVwordlike, \
      dset_order_preview , dset_order_inlinevdt , dset_bad_abba_usage



##################################################

## June 2011, changes to get relative reverse-age info for datasets 


def getINLINE_VDT_LOG() :
  
  file1 = open(inline_vdt_log_filename,'r')
  speclines = file1.readlines()
  file1.close()
  
  dirpre1a = speclines[0].split()
  if dirpre1a[0] != "{DIRREFS}" : raise Ex("vdtlogdirref")
  dirpre1 = dirpre1a[1:]
  dir1 = {}
  i=0 
  while i+1 < len(dirpre1) :
    dir1[ dirpre1[i] ] = dirpre1[i+1] 
    i = i + 2
  
  for d in dir1 :
    if d in DIRREFS :
      if dir1[d]!=DIRREFS[d] : raise Ex("vdtlogdirref2")
    else : DIRREFS[d] = dir1[d] 
  
  ############################################################
  
  ## June 2011 , add dset ordering info 
  dorder_pre1a = speclines[1].split()
  if dorder_pre1a[0] != "{DATASET-CREATION-ORDER}" : raise Ex("vdtlog_dorder")
  dorder_pre1 = dorder_pre1a[1:]
  dset_order_inlinevdt.append(dorder_pre1)
  
  ############################################################
  
  twinpre1a = speclines[2].split()
  if twinpre1a[0] != "{TWINS}" : raise Ex("vdtlogtwin")
  twinpre1 = twinpre1a[1:]
  twins = set(twinpre1)
  
  validpre1a = speclines[3].split()
  if validpre1a[0] != "{DREFVALID}" : raise Ex("vdtlogdrefvalid")
  validpre1 = validpre1a[1:]
  drefvalid = {}
  i=0 
  while i+1 < len(validpre1) :
    drefvalid[ validpre1[i] ] = validpre1[i+1] 
    i = i + 2
  
  ############################################################
  
  ## June 2011 , add badABBAconvert info 
  badabba_pre1a = speclines[4].split()
  if badabba_pre1a[0] != "{BAD-ABBA-USAGE}" : raise Ex("vdtlog_badabba")
  badabba_pre1 = badabba_pre1a[1:]
  dset_bad_abba_usage.update(badabba_pre1)
  
  ############################################################
  
  created_asc = {}
  created_vdt = {}
  vname_collect = set()
  
  mainlines = speclines[5:]
  for r in mainlines :
    delimiter=None
    strnull=None
    met1 = r.split(",")
    metf = met1[0].split()
    storage = metf[0]
    dref = metf[1]
    vnlist = met1[1].split()
    dtlist1 = met1[2].split()    # formatted as : int str flo 
    slen1 = met1[3].split()
    slen2 = [] 
    for x in slen1 : slen2.append( int(x) ) 
    if storage=="asc" :
      delim1 = met1[4].split()
      snull1 = met1[5].split()
      if len(delim1)>=2 and delim1[0]=="delimiter" :
        delimiter = delim1[1]
        if delimiter=="c" : delimiter=","
      if len(snull1)>=2 and snull1[0]=="strnullflag" :
        strnull = snull1[1] 
    
    obj = knownobj()
    obj.storage = storage 
    obj.vnames = set(vnlist)   # unordered set of vnames , 
    vname_collect.update(obj.vnames)
    # vnames needed much more often than original structs: vnamesf , dtypes , strlengths
    obj.vnamesf = vnlist       # the vnames , in order as stored in file
    obj.dtypes = dtlist1       # parallel to vnamesf 
    obj.strlengths = slen2     # for slots in vnamesf/dtypes that are string
    # so far, python code does not need to know delimiter/strnullflag 
    if storage=="asc" : created_asc[dref] = obj 
    if storage=="vdt" : created_vdt[dref] = obj
  
  
  KNOWNVNAMEupdate(vname_collect)
  anycreated = set()
  anycreated.update( created_asc.keys() )
  anycreated.update( created_vdt.keys() )
  
  for d in anycreated :
    if ( d in created_vdt and d not in created_asc and d in twins and 
         d in KNOWNDSETS and KNOWNDSETS[d].storage in ("asc","a+v") ) :
        KNOWNDSETS[d].storage = "a+v"
        if KNOWNDSETS[d].vnamesf != created_vdt[d].vnamesf : raise Ex("vdtlogmatch1")
  
    elif ( d in created_asc and d not in created_vdt and d in twins and 
           d in KNOWNDSETS and KNOWNDSETS[d].storage in ("vdt","a+v") ) :
        KNOWNDSETS[d].storage = "a+v"
        if KNOWNDSETS[d].vnamesf != created_asc[d].vnamesf : raise Ex("vdtlogmatch2")
  
    else :
      if d in KNOWNDSETS :
        if d in DSETS_USED_WITH_THINGS : raise Ex("vdtlogthingmismatch")
        del KNOWNDSETS[d] 
      if d in created_asc and not (d in drefvalid and drefvalid[d]=="vdt>asc") :
        KNOWNDSETS[d]=created_asc[d]
        KNOWNDSETS[d].storage="asc"
        if d in twins : KNOWNDSETS[d].storage="a+v"
      elif d in created_vdt and not (d in drefvalid and drefvalid[d]=="asc>vdt") :
        KNOWNDSETS[d]=created_vdt[d]
        KNOWNDSETS[d].storage="vdt"
        if d in twins : KNOWNDSETS[d].storage="a+v"
      if d not in KNOWNDSETS : raise Ex("vdtlogmatch3")     
      #                        should be there by now
      KNOWNDSETS[d].input_st_seen = False 
      KNOWNDSETS[d].stated_clevs = None 
      KNOWNDSETS[d].shadowed_vnames = None  # parseINP might change this 
      KNOWNDSETS[d].parity = None
  
#end def getINLINE_VDT_LOG


###################################################################


## is the next 15 lines of code throwaway code ?

##  # if storage=="asc" and dref in valid1 and valid1[dref]=="vdt>asc" : continue 
##  # if storage=="vdt" and dref in valid1 and valid1[dref]=="asc>vdt" : continue 

##  if dref in KNOWNDSETS : KNOWNDSETS_overwritten_dset_cleanup(dref) 
##  KNOWNDSETS[dref] = knownobj()    # if already there, is overwritten 
##  KNOWNDSETS[dref].vnames = set(vnlist)
##  KNOWNDSETS[dref].input_st_seen=False   # at least for moment, parseINP will set to true
##  KNOWNDSETS[dref].stated_clevs = None 
##  KNOWNDSETS[dref].shadowed_vnames = None  # parseINP might change this 
##  KNOWNDSETS[dref].parity = None

##  KNOWNDSETS[dref].storage = storage       # vdt or asc 
##  if dref in twins : KNOWNDSETS[dref].storage = "a+v" 

##  KNOWNDSETS[dref].vnames_vec = vnlist
##  KNOWNDSETS[dref].dtypes_vec = dtlist1 
##  KNOWNDSETS[dref].strlengths = slen2 
##  KNOWNDSETS[dref].delimiter = 


##################################################################
##################################################################

# remember: ".dat" vs ".txt"

# format thru quickpreview : 
# fullfilename , v v v , str int flo , 8 3

def previewCOLSPECSvdt(datref) :
  dref5 = datref.split("/")
  if len(dref5)!=2 or dref5[0] not in DIRREFS : raise Ex("previewvdtdirref1")
  dirref = dref5[0]
  shortdset = dref5[1] 
  filename = DIRREFS[dirref] + "/" + shortdset + ".dat" 
  cmd_str = "vilnopreview " + filename 
  execute_at_shell(cmd_str)
  
  file1 = open(preview_vdt_dataset_filename,'r')
  speclines = file1.readlines()
  file1.close()
  
  met1 = speclines[0].split(",")
  metf = met1[0].split()
  fullfilename2 = metf[0]
  if fullfilename2 != filename : raise Ex("previewvdtfname1") 
  
  vnlist = met1[1].split()
  dtlist1 = met1[2].split()    # formatted as : int str flo 
  slen1 = met1[3].split()
  slen2 = [] 
  for x in slen1 : slen2.append( int(x) ) 
  
  if datref in KNOWNDSETS : raise Ex("previewvdtknown1")
  
  # June 2011, record order in which dataset previewed 
  dset_order_preview.append(datref) 
  
  KNOWNDSETS[datref] = knownobj()    # if already there, is overwritten 
  KNOWNDSETS[datref].vnames = set(vnlist)
  KNOWNVNAMEupdate( KNOWNDSETS[datref].vnames )
  KNOWNDSETS[datref].input_st_seen=False   # at least for moment, parseINP will set to true
  KNOWNDSETS[datref].stated_clevs = None 
  KNOWNDSETS[datref].shadowed_vnames = None  # parseINP might change this 
  KNOWNDSETS[datref].parity = None
  
  KNOWNDSETS[datref].storage = "vdt"       # vdt or asc 
  
  KNOWNDSETS[datref].vnamesf = vnlist       # the vnames , in order as stored in file
  KNOWNDSETS[datref].dtypes = dtlist1       # parallel to vnamesf 
  KNOWNDSETS[datref].strlengths = slen2     # for slots in vnamesf/dtypes that are string
  
#end def previewCOLSPECSvdt


#####################################################################

# format in first row of ascii data file :
# {COL..}, v v v , str int flo , 8 3 , delimiter c , strnullflag _nul


def previewCOLSPECSasc(datref) :
  dref5 = datref.split("/")
  if len(dref5)!=2 or dref5[0] not in DIRREFS : raise Ex("previewascdirref1")
  dirref = dref5[0]
  shortdset = dref5[1] 
  filename = DIRREFS[dirref] + "/" + shortdset + ".txt" 
  
  file1 = open(filename,'r')
  specline = file1.readline()
  file1.close()
  
  delimiter="|"
  strnull=""
  met1 = specline.split(",")
  vnlist = met1[1].split()
  dtlist1 = met1[2].split()    # formatted as : int str flo 
  slen1 = met1[3].split()
  slen2 = [] 
  for x in slen1 : slen2.append( int(x) ) 
  
  if len(met1)>=5 :
    delim1 = met1[4].split()
    if len(delim1)>=2 and delim1[0]=="delimiter" :
      delimiter = delim1[1]
      if delimiter=="c" : delimiter=","
  
  if len(met1)>=6 :
    snull1 = met1[5].split()
    if len(snull1)>=2 and snull1[0]=="strnullflag" :
      strnull = snull1[1] 
  
  if datref in KNOWNDSETS : raise Ex("previewascknown1")
  
  # June 2011, record order in which dataset previewed 
  dset_order_preview.append(datref) 
  
  KNOWNDSETS[datref] = knownobj()   
  KNOWNDSETS[datref].vnames = set(vnlist)
  KNOWNVNAMEupdate( KNOWNDSETS[datref].vnames )
  KNOWNDSETS[datref].input_st_seen=False   # at least for moment, parseINP will set to true
  KNOWNDSETS[datref].stated_clevs = None 
  KNOWNDSETS[datref].shadowed_vnames = None  # parseINP might change this 
  KNOWNDSETS[datref].parity = None
  
  KNOWNDSETS[datref].storage = "asc"       # vdt or asc 
  
  KNOWNDSETS[datref].vnamesf = vnlist       # the vnames , in order as stored in file
  KNOWNDSETS[datref].dtypes = dtlist1       # parallel to vnamesf 
  KNOWNDSETS[datref].strlengths = slen2     # for slots in vnamesf/dtypes that are string
  
#end def previewCOLSPECSasc






####################################################################

## is this function still needed ?
## def KNOWNDSETS_overwritten_dset_cleanup(dref) 
## if dref in request_convert_ab : del request_convert_ab[dref] 
## if dref in request_convert_ba : del request_convert_ba[dref] 
## if dref in DSETS_USED_WITH_THINGS : raise 



#################################################################



# this version being replaced Feb 1
def KNOWNCLEVupdate_olderversion(vname,clevs) :
  for w in clevs :
    if w[0].isdigit() : 
      KNOWNCLEVdense.add(w)
      KNOWNCLEVdense_VNAME[w] = vname 
    elif w[0].isalpha() or w[0]=='_' :
      KNOWNCLEVdense.add(w)
      KNOWNCLEVdense.add("\""+w+"\"")
      KNOWNCLEVdense.add("\'"+w+"\'")
      KNOWNCLEVdense_VNAME[w] = vname
      KNOWNCLEVdense_VNAME["\""+w+"\""] = vname
      KNOWNCLEVdense_VNAME["\'"+w+"\'"] = vname
    elif w[0] in ("\"","\'") :
      w2 = w[1:-1]
      KNOWNCLEVdense.add("\""+w2+"\"")
      KNOWNCLEVdense.add("\'"+w2+"\'")
      KNOWNCLEVdense_VNAME["\""+w2+"\""] = vname
      KNOWNCLEVdense_VNAME["\'"+w2+"\'"] = vname
      wordchk=True
      for c in w2 :
        if not (c.isdigit() or c.isalpha() or c=="_") : wordchk=False
      if not (w2[0]=="_" or w2[0].isalpha()) : wordchk=False
      if wordchk : 
        KNOWNCLEVdense.add(w2)
        KNOWNCLEVdense_VNAME[w2] = vname 
#end def KNOWNCLEVupdate_olderversion

############################################################


def KNOWNCLEVupdate(vname,clevs) :
  for c in clevs :
    difficult = False 
    if c[0].isdigit() : 
      KNOWNCLEVdense.add(c)
      KNOWNCLEVdense_VNAME[c] = vname 
      KNOWNCLEVdense_notdifficult.add(c)
    else :   # string, not int clevel 
      if c[0] in ("\"","\'") and c[-1]!=c[0] : raise Ex("knownclevupdatequ")
      if c[0] in ("\"","\'") : w0 = c[1:-1]
      elif c[0].isalpha() or c[0]=='_' : w0 = c
      else : raise Ex("knownclevupdate7")
      w1 = "\"" + w0 + "\""
      w2 = "\'" + w0 + "\'"
      has_singlequote =  ( "\'" in w0 )
      has_doublequote =  ( "\"" in w0 )
      wordchk=True
      if not (w0[0].isalpha() or w0[0]=="_") : wordchk=False
      for a in w0 :
        if not (a=="_" or a.isalnum()) : wordchk=False
      if wordchk==True :  KNOWNCLEVwordlike.add(w0)
      if c[0] not in ("\"","\'") and wordchk==False : raise Ex("knownclevupdatebadclev")

      w_all = (w0,w1,w2)
      KNOWNCLEVdense.update(w_all)
      for w in w_all : KNOWNCLEVdense_VNAME[w] = vname

      if w0 not in AVAILABLEVNAMES and wordchk==True : 
        KNOWNCLEVdense_notdifficult.update(w_all)
#end def KNOWNCLEVupdate


#############################################################


# call this function not too early, when AVAILABLEVNAMES is fixed
def prep_KNOWNCLEVdense_notdiff() :
  badspell = set() 
  for v in AVAILABLEVNAMES :
    if v in KNOWNCLEVdense :
      badspell.update( (v,"\""+v+"\"","\'"+v+"\'") )
  KNOWNCLEVdense_notdifficult = KNOWNCLEVdense.difference(badspell)
#end def prep_KNOWNCLEVdense_notdiff

################################################

def KNOWNVNAMEupdate(vnameset) :
  newvn = vnameset.difference(AVAILABLEVNAMES)
  AVAILABLEVNAMES.update( newvn )
  problem1 = newvn.intersection(KNOWNCLEVwordlike)
  if len(problem1)>0 :
    problem2 = problem1.copy()
    for c in problem1 : problem2.update( ("\""+c+"\"","\'"+c+"\'") )
    KNOWNCLEVdense_notdifficult.difference_update(problem2)






