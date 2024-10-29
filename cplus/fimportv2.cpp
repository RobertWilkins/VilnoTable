
/// Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
///                  in 1984, in Massachusetts, USA 




void FIVitem::from_FIV_to_RESULTS()
{
RESULTSitem Rentry ;
if (RESULTS.find(TPATHc)==RESULTS.end())
{ Rentry.TPATHc = TPATHc ;
  Rentry.COLPATHc = COLPATHc ;
  Rentry.ROWPATHc = ROWPATHc ;
  Rentry.TPATHi = TPATHi ;
  Rentry.COLPATHi = COLPATHi ;
  Rentry.ROWPATHi = ROWPATHi ;
  Rentry.STATt = STATt ;
  Rentry.whichhasstat = whichhasstat ;
  Rentry.COLCATPATHc = COLCATPATHc ;
  Rentry.n_colcat = n_colcat ;
  Rentry.ROWCATPATHc = ROWCATPATHc ;
  Rentry.n_rowcat = n_rowcat ;
  all_table_paths.insert(TPATHc) ;   // added Jan 13 2021
  RESULTS[TPATHc] = Rentry ;
}
else
{ if (RESULTS[TPATHc].COLPATHc != COLPATHc ) throw "fivresults1" ;
  if (RESULTS[TPATHc].TPATHc != TPATHc ) throw "fivresults1b" ;
  if (RESULTS[TPATHc].TPATHi != TPATHi ) throw "fivresults1c" ;
  if (RESULTS[TPATHc].COLCATPATHc != COLCATPATHc ) throw "fivresults1d" ;
  if (RESULTS[TPATHc].n_colcat != n_colcat ) throw "fivresults1e" ;
  if (RESULTS[TPATHc].ROWCATPATHc != ROWCATPATHc ) throw "fivresults1f" ;
  if (RESULTS[TPATHc].n_rowcat != n_rowcat ) throw "fivresults1g" ;
  if (RESULTS[TPATHc].ROWPATHc != ROWPATHc ) throw "fivresults1h" ;
} ;

RESULTS[TPATHc].data2_stack.push_back(data2) ;
RESULTS[TPATHc].slot_stack.push_back(slot_ctr) ;
if (RESULTS[TPATHc].finetunes.find(slot_ctr)!=RESULTS[TPATHc].finetunes.end())
    throw "fivresults3" ;
RESULTS[TPATHc].finetunes[slot_ctr] = finetune_obj ;

}     /// end from_FIV_to_RESULTS()



///////////////////////////////////////////////////////////////////////////


void RESULTSitem::process_data_from_FIV()
{
long k , i , k2 , this_slot , c_index , r_index ;
list<fi_statrow>::iterator p ;
set< vector<int> >::iterator pcc ;

num_slots = slot_stack.size() ;
//  also err-chk to verify slots are 0,1,2
for(k=0;k<slot_stack.size();++k)
  { if (slot_stack[k]!=k) throw "bad-slot" ; }
finetune0 = finetunes[0];
slot_fmt0 = finetune0.slot_fmt;
if (num_slots>1 && finetune0.f_blank==true ) throw "blankft" ;
if (num_slots>1 && num_slots!=finetune0.num_slots) throw "blankft2" ;

extras1 = split_string_delim(slot_fmt0,'?') ;
str_vec_sizeup(extras1,num_slots+1) ;

///////////////////////////////////////////////////////////////////

for(k=0;k<data2_stack.size();++k)
  for(p=data2_stack[k].begin();p!=data2_stack[k].end();++p)
  { set_colcats.insert(p->colcatval);
    set_rowcats.insert(p->rowcatval);
  }

for(pcc=set_colcats.begin(),i=0;pcc!=set_colcats.end();++pcc,++i)
{ vec_colcats.push_back(*pcc) ;
  map_colcats[*pcc] = i ;
}
for(pcc=set_rowcats.begin(),i=0;pcc!=set_rowcats.end();++pcc,++i)
{ vec_rowcats.push_back(*pcc) ;
  map_rowcats[*pcc] = i ;
}

small_matrix.resize(map_colcats.size());
for(k=0;k<small_matrix.size();++k) small_matrix[k].resize(map_rowcats.size());
for(k=0;k<small_matrix.size();++k)
  for(k2=0;k2<small_matrix[k].size();++k2)
    small_matrix[k][k2].resize(num_slots) ;

for(k=0;k<data2_stack.size();++k)
{ this_slot = slot_stack[k] ;
  for(p=data2_stack[k].begin();p!=data2_stack[k].end();++p)
  { c_index = map_colcats[p->colcatval] ;
    r_index = map_rowcats[p->rowcatval] ;
    small_matrix[c_index][r_index][this_slot] = p->statval ;
  }
}

}    ////  end RESULTSitem::process_data_from_FIV()


//////////////////////////////////////////////////////////////////////

void RESULTSitem::statval_reformat()
{
int i , k ;
vector<string> column , column2 ;
list<fi_statrow>::iterator p ;

if (finetune0.digit_explicit==true)
{ for(k=0;k<data2_stack.size();++k)
  { column.resize(data2_stack[k].size()) ;
    for(p=data2_stack[k].begin(),i=0;p!=data2_stack[k].end();++p,++i)
      column[i] = p->statval ;
    column2 = stat_value_reformats(column,finetune0.digits[k]);   // k IS slot
    for(p=data2_stack[k].begin(),i=0;p!=data2_stack[k].end();++p,++i)
      p->statval = column2[i] ;
  }
}      /// end big IF block
else
{ column.clear();
  for(k=0;k<data2_stack.size();++k)
    for(p=data2_stack[k].begin();p!=data2_stack[k].end();++p)
      column.push_back(p->statval) ;
  column2 = stat_value_reformats(column);
  i=0;
  for(k=0;k<data2_stack.size();++k)
    for(p=data2_stack[k].begin();p!=data2_stack[k].end();++p)
      { p->statval=column2[i] ; ++i; }

}      /// end big ELSE block
}      /// end RESULTSitem::statval_reformat()



/////////////////////////////////////////////////////////////////////////


void RESULTSitem::send_to_matrix()
{
long k , cindex , rindex ;
list<fi_statrow>::iterator p ;
for(k=0;k<data2_stack.size();++k)
  for(p=data2_stack[k].begin();p!=data2_stack[k].end();++p)
  { cindex = colindex_map[COLPATHi][p->colcatval] ;
    rindex = rowindex_map[ROWPATHi][p->rowcatval] ;
    str_vec_assign(matrix0[cindex][rindex],p->statval,k) ;
    matrix0_extras[cindex][rindex] = extras1 ;
  }
}     // RESULTSitem::send_to_matrix()



void send_to_matrix3()
{
long j ;
for(j=0;j<matrix0.size();++j)
  matrix3[j] = decimal_align2(matrix0_extras[j],matrix0[j]) ;
}    // send_to_matrix3()


////////////////////////////////////////////////////////////////



