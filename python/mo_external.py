
### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 

from setup import Ex

from bull import AVAILABLEVNAMES , EXT_M2 , EXTERNAL_METAS ,  \
     EXTERNAL_STATPROC_TEXTS2

from bull2 import fullfilepath 

## need import something from generateS, but not this
## from generateS import generate_S_ttest , generate_S_q1q3med

from moclarify2 import gssMbase, gssObase 

############################################################################




# Here is the M/O module, for external stat-proc connector, will combine with 
# the older moclarify files

class gssMexternal(gssMbase) :
  # Jan 27 2021 , no EM input argument, take that input argument out
  # def __init__(self,EM) :
  def __init__(self) :
    gssMbase.__init__(self)
    ## self.normalinputvarnames.update(EM.input_vn)
  def mo_clarify(self):
    pass
  def export(self) :
    v2=[]
    tmp_inp_filename = fullfilepath(self.inputref)
    pre_text = "dataset0 <- read_ascii_datafile(\"" + tmp_inp_filename + "\")"
    if self.refnum not in EXTERNAL_STATPROC_TEXTS2 : raise Ex("exexport-index")
    text = EXTERNAL_STATPROC_TEXTS2[self.refnum]
    ## Feb 26 2021 bug fix, text is a LIST of lines of text, you forgot
    text = "\n".join(text)    ## this line added Feb 26 2021
    for od in self.OLIST :
      tmp_out_filename = fullfilepath(od.outputref)
      s = "write_ascii_datafile(" + od.pseudo_filename + "," +  \
          "\"" + tmp_out_filename + "\")" 
      v2.append(s)
    s2 = "\n".join(v2)
    text2 = pre_text + "\n" + text + "\n" + s2
    return text2
  ### end def export() - for class gssMexternal
##  end class gssMexternal







class gssOexternal(gssObase) :
  standardvnames = set() 
  def __init__(self) :
    gssObase.__init__(self)
  def mo_clarify1(self):
    pass
  def mo_clarify_post(self):
    pass
  def returnPSAT(self,ROOFcr) :        # for class gssOexternal
    # Jan 28 2021, comment this line out (handle bylist AFTERWARDS)
    # OUTPUTCOL_ROOFINDEX,OUTPUTCOL_CONST = self.genericPSAT(self.Mref,ROOFcr)
    OUTPUTCOL_CONST={}        ## March 3 2021
    OUTPUTCOL_ROOFINDEX={}    ## Oops! forgot to initialize!
    bylist0 = self.Mref.bylist
    slot_taken = {}
    found_a_place = {}
    for i in range(len(self.cat_vn)) :
      v1 = self.cat_vn[i]
      if self.cat_sendto[i]!=None  : v2 = self.cat_sendto[i]
      elif v1 in self.auto_recodes : v2 = self.auto_recodes[v1]
      else : v2 = v1
      for k in range(len(ROOFcr)) :
        t = ROOFcr[k]
        if t.type=="cat" and t.text==v2 and k not in slot_taken :
          OUTPUTCOL_ROOFINDEX[v1] = k
          slot_taken[k] = True
          found_a_place[v1] = True
          break
    for i in range(len(ROOFcr)) :
      t=ROOFcr[i]
      if t.type=="cat" and t.text in bylist0 and t.text not in self.cat_vn : 
        OUTPUTCOL_ROOFINDEX[t.text]=i
    for i in range(len(self.filter_vn)) :
      OUTPUTCOL_CONST[self.filter_vn[i]] = self.filter_values[i]
    return OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST
  ##  end returnPSAT() - gssOexternal
## end class gssOexternal

#############################################################################
#############################################################################

## Important limitation as regards spelling of column names in output datasets.
## For each custom model section, two different output datasets cannot have the
## same statistic name (with the same spelling).
## There is no limitation on the same statistic name spelling occurring in two
## or more custom model sections

def find_M_Oe(MSPEC,OSPEC) :
  Ospell = OSPEC.text
  Oslot = None
  out_spec = None
  EM = MSPEC.under[0]
  for k in range(len(EM.OUTPUT_METAS)) :
    if Ospell in EM.OUTPUT_METAS[k].stat_vn :
      out_spec = EM.OUTPUT_METAS[k]
      Oslot = k
      break
  if Oslot==None : raise Ex("no find stat name")  
  gssM = gssMexternal()
  gssO = gssOexternal()
  gssO.Mref = gssM
  gssM.em = EM
  gssM.normalinputvarnames.update(EM.input_vn)
  gssO.vnkeep.update(out_spec.vnames)
  gssM.sortby_ext = EM.sortby_ext
  gssO.cat_vn = out_spec.cat_vn
  gssO.cat_sendto = out_spec.cat_sendto
  gssO.auto_recodes = out_spec.auto_recodes
  gssO.requested_recodes = out_spec.requested_recodes
  gssO.stat_vn = out_spec.stat_vn
  gssO.filter_vn = out_spec.filter_vn
  gssO.filter_values = out_spec.filter_values
  gssM.seqno = EM.seqno
  gssM.refnum = EM.refnum
  gssO.out_seqno = out_spec.out_seqno
  gssO.pseudo_filename = out_spec.pseudo_filename
  return gssM , gssO
## end def find_M_Oe()


#############################################################################
#############################################################################

def gssM_gssO_template_set_up() :
  global EXT_M2 , EXTERNAL_METAS
  for EM in EXTERNAL_METAS :
    gssM = gssMexternal()
    gssM.seqno = EM.seqno
    gssM.refnum = EM.refnum
    gssM.em = EM
    gssM.OLIST = []
    gssM.OLIST_TYPES = set()
    gssM.inputref = None
    gssM.bylist = None
    gssM.bylist2 = None
    gssM.specialoption = None
    gssM.specialoption_set = set()
    gssM.normalinputvarnames = set(EM.input_vn)
    gssM.sortby_ext = EM.sortby_ext
    EXT_M2.append(gssM)
    for out_spec in EM.OUTPUT_METAS :
      gssO = gssOexternal()
      gssO.Mref = None   ## not til later!
      gssO.out_seqno = out_spec.out_seqno
      gssO.bylist = None
      gssO.bylist2 = None
      gssO.sorted = ()
      gssO.vnkeep = set(out_spec.vnames)
      gssO.cat_vn = out_spec.cat_vn
      gssO.cat_sendto = out_spec.cat_sendto
      gssO.auto_recodes = out_spec.auto_recodes
      gssO.requested_recodes = out_spec.requested_recodes
      gssO.stat_vn = out_spec.stat_vn
      gssO.filter_vn = out_spec.filter_vn
      gssO.filter_values = out_spec.filter_values
      gssO.pseudo_filename = out_spec.pseudo_filename
      gssM.OLIST.append(gssO)
### end of  gssM_gssO_template_set_up()






