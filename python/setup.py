# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


import os 

def execute_at_shell(cmdstr) :
  os.system(cmdstr)


# assorted small classes here

c_r_setting = None
MARK_COUNTER = {}

def reset_c_r_setting(w) :
  global c_r_setting , MARK_COUNTER
  c_r_setting = w 
  # July 2011 , for mark_parsenode
  MARK_COUNTER = {} 
#end def reset_c_r_setting


class parsenode() :
  def __init__(self) :
    self.c_r=c_r_setting
    self.type=None
    self.text=None
    self.text2nd=None
    self.under=[]
    self.understyle=None
    self.opvec=None
    self.refnum=None
    self.literalrange=None
    self.restrict_logno=None
    self.boolprint=None
    self.synthetic_vname=None
    self.mark_num = None 
    self.mark1 = None
    self.mark2 = None
  #end def __init__     for parsenode
#end class parsenode



def mark_parsenode(p,text) :
  global c_r_setting , MARK_COUNTER
  if c_r_setting not in ("c","r") : return 
  if p.c_r not in ("c","r") : raise Ex("markparsenode1")
  if text not in MARK_COUNTER :
    MARK_COUNTER[text] = 1 
  else :
    MARK_COUNTER[text] = MARK_COUNTER[text] + 1
  p.mark_num = MARK_COUNTER[text]
  p.mark1 = text
  p.mark2 = text + "." + p.c_r + str(p.mark_num)


####################################################################
### these two small classes added to this file Feb 2021


class ExternalMetaStruct :
  def __init__(self) :
    self.seqno=None
    self.refnum=None
    self.input_vn=None
    self.onlyif=None
    self.subpop=None
    self.sortby_ext=None
    self.OUTPUT_METAS = []


# THIS IS UNFINISHED : missing attr.s or attr.s unexpectedly == None
# can we solve this by initializing to [] instead of None???
# I believe that solves it: initialize to [] or {} , not None
class ExtOutputMetaStruct :
  def __init__(self) :
    self.out_seqno = None
    self.pseudo_filename = None
    self.vnames = set()
    self.cat_vn = []
    self.stat_vn = []
    self.filter_vn = []
    self.filter_values = []
    self.cat_sendto = []
    self.requested_recodes = {}
    self.auto_recodes = {}


### also this small class added Feb 2021
class FineTuneInfo :
  def __init__(self) :
    self.num_digits = None
    self.num_digits_as_list = None

######################################################

class cnode() :
  def __init__(self) :
    self.element=None
    self.under=[]
  #end def __init__   for cnode
#end class cnode 



class knownobj() :
  def __init__(self) :
    self.vnames=None    # or set()? None probably good
    self.storage=None
    self.vnamesf=None
    self.dtypes=None
    self.strlengths=None
    self.input_st_seen=False
    self.stated_clevs=None
    self.shadowed_vnames=None
    self.parity=None
  #end def __init__        for knownobj
#end class knownobj


class subpopdenomobject() :
  def __init__(self) :
    self.RESTRICTv=[]
    self.CATv=[]
    self.VARIv=[]
  #end def __init__    for subpopdenomobject
#end class subpopdenomobject




class dsnode_top() :
  def __init__(self) :
    self.maxsofar=0
    self.dsrange=[]
    self.dsetarray=[]
    self.ds_how={}
    self.vn_how={}
    self.vnall=set()
    self.ds=[]
    self.vn=[]
  #end def __init__    for dsnode_top
#end class dsnode_top 


class dsnode() :
  def __init__(self) :
    self.top = dsnode_top()
    self.depth=0
    self.dset=None
    self.under=[]
  #end def __init__     for dsnode 
#end class dsnode



class ddobj() :
  def __init__(self) :
    self.vnames = set([])
    self.parity = None
    self.hidden_vnames = None
    self.ghost_inflag = None
  #end def __init__     for ddobj
#end class ddobj



class Ex(Exception) :
  pass
  
  
  
