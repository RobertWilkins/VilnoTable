
### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


# June 2017
# this is a modified version of previewCOLSPECSasc(), grabbed from known.py
# going to read the colspecs from the first line, and read all the data too.

# unfortunately .rstrip() function removes '\n', but also white space before it
rows = file1.readlines()
rows2=[]
for row in rows :
  s = row
  if (len(s) and s[-1]=='\n') : s = s[:-1]
  rows2.append(s)






def previewCOLSPECSasc22(filename) :
  rows = []
  file1 = open(filename,'r')
  specline = file1.readline()
  
  file1.close()
  
  delimiter="|"
  strnull=""
  met1 = specline.split(",")
  vnlist = met1[1].split()
  dtlist1 = met1[2].split()    # formatted as : int str flo 
  slen1 = met1[3].split()
  slen2 = [] 
  for x in slen1 : slen2.append( int(x) ) 
  
  if len(met1)>=5 :
    delim1 = met1[4].split()
    if len(delim1)>=2 and delim1[0]=="delimiter" :
      delimiter = delim1[1]
      if delimiter=="c" : delimiter=","
  
  if len(met1)>=6 :
    snull1 = met1[5].split()
    if len(snull1)>=2 and snull1[0]=="strnullflag" :
      strnull = snull1[1] 
  
  using vnlist dtlist1 slen2     
#end def previewCOLSPECSasc






SO WHAT YOU NEED IS
vnlist
dtlist1 
slen2




