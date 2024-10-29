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

from generateS import generate_S_chi , generate_S_lm

##################################################




# class names :
# gssMbase , lm , chisq ,
# gssObase , pwise , chisqpval , coef , fstats 



####### M-CLASSES ################

####### M , BASE ################

class gssMbase :
  dom = "m"
  def __init__(self) : 
    self.OLIST = [] 
    self.OLIST_TYPES = set()
    self.normalinputvarnames = set() 
    self.specialoption_set = set() 
    self.specialoption = None 
    self.bylist = None 
    self.bylist2 = None 
    self.inputref = None 
  #end def __init__ for gssMbase
  
  ##########################################
  
  def getVARINAME(self,p) :      # in class gssMbase 
    vnspell=None
    if p.type=="word" :
      if p.text not in AVAILABLEVNAMES : return None 
      self.normalinputvarnames.add(p.text)
      return p.text 
    ## for THISROWCAT,THISROW?,N,SRC
    if p.type in VARIATORS_VARNAMESUBSTITUTES :
      if p.type=="thisrowcat" :  vnspell=translateTHISROWCAT() 
      if p.type=="thisrow?"   :  vnspell="thisrow?"
      if p.type=="n"          :  vnspell="n" 
      if p.type=="src"        :  vnspell=translateSRC() 
      if p.type in ("n","thisrow?") : self.specialoption_set.add(p.type)
      if vnspell in AVAILABLEVNAMES : self.normalinputvarnames.add(vnspell)
      return vnspell 
    return None 
  #end def getVARINAME for gssMbase 
  
  
  #   translateSRC and translateTHISROWCAT 
  #   will return None or found-vname as string 
  #   remember: IS_VNAMEPRODUCT must also think about variators 
  
#end class gssMbase

##################################
####### M , CHISQ CLASS ##########

class chisq(gssMbase) :
  multallow = { "chisqpval":False }
  def __init__(self) :
    gssMbase.__init__(self)
    self.vnliststyle = None 
    self.mainvnamelist = None 
  #end def __init__ for chisq 
  
  
  #  CHISQ, (M , not O) 
  #  CHISQ(V V V) or CHISQ(V*V*V)
  
  def mo_clarify(self,p) :        # for chisq
    vnlist=[]
    if len(p.under)<1 : raise Ex("chisqmoclarify1")
    if p.understyle=="as_spacelist" :
      self.vnliststyle="normal"
      for u in p.under : vnlist.append(self.getVARINAME(u))
    elif p.understyle=="as_commalist" and p.under[0].type=="spacelist" :
      self.vnliststyle="normal"
      for u in p.under[0].under : vnlist.append(self.getVARINAME(u))
    elif p.under[0].type=="*expr" :
      self.vnliststyle="product"
      for u in p.under[0].under : vnlist.append(self.getVARINAME(u))
    if None in vnlist : raise Ex("chisqmoclarify2")
    self.mainvnamelist=vnlist
    
    if "thisrow?" in self.specialoption_set : self.specialoption = "thisrow?" 
    elif      "n" in self.specialoption_set : self.specialoption = "n_bridge" 
    return True 
    
  #end def mo_clarify for chisq 
  
  
  #########################################################
  
  
  def export(self) :                  # for chisq class
    vnames = set()
    countvar = None
    for v in self.mainvnamelist :
      if   v=="thisrow?" : vnames.add("thisrowq")
      elif v=="n"        : countvar="n"
      else               : vnames.add(v)
    sortlist = self.bylist2
    inpfile = fullfilepath(self.inputref)
    if len(self.OLIST) != 1 : raise Ex("lenolistchisq")
    obj = self.OLIST[0]
    outfile = fullfilepath(obj.outputref)
    D={}
    D["chisqpval"] = [ (outfile,"voidparam") ]
    s = generate_S_chi(D,inpfile,sortlist,vnames,countvar)
    return s 
  #end def export                    # for chisq class 
  
#end class chisq



################################
####### M , POLY CLASS #########

## GSS, M-type, Y=POLY non-optional

## lm , for class object, not instance :
## i.e. multallow[odset_classname] = True or False 

class lm(gssMbase) :
  multallow = {"pwise":True , "coef":True , "fstats":True} 
  
  def  __init__(self) :     # for class lm 
    gssMbase.__init__(self)
    self.dependentvar = None 
    self.plusminuslist = None 
    self.termlist = None 
    self.termlist_type = None 
  #end def __init__   for lm 
  
  ##########################################
  
  def mo_clarify(self,p) :           # for lm class
    q=p.under[0]
    if q.type != "=expr" : raise Ex("lmmoclarify1")
    if len(q.under) != 2 : raise Ex("lmmoclarify2")
    if (not isVARINAME(q.under[0])) : raise Ex("lmmoclarify3")
    self.dependentvar = self.getVARINAME(q.under[0]) 
    self.termlist = [] 
    self.termlist_type = [] 
    r=q.under[1] 
    if r.type == "+-expr" :
      self.plusminuslist = r.opvec 
      for g in r.under :
        t1 , t2 = self.mo_clarify_vnameterm(g) 
        self.termlist.append(t1) 
        self.termlist_type.append(t2) 
    else :
      self.plusminuslist = [None] 
      t1 , t2 = self.mo_clarify_vnameterm(r) 
      self.termlist.append(t1) 
      self.termlist_type.append(t2)
    
    if "thisrow?" in self.specialoption_set : self.specialoption = "thisrow?" 
    elif      "n" in self.specialoption_set : self.specialoption = "n_bridge" 
    return True 
    
  #end def mo_clarify    for lm class 
  
  #############################################################
  
  def mo_clarify_vnameterm(self,p) :        # for lm class 
    vnlist=[] 
    if p.type=="intliteral" and p.text=="1" : return (["1"],"1")
    elif p.type=="*expr" : 
      termtype="*" 
      for u in p.under : vnlist.append(self.getVARINAME(u)) 
    elif p.type=="/expr" : 
      termtype="/" 
      for u in p.under : vnlist.append(self.getVARINAME(u))
    elif isVARINAME(p) : 
      termtype="SINGLE" 
      vnlist.append(self.getVARINAME(p))
    else : raise Ex("moclarterm1") 
    for v in vnlist : 
      if v==None : raise Ex("moclarterm2")
    return ( vnlist , termtype ) 
    
  #end def mo_clarify_vnameterm    for lm class
  
  #################################################
  
  def modeleqn_poly_str(self) :         # for lm class
    fv=[]
    term2=[]
    if len(self.termlist)!=len(self.plusminuslist) : raise Ex("polystr1")
    for i in range(len(self.termlist)) :
      mop = self.termlist_type[i]
      v = self.termlist[i] 
      # use the R interaction symbol, ":"
      if   mop=="*" : term2.append( ":".join(v) )
      elif mop=="/" : term2.append( "/".join(v) )
      else          : term2.append(v[0])
    for i in range(len(self.plusminuslist)) :
      op = self.plusminuslist[i] 
      if op==None : op=""
      fv.append( op+term2[i] )
    s = self.dependentvar + "~" + "".join(fv) 
    return s
  #end def modeleqn_poly_str             for lm class
  
  #######################
  
  def export(self) :                  # for lm class
    D={}
    allvn = self.normalinputvarnames
    contvn = allvn.intersection(declared_continuous)
    catvn = allvn.difference(contvn)
    sortlist = self.bylist2
    inpfile = fullfilepath(self.inputref)
    modeleqn_str = self.modeleqn_poly_str()
    for i in range(len(self.OLIST)) :
      obj = self.OLIST[i] 
      infotype = obj.__class__.__name__  
      param_str = obj.param_as_str()
      outfile = fullfilepath(obj.outputref)
      if infotype not in D : D[infotype] = []
      D[infotype].append( (outfile,param_str) )
    s = generate_S_lm(D,inpfile,sortlist,catvn,contvn,modeleqn_str)
    return s 
  #end def export                    # for lm class 
  
  
#end class lm

###################################################



################################
####### O-CLASSES ##############

####### O , BASE ###############

class gssObase :
  dom = "o"
  def __init__(self) :
    self.vnkeep = set() 
    self.vnkeep.update(self.__class__.standardvnames)
    self.Mref = None 
    self.sorted = () 
    self.bylist = None 
    self.bylist2 = None 
  #end def __init__       for gssObase class
  
  ##############################
  
  #### to do  gssO.mo_clarify1(O-EXPR parsenode) 
  
  def mo_clarify1(self,p) :     # for gssObase
    g = self.mo_clarify(p)
    if g==True : return True 
    if p.understyle=="as_commalist" :
      for p2 in p.under : 
        g = self.mo_clarify(p2) 
        if g==True : return True 
    return False 
  #end def mo_clarify1      for gssObase class 
  
  #######################
  
  ## put this at the BASE O-class 
  def mo_clarify_post_generic(self) :      # for gssObase class
    self.vnkeep.update(self.__class__.standardvnames)   # __class__ is overkill?
    self.vnkeep.update(self.Mref.bylist)
  #end def mo_clarify_post_generic    for gssObase class
  
  ##################################
  
  def genericPSAT(self,gssMref,ROOFcr) :      # for gssObase class
    bylist=gssMref.bylist
    OUTPUTCOL_CONST={}
    OUTPUTCOL_ROOFINDEX={}
    if "utp_values" in self.__dict__ :
      if len(self.utp_values)==1 :
        utpvec=list(self.utp_values)
        utp=utpvec[0]
        OUTPUTCOL_CONST[self.utpcolumnname] = utp 
    for i in range(len(ROOFcr)) :
      t=ROOFcr[i]
      if t.type=="cat" and t.text in bylist : 
        OUTPUTCOL_ROOFINDEX[t.text]=i
    return OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST
  #end def genericPSAT    for gssObase class
  
#end class gssObase 



#########################################
####### O , PAIRWISE CLASS ##############

# GSS , O-type , PAIRWISE

class pwise(gssObase) :
  ## OBJECT , NOT INSTANCE 
  standardvnames = set(["est_pw","err_pw","t_pw","df_pw","pval_pw"]) 
  def __init__(self) :
    gssObase.__init__(self)
    ## self.vnkeep.update(standardvnames)    (gssObase__init__ does this)
    self.level1 = None 
    self.level2 = None 
    self.effect = None
    self.effect2 = None 
    ## not this class , but others 
    ## self.utp_values = set() 
  #end def __init__      for pwise class
  
  ########################################
  
  def mo_clarify(self,p) :       # for pwise class 
    c=IS_VNAMEPRODUCT(p)
    if c!=False : 
      self.effect=c 
      return True 
    c=IS_DIFF_CLEVLIST(p) 
    if c!=False :
      self.level1=c[0] 
      self.level2=c[1] 
      return True 
    if not IS_LIST(p) : return False 
    
    c1 = IS_VNAMEPRODUCT(p.under[0]) 
    if c1!=False :
      self.effect=c1 
      c2=IS_DIFF_LITLIST(p.under[1]) 
      if c2!=False :
        self.level1=c2[0]
        self.level2=c2[1] 
        return True 
      if len(p.under)<3 : return True 
      c2=IS_LITLIST(p.under[1]) 
      c3=IS_LITLIST(p.under[2]) 
      if ( c2!=False and c3!=False ) :
        self.level1=c2 
        self.level2=c3 
        return True 
      return True 
    
    else  :       # no vnameproduct found 
      c2=IS_DIFF_CLEVLIST(p.under[0]) 
      if c2!=False :
        self.level1=c2[0] 
        self.level2=c2[1] 
        return True 
      if len(p.under)<2 : return False
      c2=IS_CLEVLIST(p.under[0])
      c3=IS_CLEVLIST(p.under[1])
      if (c2!=False and c3!=False) :
        self.level1=c2 
        self.level2=c3 
        return True 
      return False 
  #end def mo_clarify             for pwise class
  
  
  #################################################
  #################################################
  
  ## PWISE O-class
  
  def mo_clarify_post(self,CAT_FREQ) :      # for pwise class
    self.effect2=[]
    lev1={}
    lev2={}
    modelinput1 = self.Mref.normalinputvarnames 
    if self.effect==None :
      self.effect=[]
      if self.level1!=None : 
        for cl in self.level1 : self.effect.append(CLEV_TO_VNAME(cl))
      else : 
        for w in CAT_FREQ : 
          if CAT_FREQ[w]==2 and w in modelinput1 : 
            self.effect.append(w)
    
    for v in self.effect : 
      if v not in declared_continuous : self.effect2.append(v) 
    
    if self.level1!=None : 
      for i in range(len(self.level1)) : 
        lev1[self.effect2[i]] = self.level1[i] 
      self.level1 = lev1 
      for i in range(len(self.level2)) : 
        lev2[self.effect2[i]] = self.level2[i] 
      self.level2 = lev2 
    
    self.effect = set(self.effect)
    self.effect2 = set(self.effect2)
    ### late addition, May 25 follows 
    ### change in August, break out into generic helper fctn
    self.vnkeep.update(double_vname_spelling(self.effect2))   ## A_1 A_2 B_1 B_2
    self.mo_clarify_post_generic()
    
  #end def mo_clarify_post     for pwise class 
  
  
  ################################################################
  
  def returnPSAT(self,ROOFcr) :         # for pwise class 
    OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST = self.genericPSAT(self.Mref,ROOFcr)
    
    if self.level1!=None :
      for w in self.effect2 : 
        w1 = w + "_1" 
        w2 = w + "_2" 
        OUTPUTCOL_CONST[w1] = self.level1[w] 
        OUTPUTCOL_CONST[w2] = self.level2[w] 
    else : 
      chkEFF={}
      for g in self.effect2 : chkEFF[g]=0 
      for i in range(len(ROOFcr)) :
        t=ROOFcr[i]
        if t.type=="cat" and t.text in self.effect2 :
          vn = t.text 
          vn1 = vn+"_1" 
          vn2 = vn+"_2"
          if chkEFF[vn]==0 : OUTPUTCOL_ROOFINDEX[vn1]=i 
          elif chkEFF[vn]==1 : OUTPUTCOL_ROOFINDEX[vn2]=i 
          chkEFF[vn]=chkEFF[vn]+1 
    return OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST 
    
  #end def returnPSAT       for pwise class
  
  ##############################
  
  def param_as_str(self) :
    l = list(self.effect) 
    l.sort()
    s=":".join(l)
    return s
  #end def param_as_str      for pwise class
  
#end class pwise



#######################################################

class chisqpval(gssObase) :
  standardvnames = set(["chisqvalue","pvalue"]) 
  def __init__(self) :
    gssObase.__init__(self)
    ## self.vnkeep.update(standardvnames)   already done
  #end def __init__       for chisqpval class
  
  
  def mo_clarify(self,p) :             # for chisqpval class
    pass                              # so far, nothing to do
  #end def mo_clarify               # for chisqpval class
  
  
  def mo_clarify_post(self,CAT_FREQ) :        # for chisqpval class
    self.mo_clarify_post_generic()
  #end def mo_clarify_post          for chisqpval class
  
  
  def returnPSAT(self,ROOFcr) :               # for chisqpval class
    OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST = self.genericPSAT(self.Mref,ROOFcr)
    return OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST
  #end def returnPSAT     for chisqpval class
  
#end class chisqpval 



##############################################################
##############################################################


class coef(gssObase) :
  standardvnames = set(["est","err_c","t_c","pval_c"])
  def __init__(self) :
    gssObase.__init__(self)  
    self.level = None 
    self.effect = None
    self.effect2 = None 
  #end def __init__      for coef class

  def mo_clarify(self,p) :          # for coef class
    c=IS_VNAMEPRODUCT(p)
    if c!=False : 
      self.effect=c 
      return True 
    c=IS_CLEVLIST(p) 
    if c!=False :
      self.level=c
      return True 
    if len(p.under)<=1 : return False
    if not IS_LIST(p) : return False 
    
    c1 = IS_VNAMEPRODUCT(p.under[0]) 
    if c1!=False :
      self.effect=c1 
      if len(p.under)<=1 : return True
      c2 = IS_LITLISTremainder(p,1)
      if c2!=False : 
        self.level = c2
        return True
      c2 = IS_LITLIST(p.under[1])
      if c2!=False : 
        self.level = c2
        return True
      return True
    else :         # not VNPROD
      c2 = IS_CLEVLIST(p.under[0])
      if c2!=False :
        self.level = c2
        return True
      else : return False
    return False 
  #end def mo_clarify         for coef class

  ########################################
  
  ## COEF O-class
  
  def mo_clarify_post(self,CAT_FREQ) :      # for coef class
    self.effect2=[]
    lev={}
    modelinput1 = self.Mref.normalinputvarnames 
    if self.effect==None :
      self.effect=[]
      if self.level!=None : 
        for cl in self.level : self.effect.append(CLEV_TO_VNAME(cl))
      else : 
        for w in CAT_FREQ : 
          if CAT_FREQ[w]==1 and w in modelinput1 : 
            self.effect.append(w)
    
    for v in self.effect : 
      if v not in declared_continuous : self.effect2.append(v) 
    
    if self.level!=None : 
      for i in range(len(self.level)) : 
        lev[self.effect2[i]] = self.level[i] 
      self.level = lev 
    
    self.effect = set(self.effect)
    self.effect2 = set(self.effect2)
    self.vnkeep.update(self.effect2)   
    self.mo_clarify_post_generic()
    
  #end def mo_clarify_post     for coef class 
  
  
  ################################################################
  
  def returnPSAT(self,ROOFcr) :         # for coef class 
    OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST = self.genericPSAT(self.Mref,ROOFcr)
    
    if self.level!=None :
      for w in self.effect2 : 
        OUTPUTCOL_CONST[w] = self.level[w] 
    else : 
      chkEFF={}
      for g in self.effect2 : chkEFF[g]=0 
      for i in range(len(ROOFcr)) :
        t=ROOFcr[i]
        if t.type=="cat" and t.text in self.effect2 :
          vn = t.text 
          if chkEFF[vn]==0 : OUTPUTCOL_ROOFINDEX[vn]=i 
          chkEFF[vn]=chkEFF[vn]+1 
    return OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST 
    
  #end def returnPSAT       for coef class
  
  ##############################
  
  def param_as_str(self) :
    l = list(self.effect) 
    l.sort()
    s=":".join(l)
    return s
  #end def param_as_str      for coef class
  
#end class coef






########################################################
#######################################################

class fstats(gssObase) :
  standardvnames = set(["fvalue","numerator_df","denominator_df","pvalue"]) 
  def __init__(self) :
    gssObase.__init__(self)
    ## self.vnkeep.update(standardvnames)   already done
  #end def __init__       for fstats class
    
  def mo_clarify(self,p) :             # for fstats class
    pass                              # so far, nothing to do
  #end def mo_clarify               # for fstats class
  
  def mo_clarify_post(self,CAT_FREQ) :        # for fstats class
    self.mo_clarify_post_generic()
  #end def mo_clarify_post          for fstats class
  
  def returnPSAT(self,ROOFcr) :               # for fstats class
    OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST = self.genericPSAT(self.Mref,ROOFcr)
    return OUTPUTCOL_ROOFINDEX , OUTPUTCOL_CONST
  #end def returnPSAT     for fstats class

  def param_as_str(self) :
    return "voidparam"
  #end def param_as_str      for fstats class

#end class fstats 





##################################################################
##################################################################



