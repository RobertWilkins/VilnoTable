
/// Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
///                  in 1984, in Massachusetts, USA 



parsenode * COL_PARSE_TREE ;
parsenode * ROW_PARSE_TREE ;

map<string,gcatparseinfo> GCATPARSE ;
map< string , vector<int> > CATEXPANDLIST ;

const int PARENGRP=1 , MULTIPLYGRP=2 , ATOM=3 ;
const int PLACEHOLDER=11 , CAT=12 , STAT=13 ;
const int CATVALUE=21 , CATHEAD=22 ;
const int STR=71 , INT=72 , FLO=73 ;
const int missing = -90 ;
const int void_clev = -99 ;

connode * COL_CON_TREE_TOP ;
connode * ROW_CON_TREE_TOP ;

expnode * COL_EXP_TREE_TOP ;
expnode * ROW_EXP_TREE_TOP ;

vector<FFVitem> FFV ;
vector<FIVitem> FIV ;
vector<GFVitem> GFV ;

/// Jan 2021 add this
set< vector<string> > all_table_paths ;
map< vector<string> , RESULTSitem > RESULTS ;

FFVitem ffv_newentry ;
FIVitem FIVnewentry ;
GFVitem gfv_newentry ;

set<string> GCATNAMESset , CATNAMESset , STATNAMESset ;
set<string> tablespell ;
map<string,string> tcat_gcat ;

map<string,string> RELABEL_FORMAT ;

string tableprintfilename , sourcefilename , format_filename ;
string titletext ;

///

map< string , map<int,string> >    FORMATi ;
map< string , map<string,string> >    FORMATs ;
map< string , map<string,int> > FORMATs_order ;
map< string , map<int,string> > FORMATs_order2 ;


/////////////////////

map< vector<string> , vector<int> > pathmap_ci ;
map< vector<int> , vector<string> > pathmap_ic ;
map< vector<string> , vector<int> > COLTREE_PATH_strtoint ;
map< vector<string> , vector<int> > ROWTREE_PATH_strtoint ;
map< vector<int> , vector<string> > COLTREE_PATH_inttostr ;
map< vector<int> , vector<string> > ROWTREE_PATH_inttostr ;

map<string,int> filenameindex_map ;
vector<string> filenameindex_vec ;
/// map< pair< string , map<string,string> > , int > gfileindex_map ;
map< GFVitem_spec , int > gfileindex_map ;


map< string , set<string> > FOUND_STRVALUE ;
map< string , set<string> > FOUND_INTVALUEraw ;
map< string , set<int> > FOUND_INTVALUE ;

map< string , set<int> > gcat_filedatatypes ;
map<string,int> datatype_of_gcat ;

map< string , map<int,string> > GCAT_FORMAT ;
map< string, map<string,int> > GCAT_FORMAT2 ;
map<string,int> GCAT_INTWIDTH ;

////////////////////////////////

map< vector<int> , map< vector<int> , int > > 
     colindex_map , rowindex_map , LEAFOFFSET , leaf_counter_map ;
int colindex_counter , rowindex_counter , leaf_counter ;

vector< vector<string> > matrix , matrix2 ;

/// Jan 2021 , add these
vector< vector< vector<string> > > matrix0 , matrix0_extras ;
vector< vector<string> > matrix3 ;

vector<string> coltreeprnt , rowtreeprnt ;

vector<int> MATRIX_OFFSET , MATRIX_RSHIFT ;

////////////////

map< vector<int> , set< vector<int> > >  COLSPECT , ROWSPECT ;

/////////////////


