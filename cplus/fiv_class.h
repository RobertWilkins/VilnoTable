
/// Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
///                  in 1984, in Massachusetts, USA 



// ??? tcat_gcat
// need : remove_placeholder()
// ?? tele_type()
// remove_placestat()
// SPLIT_VEC_IN_TWO()
// ??? missing (const var)
// ?? CATEXPANDLIST 

///////////////////////////////////////////////////////////////

class parsenode {
public:
int type ;
string text ;
vector<parsenode*> next ;
} ;

class connode {
public:
int type ;
string text ;
vector<connode*> next ;
} ;

class expnode { 
public:
int type ;
string text ;
int catval , width , offset ;
map<int,expnode*> next ;
string prnt ;
vector<int> expwhere , conwhere , catwhere ;

} ;

class gcatparseinfo {
public:
string formatwhere ;
vector<string> valliststr , vallistintraw ;
vector<int> vallistint ;
string format_to_import ;
} ;

///////////////////////////////////////////////

class smallstatrow {
public:
vector<string> value ;
} ;

class gf_statrow {
public:
vector<int> catval ;
vector<string> statval ;
};

class fi_statrow {
public:
vector<int> colcatval , rowcatval ;
string statval ;
} ;

/////////////////////////////////////////////


class FineTune_item {
public:
string slot_fmt ;
long num_slots ;
bool f_blank , digit_explicit ;
vector<long> digits ;
} ;  // end class FineTune_item




/////////////////////////////////////////////

// class for FIV[]
//  Dec 2020 , add some data members and one function 
class FIVitem {
public:
void fileimportst_dataprep() ;
void fileimportst_latedataprep() ;
void statval_reformat() ;
void spectrum_and_insert() ;
void send_to_matrix() ;

void from_FIV_to_RESULTS() ;

vector<string> COLPATHc , ROWPATHc , TPATHc , FF1 ;
vector<string> COLCATv , FFCATCOLv , ROWCATv , FFCATROWv , TCATv , FFCATv ;
string STATff , STATt , whichhasstat , filename ;
vector<int> COLPATHi , ROWPATHi , TPATHi ;
map<string,string>  COLCATm , ROWCATm , GCOLCATm , 
         GROWCATm , TCATm , GCATm , FFCATCOLm , FFCATROWm ;
int filename_index , gfile_index ;
vector<string> COLCATPATHc , ROWCATPATHc ;
int n_colcat , n_rowcat ;
set<string> omit_set ; // (yes class, not local)
list<fi_statrow> data2 ;
map<string,string> subset_info ; /// add this April 2011, for subsetting ;

long slot_ctr ;
FineTune_item finetune_obj ;
} ; // end class FIVitem 

//////////////////////////////////////////////////////

/***
FOUND_STRVALUE FOUND_INTVALUE FOUND_INTVALUEraw
map<string,set<int>> gcat_filedatatypes
map<string,int> datatype_of_gcat 
map<string,map<int,string>> GCAT_FORMAT 
map<string,map<string,int>> GCAT_FORMAT2
map<string,int> GCAT_INTWIDTH
***/

/////////////////////////////////////////////////////

//  class for GFV[]
class GFVitem {
public:
void prep_GCAT1();
void gfile_dataprep();
map<string,string> GCATm ;
string filename ;
int filename_index , gfile_index , numcatcol , numstatcol ;
set<string> FFSTATset  ;
vector<string> FFCATv , FFSTATv ;
map<string,int> FFCATv_index2 , FFSTATv_index2 ;
vector<int> FFCATv_oldindex , FFCATv_dtype , FFSTATv_oldindex , FFSTATv_dtype;
list<gf_statrow> data ; //( to catval statval)
map<string,string> subset_info  ; /// add this April 2011, for subsetting ;
} ; // end class GFVitem

/////////////////////////////////////////////////////

class GFVitem_spec {
 friend bool   operator<(const GFVitem_spec &, const GFVitem_spec &)  ;
 friend bool   operator==(const GFVitem_spec &, const GFVitem_spec &)  ;
 public: 
 string filename ;
 map<string,string> GCATm ;
 map<string,string> subset_info ;
} ;   

bool operator<(const GFVitem_spec & left, const GFVitem_spec & right) 
{
if (left.filename != right.filename) return (left.filename < right.filename) ;
if (left.GCATm != right.GCATm) return (left.GCATm < right.GCATm) ;
return (left.subset_info < right.subset_info) ;
}  // end operator< 

bool operator==(const GFVitem_spec & left, const GFVitem_spec & right)  
{
return (left.filename == right.filename && left.GCATm==right.GCATm && 
        left.subset_info==right.subset_info) ;
}  // end operator==  

/////////////////////////////////////////////////////

// class for FFV[]
class FFVitem {
public:
void get_statdata();
list<smallstatrow> data ; // has .value which is vec-str
vector<string> varnames ;
vector<int> datatypes ;
map<string,int> vn_index , datatypes_map ;
string filename ;
int filename_index ;

} ;  // end class FFVitem



// FFVitem ffv_newentry ;
// GFVitem gfv_newentry ; // local or global, don't care






/// December 2020 , new classes 
/// class RESULTSitem 

class RESULTSitem {
public:
void process_data_from_FIV() ;
void statval_reformat() ;
void send_to_matrix() ;

long num_slots ;
FineTune_item finetune0 ;
string slot_fmt0 ;
vector<string> extras1 ;

string STATt , whichhasstat ;
long n_colcat , n_rowcat ;
vector<string> TPATHc , COLPATHc , ROWPATHc , COLCATPATHc , ROWCATPATHc ;

vector<int> TPATHi , COLPATHi , ROWPATHi ;

vector< list<fi_statrow> >  data2_stack ;
vector<long> slot_stack ;
map< long , FineTune_item > finetunes ;

vector< vector< vector<string> > > small_matrix ;
set< vector<int> > set_colcats , set_rowcats ;
vector< vector<int> > vec_colcats , vec_rowcats ;
map< vector<int> , long > map_colcats , map_rowcats ;
} ;   // end class RESULTSitem 





