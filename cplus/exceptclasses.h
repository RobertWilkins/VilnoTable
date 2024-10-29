// Copyright 2002-2006, Robert Wilkins (class 1984, Newton North HS, MA, USA)

/// Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
///                  in 1984, in Massachusetts, USA 

// DriveErr ErrSysBug BUG rsUnex Unex hcdUnex inswUnex fbrUnex insrUnex

class DriveErr
{ public:
  DriveErr(string s) : errorcode(s) { }
  string errorcode ;
};    // end class DriveErr 



class BUG
{ public:
  BUG(string s) : errorcode(s) { }
  string errorcode ;
};    // end class BUG 

class ErrSysBug
{ public:
  ErrSysBug(string s) : errorcode(s) { }
  string errorcode ;
};    // end class ErrSysBug 


class Unex
{ public:

  Unex(string s, string s1="", string s2="", string s3="", string s4="") : 
      errorcode(s) , word1(s1) , word2(s2) , word3(s3) , word4(s4) 
      { idrp.first=idrp.second=-1 ; }

  Unex(string s, pair<long,long> info) :
      errorcode(s) , idrp(info)  { } 

  string errorcode ;
  string word1 ;
  string word2 ;
  string word3 ;
  string word4 ;
  pair<long,long> idrp ;
};     // end class Unex 


/////////////////////////////

class rsUnex
{ public:

  rsUnex(string s, string s1="", string s2="", string s3="", string s4="") : 
      errorcode(s) , word1(s1) , word2(s2) , word3(s3) , word4(s4) { }

  string errorcode ;
  string word1 ;
  string word2 ;
  string word3 ;
  string word4 ;
};     // end class rsUnex 




class fbrUnex
{ public:

  fbrUnex(string s, string s1="", string s2="", string s3="", string s4="") : 
      errorcode(s) , word1(s1) , word2(s2) , word3(s3) , word4(s4) { }

  string errorcode ;
  string word1 ;
  string word2 ;
  string word3 ;
  string word4 ;
};     // end class fbrUnex 



class inswUnex
{ public:

  inswUnex(string s, string s1="", string s2="", string s3="", string s4="") : 
      errorcode(s) , word1(s1) , word2(s2) , word3(s3) , word4(s4) { }

  string errorcode ;
  string word1 ;
  string word2 ;
  string word3 ;
  string word4 ;
};     // end class inswUnex 



class hcdUnex
{ public:

  hcdUnex(string s, string s1="", string s2="", string s3="", string s4="") : 
      errorcode(s) , word1(s1) , word2(s2) , word3(s3) , word4(s4) { }

  string errorcode ;
  string word1 ;
  string word2 ;
  string word3 ;
  string word4 ;
};     // end class hcdUnex 




class fctnlibUnex
{ public:

  fctnlibUnex(string s, string s1="", string s2="", string s3="", string s4="") : 
      errorcode(s) , word1(s1) , word2(s2) , word3(s3) , word4(s4) { }

  string errorcode ;
  string word1 ;
  string word2 ;
  string word3 ;
  string word4 ;
};     // end class fctnlibUnex 



class insrUnex
{ public:

  insrUnex(string s, string s1="", string s2="", string s3="", string s4="") : 
      errorcode(s) , word1(s1) , word2(s2) , word3(s3) , word4(s4) { }

  string errorcode ;
  string word1 ;
  string word2 ;
  string word3 ;
  string word4 ;
};     // end class insrUnex 





