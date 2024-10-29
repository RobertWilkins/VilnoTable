
/// Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
///                  in 1984, in Massachusetts, USA 


void FIVitem::fileimportst_dataprep()
{
// locals:
vector<string> COLPATH2 , ROWPATH2 , FF1col , FF1row , omit_col , omit_row , 
  FF3col , FF3row , COLPATH3 , ROWPATH3 ; 

string tablecat , ffcat ;
// ??? ffv_newentry   ??? gfv_newentry   ;

/// April 2011 for subsetting : gfspec more complex object, not just a pair ;
/// pair< string , map<string,string> > gfspec ;
GFVitem_spec gfspec ;

int index , newindex , j ;


COLPATH2=remove_placeholder(COLPATHc) ;
ROWPATH2=remove_placeholder(ROWPATHc) ;
if (COLPATH2.size()+ROWPATH2.size()!=FF1.size()) throw "FIVPREP1" ;
SPLIT_VEC_IN_TWO(FF1,FF1col,FF1row,COLPATH2.size()) ;

for(j=0;j<COLPATH2.size();++j)   // REPEAT FOR ROW 
{ if (FF1col[j]=="*")
  { omit_col.push_back(COLPATH2[j]) ;
    omit_set.insert(COLPATH2[j]) ;
    if (tele_type(COLPATH2[j])!=CAT) throw "FIVPREP2" ;
  }
  else 
  { COLPATH3.push_back(COLPATH2[j]) ;
    FF3col.push_back(FF1col[j]) ;
  }
}
for(j=0;j<ROWPATH2.size();++j)   // and this is for ROW
{ if (FF1row[j]=="*")
  { omit_row.push_back(ROWPATH2[j]) ;
    omit_set.insert(ROWPATH2[j]) ;
    if (tele_type(ROWPATH2[j])!=CAT) throw "FIVPREP3" ;
  }
  else 
  { ROWPATH3.push_back(ROWPATH2[j]) ;
    FF3row.push_back(FF1row[j]) ;
  }
}


for(j=0;j<COLPATH3.size();++j)    // REPEAT FOR ROW 
{ if (tele_type(COLPATH3[j])==CAT)
  { COLCATv.push_back(COLPATH3[j]) ;
    FFCATCOLv.push_back(FF3col[j]) ;
  }
  else if (tele_type(COLPATH3[j])==STAT)
  { if (STATff!="") throw "FIVPREP4" ;
    STATff=FF3col[j] ;
    STATt=COLPATH3[j] ;
    whichhasstat="COLUMN" ;
  }
  else throw "FIVPREP5" ;
}
for(j=0;j<ROWPATH3.size();++j)    // and this is for ROW 
{ if (tele_type(ROWPATH3[j])==CAT)
  { ROWCATv.push_back(ROWPATH3[j]) ;
    FFCATROWv.push_back(FF3row[j]) ;
  }
  else if (tele_type(ROWPATH3[j])==STAT)
  { if (STATff!="") throw "FIVPREP6" ;
    STATff=FF3row[j] ;
    STATt=ROWPATH3[j] ;
    whichhasstat="ROW" ;
  }
  else throw "FIVPREP7" ;
}


// RENAME : COLPATH4=COLCATv FF4col=FFCATCOLv 
// RENAME: COLPATH1=COLPATHc  ROWPATH1=ROWPATHc
TCATv=CONCATENATE_VEC(COLCATv,ROWCATv) ;
FFCATv=CONCATENATE_VEC(FFCATCOLv,FFCATROWv) ;


////////////////////////////////////////////////////////

if (COLTREE_PATH_strtoint.find(COLPATHc)==COLTREE_PATH_strtoint.end()) throw "FIVPREP7b";
if (ROWTREE_PATH_strtoint.find(ROWPATHc)==ROWTREE_PATH_strtoint.end()) throw "FIVPREP7c";

COLPATHi=COLTREE_PATH_strtoint[COLPATHc] ;
ROWPATHi=ROWTREE_PATH_strtoint[ROWPATHc] ;

/// December 2020 , TPATHi = COLPATHi + ROWPATHi
TPATHi = COLPATHi ;
TPATHi.insert(TPATHi.end(),ROWPATHi.begin(),ROWPATHi.end()) ;




// AFTER COLCATv & FFCATCOLv ARE READY
for(j=0;j<COLCATv.size();++j)      // repeat for ROW 
{ tablecat=COLCATv[j] ;
  ffcat=FFCATCOLv[j] ;
  if (tcat_gcat.find(tablecat)==tcat_gcat.end()) throw "FIVPREP8" ;
  COLCATm[ffcat]=tablecat ;
  GCOLCATm[ffcat]=tcat_gcat[tablecat] ;
  TCATm[ffcat]=tablecat ;
  GCATm[ffcat]=tcat_gcat[tablecat] ;
  FFCATCOLm[tablecat]=ffcat ;
}
for(j=0;j<ROWCATv.size();++j)      // and this is for ROW 
{ tablecat=ROWCATv[j] ;
  ffcat=FFCATROWv[j] ;
  if (tcat_gcat.find(tablecat)==tcat_gcat.end()) throw "FIVPREP9" ;
  ROWCATm[ffcat]=tablecat ;
  GROWCATm[ffcat]=tcat_gcat[tablecat] ;
  TCATm[ffcat]=tablecat ;
  GCATm[ffcat]=tcat_gcat[tablecat] ;
  FFCATROWm[tablecat]=ffcat ;
}



if (filenameindex_map.find(filename)==filenameindex_map.end())
{ index=filenameindex_map.size() ;
  filenameindex_map[filename]=index ;
  filenameindex_vec.push_back(filename) ;
  FFV.push_back(ffv_newentry) ;
  FFV.back().filename=filename ;
  FFV.back().filename_index=index ;
}
filename_index=filenameindex_map[filename] ;
COLCATPATHc=remove_placestat(COLPATHc);
ROWCATPATHc=remove_placestat(ROWPATHc);
n_colcat=COLCATPATHc.size();
n_rowcat=ROWCATPATHc.size();

///////////////////////////////////////////////////////////


///  .fileimportst_dataprep()

/// gfspec.first=filename ;
/// gfspec.second=GCATm ;
/// April 2011 change for subsetting 
gfspec.filename = filename ;
gfspec.GCATm = GCATm ;
gfspec.subset_info = subset_info ;   /// both int & str together 


if (gfileindex_map.find(gfspec)==gfileindex_map.end())
{ newindex=gfileindex_map.size() ;
  gfileindex_map[gfspec]=newindex ;
  GFV.push_back(gfv_newentry) ;
  if (gfileindex_map.size()!=GFV.size()) throw "FIVPREP10" ;
  if (newindex!=GFV.size()-1) throw "FIVPREP11" ;
  GFV[newindex].GCATm=GCATm ;
  GFV[newindex].filename=filename ;
  GFV[newindex].gfile_index=newindex ;
  GFV[newindex].filename_index=filename_index ;
  /// add this , april 2011 
  GFV[newindex].subset_info = subset_info ;
}
gfile_index=gfileindex_map[gfspec];
GFV[gfile_index].FFSTATset.insert(STATff);

} // end FIVitem::fileimportst_dataprep()


/////////////////////////////////////////////////////////////////////


void GFVitem::prep_GCAT1()
{

// locals : 
int fi , dt , index ;
map<string,string>::const_iterator p ;
string fvname , gcatname ;
list<smallstatrow>::const_iterator q ;

fi=filename_index ;
for(p=GCATm.begin();p!=GCATm.end();++p)
{ fvname=p->first ;
  gcatname=p->second ;
  dt=FFV[fi].datatypes_map[fvname] ;
  index=FFV[fi].vn_index[fvname] ;
  if (dt==STR)
  { for(q=FFV[fi].data.begin();q!=FFV[fi].data.end();++q)
      FOUND_STRVALUE[gcatname].insert(q->value[index]) ;
  }
  // July 2010 addition: 
  else if (dt==INT)
  { for(q=FFV[fi].data.begin();q!=FFV[fi].data.end();++q)
    { FOUND_INTVALUEraw[gcatname].insert(q->value[index]) ;
      FOUND_INTVALUE[gcatname].insert(StringToIntM(q->value[index])) ;
    }
  }
  // cout << "filename=" << filename << "\n" ;
  // cout << "fvname=" << fvname << ", gcatname=" << gcatname << ", dt=" << dt << ":\n" ;
  gcat_filedatatypes[gcatname].insert(dt) ;   // use for errchk later 
}

}  // end GFVitem::prep_GCAT1()


/////////////////////////////////////


void prep_gcatdatatypes()   // (not m.f. of GFV) 
{
map< string , set<int> >::const_iterator q7 ;
string gcatname ;
set<int> founddtypes ;
set<int>::const_iterator q8 ;

for(q7=gcat_filedatatypes.begin();q7!=gcat_filedatatypes.end();++q7)
{ gcatname=q7->first ;
  founddtypes=q7->second ;
  if (founddtypes.size()>1) throw "GCATDT1" ;
  for(q8=founddtypes.begin();q8!=founddtypes.end();++q8)
   datatype_of_gcat[gcatname] = (*q8) ;
}
}   // end prep_gcatdatatypes()

////////////////////////////////////////////////////


void prep_GCAT2() 
{
// unlike prep_GCAT1() , not a m.f. for GFV[~] 
// locals:
map<string,gcatparseinfo>::const_iterator p ;
string gcatname , strval , intval , fmat , val1 , val2 , printval ; 
vector<string> inlinestr , rawintvec ;
set<string> inlinestr_set , prespecified_str_set ;
int i , m , maxwidth , n , intval4 , width8 ;
set<string>::const_iterator q ;
set<string>::const_iterator q8 ;
set<int>::const_iterator q9 ;
map<int,string>::const_iterator qi ;
int dt2 ;

for(p=GCATPARSE.begin();p!=GCATPARSE.end();++p)
{ gcatname=p->first ;
  dt2 = datatype_of_gcat[gcatname] ;
  
  /// cout << "gcatname=" << gcatname << " dt2=" << dt2 << "\n" ;
  
  if (dt2==STR) 
  {
    inlinestr = (p->second).valliststr ;
    inlinestr_set.clear() ;
    for(m=0;m<inlinestr.size();++m) inlinestr_set.insert(inlinestr[m]) ;
    i=0 ;
    if (!(inlinestr.empty()))
    { for(i=0;i<inlinestr.size();++i)
      { GCAT_FORMAT[gcatname][i]=inlinestr[i] ;
        GCAT_FORMAT2[gcatname][inlinestr[i]]=i ;
        CATEXPANDLIST[gcatname].push_back(i) ;
      }
      i=inlinestr.size();
    }

    prespecified_str_set = inlinestr_set ;

    /// Feb 2011 add imported format : 
    if ( (p->second).format_to_import != "" )
    { fmat = (p->second).format_to_import ;
      if (FORMATs.find(fmat)==FORMATs.end()) throw "prepgcat2_fmat" ;
      for(i=0;i<FORMATs[fmat].size();++i)
      { val1 = FORMATs_order2[fmat][i] ;
        val2 = FORMATs[fmat][val1] ;
        prespecified_str_set.insert(val1) ;
        GCAT_FORMAT[gcatname][i] = val2 ;
        GCAT_FORMAT2[gcatname][val1] = i ;
      }
      i = FORMATs[fmat].size();
    }
    /////////////////////////////////////////////////////////////////////

    if (FOUND_STRVALUE.find(gcatname)!=FOUND_STRVALUE.end())
    { for(q=FOUND_STRVALUE[gcatname].begin();q!=FOUND_STRVALUE[gcatname].end();++q)
      { strval = *q ;
        /// Feb 2011 change
        /// if (inlinestr_set.find(strval)==inlinestr_set.end())
        if (prespecified_str_set.find(strval)==prespecified_str_set.end())
        { GCAT_FORMAT[gcatname][i]=strval ;
          GCAT_FORMAT2[gcatname][strval]=i ;
          i++ ;
        }
      }
    }
  }  /// end if(STR) 
  
  if (dt2==INT) 
  {

    /// cout << "in INT block\n" ;
    
    // July 2010 addition
    if (FOUND_INTVALUEraw.find(gcatname)!=FOUND_INTVALUEraw.end())
    { maxwidth=1 ;
      for(q8=FOUND_INTVALUEraw[gcatname].begin();
             q8!=FOUND_INTVALUEraw[gcatname].end();++q8)
      { intval = *q8 ;
        if (maxwidth < intval.size()) maxwidth = intval.size() ;
      }
      GCAT_INTWIDTH[gcatname] = maxwidth ;
    }
  
    if (GCATPARSE[gcatname].vallistintraw.size()>0) 
    { maxwidth=1 ;
      CATEXPANDLIST[gcatname]=GCATPARSE[gcatname].vallistint ;
      rawintvec=GCATPARSE[gcatname].vallistintraw ;
      for(n=0;n<rawintvec.size();++n)
        { if (maxwidth<rawintvec[n].size()) maxwidth=rawintvec[n].size() ; }
      if (GCAT_INTWIDTH.find(gcatname)==GCAT_INTWIDTH.end())
          GCAT_INTWIDTH[gcatname] = maxwidth ;
      else 
        { if (GCAT_INTWIDTH[gcatname]<maxwidth) 
              GCAT_INTWIDTH[gcatname]=maxwidth ;
        }
    }

    /// Feb 2011 add imported format : 
    if ( (p->second).format_to_import != "" )
    { fmat = (p->second).format_to_import ;
      if (FORMATi.find(fmat)==FORMATi.end()) throw "prepgcat2_fmatb" ;
      for(qi=FORMATi[fmat].begin();qi!=FORMATi[fmat].end();++qi)
      { intval4 = qi->first ;
        printval = qi->second ;
        GCAT_FORMAT[gcatname][intval4] = printval ;
      }
      for(q9=FOUND_INTVALUE[gcatname].begin();q9!=FOUND_INTVALUE[gcatname].end();++q9)
      { intval4 = *q9 ;
        if (GCAT_FORMAT[gcatname].find(intval4)==GCAT_FORMAT[gcatname].end())
          GCAT_FORMAT[gcatname][intval4] = IntToString(intval4) ;  
      }
      GCAT_FORMAT[gcatname][missing] = string(" ") ;
    }   /// end INT-importformat situ 
    else 
    { GCAT_FORMAT[gcatname][missing] = string(" ") ;
      width8 = GCAT_INTWIDTH[gcatname] ;
      for(q9=FOUND_INTVALUE[gcatname].begin();q9!=FOUND_INTVALUE[gcatname].end();++q9)
        GCAT_FORMAT[gcatname][*q9] = IntToStringM(*q9,width8) ;  
      for(i=0;i<GCATPARSE[gcatname].vallistint.size();++i)
      { intval4 = GCATPARSE[gcatname].vallistint[i] ;
        GCAT_FORMAT[gcatname][intval4] = IntToStringM(intval4,width8) ;
      }
    }   /// end else block (NOT INT-importformat situ) 
  }   /// end if(INT) 

}   /// end loop thru GCATPARSE 

}   /// end prep_GCAT2()

/////////////////////////////////////////////////////////////////


void GFVitem::gfile_dataprep() 
{
// locals 
int fi , i , index , dt ;
string vn , gcatname , strval , strval2 ;
vector<string> vn1 ;
vector<int> dt1 ;
list<gf_statrow>::iterator p2 ;
list<smallstatrow>::const_iterator p1 ;

map<string,string>::const_iterator ps1 ;
bool notthisrow ;
gf_statrow gf_row1 ;

/// cout << "Inside gfile_dataprep() near line 364\n";


fi=filename_index ;
vn1=FFV[fi].varnames ;
dt1=FFV[fi].datatypes ;
for(i=0;i<vn1.size();++i)
{ vn=vn1[i] ;
  if (GCATm.find(vn)!=GCATm.end())
  { FFCATv.push_back(vn) ;
    FFCATv_index2[vn] = FFCATv.size()-1 ;
    FFCATv_oldindex.push_back(i) ;
    FFCATv_dtype.push_back(dt1[i]) ;
  }
  if (FFSTATset.find(vn)!=FFSTATset.end())
  { FFSTATv.push_back(vn) ;
    FFSTATv_index2[vn]=FFSTATv.size()-1 ;
    FFSTATv_oldindex.push_back(i) ;
    FFSTATv_dtype.push_back(dt1[i]) ;
  }
}
numcatcol=GCATm.size();
numstatcol=FFSTATset.size() ;

/// cout << "Inside gfile_dataprep() near line 388\n";


/////////////////////////////////////////////////
/////////////////////////////////////////////////


/// here , changes April 2011 for subsetting :
// GFV[].gfile_dataprep() 
/****
data.resize(FFV[fi].data.size()) ;
for(p2=data.begin();p2!=data.end();++p2)
  { p2->catval.resize(numcatcol) ; p2->statval.resize(numstatcol); }
for(p1=FFV[fi].data.begin(),p2=data.begin();p2!=data.end();++p1,++p2)
{ for(i=0;i<numcatcol;++i)
  { gcatname=GCATm[FFCATv[i]] ;
    dt=FFCATv_dtype[i] ;
    index=FFCATv_oldindex[i] ;
    if (dt==STR)
     p2->catval[i] = GCAT_FORMAT2[gcatname][p1->value[index]] ;
    else if (dt==INT) 
     p2->catval[i] = StringToIntM(p1->value[index]) ;
  }
  for(i=0;i<numstatcol;++i)
  { index=FFSTATv_oldindex[i] ;
    p2->statval[i] = p1->value[index] ;
  } 
} 
****/

gf_row1.catval.resize(numcatcol) ;
gf_row1.statval.resize(numstatcol) ;

/// cout << "Inside gfile_dataprep() near line 415\n";
/// cout << "fi=" << fi << " FFV.size()=" << FFV.size() << " \n" ;
/// cout << "FFV[fi].data.size()=" << FFV[fi].data.size() << " \n" ;
/// cout << "This is really bad\n" ;

p1=FFV[fi].data.begin() ;
/// cout << "Really bad.\n" ;

for(p1=FFV[fi].data.begin();p1!=FFV[fi].data.end();++p1)
{
  /// cout << "FFV LOOP top \n" ;
  notthisrow=false ;
  /// this does subsetting values for both str & int, int values in string form ;
  /// make sure blanks not in int values ;

  /// cout << "FFV LOOP mid0 \n" ;
  for(ps1=subset_info.begin();ps1!=subset_info.end();++ps1)   /// both int & str 
  { vn = ps1->first ;
    strval = ps1-> second ;
    if (FFV[fi].vn_index.find(vn)==FFV[fi].vn_index.end()) throw "subsetvnameunk2" ;
    index = FFV[fi].vn_index[vn] ;
    strval2 = p1->value[index] ;
    if (strval!=strval2) notthisrow=true ; 
  }
  /// cout << "FFV LOOP mid1 \n" ;
  if (notthisrow==true) continue ;
  data.push_back(gf_row1) ;
  p2 = data.end() ;
  p2-- ;

  /// cout << "FFV LOOP mid2 \n" ;
  /// cout << "numcatcol=" << numcatcol << " numstatcol=" << numstatcol << 
  ///      " FFCATv.size()=" << FFCATv.size() << " FFSTATv_oldindex.size()=" << 
  ///      FFSTATv_oldindex.size() << " \n" ;
  
  for(i=0;i<numcatcol;++i)
  { gcatname=GCATm[FFCATv[i]] ;
    dt=FFCATv_dtype[i] ;
    index=FFCATv_oldindex[i] ;
    if (dt==STR)
     p2->catval[i] = GCAT_FORMAT2[gcatname][p1->value[index]] ;
    else if (dt==INT) 
     p2->catval[i] = StringToIntM(p1->value[index]) ;
  }
  for(i=0;i<numstatcol;++i)
  { index=FFSTATv_oldindex[i] ;
    p2->statval[i] = p1->value[index] ;
  } 
  /// cout << "FFV LOOP end\n" ;
} 

/// cout << "Inside gfile_dataprep() at bottom function\n";


}    // end GFVitem::gfile_dataprep() 


//////////////////////////////////////////////////////

void FIVitem::fileimportst_latedataprep() 
{
// locals 
vector<bool> col_skip , row_skip ;
vector<int> rindex , cindex ;
int gi , i , sindex ; 
string tableword , ffvname ;
list<gf_statrow>::iterator p1 ;
list<fi_statrow>::iterator p2 ;

row_skip.resize(n_rowcat) ;
rindex.resize(n_rowcat) ;
cindex.resize(n_colcat) ;

gi=gfile_index ;
sindex=GFV[gi].FFSTATv_index2[STATff] ;
col_skip.resize(n_colcat) ;

for(i=0;i<n_colcat;++i)      /// REPEAT for ROW SITU 
{ tableword=COLCATPATHc[i] ;
  if (omit_set.find(tableword)==omit_set.end())
  { ffvname=FFCATCOLm[tableword] ;
    cindex[i]=GFV[gi].FFCATv_index2[ffvname] ;
    col_skip[i]=false ;
  }
  else col_skip[i]=true ;
}
for(i=0;i<n_rowcat;++i)      /// and this is for ROW SITU 
{ tableword=ROWCATPATHc[i] ;
  if (omit_set.find(tableword)==omit_set.end())
  { ffvname=FFCATROWm[tableword] ;
    rindex[i]=GFV[gi].FFCATv_index2[ffvname] ;
    row_skip[i]=false ;
  }
  else row_skip[i]=true ;
}


/// July 2011 : use void_clev code instead of missing code 
data2.resize(GFV[gi].data.size()) ;
for(p1=GFV[gi].data.begin(),p2=data2.begin();p2!=data2.end();++p1,++p2)
{ p2->colcatval.resize(n_colcat) ;
  p2->rowcatval.resize(n_rowcat) ;
  p2->statval=p1->statval[sindex] ;
  for(i=0;i<n_colcat;++i)    /// REPEAT for ROW SITU 
  { if (col_skip[i]!=true) 
       p2->colcatval[i] = p1->catval[cindex[i]] ;
    else 
       p2->colcatval[i] = void_clev ;  /// July 2011, void_clev, not missing ;
  }
  for(i=0;i<n_rowcat;++i)    /// and this is for ROW SITU 
  { if (row_skip[i]!=true) 
       p2->rowcatval[i] = p1->catval[rindex[i]] ;
    else 
       p2->rowcatval[i] = void_clev ;  /// July 2011, void_clev, not missing ;
  }
}

}    // end FIVitem::fileimportst_latedataprep() 


/////////////////////////////////////////////////////////

///// it is 3 o clock Mar 17
////  everything above got one quick single proofread pass 
////  and earlier files





void ci_translate(connode * HERE, vector<string> PATHc, vector<int> PATHi, int me_slot)
{
vector<string> PATHc2 ;
vector<int> PATHi2 ;
int k ;
PATHc2 = PATHc ;
PATHc2.push_back(HERE->text) ;
PATHi2 = PATHi ;
PATHi2.push_back(me_slot) ;
pathmap_ci[PATHc2] = PATHi2 ;
pathmap_ic[PATHi2] = PATHc2 ;
for(k=0;k<HERE->next.size();++k)
  ci_translate(HERE->next[k],PATHc2,PATHi2,k) ;
}


void ci_translate_topper(connode * topptr)
{
vector<string> EMPTYc ;
vector<int> EMPTYi ;
int k ;
for(k=0;k<topptr->next.size();++k)
  ci_translate(topptr->next[k],EMPTYc,EMPTYi,k) ;
}


void executeCI_TRANSLATE()
{
pathmap_ci.clear();
pathmap_ic.clear();
ci_translate_topper(COL_CON_TREE_TOP) ;
COLTREE_PATH_strtoint = pathmap_ci ;
COLTREE_PATH_inttostr = pathmap_ic ;

pathmap_ci.clear();
pathmap_ic.clear();
ci_translate_topper(ROW_CON_TREE_TOP) ;
ROWTREE_PATH_strtoint = pathmap_ci ;
ROWTREE_PATH_inttostr = pathmap_ic ;
pathmap_ci.clear();
pathmap_ic.clear();
}    //  end executeCI_TRANSLATE() ;

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

// in FFV[] class: list<smallstatrow> data ; 
// note, data.back().value is a vector<string> 


void FFVitem::get_statdata()
{
// FFV[] data members built: data varnames datatypes vn_index datatypes_map
ifstream file1 ;
string colspecsrow ;
vector<string> dtlist , cspecs1 ;
list<string> drows ;
list<string>::iterator q1 ;
smallstatrow emptyrow1 ;
bool b ;

file1.open(filename.c_str(),ios::in);
if (!file1) throw "GETSTAT1" ;
b = getline(file1,colspecsrow) ;
if (!b) throw "GETSTAT2" ;
drows.push_back("");
while (getline(file1,drows.back()))  drows.push_back("");
drows.pop_back();
file1.close();

// Sept 2010 , change "()()" separate to ",,,," ;
// cspecs1 = split_string_vs(colspecsrow,"()()") ;
cspecs1 = split_string_delim(colspecsrow,',') ;
if (cspecs1.size()<=3) throw "GETSTAT3" ;
varnames = split_string_blank(cspecs1[1]);
dtlist = split_string_blank(cspecs1[2]);
datatypes.resize(dtlist.size()) ;
if (varnames.size()!=dtlist.size()) throw "GETSTAT4" ;

for(int i=0;i<dtlist.size();++i)
{ if (dtlist[i]=="str") datatypes[i]=STR ;
  else if (dtlist[i]=="int") datatypes[i]=INT ;
  else if (dtlist[i]=="flo") datatypes[i]=FLO ;
  else throw "GETSTAT5" ;
  varnames[i] = lowercase_str(varnames[i]) ;
  vn_index[varnames[i]] = i ;
  datatypes_map[varnames[i]] = datatypes[i] ;
}

for(q1=drows.begin();q1!=drows.end();++q1)
{ data.push_back(emptyrow1) ;
  data.back().value = split_string_delim(*q1,'|') ;
  
  /// for(int i=0;i<data.back().value.size();++i)
  ///  cout << " %" << data.back().value[i] << "% " ;
  /// cout << "\n" ;
  
  if (data.back().value.size() != varnames.size()) throw "GETSTAT6" ;
}

}    // end FFVitem::get_statdata()


//////////////////



void FIVitem::statval_reformat()
{
int i ;
vector<string> column , column2 ;
list<fi_statrow>::iterator p1 ;
column.resize(data2.size()) ;
for(p1=data2.begin(),i=0;p1!=data2.end();++p1,++i)
{ 
  // if (statval_isnull(p1->statval)) column[i]="";
  // else  column[i]=p1->statval ;
  column[i] = p1->statval ;
}


/// June 2011, new fctn stat_value_reformats()
/// column2 = round_format(column);
column2 = stat_value_reformats(column) ;
for(p1=data2.begin(),i=0;p1!=data2.end();++p1,++i)
   p1->statval = column2[i] ;
}  // end FIV[].statval_reformat()














