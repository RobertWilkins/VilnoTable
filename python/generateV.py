# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 

from setup import Ex

# Feb 8 , switch screen=None to just screen 

def generate_DPF(inlist,out,screen,outvnlist,RMJoption=None,
              inflag_map=None,bylist=None,
              agv=None,classicals=None,classicals_rg=None,restricts=None,
              JUSTSORT=False,select_list=None) :
  
  if bylist==None : bylist=()
  
  if JUSTSORT==True :
    if len(inlist)!=1 : raise Ex("gendpfjustsort")
    s = ( "sort(" + inlist[0] + "->" + out + ") " + 
          " ".join(bylist) + " ;\n"  )
    return s 
  
  ########################################################
  
  # switch as to as8 , looks like as might be reserved keyword, syntax error
  a_st=""
  if agv!=None and agv!=[] :
    ai = []
    as8 = []
    af = []
    secni = ""
    secns = ""
    secnf = ""
    for g in agv :
      v = g[0]
      dt = g[1]
      initval = g[2]
      if dt=="str" : slen = g[3]
      p = v 
      if initval!=None : p += "="+initval
      if dt=="str" : p += " " + str(slen)
      if dt=="int" : ai.append(p)
      elif dt=="str" : as8.append(p)
      elif dt=="flo" : af.append(p)
    if ai!=[] : secni = " int: "   + " ".join(ai)
    if as8!=[] : secns = " str: "   + " ".join(as8)
    if af!=[] : secnf = " float: " + " ".join(af)
    a_st = "addgridvars " + secni + secns + secnf + " ;\n" 
  
  
  ########################################################
  
  procst = []
  
  if classicals_rg != None :
    for s1 in classicals_rg : procst .append( s1+" copyrow;" )
    procst.append( "deleterow;")
  if classicals!=None :
    for s1 in classicals : procst.append( s1 )
  if restricts!=None :
    for s1 in restricts :
      procst.append( "if (not(" + s1 + ")) deleterow;" )
  
  if procst!=[] : procst = "\n".join(procst) + "\n" 
  else : procst=""
  
  
  
  
  ###########################################################
  
  sel = ""
  if select_list!=None and select_list!=[] :
    if len(select_list)==0 : raise Ex("gendpfsel0")
    if len(select_list[0])!=3 : raise Ex("gendpfsel1")
    if select_list[0][1]=="distinct" :
      sel = "select distinct " + " ".join(bylist) + " ;\n" 
    else :
      L=[]
      bystr = ""
      if len(bylist)>0 : bystr = " by " + " ".join(bylist)
      for e in select_list :
        if len(e) != 3 : raise Ex("gendpf_three")
        vn , stattype , src = e 
        if src==None : src=""
        if stattype=="mean" : stattype="avg"
        p = vn + "=" + stattype + "(" + src + ")" 
        L.append(p)
      sel = "select " + " ".join(L) + bystr + " ;\n" 
  
  
  
  ##########################################################
  
  
  
  inlist_st = "inlist " + " ".join(inlist) + " ;\n" 
  
  
  screen_st=""
  if screen!=None and len(screen)>0 :
    scrvec1 = []
    for dref in screen :
      s1 = dref + ": " + " ".join(tuple(screen[dref]))
      scrvec1.append(s1)
    screen_st = "screen " + " ".join(scrvec1) + " ;\n" 
  
  
  sendoff_st = "sendoff(" + out + ") " + " ".join(tuple(outvnlist)) + " ;\n"
  
  rmj_st = ""
  if RMJoption!=None and RMJoption!="" :
    if   RMJoption=="m" : s1 = "mergeby(excl) " 
    elif RMJoption=="j" : s1 = "joinby "
    elif RMJoption=="r" : s1 = "readby "
    else : raise Ex("gendpf_rmjopt")
    rmj_st = s1 + " ".join(bylist) + " ;\n" 
  
  
  inflag_st = ""
  v1=[]
  v2=[]
  if inflag_map!=None and len(inflag_map)>0 :
    for dref in inflag_map :
      v1.append(dref)
      v2.append(inflag_map[dref])
    inflag_st = "inflags " + " ".join(v2) + " = " + " ".join(v1) + " ;\n"
  
  
  turnoff_st = "turnoff;\n"
  wholedpf = ( inlist_st + screen_st + rmj_st + inflag_st + a_st + 
               procst + sel + sendoff_st + turnoff_st + "\n"  )
  
  return wholedpf
  
  
#end def generate_DPF


########################################################################
########################################################################
########################################################################






# for mean, std, min, max, sum 
# not for n/% , not for median 

def generate_DPF_mean_etc(inlist,out,screen,outvnlist,bylist,select_list) :
  if inlist==None or len(inlist)!=1 : raise Ex("gendpfmean00")
  inputref = inlist[0]
  mean_askedfor=False
  n_askedfor=False
  n_vname = "n" 
  avg_vname = "mean" 
  if bylist==None : bylist=()
  if select_list==None or select_list==[] : raise Ex("gendpfmean0")
  if len(select_list)==0 : raise Ex("gendpfmean1")
  if len(select_list[0])!=3 : raise Ex("gendpfmean2")
  sourcevname = select_list[0][2]
  stats_set = set()
  for item in select_list :
    if item==None : raise Ex("gendpfmean11") 
    if len(item)!=3 : raise Ex("gendpfmean12")
    if item[2]!=sourcevname : raise Ex("gendpfmean13")
    stats_set.add(item[1])
    if item[1]=="n" : 
      n_vname=item[0]
      n_askedfor=True
    if item[1] in ("mean","avg") : 
      avg_vname=item[0]
      mean_askedfor=True
  ###########################################################
  
  if "std" not in stats_set : 
    return generate_DPF_select_para(inlist=inlist,out=out,screen=screen,
               outvnlist=outvnlist,bylist=bylist,select_list=select_list)
  # rest of function, assume you need STD
  
  
  select_list1 = []
  for e in select_list :
    if e[1]!="std" : select_list1.append(e)
  if n_askedfor==False : select_list1.append(("n","n",sourcevname))
  if mean_askedfor==False : select_list1.append(("mean","avg",sourcevname))
  outref_p1 = out + "_pre1"
  outvnlist1 = set(bylist)
  for e in select_list1 : outvnlist1.add(e[0])
  para1 = generate_DPF_select_para(inlist=inlist,out=outref_p1,screen=screen,
            outvnlist=outvnlist1,bylist=bylist,select_list=select_list1)

  ##########################################################
  
  outref_p2 = out + "_pre2" 
  byliststr = " "
  if len(bylist)>0 : byliststr = " by " + " ".join(bylist) + " "
  byliststr2 = " " 
  if len(bylist)>0 : byliststr2 = " " + " ".join(bylist) + " "
    

  vnames_from_outp1 = []
  vnames_to_enduser = []
  if n_askedfor==True : vnames_to_enduser.append(n_vname)
  if mean_askedfor==True : vnames_to_enduser.append(avg_vname)
  for item in select_list1 :
    vnames_from_outp1.append(item[0])
    if item[1] not in ("mean","avg","n") : 
      vnames_to_enduser.append(item[0])

  vnames_from_outp1_2 = " ".join(vnames_from_outp1)
  vnames_to_enduser_2 = " ".join(vnames_to_enduser)

  para2 = (
    "inlist " + inputref + " " + outref_p1 + " ;\n" + 
    "screen " + inputref + ": " + byliststr2 + " " + sourcevname + " " + 
    outref_p1 + ": " + byliststr2 + " " + avg_vname + " ;\n" + 
    "mergeby(excl) " + byliststr2 + " ;\n" + 
    "addgridvars float: tmp_88 ;\n" + 
    "tmp_88=(" + sourcevname + "-" + avg_vname + ")*(" + sourcevname + "-" + avg_vname+ ");\n" +
    "select tmp88sum=sum(tmp_88) " + byliststr + ";\n" +
    "sendoff(" + outref_p2 + ") tmp88sum " + byliststr2 + ";\n"  )


  para3 = (
    "inlist " + outref_p1 + " " + outref_p2  + " ;\n" + 
    "screen " + outref_p1 + ": " + byliststr2 + " " + vnames_from_outp1_2 + " " + 
    outref_p2 + ": " +  byliststr2 + " " + "tmp88sum" + " ;\n" + 
    "mergeby " + byliststr2 + " ;\n" + 
    "addgridvars float: std ;\n" + 
    "std = sqrt( tmp88sum / (" + n_vname + "-1) ) ;\n" +
    "sendoff(" + out + ") " + byliststr2 + " " + vnames_to_enduser_2 + " std " + ";\n"  )

  return para1 + "\n" + para2 + "\n" + para3 




################################################################
################################################################


def generate_DPF_select_para(inlist,out,screen,outvnlist,bylist,select_list):
  return generate_DPF(inlist=inlist,out=out,screen=screen,outvnlist=outvnlist,
                      bylist=bylist,select_list=select_list)


def generate_DPF_median(inlist,out,screen,outvnlist,bylist,select_list) :
  if select_list==None or len(select_list)!=1 : raise Ex("gendpfmedian0")
  if len(select_list[0])!=3 : raise Ex("gendpfmedian1")
  sourcevname = select_list[0][2]
  inputref = inlist[0] 
  byliststr = " "
  if len(bylist)>0 : byliststr = " by " + " ".join(bylist) + " "
  byliststr2 = " " 
  if len(bylist)>0 : byliststr2 = " " + " ".join(bylist) + " "
  byliststr5 = " by " + sourcevname + " " 
  if len(bylist)>0 : byliststr5 = byliststr + sourcevname + " " 
  para = ( 
    "inlist " + inputref + " ;\n" +
    "if (" + sourcevname + " is null) deleterow ;\n" +
    "gridfunc n1_jnk = n() " + byliststr5 + " ;\n" +
    "gridfunc n1_tmp88 = rowno() " + byliststr + " ;\n" + 
    "gridfunc n_tmp88 = n() " + byliststr + " ;\n" +
    "if (2*n1_tmp88<n_tmp88 or 2*n1_tmp88>n_tmp88+2) deleterow ;\n" +
    "select median=avg(" + sourcevname + ") " + byliststr + " ;\n" +
    "sendoff(" + out + ") " + byliststr2 + " median ;\n"      )
  return para


# inlist inputref ;
# if ( sourcevname is null ) deleterow ;
# gridfunc n1 = rowno() by byliststr ;
# gridfunc n  = n() by byliststr ;
# if ( 2*n1<n  or 2*n1>n+2   ) deleterow ;
# select median = avg(sourcevname) by byliststr ;
# sendoff(out) byliststr median ;








