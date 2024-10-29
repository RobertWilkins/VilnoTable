// Copyright 2002-2006, Robert Wilkins (class 1984, Newton North HS, MA, USA)

/// Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
///                  in 1984, in Massachusetts, USA 


// find this codetag tr bug rsunex 
//           stringtolong string to double


static map<char,int> shortlist ;
static map<string,int> twolist ;
CodeTag nextTOK1 , nextTOK2 ;
static char hw=' ' ;
//////////////////////////////////

class hzholder {
public:
  string tx ;
  map< long , pair<long,long> > tokidcolnum ;
  long rownum ;
};

static char hz=' ' ;
long hzindex=-1 , hzlinenum=-1 , hztokidctr=-1 ,
     currentSTtokid=-1 , currentSTrownum=-1 , 
     currentPARAtokid=-1 , currentPARArownum=-1 ;
ifstream hzinput ;
list<hzholder> hzh ;

/////////////////////////////////
void offSOURCE() ;
void emptyreadsourcedicts();
void setupSOURCE(const char *);
CodeTag peekTOK1();
CodeTag peekSECONDTOK();
CodeTag getTOK();
CodeTag getTOK1();
///////////////////////////////////

void hz_open(const char *);
char hz_peek();
char hz_get();
void hz_close();


//long willreadtokennow();
//void justreadtoken();
//long mostrecenttokenlinenum(string &);
//long mostrecentlinenum();
//void resetCURRENTSTATEMENT();
//void resetCURRENTPARAGRAPH();
//void getCURRSTPAR(int, long&, list<string>&, const pair<long,long>&,
//                    pair<long,long>&, pair<long,long>& );
//void getCURRSTPLUS(long&, list<string>&, const pair<long,long>&,
//                    pair<long,long>&, pair<long,long>& );
//void getCURRENTSTATEMENT(long & , list<string> &);
//void getCURRENTPARAGRAPH(long & , list<string> &);

////////////////////////////////////////////////////////////////////////////////////


void hz_open(const char * filename)
{
hzholder tmp ;
bool b ;
if (!hzh.empty()) throw BUG("HZOPEN-HZHNOTEMPTY");
if (!hzinput) throw rsUnex("HZOPEN-FILEPTRERR");

hzinput.open(filename,ios::in);
if (!hzinput) throw rsUnex("HZOPEN-OPENFAIL",filename);

hztokidctr = 0 ;
// currentSTtokid=currentPARAtokid=currentSTrownum=currentPARArownum=-1;

hzh.push_back(tmp);
b = getline(hzinput,hzh.back().tx);
if (!b) throw rsUnex("HZOPEN-EMPTYFILE",filename);

hzh.back().tx += "\n" ;
hz = hzh.back().tx[0] ;
if (!isprint(hz) && !isspace(hz)) throw rsUnex("HZOPEN-BINARY",filename);
hzindex = 0 ;
hzh.back().rownum=hzlinenum=1 ;
}   // end hz_open()  


void hz_close()
{
hzinput.close();
hzinput.clear();
hzh.clear();
hz=' ';
hzindex=hzlinenum=hztokidctr=-1;
// currentSTtokid=currentPARAtokid=currentSTrownum=currentPARArownum=-1;
}   // end hz_close() 


char hz_peek() { return hz ; } 


char hz_get()
{
static char hzz ;
static hzholder tmp ;
static bool b ;
hzz = hz ;
if (hz==EOF) return EOF ;

if (!isprint(hz) && !isspace(hz)) throw rsUnex("HZGET-BINARY");
if (hzh.empty()) throw BUG("HZGET-HZHEMPTY");
if (hzh.back().tx.empty()) throw BUG("HZGET-TXEMPTY");
if (hzindex<0 || hzindex>hzh.back().tx.size()-1) throw BUG("HZGET-HZINDEX1");

if (hzindex < hzh.back().tx.size()-1)
{ hzindex++;
  hz = hzh.back().tx[hzindex] ;
} 
else
{ if (hz!='\n') throw BUG("HZGET-HZNOTNEWLINE");
  hzh.push_back(tmp);
  b = getline(hzinput,hzh.back().tx);
  if (!b)
  { hzh.pop_back() ;
    hz = EOF ;
    hzindex = hzlinenum = -1 ;
  }
  else
  { hzh.back().tx += "\n" ;
    hz = hzh.back().tx[0] ;
    hzindex = 0 ;
    hzlinenum++ ;
    hzh.back().rownum = hzlinenum ;
  }
}
return hzz ;
}   // end hz_get() 



////////////////////////////////////////////////////////////////////////////////////


void offSOURCE() 
{ 
hz_close() ; 
hw=' ';
nextTOK1.specify=nextTOK2.specify="";
nextTOK1.tokid1=nextTOK1.tokid2=nextTOK2.tokid1=nextTOK2.tokid2=-1;
nextTOK1.type=nextTOK2.type=0;
}   // end offSOURCE() 

CodeTag peekTOK1() { return nextTOK1; }
CodeTag peekSECONDTOK() { return nextTOK2 ;}

void emptyreadsourcedicts()
{
shortlist.clear();
twolist.clear();
hw=' ';
nextTOK1.specify=nextTOK2.specify="";
nextTOK1.tokid1=nextTOK1.tokid2=nextTOK2.tokid1=nextTOK2.tokid2=-1;
nextTOK1.type=nextTOK2.type=0;
} // end emptyreadsourcedicts()


void setupSOURCE(const char * fullpathsource)
{
hz_open(fullpathsource);

shortlist['!']=tr::EXCLAM   ; shortlist['=']=tr::EQUAL ; 
shortlist['>']=tr::OP_REL   ; shortlist['<']=tr::OP_REL ; 
shortlist['-']=tr::OP_MINUS ; shortlist['+']=tr::OP_PLUS ; 
shortlist['/']=tr::OP_DIV   ; shortlist['*']=tr::OP_MULT ; 
shortlist[':']=tr::COLON    ; shortlist[';']=tr::SEMICOLON ; 
shortlist['{']=tr::LCURLY   ; shortlist['}']=tr::RCURLY ; 
shortlist['[']=tr::LBRACK   ; shortlist[']']=tr::RBRACK ; 
shortlist['(']=tr::LPAREN   ; shortlist[')']=tr::RPAREN ; 
shortlist[',']=tr::COMMA    ; 

// July 2010 addition ;
shortlist['~']=tr::TILDA ;

twolist["!="]=tr::OP_REL ;
twolist[">="]=tr::OP_REL ;
twolist["<="]=tr::OP_REL ;
twolist["=="]=tr::OP_REL ;
twolist["->"]=tr::ARROW ;

hw=' ' ;
nextTOK1=getTOK();
nextTOK2=getTOK();
} // end setupSOURCE function ;


CodeTag getTOK1()
{
CodeTag tok2 ;
tok2=nextTOK1;
nextTOK1=nextTOK2;
nextTOK2=getTOK();
return tok2 ;
}  // end getTOK1() 


CodeTag getTOK()
{
CodeTag tok1 ;
char quotetype , shortsymbol ;
bool dotfound , esignfound , strnumerrcode ;
string twosymbol ;
long  i ;
long inttmp ;
double flotmp ;
tok1.wraptype=0 ;

while(isspace(hw) || (hw=='/' && hz_peek()=='/') )
{ if (isspace(hw))
   { while(isspace(hw)) hw = hz_get() ; }
  else 
  { while (hw!='\n' && hw!=EOF) hw = hz_get() ;
    if (hw=='\n') hw = hz_get() ;
  }
}
if (hw==EOF) { tok1.type=tr::ENDOFFILE; return tok1; }
// tok1.tokid1 = tok1.tokid2 = willreadtokennow();

if (hw=='"' || hw=='\'')
{ quotetype=hw;
  tok1.wraptype=tr::LITERAL;
  tok1.type=tr::STR;
  hw=hz_get();
  while(hw!=quotetype && hw!=EOF && hw!='\n')   // do not allow multiline string
  { tok1.specify.append(&hw,1);
    hw=hz_get();
  }
  if(hw!=quotetype) throw rsUnex("GETTOK-QUOTEMISS");
  hw=hz_get();
}    // end quoted literal section 

else if (hw=='_' || isalpha(hw))
{ tok1.type=tr::WORDUNK;
  while(isalnum(hw)||hw=='_')
  { tok1.specify.append(&hw,1);
    hw=hz_get();
  }
  for(i=0;i<tok1.specify.size();++i) 
    tok1.specify[i]=tolower(tok1.specify[i]) ;
}    // end word token section

else if (hw=='.' || isdigit(hw))
{ dotfound=esignfound=false;
  tok1.wraptype=tr::LITERAL;
  while (isdigit(hw))
  { tok1.specify.append(&hw,1);
    hw=hz_get();
  }
  if (hw=='.')
  { dotfound=true ;
    tok1.specify.append(&hw,1);
    hw=hz_get();
  }
  while (isdigit(hw))
  { tok1.specify.append(&hw,1);
    hw=hz_get();
  }
  if(tok1.specify==".") throw rsUnex("GETTOK-LONEDOT");

  if (hw=='e' || hw=='E')
  { esignfound=true ;
    tok1.specify.append(&hw,1);
    hw=hz_get();
    if (hw=='+' || hw=='-')
    { tok1.specify.append(&hw,1);
      hw=hz_get();
    }
    if (!isdigit(hw)) throw rsUnex("GETTOK-EXPNODIGIT");
    while (isdigit(hw))
    { tok1.specify.append(&hw,1);
      hw=hz_get();
    }
    if (hw=='.') throw rsUnex("GETTOK-NONINTEXP");
  }    // end e/E section 

  if(dotfound==false && esignfound==false)
  { tok1.type=tr::INTR;   
    inttmp=StringToLong(tok1.specify,strnumerrcode);  
    if (strnumerrcode) throw rsUnex("GETTOK-STRNUMERR1");
  }
  else 
  { tok1.type=tr::FLO;
    flotmp=StringToDouble(tok1.specify,strnumerrcode);  
    if (strnumerrcode) throw rsUnex("GETTOK-STRNUMERR2");
  }
}   // end numeric token section 

else if (shortlist.find(hw)!=shortlist.end())
{ shortsymbol=hw;
  hw=hz_get();
  if(shortsymbol=='!' && hw!='=') throw rsUnex("GETTOK-LONEEXCLAM");
  twosymbol.append(&shortsymbol,1);
  twosymbol.append(&hw,1);
  if(twolist.find(twosymbol)!=twolist.end())
  { tok1.type=twolist[twosymbol];
    if(tok1.type==tr::OP_REL) tok1.specify=twosymbol;
    hw=hz_get();
  }
  else
  { tok1.type=shortlist[shortsymbol];
    if(tok1.type==tr::OP_REL) tok1.specify.assign(&shortsymbol,1);
  }
}   // end punctuation token section 

else throw rsUnex("GETTOK-UNK1");
// justreadtoken();
return tok1;
} // end of getTOK() function ;


///////////////////////////////////////////////////


bool seeENDOFFILE()
{ return nextTOK1.type==tr::ENDOFFILE ; }

bool seeWORD(const string & s = "")
{
if (s=="") return (nextTOK1.type==tr::WORDUNK) ;
else return (nextTOK1.type==tr::WORDUNK && nextTOK1.specify==s) ;
}



void toss_token()
{ getTOK1() ; }


string text_and_toss_token()
{
string val ;
if (nextTOK1.type!=tr::WORDUNK) throw "textandtosstoken1" ;
val=nextTOK1.specify ;
getTOK1();
return val ;
}



string textunquote_and_toss_token()
{
string val ;
if (nextTOK1.type!=tr::STR || nextTOK1.wraptype!=tr::LITERAL) 
    throw "textunquoteandtosstoken1" ;
val=nextTOK1.specify ;
getTOK1();
return val ;
}




long intliteral_and_toss_token()
{
long val ;
bool errorcode ;
if (nextTOK1.type!=tr::INTR || nextTOK1.wraptype!=tr::LITERAL) 
     throw "intliteralandtosstoken1" ;
val=StringToLong(nextTOK1.specify,errorcode) ;
if (errorcode==true) throw "intliteralandtosstoken2" ;
getTOK1();
return val ;
}

string intliteralraw_and_toss_token()
{
string val ;
if (nextTOK1.type!=tr::INTR || nextTOK1.wraptype!=tr::LITERAL) 
     throw "intliteralrawandtosstoken1" ;
val=nextTOK1.specify ;
getTOK1();
return val ;
}

bool seeSTRLITERAL()
{ 
return (nextTOK1.type==tr::STR && nextTOK1.wraptype==tr::LITERAL) ;
}

bool seeINTLITERAL()
{ 
return (nextTOK1.type==tr::INTR && nextTOK1.wraptype==tr::LITERAL) ;
}

///////


bool seeLESSTHAN() 
{ return nextTOK1.type==tr::OP_REL && nextTOK1.specify=="<" ; }

bool seeTILDA() { return nextTOK1.type==tr::TILDA ; }

////  bool see() { return nextTOK1.type==tr:: ; }


bool seeSEMICOLON() { return nextTOK1.type==tr::SEMICOLON ; }
bool seeLPAREN() { return nextTOK1.type==tr::LPAREN ; }
bool seeRPAREN() { return nextTOK1.type==tr::RPAREN ; }
bool seeLBRACK() { return nextTOK1.type==tr::LBRACK ; }
bool seeRBRACK() { return nextTOK1.type==tr::RBRACK ; }
bool seeCOMMA() { return nextTOK1.type==tr::COMMA ; }

bool seeMULTIPLY() { return nextTOK1.type==tr::OP_MULT ; }
bool seeTIMES() { return nextTOK1.type==tr::OP_MULT ; }


/// Dec 2020 , add function seePLUS()
bool seePLUS() { return nextTOK1.type==tr::OP_PLUS ; }


////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////


vector<string> split_string_tk(const string & s)
{

vector<string> stuff ;
string word , twosymbol ;
int i=0 , m=s.size() , u , h ;
char quotetype , shortsymbol , secondsymbol ;

while (i<m) {

while( i<m && isspace(s[i]) ) i++ ;
if (i==m) break ;

if (s[i]=='"' || s[i]=='\'')
{ quotetype=s[i] ;
  h=i ; 
  ++i ;
  while(i<m && s[i]!=quotetype) ++i ;
  if (i==m) throw rsUnex("SPLIT9-IM");
  if (s[i]=='\n') throw rsUnex("SPLIT9-QN");
  if (s[i]!=quotetype) throw rsUnex("SPLIT9-QQNOT");
  i++ ;
  word = string(s,h,i-h) ;
  stuff.push_back(word) ;
}    // end quoted literal section 


else if (s[i]=='_' || isalpha(s[i]))
{ h=i;
  while(i<m && (isalnum(s[i])||s[i]=='_')) ++i ;
  word = string(s,h,i-h) ;
  for(u=0;u<word.size();++u) word[u]=tolower(word[u]) ;
  stuff.push_back(word) ;
}    // end word token section


else if (s[i]=='.' || isdigit(s[i]))
{ h=i ;
  while (i<m && isdigit(s[i])) ++i ;
  if (i<m && s[i]=='.')   ++i ; 
  while (i<m && isdigit(s[i])) ++i ;
  // remember this could get lone dot 
  word = string(s,h,i-h) ;
  stuff.push_back(word) ;  
}   // end numeric token section 

else if (shortlist.find(s[i])!=shortlist.end())
{ shortsymbol=s[i];
  if (i+1<m) 
    { secondsymbol = s[i+1] ;
      twosymbol = string(s,i,2) ;
      if(twolist.find(twosymbol)!=twolist.end())
        { word=twosymbol; i=i+2; }
      else 
        { word=string(s,i,1); i=i+1; }
    }
  else
      { word=string(s,i,1); i=i+1; }
  stuff.push_back(word) ;
}   // end punctuation token section 

else throw "splitstringtk-unk" ;

}   // end while(i<m) loop 


return stuff ;

}   // end function split_string_tk() 







