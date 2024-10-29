# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import Ex
from bull import ANY_O_SPELLINGS

from moclarify2 import lm, chisq, pwise, chisqpval, coef, fstats 
from moclarify3 import ttest, quartiles, tstat_and_pval, each_level, q1q3median

from mo_external import find_M_Oe

##################################################


######## class gssMbase, gssObase, lm, chisq, pwise, chisqpval, coef, fstats
########   have been moved to moclarify2.py

########################################################

# when you use a O-class with utp feature , use these :
# 
# class object , not instance : 
# utpcolumnname = "variablename" 
# in __init__ :
# utp_values = set() 

#########################################################
## M/O accounts

## Mindex = { "lm":lm , "chisq":chisq  }
## Oindex = { "pwise":pwise, "chisqpval":chisqpval,"coef":coef , "fstats":fstats }

### Important, put this back in when t-test and q1q3 are ready
## June 2017 add entries here for t-test and Q1/Q3/median 
Mindex = { "lm":lm , "chisq":chisq , "ttest":ttest, "quartiles":quartiles }
Oindex = { "pwise":pwise , "chisqpval":chisqpval , 
           "coef":coef , "fstats":fstats , 
           "tstat_and_pval":tstat_and_pval, "each_level":each_level , 
           "q1q3median":q1q3median }


MgiveOspell = {}
MgiveODSspell = {}
MODELCALLSDICT = Mindex

def prep_findMO() :
  for Mspell in Mindex :
    Mclass = Mindex[Mspell]
    MgiveOspell[Mspell] = set()
    MgiveODSspell[Mspell] = {}
    for ODSspell in Mclass.multallow.keys() :
      if ODSspell in Oindex :   # hey! still missing coef & fstats 
        Oclass = Oindex[ODSspell] 
        for argspell in Oclass.standardvnames :
          ### Feb 2021 , update ANY_O_SPELLINGS as well
          ANY_O_SPELLINGS.add(argspell)       ### this line Feb 19 , 2021
          MgiveOspell[Mspell].add(argspell)
          MgiveODSspell[Mspell][argspell] = ODSspell
          # issue: if 2 O-classes map to same M-class and 
          # share same variable name spelling -> problem
#end def prep_findMO


prep_findMO()  # execute now 

## Nov 2020 small edit, only one line at top of function
def find_M_O(MSPEC,OSPEC) :
  if MSPEC.type=="m_expr_ext" : return find_M_Oe(MSPEC,OSPEC)
  Mspell=MSPEC.text 
  Ospell=OSPEC.text
  if Mspell not in MgiveOspell : raise Ex("notavailableMspell1")
  availableOspell=MgiveOspell[Mspell]
  if Ospell not in availableOspell : raise Ex("notavailableOspell")
  ODSspell = MgiveODSspell[Mspell][Ospell]
  # Mclass=Mclass_module.__dict__[Mspell]
  # Oclass=Oclass_module.__dict__[ODSspell]
  Mclass=Mindex[Mspell]
  Oclass=Oindex[ODSspell]
  gssM = Mclass()
  gssO = Oclass()
  gssO.Mref = gssM
  return gssM , gssO 
#end def find_M_O



###################################################
###################################################



