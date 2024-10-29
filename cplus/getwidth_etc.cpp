
/// Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
///                  in 1984, in Massachusetts, USA 




void GETWIDTH(expnode *) ;
void COLTREE_PRINTOUT(expnode * ) ;
void executeCOLTREEPRINT() ;
void GETOFFSET(expnode *) ;
void LEAFCOUNT(expnode *) ;
void executeLEAFCOUNT() ;
// void FIVitem::spectrum_and_insert()
// void FIVitem::send_to_matrix()
void send_to_matrix2() ;
void SAYWHERE(expnode *) ;

void FILL_TOP() ;
void FILL_UNDER(connode * p , expnode * q) ;
void expand_big_tree(vector<int> where, vector<int> catlevel,
               connode * whichtree1, expnode * whichtree) ;

void SETUP_PRNT(expnode *) ;
void ROWTREE_PRINTOUT(expnode *) ;
void executeROWTREEPRINT() ;
void finish_the_print() ;
int maximum_depth(expnode*) ;

///////////////////////////////////////////////

/// Jan 2021 , only change spelling, matrix2 -> matrix3
void GETWIDTH(expnode * HERE)
{
string tcat , gcat , s1 , s ;
int dt , topwidth , underwidth , cindex  ;
map<int,expnode*>::iterator q ;
if (HERE->type==CATVALUE)
{ tcat=HERE->text ;
  gcat=tcat_gcat[tcat] ;
  dt=datatype_of_gcat[gcat] ;
  /// July 2010 , modify , add second input arg 
  /// Feb 2011 , just use GCAT_FORMAT straight
  /// if (dt==INT) s=IntToStringM(HERE->catval,GCAT_INTWIDTH[gcat]) ;
  /// else if (dt==STR) s=GCAT_FORMAT[gcat][HERE->catval] ;
  s=GCAT_FORMAT[gcat][HERE->catval] ;    /// Feb 2011, this is all u need , preprepped
}
else
{ s1=HERE->text ;
  s=s1 ;
  if (RELABEL_FORMAT.find(s1)!=RELABEL_FORMAT.end()) 
     s=RELABEL_FORMAT[s1] ;
}
HERE->prnt=s ;
topwidth=s.size() ;

if (HERE->next.empty() && HERE->type!=CATHEAD)
{ cindex=colindex_map[HERE->conwhere][HERE->catwhere] ;
  // underwidth=MATRIXCOLUMN_WIDTH(matrix2[cindex]) ;
  // know each element of column has same width, via decimal_align() 
  // column will have least one entry unless row tree is really weird 
  //// Jan 2021, minor spelling change, matrix2 -> matrix3
  if (matrix3[cindex].size()>0)
   underwidth = matrix3[cindex][0].size() ;
  else underwidth=0 ;
}
else
{ underwidth=0 ;
  for(q=HERE->next.begin();q!=HERE->next.end();++q)
  { GETWIDTH(q->second) ;
    underwidth += (q->second)->width + 1 ;
  }
  if (underwidth>0) underwidth = underwidth-1 ;
}
if (underwidth>topwidth) HERE->width=underwidth ;
else HERE->width=topwidth ;
}   // end GETWIDTH()
/// REMEMBER: BOTH CATHEAD & CATVALUE , .text=CATNAME 


///////////////////////////////////////////////////////////


void COLTREE_PRINTOUT(expnode * HERE) 
{
int d , w , offset1 , w2 , ow ;
string s , unders ;
map<int,expnode*>::iterator p ;
d=2*(HERE->expwhere.size()) ;
w=HERE->width ;

offset1=HERE->offset ;
s=HERE->prnt ;

w2=s.size() ;
ow=(w-w2)/2 ;  // integer divis ;
unders=underscorestring(w);
string_writein(coltreeprnt[d],s,offset1+ow) ;
string_writein(coltreeprnt[d+1],unders,offset1) ;

for(p=HERE->next.begin();p!=HERE->next.end();++p)
  COLTREE_PRINTOUT(p->second) ;
}        //      end COLTREE_PRINTOUT() 

///////////

void executeCOLTREEPRINT()
{
string bs ;
int d , i ;
bs=blankstring(COL_EXP_TREE_TOP->width) ;
d=maximum_depth(COL_EXP_TREE_TOP);   // max of expwhere.size ;
d=2*d ;
coltreeprnt.resize(d+2);
for(i=0;i<coltreeprnt.size();++i) coltreeprnt[i]=bs ;

COLTREE_PRINTOUT(COL_EXP_TREE_TOP) ;
}   //  end executeCOLTREEPRINT() 


//////////////////////////////////////////////////////////



void GETOFFSET(expnode * HERE)
{
expnode * kthptr ;
map<int,expnode*>::iterator q ;
int off1 , sofar , k , cindex ;
off1=HERE->offset ;
sofar=off1 ;
for(q=HERE->next.begin();q!=HERE->next.end();++q)
{ k=q->first ;
  kthptr=q->second ;
  kthptr->offset=sofar ;
  GETOFFSET(kthptr) ;
  sofar += kthptr->width + 1 ;
}
if (HERE->next.empty() && HERE->type!=CATHEAD)
{  LEAFOFFSET[HERE->conwhere][HERE->catwhere] = off1 ;
   // July 2010 addition 
   cindex = colindex_map[HERE->conwhere][HERE->catwhere] ;
   MATRIX_OFFSET[cindex] = off1 ;
}
}     //   end GETOFFSET() 

// before GETOFFSET(COL_EXP_TREE_TOP) ;
// do COL_EXP_TREE_TOP->offset=0 ;


//////////////////////////////////////////

void LEAFCOUNT(expnode * HERE)
{
map<int,expnode*>::iterator q ;
if (HERE->next.empty() && HERE->type!=CATHEAD)
{ leaf_counter_map[HERE->conwhere][HERE->catwhere]=leaf_counter ;
  leaf_counter++ ;
}
for(q=HERE->next.begin();q!=HERE->next.end();++q)
   LEAFCOUNT(q->second) ;
}   // end LEAFCOUNT() 

/// January 2021 , changes to resize matrix0, matrix0_extras, matrix3
void executeLEAFCOUNT() 
{
int j ;
leaf_counter=0 ;
leaf_counter_map.clear() ;
LEAFCOUNT(COL_EXP_TREE_TOP) ;
colindex_counter=leaf_counter ;
colindex_map=leaf_counter_map ;
leaf_counter_map.clear() ;
leaf_counter=0 ;
LEAFCOUNT(ROW_EXP_TREE_TOP);
rowindex_counter=leaf_counter ;
rowindex_map=leaf_counter_map ;
leaf_counter_map.clear() ;
leaf_counter=0 ;


/// January 2021, resize matrix0,matrix0_extras,matrix3 and not matrix,matrix2
matrix0.resize(colindex_counter) ;  
for(j=0;j<matrix0.size();++j) matrix0[j].resize(rowindex_counter) ;
matrix0_extras.resize(colindex_counter) ;   
for(j=0;j<matrix0_extras.size();++j) matrix0_extras[j].resize(rowindex_counter) ;
matrix3.resize(colindex_counter) ;  


MATRIX_RSHIFT.resize(rowindex_counter);
MATRIX_OFFSET.resize(colindex_counter) ;  // added Nov 18 
}  // end executeLEAFCOUNT() 

//////////////////////////////////////////////

// REVIEW THIS FUNCTION !!!!!!!!!!!!!!!

void FIVitem::spectrum_and_insert()
{
list<fi_statrow>::const_iterator p ;
set< vector<int> >::const_iterator q ;
for(p=data2.begin();p!=data2.end();++p)
{ COLSPECT[COLPATHi].insert(p->colcatval) ;
  ROWSPECT[ROWPATHi].insert(p->rowcatval) ;
}
for(q=COLSPECT[COLPATHi].begin();q!=COLSPECT[COLPATHi].end();++q)
  expand_big_tree(COLPATHi,*q,COL_CON_TREE_TOP,COL_EXP_TREE_TOP) ;
for(q=ROWSPECT[ROWPATHi].begin();q!=ROWSPECT[ROWPATHi].end();++q)
  expand_big_tree(ROWPATHi,*q,ROW_CON_TREE_TOP,ROW_EXP_TREE_TOP) ;
}   // end FIVitem::spectrum_and_insert() 


////////////////////////////////

void FIVitem::send_to_matrix()
{
list<fi_statrow>::const_iterator p ;
int cindex , rindex ;
for(p=data2.begin();p!=data2.end();++p)
{ cindex=colindex_map[COLPATHi][p->colcatval] ;
  rindex=rowindex_map[ROWPATHi][p->rowcatval] ;
  matrix[cindex][rindex]=p->statval ;
}
}   ///   end FIVitem::send_to_matrix()

void send_to_matrix2()
{
int j ;
for(j=0;j<matrix.size();++j) 
  matrix2[j] = decimal_align(matrix[j]) ;
/// column of data = fctn( column of data ) 
}    /// end of send_to_matrix2() 

//////////////////////////////////////////////////////////


void SAYWHERE(expnode * HERE)
{
vector<int> cw , EW , CCW ;
map<int,expnode*>::iterator q ;
int k ;
expnode * kth_ptr ;
cw=HERE->catwhere ;
EW=HERE->expwhere ;
CCW=HERE->conwhere ;
if (HERE->type==CATHEAD)
{ for(q=HERE->next.begin();q!=HERE->next.end();++q)
  { k=q->first ;
    kth_ptr=q->second ;
    kth_ptr->conwhere=CCW ;
    kth_ptr->catwhere=cw ;
    kth_ptr->catwhere.push_back(k) ;
    kth_ptr->expwhere=EW ;
    kth_ptr->expwhere.push_back(k) ;
    SAYWHERE(kth_ptr) ;
  }
}
else    // anything but CATHEAD 
{ for(q=HERE->next.begin();q!=HERE->next.end();++q)
  { k=q->first ;
    kth_ptr=q->second ;
    kth_ptr->conwhere=CCW ;
    kth_ptr->conwhere.push_back(k) ;
    kth_ptr->catwhere=cw ;
    kth_ptr->expwhere=EW ;
    kth_ptr->expwhere.push_back(k) ;
    SAYWHERE(kth_ptr) ;
  }
}
}   //   end SAYWHERE() 

////////////////////////////////////////////////


void FILL_TOP()
{
COL_EXP_TREE_TOP = new expnode ;   // repeat for ROW SITU
COL_EXP_TREE_TOP->type = PLACEHOLDER ;
COL_EXP_TREE_TOP->text = "TOPTOP" ;
FILL_UNDER(COL_CON_TREE_TOP,COL_EXP_TREE_TOP) ;

ROW_EXP_TREE_TOP = new expnode ;   // and now for ROW situ 
ROW_EXP_TREE_TOP->type = PLACEHOLDER ;
ROW_EXP_TREE_TOP->text = "TOPTOP" ;
FILL_UNDER(ROW_CON_TREE_TOP,ROW_EXP_TREE_TOP) ;
}   // end FILL_TOP() ;

/////////////////////////////////////////////////

/// q has nothing underneath when called 
void FILL_UNDER(connode * p , expnode * q)
{
int k , j , d ;
vector<int> defaultcatvals ;
connode *p2 ;
expnode *q2, *q3 ;
if (!(q->next.empty())) throw "fillunder1" ;

for(k=0;k<p->next.size();++k)
{ p2=p->next[k] ;
  q->next[k] = new expnode ;
  q2 = q->next[k] ;
  q2->text=p2->text ;
  /// ????
  /// q2->type=node_type_conv(p2->type) ; // huh 
  q2->type=p2->type ;
  if (p2->type==CAT)
  { defaultcatvals = CATEXPANDLIST[tcat_gcat[p2->text]] ;
    q2->type=CATHEAD ;
    for(j=0;j<defaultcatvals.size();++j)
    { d=defaultcatvals[j] ;
      q2->next[d] = new expnode ;
      q3 = q2->next[d] ;
      q3->text=p2->text ;
      q3->type=CATVALUE ;
      q3->catval=d ;
      FILL_UNDER(p2,q3) ;
    }
  }
  else   // p2 = not cat 
  {
    FILL_UNDER(p2,q2) ;
  }

}
}    // end FILL_UNDER()

////////////////////////////////////////////////////////

// July 2010, change function header , function name and order of input args
void expand_big_tree(vector<int> where, vector<int> catlevel,
               connode * whichtree1, expnode * whichtree)
{
connode *p ;
expnode *q, *qq ;
int k , cctr , cval , k1 ;
p=whichtree1 ;
q=whichtree ;
cctr=0 ;
// July 2010 bug fix, confusing k with where[k] 
for(k1=0;k1<where.size();++k1)
{ k = where[k1] ;
  if (p->next.size()-1<k) throw "expand1" ;
  if (q->next.find(k)==q->next.end()) throw "expand2" ;
  p=p->next[k] ;
  q=q->next[k] ;
  if (p->type==CAT)
  { cval=catlevel[cctr] ;
    if (q->next.find(cval)==q->next.end())
    { q->next[cval] = new expnode ;
      qq = q->next[cval] ;
      qq->type=CATVALUE ;
      qq->catval = cval ;
      qq->text = p->text ;
      FILL_UNDER(p,qq) ;
    }
    q=q->next[cval] ;
    cctr++ ;
  }
}
}     //   end expand_big_tree() 


////////////////////////////////////////////////////////



//////////
//July 2010

// for ROW, ( for COL, done during GETWIDTH )
void SETUP_PRNT(expnode * HERE)
{
map<int,expnode*>::iterator q ;
string tcat , gcat , s , s1 ;
int dt ;
if (HERE->type==CATVALUE)
{ 
  tcat=HERE->text ;
  gcat=tcat_gcat[tcat] ;
  dt=datatype_of_gcat[gcat] ;
  /// Feb 2011 , modify 
  /// if (dt==INT) 
  ///    s=IntToStringM(HERE->catval,GCAT_INTWIDTH[gcat]) ;
  /// else if (dt==STR) 
  ///    s=GCAT_FORMAT[gcat][HERE->catval] ;
  s = GCAT_FORMAT[gcat][HERE->catval] ;     /// Feb 2011, this is all u need 
}
else
{ 
  s1=HERE->text ;
  s=s1 ;
  if (RELABEL_FORMAT.find(s1)!=RELABEL_FORMAT.end()) 
     s=RELABEL_FORMAT[s1] ;
}
HERE->prnt = s ;
for(q=HERE->next.begin();q!=HERE->next.end();++q)
   SETUP_PRNT(q->second) ;
}   //   end fctn SETUP_PRNT()



///////////////////////////////////////////////////


/// July 2011 : subtle changes in ROWTREE_PRINTOUT() :
///   do not print a row for void_clev 
///   and MATRIX_RSHIFT for void_clev datapoints needs to point to above CATHEAD row

void ROWTREE_PRINTOUT(expnode * HERE)
{
int d , rindex ;
string blankstr , s ;
map<int,expnode*>::iterator p ;
d = 2*(HERE->expwhere.size()) ;
blankstr = string(d,' ') ;
s = blankstr + HERE->prnt ;
/// July 2011 : do not print a row if it's a void catlev 
if (!(HERE->type==CATVALUE && HERE->catval==void_clev)) 
  rowtreeprnt.push_back(s) ;
if (HERE->next.empty() && HERE->type!=CATHEAD)
{ rindex=rowindex_map[HERE->conwhere][HERE->catwhere] ;
  if (rindex<0) throw "rindexnegative" ;
  if (rindex>=MATRIX_RSHIFT.size()) throw "rindextoobig" ;
  /// July 2011 : this still works for void_clev datapoint 
  /// because last row added was for the above CATHEAD 
  MATRIX_RSHIFT[rindex] = rowtreeprnt.size() - 1 ;
}
for(p=HERE->next.begin();p!=HERE->next.end();++p)
   ROWTREE_PRINTOUT(p->second) ;
}    // end ROWTREE_PRINTOUT() 

/////////////////////////////////////////

void executeROWTREEPRINT()
{
SETUP_PRNT(ROW_EXP_TREE_TOP);
ROWTREE_PRINTOUT(ROW_EXP_TREE_TOP);
}     //   executeROWTREEPRINT() ;






/////////////////////////////////////////

/// Jan 2021, spelling change, matrix2 -> matrix3 
void finish_the_print()
{
ofstream printfileobj ;
vector<string> toprows , mainrows ;
string page ;
int i , WIDTH_CC , WIDTH_RR , c , r ;
vector<string> matrixprnt ;

WIDTH_CC = COL_EXP_TREE_TOP->width ;
WIDTH_RR = 3 ;
for(i=0;i<rowtreeprnt.size();++i) 
  { if (WIDTH_RR<rowtreeprnt[i].size()) WIDTH_RR=rowtreeprnt[i].size() ; }
WIDTH_RR += 2 ;
matrixprnt.resize(rowtreeprnt.size()) ;
for(i=0;i<matrixprnt.size();++i) matrixprnt[i]=string(WIDTH_CC,' ') ;

/// Jan 2021 , spelling change, matrix2 -> matrix3 
for(c=0;c<matrix3.size();++c) 
  for(r=0;r<matrix3[c].size();++r)
    string_writein(matrixprnt[MATRIX_RSHIFT[r]],matrix3[c][r],MATRIX_OFFSET[c]);

toprows.resize(coltreeprnt.size());
for(i=0;i<toprows.size();++i) 
  toprows[i] = string(WIDTH_RR,' ') + coltreeprnt[i] + "\n" ;
mainrows.resize(rowtreeprnt.size());
for(i=0;i<mainrows.size();++i)
  mainrows[i] = rowtreeprnt[i] + string(WIDTH_RR-rowtreeprnt[i].size(),' ') 
                + matrixprnt[i] + "\n" ;


/// page="" ;   Feb 2011 , add title
page = titletext + "\n" ;
for(i=0;i<toprows.size();++i) page += toprows[i] ;
for(i=0;i<mainrows.size();++i) page += mainrows[i] ;
printfileobj.open(tableprintfilename.c_str(),ios::out);
if (!printfileobj) throw "FINISHPRINT1-OPENFAIL" ;
printfileobj << page ;
if (!printfileobj) throw "FINISHPRINT2-WRITEFAIL" ;
printfileobj.close() ;

}   //// end finish_the_print() 


///////////////////////////////


int maximum_depth(expnode * HERE)
{
int d1 , d2 ;
map<int,expnode*>::const_iterator q ;
d1 = HERE->expwhere.size() ;
for(q=HERE->next.begin();q!=HERE->next.end();++q)
{ d2 = maximum_depth(q->second) ;
  if (d1<d2) d1=d2 ;
}
return d1 ;
}     // end function maximum_depth() 






