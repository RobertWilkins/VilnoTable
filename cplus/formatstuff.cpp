
/// Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
///                  in 1984, in Massachusetts, USA 



/// Feb 2011
/// formatfile shit


void load_formatfile() 
{

ifstream file1 ;
string firstrow ;
vector<string> info_thisrow , cspecs1 ;
list<string> drows ;
list<string>::iterator q ;
bool b ;

vector<string> info ;
vector< vector<string> > header ;
vector< vector< vector<string> > > stuff ;
vector< vector<string> > empty_vec_of_infos ;
bool loading , error_code ;
int intval , h , i ;
string intlit , printval , printval2 , strlit , strlit2 , dt , formatname ;

///


if (format_filename=="") return ;  /// no format file to load this example
file1.open(format_filename.c_str(),ios::in);
if (!file1) throw "GETFORMAT1" ;
b = getline(file1,firstrow) ;
if (!b) throw "GETFORMAT2" ;
if (firstrow!="{FORMAT-FILE}") throw "GETFORMAT3" ;

drows.push_back("");
while (getline(file1,drows.back()))  drows.push_back("");
drows.pop_back();

file1.close();


/// semicolon needs it's own row
/// "a" = "b"  must separate by space, everything must separate by space 


loading=false ;
h = -1 ;
for (q=drows.begin();q!=drows.end();++q)
{ /// June 2011 , use split_string_tk instead 
  /// info = split_string_blank(*q) ;
  info = split_string_tk(*q) ;
  if (info.size()==0) continue ;
  if (info[0]==";") { loading=false ; continue ; }   /// note: semicolon on own row
  if (info[0]=="format")
  { header.push_back(info) ;
    stuff.push_back(empty_vec_of_infos) ;
    h = h + 1 ;
    loading=true ;
  }
  else if (info.size()==3 && loading==true && info[1]=="=" ) 
    stuff[h].push_back(info) ;
}


for(h=0;h<header.size();++h)
{ if (header[h].size()<2) throw "formatfile11" ;
  formatname = header[h][1] ;
  dt = "int" ;
  if (header[h].size()==3) dt=header[h][2] ;
  if (dt!="int" && dt!="str") throw "formatfile12" ;
  if (FORMATi.find(formatname)!=FORMATi.end() || 
      FORMATs.find(formatname)!=FORMATs.end() ) throw "formatfile13" ;  
  if (dt=="int") 
    for(i=0;i<stuff[h].size();++i)
    { intlit = stuff[h][i][0] ;
      printval = stuff[h][i][2] ;
      if (intlit=="" || printval=="") throw "formatfile14" ;
      if (printval.size()<2) throw "formatfile44a" ;
      if (!isdigit(intlit[0])) throw "formatfile15" ;
      if (printval[0]!='\"') throw "formatfile15b" ;
      if (printval[printval.size()-1]!='\"') throw "formatfile15c" ;
      intval = StringToLong(intlit,error_code) ;
      if (error_code==true) throw "formatfile16" ;
      printval2 = string(printval,1,printval.size()-2) ;
      FORMATi[formatname][intval] = printval2 ;
    }
  if (dt=="str") 
    for(i=0;i<stuff[h].size();++i)
    { strlit = stuff[h][i][0] ;
      printval = stuff[h][i][2] ;
      if (strlit=="" || printval=="") throw "formatfile14" ;
      if (strlit.size()<2 || printval.size()<2) throw "formatfile44" ;
      
      if (printval[0]!='\"') throw "formatfile15bb" ;
      if (printval[printval.size()-1]!='\"') throw "formatfile15cc" ;
      if (strlit[0]!='\"') throw "formatfile15bb2" ;
      if (strlit[strlit.size()-1]!='\"') throw "formatfile15cc2" ;
      
      printval2 = string(printval,1,printval.size()-2) ;
      strlit2 = string(strlit,1,strlit.size()-2) ;
      FORMATs[formatname][strlit2] = printval2 ;
      FORMATs_order[formatname][strlit2] = i ;
      FORMATs_order2[formatname][i] = strlit2 ;
    }
}


}   /// end load_formatfile()
