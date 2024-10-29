
/// Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
///                  in 1984, in Massachusetts, USA 



/// December 2020, make copy of numformat.cpp and make changes to it

set<char> digit56789 ;
map<char,char> roundup ;

void numformat_initialize() ;
string roundoff(const string & s1 , int cutoff) ;
int peg_category(const string & s) ;
vector<string> round_format(const vector<string> & column1) ;
vector<string> round_format2(const vector<string> & column1,int cutoff) ;  // year 2020
vector<string> decimal_align(const vector<string> & col1) ;
vector<string> decimal_align2(const vector< vector<string> > & extras , 
                              const vector< vector<string> > & banner) ;   // year 2020

// year 2020, 2nd input argument is new
// do not forget, default argument is here and not at function definition
vector<string> stat_value_reformats(const vector<string> & col1, 
                                    int cutoff_override=-999) ;
string number_type(const string & s) ;
string undo_sci_notatation(const string & s) ;
string remove_spaces_on_margin(const string & s) ;


////////////////////////////////////////////////////////////////////////////


/// June 2011, next 4 functions for more robust roundoff-reformatting 

// December 2020 , minor changes to this function
// December 2020 , add input argument cutoff_override
vector<string> stat_value_reformats(const vector<string> & col1,
                                          int cutoff_override)
{
vector<int> index_prev ;
vector<string> col2 , col3 , col4 ;
int i , j ;
string numtype , val ;
col4 = col1 ;
for(i=0;i<col4.size();++i)
{ if (col4[i]=="") continue ;
  val = col4[i] ;
  if (isspace(val[0]) || isspace(val[val.size()-1])) 
    val=remove_spaces_on_margin(val) ;
  if ( (val.size()>=2 && val[0]=='+' && isdigit(val[1])) ||
       (val.size()>=3 && val[0]=='+' && val[1]=='.' && isdigit(val[2])) )
    val = string(val,1,val.size()-1) ;
  numtype = number_type(val) ;   /// return sci_not or regular 
  if (numtype=="sci_not") val = undo_sci_notatation(val) ;   /// make not scientific not.
  if (numtype=="sci_not" || numtype=="regular")
    { index_prev.push_back(i) ; col2.push_back(val) ; }
  else 
    { if (val=="NotANum") val="" ;    }   /// NaN 
  col4[i] = val ;
}

/// December 2020 change, call round_format OR round_format2, depending
if (cutoff_override>=0) col3 = round_format2(col2,cutoff_override) ;
else col3 = round_format(col2) ;

for(j=0;j<index_prev.size();++j)
  col4[index_prev[j]] = col3[j] ;
return col4 ;
}   /// end fctn stat_value_reformats() 


//////////////////////////////////////////////////////////


/// return sci_not (scientific notation) , or regular (regular number) or "" ;
string number_type(const string & s) 
{
int i=0 , m=s.size() ;
bool not_a_number=true , e_found=false ;
if (s=="") return "" ;

if (s[0]=='+' || s[0]=='-') i=1 ;
if (i>=m) return "" ;

if (i<m && isdigit(s[i])) not_a_number=false ;
if (i+1<m && s[i]=='.' && isdigit(s[i+1])) not_a_number=false ;
if (not_a_number==true) return "" ;

while (i<m && isdigit(s[i])) ++i ;
if (i<m && s[i]=='.') ++i ;
while (i<m && isdigit(s[i])) ++i ;
if (i<m && (s[i]=='e' || s[i]=='E'))
{ e_found=true ;
  ++i ;
  if (i<m && (s[i]=='+' || s[i]=='-')) ++i ;
  while (i<m && isdigit(s[i])) ++i ;
  if (i<m && s[i]=='.') ++i ;
  while (i<m && isdigit(s[i])) ++i ;
  return "sci_not" ;
}
else return "regular" ;

} /// end fctn number_type() 



string undo_sci_notatation(const string & s)
{
bool b_chk ;
double flo1 ;
string s2 ;
flo1 = StringToDouble(s,b_chk) ;
s2 = DoubleToString(flo1,15) ;
return s2 ;
} /// end undo_sci_notatation()


string remove_spaces_on_margin(const string & s)
{
string s2 , s3 ;
int i=0 , m=s.size() ;
while (i<m && isspace(s[i])) ++i ;
s2 = string(s,i,s.size()-i) ;
i = s2.size()-1 ;
while(i>=0 && isspace(s2[i])) --i ;
s3 = string(s2,0,i+1) ;
return s3 ;
}










////////////////////////////////////////////////////////////////////////////

void numformat_initialize() 
{
roundup['0']='1';
roundup['1']='2' ;
roundup['2']='3' ;
roundup['3']='4' ;
roundup['4']='5' ;
roundup['5']='6' ;
roundup['6']='7' ;
roundup['7']='8' ;
roundup['8']='9' ;
roundup['9']='0' ;
digit56789.insert('5');
digit56789.insert('6');
digit56789.insert('7');
digit56789.insert('8');
digit56789.insert('9');
}


//////////////////////////////////////////////////////

/// June 2011, for roundoff() fctn, instead of throw-ing when input string has 
///  unexpected format, just return the original string , in place of reformatted string
///  any blanks on left or right side must be removed before using this function
string roundoff(const string & s1 , int cutoff)
{
int m=s1.size() , i , wheredot , lastcall , goner , i2 ;
string s(s1) ;
bool useminus=false ;
if (s1=="" || s1=="-" || s1=="." || s1=="-.") return s1 ;
if (cutoff<0 || cutoff>30) return s1 ;

/// test print
/// cout << s1 << " " << cutoff << "\n" ;

if (s[m-1]=='.') { s=string(s,0,m-1); m=s.size(); }
if (m>=3 && s[0]=='-' && s[1]=='.' && isdigit(s[2]))
  { s = "-0" + string(s,1,m-1); m=s.size(); }
if (m>=2 && s[0]=='.' && isdigit(s[1]))
  { s = "0" + s ; m=s.size(); }

i=0;
if (s[0]=='-') { i=1; useminus=true; }
if (!(i<m && isdigit(s[i]))) return s1 ;
while (i<m && isdigit(s[i])) ++i ;
if (i==m) return s ;
if (s[i]!='.') return s1 ;  /// just return original instead of throwing
wheredot=i ;
for(i2=i+1;i2<m;++i2) { if (!(isdigit(s[i2]))) return s1 ; }
lastcall = wheredot + cutoff ;
goner = lastcall + 1 ;
if (cutoff==0)
  { lastcall=wheredot-1; goner=wheredot+1; }

if (goner>=m) return s ;
if (digit56789.find(s[goner])==digit56789.end())
  return string(s,0,lastcall+1) ;

// still here? then goner is in range and must be 5-9, must round up
i=lastcall;
while(i>=0 && s[i]=='9') { s[i]='0'; --i; }
if (i>=0 and s[i]=='.') --i ;
while(i>=0 && s[i]=='9') { s[i]='0'; --i; }

if (i>=0 && isdigit(s[i]))
  { s[i]=roundup[s[i]]; return string(s,0,lastcall+1); }
else
  { if (useminus) return ( "-1" + string(s,1,lastcall) ) ;
    else          return ( "1"  + string(s,0,lastcall+1) ) ;
  }

} // end fctn roundoff()



///////////////////////////////////////////////////////////////////////



int peg_category(const string & s)
{
int m=s.size() , a1=-1 , a2=-1 , b1=-1 , b2=-1 , c1=-1 , c2=-1 , 
    dotwhere=-1 , i , peg ;
if (s=="") throw "PEGCAT1" ;

i=0 ;
if (s[0]=='-') i=1;
if (i<m && isdigit(s[i]))
  { a1=i; while(i<m && isdigit(s[i]))++i; a2=i; }
if (i<m && s[i]=='.')
  { dotwhere=i; ++i; }
if (i<m && s[i]=='0')
  { b1=i; while(i<m && s[i]=='0')++i; b2=i; }
if (i<m && isdigit(s[i]))
  { c1=i; }

if (a2-a1==1 && s[a1]!='0')
{ if (s[a1]=='1' && (c1 == -1)) peg = -1 ;
  else peg = 1 ;
}
else if (a2-a1>1) peg = a2-a1 ;
else 
{ if (c1 == -1) peg = 0 ;
  else 
  { if (b1 == -1) peg = -1 ;
    else  peg = -1 - (b2-b1) ;
  }
}

return peg ;
}  // end fctn peg_category() 


/////////////////////////////////////


///////////////////////////////////////////////////

vector<string> round_format(const vector<string> & column1)
{
int DUMMY_HUGE_NEG=-1000 ;
int peg , cutoff , i , pg ;
vector<string> column2 ;
column2.resize(column1.size()) ;
peg = DUMMY_HUGE_NEG ;
for(i=0;i<column1.size();++i)
{ if (column1[i]=="") continue ;
  pg = peg_category(column1[i]) ;
  if (pg!=0 && pg>peg) peg=pg ;
}
if (peg==DUMMY_HUGE_NEG) cutoff = 0 ;
else if (peg>=4)         cutoff = 0 ;
else if (peg==0)         cutoff = 0 ;
else if (peg>0)          cutoff = 4-peg ;
else if (peg<0 && peg!=DUMMY_HUGE_NEG) 
                         cutoff = -peg + 3 ;

/// cout << "peg=" << peg << " cutoff=" << cutoff << " column=" ;
/// for(i=0;i<column1.size();++i) cout << column1[i] << " " ;
/// cout << "\n" ;

for(i=0;i<column1.size();++i)
{ if (column1[i]!="")
     column2[i] = roundoff(column1[i],cutoff) ;
}
return column2 ;
}    // end fctn round_format()


/////////////////////////////////////////////////////////

/// Dec 2020 , this is a modified version of round_format()
///   since cutoff does not need to be guess-timated, can remove much code
///   end-user chooses "cutoff", so don't guess at it
vector<string> round_format2(const vector<string> & column1, int cutoff)
{
int  i ;
vector<string> column2 ;
column2.resize(column1.size()) ;

for(i=0;i<column1.size();++i)
{ if (column1[i]!="")
     column2[i] = roundoff(column1[i],cutoff) ;
}
return column2 ;
}    // end fctn round_format2()



////////////////////////////////////////////////////



///////////////////////////////////////////////////////

vector<string> decimal_align(const vector<string> & col1)
{
string s ;
int i , j , m , before=0 , after=0 ;
vector<string> col2 ;
vector<int> beforedot , afterdot ;
beforedot.resize(col1.size()) ;
afterdot.resize(col1.size()) ;
col2.resize(col1.size());

for(j=0;j<col1.size();++j)
{ m=col1[j].size() ;
  s=col1[j] ;
  for(i=0;i<m && s[i]!='.';++i) ;
  beforedot[j] = i ;
  afterdot[j] = m-i ;
  if (before<beforedot[j]) before=beforedot[j] ;
  if (after<afterdot[j]) after=afterdot[j] ;
}

for(j=0;j<col1.size();++j)
  col2[j] = string(before-beforedot[j],' ') + 
            col1[j] +
            string(after-afterdot[j],' ') ;
return col2 ;
}  // end fctn decimal_align() 

//////////////////////////////////////////


/// December 2020 , this function is new
vector<string> decimal_align2(const vector< vector<string> > & extras ,
                              const vector< vector<string> > & banner )
{
int i , j , k , m , max=0 , before=0 ;
string s ;
vector<int> beforedot , beforedot2 ;
vector<string> combined ;
beforedot.resize(banner.size());
beforedot2.resize(banner.size());
combined.resize(banner.size());

if (extras.size()!=banner.size()) throw "decalign2" ;

for(j=0;j<banner.size();++j)
{ if (banner[j].size()==0) continue ;
  m = banner[j][0].size() ;
  s = banner[j][0] ;
  for(i=0;i<m && s[i]!='.';++i) ;
  beforedot[j] = i ;
  beforedot2[j] = beforedot[j] + extras[j][0].size() ;
  if (before < beforedot2[j])  before = beforedot2[j] ;
}

for(j=0;j<banner.size();++j)
{ if (banner[j].size()==0) continue ;
  s = string(before-beforedot2[j],' ') ;
  for(k=0;k<banner[j].size();++k)
  { if (k<extras[j].size()) s += extras[j][k] ;
    s += banner[j][k] ;
  }
  if (k<extras[j].size()) s += extras[j][k] ;
  combined[j] = s ;
}

for(j=0;j<combined.size();++j)
  { if (max<combined[j].size()) max=combined[j].size();  }
for(j=0;j<combined.size();++j)
  combined[j] += string(max-combined[j].size(),' ');

return combined ;
}    /// end function decimal_align2()












