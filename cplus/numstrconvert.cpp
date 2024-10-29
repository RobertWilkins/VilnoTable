
/// Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
///                  in 1984, in Massachusetts, USA 



// SOME FUNCTIONS IN THIS FILE YOU DON'T NEED TO CARRY OVER
// StringToLong or StringToInt , make up your mind

string IntToStringM(long intval,int width=1) ;
string lowercase_str(const string & s1) ;
void string_writein(string & bigstr, const string & smallstr, int offset) ;
string underscorestring(int w) ; 
string blankstring(int w) ;
vector<string> split_string_vs(string s1, string x) ;
vector<string> split_string_blank( string s1 ) ;
vector<string> split_string_delim( string s1 , char delim) ;
string remove_trailing_digits(const string & v) ;
int StringToIntM(const string & value) ;
long StringToLong(string value, bool & errcode) ;

double StringToDouble(string value, bool & errcode);
bool weirdchar(const string & s);
bool letterdigitunderscore(const string & s);

void assignupto(string & s, const char * cp, long maxlim) ;
string IntToString(long intval) ;

string PosIntToString(unsigned long intval);

string DoubleToString(const double & data) ;
string DoubleToStringScientific(const double & data) ;
string DoubleToString(const double & data, int precise);

void replaceblanks(string & s , char c) ;
void replacetrailingblanks(string & s , char c) ;
vector<long> vectorlongsum(const vector<long> & v1, const vector<long> & v2) ;
vector<int> vectorintsum(const vector<int> & v1, const vector<int> & v2) ;


// these 2 tiny utility functions added 2020 2021
void str_vec_assign(vector<string> & vec1 , const string & s, long index) ;
void str_vec_sizeup(vector<string> & vec1, long size) ;


////////////////////////////////////////////////////////////////////////

// default : width=1 
string IntToStringM(long intval,int width)
{
string s ;
if (intval==missing) return string(width,' ') ;
s=IntToString(intval) ;
if (s.size()<width) s = string(width-s.size(),' ') + s ;
return s ;
}


string lowercase_str(const string & s1)
{
string s2=s1 ;
for(int i=0;i<s1.size();++i)
   s2[i] = tolower(s1[i]) ;
return s2 ;
}

////////////////////////////////////////////////////////////////////

void string_writein(string & bigstr, const string & smallstr, int offset)
{
if (offset>bigstr.size()) throw "stringwritein1" ;
bigstr.replace(offset,smallstr.size(),smallstr,0,smallstr.size()) ;
}

string underscorestring(int w) 
{  return string(w,'_') ; }

string blankstring(int w) 
{  return string(w,' ') ; }

///////////////////////////////////////////////////////////////////

vector<string> split_string_vs(string s1, string x)
{
vector<string> svec ;
int k1 , k2 , i , m=s1.size() ;
k2=0 ;
for(i=0;i<x.size()+1 && k2<m;++i)
{ k1=k2 ;
  if (i<x.size())
     while (k2<m && s1[k2]!=x[i]) ++k2 ;
  else 
     k2 = m ;
  svec.push_back( string(s1,k1,k2-k1) ) ;
  if (k2<m) ++k2 ;
}
return svec ;
}  

vector<string> split_string_blank( string s1 )
{
int k1 , k2 , m=s1.size() ;
vector<string> svec ;
k2 = 0 ;
while (k2<m && s1[k2]==' ') ++k2 ;
while (k2<m)
{ k1 = k2 ;
  while (k2<m && s1[k2]!=' ') ++k2 ;
  svec.push_back( string(s1,k1,k2-k1) ) ;
  while (k2<m && s1[k2]==' ') ++k2 ;
}
return svec ;
}  



vector<string> split_string_delim( string s1 , char delim)
{
int k1 , k2 , m=s1.size() ;
vector<string> svec ;
k2 = 0 ;
while (k2<m)
{ k1 = k2 ;
  while (k2<m && s1[k2]!=delim) ++k2 ;
  svec.push_back( string(s1,k1,k2-k1) ) ;
  if (k2<m) ++k2 ;
}
if (m==0) svec.push_back("");
if (m>0 && s1[m-1]==delim) svec.push_back("");
return svec ;
}  


///////////////////////////////////////////


string remove_trailing_digits(const string & v)
{
int k=v.size()-1 ;
string s ;
while (k>=0 && isdigit(v[k])) --k ;
s.assign(v,0,k+1) ;
return s ;
}




//////////////////////////////////////////




int StringToIntM(const string & value)
{
bool errorcode ;
int answer ;
answer = (int) StringToLong(value,errorcode) ;
if (errorcode==true) answer=missing ;
return answer ;
}   // end StringToIntM()



long StringToLong(string value, bool & errcode)
{
long result ;
char *tmp ;
errno=0 ;
result=strtol(value.c_str(),&tmp,10);
errcode=false;
if(errno==ERANGE) errcode=true;
return result ;
}

double StringToDouble(string value, bool & errcode)
{
double result ;
char *tmp ;
errno=0 ;
result=strtod(value.c_str(),&tmp);
errcode=false;
if(errno==ERANGE) errcode=true;
return result ;
}


bool weirdchar(const string & s)
{
long i ;
bool answer=false ;
for(i=0;i<s.size();++i) 
  { if(!isprint(s[i])) answer=true ; }
return answer;
}


bool letterdigitunderscore(const string & s)
{
long i ;
if (s.size()==0) return false ;
for(i=0;i<s.size();++i) 
  { if( !isalnum(s[i]) && s[i]!='_') return false ; }
return true ;
}



// this function similar to string.assign(charptr,numchar)
// but checks for terminating null to make smaller string 
void assignupto(string & s, const char * cp, long maxlim)
{
long i ;
for(i=0;i<maxlim && cp[i]!='\0';++i);
s.assign(cp,i);
}

string IntToString(long intval)
{
static char buff[21] ;
long numchar ;
string result ;
//memset(buff,'\0',21);
numchar = sprintf(buff,"%li",intval);
if (numchar<1 || numchar>21) throw BUG("INTTOSTRING-SPRINTFNUMCHARS");
result.assign(buff,numchar) ;
return result ;
}


///////////////////////////

string PosIntToString(unsigned long intval)
{
static char buff[21] ;
long numchar ;
string result ;
//memset(buff,'\0',21);
numchar = sprintf(buff,"%lu",intval);
if (numchar<1 || numchar>21) throw BUG("POSINTTOSTRING-SPRINTFNUMCHARS");
result.assign(buff,numchar) ;
return result ;
}



///////////////////////////



string DoubleToString(const double & data)
{
static char buff[51] ;
long numchar ;
string result ;
//memset(buff,'\0',51);
numchar = sprintf(buff,"%g",data);
if (numchar<1 || numchar>51) throw BUG("DOUBLETOSTRING-SPRINTFNUMCHARS");
result.assign(buff,numchar) ;
return result ;
} 


string DoubleToStringScientific(const double & data)
{
static char buff[51] ;
long numchar ;
string result ;
//memset(buff,'\0',51);
numchar = sprintf(buff,"%e",data);
if (numchar<1 || numchar>51) throw BUG("DOUBLETOSTRING2-SPRINTFNUMCHARS");
result.assign(buff,numchar) ;
return result ;
} 


string DoubleToString(const double & data, int precise)
{
if (precise<0 || precise>1000) throw BUG("DOUBLETOSTRING3-PRECISE");
static char buff[151] ;
long numchar ;
string result ;
//memset(buff,'\0',151);
numchar = sprintf(buff,"%.*f",precise,data);
if (numchar<1 || numchar>151) throw BUG("DOUBLETOSTRING3-SPRINTFNUMCHARS");
result.assign(buff,numchar) ;
return result ;
} 


void replaceblanks(string & s , char c)
{
long i ;
for(i=0;i<s.size();++i) { if (s[i]==' ') s[i]=c ; }
}



void replacetrailingblanks(string & s , char c)
{
long i ;
for(i=s.size()-1;i>=0 && s[i]==' ';--i)  s[i]=c ;
} 


//////////////////////////////////////////////////////////////////


vector<long> vectorlongsum(const vector<long> & v1, const vector<long> & v2) 
{
long i ;
vector<long> v ;
v = v1 ;
for(i=0;i<v2.size();++i) v.push_back(v2[i]) ;
return v ;
}

vector<int> vectorintsum(const vector<int> & v1, const vector<int> & v2) 
{
long i ;
vector<int> v ;
v = v1 ;
for(i=0;i<v2.size();++i) v.push_back(v2[i]) ;
return v ;
}


//////////////////////////////////////////////////////////////////////

/// These two small utility functions added 2021


void str_vec_assign(vector<string> & vec1 , const string & s, long index)
{
if (index>=vec1.size()) vec1.resize(index+1) ;
vec1[index] = s ;
}


void str_vec_sizeup(vector<string> & vec1, long size)
{
if (size>vec1.size()) vec1.resize(size) ;
}






