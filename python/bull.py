# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 

# to do list: sychronize vn/clev

from setup import subpopdenomobject, parsenode, cnode

zdirectory = "/home/robert/tmp/pcall_zdir"
tableprint_communicate_filename="/home/robert/tmp/pcall_zdir/gstscript.txt"


### VDT, as currently figured (in /usr/local/bin) does not send meta-data files
###  to /home/robert/tmp, but to /tmp, so switch from /home/robert/tmp to /tmp
inline_vdt_log_filename = "/tmp/colspecs_communicate.txt"
preview_vdt_dataset_filename = "/tmp/vilnoquickpreview.txt"
# inline_vdt_log_filename = "/home/robert/tmp/colspecs_communicate.txt"
# preview_vdt_dataset_filename = "/home/robert/tmp/vilnoquickpreview.txt"

# ?execute_at_shell() and other stuff in previewCOLSPECSvdt() , vilnopreview ?
# have_vdt_code_executed() with list-of-string


COL_PARSE_TREE = parsenode()
COL_PARSE_TREE.c_r = "c"
ROW_PARSE_TREE = parsenode()
ROW_PARSE_TREE.c_r = "r"

COL_PTRANS_TREE = cnode()
ROW_PTRANS_TREE = cnode()

printto_filename_val = None
def printto_filename_set(value) :
  global printto_filename_val
  printto_filename_val = value 
def printto_filename() :    # get() 
  return printto_filename_val

#######################################

format_filename_val = None
def format_filename_set(value) :
  global format_filename_val
  format_filename_val = value 
def format_filename() :    # get() 
  return format_filename_val

VN_FORMAT = {}

title_text_val = None
def title_text_set(value) :
  global title_text_val
  title_text_val = value 
def title_text() :    # get() 
  return title_text_val





#######################################

LABELS = {}
HAVE_NOTHAVE_DATASETS = set() 
using_shortbinstyle = False
BINARYVNAMES = set()

VARIATORS_VARNAMESUBSTITUTES = ("n","thisrow?","thisrowcat","src")
SUMMSTATOPTIONS = ("mean","sum","median","min","max","std")
HAVE_SPELLINGS = ("have","nothave","have?")
TELE_KEYWORDS = ("all","have","nothave","have?","model",
                 "n","%","mean","sum","median","min","max","std")
SD_VARIATORS = ("thisrowcat","factorunk","toprowlevel")

### Feb 2021 , more global dat structs:
SUMM_STAT_NAMES = ("n","%","mean","sum","median","min","max","std")

### The update of ANY_O_SPELLINGS will need more work
### want to make sure no name clash between placeholder stat spellings
###   and any other type of statistic name spelling
ANY_O_SPELLINGS = set()      ### added Feb 19 2021

##########################################

DENOMglobal1 = subpopdenomobject()
def DENOMglobal_set(value) :
  global DENOMglobal1
  DENOMglobal1 = value
def DENOMglobal() :
  return DENOMglobal1

SUBPOPglobal1 = subpopdenomobject()
def SUBPOPglobal_set(value) :
  global SUBPOPglobal1
  SUBPOPglobal1 = value
def SUBPOPglobal() :
  return SUBPOPglobal1

## Feb 2021, SUBPOPnull() as well as SUBPOPglobal()
SUBPOPnull1 = subpopdenomobject()
def SUBPOPnull() :
  return SUBPOPnull1



# Feb 2021, put (from drive.py) here 
ALLSECNS = []
ALLSECNS_line_ctr=[]
ALLSECNS_type = []
ALLSECNS_borders = []

# November 2020, put EXTERNAL_METAS here, near MODELFOOTS
EXTERNAL_METAS = []
EXTERNAL_STATPROC_TEXTS = []
EXTERNAL_STATPROC_TEXTS2 = {}
EXTERNAL_STATPROC_refnums = []
EXT_M2 = []

# November 2020, MODELFOOTS change from list to dictionary
MODELFOOTS = {}
MODELFOOTS_ONLYIF = {}
MODELFOOTS_SUBPOP = {}
ONLYIFstack = []

# May 2021, you forgot these hodge-podge data structures
hodge_rows = {}
hodge_cols = {}
hodge_fine = {}
hodge_fine_0 = {}
hodge_simple = {}
FineTunes = {}


##########################################

VNAME_CLEVEL = {}
KNOWNCLEVdense = set()
KNOWNCLEVdense_notdifficult = set()
KNOWNCLEVwordlike = set()
KNOWNCLEVdense_VNAME = {}

def CLEV_TO_VNAME(clev) : 
  if clev not in KNOWNCLEVdense_VNAME : return None 
  return KNOWNCLEVdense_VNAME[clev] 
#end def CLEV_TO_VNAME


###########################################

KNOWNDSETS = {}
DIRREFS = {}
declared_categorical = set()
declared_continuous = set() 
AVAILABLEVNAMES = set() 
CATVNAMES = set()
request_convert_ab = {}
request_convert_ba = {}
dd = {}
ORIGDSETS = []

###########################################

PHtask = {}
Ptask1 = {}
DSETMULTIRANGE = {}
feedin = {}
FEEDINvnames = set() 
# suppressDS = None                put this in another file

DSET2_OF_THING = {}
THING_DSET = {}
THING_KEYVARS = {}
KEYVARS_OF_THING = {}
THINGCHOICES = []
THINGDEFNS = set()
DSETS_USED_WITH_THINGS = {}
BOOLLOG_PH = {}

defaultPIrange1 = None
def defaultPIrange_reset(value) :
  global defaultPIrange1
  defaultPIrange1 = value
def defaultPIrange() :
  return defaultPIrange1

###########################################

BOOLLOG = []
RESTRICT_SPELL_LOG = [] 
FACUNK_VNSET_TO_LOGNO = {}
FACUNK_LOGNO_SET = set()

INFLAG_RESTRICTS = {}
inflag_varnames = {}    # which module gets this ?? here i think 

############################################

dsetname_Href = {}
Href_to_fullfilename = {}
Href_to_datref = {}
sorted_tvars = []
H_for_GST = set()


###################################################


setting_thisrowcat = None
def translateTHISROWCAT_reset(value) :
  global setting_thisrowcat
  setting_thisrowcat = value
def translateTHISROWCAT() :
   return setting_thisrowcat


setting_src = None
def translateSRC_reset(value) :
  global setting_src
  setting_src = value
def translateSRC() :
   return setting_src


##################################

setting_thing = None
def thingglobalsetting_reset(value) :
  global setting_thing
  setting_thing = value
def thingglobalsetting() :
  return setting_thing

###################################


#######################################

#########################################


def addbackquotes(s) :
  if len(s)>0 and s[0] not in ("\"","\'") and s[-1] not in ("\"","\'") :
    if s[0].isdigit() or s[0]=='.' : return s 
    return  "\"" + s + "\"" 
  else : 
    return s 
#end def addbackquotes

#################################

PCALL_filename = []
PCALL_mode = []

PCALL = []

PCALLbegin_setting = None
def PCALLbegin_set(val) :
  global PCALLbegin_setting
  PCALLbegin_setting = val
def PCALLbegin() :
  return PCALLbegin_setting


########################################

# June 2011 , add for order datasets introduced 
dset_order_preview = []
dset_order_inlinevdt = []
dset_bad_abba_usage = set()



#### July 2011 
STATISTICS_WHERE = {} 



