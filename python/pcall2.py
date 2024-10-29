# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import Ex
from bull import PCALL 
from bull2 import dsetname
from pcall4 import BEST_SORT_WAY , expand_bool
from generateV import generate_DPF , generate_DPF_mean_etc , generate_DPF_median

# PLACE_GSD has been moved to this file from pcall


# non-GSD-class functions bottom this file: 
# inputdset_vnamesetref_sortedtoo inputdset_vname_set_ref
# figure_newsort this_sorted_is_enough ghost_inflag_of 

###################################################


def PLACE_GSD(gsd1) :
  found=False
  for i in range(len(PCALL)) :
    PROC = PCALL[i]
    if PROC.__class__.__name__ != gsd1.__class__.__name__ : continue 
    if PROC.POSSIBLE_MATCH_D(gsd1) :
      PROC.UPDATE_D(gsd1)
      H = (i,0)
      return H
  PCALL.append(gsd1)
  H = (len(PCALL)-1,0) 
  return H 
#end def PLACE_GSD



###################################################


class gsdbase :
  dom="d"
  
  def ghost_check_1INP(self) :                # for base class gsdbase 
    ghost_inflag = ghost_inflag_of(self.inputref)
    self.make_real_ghostinflag=None
    if ghost_inflag!=None and ghost_inflag in self.vnlist :
       self.make_real_ghostinflag = ghost_inflag 
    self.ghost_inflag=None
  #end def ghost_check_1INP
  
  
  def ghost_check_2INP(self) :               # for base  class gsdbase 
    ghost_inflag1 = ghost_inflag_of(self.inputref1)
    ghost_inflag2 = ghost_inflag_of(self.inputref2)
    self.make_real_ghostinflag1=None
    self.make_real_ghostinflag2=None
    if ghost_inflag1!=None and ghost_inflag1 in self.vnlist1 :
       self.make_real_ghostinflag1 = ghost_inflag1 
    if ghost_inflag2!=None and ghost_inflag2 in self.vnlist2 :
       self.make_real_ghostinflag2 = ghost_inflag2 
    self.ghost_inflag=None
  #end def ghost_check_2INP
  
  
  def keeptheghost(self) :                   # for base class gsdbase 
    ghost_inflag = ghost_inflag_of(self.inputref)
    self.ghost_inflag = ghost_inflag
    ## most atomic-GSDs do not use this, just PRESORTC, if keep it as a ghost
  #end def keeptheghost 
  
#end class gsdbase 


########################################
######## MERGEIN #######################

def MERGEIN0(H1,H2,bylist,vnlist1=(),vnlist2=(),inflagname=None) :
  merobj = mergein(H1,H2,bylist,vnlist1,vnlist2,inflagname)
  H = PLACE_GSD(merobj)
  return H
#end def MERGEIN0


class mergein(gsdbase) :
  def __init__(self,H1,H2,bylist,vnlist1,vnlist2,inflagname=None) :
    self.vnlist1 = set(vnlist1)
    self.vnlist1.update(bylist)
    self.vnlist2 = set(vnlist2)
    self.vnlist2.update(bylist)
    self.inputref1=H1
    self.inputref2=H2
    self.inflagname=inflagname
    self.bylist=tuple(bylist)
    self.vnkeep=set(vnlist1)
    self.vnkeep.update(vnlist2)
    self.vnkeep.update(bylist)
    if inflagname != None : self.vnkeep.add(inflagname)
    self.sorted = figure_newsort(H1,self.vnlist1)
    self.ghost_check_2INP()
  #end def __init__          for mergein class 
  
  
  
  def POSSIBLE_MATCH_D(self,othr) :       # for mergein class 
    if ( self.inputref1!=othr.inputref1 or self.inputref2!=othr.inputref2 or 
         self.bylist!=othr.bylist  ) : return False 
    if ( self.inflagname!=None and othr.inflagname!=None and 
         self.inflagname!=othr.inflagname ) : return False
    overlap1 = self.vnlist1.intersection(othr.vnlist2) 
    overlap2 = self.vnlist2.intersection(othr.vnlist1)
    if ( (not overlap1.issubset(self.bylist)) or 
         (not overlap2.issubset(self.bylist)) ) : return False 
    return True 
  #end def POSSIBLE_MATCH_D            for mergein class
  
  
  def UPDATE_D(self,othr) :          # for mergein class
    if self.inflagname==None : self.inflagname=othr.inflagname 
    self.vnlist1.update(othr.vnlist1)
    self.vnlist2.update(othr.vnlist2)
    self.vnkeep.update(othr.vnkeep)
    # August, fixing ghost-inflag
    self.ghost_check_2INP()
  #end def UPDATE_D      for mergein class 
  
  ################################################
  
  def export(self) :      # for mergein class
    dref1 = dsetname(self.inputref1)
    dref2 = dsetname(self.inputref2)
    outref = dsetname(self.outputref)
    inflagmap1 = {}
    agvlist1 = [] 
    vcla = []
    screen1 = {}
    
    if ( self.inflagname!=None and self.make_real_ghostinflag2!=None and 
         self.make_real_ghostinflag2!=self.inflagname ) :
      inflagmap1[dref2] = self.make_real_ghostinflag2
      agvlist1.append( (self.inflagname,"int",None) )
      vcla.append( self.inflagname+"="+self.make_real_ghostinflag2+";" )
    
    elif self.inflagname!=None : 
      inflagmap1[dref2] = self.inflagname 
    elif self.make_real_ghostinflag2!=None :
      inflagmap1[dref2] = self.make_real_ghostinflag2 
    
    if self.make_real_ghostinflag1!=None :
      inflagmap1[dref1] = self.make_real_ghostinflag1 
    
    screen1[dref1] = set(self.vnlist1)
    screen1[dref2] = set(self.vnlist2)
    # Feb 10 bug fix : ghost not allow in screen 
    screen1[dref1].discard(self.make_real_ghostinflag1)
    screen1[dref2].discard(self.make_real_ghostinflag2)
    
    s = generate_DPF(inlist=(dref1,dref2),out=outref,
                     screen=screen1,outvnlist=set(self.vnkeep),
                     inflag_map=inflagmap1,RMJoption="m",bylist=self.bylist[:],
                     agv=agvlist1,classicals=vcla)
    return s 
    
  #end def export      for mergein class 
  
  ################################################
    
#end class mergein 






########////////////////////////////////
######## JOINBY ////////////////////////

def JOINBY1(H1,H2,bylist,vnlist1,vnlist2) :
  bylist2 = BEST_SORT_WAY(bylist)
  H3 = PRESORT(H1,bylist2)
  H4 = PRESORT(H2,bylist2)
  H5 = JOINBY0(H3,H4,bylist2,vnlist1,vnlist2)
  return H5
#end def JOINBY1 


def JOINBY0(H1,H2,bylist,vnlist1,vnlist2) :
  joinobj = joinby(H1,H2,bylist,vnlist1,vnlist2)
  H = PLACE_GSD(joinobj)
  return H
#end def JOINBY0


class joinby(gsdbase) :
  def __init__(self,H1,H2,bylist,vnlist1,vnlist2) :
    self.vnlist1=set(vnlist1)
    self.vnlist1.update(bylist)
    self.vnlist2=set(vnlist2)
    self.vnlist2.update(bylist)
    self.inputref1=H1
    self.inputref2=H2
    self.bylist=tuple(bylist)
    self.vnkeep=set(vnlist1)
    self.vnkeep.update(vnlist2)
    self.vnkeep.update(bylist)
    self.sorted = tuple(bylist)
    self.ghost_check_2INP()
  #end def __init__       for joinby class
  
  
  def POSSIBLE_MATCH_D(self,othr) :          # for joinby class
    if ( self.inputref1!=othr.inputref1 or self.inputref2!=othr.inputref2 or 
         self.bylist!=othr.bylist )  : return False 
    overlap1 = self.vnlist1.intersection(othr.vnlist2) 
    overlap2 = self.vnlist2.intersection(othr.vnlist1)
    if ( (not overlap1.issubset(self.bylist)) or 
         (not overlap2.issubset(self.bylist)) ) : return False 
    return True 
  #end def POSSIBLE_MATCH_D             for joinby class 
  
  
  def UPDATE_D(self,othr) :              # for joinby class 
    self.vnlist1.update(othr.vnlist1)
    self.vnlist2.update(othr.vnlist2)
    self.vnkeep.update(othr.vnkeep)
    self.ghost_check_2INP()
  #end def UPDATE_D                   for joinby class 
  
  ########################################################################
  
  def export(self) :      # for joinby class
    
    dref1 = dsetname(self.inputref1)
    dref2 = dsetname(self.inputref2)
    outref = dsetname(self.outputref)
    inflagmap1 = {}
    screen1 = {}
    
    if self.make_real_ghostinflag2!=None :
      inflagmap1[dref2] = self.make_real_ghostinflag2 
    
    if self.make_real_ghostinflag1!=None :
      inflagmap1[dref1] = self.make_real_ghostinflag1 
    
    screen1[dref1] = set(self.vnlist1)
    screen1[dref2] = set(self.vnlist2)
    # Feb 10 bug fix : ghost not allow in screen 
    screen1[dref1].discard(self.make_real_ghostinflag1)
    screen1[dref2].discard(self.make_real_ghostinflag2)
    
    s = generate_DPF(inlist=(dref1,dref2),out=outref,
                     screen=screen1,outvnlist=set(self.vnkeep),
                     inflag_map=inflagmap1,RMJoption="j",bylist=self.bylist[:])
    return s 
    
  #end def export                           for joinby class
  
  ########################################################################
  
#end class joinby 





########################################
######## READBY_DUO0 ###################

def READBY_DUO1(H1,H2,bylist,vnlist1,vnlist2) :
  bylist2 = BEST_SORT_WAY(bylist)
  H3 = PRESORT(H1,bylist2)
  H4 = PRESORT(H2,bylist2)
  H5 = READBY_DUO0(H3,H4,bylist2,vnlist1,vnlist2)
  return H5
#end def READBY_DUO1

def READBY_DUO0(H1,H2,bylist,vnlist1,vnlist2) :
  readobj = readby_duo(H1,H2,bylist,vnlist1,vnlist2)
  H = PLACE_GSD(readobj)
  return H
#end def READBY_DUO0


class readby_duo(gsdbase) :
  def __init__(self,H1,H2,bylist,vnlist1,vnlist2) :
    self.vnlist1=set(vnlist1)
    self.vnlist1.update(bylist)
    self.vnlist2=set(vnlist2)
    self.vnlist2.update(bylist)
    self.inputref1=H1
    self.inputref2=H2
    self.bylist=tuple(bylist)
    self.vnkeep=set(vnlist1)
    self.vnkeep.update(vnlist2)
    self.vnkeep.update(bylist)
    self.sorted = tuple(bylist)
    self.ghost_check_2INP()
  #end def __init__      for readby_duo class 
  
  ################
  
  def POSSIBLE_MATCH_D(self,othr) :           # for readby_duo class 
    if ( self.inputref1!=othr.inputref1 or self.inputref2!=othr.inputref2 or 
         self.bylist!=othr.bylist  ) : return False 
    vnboth = self.vnkeep.intersection(othr.vnkeep) 
    for v in vnboth : 
     if v     in self.vnlist1 and v not in othr.vnlist1 : return False 
     if v not in self.vnlist1 and v     in othr.vnlist1 : return False 
     if v     in self.vnlist2 and v not in othr.vnlist2 : return False 
     if v not in self.vnlist2 and v     in othr.vnlist2 : return False 
    return True 
  #end def POSSIBLE_MATCH_D         for readby_duo class 
  
  
  def UPDATE_D(self,othr) :            # for readby_duo class 
    for v in othr.vnkeep :
      if v not in self.vnkeep :
        if v in othr.vnlist1 : self.vnlist1.add(v) 
        if v in othr.vnlist2 : self.vnlist2.add(v) 
    self.vnkeep.update(othr.vnkeep) 
    self.ghost_check_2INP()
  #end def UPDATE_D                  for readby_duo class 
  
  
  ############################################################################
  
  def export(self) :                        # for readby_duo class 
    
    dref1 = dsetname(self.inputref1)
    dref2 = dsetname(self.inputref2)
    outref = dsetname(self.outputref)
    inflagmap1 = {}
    screen1 = {}
    
    if self.make_real_ghostinflag2!=None :
      inflagmap1[dref2] = self.make_real_ghostinflag2 
    
    if self.make_real_ghostinflag1!=None :
      inflagmap1[dref1] = self.make_real_ghostinflag1 
    
    screen1[dref1] = set(self.vnlist1)
    screen1[dref2] = set(self.vnlist2)
    # Feb 10 bug fix : ghost not allow in screen 
    screen1[dref1].discard(self.make_real_ghostinflag1)
    screen1[dref2].discard(self.make_real_ghostinflag2)
    
    s = generate_DPF(inlist=(dref1,dref2),out=outref,
                     screen=screen1,outvnlist=set(self.vnkeep),
                     inflag_map=inflagmap1,RMJoption="r",bylist=self.bylist[:])
    return s 
    
  #end def export                             for readby_duo class
  
  ############################################################################
  
#end class readby_duo






###/////////////////////////////////////
###///// PRESORT ///////////////////////

def PRESORT(H1,bylist1) :
  if bylist1==() : return H1 
  if this_sorted_is_enough(H1,bylist1) : return H1 
  sortobj = presortc(H1,bylist1)
  H2 = PLACE_GSD(sortobj) 
  return H2 
#end def PRESORT


class presortc(gsdbase) :
  def __init__(self,H1,bylist1) :
    self.inputref=H1
    self.bylist=tuple(bylist1)
    self.sorted=tuple(bylist1)
    self.vnlist=inputdset_vname_set_ref(H1)
    ## returns actual reference , not just copy !
    self.vnkeep=self.vnlist
    self.keeptheghost()
  #end def __init__           for presortc class 
  
  
  def POSSIBLE_MATCH_D(self,othr) :        # for presortc 
    return self.inputref==othr.inputref and self.bylist==othr.bylist 
  #end def POSSIBLE_MATCH_D                  for presortc 
  
  
  def UPDATE_D(self,othr):           # for presortc 
        pass
  #end def UPDATE_D                    for presortc 
  
  #####################################################################
  
  def export(self) :                          # for presortc class 
    
    dref1 = dsetname(self.inputref)
    outref = dsetname(self.outputref)
    screen1 = {}
    screen1[dref1] = set(self.vnlist)
    # Feb 10 bug fix, screen not the ghost 
    screen1[dref1].discard(self.ghost_inflag)

    s = generate_DPF(inlist=(dref1,),out=outref,
                     screen=screen1,outvnlist=set(self.vnkeep),
                     bylist=self.bylist[:],
                     JUSTSORT=True)
    return s 
    
  #end def export                               for presortc class
  
  #####################################################################
  
#end class presortc 


########################################
######## RESTRICT ######################

def RESTRICTIFY(H1,RESTRICTvec) :
  if len(RESTRICTvec)==0 : return H1 
  resobj = restrictifyc(H1,RESTRICTvec)
  H2 = PLACE_GSD(resobj)
  return H2 
#end def RESTRICTIFY   


class restrictifyc(gsdbase) :
  def __init__(self,H1,RESTRICTvec) :
    oldvnset , oldsorted = inputdset_vnamesetref_sortedtoo(H1)
    self.inputref = H1 
    self.sorted = oldsorted 
    self.vnlist = oldvnset  ## reference, not just copy
    self.vnkeep = oldvnset
    self.boolexpvec = RESTRICTvec
    self.boolexplogset = set()
    for p in RESTRICTvec : self.boolexplogset.add(p.restrict_logno)
    self.ghost_check_1INP()
  #end def __init__                  for restrictifyc class 
  
  
  def  POSSIBLE_MATCH_D(self,othr) :           # for restrictifyc class 
    return self.inputref==othr.inputref and self.boolexplogset==othr.boolexplogset
  #end def POSSIBLE_MATCH_D                      for restrictify class 
  
  
  def UPDATE_D(self,othr) :           # for restrictifyc 
        pass
  #end def UPDATE_D                                      for restrictifyc
  
  
  
  ##############################################################
  
  
  def export(self) :             # for restrictifyc class 
    screen1={}
    agvlist1=[]
    dref1=dsetname(self.inputref)
    outref=dsetname(self.outputref)
    screen1[dref1]=set(self.vnlist)
    # Feb 10 bug fix : ghost not allow in screen 
    screen1[dref1].discard(self.make_real_ghostinflag)

    if self.make_real_ghostinflag != None :
      agvlist1.append( (self.make_real_ghostinflag,"int","1") )
    
    ss = [None]*len(self.boolexpvec)
    for k in range(len(ss)) :
      ss[k]=expand_bool(self.boolexpvec[k])
    
    s = generate_DPF(inlist=(dref1,),out=outref,screen=screen1,
                     outvnlist=set(self.vnkeep) , 
                     agv=agvlist1,restricts=ss )
    return s 
  #end def export                     for restrictifyc class 
  
  ###############################################################
  
#end class restrictifyc 


########################################
######## SEL_DISTINCT ##################

def SEL_DISTINCT1(H1,bylist) :
  bylist2=BEST_SORT_WAY(bylist)
  H2=PRESORT(H1,bylist2)
  H3=SEL_DISTINCT0(H2,bylist2)
  return H3
#end def SEL_DISTINCT1


def SEL_DISTINCT0(H1,bylist) :
  distobj=sel_distinct(H1,bylist)
  H=PLACE_GSD(distobj)
  return H
#end def SEL_DISTINCT0


class sel_distinct(gsdbase) :
  def __init__(self,H1,bylist) :
    self.inputref=H1
    self.bylist=tuple(bylist)
    self.sorted=tuple(bylist)
    self.vnlist=set(bylist)
    self.vnkeep=set(bylist)
    self.ghost_inflag=None
  #end def __init__       for sel_distinct
  
  
  def POSSIBLE_MATCH_D(self,othr) :           # for sel_distinct
    return self.inputref==othr.inputref and self.bylist==othr.bylist 
  #end def POSSIBLE_MATCH_D                     for sel_distinct
  
  
  def UPDATE_D(self,othr) :         # for sel_distinct
       pass
  #end def UPDATE_D                   for sel_distinct
  
  #####################################################
  
  def export(self) :                         # for sel_distinct class 
    dref1 = dsetname(self.inputref)
    outref=dsetname(self.outputref)
    screen1={}
    screen1[dref1] = set(self.vnlist) 
    sel1 = [ (None,"distinct",None) ]
    
    # Feb 11 , no empty screen statement
    # if len(screen1[dref1])==0 :
    #   impose_dummy_var(self.inputref,screen1,dref1)
    # but above wont do any good, because if bylist is empty sel_distinct will not work
    
    s = generate_DPF(inlist=(dref1,),out=outref,screen=screen1,
                     outvnlist=set(self.vnkeep),bylist=self.bylist[:],
                     select_list=sel1)
    return s
    
  #end def export                              for sel_distinct class
  
  #####################################################
  
#end class sel_distinct


########################################
######## SEL_N #########################

def SEL_N_1(H1,bylist,nameN="n") :
  bylist2=BEST_SORT_WAY(bylist)
  H2=PRESORT(H1,bylist2)
  H3=SEL_N_0(H2,bylist2,nameN)
  return H3
#end def SEL_N_1 


def SEL_N_0(H1,bylist,nameN="n") :
  nobj = sel_n(H1,bylist,nameN)
  H=PLACE_GSD(nobj)
  return H
#end def SEL_N_0


class sel_n(gsdbase) :
  def __init__(self,H1,bylist,nameN) :
    self.inputref=H1
    self.bylist=tuple(bylist)
    self.sorted=tuple(bylist)
    self.vnlist=set(bylist)
    self.vnkeep=set(bylist)
    self.vnkeep.add(nameN)
    self.nameN=nameN
    self.ghost_inflag=None
  #end def __init__        for class sel_n
  
  
  def POSSIBLE_MATCH_D(self,othr) :           # for class sel_n
    return ( self.inputref==othr.inputref and self.bylist==othr.bylist and
             self.nameN==othr.nameN  )
  #end def POSSIBLE_MATCH_D                     for class sel_n
  
  def UPDATE_D(self,othr) :                # for class sel_n
       pass
  #end def UPDATE_D                             for sel_n
  
  ##########################################
  
  def export(self) :                         # for sel_n class 
    dref1 = dsetname(self.inputref)
    outref=dsetname(self.outputref)
    screen1={}
    screen1[dref1] = set(self.vnlist) 
    sel1 = [ (self.nameN,"n",None) ]
    
    # Feb 11 , no empty screen statement
    if len(screen1[dref1])==0 :
      impose_dummy_var(self.inputref,screen1,dref1)
    
    s = generate_DPF(inlist=(dref1,),out=outref,screen=screen1,
                     outvnlist=set(self.vnkeep),bylist=self.bylist[:],
                     select_list=sel1)
    return s
    
  #end def export                              for sel_n class
  
  ##########################################
  
#end class sel_n


########################################
######## SEL_MEAN //////////////////////

def SEL_MEAN1(H1,bylist,nameSRC,statchoice) :
  bylist2=BEST_SORT_WAY(bylist)
  H2=PRESORT(H1,bylist2)
  H3=SEL_MEAN0(H2,bylist2,nameSRC,statchoice)
  return H3
#end def SEL_MEAN1


def SEL_MEAN0(H1,bylist,nameSRC,statchoice) :
  meanobj = sel_mean(H1,bylist,nameSRC,statchoice)
  H=PLACE_GSD(meanobj)
  return H
#end def SEL_MEAN0 


class sel_mean(gsdbase) :
  def __init__(self,H1,bylist,nameSRC,statchoice) :
    self.inputref=H1
    self.bylist=tuple(bylist)
    self.sorted=tuple(bylist)
    self.nameSRC=nameSRC
    self.summstats = set([statchoice])
    self.vnlist = set(tuple(bylist)+(nameSRC,))
    self.vnkeep = set(tuple(bylist)+(statchoice,))
    self.ghost_inflag=None
  #end def __init__                for class sel_mean
  
  
  
  def   POSSIBLE_MATCH_D(self,othr) :          # for class sel_mean
    if self.inputref!=othr.inputref : return False
    if self.bylist!=othr.bylist : return False 
    if self.nameSRC!=othr.nameSRC : return False
    return True
  #end def POSSIBLE_MATCH_D                      for class sel_mean
  
  
  def UPDATE_D(self,othr) :              # for class sel_mean
    self.summstats.update(othr.summstats)
    self.vnkeep.update(othr.vnkeep)
  #end def UPDATE_D                        for class sel_mean
  
  ###################################################################
  
  # remember : std is a special case 
  
  def export(self) :                         # for sel_mean class 
    
    dref1 = dsetname(self.inputref)
    outref=dsetname(self.outputref)
    screen1={}
    screen1[dref1] = set(self.vnlist) 
    sel1=[]
    
    for w in self.summstats :
      sel1.append( (w,w,self.nameSRC) )
    
    s = generate_DPF_mean_etc(inlist=(dref1,),out=outref,screen=screen1,
                     outvnlist=set(self.vnkeep),bylist=self.bylist[:],
                     select_list=sel1)
    return s
    
  #end def export                              for sel_mean class
  
  ###################################################################
  
#end class sel_mean 



########################################
######## SEL_MEDIAN ####################

def SEL_MEDIAN1(H1,bylist,nameSRC) :
  bylist2=BEST_SORT_WAY(bylist)
  H2=PRESORT(H1,bylist2)
  H3=SEL_MEDIAN0(H2,bylist2,nameSRC)
  return H3
#end def SEL_MEDIAN1


def SEL_MEDIAN0(H1,bylist,nameSRC) :
  medobj = sel_median(H1,bylist,nameSRC)
  H=PLACE_GSD(medobj)
  return H
#end def SEL_MEDIAN0


class sel_median(gsdbase) :
  def __init__(self,H1,bylist,nameSRC) :
    self.inputref=H1
    self.bylist=tuple(bylist)
    self.sorted=tuple(bylist)
    self.nameSRC=nameSRC
    self.vnlist = set(tuple(bylist)+(nameSRC,))
    self.vnkeep = set(tuple(bylist)+("median",))
    self.ghost_inflag=None
  #end def __init__                   for sel_median
  
  
  def  POSSIBLE_MATCH_D(self,othr) :              # for class sel_median
    return ( self.inputref==othr.inputref and self.bylist==othr.bylist and
             self.nameSRC==othr.nameSRC  )
  #end def POSSIBLE_MATCH_D                        for class sel_median
  
  
  def UPDATE_D(self,othr) :              # for class sel_median
      pass
  #end def UPDATE_D                        for class sel_median
  
  ######################################
  
  # tougher than you think , function called by gen_DPF will have to 
  #    do extra work for both std and median 
  
  def export(self) :                         # for sel_median class 
    dref1 = dsetname(self.inputref)
    outref=dsetname(self.outputref)
    screen1={}
    screen1[dref1] = set(self.vnlist) 
    sel1 = [ ("median","median",self.nameSRC) ]
    
    s = generate_DPF_median(inlist=(dref1,),out=outref,screen=screen1,
                     outvnlist=set(self.vnkeep),bylist=self.bylist[:],
                     select_list=sel1)
    return s
    
  #end def export                              for sel_median class
  
  ##########################################
  
#end class sel_median


########################################
######## EASYCALC ######################

def EASYCALC(H1,requestvec,vnlist,vncreate) :
  calcobj = easycalc_c(H1,requestvec,vnlist,vncreate)
  H = PLACE_GSD(calcobj)
  return H
#end def EASYCALC


class easycalc_c(gsdbase) :
  def __init__(self,H1,requestvec,vnlist,vncreate) :
    self.inputref = H1 
    self.requestvec = requestvec 
    self.vnlist = set(vnlist)
    self.vncreate = set(vncreate)
    self.vnkeep = set(vnlist) 
    self.vnkeep.update(vncreate)
    
    oldvnset , oldsorted = inputdset_vnamesetref_sortedtoo(H1)
    
    self.spell = set()
    self.leftvals = set() 
    self.sorted = [] 
    for subvec in requestvec : 
      self.leftvals.add(subvec[0]) 
      for s in subvec :
        if s not in ("=","-","+","*","/","0","1") :
          self.spell.add(s)
    
    for s in oldsorted : 
      if s in vnlist and s not in self.leftvals : self.sorted.append(s) 
      else : break 
    self.sorted = tuple(self.sorted)
    
    self.ghost_check_1INP()
    
  #end def __init__                    for easycalc_c
  
  
  
  def POSSIBLE_MATCH_D(self,othr) :                  # for class easycalc_c
    if self.inputref!=othr.inputref : return False 
    if self.vnlist!=othr.vnlist or self.vncreate!=othr.vncreate : return False
    if self.requestvec!=othr.requestvec : return False 
    return True
  #end def POSSIBLE_MATCH_D                            for class easycalc_c
  
  
  def UPDATE_D(self,othr) :                         #  for class easycalc_c
      pass
  #end def UPDATE_D                                    for class easycalc_c
  
  
  ##########################################################################
  
  
  def export(self) :                    # for easycalc_c class 
    agvlist1 = []
    classicals = []
    
    dref1 = dsetname(self.inputref)
    outref = dsetname(self.outputref)
    screen1={}
    screen1[dref1]=set(self.vnlist)
    # Feb 10 bug fix : don't put ghost into screen 
    screen1[dref1].discard(self.make_real_ghostinflag)
    
    for item in self.requestvec :
      classical1 = "".join(item) + " ;" 
      classicals.append(classical1)
    
    if self.make_real_ghostinflag != None :
      agvlist1.append( (self.make_real_ghostinflag,"int","1") )
    
    for w in self.vncreate :
      if w=="n" or (len(w)>=3 and w[:2]=="n_") or w=="thisrowq" :
          agvlist1.append( (w,"int",None) )
      if w=="pct" :
          agvlist1.append( (w,"flo",None) )
    
    s = generate_DPF(inlist=(dref1,),out=outref,screen=screen1,
                     outvnlist=set(self.vnkeep),
                     agv=agvlist1,
                     classicals=classicals)
    
    return s
    
  #end def export                        for easycalc_c class 
  
  
  ############################################################
  
  
#end class easycalc_c




########################################
######## EXP ###########################

def EXP0(CATvec,VALRANGE_MAP) :
  RANGES = {} 
  for c in CATvec :
    if c in VALRANGE_MAP : RANGES[c] = frozenset(VALRANGE_MAP[c])
  eobj = exp_c(RANGES) 
  H = PLACE_GSD(eobj) 
  return H 
#end def EXP0


class exp_c(gsdbase) :
  def __init__(self,RANGES) :                 
    self.CAT_RANGES = RANGES 
    self.ghost_inflag=None 
    self.sorted=()
    self.vnkeep=set()
    for v in RANGES : self.vnkeep.add(v)
  #end def __init__                          for exp_c
  
   
  def POSSIBLE_MATCH_D(self,othr) :           # for exp_c
    if self.CAT_RANGES!=othr.CAT_RANGES : return False
    return True 
  #end def POSSIBLE_MATCH_D                     for exp_c
  
  
  def UPDATE_D(self,othr) :                # for exp_c
       pass
  #end def UPDATE_D                          for exp_c
  
  
  #######################################################################
  
  def export(self) :                      # for exp_c class
    
    outref=dsetname(self.outputref)
    agvlist1=[]
    list_vn=[]
    for v in self.CAT_RANGES : list_vn.append(v)
    list_vn.sort()
    strlist=[""]
    for v in list_vn :
      litvec = self.CAT_RANGES[v]
      strlist = exphelp(strlist,v,litvec)
      if litvec[0][0].isdigit() : dt="int"
      elif litvec[0][0] in ("\"","\'") : dt="str"
      else : raise Ex("exp_c_strint_neither")
      if dt=="str" :
        m=1 
        for val in litvec :
          if m<len(val)-2 : m=len(val)-2
        agvlist1.append( (v,dt,None,m) )
      if dt=="int" :
        agvlist1.append( (v,dt,None) )
    
    
    s=generate_DPF(inlist=(),out=outref,screen={},outvnlist=set(self.vnkeep),
                   agv=agvlist1,classicals_rg=strlist)
    # classicals_rg , not classicals, rg~row generator
    return s 
    
  #end def export                             for exp_c class 
  
#end class exp_c 

##########################

def exphelp(sofar_strings,vname,list_values) :
  newlist=[]
  for s1 in sofar_strings :
    for val in list_values :
      s = s1 + vname + "=" + val + "; " 
      newlist.append(s)
  return newlist
#end def exphelp 



###################################################################




def NULLZEROFY(H1,zerovnlist) :
  zeroobj = nullzerofyc(H1,zerovnlist)
  H2 = PLACE_GSD(zeroobj)
  return H2 
#end def NULLZEROFY


class nullzerofyc(gsdbase) :
  def __init__(self,H1,zerovnlist) : 
    self.inputref=H1
    oldvnset , oldsorted = inputdset_vnamesetref_sortedtoo(H1)
    self.zerovnlist = set(zerovnlist)
    self.vnlist = set(oldvnset) 
    self.vnkeep = self.vnlist 
    self.sorted = oldsorted 
    for v in oldsorted :
      if v in zerovnlist : self.sorted = () 
    self.ghost_check_1INP()
  #end def __init__                     for class nullzerofyc
  
  
  def POSSIBLE_MATCH_D(self,othr) :               # for class nullzerofyc
    if ( self.inputref!=othr.inputref or self.vnlist!=othr.vnlist or 
         self.zerovnlist!=othr.zerovnlist ) : return False 
    return True 
  #end def POSSIBLE_MATCH_D                         for class nullzerofyc
  
  
  def UPDATE_D(self,othr) :             # for class nullzerofyc
      pass
  #end def UPDATE_D                       for class nullzerofyc
  
  
  ########################################################
  
  def export(self) :                            # for nullzerofyc class
    
    dref1 = dsetname(self.inputref)
    outref = dsetname(self.outputref)
    screen1={}
    screen1[dref1] = set(self.vnlist)
    # Feb 10 bug fix : ghost not allow in screen 
    screen1[dref1].discard(self.make_real_ghostinflag)
    
    classicals=[]
    agvlist1=[]
    
    for v in self.zerovnlist : 
      s = "if (" + v + " is null) " + v + "=0;"
      classicals.append(s)
    
    if self.make_real_ghostinflag!=None :
      agvlist1.append( (self.make_real_ghostinflag,"int","1") )
    
    
    s=generate_DPF(inlist=(dref1,),out=outref,screen=screen1,outvnlist=set(self.vnkeep),
                   agv=agvlist1,classicals=classicals)
    return s 
    
  #end def export                                 for nullzerofyc class
  
  #########################################################
  
#end class nullzerofyc



##################################################################



def EMPTYDS0() :
  emptyobj = emptydataset()
  H = PLACE_GSD(emptyobj)
  return H
#end def EMPTYDS0


class emptydataset(gsdbase) :
  def __init__(self) :       
    self.vnkeep = set(["_dummy_"])
    self.sorted = ()
    self.ghost_inflag = None 
  #end def __init__                 for class emptydataset
  
  
  # careful, choice here (False/True) is tricky 
  def POSSIBLE_MATCH_D(self,othr) :        # for class emptydataset
    return True
  #end def POSSIBLE_MATCH_D                  for class emptydataset
  
  
  def UPDATE_D(self,othr) :       # for class emptydataset
      pass
  #end def UPDATE_D                         for class emptydataset 
  
  #######################################################
  
  def export(self) :                            # for emptydataset class
    outref = dsetname(self.outputref)
    agvlist1=[ ("_dummy_","int","1") ]
    s=generate_DPF(inlist=(),out=outref,screen={},outvnlist=set(self.vnkeep),
                   agv=agvlist1)
    return s 
  #end def export                                 for emptydataset class
  
  #######################################################
  
#end class emptydataset

#######################################################


class incomingdataset(gsdbase) :
  def __init__(self,dsetname,vname_set,ghost_inflag) :
    self.vnkeep = set(vname_set)
    self.ghost_inflag = ghost_inflag
    self.datasetname = dsetname
    self.sorted = () 
  #end def __init__                   for class incomingdataset
  
#end class incomingdataset


########################################################



# at bottom of _init_,update call
# self.ghost_check_2INP()
# or
# self.ghost_check_1INP()


#######################################################


def inputdset_vnamesetref_sortedtoo(H) :
  i=H[0]
  j=H[1]
  PROC=PCALL[i]
  if PROC.dom=="d" : obj=PROC
  elif PROC.dom=="m" : obj=PROC.OLIST[j]
  return obj.vnkeep , obj.sorted[:]
#end def inputdset_vnamesetref_sortedtoo



def inputdset_vname_set_ref(H) :
  i=H[0]
  j=H[1]
  PROC=PCALL[i]
  if PROC.dom=="d" : obj=PROC
  elif PROC.dom=="m" : obj=PROC.OLIST[j]
  return obj.vnkeep 
#end def inputdset_vname_set_ref



def figure_newsort(H,vnameinuse) :
  i=H[0]
  j=H[1]
  PROC=PCALL[i]
  if PROC.dom=="d" : obj=PROC
  elif PROC.dom=="m" : obj=PROC.OLIST[j]
  newsort=[]
  for s in obj.sorted :
    if s not in vnameinuse : break 
    newsort.append(s)
  return tuple(newsort)
#end def figure_newsort 



def this_sorted_is_enough(H,bylist) :
  i=H[0]
  j=H[1]
  PROC=PCALL[i]
  if PROC.dom=="d" : obj=PROC
  elif PROC.dom=="m" : obj=PROC.OLIST[j]
  if len(bylist)==0 : return True 
  if len(bylist) > len(obj.sorted) : return False
  return (obj.sorted[0:len(bylist)]==bylist)
#end def this_sorted_is_enough



def ghost_inflag_of(H) :
  i=H[0]
  j=H[1]
  PROC=PCALL[i]
  if PROC.dom=="d" : obj=PROC
  elif PROC.dom=="m" : return None
  return obj.ghost_inflag
#end def ghost_inflag_of



########################################

def get_dummy_var(H) :
  i=H[0]
  j=H[1]
  PROC=PCALL[i]
  if PROC.dom=="d" : obj=PROC
  elif PROC.dom=="m" : obj=PROC.OLIST[j]
  ghost = None 
  if "ghost_inflag" in obj.__dict__ : ghost=obj.ghost_inflag
  vn2 = list(obj.vnkeep)
  vn2.sort()
  v = vn2[0] 
  if v==ghost : v=vn2[1]
  return v
#end def get_dummy_var

def impose_dummy_var(inputref,screenhold,dref) :
  v = get_dummy_var(inputref)
  screenhold[dref].add(v)
#end def impose_dummy_var
# at the moment , used by sel_distinct and sel_n
# but to deal with weirder corner cases : may need to 
# use recode statements and use in more subclasses   :(


######################################################
