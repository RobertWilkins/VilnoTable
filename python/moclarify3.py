# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import Ex

from bull import translateSRC , translateTHISROWCAT, CLEV_TO_VNAME, \
    VARIATORS_VARNAMESUBSTITUTES, AVAILABLEVNAMES, declared_continuous, \
    addbackquotes

# KNOWNCLEVdense KNOWNCLEVdense_notdifficult

from bull2 import fullfilepath 

from parse_we2 import IS_LITLIST , IS_CLEVLIST , IS_DIFF_LITLIST , \
       IS_DIFF_CLEVLIST , IS_VNAMEPRODUCT , \
       getVARINAMEo , isVARINAME , IS_LIST , double_vname_spelling , \
       IS_LITLISTremainder

from generateS import generate_S_ttest , generate_S_q1q3med

from moclarify2 import gssMbase, gssObase 

#############################################################################

# this is additions to moclarify.py 2017
# for t-test and Q1,Q3,median

# ttest class 
class ttest(gssMbase) :
  ## you may have ambiguous grammar o_expr_spelling left_paren , look into it
  ## at the moment, implementing tstat_and_pval, each_level later
  multallow = {"tstat_and_pval":False , "each_level":False} 
  def  __init__(self) :     # for class lm 
    gssMbase.__init__(self)
    self.dependentvar = None 
    self.groupvar = None 
    self.groupvar_level1 = None 
    self.groupvar_level2 = None
  #end def __init__   for ttest 
  def mo_clarify(self,p) :           # for ttest class
    ## expecting ttest(Y=trtgrp,"Placebo","500mg") syntax exactly
    ## subpop, or onlyif, if present comes after first three arguments
    if len(p.under) < 3 : raise Ex("ttmoclarify00")
    q=p.under[0]
    if q.type != "=expr" : raise Ex("ttmoclarify1")
    if len(q.under) != 2 : raise Ex("ttmoclarify2")
    if (not isVARINAME(q.under[0])) : raise Ex("ttmoclarify3")
    self.dependentvar = self.getVARINAME(q.under[0]) 
    if (not isVARINAME(q.under[1])) : raise Ex("ttmoclarify4")
    self.groupvar = self.getVARINAME(q.under[1])
    # do not use "thisrow?" or "n" feature in ttest expression
    # however, groupvar could be in "thisrowcat" format and 
    # dependentvar could be in "src" format, getVARINAME() will translate 
    # that to normal input variable name for you.
    q = p.under[1]
    if (q.type!="strliteral" and q.type!="intliteral") : raise Ex("ttmoclarify5")
    self.groupvar_level1 = q.text  # strliteral(quotes included), or intliteral
    q = p.under[2]
    if (q.type!="strliteral" and q.type!="intliteral") : raise Ex("ttmoclarify6")
    self.groupvar_level2 = q.text  # strliteral(quotes included), or intliteral
  def export(self) :                # for ttest class
    sortlist = self.bylist2
    inpfile = fullfilepath(self.inputref)
    # This is tricky: the ttest procedure will always produce two output 
    # datasets as automatic, but one of them might not be requested by an 
    # o-expression, so be careful here. In any case, OLIST has 1 or 2 items.
    # If the V-Table code does not request both of them, R code will silently 
    # drop one of them.
    D = {}
    if (len(self.OLIST)<1 or len(self.OLIST)>2) : raise Ex("ttestOLISTlength")
    for i in range(len(self.OLIST)) :
      obj = self.OLIST[i] 
      infotype = obj.__class__.__name__  
      if (infotype!="tstat_and_pval" and infotype!="each_level") :
          raise Ex("ttestOLISTinfotype")
      outfile = fullfilepath(obj.outputref)
      if infotype in D : raise Ex("ttest_infotype_onlyseeonce")
      D[infotype] = [ (outfile,"voidparam") ] 
    s = generate_S_ttest(D,inpfile,sortlist,
                         self.dependentvar,self.groupvar,
                         self.groupvar_level1,self.groupvar_level2)
    return s 
  #end def export                    # for ttest class 
  # end class ttest 

  # this is critical. CHISQ, unlike LM, does not require output datasets to 
  # be identified by a parameter spec (such as TRTGRP*GENDER). T-test and 
  # Q1/Q3/median are like chi-square in this respect. Most stat procedures 
  # are not as subtle as the lm() procedure: you have a number of categories 
  # of output datasets (for Q1/Q3, just one type of output file, for the 
  # t-test, only two types of output file), but for each type of output file,
  # the output file is UNIQUE, a parameter string is not needed.

class tstat_and_pval(gssObase) :
  standardvnames = set(["t_stat","pval_tt"])
  def __init__(self) :
    gssObase.__init__(self)  
  #end def __init__      for tstat_and_pval class
  def mo_clarify(self,p) :               # for tstat_and_pval class
    pass                                 # so far, nothing to do
  #end def mo_clarify                    # for tstat_and_pval class  
  def mo_clarify_post(self,CAT_FREQ) :   # for tstat_and_pval class
    self.mo_clarify_post_generic()
  #end def mo_clarify_post                 for tstat_and_pval class
  
  def returnPSAT(self,ROOFcr) :               # for tstat_and_pval class
    OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST = self.genericPSAT(self.Mref,ROOFcr)
    return OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST
  #end def returnPSAT                           for tstat_and_pval class
#end class tstat_and_pval

## tstat_and_pval now active, each_level not yet active 
## each_level will have only two rows, one for each subgroup 
## actual requests for each_level, not satisfied by mean(std) should be rare.
class each_level(gssObase) :           # each_level not yet active (for ttest)
  standardvnames = set(["n","mean","stddev"])
  def __init__(self) :
    gssObase.__init__(self)  
  #end def __init__      for each_level class
  def mo_clarify(self,p) :               # for each_level class
    pass                                 # so far, nothing to do
  #end def mo_clarify                    # for each_level class  
  def mo_clarify_post(self,CAT_FREQ) :   # for each_level class
    self.mo_clarify_post_generic()   # WHEN? TOP OR BOTTOM OF FUNCTION???
    modelinput1 = self.Mref.normalinputvarnames 
    self.groupvar = self.Mref.groupvar   # self.groupvar or just local groupvar?
    # may need to look at CAT_FREQ[.groupvar]
    self.vnkeep.add( self.Mref.groupvar  )  
    self.mo_clarify_post_generic()
  #end def mo_clarify_post                 for each_level class
  def returnPSAT(self,ROOFcr) :         # for each_level class 
    OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST = self.genericPSAT(self.Mref,ROOFcr)
    chkCAT_GROUPVAR = 0
    for i in range(len(ROOFcr)) :
        t=ROOFcr[i]
        if t.type=="cat" and t.text==self.groupvar :
          OUTPUTCOL_ROOFINDEX[self.groupvar]=i 
          chkCAT_GROUPVAR = chkCAT_GROUPVAR + 1 
    # at this point, chkCAT_GROUPVAR should be exactly 1, err-chk up to you
    if (chkCAT_GROUPVAR!=1) : raise Ex("ttest_eachlevel_wrongparity") 
    return OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST
  #end def returnPSAT       for each_level class
# end class each_level 



###################################################################
###################################################################

### Here begins the quartiles connector, for Q1, Q3, median 
### code above is for t-test connector


class quartiles(gssMbase) :
  multallow = {"q1q3median":False } 
  def  __init__(self) :     # for class quartiles
    gssMbase.__init__(self)
    self.cont_var = None    # continous var-name, going into model
  #end def __init__   for ttest 
  def mo_clarify(self,p) :           # for quartiles class
    if (len(p.under) < 1) : raise Ex("quartunderempty")
    q=p.under[0]
    if (not isVARINAME(q)) : raise Ex("moclarifyquart1")
    self.cont_var = self.getVARINAME(q) 
    # do not use "thisrow?" or "n" feature in quartiles expression
    # however, cont_var could be in "src" format, getVARINAME() will translate 
    # that to normal input variable name for you.
  def export(self) :                # for quartiles class
    sortlist = self.bylist2
    inpfile = fullfilepath(self.inputref)
    if len(self.OLIST) != 1 : raise Ex("lenolistquart2")
    D = {}
    obj = self.OLIST[0] 
    infotype = obj.__class__.__name__  
    if (infotype!="q1q3median") : raise Ex("quartOLISTinfotype")
    outfile = fullfilepath(obj.outputref)
    if infotype in D : raise Ex("quart_infotype_onlyseeonce")
    D[infotype] = [ (outfile,"voidparam") ] 
    s = generate_S_q1q3med(D,inpfile,sortlist,self.cont_var)
    return s 
  #end def export                    # for quartiles class 
# end class quartiles 

#####################################################################


class q1q3median(gssObase) :
  standardvnames = set(["q_min","q_max","q_median","q1","q3"]) 
  def __init__(self) :
    gssObase.__init__(self)
    ## self.vnkeep.update(standardvnames)   already done
  #end def __init__       for q1q3median class
  def mo_clarify(self,p) :             # for q1q3median class
    pass                              # so far, nothing to do
  #end def mo_clarify               # for q1q3median class
  def mo_clarify_post(self,CAT_FREQ) :        # for q1q3median class
    self.mo_clarify_post_generic()
  #end def mo_clarify_post          for q1q3median class
  def returnPSAT(self,ROOFcr) :               # for q1q3median class
    OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST = self.genericPSAT(self.Mref,ROOFcr)
    return OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST
  #end def returnPSAT     for q1q3median class
#end class q1q3median 

##########################################################################
##########################################################################
##########################################################################










