# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import Ex, cnode , parsenode
from bull import COL_PTRANS_TREE , ROW_PTRANS_TREE , \
                 COL_PARSE_TREE , ROW_PARSE_TREE

from pneed_hp import PROCESS_THIS_LEAF0

################################################

def PTRANS(under1,LP) :
  ## under1 is a cnode , LP is list of parsenodes 
  # LP.empty() change to LP==[]
  if LP==[] : return 
  Q=LP[0]
  # if IS_SINGLE_TELE(Q) :
  if Q.type not in ("multiplygrp","parengrp","coltop","rowtop") :
   under2=cnode()
   under2.element=Q
   under1.under.append(under2)
   if len(LP) >= 2 :
     LP2 = LP[1:] 
     PTRANS(under2,LP2)
  elif Q.type=="multiplygrp" :
   LP2=Q.under + LP[1:] 
   PTRANS(under1,LP2)
  elif (Q.type in ("parengrp","coltop","rowtop")) :
   for u in Q.under :
     LP2 = [u] + LP[1:] 
     PTRANS(under1,LP2)
#end def PTRANS

###################################################


def execPTRANS() :
  global ROW_PTRANS_TREE , COL_PTRANS_TREE
  
  # ROW_PTRANS_TREE = cnode()   (not here)
  LP0 = [ ROW_PARSE_TREE ]
  PTRANS(ROW_PTRANS_TREE,LP0)
  
  # COL_PTRANS_TREE = cnode()    (not here)
  LP0 = [ COL_PARSE_TREE ]
  PTRANS(COL_PTRANS_TREE,LP0)
  
  embed_R_inC_1(COL_PTRANS_TREE)
  
#end def execPTRANS


####################################################


def embed_R_inC_1(p) :
  if len(p.under) > 0 :
    for u in p.under :
      embed_R_inC_1(u) 
  else :
    embedRinC(p,ROW_PTRANS_TREE)
#end def embed_R_inC_1


def embedRinC(h,g) :
  for u in g.under :
    u2 = cnode() 
    u2.element = u.element 
    h.under.append(u2)
    embedRinC(u2,u)
#end def embedRinC


# PROCESS_EACH(COL_PTRANS_TREE,[])

def PROCESS_EACH(p,L) :
  if len(p.under) > 0 :
    for u in p.under :
      L2 = L + [u.element] 
      PROCESS_EACH(u,L2)
  else :
    ## Feb 2021 - change spelling of function you call
    PROCESS_THIS_LEAF0(p,L)
#end def PROCESS_EACH


#############################













