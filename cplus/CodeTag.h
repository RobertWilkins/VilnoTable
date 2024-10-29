
/// Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
///                  in 1984, in Massachusetts, USA 



class CodeTag
{
public:
CodeTag() ;
int type , wraptype , level ;
long tokid1 , tokid2 ;
string specify ;
};

CodeTag::CodeTag() { type=wraptype=level=0; tokid1=tokid2=-1; }

