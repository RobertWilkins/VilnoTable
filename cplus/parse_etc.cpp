
/// Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
///                  in 1984, in Massachusetts, USA 



void parseMAIN() ;
void parsePRINTTO() ;
void parseCOLSPEC() ;
void parseROWSPEC() ;
void parseFILEIMPORT() ;
parsenode * getPARENEXPR() ;
parsenode * getMULTEXPR() ;
parsenode * getWORD_OR_PARENEXPR() ;
parsenode * getWORDEXPR() ;
void parseCATSTATEMENT() ;
void parseSTATSTATEMENT() ;
void parseRELABEL() ;
void parseFORMATFILE() ;
void parseTITLETEXT() ;

void executePTRANS() ;
void PTRANS(connode * , vector< parsenode * >);

void parsetree_again(parsenode *);
void execute_parseagain();

vector<string> remove_placeholder(const vector<string> & vec1) ;
vector<string> remove_placestat(const vector<string> & vec1) ;
void SPLIT_VEC_IN_TWO(const vector<string>& , vector<string>& ,vector<string>& , int );
int tele_type(const string& word) ;
vector<string> CONCATENATE_VEC(const vector<string>& , const vector<string>& ) ;


/////////////////////////////////////////////////

void parseMAIN()
{
parsePRINTTO() ;
parseCOLSPEC() ;
parseROWSPEC() ;
if (seeWORD("cat")) parseCATSTATEMENT() ;
if (seeWORD("stat")) parseSTATSTATEMENT() ;
while (seeWORD("fileimport")) parseFILEIMPORT() ;
parseRELABEL() ;
parseFORMATFILE() ;
parseTITLETEXT() ;
}

void parseCOLSPEC()
{
if (!seeWORD("col")) throw "parsecolspec1" ; 
toss_token() ;
COL_PARSE_TREE = getPARENEXPR() ;
if (!seeSEMICOLON()) throw "parsecolspec2" ; 
toss_token() ;
}

void parseROWSPEC()
{
if (!seeWORD("row")) throw "parserowspec1" ; 
toss_token() ;
ROW_PARSE_TREE = getPARENEXPR() ;
if (!seeSEMICOLON()) throw "parserowspec2" ; 
toss_token() ;
}

////////////////////////////

//// year 2020, December, substantial additions to this function
void parseFILEIMPORT()
{
vector<string> clist , rlist , ff ;
int k ;
string fn , vn , val ;
map<string,string> subset_inform ;

/// Dec 2020, add these local variables
bool finetune_blank=true , digit_explicitly=false ;
vector<long> digit_vec ;
string slot_format ;
long number_slots=1 , slot_counter ;

if (!seeWORD("fileimport")) throw "pimp1" ; 
toss_token() ;

/// Dec 2020, parse slot_ctr, which is new
if (!seeINTLITERAL()) throw "pimp1b" ;
slot_counter = intliteral_and_toss_token() ;

if (!seeWORD("col")) throw "pimp2" ; 
toss_token() ;
if (!seeLBRACK()) throw "pimp3" ; 
toss_token() ;

while (seeWORD())
   clist.push_back(text_and_toss_token()) ;
// is the { before clist.pushback a typo, i think so ;

if (!seeRBRACK()) throw "pimp4" ; 
toss_token() ;
if (!seeWORD("row")) throw "pimp5" ; 
toss_token() ;
if (!seeLBRACK()) throw "pimp6" ; 
toss_token() ;

while (seeWORD()) rlist.push_back(text_and_toss_token()) ;

if (!seeRBRACK()) throw "pimp7" ; 
toss_token() ;
if (!seeLESSTHAN()) throw "pimp8" ; 
toss_token() ;
if (!seeSTRLITERAL()) throw "pimp9" ; 

fn = textunquote_and_toss_token() ;

while ( seeMULTIPLY() || seeWORD() )
{ if (seeMULTIPLY()) 
    { ff.push_back("*") ; toss_token() ; } 
  else ff.push_back(text_and_toss_token()) ;
}

/// new code, April 2011 , for subsetting :
if ( seeCOMMA() )
{ toss_token() ;
  while ( seeWORD() )
  { vn = text_and_toss_token() ;
    if ( seeSTRLITERAL() ) val = textunquote_and_toss_token() ;
    else if ( seeINTLITERAL() ) val = intliteralraw_and_toss_token() ;
    else throw "expectingsubsetliteralvalue" ;
    subset_inform[vn] = val ;  // both int literal and str literal ;
  }
}

///////////////////////////
/// Dec 2020, this section of code is new
if ( seePLUS() )
{ toss_token() ;
  finetune_blank = false ;
  if (!seeINTLITERAL()) throw "pimp9b" ;
  number_slots = intliteral_and_toss_token() ;
  if (seeSTRLITERAL()) slot_format=textunquote_and_toss_token() ;
  if (seeWORD("d"))
  { toss_token() ;
    digit_explicitly=true ;
    if (!seeLBRACK()) throw "pimp9c" ;
    toss_token() ;
    while (seeINTLITERAL()) digit_vec.push_back(intliteral_and_toss_token());
    if (!seeRBRACK()) throw "pimp9d" ;
    toss_token() ;
  }
}



if (!seeSEMICOLON()) throw "pimp10" ; 
toss_token() ;






FIV.push_back(FIVnewentry) ;
k = FIV.size() - 1 ;
FIV[k].COLPATHc = clist ;
FIV[k].ROWPATHc = rlist ;
FIV[k].filename = fn ;
FIV[k].FF1 = ff ;
FIV[k].subset_info = subset_inform ;

/// December 2020 , TPATHc = COLPATHc + ROWPATHc
FIV[k].TPATHc = clist ;
FIV[k].TPATHc.insert(FIV[k].TPATHc.end(),rlist.begin(),rlist.end()) ;

/// Dec 2020 , new code 
FIV[k].slot_ctr = slot_counter ;
FIV[k].finetune_obj.f_blank = finetune_blank ;
FIV[k].finetune_obj.num_slots = number_slots ;
FIV[k].finetune_obj.slot_fmt = slot_format ;
FIV[k].finetune_obj.digit_explicit = digit_explicitly ;
FIV[k].finetune_obj.digits = digit_vec ;

} //   end parseFILEIMPORT() ;


//////////////////////////////////////////////////////


parsenode* getPARENEXPR() 
{
parsenode *g, *g2 ;
if (!seeLPAREN()) throw "PARENEXPR1" ; 
toss_token() ;
g = new parsenode ;
g->type = PARENGRP ;
while (!seeRPAREN()) 
  { g2=getMULTEXPR() ; g->next.push_back(g2) ; }
toss_token() ;
return g ;
}

parsenode* getMULTEXPR() 
{
parsenode *g , *g2 ;
g = new parsenode ;
while (true)
{ g2 = getWORD_OR_PARENEXPR() ;
  g->next.push_back(g2) ;
  if (seeTIMES()) toss_token() ;
   else break ;
}
if (g->next.size()>1)
  { g->type=MULTIPLYGRP ; return g ; }
else 
  { g2=g->next[0] ; g->next.clear() ; delete g ; return g2 ; }
}


//////////////////////////////////////////////////////////////


parsenode* getWORD_OR_PARENEXPR()
{
if (seeWORD()) return getWORDEXPR() ;
else if (seeLPAREN()) return getPARENEXPR() ;
else throw "WORDPARENEXPR1" ; 
}

parsenode* getWORDEXPR() 
{
parsenode* g ;
g = new parsenode ;
g->type = ATOM ;
g->text = text_and_toss_token() ;
return g ;
}

////////////////////////////////////////////////////////////////////



void parseCATSTATEMENT() 
{
gcatparseinfo newgc_entry ;
string vn , intstring ;
int int1 ;
if (!seeWORD("cat")) return ;
toss_token() ;
while (seeWORD())
{ vn = text_and_toss_token();
  if (GCATNAMESset.find(vn)!=GCATNAMESset.end()) throw "pcat1" ; 
  GCATNAMESset.insert(vn) ;
  GCATPARSE[vn]=newgc_entry ;
  if (seeTILDA())
  { toss_token() ;
    if (seeLBRACK()) 
    { toss_token() ;
      if (seeSTRLITERAL()) 
      { GCATPARSE[vn].valliststr.push_back(textunquote_and_toss_token()) ;
        while (seeCOMMA())
        { toss_token() ;
          if (!seeSTRLITERAL()) throw "pcat2" ; 
          GCATPARSE[vn].valliststr.push_back(textunquote_and_toss_token());
        }
      }

      else if (seeINTLITERAL()) 
      { intstring=intliteralraw_and_toss_token() ;
        int1=StringToIntM(intstring) ;
        GCATPARSE[vn].vallistintraw.push_back(intstring) ;
        GCATPARSE[vn].vallistint.push_back(int1) ;
        while (seeCOMMA())
        { toss_token() ;
          if (!seeINTLITERAL()) throw "pcat3" ; 
          intstring=intliteralraw_and_toss_token() ;
          int1=StringToIntM(intstring) ;
          GCATPARSE[vn].vallistintraw.push_back(intstring) ;
          GCATPARSE[vn].vallistint.push_back(int1) ;
        }
      }

      else throw "pcat4" ;    // need see intlit or strlit 
      if (!seeRBRACK()) throw "pcat5" ; 
      toss_token() ;
    }    // END LBRACK

    else if (seeWORD("formatfile")) 
    { toss_token() ;
      if (!seeLPAREN()) throw "pcat6" ; 
      toss_token() ;
      if (!seeSTRLITERAL()) throw "pcat7" ;
      /// GCATPARSE[vn].formatwhere = textunquote_and_toss_token() ;
      /// Feb 2011 change 
      GCATPARSE[vn].format_to_import = textunquote_and_toss_token() ;
      if (!seeRPAREN()) throw "pcat8" ; 
      toss_token() ;
    }
    else throw "pcat9" ;      // AFTER ~ , NEED .....
  }    // END TILDA 
}    // END WHILE-SEEWORD
if (!seeSEMICOLON()) throw "pcat10" ; 
toss_token() ;
}   //// end parseCATSTATEMENT() 

///////////////////////////////////////////////////



//// calling PTRANS() 

void executePTRANS()
{
connode * UNDER ;
vector<parsenode*> LP ;

UNDER = new connode ; 
UNDER->type = PLACEHOLDER ;
UNDER->text = "TREETOP" ;
LP.clear() ;
COL_CON_TREE_TOP = UNDER ;
LP.push_back(COL_PARSE_TREE) ;
PTRANS(UNDER,LP)  ;     /// repeat this for ROW SITU 

UNDER = new connode ; 
UNDER->type = PLACEHOLDER ;
UNDER->text = "TREETOP" ;
LP.clear() ;
ROW_CON_TREE_TOP = UNDER ;
LP.push_back(ROW_PARSE_TREE) ;
PTRANS(UNDER,LP)  ;     /// and again for ROW SITU 
}    // end executePTRANS() 

///////////////////////////////////////////////////

void PTRANS(connode * UNDER1 , vector< parsenode * > LP)
{
connode *UNDER2 ;
vector< parsenode * > LP2 ;
parsenode *Q ;
string tx ;
int i, k ;
if (LP.empty()) return ;
Q=LP[0] ;
if (Q->type==ATOM)
{ UNDER2 = new connode ;
  UNDER1->next.push_back(UNDER2) ;
  tx=Q->text ;
  UNDER2->text = tx ;
  if (CATNAMESset.find(tx)!=CATNAMESset.end()) UNDER2->type=CAT ;
  else if (STATNAMESset.find(tx)!=STATNAMESset.end()) UNDER2->type=STAT ;
  else UNDER2->type = PLACEHOLDER ;
  if (LP.size()>=2)
  { for(i=1;i<LP.size();++i) LP2.push_back(LP[i]) ;
    PTRANS(UNDER2,LP2) ;
  }
}
else if (Q->type==MULTIPLYGRP)
{ for(i=0;i<Q->next.size();++i) LP2.push_back(Q->next[i]) ;
  for(i=1;i<LP.size();++i) LP2.push_back(LP[i]) ;
  PTRANS(UNDER1,LP2) ;
}
else if (Q->type==PARENGRP)
{ for(k=0;k<Q->next.size();++k)
  { LP2.clear() ;
    LP2.push_back(Q->next[k]) ;
    for(i=1;i<LP.size();++i) LP2.push_back(LP[i]) ;
    PTRANS(UNDER1,LP2) ;
  }
}
}  //   end PTRANS() ;



///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////


void parsetree_again(parsenode * p)
{
if (p->type==ATOM)
  { if (tablespell.find(p->text)!=tablespell.end()) throw "PARSETREEAGAIN1" ; 
    if (p->text=="") throw "PARSETREEAGAIN2" ; 
    tablespell.insert(p->text) ;
  }
for(int i=0;i<p->next.size();++i)
   parsetree_again(p->next[i]) ;
}     //      end parsetree_again() ;



void execute_parseagain()
{
set<string>::const_iterator q ;
string vn , s ;
int m ;

parsetree_again(COL_PARSE_TREE);
parsetree_again(ROW_PARSE_TREE);

for(q=tablespell.begin();q!=tablespell.end();++q)
{ vn = *q ;
  m = vn.size() ;
  if (STATNAMESset.find(vn)!=STATNAMESset.end()) continue ;
  if (GCATNAMESset.find(vn)!=GCATNAMESset.end())
    { tcat_gcat[vn]=vn ; CATNAMESset.insert(vn) ; }
  else 
    { if (isdigit(vn[m-1]))
      { s = remove_trailing_digits(vn) ;
        if (GCATNAMESset.find(s)!=GCATNAMESset.end())
         { tcat_gcat[vn]=s ; CATNAMESset.insert(vn); }
      }
    }
}

}   // end execute_parseagain() ;

//////////////////////////////////


void parseRELABEL()
{
string tele , txt ;
if (!seeWORD("relabel")) return ;
toss_token() ;
while (seeWORD())
{ tele = text_and_toss_token();
  if (!seeTILDA()) throw "prelabel1" ; 
  toss_token();
  if (!seeSTRLITERAL()) throw "prelabel2" ;
  txt = textunquote_and_toss_token() ;
  RELABEL_FORMAT[tele] = txt ;
}
if (!seeSEMICOLON()) throw "prelabel3" ; 
toss_token() ;
}    //// end parseRELABEL() 


void parseSTATSTATEMENT()
{
string statword ;
if (!seeWORD("stat")) throw "pstat1" ; 
toss_token() ;
while (seeWORD())
{ statword=text_and_toss_token() ;
  STATNAMESset.insert(statword) ;
}
if (!seeSEMICOLON()) throw "pstat2" ; 
toss_token() ;
}    //// end parseSTATSTATEMENT() 

void parsePRINTTO()
{
if (!seeWORD("printto")) throw "pprint1" ; 
toss_token() ;
if (!seeSTRLITERAL()) throw "pprint2" ;
tableprintfilename = textunquote_and_toss_token() ;
if (!seeSEMICOLON()) throw "pprint3" ; 
toss_token() ;
}


void parseFORMATFILE() 
{
if (!seeWORD("formatfile")) return  ; 
toss_token() ;
if (!seeSTRLITERAL()) throw "pformfile2" ;
format_filename = textunquote_and_toss_token() ;
if (!seeSEMICOLON()) throw "pformfile3" ; 
toss_token() ;
}


void parseTITLETEXT()
{
if (!seeWORD("title")) return ; 
toss_token() ;
if (!seeSTRLITERAL()) throw "ptitletext2" ;
titletext = textunquote_and_toss_token() ;
if (!seeSEMICOLON()) throw "ptitletext3" ; 
toss_token() ;
}




/////////////////////////////////////////////////////////////

vector<string> remove_placeholder(const vector<string> & vec1)
{
vector<string> vec2 ;
int i ;
for(i=0;i<vec1.size();++i)
{ if (CATNAMESset.find(vec1[i])!=CATNAMESset.end() || 
      STATNAMESset.find(vec1[i])!=STATNAMESset.end() )
     vec2.push_back(vec1[i]) ;
}
return vec2 ;
}    // end function remove_placeholder()



vector<string> remove_placestat(const vector<string> & vec1)
{
vector<string> vec2 ;
int i ;
for(i=0;i<vec1.size();++i)
{ if (CATNAMESset.find(vec1[i])!=CATNAMESset.end())
     vec2.push_back(vec1[i]) ;
}
return vec2 ;
}    // end function remove_placestat()



void SPLIT_VEC_IN_TWO(const vector<string>& vec1,
          vector<string>& vec1a,vector<string>& vec1b, int cutoffsize)
{
int i ;
if (cutoffsize>vec1.size()) throw "SPLITVECTWO1" ;
vec1a.clear() ;
vec1b.clear() ;
for(i=0;i<cutoffsize;++i) vec1a.push_back(vec1[i]);
for(i=cutoffsize;i<vec1.size();++i) vec1b.push_back(vec1[i]) ;
}    // end function SPLIT_VEC_IN_TWO()




int tele_type(const string& word)
{
if (word=="") throw "TELETYPE1" ;
if (tablespell.find(word)==tablespell.end()) throw "TELETYPE2" ;
if (CATNAMESset.find(word)!=CATNAMESset.end()) return CAT ;
if (STATNAMESset.find(word)!=STATNAMESset.end()) return STAT ;
return PLACEHOLDER ;
}




vector<string> CONCATENATE_VEC(const vector<string>& vec1, const vector<string>& vec2)
{
vector<string> vec3 ;
int i ;
vec3 = vec1 ;
for(i=0;i<vec2.size();++i) vec3.push_back(vec2[i]) ;
return vec3 ;
}     // end function CONCATENATE_VEC() 








