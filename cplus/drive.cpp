
/// Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
///                  in 1984, in Massachusetts, USA 



void mainprocdriver(int, char**) ;
void mainproc() ;

//////////////////////////////////

void mainprocdriver(int argc , char** argv)
{
sourcefilename = argv[1] ;
// sourcefilename = "/home/robert/tallinn/cplus/build/" + sourcefilename ;
try 
{
  mainproc() ;
}  // end try 
catch (char const * s) 
{ 
  cerr << "Error code: " << s << "\n" ;
}  // end catch 
catch (rsUnex b) 
{ 
  cerr << "Error code: " << b.errorcode << "\n" ;
}  // end catch 

}  // end mainprocdriver 


///////////////////////////////////////////////////////////
//// DRIVER CODE

void mainproc()
{
int m ;
set< vector<string> >::const_iterator pss ;     /// new, Jan 2021

numformat_initialize() ;
setupSOURCE(sourcefilename.c_str());

parseMAIN();
offSOURCE();
load_formatfile() ;


execute_parseagain();
executePTRANS();

// COL_CON_TREE_TOP what?
// ROW_CON_TREE_TOP what?
executeCI_TRANSLATE();

for(m=0;m<FIV.size();++m) FIV[m].fileimportst_dataprep() ;

for(m=0;m<FFV.size();++m) FFV[m].get_statdata() ;

for(m=0;m<GFV.size();++m) GFV[m].prep_GCAT1() ;
prep_gcatdatatypes();


prep_GCAT2() ;

for(m=0;m<GFV.size();++m) GFV[m].gfile_dataprep() ;


for(m=0;m<FIV.size();++m) FIV[m].fileimportst_latedataprep() ;

/// for(m=0;m<FIV.size();++m) FIV[m].statval_reformat() ;

for(m=0;m<FIV.size();++m) FIV[m].from_FIV_to_RESULTS() ;
for(pss=all_table_paths.begin();pss!=all_table_paths.end();++pss)
  RESULTS[*pss].process_data_from_FIV() ;

FILL_TOP();
for(m=0;m<FIV.size();++m) FIV[m].spectrum_and_insert() ;



SAYWHERE(COL_EXP_TREE_TOP);
SAYWHERE(ROW_EXP_TREE_TOP);


executeLEAFCOUNT();  // including resize matrix 


// for(m=0;m<FIV.size();++m) FIV[m].send_to_matrix();
// send_to_matrix2() ; //  call decimal_align

for(pss=all_table_paths.begin();pss!=all_table_paths.end();++pss)
 { RESULTS[*pss].statval_reformat() ;
   RESULTS[*pss].send_to_matrix() ;
 }
send_to_matrix3() ;



GETWIDTH(COL_EXP_TREE_TOP);
COL_EXP_TREE_TOP->offset = 0 ;

GETOFFSET(COL_EXP_TREE_TOP) ;

executeCOLTREEPRINT()  ;   // prep and call COLTREE_PRINTOUT()

executeROWTREEPRINT() ;

finish_the_print() ;


}  // end mainproc() ;




/***
cout << "FORMATi.size()=" << FORMATi.size() << "\n" ;
cout << "FORMATi*bodysysf*2 = " << FORMATi["bodysysf"][2] << "\n" ;
cout << "FORMATi*ptermf*3 = " << FORMATi["ptermf"][3] << "\n" ;

map< string , map<int,string> >::const_iterator qq8a ;
map<int,string>::const_iterator qq8b ;
string gggcat , val2 ;
int val1 ;
for(qq8a=GCAT_FORMAT.begin();qq8a!=GCAT_FORMAT.end();++qq8a)
{ gggcat = qq8a->first ;
  cout << gggcat << " -- " ;
  for(qq8b=GCAT_FORMAT[gggcat].begin();qq8b!=GCAT_FORMAT[gggcat].end();++qq8b)
  { val1 = qq8b->first ;
    val2 = qq8b->second ;
    cout << val1 << "=" << val2 << " " ;
  }
  cout << "\n" ;
}
***/




