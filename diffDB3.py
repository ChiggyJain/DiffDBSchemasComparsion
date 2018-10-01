#!/usr/bin/python3


'''

Author Name : Chirag D Jain
Created On : 2018-06-01
Currently Contributing at : DigitalEdu IT Solutions Pvt Ltd
Domain : Education Sector
Country : India
City : Pune
 
'''


### Section abt to import different types of python inbuilt utilities ###

import os
import sys
import pymysql
import re
import urllib
import datetime 
import glob
import shutil
import subprocess
import threading
import traceback
import getpass
import copy
import json
import platform
import string
from subprocess import Popen, PIPE


### Section abt to declare script global variables ###

scriptExeStartDatetime = datetime.datetime.now();
dateTime = str(datetime.datetime.now());
timeStampStr = dateTime.replace(" ", "").replace("-", "").replace(":", "").split(".")[0];


### Section abt to declare variable for accepting input arguments ###

inputArgsDataObj = {};

### setup variables for source server ###

inputArgsDataObj['srcDbSvrHostName'] = '';
inputArgsDataObj['srcDbSvrPortNo'] = '';
inputArgsDataObj['srcDbSvrUserName'] = '';
inputArgsDataObj['srcDbSvrPwd'] = '';
inputArgsDataObj['srcDbSvrDbType'] = '';
inputArgsDataObj['srcDbSvrSetupInfoSchemaNameArr'] = [];
inputArgsDataObj['srcDbSvrDbName'] = '';

### setup variables for destination server ###

inputArgsDataObj['dstDbSvrHostName'] = '';
inputArgsDataObj['dstDbSvrPortNo'] = '';
inputArgsDataObj['dstDbSvrUserName'] = '';
inputArgsDataObj['dstDbSvrPwd'] = '';
inputArgsDataObj['dstDbSvrDbType'] = '';
inputArgsDataObj['dstDbSvrSetupInfoSchemaNameArr'] = [];
inputArgsDataObj['dstDbSvrDbNames'] = '';


### comparsion purpose variables btwn source and destination server ###

inputArgsDataObj['isSrcDbSvrDbNameExist'] = 'N';
inputArgsDataObj['isDstDbSvrDbNameExist'] = 'N';
inputArgsDataObj['cmpCtgryDataObj'] = {
      'cmpCtgryNo' : '0', 
      'includeMethodsArr' : [],
      'excludeMethodsArr' : [],
      'findStr' : '',
      'dbTblNamesStr' : "",
      'dbTblColNamesStr' : "",
      'dbTblIndxNamesStr' : "",
      'dbTblFKNamesStr' : "",
      'dbTblTgrNamesStr' : "",
      'dbRoutineNamesStr' : "",
      'dbViewNamesStr' : "",
      'customSearchCondStr' : "",
      'customSearchCondStrForCmptCtgryNoArr' :  []
};

inputArgsDataObj['applyChangesOn'] = "DstSvr";
inputArgsDataObj['isMakeExactDbSchemasCopy'] = "N";
inputArgsDataObj['isExecuteChanges'] = 'N';
inputArgsDataObj['isIncludeSysGlblVariableComparsion'] = 'N';
inputArgsDataObj['isIncludeTblAttrOptnComparsion'] = 'Y';
inputArgsDataObj['isRearrangeTblColPos'] = 'Y';
inputArgsDataObj['isIncludeTblColDataTypeComparsion'] = 'Y';
inputArgsDataObj['isIncludeTblColDefComparsion'] = 'Y';
inputArgsDataObj['isIncludeTblForeignKeysConstraintsComparsion'] = 'Y';
inputArgsDataObj['isIncludeTblColIndexesComparsion'] = 'Y';
inputArgsDataObj['isIncludeTblTrgsDefComparsion'] = 'Y';
inputArgsDataObj['isIncludeDbRoutinesDefComparsion'] = 'Y';
inputArgsDataObj['isIncludeDbViewsDefComparsion'] = 'Y';
inputArgsDataObj['dstDbSvrConTestedOnDbNameArr'] = [];
inputArgsDataObj['uniqInfoSchemaNameArrBtwnSrcAndDstDbSvr'] = [];
inputArgsDataObj['canUseSrcDbSvrDbNamesFurtherComparsionAgainstDstDbSvr'] = 'Y';
inputArgsDataObj['includeSchemasNameBasedOnIndentifierCharsRegexStr'] = "^[a-zA-Z0-9$_]";
inputArgsDataObj['ntSysSchemasNamesStr'] = "'INFORMATION_SCHEMA','mysql','performance_schema','phpmyadmin'";


### Section abt to declare variable for storing db server config between SOURCE and DESTINATION server ###

srcDbSvrConfigDataObj = {};
dstDbSvrConfigDataObj = {};

### Section abt to declare variable for storing infoSchemas data between SOURCE and DESTINATION server all Dbs ###

srcDbSvrInfoSchemasDataObj = {
   'sysGlobalVariablesDataObj' : {},
   'schemasDataObj' : {}
};
dstDbSvrInfoSchemasDataObj = {
   'sysGlobalVariablesDataObj' : {},
   'schemasDataObj' : {}
};


### operating system level info ###

curWrkngDirPath = os.getcwd() + "/" ;
   

### to create directory info for storing all sql files btwn SOURCE and DESTINATION server all Dbs ###

diffDBLogDirnameStr = 'diffDB' + timeStampStr;
diffDBLogDirnameWithPathStr = curWrkngDirPath + diffDBLogDirnameStr;
toStoreTempSqlFileDirPath = curWrkngDirPath;
srcDbSvrFolderName = 'SOURCE_SERVER';
dstDbSvrFolderName = 'DESTINATION_SERVER';
runtimeScriptErrFolderName = "RuntimeScriptError";
toStoreDiffDbChangesFoldernameDataObj = {};
toStoreDiffDbChangesFoldernameDataObj['executeAllChangesFoldername'] = "executeAllChanges";
toStoreDiffDbChangesFoldernameDataObj['addingNewChangesFoldername'] = "addingNewChanges";
toStoreDiffDbChangesFoldernameDataObj['updationChangesFoldername'] = "updationChanges";
toStoreDiffDbChangesFoldernameDataObj['droppedChangesFoldername'] = "droppedChanges";
toStoreDiffDbChangesFoldernameDataObj['importantRestrictionsFoldername'] = "importantRestrictions";
toStoreDiffDbChangesFoldernameDataObj['errFoldername'] = "error";


### stored diff DB changes sql query files btwn SOURCE and DESTINATION server ###

toStoreSqlQryFilesLogAbtSrcSvrDataObj = {
   'sysGlobalVariablesDataObj' : {},
   'schemasDataObj' : {}  
};
toStoreSqlQryFilesLogAbtDstSvrDataObj = {
   'sysGlobalVariablesDataObj' : {},
   'schemasDataObj' : {} 
};


### variable declare for collecting diff db comparsion summary report data ###

diffDBComparsionSummaryDataObj = {

    'DstSvr' : {
        'diffFoundOnDBSDataObj' : {},
        'diffNtFoundOnDBSDataObj' : {},
        'isChangesExecuted' : 'N'
    },
 
    'SrcSvr' : {
        'diffFoundOnDBSDataObj' : {},
        'diffNtFoundOnDBSDataObj' : {},
        'isChangesExecuted' : 'N'
    },

    'executionStartDateTime' : scriptExeStartDatetime,
    'executionEndDateTime' : scriptExeStartDatetime,
    'executionTotalTime' : scriptExeStartDatetime

};


### queries related to extract setup data about info schemas wise ###

infoSchemasWiseQryDataObj = {

    "allTblsAttrOptns" : {
         "selectToWhereStmt" : """SELECT
                        t.TABLE_SCHEMA dbName, t.TABLE_NAME tblName, t.ENGINE tblEngine,
                        t.ROW_FORMAT tblRowFormat, t.TABLE_COLLATION tblCollation, 
                        t.TABLE_COMMENT tblCmnt, t.CREATE_OPTIONS tblCreateOptn, 
                        COALESCE(t.CHECKSUM, '') tblCheckSum, CAST(COALESCE(t.TABLE_ROWS, 0) AS UNSIGNED) tblRows
                        FROM INFORMATION_SCHEMA.TABLES t
                        WHERE 1
                        AND t.TABLE_TYPE NOT IN ('VIEW')""", 
         "ntSysSchemasNamesWhereCondStr" : """ AND t.TABLE_SCHEMA NOT IN ({ntSysSchemasNamesStr})""",
         "sysSchemaNamesRegexExpWhereCondStr" : """ AND (t.TABLE_SCHEMA REGEXP {sysSchemaNamesRegexExpStr})>0
                            AND (t.TABLE_NAME REGEXP {sysSchemaNamesRegexExpStr})>0""",
         "dbBasedTypeWhereCondStr" : """ AND t.TABLE_SCHEMA LIKE '%\_{dbBasedTypeStr}%'""",
         "ntDbNamesWhereCondStr" : """ AND t.TABLE_SCHEMA NOT IN ({ntDbNamesStr})""",
         "dbNamesWhereCondStr" : """ AND t.TABLE_SCHEMA IN ({dbNamesStr})""",
         "dbTblNamesWhereCondStr" : """ AND t.TABLE_NAME IN ({dbTblNamesStr})""",
         "dbTblColNamesWhereCondStr" : "",
         "dbTblIndxNamesWhereCondStr" : "",
         "dbTblFKNamesWhereCondStr" : "",   
         "dbTblTgrNamesWhereCondStr" : "",
         "dbRoutineNamesWhereCondStr" : "",
         "dbViewNamesWhereCondStr" : "",
         "groupByStmt" : "",
         "orderByStmt" : """ ORDER BY t.TABLE_SCHEMA ASC, t.TABLE_NAME ASC""",    
     },

     "allTbls" : {
         "selectToWhereStmt" : """SELECT
                        c.TABLE_SCHEMA dbName, c.TABLE_NAME tblName, 
                        c.COLUMN_NAME colName, c.DATA_TYPE dataType, 
                        c.COLUMN_TYPE colType, COALESCE(c.COLUMN_DEFAULT, 'ONLYNULL') colDefault, 
                        (CASE WHEN c.EXTRA='' THEN 'ONLYBLANK' ELSE c.EXTRA END) colExtra,
                        c.IS_NULLABLE isNull, c.COLUMN_COMMENT colCmnt, 
                        c.COLUMN_KEY colKey, c.ORDINAL_POSITION colPosition
                        FROM INFORMATION_SCHEMA.COLUMNS c
                        WHERE 1""", 
         "ntSysSchemasNamesWhereCondStr" : """ AND c.TABLE_SCHEMA NOT IN ({ntSysSchemasNamesStr})""",
         "sysSchemaNamesRegexExpWhereCondStr" : """ AND (c.TABLE_SCHEMA REGEXP {sysSchemaNamesRegexExpStr})>0 AND (c.TABLE_NAME REGEXP {sysSchemaNamesRegexExpStr})>0 AND (c.COLUMN_NAME REGEXP {sysSchemaNamesRegexExpStr})>0""",
         "dbBasedTypeWhereCondStr" : """ AND c.TABLE_SCHEMA LIKE '%\_{dbBasedTypeStr}%'""",
         "ntDbNamesWhereCondStr" : """ AND c.TABLE_SCHEMA NOT IN ({ntDbNamesStr})""",
         "dbNamesWhereCondStr" : """ AND c.TABLE_SCHEMA IN ({dbNamesStr})""",
         "dbTblNamesWhereCondStr" : """ AND c.TABLE_NAME IN ({dbTblNamesStr})""",
         "dbTblColNamesWhereCondStr" : """ AND c.COLUMN_NAME IN ({dbTblColNamesStr})""",
         "dbTblIndxNamesWhereCondStr" : "",
         "dbTblFKNamesWhereCondStr" : "",   
         "dbTblTgrNamesWhereCondStr" : "",
         "dbRoutineNamesWhereCondStr" : "",
         "dbViewNamesWhereCondStr" : "",
         "groupByStmt" : "",
         "orderByStmt" : """ ORDER BY c.TABLE_SCHEMA ASC, c.TABLE_NAME ASC, c.ORDINAL_POSITION ASC""",    
     },

     "indexes" : {
         "selectToWhereStmt" : """SELECT
                        s.TABLE_SCHEMA dbName, s.TABLE_NAME tblName,
                        s.INDEX_SCHEMA indxDbName, s.INDEX_NAME indxName, s.NON_UNIQUE,
                        s.SEQ_IN_INDEX, s.COLUMN_NAME,
                        s.INDEX_TYPE indxType, COALESCE(s.COMMENT, '') indxCmnt, COALESCE(s.SUB_PART, '') indxSubpart
                        FROM INFORMATION_SCHEMA.STATISTICS s
                        WHERE 1""", 
         "ntSysSchemasNamesWhereCondStr" : """ AND s.TABLE_SCHEMA NOT IN ({ntSysSchemasNamesStr})""",
         "sysSchemaNamesRegexExpWhereCondStr" : """ AND (s.TABLE_SCHEMA REGEXP {sysSchemaNamesRegexExpStr})>0 AND (s.TABLE_NAME REGEXP {sysSchemaNamesRegexExpStr})>0 AND (s.INDEX_SCHEMA REGEXP {sysSchemaNamesRegexExpStr})>0
                            AND (s.COLUMN_NAME REGEXP {sysSchemaNamesRegexExpStr})>0""",
         "dbBasedTypeWhereCondStr" : """ AND s.TABLE_SCHEMA LIKE '%\_{dbBasedTypeStr}%'""",
         "ntDbNamesWhereCondStr" : """ AND s.TABLE_SCHEMA NOT IN ({ntDbNamesStr})""",
         "dbNamesWhereCondStr" : """ AND s.TABLE_SCHEMA IN ({dbNamesStr})""",
         "dbTblNamesWhereCondStr" : """ AND s.TABLE_NAME IN ({dbTblNamesStr})""",
         "dbTblColNamesWhereCondStr" : "",
         "dbTblIndxNamesWhereCondStr" : """ AND s.INDEX_NAME IN ({dbTblIndxNamesStr})""",
         "dbTblFKNamesWhereCondStr" : "",   
         "dbTblTgrNamesWhereCondStr" : "",
         "dbRoutineNamesWhereCondStr" : "",
         "dbViewNamesWhereCondStr" : "",
         "groupByStmt" : "",
         "orderByStmt" : """ ORDER BY s.NON_UNIQUE DESC""",    
     },

    "fkConstraints" : {
         "selectToWhereStmt" : """SELECT
                        kcs.REFERENCED_TABLE_SCHEMA NFKDbName, kcs.REFERENCED_TABLE_NAME NFKTblName, 
                        kcs.REFERENCED_COLUMN_NAME NFKColName,
                        kcs.TABLE_SCHEMA fkDbName, kcs.TABLE_NAME fkTblName,
                        kcs.CONSTRAINT_NAME FKName, kcs.COLUMN_NAME fkColName, 
                        kcs.ORDINAL_POSITION fkColPosition
                        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcs
                        WHERE 1
                        AND kcs.REFERENCED_TABLE_SCHEMA IS NOT NULL
                        AND kcs.REFERENCED_TABLE_NAME IS NOT NULL
                        AND kcs.REFERENCED_COLUMN_NAME IS NOT NULL""", 
         "ntSysSchemasNamesWhereCondStr" : """ AND kcs.REFERENCED_TABLE_SCHEMA NOT IN ({ntSysSchemasNamesStr})
                            AND kcs.TABLE_SCHEMA NOT IN ({ntSysSchemasNamesStr})""",
         "sysSchemaNamesRegexExpWhereCondStr" : """ AND (kcs.REFERENCED_TABLE_SCHEMA REGEXP {sysSchemaNamesRegexExpStr})>0
                            AND (kcs.REFERENCED_TABLE_NAME REGEXP {sysSchemaNamesRegexExpStr})>0
                            AND (kcs.REFERENCED_COLUMN_NAME REGEXP {sysSchemaNamesRegexExpStr})>0
                            AND (kcs.TABLE_SCHEMA REGEXP {sysSchemaNamesRegexExpStr})>0
                            AND (kcs.TABLE_NAME REGEXP {sysSchemaNamesRegexExpStr})>0
                            AND (kcs.COLUMN_NAME REGEXP {sysSchemaNamesRegexExpStr})>0""",
         "dbBasedTypeWhereCondStr" : """ AND kcs.TABLE_SCHEMA LIKE '%\_{dbBasedTypeStr}%'""",
         "ntDbNamesWhereCondStr" : """ AND kcs.TABLE_SCHEMA NOT IN ({ntDbNamesStr})""",
         "dbNamesWhereCondStr" : """ AND kcs.TABLE_SCHEMA IN ({dbNamesStr})""",
         "dbTblNamesWhereCondStr" : """ AND kcs.TABLE_NAME IN ({dbTblNamesStr})""",
         "dbTblColNamesWhereCondStr" : "",
         "dbTblIndxNamesWhereCondStr" : "",
         "dbTblFKNamesWhereCondStr" : """ AND kcs.CONSTRAINT_NAME IN ({dbTblFKNamesStr})""",   
         "dbTblTgrNamesWhereCondStr" : "",
         "dbRoutineNamesWhereCondStr" : "",
         "dbViewNamesWhereCondStr" : "",
         "groupByStmt" : "",
         "orderByStmt" : "",    
     },

     "fkColsRulesConstraints" : {
         "selectToWhereStmt" : """SELECT
                        rc.REFERENCED_TABLE_NAME NFKTblName,
                        rc.CONSTRAINT_SCHEMA fkDbName, rc.TABLE_NAME fkTblName, rc.CONSTRAINT_NAME FKName,
                        rc.MATCH_OPTION matchOption, rc.UPDATE_RULE updateRule, rc.DELETE_RULE deleteRule
                        FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc
                        WHERE 1""", 
         "ntSysSchemasNamesWhereCondStr" : """ AND rc.CONSTRAINT_SCHEMA NOT IN ({ntSysSchemasNamesStr})""",
         "sysSchemaNamesRegexExpWhereCondStr" : """ AND (rc.REFERENCED_TABLE_NAME REGEXP {sysSchemaNamesRegexExpStr})>0 AND (rc.CONSTRAINT_SCHEMA REGEXP {sysSchemaNamesRegexExpStr})>0 AND (rc.TABLE_NAME REGEXP {sysSchemaNamesRegexExpStr})>0""",
         "dbBasedTypeWhereCondStr" : "",
         "ntDbNamesWhereCondStr" : "",
         "dbNamesWhereCondStr" : """ AND rc.CONSTRAINT_SCHEMA IN ({dbNamesStr})""",
         "dbTblNamesWhereCondStr" : """ AND rc.TABLE_NAME IN ({dbTblNamesStr})""",
         "dbTblColNamesWhereCondStr" : "",
         "dbTblIndxNamesWhereCondStr" : "",
         "dbTblFKNamesWhereCondStr" : """ AND rc.CONSTRAINT_NAME IN ({dbTblFKNamesStr})""",   
         "dbTblTgrNamesWhereCondStr" : "",
         "dbRoutineNamesWhereCondStr" : "",
         "dbViewNamesWhereCondStr" : "",
         "groupByStmt" : "",
         "orderByStmt" : "",    
     },

     "triggers" : {
         "selectToWhereStmt" : """SELECT
                        t.TRIGGER_SCHEMA dbName, t.EVENT_OBJECT_TABLE tblName, 
                        t.TRIGGER_NAME triggerName, t.ACTION_TIMING tActionTime,
                        t.EVENT_MANIPULATION tEvent, t.ACTION_STATEMENT tStmt, 
                        t.DEFINER tDefiner, t.ACTION_STATEMENT tOrgStmt
                        FROM INFORMATION_SCHEMA.TRIGGERS t
                        WHERE 1""", 
         "ntSysSchemasNamesWhereCondStr" : """ AND t.TRIGGER_SCHEMA NOT IN ({ntSysSchemasNamesStr})""",
         "sysSchemaNamesRegexExpWhereCondStr" : """ AND (t.TRIGGER_SCHEMA REGEXP {sysSchemaNamesRegexExpStr})>0
                            AND (t.EVENT_OBJECT_TABLE REGEXP {sysSchemaNamesRegexExpStr})>0""",
         "dbBasedTypeWhereCondStr" : """ AND t.TRIGGER_SCHEMA LIKE '%\_{dbBasedTypeStr}%'""",
         "ntDbNamesWhereCondStr" : """ AND t.TRIGGER_SCHEMA NOT IN ({ntDbNamesStr})""",
         "dbNamesWhereCondStr" : """ AND t.TRIGGER_SCHEMA IN ({dbNamesStr})""",
         "dbTblNamesWhereCondStr" : """ AND t.EVENT_OBJECT_TABLE IN ({dbTblNamesStr})""",
         "dbTblColNamesWhereCondStr" : "",
         "dbTblIndxNamesWhereCondStr" : "",
         "dbTblFKNamesWhereCondStr" : "",   
         "dbTblTgrNamesWhereCondStr" : """ AND t.TRIGGER_NAME IN ({dbTblTgrNamesStr})""",
         "dbRoutineNamesWhereCondStr" : "",
         "dbViewNamesWhereCondStr" : "",
         "groupByStmt" : "",
         "orderByStmt" : "",    
     },

     "routines" : {
         "selectToWhereStmt" : """SELECT
                        r.ROUTINE_SCHEMA dbName, r.ROUTINE_TYPE rType, r.ROUTINE_NAME rName,
                        r.ROUTINE_DEFINITION rDetails, r.IS_DETERMINISTIC rIsDeterministic, r.DEFINER rDefiner, 
                        r.SQL_MODE rSqlMode, r.SECURITY_TYPE rSecurityType, r.ROUTINE_COMMENT rCmnt
                        FROM INFORMATION_SCHEMA.ROUTINES r
                        WHERE 1""", 
         "ntSysSchemasNamesWhereCondStr" : """ AND r.ROUTINE_SCHEMA NOT IN ({ntSysSchemasNamesStr})""",
         "sysSchemaNamesRegexExpWhereCondStr" : """ AND (r.ROUTINE_SCHEMA REGEXP {sysSchemaNamesRegexExpStr})>0""",
         "dbBasedTypeWhereCondStr" : """ AND r.ROUTINE_SCHEMA LIKE '%\_{dbBasedTypeStr}%'""",
         "ntDbNamesWhereCondStr" : """ AND r.ROUTINE_SCHEMA NOT IN ({ntDbNamesStr})""",
         "dbNamesWhereCondStr" : """ AND r.ROUTINE_SCHEMA IN ({dbNamesStr})""",
         "dbTblNamesWhereCondStr" : """ AND r.ROUTINE_NAME IN ({dbTblNamesStr})""",
         "dbTblColNamesWhereCondStr" : "",
         "dbTblIndxNamesWhereCondStr" : "",
         "dbTblFKNamesWhereCondStr" : "",   
         "dbTblTgrNamesWhereCondStr" : "",
         "dbRoutineNamesWhereCondStr" : """ AND r.ROUTINE_NAME IN ({dbRoutineNamesStr})""",
         "dbViewNamesWhereCondStr" : "",
         "groupByStmt" : "",
         "orderByStmt" : """ ORDER BY r.ROUTINE_TYPE""",    
     },

     "views" : {
         "selectToWhereStmt" : """SELECT
                        v.TABLE_SCHEMA dbName, v.TABLE_NAME tblName, v.VIEW_DEFINITION vStmt, v.IS_UPDATABLE vIsUpdatable, 
                        v.DEFINER vDefiner, v.SECURITY_TYPE vSecurityType, v.VIEW_DEFINITION vOrgStmt
                        FROM INFORMATION_SCHEMA.VIEWS v
                        WHERE 1""", 
         "ntSysSchemasNamesWhereCondStr" : """ AND v.TABLE_SCHEMA NOT IN ({ntSysSchemasNamesStr})""",
         "sysSchemaNamesRegexExpWhereCondStr" : """ AND (v.TABLE_SCHEMA REGEXP {sysSchemaNamesRegexExpStr})>0 AND (v.TABLE_NAME REGEXP {sysSchemaNamesRegexExpStr})>0""",
         "dbBasedTypeWhereCondStr" : """ AND v.TABLE_SCHEMA LIKE '%\_{dbBasedTypeStr}%'""",
         "ntDbNamesWhereCondStr" : """ AND v.TABLE_SCHEMA NOT IN ({ntDbNamesStr})""",
         "dbNamesWhereCondStr" : """ AND v.TABLE_SCHEMA IN ({dbNamesStr})""",
         "dbTblNamesWhereCondStr" : "",
         "dbTblColNamesWhereCondStr" : "",
         "dbTblIndxNamesWhereCondStr" : "",
         "dbTblFKNamesWhereCondStr" : "",   
         "dbTblTgrNamesWhereCondStr" : "",
         "dbRoutineNamesWhereCondStr" : "",
         "dbViewNamesWhereCondStr" : """ AND v.TABLE_NAME IN ({dbViewNamesStr})""",
         "groupByStmt" : "",
         "orderByStmt" : "",    
     }

};


### replace file path separator based on os platform ###

def replaceFilePathSeparatorViaOsPlatform(filePathStr):

    if filePathStr != "" :
       osPlatform = platform.system();
       if (osPlatform).lower() == "linux" or (osPlatform).lower() == "ubuntu" : 
          filePathStr = filePathStr.replace("//", "/");
       if (osPlatform).lower() == "windows" : 
          filePathStr = '\\\\'.join("{0}".format(eachStr) for eachStr in filePathStr.split('\\'));
          filePathStr = '\\\\'.join("{0}".format(eachStr) for eachStr in filePathStr.split('/'));

    return filePathStr;
 

### get db name installed path based on os platform ###

def getDBInstalledPathViaOsPlatform(dbInstalledName):

    dbInstalledPath = "mysql";

    if dbInstalledName == "mysql" :
       osPlatform = platform.system();

       if (osPlatform).lower() == "linux" or (osPlatform).lower() == "ubuntu" : 
          dbInstalledPath = "mysql";

       if (osPlatform).lower() == "windows" : 
          # dbInstalledPath = "C:\\xampp\\mysql\\bin\\mysql";
          lettersArr = list(string.ascii_lowercase);
          cmpDriveArr = ["C"];
          cmpDriveArr.extend(lettersArr);
          isPathFound = 'N';
          for driveName in cmpDriveArr :
              if isPathFound == 'Y' :
                 break;  
              if isPathFound == 'N' :
                 cmdArr = ["cmd", "/"+driveName, "dir my.ini /S"];
                 proc = subprocess.Popen(cmdArr, cwd=driveName+":/", stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True);
                 otStr, errStr = proc.communicate();
                 otArr = otStr.split("\n");
                 for otStr in otArr :
                     if re.search("bin", otStr, re.M | re.I) :
                        otStrReplacedBackslashStr = otStr.replace("\\", "");
                        if re.search("mysqlbin", otStrReplacedBackslashStr, re.M | re.I) :
                           driveName = driveName+":";
                           drivePathArr = (otStr[otStr.find(driveName):]).split(os.sep);
                           drivePathArr[len(drivePathArr)-1] = "bin";
                           drivePathArr.append("mysql");
                           dbInstalledPath = os.sep.join("{0}".format(splittedStr) for splittedStr in drivePathArr);
                           isPathFound = 'Y';
                           break;
                         

    
    return dbInstalledPath;


### convert content string into bytes to write into file obj ###

def getConvertedStrIntoBytesToWriteIntoFileObj(contentStr, fileMode='r', charSet='UTF-8'):

    pythonVs = sys.version_info[0];
    if (pythonVs)<3 :
       contentStr = contentStr;
    else:
        if fileMode == "ab+" : 
           contentStr = bytes(contentStr, charSet);
        else:
            contentStr = contentStr;

    return contentStr;
 

### remove created sql temporary file from system ###

def removeTemporaryCreatedSqlFiles():

    global toStoreTempSqlFileDirPath;
    toStoreTempSqlFileDirPath = replaceFilePathSeparatorViaOsPlatform(toStoreTempSqlFileDirPath);
   
    filenameWithPathStr = toStoreTempSqlFileDirPath + "diffDbTemp.sql";
    if os.path.exists(filenameWithPathStr) == True:
       os.remove(filenameWithPathStr);


### create run time script error directory/folder ###

def createRuntimeScriptErrDirectory():

    global diffDBLogDirnameWithPathStr;
    global runtimeScriptErrFolderName;   
    isDirCreated = 'N';

    try:

        ### section related to base directory name ###

        diffDBLogDirnameWithPathStr = replaceFilePathSeparatorViaOsPlatform(diffDBLogDirnameWithPathStr);
        runtimeScriptErrFolderNameWithPathStr = diffDBLogDirnameWithPathStr+"/"+runtimeScriptErrFolderName;
        runtimeScriptErrFolderNameWithPathStr = replaceFilePathSeparatorViaOsPlatform(runtimeScriptErrFolderNameWithPathStr);
  
        if os.path.exists(diffDBLogDirnameWithPathStr) == False:
           os.mkdir(diffDBLogDirnameWithPathStr);
           os.chmod(diffDBLogDirnameWithPathStr, 0o777);
           os.mkdir(runtimeScriptErrFolderNameWithPathStr);
           os.chmod(runtimeScriptErrFolderNameWithPathStr, 0o777);
           isDirCreated = "Y";
        else:
             os.chmod(diffDBLogDirnameWithPathStr, 0o777);
             if os.path.exists(runtimeScriptErrFolderNameWithPathStr) == False:
                os.mkdir(runtimeScriptErrFolderNameWithPathStr);
                os.chmod(runtimeScriptErrFolderNameWithPathStr, 0o777);  
             isDirCreated = "Y";


    except Exception as e:
           handleProcsngAbtErrException("Y");
 
    return isDirCreated;


### handle processing to display msg on screen ###

def displayMsg(labelStr, valueStr):

    try:

       displayMsgStr = "";

       if labelStr!="" :
          displayMsgStr+=  labelStr;
       if valueStr!="" :
          displayMsgStr+=  valueStr;   

       print (displayMsgStr);

    except Exception as e:
           print ("Exception : ", e);


### handle processing about error exception ###

def handleProcsngAbtErrException(isDispScriptErrMsg):
   
    global diffDBLogDirnameWithPathStr;
    global runtimeScriptErrFolderName;
    msgStr = "";
  
    runtimeScriptErrFilename = "RuntimeScriptErrorOccuredMsg";
    errFilenameWithPath = diffDBLogDirnameWithPathStr+"/"+runtimeScriptErrFolderName+"/"+runtimeScriptErrFilename;
    errFilenameWithPath = replaceFilePathSeparatorViaOsPlatform(errFilenameWithPath);
  
    exType, exObj, exTb = sys.exc_info();
    errFileName = str(os.path.split(exTb.tb_frame.f_code.co_filename)[1]);
    errInFunctionName = str(sys._getframe().f_code.co_name);
    errLineNoInFile = str(exTb.tb_lineno);

    traceBackList = traceback.format_stack();
    traceBackList = traceBackList[:-2]
    traceBackList.extend(traceback.format_tb(sys.exc_info()[2]))
    traceBackList.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
    traceBackStr = "".join(traceBackList);
    traceBackStr+= traceBackStr[:-1];


    msgStr = "\n"; 
    msgStr+= "Error Details:";
    msgStr+= "\n"; 
    msgStr+= "Error in File name : " + errFileName;
    msgStr+= "\n"; 
    msgStr+= "Error msg: " + str(exObj);
    msgStr+= "\n"; 
    msgStr+= "Error line no: " + errLineNoInFile;
    msgStr+= "\n";
    msgStr+= "Error traceback: " + traceBackStr; 
    msgStr+= "\n";

    ### store runtime all error of script into file ###
 
    isDirCreated = createRuntimeScriptErrDirectory();
    if isDirCreated == "Y" :
       appendingCntInFileObj = "\n" + msgStr;
       fileObj = open(errFilenameWithPath, "ab+");
       fileObj.write(getConvertedStrIntoBytesToWriteIntoFileObj(appendingCntInFileObj, 'ab+'));
       fileObj.close();

    
    ### display error msg on screen to user ###

    if isDispScriptErrMsg != "Y" :
       msgStr = "Some unwanted errors occured, script further execution processing has been stopped.";
       msgStr+= "\n";
       msgStr+= "Check path : " + errFilenameWithPath;
        
 
    displayMsg('', msgStr);
  
    sys.exit();


### get status of keyname exist in dictionary obj ###

def iskeynameExistInDictObj(dictObj, keyName):

    keynameExistStatus = False;
    
    try:

       if len(dictObj)>0 :
          pythonVs = sys.version_info[0];
          if (pythonVs)<3 :
              keynameExistStatus = dictObj.has_key(keyName);
          else:
              keynameExistStatus = keyName in dictObj;            

    except Exception as e:
           handleProcsngAbtErrException("Y");

    return keynameExistStatus;

    
### display diff DB comparsion summary report on screen ###

def displayDiffDBCmpSummaryReport():

    try:

        global diffDBComparsionSummaryDataObj;
      
        executionStartDateTime = diffDBComparsionSummaryDataObj['executionEndDateTime'];
        executionEndDateTime = datetime.datetime.now();
        executionTotalTime = executionEndDateTime - executionStartDateTime;
        displayMsgStr = "";

        for svrType in diffDBComparsionSummaryDataObj:
            
            if svrType == 'DstSvr' :
                       
               svrTypeLblStr = "";
               svrTypeDataObj = diffDBComparsionSummaryDataObj[svrType];
  
               if svrType == 'SrcSvr' :
                  svrTypeLblStr = "Source server";                  
               if svrType == 'DstSvr' :
                  svrTypeLblStr = "Destination server";
                
               if svrTypeLblStr!="" and len(svrTypeDataObj)>0 :

                  countOfDiffFoundOnDBS = len(svrTypeDataObj['diffFoundOnDBSDataObj']);
                  countOfDiffNtFoundOnDBS = len(svrTypeDataObj['diffNtFoundOnDBSDataObj']);
                  isChangesExecuted = svrTypeDataObj['isChangesExecuted'];
                  if isChangesExecuted == "Y" :
                     isChangesExecuted = "YES";
                  else :
                       isChangesExecuted = "NO";
 
                  if countOfDiffFoundOnDBS>=0 or countOfDiffNtFoundOnDBS>=0 :

                     displayMsgStr+= "\n";
                     displayMsgStr+= svrTypeLblStr + " changes found on DBS : " + str(countOfDiffFoundOnDBS);
                     if countOfDiffFoundOnDBS>0 :
                        dbNamesStr = ", ".join(list(svrTypeDataObj['diffFoundOnDBSDataObj'].keys()));
                        displayMsgStr+= " (" + dbNamesStr + ")";
                     displayMsgStr+= "\n";
                     displayMsgStr+= svrTypeLblStr + " changes not found on DBS : " + str(countOfDiffNtFoundOnDBS);
                     if countOfDiffNtFoundOnDBS>0 :
                        dbNamesStr = ", ".join(list(svrTypeDataObj['diffNtFoundOnDBSDataObj'].keys()));
                        displayMsgStr+= " (" + dbNamesStr + ")";
                     displayMsgStr+= "\n";
                     displayMsgStr+= "Is changes executed on DBS (" + svrTypeLblStr + ") : " + str(isChangesExecuted);
                     displayMsgStr+= "\n";
                     displayMsgStr+= "\n";
 
               break;


        msgStr = "##### DBS Comparsion Summary Report #####" + "\n" + displayMsgStr;
        msgStr+= "Overall execution started datetime : " + str(executionStartDateTime);
        msgStr+= "\n";
        msgStr+= "Overall execution ended datetime : " + str(executionEndDateTime);
        msgStr+= "\n";
        msgStr+= "Overall execution total time taken : " + str(executionTotalTime);
        msgStr+= "\n"; 

        displayMsg('', msgStr);


    except Exception as e:
           handleProcsngAbtErrException("Y");



### split arr into sub array ###

def splitArrIntoSubArr(inputArr, cntOfSubArr):

    inputArrLen = len(inputArr);
    inputArr = [ inputArr [ i * inputArrLen // cntOfSubArr : (i+1) * inputArrLen // cntOfSubArr] for i in range(cntOfSubArr) ];

    return inputArr;


### get single quotes around comma seperated string ###

def getStringWrappedBySingleQuotes(strContent):

    try:

        if strContent!="" :
           splittedStrAsArr = strContent.split(",");
           if len(splittedStrAsArr)>0:
              strContent = ','.join("'{0}'".format(splittedStr) for splittedStr in splittedStrAsArr);
          
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return strContent;


### get db system level schemas names configuration to not include further in comparsion DBS ###

def getDbSysLvlSchemaNamesConfigToNotIncludeInComparsion():

    ntSchemaNamesConfigDataObj = {};
    ntSchemaNamesConfigDataObj['sysSchemaNamesRegexExpStr'] = '';
    ntSchemaNamesConfigDataObj['ntSysSchemasNamesStr'] = '';
 
    try:

        global inputArgsDataObj;
           
        if inputArgsDataObj['includeSchemasNameBasedOnIndentifierCharsRegexStr']!="":
           sysSchemaNamesRegexExpStr = "'" + inputArgsDataObj['includeSchemasNameBasedOnIndentifierCharsRegexStr'] + "+$'";
           ntSchemaNamesConfigDataObj['sysSchemaNamesRegexExpStr'] = sysSchemaNamesRegexExpStr;
        if inputArgsDataObj['ntSysSchemasNamesStr']!="":
           ntSchemaNamesConfigDataObj['ntSysSchemasNamesStr'] = inputArgsDataObj['ntSysSchemasNamesStr'];


    except Exception as e:
           handleProcsngAbtErrException("Y");
 
    return ntSchemaNamesConfigDataObj;


### get stored db server configuraton details ###

def getStoredDBSvrConfigData(againstSvr):
   
    dbSvrSchemaNamesConfigDataObj = {};
    dbSvrSchemaNamesConfigDataObj['dbHOST'] = '';
    dbSvrSchemaNamesConfigDataObj['dbPORTNO'] = ''; 
    dbSvrSchemaNamesConfigDataObj['dbUSER'] = '';
    dbSvrSchemaNamesConfigDataObj['dbPASS'] = '';
 
    try:
       
        ### section about source server details ###

        if againstSvr == "SrcSvr":
           global srcDbSvrConfigDataObj;
           dbSvrSchemaNamesConfigDataObj['dbHOST'] = srcDbSvrConfigDataObj['dbHOST'];
           dbSvrSchemaNamesConfigDataObj['dbPORTNO'] = srcDbSvrConfigDataObj['dbPORTNO'];
           dbSvrSchemaNamesConfigDataObj['dbUSER'] = srcDbSvrConfigDataObj['dbUSER'];
           dbSvrSchemaNamesConfigDataObj['dbPASS'] = srcDbSvrConfigDataObj['dbPASS'];

        ### section about destination server details ###
 
        if againstSvr == "DstSvr":
           global dstDbSvrConfigDataObj;
           dbSvrSchemaNamesConfigDataObj['dbHOST'] = dstDbSvrConfigDataObj['dbHOST'];
           dbSvrSchemaNamesConfigDataObj['dbPORTNO'] = dstDbSvrConfigDataObj['dbPORTNO'];
           dbSvrSchemaNamesConfigDataObj['dbUSER'] = dstDbSvrConfigDataObj['dbUSER'];
           dbSvrSchemaNamesConfigDataObj['dbPASS'] = dstDbSvrConfigDataObj['dbPASS'];
         

    except Exception as e:
           handleProcsngAbtErrException("Y");

    return dbSvrSchemaNamesConfigDataObj;   

 
### create db directory to store sql query stmt files ###

def createDbDirectoryToStoreSqlQryFiles(diffDbLogDirNamePath, dbSvrFoldername, dbName, createDirNamesDataObj):

    isDirCreated = 'N';

    try:

       if diffDbLogDirNamePath!="" and dbSvrFoldername!="" and dbName!="" and len(createDirNamesDataObj)>0 :

          isAllowDbDirNameToCreate = "N";
          dbSvrFoldernameWithPathStr = diffDbLogDirNamePath+"/"+dbSvrFoldername;
          dbSvrFoldernameWithPathStr = replaceFilePathSeparatorViaOsPlatform(dbSvrFoldernameWithPathStr);
          dbSvrFoldernameDbNameWithPathStr = diffDbLogDirNamePath+"/"+dbSvrFoldername+"/"+dbName;
          dbSvrFoldernameDbNameWithPathStr = replaceFilePathSeparatorViaOsPlatform(dbSvrFoldernameDbNameWithPathStr);

          if os.path.exists(diffDbLogDirNamePath+"/"+dbSvrFoldername) == False:
             os.mkdir(dbSvrFoldernameWithPathStr);
             os.chmod(dbSvrFoldernameWithPathStr, 0o777);
             isAllowDbDirNameToCreate = "Y";
          else :
               if os.path.exists(dbSvrFoldernameDbNameWithPathStr) == False:
                  os.chmod(dbSvrFoldernameWithPathStr, 0o777);       
                  isAllowDbDirNameToCreate = "Y";
               else:
                   isDirCreated = 'Y';

          if isAllowDbDirNameToCreate == 'Y' :

             os.mkdir(dbSvrFoldernameDbNameWithPathStr);
             os.chmod(dbSvrFoldernameDbNameWithPathStr, 0o777);

             executeAllChangesFoldername = createDirNamesDataObj['executeAllChangesFoldername'];
             filePathStr1 = diffDbLogDirNamePath+"/"+dbSvrFoldername+"/"+dbName+"/"+executeAllChangesFoldername;
             filePathStr1 = replaceFilePathSeparatorViaOsPlatform(filePathStr1);
             os.mkdir(filePathStr1);
             os.chmod(filePathStr1, 0o777);

             addingNewChangesFoldername = createDirNamesDataObj['addingNewChangesFoldername'];
             filePathStr2 = diffDbLogDirNamePath+"/"+dbSvrFoldername+"/"+dbName+"/"+addingNewChangesFoldername;
             filePathStr2 = replaceFilePathSeparatorViaOsPlatform(filePathStr2);
             os.mkdir(filePathStr2);
             os.chmod(filePathStr2, 0o777);
                  
             updationChangesFoldername = createDirNamesDataObj['updationChangesFoldername'];
             filePathStr3 = diffDbLogDirNamePath+"/"+dbSvrFoldername+"/"+dbName+"/"+updationChangesFoldername;
             filePathStr3 = replaceFilePathSeparatorViaOsPlatform(filePathStr3);
             os.mkdir(filePathStr3);
             os.chmod(filePathStr3, 0o777);

             droppedChangesFoldername = createDirNamesDataObj['droppedChangesFoldername'];
             filePathStr4 = diffDbLogDirNamePath+"/"+dbSvrFoldername+"/"+dbName+"/"+droppedChangesFoldername;
             filePathStr4 = replaceFilePathSeparatorViaOsPlatform(filePathStr4);
             os.mkdir(filePathStr4);
             os.chmod(filePathStr4, 0o777);
   
             importantRestrictionsFoldername = createDirNamesDataObj['importantRestrictionsFoldername'];
             filePathStr5 = diffDbLogDirNamePath+"/"+dbSvrFoldername+"/"+dbName+"/"+importantRestrictionsFoldername;
             filePathStr5 = replaceFilePathSeparatorViaOsPlatform(filePathStr5);
             os.mkdir(filePathStr5);
             os.chmod(filePathStr5, 0o777); 

             errFoldername = createDirNamesDataObj['errFoldername'];
             filePathStr6 = diffDbLogDirNamePath+"/"+dbSvrFoldername+"/"+dbName+"/"+errFoldername;
             filePathStr6 = replaceFilePathSeparatorViaOsPlatform(filePathStr6);
             os.mkdir(filePathStr6);
             os.chmod(filePathStr6, 0o777);

             isDirCreated = 'Y';

 
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return isDirCreated;


### create diff db log base directory ###

def createDiffDBLogBaseDirectory(diffDbLogDirNamePath, againstSvr, dbName):
 
    isDirCreated = 'N';

    try:
        
        global toStoreDiffDbChangesFoldernameDataObj;
        dbSvrFoldername = "";
 
        if againstSvr == "SrcSvr" :
           global srcDbSvrFolderName;
           dbSvrFoldername = srcDbSvrFolderName;
        if againstSvr == "DstSvr" :
           global dstDbSvrFolderName;
           dbSvrFoldername = dstDbSvrFolderName;  

        diffDbLogDirNamePath = replaceFilePathSeparatorViaOsPlatform(diffDbLogDirNamePath);

        if os.path.exists(diffDbLogDirNamePath) == False:
           os.mkdir(diffDbLogDirNamePath);
           os.chmod(diffDbLogDirNamePath, 0o777);
        
        isDirCreated = createDbDirectoryToStoreSqlQryFiles(
             diffDbLogDirNamePath, dbSvrFoldername, dbName, toStoreDiffDbChangesFoldernameDataObj
        );

    except Exception as e:
           handleProcsngAbtErrException("Y");
 
    return isDirCreated;



### return sql queries stmt log files names to store sql queries ###

def getFileNamesToStoreSqlQry(diffDbLogDirNamePath, againstSvr, dbName):

   fileNamesDataObj = {};
   
   try:

       if diffDbLogDirNamePath!="" and againstSvr!="" and dbName!="":
         
          dbSvrFoldername = "";
          dbsFileNamesDataObj = {};

          ### section about source server ###

          if againstSvr == "SrcSvr" :
             global srcDbSvrFolderName;
             global toStoreSqlQryFilesLogAbtSrcSvrDataObj; 
             dbSvrFoldername = srcDbSvrFolderName;
             dbsFileNamesDataObj = toStoreSqlQryFilesLogAbtSrcSvrDataObj['schemasDataObj'];

          ### section about destination server ###

          if againstSvr == "DstSvr" :
             global dstDbSvrFolderName;
             global toStoreSqlQryFilesLogAbtDstSvrDataObj; 
             dbSvrFoldername = dstDbSvrFolderName;
             dbsFileNamesDataObj = toStoreSqlQryFilesLogAbtDstSvrDataObj['schemasDataObj'];


          isDbNameDirExist = iskeynameExistInDictObj(dbsFileNamesDataObj, dbName);
          if isDbNameDirExist == False:

             fileName1 = "executeAllChanges.sql";
             filePath1 = diffDbLogDirNamePath+"/"+dbSvrFoldername+"/"+dbName+"/executeAllChanges/"+fileName1;
             filePath1 = replaceFilePathSeparatorViaOsPlatform(filePath1);
             
             fileName2 = "addingNewChanges.sql";
             filePath2 = diffDbLogDirNamePath+"/"+dbSvrFoldername+"/"+dbName+"/addingNewChanges/"+fileName2;
             filePath2 = replaceFilePathSeparatorViaOsPlatform(filePath2);

             fileName3 = "updationChanges.sql";
             filePath3 = diffDbLogDirNamePath+"/"+dbSvrFoldername+"/"+dbName+"/updationChanges/"+fileName3;
             filePath3 = replaceFilePathSeparatorViaOsPlatform(filePath3);

             fileName4 = "droppedChanges.sql";
             filePath4 = diffDbLogDirNamePath+"/"+dbSvrFoldername+"/"+dbName+"/droppedChanges/"+fileName4;
             filePath4 = replaceFilePathSeparatorViaOsPlatform(filePath4);

             fileName5 = "importantRestrictions.sql";
             filePath5 = diffDbLogDirNamePath+"/"+dbSvrFoldername+"/"+dbName+"/importantRestrictions/"+fileName5;
             filePath5 = replaceFilePathSeparatorViaOsPlatform(filePath5);

             fileName6 = "error.sql";
             filePath6 = diffDbLogDirNamePath+"/"+dbSvrFoldername+"/"+dbName+"/error/"+fileName6;
             filePath6 = replaceFilePathSeparatorViaOsPlatform(filePath6);

             dbsFileNamesDataObj[dbName] = {};
             dbsFileNamesDataObj[dbName]['executeAllChanges'] = {"filePath": filePath1, "fileName" : fileName1};
             dbsFileNamesDataObj[dbName]['addingNewChanges'] = {"filePath": filePath2, "fileName" : fileName2};
             dbsFileNamesDataObj[dbName]['updationChanges'] = {"filePath": filePath3, "fileName" : fileName3};
             dbsFileNamesDataObj[dbName]['droppedChanges'] = {"filePath": filePath4, "fileName" : fileName4};
             dbsFileNamesDataObj[dbName]['importantRestrictions'] = {"filePath": filePath5, "fileName" : fileName5};
             dbsFileNamesDataObj[dbName]['error'] = {"filePath": filePath6};  

             fileNamesDataObj = dbsFileNamesDataObj[dbName];   

          if isDbNameDirExist == True:
             fileNamesDataObj = dbsFileNamesDataObj[dbName];  

    
   except Exception as e:
           handleProcsngAbtErrException("Y");

   return fileNamesDataObj;



### checking db connection link can open ###

def isDbConnectionLinkCanOpen(dbHOST, dbPORTNO, dbUSER, dbPASS, dbNAME):

    isDbConnectionCanLink = 'Y';

    try:
 
        if dbNAME == "" :
           dbNAME = "INFORMATION_SCHEMA";

        dbPORTNO = int(dbPORTNO);  
 
        dbCon = pymysql.connect(host=dbHOST, user=dbUSER, passwd=dbPASS, db=dbNAME, port=dbPORTNO);
        dbCon.close();
       
    except Exception as e:
           ## handleProcsngAbtErrException("Y");
           isDbConnectionCanLink = 'N';

    return isDbConnectionCanLink;



### fetch data from db ###

def fetchDataFromDB(dbHOST, dbPORTNO, dbUSER, dbPASS, dbNAME, dbQUERY):

    arrOfArrData = ();

    try:
 
        if dbNAME == "":
           dbNAME = "INFORMATION_SCHEMA";

        dbPORTNO = int(dbPORTNO); 

        dbCon = pymysql.connect(host=dbHOST, user=dbUSER, passwd=dbPASS, db=dbNAME, port=dbPORTNO); 
        cursor = dbCon.cursor();
        cursor._defer_warnings = True; 
        cursor.execute(dbQUERY);
        arrOfArrData = cursor.fetchall(); 
        dbCon.close();
       
    except Exception as e:
           handleProcsngAbtErrException("Y");
           arrOfArrData = ();

    return arrOfArrData;


### fetch info schemas data from db ###

def getInfoSchemasData(paramDataObj):

    arrOfArrData = ();
 
    try:

       if len(paramDataObj)>0 :

          ### given param data to fetch related to info schemas data ###

          dbHOST = paramDataObj['dbHOST'];
          dbPORTNO = paramDataObj['dbPORTNO'];
          dbUSER = paramDataObj['dbUSER'];
          dbPASS = paramDataObj['dbPASS'];
          dbNAME = paramDataObj['dbNAME'];
          ntSysSchemasNamesStr = paramDataObj['ntSysSchemasNamesStr'];
          sysSchemaNamesRegexExpStr = paramDataObj['sysSchemaNamesRegexExpStr'];
          dbBasedTypeStr = paramDataObj['dbBasedTypeStr'];
          ntDbNamesStr = paramDataObj['ntDbNamesStr'];
          dbNamesStr = paramDataObj['dbNamesStr'];
          dbTblNamesStr = paramDataObj['dbTblNamesStr'];
          dbTblColNamesStr = paramDataObj['dbTblColNamesStr'];
          dbTblIndxNamesStr = paramDataObj['dbTblIndxNamesStr'];
          dbTblFKNamesStr = paramDataObj['dbTblFKNamesStr'];
          dbTblTgrNamesStr = paramDataObj['dbTblTgrNamesStr'];
          dbRoutineNamesStr = paramDataObj['dbRoutineNamesStr'];
          dbViewNamesStr = paramDataObj['dbViewNamesStr']; 
          customSearchCondStr = paramDataObj['customSearchCondStr'];

          ### info schemas predfined config data ###

          infoSchemasConfigDataObj = paramDataObj['infoSchemasConfigDataObj'];
          selectToWhereStmt = infoSchemasConfigDataObj['selectToWhereStmt'];
          ntSysSchemasNamesWhereCondStr = infoSchemasConfigDataObj['ntSysSchemasNamesWhereCondStr'];
          sysSchemaNamesRegexExpWhereCondStr = infoSchemasConfigDataObj['sysSchemaNamesRegexExpWhereCondStr'];
          dbBasedTypeWhereCondStr = infoSchemasConfigDataObj['dbBasedTypeWhereCondStr'];
          ntDbNamesWhereCondStr = infoSchemasConfigDataObj['ntDbNamesWhereCondStr'];
          dbNamesWhereCondStr = infoSchemasConfigDataObj['dbNamesWhereCondStr'];
          dbTblNamesWhereCondStr = infoSchemasConfigDataObj['dbTblNamesWhereCondStr'];
          dbTblColNamesWhereCondStr = infoSchemasConfigDataObj['dbTblColNamesWhereCondStr'];
          dbTblIndxNamesWhereCondStr = infoSchemasConfigDataObj['dbTblIndxNamesWhereCondStr'];
          dbTblFKNamesWhereCondStr = infoSchemasConfigDataObj['dbTblFKNamesWhereCondStr'];
          dbTblTgrNamesWhereCondStr = infoSchemasConfigDataObj['dbTblTgrNamesWhereCondStr'];
          dbRoutineNamesWhereCondStr = infoSchemasConfigDataObj['dbRoutineNamesWhereCondStr'];
          dbViewNamesWhereCondStr = infoSchemasConfigDataObj['dbViewNamesWhereCondStr'];
          groupByStmt = infoSchemasConfigDataObj['groupByStmt'];
          orderByStmt = infoSchemasConfigDataObj['orderByStmt'];

          if dbHOST!="" and dbPORTNO!="" and dbUSER!="" and dbPASS!="" and selectToWhereStmt!="" :
        
             dbQUERY = selectToWhereStmt;
             
             if ntSysSchemasNamesWhereCondStr!="" and ntSysSchemasNamesStr!="" :
                dbQUERY+= ntSysSchemasNamesWhereCondStr.format(ntSysSchemasNamesStr = ntSysSchemasNamesStr);             
             if sysSchemaNamesRegexExpWhereCondStr!="" and sysSchemaNamesRegexExpStr!="" :
                dbQUERY+= sysSchemaNamesRegexExpWhereCondStr.format(sysSchemaNamesRegexExpStr = sysSchemaNamesRegexExpStr);
             if dbBasedTypeWhereCondStr!="" and dbBasedTypeStr!="" :
                dbQUERY+= dbBasedTypeWhereCondStr.format(dbBasedTypeStr = dbBasedTypeStr);  
             if ntDbNamesWhereCondStr!="" and ntDbNamesStr!="" :
                dbQUERY+= ntDbNamesWhereCondStr.format(ntDbNamesStr = ntDbNamesStr);    
             if dbNamesWhereCondStr!="" and dbNamesStr!="" :
                dbQUERY+= dbNamesWhereCondStr.format(dbNamesStr = dbNamesStr);

             if dbTblNamesWhereCondStr!="" and dbTblNamesStr!="" :
                dbQUERY+= dbTblNamesWhereCondStr.format(dbTblNamesStr = dbTblNamesStr);
             if dbTblColNamesWhereCondStr!="" and dbTblColNamesStr!="" :
                dbQUERY+= dbTblColNamesWhereCondStr.format(dbTblColNamesStr = dbTblColNamesStr);
             if dbTblIndxNamesWhereCondStr!="" and dbTblIndxNamesStr!="" :
                dbQUERY+= dbTblIndxNamesWhereCondStr.format(dbTblIndxNamesStr = dbTblIndxNamesStr); 
             if dbTblFKNamesWhereCondStr!="" and dbTblFKNamesStr!="" :
                dbQUERY+= dbTblFKNamesWhereCondStr.format(dbTblFKNamesStr = dbTblFKNamesStr);
             if dbTblTgrNamesWhereCondStr!="" and dbTblTgrNamesStr!="" :
                dbQUERY+= dbTblTgrNamesWhereCondStr.format(dbTblTgrNamesStr = dbTblTgrNamesStr);
             if dbRoutineNamesWhereCondStr!="" and dbRoutineNamesStr!="" :
                dbQUERY+= dbRoutineNamesWhereCondStr.format(dbRoutineNamesStr = dbRoutineNamesStr);
             if dbViewNamesWhereCondStr!="" and dbViewNamesStr!="" :
                dbQUERY+= dbViewNamesWhereCondStr.format(dbViewNamesStr = dbViewNamesStr); 
             if customSearchCondStr!="" :
                dbQUERY+= customSearchCondStr;

             if groupByStmt!="" :
                dbQUERY+= groupByStmt;
             if orderByStmt!="" :
                dbQUERY+= orderByStmt;
  
             arrOfArrData = fetchDataFromDB(dbHOST, dbPORTNO, dbUSER, dbPASS, dbNAME, dbQUERY);
   

    except Exception as e:
           handleProcsngAbtErrException("Y");  

    return arrOfArrData;




### execute sql query stmt file on db ###

def executeSqlQryFileOnDB(dbHOST, dbPORTNO, dbUSER, dbPASS, dbNAME, filenameWithPath):

    qryExecutedStatusDataObj = {};
    qryExecutedStatusDataObj['isQryExecutedSuccessfully'] = "Y";
    qryExecutedStatusDataObj['errorStr'] = "";  

    try:
 
        if dbHOST!="" and dbPORTNO!="" and dbUSER!="" and dbPASS!="" and dbNAME!="" and filenameWithPath!="":
           if os.path.exists(filenameWithPath) == True:
              dbPORTNO = str(dbPORTNO);
              dbInstalledPath = getDBInstalledPathViaOsPlatform("mysql");
              dbInstCmdArr = [dbInstalledPath, '-port='+dbPORTNO, '-u'+dbUSER, '-p'+dbPASS, '-h'+dbHOST, '--force', '--database='+dbNAME];
              with open(filenameWithPath) as inputFile:
                   proc = subprocess.Popen(dbInstCmdArr, stdout=PIPE, stdin=inputFile, stderr=PIPE, shell=False);
                   output, err = proc.communicate();
                   qryExecutedStatusDataObj['isQryExecutedSuccessfully'] = 'Y';
                   qryExecutedStatusDataObj['errorStr'] = err;
         
    except Exception as e:
           handleProcsngAbtErrException("Y");
           qryExecutedStatusDataObj['isQryExecutedSuccessfully'] = "N";
           qryExecutedStatusDataObj['errorStr'] = str(e);

    
    return qryExecutedStatusDataObj;




### get db schemas names via info schemas ###

def getDbSchemasNamesViaInfoSchemas(dbHOST,dbPORTNO,dbUSER,dbPASS,dbBasedTypeStr,ntDbNamesStr,dbNamesStr):

    dbSchemasNamesArr = [];

    try:

       if dbHOST!="" and dbPORTNO!="" and dbUSER!="" and dbPASS!="" :
          
           global inputArgsDataObj;
           sysSchemaNamesRegexExpStr = "";
           if inputArgsDataObj['includeSchemasNameBasedOnIndentifierCharsRegexStr']!="":
              sysSchemaNamesRegexExpStr = "'" + inputArgsDataObj['includeSchemasNameBasedOnIndentifierCharsRegexStr'] + "+$'";

           dbQuery = """SELECT
                        s.SCHEMA_NAME dbName
                        FROM INFORMATION_SCHEMA.SCHEMATA s
                        WHERE 1
                        AND s.SCHEMA_NAME NOT IN ('INFORMATION_SCHEMA','mysql','performance_schema','phpmyadmin')""";

           if sysSchemaNamesRegexExpStr!="":
              dbQuery+= """ AND (s.SCHEMA_NAME REGEXP {sysSchemaNamesRegexExpStr})>0""".format(sysSchemaNamesRegexExpStr = sysSchemaNamesRegexExpStr);
   
           if dbBasedTypeStr!="" :
              dbQuery+= """ AND s.SCHEMA_NAME LIKE '%\_{includeDbBasedTypeStr}%'""".format(includeDbBasedTypeStr = dbBasedTypeStr);
           if ntDbNamesStr!="" :
              dbNamesArr = ntDbNamesStr.split(",");
              if len(dbNamesArr)>0:
                 ntDbNamesStr = ','.join("'{0}'".format(eachDbName) for eachDbName in dbNamesArr);
              dbQuery+= """ AND s.SCHEMA_NAME NOT IN ({ntIncludeDbNamesStr})""".format(ntIncludeDbNamesStr = ntDbNamesStr);
           if dbNamesStr!="" :
              dbNamesArr = dbNamesStr.split(",");
              if len(dbNamesArr)>0:
                 dbNamesStr = ','.join("'{0}'".format(eachDbName) for eachDbName in dbNamesArr); 
              dbQuery+= """ AND s.SCHEMA_NAME IN ({includeDbNamesStr})""".format(includeDbNamesStr = dbNamesStr);

           dbQuery+= """ ORDER BY s.SCHEMA_NAME ASC""";
          
           dataArrOfArr = fetchDataFromDB(dbHOST, dbPORTNO, dbUSER, dbPASS, '', dbQuery);
           dataArrOfArrLen = len(dataArrOfArr);
           for dataArrIndx in range(dataArrOfArrLen): 
               dataArr = list(dataArrOfArr[dataArrIndx]);
               dbSchemasNamesArr.append(dataArr[0]);


    except Exception as e:
           handleProcsngAbtErrException("Y");

 
    return dbSchemasNamesArr;



### handle processing to execute sql queries files on DBS ###

def handleProcsngToExecuteSqlQryFilesOnDBS(dbNameFolderwiseDataObj,dbSvrSchemaNamesConfigDataObj,isExecuteChanges):

    try:

        countOfDbNamesArr = len(dbNameFolderwiseDataObj);
        if countOfDbNamesArr>0 and len(dbSvrSchemaNamesConfigDataObj)>0:

           global diffDBComparsionSummaryDataObj;
  
           allDbNamesArr = list(dbNameFolderwiseDataObj.keys());
           sortedAscOdrDbNamesArr = sorted(allDbNamesArr);

           ### iterating each db ###
 
           for dbName in sortedAscOdrDbNamesArr:

               ### variable declare ###
  
               foldernamesDataObj = dbNameFolderwiseDataObj[dbName]; 
               sqlQryExecutionFileNameWithPathStr = "";
               isSqlQryExecutionFileExist = 'N';
               sqlQryErrFileNameWithPathStr = "";
               sqlQryImpRestrictionsFileNameWithPathStr = "";
               isSqlQryImpRestrictionsFileExist = 'N'; 

               
               ### extracting sql query execution file name with path ###
                
               isexecuteAllChangesFoldernameExist = iskeynameExistInDictObj(foldernamesDataObj, 'executeAllChanges');
               if isexecuteAllChangesFoldernameExist == True:   
                  isSqlQryFilenamePathExist = iskeynameExistInDictObj(foldernamesDataObj['executeAllChanges'], 'filePath');
                  if isSqlQryFilenamePathExist == True:
                     sqlQryExecutionFileNameWithPathStr = foldernamesDataObj['executeAllChanges']['filePath'];

               ### extracting sql query important restrictions file name with path ###

               isImpRestrictionsFoldernameExist = iskeynameExistInDictObj(foldernamesDataObj, 'importantRestrictions');
               if isImpRestrictionsFoldernameExist == True:   
                  isSqlQryFilenamePathExist = iskeynameExistInDictObj(foldernamesDataObj['importantRestrictions'], 'filePath');
                  if isSqlQryFilenamePathExist == True:
                     sqlQryImpRestrictionsFileNameWithPathStr = foldernamesDataObj['importantRestrictions']['filePath']; 

               ### extracting sql query error file name with path ###

               isErrorFoldernameExist = iskeynameExistInDictObj(foldernamesDataObj, 'error');
               if isErrorFoldernameExist == True:   
                  isSqlQryErrFilenamePathExist = iskeynameExistInDictObj(foldernamesDataObj['error'], 'filePath');
                  if isSqlQryErrFilenamePathExist == True:
                     sqlQryErrFileNameWithPathStr = foldernamesDataObj['error']['filePath'];


               ### checking file exist or not ###
 
               if os.path.exists(sqlQryExecutionFileNameWithPathStr) == True:
                  isSqlQryExecutionFileExist = 'Y';
 
               ### checking file exist or not ###

               if os.path.exists(sqlQryImpRestrictionsFileNameWithPathStr) == True:
                  isSqlQryImpRestrictionsFileExist = 'Y';
 

               ### file exist then process further ###

               if isSqlQryExecutionFileExist == "Y" or isSqlQryImpRestrictionsFileExist == "Y" :

                  msgStr1 = "\n";
                  msgStr2 = "\n";

                  ### sql query execution file exist with content, then process further ###

                  if isSqlQryExecutionFileExist == "Y" :
 
                     executeAllChangesFileName = foldernamesDataObj['executeAllChanges']['fileName']; 
                     executeAllChangesFilePath = sqlQryExecutionFileNameWithPathStr.split(executeAllChangesFileName)[0];

                     ### display starting point msg ####
 
                     if isExecuteChanges == "Y" :
                        msgStr1+= "Executing changes on DB : " + dbName;
                     else:
                         msgStr1+= "Execute changes manually on DB : " + dbName;


                     msgStr1+= "\n";
                     msgStr1+= "File path : " + executeAllChangesFilePath;
                     msgStr1+= "\n";
                     msgStr1+= "File name : " + executeAllChangesFileName;
                     msgStr1+= "\n"; 
                     displayMsg('', msgStr1);


                     dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
                     dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];  
                     dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
                     dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

                     os.chmod(sqlQryExecutionFileNameWithPathStr, 0o777);

                     appendContentInFileAtBegLevelStr = "\n" + "\n" + "SET UNIQUE_CHECKS = 0;"  + "\n";
                     appendContentInFileAtBegLevelStr+= "SET foreign_key_checks = 0;" + "\n" + "\n";
                     fileObj1 = open(sqlQryExecutionFileNameWithPathStr, "r+");
                     fileObj1ExistContent = fileObj1.read();
                     fileObj1.seek(0,0);
                     appendingContentInToFileObj = appendContentInFileAtBegLevelStr + fileObj1ExistContent;
                     fileObj1.write(getConvertedStrIntoBytesToWriteIntoFileObj(appendingContentInToFileObj, 'r+'));
                     fileObj1.close();

                     appendContentInFileAtEndLevelStr = "\n" + "\n" + "SET UNIQUE_CHECKS = 1;"  + "\n";
                     appendContentInFileAtEndLevelStr+= "SET foreign_key_checks = 1;" + "\n" + "\n";
                     fileObj2 = open(sqlQryExecutionFileNameWithPathStr, "a+");
                     fileObj2.write(getConvertedStrIntoBytesToWriteIntoFileObj(appendContentInFileAtEndLevelStr, 'a+'));
                     fileObj2.close(); 


                     ### execute sql file query smt on corresponding DB ###

                     if isExecuteChanges == "Y" :

                        qryExecutionStatus = executeSqlQryFileOnDB(
                             dbHOST, dbPORTNO, dbUSER, dbPASS, dbName, sqlQryExecutionFileNameWithPathStr
                        );

                        ### store error occured while executing sql query stmt file on DB ###

                        if qryExecutionStatus['errorStr'] !="":
                           appendingCntInFileObj = str("\n\n") + str(qryExecutionStatus['errorStr']);
                           fileObj = open(sqlQryErrFileNameWithPathStr, "ab+");
                           fileObj.write(getConvertedStrIntoBytesToWriteIntoFileObj(appendingCntInFileObj, 'ab+'));
                           fileObj.close();

                     
                     ### store dbName info for displaying summary report purpose (schemas changes found) ###

                     diffDBComparsionSummaryDataObj['DstSvr']['diffFoundOnDBSDataObj'][dbName] = {}; 
                     diffDBComparsionSummaryDataObj['DstSvr']['isChangesExecuted'] = isExecuteChanges;  
        
                  
                  if isSqlQryImpRestrictionsFileExist == "Y" :

                     importantRestrictionsFileName = foldernamesDataObj['importantRestrictions']['fileName']; 
                     importantRestrictionsFilePath = sqlQryImpRestrictionsFileNameWithPathStr.split(importantRestrictionsFileName)[0];
                     msgStr2+= "Important restrictions query on DB : " + dbName;
                     msgStr2+= "\n";  
                     msgStr2+= "File path : " + importantRestrictionsFilePath;
                     msgStr2+= "\n";
                     msgStr2+= "File name : " + importantRestrictionsFileName;
                     msgStr2+= "\n";
                     
                     displayMsg('', msgStr2);

               else:

                   diffDBComparsionSummaryDataObj['DstSvr']['diffNtFoundOnDBSDataObj'][dbName] = {}; 


    except Exception as e:
           handleProcsngAbtErrException("Y");


### execute diff db changes between source and destination server ###

def handleProcsngExecuteDiffDBChangesBtwnSrcAndDstSvr():
 
    try:
      
        global inputArgsDataObj;
        applyChangesOn = inputArgsDataObj['applyChangesOn'];
        isExecuteChanges = inputArgsDataObj['isExecuteChanges'];

        ### section related to source server ###

        if applyChangesOn == "SrcSvr":

           global srcDbSvrConfigDataObj;
           global toStoreSqlQryFilesLogAbtSrcSvrDataObj;
           schemasLvlChangesOnDBSDataObj = toStoreSqlQryFilesLogAbtSrcSvrDataObj['schemasDataObj'];          

           ### schemas level changes on DBS ###

           handleProcsngToExecuteSqlQryFilesOnDBS(
                 schemasLvlChangesOnDBSDataObj, srcDbSvrConfigDataObj, isExecuteChanges
           ); 
           

        ### section related to destination server ###

        if applyChangesOn == "DstSvr":
           
           global dstDbSvrConfigDataObj;
           global toStoreSqlQryFilesLogAbtDstSvrDataObj;
           schemasLvlChangesOnDBSDataObj = toStoreSqlQryFilesLogAbtDstSvrDataObj['schemasDataObj'];
           
           ### schemas level changes on DBS ###

           handleProcsngToExecuteSqlQryFilesOnDBS(
                 schemasLvlChangesOnDBSDataObj, dstDbSvrConfigDataObj, isExecuteChanges
           );


        ### remove created sql temporary file ###
     
        removeTemporaryCreatedSqlFiles();  


    except Exception as e:
           handleProcsngAbtErrException("Y");



### store sql queries into sql files log ###

def storeDbLvlChangesSqlQryInFilesLog(againstSvr, dbName, qryStmtChangesType, qryStmtStr, isExecuteChanges):
        
    isSqlQryStored = "N";
        
    try:

        if againstSvr!="" and dbName!="" and qryStmtChangesType!="" and qryStmtStr!="" and isExecuteChanges!="" :

           global diffDBLogDirnameWithPathStr;
 
           isDirCreated = createDiffDBLogBaseDirectory(diffDBLogDirnameWithPathStr, againstSvr, dbName);
           if isDirCreated == "Y":
              toStoredSqlQryLogFileNamesDataObj = getFileNamesToStoreSqlQry(diffDBLogDirnameWithPathStr, againstSvr, dbName);
              if len(toStoredSqlQryLogFileNamesDataObj) > 0:
                 
                 if qryStmtChangesType != "importantRestrictions":
                    appendingCntInFileObj = "\n\n" + qryStmtStr;   
                    filePath = toStoredSqlQryLogFileNamesDataObj['executeAllChanges']['filePath'];    
                    fileObj = open(filePath, "ab+");
                    fileObj.write(getConvertedStrIntoBytesToWriteIntoFileObj(appendingCntInFileObj, "ab+"));
                    fileObj.close();
                    isSqlQryStored = 'Y';

                 if qryStmtChangesType == "addingNewChanges":
                    appendingCntInFileObj = "\n\n" + qryStmtStr;
                    filePath = toStoredSqlQryLogFileNamesDataObj['addingNewChanges']['filePath'];    
                    fileObj = open(filePath, "ab+");
                    fileObj.write(getConvertedStrIntoBytesToWriteIntoFileObj(appendingCntInFileObj, "ab+"));
                    fileObj.close();
                    isSqlQryStored = 'Y';

                 if qryStmtChangesType == "updationChanges":
                    appendingCntInFileObj = "\n\n" + qryStmtStr;  
                    filePath = toStoredSqlQryLogFileNamesDataObj['updationChanges']['filePath'];    
                    fileObj = open(filePath, "ab+");
                    fileObj.write(getConvertedStrIntoBytesToWriteIntoFileObj(appendingCntInFileObj, "ab+"));
                    fileObj.close();
                    isSqlQryStored = 'Y';

                 if qryStmtChangesType == "droppedChanges":
                    appendingCntInFileObj = "\n\n" + qryStmtStr;  
                    filePath = toStoredSqlQryLogFileNamesDataObj['droppedChanges']['filePath'];    
                    fileObj = open(filePath, "ab+");
                    fileObj.write(getConvertedStrIntoBytesToWriteIntoFileObj(appendingCntInFileObj, "ab+"));
                    fileObj.close();
                    isSqlQryStored = 'Y';

                 if qryStmtChangesType == "importantRestrictions":
                    appendingCntInFileObj = "\n\n" + qryStmtStr;
                    filePath = toStoredSqlQryLogFileNamesDataObj['importantRestrictions']['filePath'];    
                    fileObj = open(filePath, "ab+");
                    fileObj.write(getConvertedStrIntoBytesToWriteIntoFileObj(appendingCntInFileObj, "ab+"));
                    fileObj.close();
                    isSqlQryStored = 'Y'; 
              


    except Exception as e:
           handleProcsngAbtErrException("Y");
 
    return isSqlQryStored;



### search string and replace string ###

def searchStrAndReplaceStr(strContent, searchStrWithReplaceStrDataObj):

    try:

       if strContent!="" and len(searchStrWithReplaceStrDataObj) > 0 :

          rc = re.compile('|'.join(map(re.escape, searchStrWithReplaceStrDataObj)));
          def translate(match):
              return searchStrWithReplaceStrDataObj[match.group(0)]; 
          strContent = rc.sub(translate, strContent);
              
    except Exception as e:
           handleProcsngAbtErrException("Y"); 

    return strContent;


### get db svr system default date format string ###

def getDbSvrSystemDefaultDateFormat(againstSvr):

    defaultStr = '%Y-%m-%d';

    try:

       dbSvrSystemGlobalVariablesInfoDataObj = {};

       if againstSvr == "SrcSvr" :
          global srcDbSvrInfoSchemasDataObj;
          dbSvrSystemGlobalVariablesInfoDataObj = srcDbSvrInfoSchemasDataObj['sysGlobalVariablesDataObj'];
       if againstSvr == "DstSvr" :
          global dstDbSvrInfoSchemasDataObj;   
          dbSvrSystemGlobalVariablesInfoDataObj = dstDbSvrInfoSchemasDataObj['sysGlobalVariablesDataObj'];          

       isDateFormatKeyExist = iskeynameExistInDictObj(dbSvrSystemGlobalVariablesInfoDataObj, 'DATE_FORMAT');
       if isDateFormatKeyExist == True:
          if dbSvrSystemGlobalVariablesInfoDataObj['DATE_FORMAT']!="":         
             defaultStr = dbSvrSystemGlobalVariablesInfoDataObj['DATE_FORMAT'];
 

    except Exception as e:
           handleProcsngAbtErrException("Y"); 

    return defaultStr;


### get db svr system default datetime format string ###

def getDbSvrSystemDefaultDateTimeFormat(againstSvr):

    defaultStr = '%Y-%m-%d %H:%i:%s';

    try:

       dbSvrSystemGlobalVariablesInfoDataObj = {};

       if againstSvr == "SrcSvr" :
          global srcDbSvrInfoSchemasDataObj;
          dbSvrSystemGlobalVariablesInfoDataObj = srcDbSvrInfoSchemasDataObj['sysGlobalVariablesDataObj'];
       if againstSvr == "DstSvr" :
          global dstDbSvrInfoSchemasDataObj;
          dbSvrSystemGlobalVariablesInfoDataObj = dstDbSvrInfoSchemasDataObj['sysGlobalVariablesDataObj'];          

       isDateTimeFormatKeyExist = iskeynameExistInDictObj(dbSvrSystemGlobalVariablesInfoDataObj, 'DATETIME_FORMAT');
       if isDateTimeFormatKeyExist == True:
          if dbSvrSystemGlobalVariablesInfoDataObj['DATETIME_FORMAT']!="":             
             defaultStr = dbSvrSystemGlobalVariablesInfoDataObj['DATETIME_FORMAT'];
 

    except Exception as e:
           handleProcsngAbtErrException("Y"); 

    return defaultStr;


### get db svr system default time format string ###

def getDbSvrSystemDefaultTimeFormat(againstSvr):

    defaultStr = '%H:%i:%s';

    try:

       dbSvrSystemGlobalVariablesInfoDataObj = {};

       if againstSvr == "SrcSvr" :
          global srcDbSvrInfoSchemasDataObj;
          dbSvrSystemGlobalVariablesInfoDataObj = srcDbSvrInfoSchemasDataObj['sysGlobalVariablesDataObj'];
       if againstSvr == "DstSvr" :
          global dstDbSvrInfoSchemasDataObj;
          dbSvrSystemGlobalVariablesInfoDataObj = dstDbSvrInfoSchemasDataObj['sysGlobalVariablesDataObj'];          

       isTimeFormatKeyExist = iskeynameExistInDictObj(dbSvrSystemGlobalVariablesInfoDataObj, 'TIME_FORMAT');
       if isTimeFormatKeyExist == True:
          if dbSvrSystemGlobalVariablesInfoDataObj['TIME_FORMAT']!="":         
             defaultStr = dbSvrSystemGlobalVariablesInfoDataObj['TIME_FORMAT'];
 

    except Exception as e:
           handleProcsngAbtErrException("Y"); 

    return defaultStr;



### check data available in table ###

def checkDataAvailableInDbTbl(againstSvr, dbName, tblName):

    isDataAvailableInTbl = 'N';

    try:

       infoSchemasDataObj = {};
 
       if againstSvr == "SrcSvr" :
          global srcDbSvrInfoSchemasDataObj;
          infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
          
       if againstSvr == "DstSvr" :
          global dstDbSvrInfoSchemasDataObj;
          infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;

       isDbNameExist = iskeynameExistInDictObj(infoSchemasDataObj, dbName);
       if isDbNameExist == True:
          isTblsAttrOptnDataExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'tblsAttrOptnDataObj');
          if isTblsAttrOptnDataExist == True: 
             isTblNameExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName]['tblsAttrOptnDataObj'], tblName);
             if isTblNameExist == True:
                isDataAvailableInTblStatus = iskeynameExistInDictObj(infoSchemasDataObj[dbName]['tblsAttrOptnDataObj'][tblName], 'isDataAvailableInTbl');
                if isDataAvailableInTblStatus == True:
                   isDataAvailableInTbl = 'Y';

    except Exception as e:
           handleProcsngAbtErrException("Y"); 

    return isDataAvailableInTbl;



### configure db server before checking data available in table ###

def configureDbSvrToCheckDataAvailableInTbl(againstSvr, dbName, tblName):

    isDataAvailableInTbl = 'N';

    try:

        if againstSvr == "SrcSvr" :
           isDataAvailableInTbl = checkDataAvailableInDbTbl('DstSvr', dbName, tblName);
        if againstSvr == "DstSvr" :
           isDataAvailableInTbl = checkDataAvailableInDbTbl('SrcSvr', dbName, tblName);

    except Exception as e:
           handleProcsngAbtErrException("Y"); 

    return isDataAvailableInTbl;



### get status to execute schemas comparsion function ###
### on exist db exist views definition options ###

def isExecuteSchmsCmpOnExistDbViewsDefOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0:
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "8":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-db-views-definition" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0:
                    executionStatus = 'Y'; 
                    if "exist-db-views-definition" in excludeMethodsArr :
                       executionStatus = 'N';
                 else:
                     executionStatus = 'Y';
             
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;


### get status to execute schemas comparsion function ###
### on exist db new views options ###

def isExecuteSchmsCmpOnExistDbNewViewsOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0:
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "8":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-db-new-views" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0:
                    executionStatus = 'Y';   
                    if "exist-db-new-views" in excludeMethodsArr :
                       executionStatus = 'N';
                 else:
                     executionStatus = 'Y';
             
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;



### get status to execute schemas comparsion function ###
### on exist db exist routines definition options ###

def isExecuteSchmsCmpOnExistDbRoutineDefOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0:
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "7":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-db-routines-definition" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0:
                    executionStatus = 'Y';   
                    if "exist-db-routines-definition" in excludeMethodsArr :
                       executionStatus = 'N';
                 else:
                     executionStatus = 'Y';
             
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;


### get status to execute schemas comparsion function ###
### on exist db new routines options ###

def isExecuteSchmsCmpOnExistDbNewRoutineOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0:
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "7":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-db-new-routines" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0:
                    executionStatus = 'Y';  
                    if "exist-db-new-routines" in excludeMethodsArr :
                       executionStatus = 'N';
                 else:
                     executionStatus = 'Y';
             
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;


### get status to execute schemas comparsion function ###
### on exist table exist triggers definition options ###

def isExecuteSchmsCmpOnExistTblTgrDefOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0:
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "6":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbl-tgrs-definition" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0:
                    executionStatus = 'Y'; 
                    if "exist-tbl-tgrs-definition" in excludeMethodsArr :
                       executionStatus = 'N';
                 else:
                     executionStatus = 'Y';
             
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;


### get status to execute schemas comparsion function ###
### on exist table new triggers options ###

def isExecuteSchmsCmpOnExistTblNewTgrOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0:
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "6":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbl-new-tgrs" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0:
                    executionStatus = 'Y';
                    if "exist-tbl-new-tgrs" in excludeMethodsArr :
                       executionStatus = 'N';
                 else:
                     executionStatus = 'Y';
             
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;



### get status to execute schemas comparsion function ###
### on exist table exist foreign key definition options ###

def isExecuteSchmsCmpOnExistTblFKDefOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0:
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "2":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbls" in includeMethodsArr :
                    executionStatus = 'Y'; 
              if cmpCtgryDataObj['cmpCtgryNo'] == "5":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbl-fks-definition" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0:
                    executionStatus = 'Y';
                    if "exist-tbl-fks-definition" in excludeMethodsArr :
                       executionStatus = 'N';
                 else:
                     executionStatus = 'Y';
             
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;


### get status to execute schemas comparsion function ###
### on exist table new foreign key options ###

def isExecuteSchmsCmpOnExistTblNewFKOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0:
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "2":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbls" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "5":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbl-new-fks" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0:
                    executionStatus = 'Y'; 
                    if "exist-tbl-new-fks" in excludeMethodsArr :
                       executionStatus = 'N';
                 else:
                     executionStatus = 'Y';
             
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;



### get status to execute schemas comparsion function ###
### on exist table exist indexes definition options ###

def isExecuteSchmsCmpOnExistTblIndexesDefOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0:
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "2":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbls" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "4":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbl-indx-definition" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0:
                    executionStatus = 'Y';
                    if "exist-tbl-indx-definition" in excludeMethodsArr :
                       executionStatus = 'N';
                 else:
                     executionStatus = 'Y';
             
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;


### get status to execute schemas comparsion function ###
### on exist table new indexes options ###

def isExecuteSchmsCmpOnExistTblNewIndexesOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0:
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "2":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbls" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "4":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbl-new-indexes" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0:
                    executionStatus = 'Y';
                    if "exist-tbl-new-indexes" in excludeMethodsArr :
                       executionStatus = 'N';
                 else:
                     executionStatus = 'Y';
             
    except Exception as e:
           handleProcsngAbtErrException("Y");
  
    return executionStatus;



### get status to execute schemas comparsion function ###
### on exist table exist columns dataType options ###

def isExecuteSchmsCmpOnExistTblColDTypeOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0:
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "2":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbls" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "3":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbl-col-datatype" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0:
                    executionStatus = 'Y';  
                    if "exist-tbl-col-datatype" in excludeMethodsArr :
                       executionStatus = 'N';
                 else:
                     executionStatus = 'Y';
             
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;


### get status to execute schemas comparsion function ###
### on exist table exist columns definitions options ###

def isExecuteSchmsCmpOnExistTblColDefOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0:
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "2":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbls" in includeMethodsArr :
                    executionStatus = 'Y'; 
              if cmpCtgryDataObj['cmpCtgryNo'] == "3":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbl-col-definition" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0:
                    executionStatus = 'Y'; 
                    if "exist-tbl-col-definition" in excludeMethodsArr :
                       executionStatus = 'N';
                 else:
                     executionStatus = 'Y';
             
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;


### get status to execute schemas comparsion function ###
### on exist table new cols options ###

def isExecuteSchmsCmpOnExistTblNewColsOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0:
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "2":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbls" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "3":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbl-new-cols" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0:
                    executionStatus = 'Y';
                    if "exist-tbl-new-cols" in excludeMethodsArr :
                       executionStatus = 'N';
                 else:
                     executionStatus = 'Y';
             
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;


### get status to execute schemas comparsion function ###
### on new tabl options ###

def isExecuteSchmsCmpOnNewTblsOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0 :
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "2":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "new-tbls" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0 : 
                    executionStatus = 'Y'; 
                    if "new-tbls" in excludeMethodsArr :
                       executionStatus = 'N';
                 else:
                     executionStatus = 'Y'; 
             

    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;


### get status to execute schemas comparsion function ###
### on exist tabl options ###

def isExecuteSchmsCmpOnExistTblsOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0 :
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "2":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbls" in includeMethodsArr :
                    executionStatus = 'Y';
             

    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;


### get status to execute schemas comparsion function ###
### on new tbls attributes options ###

def isExecuteSchmsCmpOnNewTblsAttrOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0 :
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "2":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "new-tbls" in includeMethodsArr :
                    executionStatus = 'Y';
              if cmpCtgryDataObj['cmpCtgryNo'] == "9":
                 excludeMethodsArr = cmpCtgryDataObj['excludeMethodsArr'];
                 if len(excludeMethodsArr)>0 :
                    if "new-tbls" not in excludeMethodsArr :
                       executionStatus = 'Y';
                 else:
                     executionStatus = 'Y';  
 

    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;


### get status to execute schemas comparsion function ###
### on exist tbls attributes options ###

def isExecuteSchmsCmpOnExistTblsAttrOptns(inputArgsDataObj):

    executionStatus = 'N';
 
    try:

        if len(inputArgsDataObj)>0 :
           if iskeynameExistInDictObj(inputArgsDataObj, 'cmpCtgryDataObj') == True :
              cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
              if cmpCtgryDataObj['cmpCtgryNo'] == "1":
                 includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];   
                 if "exist-tbls" in includeMethodsArr :
                    executionStatus = 'Y';
              
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return executionStatus;



### store tables colums definition sql query stmt after dependency resolved ###

def storeTblsColsDefAfterDependencyResolvedSqlQry(dbDataObj,dbName,dbTblsColsDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['tblsColsDefChangedStatusDataObj'] = {};
    statusDataObj['cntOfColDefUpdated'] = 0; 

    try:

       if dbName!="" and len(dbTblsColsDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
          for tblName in dbTblsColsDataObj:
              tblAllColsDataObj = dbTblsColsDataObj[tblName];
              tblAllColsDataObjLen = len(tblAllColsDataObj);
              if tblAllColsDataObjLen > 0:
                 statusDataObj['tblsColsDefChangedStatusDataObj'][tblName] = 0;
                 for colName in tblAllColsDataObj:
                     qryStmt = tblAllColsDataObj[colName]['qryStmt'];
                     if qryStmt!="":
                        isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                             againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                        );
                        statusDataObj['tblsColsDefChangedStatusDataObj'][tblName]+= 1;
                        statusDataObj['cntOfColDefUpdated']+= 1;
 

    except Exception as e:
           handleProcsngAbtErrException("Y");

    return statusDataObj;


### get view creation sql query stmt ###

def getViewsCreationSqlQry(dbDataObj, dbName, viewName, viewNameDataArr, againstSvr):
    
    qryStmt = ""; 

    try:

        if dbName!="" and viewName!="" and len(viewNameDataArr)>0 and againstSvr!="":
           
           global inputArgsDataObj;
           uniqInfoSchemaNameArrBtwnSrcAndDstDbSvr = inputArgsDataObj['uniqInfoSchemaNameArrBtwnSrcAndDstDbSvr'];
           searchStrWithReplaceStrDataObj = dict(('`'+element+'`.', dbName) for element in uniqInfoSchemaNameArrBtwnSrcAndDstDbSvr);
  
           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];

           refViewDbName = viewNameDataArr[0];
           viewDefinitionStmt = viewNameDataArr[2];
 
           if viewDefinitionStmt!="" :
              
              viewWordIndx = viewDefinitionStmt.find("VIEW");
              viewSubpartQry =  viewDefinitionStmt[viewWordIndx: len(viewDefinitionStmt)];
              redefinedViewQry = "CREATE ALGORITHM=UNDEFINED DEFINER=" + "`" + dbUSER + "`";
              redefinedViewQry+=  "@"+"`%`" + " "; 
              redefinedViewQry+=  viewSubpartQry;
              redefinedViewQry = searchStrAndReplaceStr(redefinedViewQry, searchStrWithReplaceStrDataObj);

              dropViewQry = "DROP VIEW IF EXISTS " + dbName + "." + "`" + viewName + "`" + ";" + "\n";   
              createViewQryStmt = "DELIMITER // " + "\n" + redefinedViewQry + "\n" + " // " + "\n" + " DELIMITER ;";
              qryStmt = dropViewQry + createViewQryStmt;
              
    except Exception as e:
           handleProcsngAbtErrException("Y");  

    return qryStmt;



### store all views creations sql query stmt ###

def storeViewsCreationSqlQry(dbDataObj, dbName,dbViewsDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {}; 
    statusDataObj['cntOfViewsCreation'] = 0;

    try:

        if dbName!="" and len(dbViewsDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="" :
       
           for eachViewName in dbViewsDataObj:
               updatedViewData = dbViewsDataObj[eachViewName]['updatedViewData'];
               qryStmt = getViewsCreationSqlQry(dbDataObj, dbName, eachViewName, updatedViewData, againstSvr);
               if qryStmt!="":
                  isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                       againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                  );
                  statusDataObj['cntOfViewsCreation']+= 1;

    except Exception as e:
           handleProcsngAbtErrException("Y"); 

    return statusDataObj;


### store to dropping all views sql query stmt ###

def storeToDropViewsSqlQry(dbDataObj, dbName,dbViewsDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['cntOfViewsDropped'] = 0;

    try:

        if dbName!="" and len(dbViewsDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
           for eachViewName in dbViewsDataObj:
               qryStmt = "DROP VIEW IF EXISTS " + dbName + "." + "`" + eachViewName + "`" + ";";
               if qryStmt!="":
                  isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                       againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                  );
                  statusDataObj['cntOfViewsDropped']+= 1;

    except Exception as e:
           handleProcsngAbtErrException("Y"); 

    return statusDataObj;



### get routine creation sql query stmt ###

def getRoutineCreationSqlQry(dbDataObj, dbName, routineType, routineName, routineNameDataArr, againstSvr):
    
    qryStmt = ""; 

    try:

        if dbName!="" and routineType!="" and routineName!="" and len(routineNameDataArr)>0 and againstSvr!="":
       
           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER']; 

           routineDefinitionStmt = routineNameDataArr[3];
           if routineDefinitionStmt!="":
              
              routineTypeWordIndx = routineDefinitionStmt.find(routineType);
              routineSubpartQry =  routineDefinitionStmt[routineTypeWordIndx: len(routineDefinitionStmt)];
              redefinedRoutineQry = "CREATE DEFINER=" + "`" + dbUSER + "`";
              redefinedRoutineQry+=  "@"+"`%`" + " "; 
              redefinedRoutineQry+=  routineSubpartQry;

              dropRoutineQryStmt = "DROP " + routineType + " IF EXISTS";
              dropRoutineQryStmt+= " " + dbName + "." + "`" + routineName + "`" + ";" + "\n"; 
              createRoutineQryStmt = "DELIMITER // " + "\n" + redefinedRoutineQry + "\n" + " // " + "\n" + " DELIMITER ;";
              qryStmt = dropRoutineQryStmt + createRoutineQryStmt; 

    except Exception as e:
           handleProcsngAbtErrException("Y"); 

    return qryStmt;



### store all routine creation sql query stmt ###

def storeRoutineCreationSqlQry(dbDataObj, dbName,dbRoutinesDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['cntOfRoutinesCreation'] = 0;

    try:

        if dbName!="" and len(dbRoutinesDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
           for eachRoutineType in dbRoutinesDataObj:
               eachRtypeAllRoutinesDataObj = dbRoutinesDataObj[eachRoutineType]['rTypeAllRoutineNames'];
               eachRtypeAllRoutinesDataObjLen = len(eachRtypeAllRoutinesDataObj);
               if eachRtypeAllRoutinesDataObjLen > 0:
                  for eachRoutineName in eachRtypeAllRoutinesDataObj:
                      updatedRnameData = eachRtypeAllRoutinesDataObj[eachRoutineName]['updatedRnameData'];
                      qryStmt = getRoutineCreationSqlQry(dbDataObj, dbName, eachRoutineType, eachRoutineName, updatedRnameData, againstSvr);
                      if qryStmt!="":
                         isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                              againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                         );
                         statusDataObj['cntOfRoutinesCreation']+= 1; 

    except Exception as e:
           handleProcsngAbtErrException("Y");  

    return statusDataObj;


### store to dropping all routine sql query stmt ###

def storeToDropRoutinesSqlQry(dbDataObj, dbName,dbRoutinesDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['cntOfRoutinesDropped'] = 0;

    try:

        if dbName!="" and len(dbRoutinesDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
           for eachRoutineType in dbRoutinesDataObj:
               eachRtypeAllRoutinesDataObj = dbRoutinesDataObj[eachRoutineType]['rTypeAllRoutineNames'];
               eachRtypeAllRoutinesDataObjLen = len(eachRtypeAllRoutinesDataObj);
               if eachRtypeAllRoutinesDataObjLen > 0:
                  for eachRoutineName in eachRtypeAllRoutinesDataObj:
                      qryStmt = "DROP " + eachRoutineType + " IF EXISTS";
                      qryStmt+= " " + dbName + "." + "`" + eachRoutineName + "`" + ";";
                      if qryStmt!="":
                         isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                              againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                         );
                         statusDataObj['cntOfRoutinesDropped']+= 1;
          
    except Exception as e:
           handleProcsngAbtErrException("Y");  

    return statusDataObj;



### get table trigger creation sql query stmt ###

def getTblTgrCreationSqlQry(dbDataObj, dbName, tblName, tgrName, tgrNameDataArr, againstSvr):
    
    qryStmt = ""; 

    try:

        if dbName!="" and tblName!="" and tgrName!="" and len(tgrNameDataArr)>0 and againstSvr!="":
       
           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];

           refTgrDbName = tgrNameDataArr[0];
           tgrDefinitionStmt = tgrNameDataArr[5];
           if tgrDefinitionStmt!="":
          
              tgrWordIndx = tgrDefinitionStmt.find("TRIGGER");
              tgrSubpartQry =  tgrDefinitionStmt[tgrWordIndx: len(tgrDefinitionStmt)];
              tgrSubpartQry = tgrSubpartQry.replace(refTgrDbName, dbName);
              redefinedTgrQry = "CREATE DEFINER=" + "`" + dbUSER + "`";
              redefinedTgrQry+= "@"+"`%`" + " "; 
              redefinedTgrQry+= tgrSubpartQry;
   
              dropTgrQryStmt = "DROP TRIGGER IF EXISTS " + dbName + "." + "`" + tgrName + "`" + ";" + "\n"; 
              createTgrQryStmt = "DELIMITER // " + "\n" + redefinedTgrQry + "\n" + " // " + "\n" + " DELIMITER ;";
              qryStmt = dropTgrQryStmt + createTgrQryStmt;
          
    except Exception as e:
           handleProcsngAbtErrException("Y");  

    return qryStmt;
  


### store tables all trigger creation sql query stmt ###

def storeTblsTriggersCreationSqlQry(dbDataObj,dbName,dbTblsTgrsDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['tblsTgrsCreationStatusDataObj'] = {};
    statusDataObj['cntOfTgrsCreation'] = 0;
 
    try:

        if dbName!="" and len(dbTblsTgrsDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
           for eachTblName in dbTblsTgrsDataObj:
               eachTblAllTgrsDataObj = dbTblsTgrsDataObj[eachTblName];
               eachTblAllTgrsDataObjLen = len(eachTblAllTgrsDataObj);
               if eachTblAllTgrsDataObjLen > 0:
                  statusDataObj['tblsTgrsCreationStatusDataObj'][eachTblName] = 0;
                  for eachTgrName in eachTblAllTgrsDataObj:
                      updatedTgrNameData = eachTblAllTgrsDataObj[eachTgrName]['updatedTgrNameData'];
                      qryStmt = getTblTgrCreationSqlQry(dbDataObj, dbName, eachTblName, eachTgrName, updatedTgrNameData, againstSvr);
                      if qryStmt!="":
                         isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                              againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                         );
                         statusDataObj['tblsTgrsCreationStatusDataObj'][eachTblName]+= 1;
                         statusDataObj['cntOfTgrsCreation']+= 1; 

    except Exception as e:
           handleProcsngAbtErrException("Y");  

    return statusDataObj;



### store to dropping tables all triggers sql query stmt ###

def storeToDropTblsTgrsSqlQry(dbDataObj,dbName,dbTblsTgrsDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['tblsTgrsDroppedStatusDataObj'] = {};
    statusDataObj['cntOfTgrsDropped'] = 0;

    try:

        if dbName!="" and len(dbTblsTgrsDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
           for eachTblName in dbTblsTgrsDataObj:
               eachTblAllTgrsDataObj = dbTblsTgrsDataObj[eachTblName];
               eachTblAllTgrsDataObjLen = len(eachTblAllTgrsDataObj);
               if eachTblAllTgrsDataObjLen > 0:
                  statusDataObj['tblsTgrsDroppedStatusDataObj'][eachTblName] = 0; 
                  for eachTgrName in eachTblAllTgrsDataObj:
                      qryStmt = "DROP TRIGGER IF EXISTS " + dbName + "." + "`" + eachTgrName + "`" + ";";
                      if qryStmt!="":
                         isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                              againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                         );
                         statusDataObj['tblsTgrsDroppedStatusDataObj'][eachTblName]+= 1;
                         statusDataObj['cntOfTgrsDropped']+= 1;
 
    except Exception as e:
           handleProcsngAbtErrException("Y");  

    return statusDataObj;



### get fkName constraints creation sql query stmt ###

def getFKNameColConstraintsCreationSqlQry(dbDataObj, dbName, tblName, FKName, FKNameAllColsDataObj):

    qryStmt = ""; 

    try:

        if dbName!="" and tblName!="" and FKName!="" and len(FKNameAllColsDataObj)>0:

           FKAsNFKColNamesArr = [];
           FKColNamesArr = [];
           FKAsNFKColsSequenceDataObj = {};    
           FKColsSequenceDataObj = {};
           refFKTblName = "";
           onDeleteFkNameRuleStr = "ON DELETE NO ACTION";
           onUpdateFkNameRuleStr = "ON UPDATE NO ACTION ";
            
           for eachColName in FKNameAllColsDataObj:

               colDataArr = FKNameAllColsDataObj[eachColName]['updatedFKColNameData'];              
               colSequenceNo = colDataArr[7];
               FKAsNFKColSequenceName = colDataArr[2];
               FKColSequenceName = colDataArr[6];
               refFKTblName = colDataArr[1];
               onUpdateFkNameRuleStr = "ON UPDATE " + colDataArr[8];
               onDeleteFkNameRuleStr = "ON DELETE " + colDataArr[9];
 
               isFKAsNFKColSequenceNoExist = iskeynameExistInDictObj(FKAsNFKColsSequenceDataObj, colSequenceNo);
               if isFKAsNFKColSequenceNoExist == False : 
                  FKAsNFKColsSequenceDataObj[colSequenceNo] = [FKAsNFKColSequenceName];
               else:
                   FKAsNFKColsSequenceDataObj[colSequenceNo].append(FKAsNFKColSequenceName);

               isFKColSequenceNoExist = iskeynameExistInDictObj(FKColsSequenceDataObj, colSequenceNo);
               if isFKColSequenceNoExist == False : 
                  FKColsSequenceDataObj[colSequenceNo] = [FKColSequenceName];
               else:
                   FKColsSequenceDataObj[colSequenceNo].append(FKColSequenceName);   


           if len(FKColsSequenceDataObj)>0:
              FKColSequenceNoList = list(FKColsSequenceDataObj.keys());
              FKColSequenceNoList.sort();
              for sequenceNo in FKColSequenceNoList:
                  FKAsNFKColNamesArr.extend(FKAsNFKColsSequenceDataObj[sequenceNo]);    
                  FKColNamesArr.extend(FKColsSequenceDataObj[sequenceNo]);

           if len(FKColNamesArr)>0:
              
              dropFKQryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`";
              dropFKQryStmt+= " DROP FOREIGN KEY " + "`" + FKName + "`" + " ; ";

              createFKQryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`" ;
              createFKQryStmt+= " ADD CONSTRAINT " + "`" +  FKName + "`";
              createFKQryStmt+= " FOREIGN KEY " + "("+ ','.join(FKColNamesArr) + ")";
              createFKQryStmt+= " REFERENCES " + "`" + refFKTblName + "`";
              createFKQryStmt+= " (" + ','.join(FKAsNFKColNamesArr) + ")";
              createFKQryStmt+= " " + onDeleteFkNameRuleStr + " " + onUpdateFkNameRuleStr + " ;";

              qryStmt = dropFKQryStmt + "\n" + createFKQryStmt + "\n";

    except Exception as e:
           handleProcsngAbtErrException("Y");  

    return qryStmt;



### store tables all new constraints name creation sql query stmt ###

def storeTblsFkNameColsConstraintsSqlQry(dbDataObj,dbName,dbTblsConstraintsDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['tblsFKCreationStatusDataObj'] = {};
    statusDataObj['cntOfFKCreation'] = 0;
  
    try:

        if dbName!="" and len(dbTblsConstraintsDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
           for eachTblName in dbTblsConstraintsDataObj:
               eachTblsAllFkNameConstraintsDataObj = dbTblsConstraintsDataObj[eachTblName];
               eachTblsAllFkNameConstraintsDataObjLen = len(eachTblsAllFkNameConstraintsDataObj);
               if eachTblsAllFkNameConstraintsDataObjLen > 0:
                  statusDataObj['tblsFKCreationStatusDataObj'][eachTblName] = 0;
                  for eachTblEachFKName in eachTblsAllFkNameConstraintsDataObj:
                      eachFKNameAllColsDataObj = eachTblsAllFkNameConstraintsDataObj[eachTblEachFKName]['fkAllCols'];
                      qryStmt = getFKNameColConstraintsCreationSqlQry(
                         dbDataObj, dbName, eachTblName, eachTblEachFKName, eachFKNameAllColsDataObj
                      );
                      if qryStmt!="":
                         isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                              againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                         );
                         statusDataObj['tblsFKCreationStatusDataObj'][eachTblName]+= 1; 
                         statusDataObj['cntOfFKCreation']+= 1; 

    except Exception as e:
           handleProcsngAbtErrException("Y");  

    return statusDataObj;



### store to drop table foreign key constraints sql query stmt ###

def storeToDropTblsFkConstraintSqlQry(dbDataObj,dbName,dbTblsConstraintsDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['tblsFKDroppedStatusDataObj'] = {};
    statusDataObj['cntOfFKDropped'] = 0;

    try:

        if dbName!="" and len(dbTblsConstraintsDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
           for eachTblName in dbTblsConstraintsDataObj:
               eachTblsAllFkNameConstraintsDataObj = dbTblsConstraintsDataObj[eachTblName];
               eachTblsAllFkNameConstraintsDataObjLen = len(eachTblsAllFkNameConstraintsDataObj);
               if eachTblsAllFkNameConstraintsDataObjLen > 0:
                  statusDataObj['tblsFKDroppedStatusDataObj'][eachTblName] = 0;
                  for eachTblEachFKName in eachTblsAllFkNameConstraintsDataObj:
                      qryStmt = "ALTER TABLE " + dbName + "." + "`" + eachTblName + "`";
                      qryStmt+= " DROP FOREIGN KEY " + "`" + eachTblEachFKName + "`" + ";";
                      if qryStmt!="":
                         isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                              againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                         );
                         statusDataObj['tblsFKDroppedStatusDataObj'][eachTblName]+= 1;
                         statusDataObj['cntOfFKDropped']+= 1;
             

    except Exception as e:
           handleProcsngAbtErrException("Y");  

    return statusDataObj;



### get important restrictions content for table indexes ###

def getImpRestrictionsContentB4ExecutingTblIndexChanges(tblDataQryStmt, indxQryStmt):

    impRestrictionsContentStr = "";

    try:
       
       if tblDataQryStmt!="" and indxQryStmt!="" :

          impRestrictionsContentStr = "/*" + "\n" + "\n";
          impRestrictionsContentStr+= "Step1 : Remove / Sort-out data from table before adding index" + "\n";
          impRestrictionsContentStr+= "Step2: Execute given below query to remove / sort-out data from table" + "\n";
          impRestrictionsContentStr+= tblDataQryStmt + "\n"; 
          impRestrictionsContentStr+= "Step3: Execute given below query OR execute again difffDB.py script for DB comparsion." + "\n";  
          impRestrictionsContentStr+= indxQryStmt + "\n";
          impRestrictionsContentStr+= "*/"; 
          impRestrictionsContentStr = impRestrictionsContentStr.strip();
  
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return impRestrictionsContentStr;  


### get query stmt to find duplicate data based on given cols ###

def getQryStmtToFindDupDataBasedOnGivenTblColsBeforeAddingIndx(dbName, tblName, tblAllColNamesArr):

    qryStmt = '';

    try:

       if dbName!='' and tblName!='' and len(tblAllColNamesArr)>0:

          tblAllColNamesStr = ','.join(tblAllColNamesArr);
          orderByClauseStmtStrArr = [];
          joinOnClauseStmtStrArr = [];
          for colName in tblAllColNamesArr:
              orderByClauseStmtStr = "oData" + "." + colName;
              joinOnClauseStmtStr = "dData" + "." + colName + "=" + "oData" + "." + colName;
              orderByClauseStmtStrArr.append(orderByClauseStmtStr);
              joinOnClauseStmtStrArr.append(joinOnClauseStmtStr);
          
          orderByClauseStmtStr = ','.join(orderByClauseStmtStrArr);
          joinOnClauseStmtStr = ' AND '.join(joinOnClauseStmtStrArr);

          qryStmt+= """SELECT
                       oData.*
                       FROM {dbName}.{tblName} oData
                       JOIN (
                             SELECT
                             {tblAllColNamesStr}, COUNT(*) cntOfDupData
                             FROM {dbName}.{tblName}
                             WHERE 1
                             GROUP BY {tblAllColNamesStr}
                             HAVING cntOfDupData>1
                       ) dData ON {joinOnClauseStmtStr}
                       WHERE 1
                       ORDER BY {orderByClauseStmtStr}""".format(dbName = dbName, tblName = tblName, tblAllColNamesStr = tblAllColNamesStr, orderByClauseStmtStr = orderByClauseStmtStr, joinOnClauseStmtStr = joinOnClauseStmtStr);
 
          qryStmt = qryStmt.strip();

    except Exception as e:
           handleProcsngAbtErrException("Y");

    return qryStmt;


### is new shcemas exist in index all cols ###

def isNewSchemasExistInIndexSchemasData(indxAllColsDataObj):

    isNewSchemas = 'N';

    try:
      
        for eachColName in indxAllColsDataObj:
            isNewSchemasKeyExist = iskeynameExistInDictObj(indxAllColsDataObj[eachColName], 'isNewSchemas');
            if isNewSchemasKeyExist == True : 
               isNewSchemas = indxAllColsDataObj[eachColName]['isNewSchemas'];              
               if isNewSchemas == "Y" :
                  break;
 

    except Exception as e:
           handleProcsngAbtErrException("Y");

    return isNewSchemas;


### get table index all col names sequence wise for helping indexing sql smt ###

def getTblIndexAllColsSequencewise(indxAllColsDataObj):

    indexAllColNamesArr = [];

    try:
  
        colsSequenceForIndexDataObj = {};
            
        for eachColName in indxAllColsDataObj:  
            colDataArr = indxAllColsDataObj[eachColName]['updatedIndxColData'];              
            colSequenceNo = colDataArr[5];
            colSequenceName = colDataArr[6];
            colSequenceNameSubpart = colDataArr[9];
            if colSequenceNameSubpart !="" :
               colSequenceName = colSequenceName + " (" + colSequenceNameSubpart + ")"; 
            isColSequenceNoExist = iskeynameExistInDictObj(colsSequenceForIndexDataObj, colSequenceNo);
            if isColSequenceNoExist == False : 
               colsSequenceForIndexDataObj[colSequenceNo] = [colSequenceName];
            else:
                colsSequenceForIndexDataObj[colSequenceNo].append(colSequenceName);   
 
        if len(colsSequenceForIndexDataObj)>0:
           colSequenceNoList = list(colsSequenceForIndexDataObj.keys());
           colSequenceNoList.sort();
           for sequenceNo in colSequenceNoList:
               indexAllColNamesArr.extend(colsSequenceForIndexDataObj[sequenceNo]);       


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return indexAllColNamesArr;



### get table index creation sql query stmt ###

def getTblIndexCreationSqlQry(dbDataObj, dbName, tblName, indxName, indxType, indxAllColsDataObj):

    qryStmt = ""; 

    try:

        if dbName!="" and tblName!="" and indxName!="" and len(indxAllColsDataObj)>0:

           indexAllColNamesArr = getTblIndexAllColsSequencewise(indxAllColsDataObj);

           if len(indexAllColNamesArr)>0:
              
              ### handle case for primary key indexes 

              if indxName == "PRIMARY" :  
                 qryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`" ;
                 qryStmt+= " ADD PRIMARY KEY (" + ','.join(indexAllColNamesArr) + ")" + ";" + "\n";

              ### handle case for unique key indexes 

              if indxName != "PRIMARY" and indxType == "UNIQUE" :  
                 qryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`" ;
                 qryStmt+= " ADD UNIQUE KEY " + "`" + indxName + "`" + " (" + ','.join(indexAllColNamesArr) + ")" + ";" + "\n";  

              ### handle case only key indexes 

              if indxName != "PRIMARY" and indxType != "UNIQUE" :  
                 qryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`" ;
                 qryStmt+= " ADD KEY " + "`" + indxName + "`" + " (" + ','.join(indexAllColNamesArr) + ")" + ";" + "\n";   


    except Exception as e:
           handleProcsngAbtErrException("Y");  

    return qryStmt;



### check table index limitation before implementing changes ###

def checkTblIndxLimitationB4ImplementingChanges(dbDataObj,dbName,tblName,indxName,indxType,indxAllColsDataObj,isDataAvailableInTbl,againstSvr):

    statusDataObj = {};
    statusDataObj['isDependencyExist'] = 'N';
    statusDataObj['isRestrictionExist'] = 'N';  
    statusDataObj['impRestrictionsContentStr'] = '';
    statusDataObj['dependsOnArr'] = [];
        
    try:

        if dbName!="" and len(tblName)>0 and indxName!="" and indxType!="" and len(indxAllColsDataObj)>0 :

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

           if isDataAvailableInTbl == 'Y' :

              if indxType == "UNIQUE" :
    
                 isTblDuplicateDataExist = 'N';
 
                 isNewSchemasExist = isNewSchemasExistInIndexSchemasData(indxAllColsDataObj);
                 if isNewSchemasExist == "N" :
                    tblIndxAllColsSequencewiseArr = getTblIndexAllColsSequencewise(indxAllColsDataObj);
                    dupDataQryStmt = getQryStmtToFindDupDataBasedOnGivenTblColsBeforeAddingIndx(
                         dbName, tblName, tblIndxAllColsSequencewiseArr
                    );
                    if dupDataQryStmt!="":
                       dataArrOfArr = fetchDataFromDB(dbHOST, dbPORTNO, dbUSER, dbPASS, dbName, dupDataQryStmt);  
                       if len(dataArrOfArr)>0:
                          isTblDuplicateDataExist = 'Y'; 

                 if isTblDuplicateDataExist == 'Y':  
                    dropIndxQryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`" ;
                    dropIndxQryStmt+= " DROP INDEX " + "`" + indxName + "`" + ";" + "\n";
                    indxQryStmt = getTblIndexCreationSqlQry(dbDataObj, dbName, tblName, indxName, indxType, indxAllColsDataObj);
                    indxQryStmt = dropIndxQryStmt + indxQryStmt;
                    impRestrictionsContentStr = getImpRestrictionsContentB4ExecutingTblIndexChanges(dupDataQryStmt, indxQryStmt);
                    if impRestrictionsContentStr!="":
                       statusDataObj['isRestrictionExist'] = 'Y';  
                       statusDataObj['impRestrictionsContentStr'] = impRestrictionsContentStr;          
        

    except Exception as e:
           handleProcsngAbtErrException("Y");

    return statusDataObj;


### store tables index with all updation sql query stmt ###

def storeTblsIndexUpdationSqlQry(dbDataObj,dbName,dbTblsIndxDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['tblsIndxsCreationStatusDataObj'] = {};
    statusDataObj['cntOfIndxCreation'] = 0;
 
    try:

        if dbName!="" and len(dbTblsIndxDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
           for tblName in dbTblsIndxDataObj:
               allIndexesDataObj = dbTblsIndxDataObj[tblName];
               allIndexesDataObjLen = len(allIndexesDataObj);
               if allIndexesDataObjLen > 0:
                  statusDataObj['tblsIndxsCreationStatusDataObj'][tblName] = 0;
                  for indxName in allIndexesDataObj:

                      isDataAvailableInTbl = 'N';
                      isDataAvailableInTblKeyExist = iskeynameExistInDictObj(allIndexesDataObj[indxName], 'isDataAvailableInTbl');
                      if isDataAvailableInTblKeyExist == True:
                         isDataAvailableInTbl = allIndexesDataObj[indxName]['isDataAvailableInTbl'];

                      indxType = allIndexesDataObj[indxName]['dbTblIndxType'];
                      indxAllColsDataObj = allIndexesDataObj[indxName]['indxAllCols'];
                      isIndxUpdationQryCanStore = 'Y';
          
                      if isDataAvailableInTbl == 'Y' :
                         indxLimitationStatusDataObj = checkTblIndxLimitationB4ImplementingChanges(
                              dbDataObj, dbName, tblName, indxName, indxType, indxAllColsDataObj, isDataAvailableInTbl, againstSvr
                         );
                         if indxLimitationStatusDataObj['isRestrictionExist'] == "Y" :
                            impRestrictionsContentStr = indxLimitationStatusDataObj['impRestrictionsContentStr'];
                            isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                                 againstSvr, dbName, 'importantRestrictions', impRestrictionsContentStr, 'N'
                            );
                            
                      if isIndxUpdationQryCanStore == 'Y' :
                         indxQryStmt = getTblIndexCreationSqlQry(
                             dbDataObj, dbName, tblName, indxName, indxType, indxAllColsDataObj
                         );
                         if indxQryStmt!="":
                            dropIndxQryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`" ;
                            dropIndxQryStmt+= " DROP INDEX " + "`" + indxName + "`" + ";" + "\n";
                            qryStmt = dropIndxQryStmt + indxQryStmt;
                            isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                                 againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                            );
                            statusDataObj['tblsIndxsCreationStatusDataObj'][tblName]+= 1;
                            statusDataObj['cntOfIndxCreation']+= 1;


    except Exception as e:
           handleProcsngAbtErrException("Y"); 

    return statusDataObj;



### store tables all new index creation sql query stmt ###

def storeTblsIndexesCreationSqlQry(dbDataObj,dbName,dbTblsIndxDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['tblsIndxsCreationStatusDataObj'] = {};
    statusDataObj['cntOfIndxCreation'] = 0;
 
    try:

        if dbName!="" and len(dbTblsIndxDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
           for tblName in dbTblsIndxDataObj:
               allIndexesDataObj = dbTblsIndxDataObj[tblName];
               allIndexesDataObjLen = len(allIndexesDataObj);
               if allIndexesDataObjLen > 0:
                  statusDataObj['tblsIndxsCreationStatusDataObj'][tblName] = 0;
                  for indxName in allIndexesDataObj:

                      isDataAvailableInTbl = 'N';
                      isDataAvailableInTblKeyExist = iskeynameExistInDictObj(allIndexesDataObj[indxName], 'isDataAvailableInTbl');
                      if isDataAvailableInTblKeyExist == True:
                         isDataAvailableInTbl = allIndexesDataObj[indxName]['isDataAvailableInTbl'];

                      indxType = allIndexesDataObj[indxName]['dbTblIndxType'];
                      indxAllColsDataObj = allIndexesDataObj[indxName]['indxAllCols'];
                      isIndxCreationQryCanStore = 'Y';
 
                      if isDataAvailableInTbl == 'Y' :

                         indxLimitationStatusDataObj = checkTblIndxLimitationB4ImplementingChanges(
                              dbDataObj, dbName, tblName, indxName, indxType, indxAllColsDataObj, isDataAvailableInTbl, againstSvr
                         );
                         if indxLimitationStatusDataObj['isRestrictionExist'] == "Y" :
                            isIndxCreationQryCanStore = 'N'; 
                            impRestrictionsContentStr = indxLimitationStatusDataObj['impRestrictionsContentStr'];
                            isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                                 againstSvr, dbName, 'importantRestrictions', impRestrictionsContentStr, 'N'
                            );
                               
                      if isIndxCreationQryCanStore == 'Y' :
                         qryStmt = getTblIndexCreationSqlQry(
                             dbDataObj, dbName, tblName, indxName, indxType, indxAllColsDataObj
                         );
                         if qryStmt!="":
                            isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                                 againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                            );
                            statusDataObj['tblsIndxsCreationStatusDataObj'][tblName]+= 1;
                            statusDataObj['cntOfIndxCreation']+= 1;
         

    except Exception as e:
           handleProcsngAbtErrException("Y");  

    return statusDataObj;



### store to dropping tables indexes sql query stmt ###

def storeToDropTblsIndexesSqlQry(dbDataObj,dbName,dbTblsIndxDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['tblsIndxsDroppedStatusDataObj'] = {};
    statusDataObj['cntOfIndxDropped'] = 0;

    try:

        if dbName!="" and len(dbTblsIndxDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
           for tblName in dbTblsIndxDataObj:
               allIndexesDataObj = dbTblsIndxDataObj[tblName];
               allIndexesDataObjLen = len(allIndexesDataObj);
               if allIndexesDataObjLen > 0:
                  statusDataObj['tblsIndxsDroppedStatusDataObj'][tblName] = 0;
                  for indxName in allIndexesDataObj:
                      qryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`" + " DROP INDEX " + "`" + indxName + "`" + ";";
                      if qryStmt!="":
                         isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                              againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                         );
                         statusDataObj['tblsIndxsDroppedStatusDataObj'][tblName]+= 1;
                         statusDataObj['cntOfIndxDropped']+= 1;


    except Exception as e:
           handleProcsngAbtErrException("Y");  

    return statusDataObj;



### check table column limitation before implementing any changes ###

def checkTblColLimitationB4ImplementingChanges(dbDataObj, dbName, tblName, isDataAvailableInTbl, colName, colDataObj, againstSvr):

    statusDataObj = {};
    statusDataObj['isDependencyExist'] = 'N';
    statusDataObj['isRestrictionExist'] = 'N';  
    statusDataObj['impRestrictionsContentStr'] = '';
    statusDataObj['dependsOnArr'] = [];
        
    try:

        if dbName!="" and tblName!="" and colName!="" and len(colDataObj)>0 and isDataAvailableInTbl!="" :

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];
   
           colDataArr = colDataObj['updatedColData'];
           colDataType = colDataArr[3];
           colDefaultValStr = colDataArr[5];
           colExtraKeyStr = colDataArr[6]; 
           colKeyConstraintStr = colDataArr[9];
           
           ### Case1.1 unique key with auto increment ###

           if colKeyConstraintStr == "UNI" and colExtraKeyStr == "auto_increment" :

              tblIndexesDataObj = {};
              tblIndxDataObj = {};
           
              isTblExist1 = iskeynameExistInDictObj(dbDataObj['dbNFKTblIndxCreationDataObj'], tblName);
              isTblExist2 = iskeynameExistInDictObj(dbDataObj['dbNFKTblIndxUpdationDataObj'], tblName);
              isTblExist3 = iskeynameExistInDictObj(dbDataObj['dbFKAsNFKTblsIndxCreationDataObj'], tblName);
              isTblExist4 = iskeynameExistInDictObj(dbDataObj['dbFKAsNFKTblIndxUpdationDataObj'], tblName);
              isTblExist5 = iskeynameExistInDictObj(dbDataObj['dbFKTblsIndxCreationDataObj'], tblName);
              isTblExist6 = iskeynameExistInDictObj(dbDataObj['dbFkTblIndxUpdationDataObj'], tblName);
  
              if isTblExist1 == True :
                 tblIndexesDataObj = dbDataObj['dbNFKTblIndxCreationDataObj'][tblName];
              elif isTblExist2 == True :
                  tblIndexesDataObj = dbDataObj['dbNFKTblIndxUpdationDataObj'][tblName];
              elif isTblExist3 == True :
                  tblIndexesDataObj = dbDataObj['dbFKAsNFKTblsIndxCreationDataObj'][tblName];
              elif isTblExist4 == True :
                  tblIndexesDataObj = dbDataObj['dbFKAsNFKTblIndxUpdationDataObj'][tblName];
              elif isTblExist5 == True :
                  tblIndexesDataObj = dbDataObj['dbFKTblsIndxCreationDataObj'][tblName];
              elif isTblExist6 == True :
                  tblIndexesDataObj = dbDataObj['dbFkTblIndxUpdationDataObj'][tblName]; 
          
              if len(tblIndexesDataObj)>0 :
                 for indxName in tblIndexesDataObj:
                     indxColsDataObj = tblIndexesDataObj[indxName]['indxAllCols'];
                     isTblColExist = iskeynameExistInDictObj(indxColsDataObj, colName);
                     if isTblColExist == True :
                        tblIndxDataObj[indxName] = tblIndexesDataObj[indxName];

              if len(tblIndxDataObj)>0:

                 for indxName in tblIndxDataObj:

                     indxType = tblIndxDataObj[indxName]['dbTblIndxType'];
                     indxColsDataObj = tblIndxDataObj[indxName]['indxAllCols'];

                     ### Case1.1 table data is available ###
               
                     if isDataAvailableInTbl == 'Y' :

                        if indxType == "UNIQUE" :

                           isTblDuplicateDataExist = 'N';
                               
                           isNewSchemasExist = isNewSchemasExistInIndexSchemasData(indxColsDataObj);
                           if isNewSchemasExist == "N" :                
                              tblIndxAllColsSequencewiseArr = getTblIndexAllColsSequencewise(indxColsDataObj);
                              dupDataQryStmt = getQryStmtToFindDupDataBasedOnGivenTblColsBeforeAddingIndx(
                                 dbName, tblName, tblIndxAllColsSequencewiseArr
                              );
                              if dupDataQryStmt!="":
                                 dataArrOfArr = fetchDataFromDB(
                                     dbHOST, dbPORTNO, dbUSER, dbPASS, dbName, dupDataQryStmt
                                 ); 
                                 if len(dataArrOfArr)>0:
                                    isTblDuplicateDataExist = 'Y';

                           if isTblDuplicateDataExist == 'Y' :
                              indxQryStmt = getTblIndexCreationSqlQry(
                                  dbDataObj, dbName, tblName, indxName, indxType, indxColsDataObj
                              );
                              impRestrictionsContentStr = getImpRestrictionsContentB4ExecutingTblIndexChanges(dupDataQryStmt,indxQryStmt);
                              if impRestrictionsContentStr!="":
                                 statusDataObj['isRestrictionExist'] = 'Y';  
                                 statusDataObj['impRestrictionsContentStr'] = impRestrictionsContentStr;
                              
                           else :
                                statusDataObj['isDependencyExist'] = 'Y';
                                statusDataObj['dependsOnArr'].extend("index");

                     
                     ### Case1.2 table data is not available ###
  
                     if isDataAvailableInTbl == 'N' :
                            
                        if indxType == "UNIQUE" :
                       
                           statusDataObj['isDependencyExist'] = 'Y';
                           statusDataObj['dependsOnArr'].extend("index");
                         


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return statusDataObj;



### get tbl column creation sql query stmt ###

def getTblColCreationSqlQry(dbDataObj, dbName, tblName, isDataAvailableInTbl, colName, colDataObj, againstSvr):

    statusDataObj = {};
    statusDataObj['qryStmt'] = "";
    statusDataObj['updateColDefAfterDependencyResolvedDataObj'] = "";
    statusDataObj['impRestrictionsContentStr'] = "";
 
    try:

        if dbName!="" and tblName!="" and colName!="" and len(colDataObj)>0:

           global toStoreTempSqlFileDirPath;
           
           colDataArr = colDataObj['updatedColData'];
           colExtraKeyStr = colDataArr[6];
           colKeyConstraintStr = colDataArr[9];
           updatedColConfig = colDataObj['updatedColConfig'];
           refDbHost = updatedColConfig['dbHOST'];
           refDbPORTNO = updatedColConfig['dbPORTNO'];
           refDbUser = updatedColConfig['dbUSER'];
           refDbPwd = updatedColConfig['dbPASS']; 
           refDbName = colDataArr[0];
           refTblStructureQry = "SHOW CREATE TABLE " + refDbName + "." + tblName + ";";
           refTblStructureDataArr = fetchDataFromDB(refDbHost, refDbPORTNO, refDbUser, refDbPwd, refDbName, refTblStructureQry);
           if len(refTblStructureDataArr)>0:
              filenameWithPathStr = toStoreTempSqlFileDirPath + "diffDbTemp.sql";
              fileObj = open(filenameWithPathStr, "w+");
              fileObj.write(getConvertedStrIntoBytesToWriteIntoFileObj(refTblStructureDataArr[0][1], "w+")); 
              fileObj.close();
              foundColDefStr = "";
              isColStructureFound = 'N'; 
              with open(filenameWithPathStr) as fp:
                   line = fp.readline();
                   while line:
                         isColStructureFound = 'N';
                         findColName = "`" + colName + "`";
                         if (line.find(findColName, 0, len(line)))>=0:
                            foundColDefStr = line.strip().rstrip(',');
                            isColStructureFound = 'Y';  
                            if isColStructureFound == 'Y':
                               break;
                         else:
                              line = fp.readline();  
              

              if isColStructureFound == "Y" and foundColDefStr != "" :

                 dropIndxQryStmt = "";
                 updateTblRowsDataQryStmt = ""; 

                 colSqlQryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`" + " ADD ";
                 colSqlQryStmt+= foundColDefStr;  

                 ### Case1.1 primary column key with auto increment value ###
 
                 if colKeyConstraintStr == "PRI" and colExtraKeyStr == "auto_increment" :

                    # indxName = "PRIMARY"; 
                    # dropIndxQryStmt = "ALTER TABLE " +dbName+"."+"`"+tblName+"`"+" DROP INDEX "+"`"+indxName+"`"+";";
                    # dropIndxQryStmt+= "\n"; 

                    colSqlQryStmt = colSqlQryStmt.replace("AUTO_INCREMENT", "PRIMARY KEY");
                    colSqlQryStmt+= " AUTO_INCREMENT";
                    colSqlQryStmt+= ";";

                    statusDataObj['qryStmt'] = dropIndxQryStmt + colSqlQryStmt; 


                 ### Case1.2 unique column key with auto increment value ###

                 elif colKeyConstraintStr == "UNI" and colExtraKeyStr == "auto_increment" :

                      updateTblRowsDataQryStmt = "SET @seqNo = 0;" + "\n";
                      updateTblRowsDataQryStmt+= "UPDATE " +dbName + "." + "`" + tblName + "`";
                      updateTblRowsDataQryStmt+= " SET " + colName + " = " + " @seqNo:= @seqNo + 1 ";
                      updateTblRowsDataQryStmt+= " WHERE 1;";
                      updateTblRowsDataQryStmt+= "\n";
 
                      addColSqlQryStmt = colSqlQryStmt.replace("AUTO_INCREMENT", "");
                      addColSqlQryStmt = addColSqlQryStmt.replace("PRIMARY KEY", "");
                      addColSqlQryStmt = addColSqlQryStmt + ";" + "\n";
                      
                      updateColDefSqlQryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`" + " CHANGE ";
                      updateColDefSqlQryStmt = updateColDefSqlQryStmt + "`" + colName + "`" + " " + foundColDefStr;  
                      updateColDefSqlQryStmt = updateColDefSqlQryStmt.replace("PRIMARY KEY", "");
                      updateColDefSqlQryStmt = updateColDefSqlQryStmt + ";"; 
 
                      statusDataObj['qryStmt'] = addColSqlQryStmt + updateTblRowsDataQryStmt;
                      statusDataObj['updateColDefAfterDependencyResolvedDataObj'] = {
                          colName : {
                             'colDataObj' : colDataObj, 'qryStmt' : updateColDefSqlQryStmt, 
                             'dependsOnArr' : ["index"]
                          } 
                      };

                 else :

                       colSqlQryStmt = colSqlQryStmt + ";";
                       statusDataObj['qryStmt'] = colSqlQryStmt; 


    except Exception as e:
           handleProcsngAbtErrException("Y"); 
    
    return statusDataObj;



### store tables colums creation sql query stmt ###

def storeTblsColsCreationSqlQry(dbDataObj, dbName,dbTblsColsDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['tblsColsCreationStatusDataObj'] = {};
    statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj'] = {};
    statusDataObj['cntOfColCreation'] = 0; 

    try:

       if dbName!="" and len(dbTblsColsDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
          for tblName in dbTblsColsDataObj:
              isDataAvailableInTbl = dbTblsColsDataObj[tblName]['isDataAvailableInTbl'];
              eachTblAllColsDataObj = dbTblsColsDataObj[tblName]['tblAllCols'];
              eachTblAllColsDataObjLen = len(eachTblAllColsDataObj);
              if eachTblAllColsDataObjLen > 0:
                 statusDataObj['tblsColsCreationStatusDataObj'][tblName] = 0;
                 updateColsDefAfterDependencyResolvedDataObj = {};
                 for colName in eachTblAllColsDataObj:

                     colDataObj = eachTblAllColsDataObj[colName];
                     qryStatusDataObj = getTblColCreationSqlQry(
                        dbDataObj, dbName, tblName, isDataAvailableInTbl, colName, colDataObj, againstSvr
                     );

                     if qryStatusDataObj['qryStmt']!="":
                        qryStmt = qryStatusDataObj['qryStmt'];
                        isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                             againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                        );
                        statusDataObj['tblsColsCreationStatusDataObj'][tblName]+= 1;
                        statusDataObj['cntOfColCreation']+= 1;
                    
                     if qryStatusDataObj['updateColDefAfterDependencyResolvedDataObj']!="" :
                        updateColsDefAfterDependencyResolvedDataObj.update(qryStatusDataObj['updateColDefAfterDependencyResolvedDataObj']);
                 
                     if qryStatusDataObj['impRestrictionsContentStr']!="" :
                        impRestrictionsContentStr = qryStatusDataObj['impRestrictionsContentStr'];
                        isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                            againstSvr, dbName, 'importantRestrictions', impRestrictionsContentStr, 'N'
                        );
 

                 if len(updateColsDefAfterDependencyResolvedDataObj)>0 :
                    statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj'][tblName] = updateColsDefAfterDependencyResolvedDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return statusDataObj;



### get table column data type schemas sql query stmt ###

def getTblColDataTypeChangedSqlQry(dbDataObj, dbName, tblName, isDataAvailableInTbl, colName, colDataObj, againstSvr):

    statusDataObj = {};
    statusDataObj['qryStmt'] = "";
    statusDataObj['updateColDefAfterDependencyResolvedDataObj'] = "";
    statusDataObj['impRestrictionsContentStr'] = "";

    try:

        if dbName!="" and tblName!="" and colName!="" and len(colDataObj)>0 and isDataAvailableInTbl!="" :

           global toStoreTempSqlFileDirPath;
    
           colDataArr = colDataObj['updatedColData'];
           colDataType = colDataArr[3];
           colDefaultValStr = colDataArr[5];
           colKeyConstraintStr = colDataArr[9];
           updatedColConfig = colDataObj['updatedColConfig'];
           refDbHost = updatedColConfig['dbHOST'];
           refDbPORTNO = updatedColConfig['dbPORTNO'];
           refDbUser = updatedColConfig['dbUSER'];
           refDbPwd = updatedColConfig['dbPASS']; 
           refDbName = colDataArr[0];
           refTblStructureQry = "SHOW CREATE TABLE " + refDbName + "." + tblName + ";";
           refTblStructureDataArr = fetchDataFromDB(refDbHost, refDbPORTNO, refDbUser, refDbPwd, refDbName, refTblStructureQry);
           if len(refTblStructureDataArr)>0:
              filenameWithPathStr = toStoreTempSqlFileDirPath + "diffDbTemp.sql";
              fileObj = open(filenameWithPathStr, "w+");
              fileObj.write(getConvertedStrIntoBytesToWriteIntoFileObj(refTblStructureDataArr[0][1], "w+"));
              fileObj.close();
              foundColDefStr = ""; 
              isColStructureFound = 'N'; 
              with open(filenameWithPathStr) as fp:
                   line = fp.readline();
                   while line:
                         isColStructureFound = 'N';
                         findColName = "`" + colName + "`";
                         if (line.find(findColName, 0, len(line)))>=0:
                            foundColDefStr = line.strip().rstrip(',');
                            isColStructureFound = 'Y';  
                            if isColStructureFound == 'Y':
                               break;
                         else:
                              line = fp.readline();  

              if isColStructureFound == "Y" and foundColDefStr != "" :

                 updateTblRowsColDataByDefaultValSqlQryStmt = "";
  
                 colSqlQryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`" + " CHANGE ";
                 colSqlQryStmt+= "`" + colName + "`" + " ";
                 colSqlQryStmt+= foundColDefStr;

                 ### Case1.1 converting existing table row column null value with default values ###
                 ### Error can be occur and default value should be identify based on system setup accepting value ###

                 if colSqlQryStmt.find("NOT NULL DEFAULT")>=0 :

                    updateTblRowsColDataByDefaultValSqlQryStmt = "UPDATE " + dbName + "." + "`" + tblName + "`";
                    updateTblRowsColDataByDefaultValSqlQryStmt+= " SET " + colName + "=" + "'" + colDefaultValStr + "'"
                    updateTblRowsColDataByDefaultValSqlQryStmt+= " WHERE 1 AND " + colName + " IS NULL ;";
                    updateTblRowsColDataByDefaultValSqlQryStmt+= "\n";

                    colSqlQryStmt+= ";";
                    statusDataObj['qryStmt'] = updateTblRowsColDataByDefaultValSqlQryStmt + colSqlQryStmt;


                 ### Case1.2 converting existing table row column null value with not null values (own default values) ###
                 ### Error can be occur and own default value should be identify based on system setup accepting value ###

                 elif colSqlQryStmt.find("NOT NULL")>=0 and colDefaultValStr=='ONLYNULL' :

                      colDefaultValStr = '0'; 
                      if colDataType == "date" :
                         colDefaultValStr = "0000-00-00";
                      if colDataType == "datetime" :
                         colDefaultValStr = "0000-00-00 00:00:00";
                      if colDataType == "time" :
                         colDefaultValStr = "00:00:00";
                       
                      # updateTblRowsColDataByDefaultValSqlQryStmt = "UPDATE " + dbName + "." + "`" + tblName + "`";
                      # updateTblRowsColDataByDefaultValSqlQryStmt+= " SET " + colName + "=" + "'" + colDefaultValStr + "'"
                      # updateTblRowsColDataByDefaultValSqlQryStmt+= " WHERE 1 AND " + colName + " IS NULL ;";
                      # updateTblRowsColDataByDefaultValSqlQryStmt+= "\n";
                 
                      colSqlQryStmt+= ";";
                      statusDataObj['qryStmt'] = updateTblRowsColDataByDefaultValSqlQryStmt + colSqlQryStmt;

                 else :
                 
                      colSqlQryStmt+= ";";
                      statusDataObj['qryStmt'] = colSqlQryStmt;
                       
 
                
        
    except Exception as e:
           handleProcsngAbtErrException("Y"); 
    
    return statusDataObj;



### store tables columns data type changed sql query stmt ###

def storeTblsColsDataTypeChangedSqlQry(dbDataObj, dbName,dbTblsColsDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['tblsColsDataTypeChangedStatusDataObj'] = {};
    statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj'] = {};
    statusDataObj['cntOfColDefChanged'] = 0;

    try:

        if dbName!="" and len(dbTblsColsDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
           for tblName in dbTblsColsDataObj:
               isDataAvailableInTbl = dbTblsColsDataObj[tblName]['isDataAvailableInTbl'];
               eachTblAllColsDataObj = dbTblsColsDataObj[tblName]['tblAllCols'];
               eachTblAllColsDataObjLen = len(eachTblAllColsDataObj);
               if eachTblAllColsDataObjLen > 0:
                  statusDataObj['tblsColsDataTypeChangedStatusDataObj'][tblName] = 0;
                  updateColsDefAfterDependencyResolvedDataObj = {};
                  for colName in eachTblAllColsDataObj:

                      colDataObj = eachTblAllColsDataObj[colName];
                      qryStatusDataObj = getTblColDataTypeChangedSqlQry(
                           dbDataObj, dbName, tblName, isDataAvailableInTbl, colName, colDataObj, againstSvr
                      );
      
                      if qryStatusDataObj['qryStmt']!="" :
                         qryStmt = qryStatusDataObj['qryStmt'];
                         isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                             againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                         );
                         statusDataObj['tblsColsDataTypeChangedStatusDataObj'][tblName]+= 1;
                         statusDataObj['cntOfColDefChanged']+= 1;

                      if qryStatusDataObj['updateColDefAfterDependencyResolvedDataObj']!="" :
                         updateColsDefAfterDependencyResolvedDataObj.update(qryStatusDataObj['updateColDefAfterDependencyResolvedDataObj']);
 
                      if qryStatusDataObj['impRestrictionsContentStr']!="" :
                         impRestrictionsContentStr = qryStatusDataObj['impRestrictionsContentStr'];
                         isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                              againstSvr, dbName, 'importantRestrictions', impRestrictionsContentStr, 'N'
                         ); 
 

                  if len(updateColsDefAfterDependencyResolvedDataObj)>0:
                     statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj'][tblName] = updateColsDefAfterDependencyResolvedDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return statusDataObj;



### get table column definition sql query stmt ###

def getTblColDefChangedSqlQry(dbDataObj, dbName, tblName, isDataAvailableInTbl, colName, colDataObj, againstSvr):

    statusDataObj = {};
    statusDataObj['qryStmt'] = "";
    statusDataObj['updateColDefAfterDependencyResolvedDataObj'] = "";
    statusDataObj['impRestrictionsContentStr'] = ""; 

    try:

        if dbName!="" and tblName!="" and colName!="" and len(colDataObj)>0 and isDataAvailableInTbl!="" :

           global toStoreTempSqlFileDirPath;
                
           colDataArr = colDataObj['updatedColData'];
           colDataType = colDataArr[3];
           colDefaultValStr = colDataArr[5];
           colExtraKeyStr = colDataArr[6]; 
           colKeyConstraintStr = colDataArr[9];
           orgColDataArr = colDataObj['orgColData'];
           colPrevDefaultValStr = orgColDataArr[5];
           colPrevExtraKeyStr = orgColDataArr[6]; 
           colPrevKeyConstraintStr = orgColDataArr[9];
           updatedColConfig = colDataObj['updatedColConfig'];
           refDbHost = updatedColConfig['dbHOST'];
           refDbPORTNO = updatedColConfig['dbPORTNO'];
           refDbUser = updatedColConfig['dbUSER'];
           refDbPwd = updatedColConfig['dbPASS']; 
           refDbName = colDataArr[0];
           refTblStructureQry = "SHOW CREATE TABLE " + refDbName + "." + tblName + ";";
           refTblStructureDataArr = fetchDataFromDB(refDbHost, refDbPORTNO, refDbUser, refDbPwd, refDbName, refTblStructureQry);
           if len(refTblStructureDataArr)>0:
              filenameWithPathStr = toStoreTempSqlFileDirPath + "diffDbTemp.sql";
              fileObj = open(filenameWithPathStr, "w+");
              fileObj.write(getConvertedStrIntoBytesToWriteIntoFileObj(refTblStructureDataArr[0][1], "w+"));
              fileObj.close();
              foundColDefStr = ""; 
              isColStructureFound = 'N'; 
              with open(filenameWithPathStr) as fp:
                   line = fp.readline();
                   while line:
                         findColName = "`" + colName + "`";
                         if (line.find(findColName, 0, len(line)))>=0:
                            foundColDefStr = line.strip().rstrip(',');   
                            isColStructureFound = 'Y';  
                            if isColStructureFound == 'Y':
                               break;
                         else:
                              line = fp.readline();  
              
              if isColStructureFound == "Y" and foundColDefStr != "" :

                 updateTblRowsColDataByDefaultValSqlQryStmt = "";
                 colDefTmpryChangedSqlQryStmt = "";
                 dropIndxQryStmt = "";
                 oldColName = colName; 
                 renameColName = colName;

                 ### detetcing is col name rename as new name ###
                 isOldColNameKeyExist = iskeynameExistInDictObj(colDataObj, 'oldColName');
                 if isOldColNameKeyExist == True:
                    if colDataObj['oldColName']!="" :
                       colName = colDataObj['oldColName'];
                       oldColName = colDataObj['oldColName'];
                       

                 colSqlQryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`" + " CHANGE ";
                 colSqlQryStmt+= "`" + colName + "`" + " ";
                 colSqlQryStmt+= foundColDefStr;
    
 
                 ### Case1.1 converting existing table row column null value with default values ###
                 ### Error can be occur and default value should be identify based on system setup accepting value ### 
 
                 if colSqlQryStmt.find("NOT NULL DEFAULT")>=0 and colKeyConstraintStr!="PRI" and colExtraKeyStr!="auto_increment" :

                    updateTblRowsColDataByDefaultValSqlQryStmt = "UPDATE " + dbName + "." + "`" + tblName + "`";
                    updateTblRowsColDataByDefaultValSqlQryStmt+= " SET " + colName + "=" + "'" + colDefaultValStr + "'"
                    updateTblRowsColDataByDefaultValSqlQryStmt+= " WHERE 1 AND " + colName + " IS NULL ;";
                    updateTblRowsColDataByDefaultValSqlQryStmt+= "\n";

                    colSqlQryStmt+= ";";
                    statusDataObj['qryStmt'] = updateTblRowsColDataByDefaultValSqlQryStmt + colSqlQryStmt;


                 ### Case1.2 converting existing table row column null value with not null values (own default values) ###
                 ### Error can be occur and own default value should be identify based on system setup accepting value ###
                 ### col prev definition must not contain any primary/auto-increment values 

                 elif colSqlQryStmt.find("NOT NULL")>=0 and colDefaultValStr=='ONLYNULL' and colKeyConstraintStr!="PRI" and colExtraKeyStr!="auto_increment" and colPrevKeyConstraintStr!="PRI" and colPrevExtraKeyStr!="auto_increment" :
                      
                      colDefaultValStr = '0'; 
                      if colDataType == "date" :
                         colDefaultValStr = "0000-00-00";
                      if colDataType == "datetime" :
                         colDefaultValStr = "0000-00-00 00:00:00";
                      if colDataType == "time" :
                         colDefaultValStr = "00:00:00";

                      # updateTblRowsColDataByDefaultValSqlQryStmt = "UPDATE " + dbName + "." + "`" + tblName + "`";
                      # updateTblRowsColDataByDefaultValSqlQryStmt+= " SET " + colName + "=" + "'" + colDefaultValStr + "'"
                      # updateTblRowsColDataByDefaultValSqlQryStmt+= " WHERE 1 AND " + colName + " IS NULL ;";
                      # updateTblRowsColDataByDefaultValSqlQryStmt+= "\n";
   
                      colSqlQryStmt+= ";";
                      statusDataObj['qryStmt'] = updateTblRowsColDataByDefaultValSqlQryStmt + colSqlQryStmt;

                
                 ### Case1.3 converting existing table row column null value with not null values (own default values) ###
                 ### Error can be occur and own default value should be identify based on system setup accepting value ###
                 ### col prev definition must contain any primary key index & autoincrement values

                 elif colSqlQryStmt.find("NOT NULL")>=0 and colDefaultValStr=='ONLYNULL' and colKeyConstraintStr!="PRI" and colExtraKeyStr!="auto_increment" and colPrevKeyConstraintStr=="PRI" and colPrevExtraKeyStr=="auto_increment" :
                      
                      colDefaultValStr = '0'; 
                      if colDataType == "date" :
                         colDefaultValStr = "0000-00-00";
                      if colDataType == "datetime" :
                         colDefaultValStr = "0000-00-00 00:00:00";
                      if colDataType == "time" :
                         colDefaultValStr = "00:00:00";

                      updateTblRowsColDataByDefaultValSqlQryStmt = "UPDATE " + dbName + "." + "`" + tblName + "`";
                      updateTblRowsColDataByDefaultValSqlQryStmt+= " SET " + colName + "=" + "'" + colDefaultValStr + "'"
                      updateTblRowsColDataByDefaultValSqlQryStmt+= " WHERE 1 AND " + colName + " IS NULL ;";
                      updateTblRowsColDataByDefaultValSqlQryStmt+= "\n";

                      dropIndxQryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`" + " DROP INDEX `PRIMARY`;";
                      dropIndxQryStmt+= "\n"; 
   
                      colSqlQryStmt+= ";" + "\n";
                      statusDataObj['qryStmt'] = updateTblRowsColDataByDefaultValSqlQryStmt + colSqlQryStmt + dropIndxQryStmt;

   
                 ### Case1.4 converting column with primary key and auto increment ###

                 elif colKeyConstraintStr == "PRI" and colExtraKeyStr == "auto_increment" :
                               
                      colDefTmpryChangedSqlQryStmt = colSqlQryStmt;
                      colDefTmpryChangedSqlQryStmt = colDefTmpryChangedSqlQryStmt.replace("AUTO_INCREMENT", "");
                      colDefTmpryChangedSqlQryStmt = colDefTmpryChangedSqlQryStmt.replace("PRIMARY KEY", "");
                      colDefTmpryChangedSqlQryStmt = colDefTmpryChangedSqlQryStmt.replace("PRIMARY", "");
                      colDefTmpryChangedSqlQryStmt = colDefTmpryChangedSqlQryStmt + ";" + "\n";

                      dropIndxQryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`" + " DROP PRIMARY KEY ;";
                      dropIndxQryStmt+= "\n"; 

                      colSqlQryStmt = colSqlQryStmt.replace("AUTO_INCREMENT", "PRIMARY KEY");
                      colSqlQryStmt+= " AUTO_INCREMENT";

                      colSqlQryStmt+= ";";
                      statusDataObj['qryStmt'] = colDefTmpryChangedSqlQryStmt + dropIndxQryStmt + colSqlQryStmt;


                 ### Case1.5 converting column with unique key and auto increment ###

                 elif colKeyConstraintStr == "UNI" and colExtraKeyStr == "auto_increment" :
                     
                      colLimitationStatusDataObj = checkTblColLimitationB4ImplementingChanges(
                            dbDataObj, dbName, tblName, isDataAvailableInTbl, colName, colDataObj, againstSvr
                      );
                      if colLimitationStatusDataObj["isDependencyExist"] == "Y" :
                         colSqlQryStmt+= ";";   
                         statusDataObj['qryStmt'] = "";  
                         statusDataObj['updateColDefAfterDependencyResolvedDataObj'] = {
                             colName : {
                                'colDataObj' : colDataObj, 'qryStmt' : colSqlQryStmt, 
                                'dependsOnArr' : colLimitationStatusDataObj['dependsOnArr']
                             } 
                         };
                      if colLimitationStatusDataObj["isRestrictionExist"] == "Y" :
                         statusDataObj['qryStmt'] = "";  
                         statusDataObj['impRestrictionsContentStr'] = colLimitationStatusDataObj['impRestrictionsContentStr'];
 
                 else :
                       
                      colSqlQryStmt+= ";";
                      statusDataObj['qryStmt'] = colSqlQryStmt;

        
    except Exception as e:
           handleProcsngAbtErrException("Y"); 
    
    return statusDataObj;



### store tables columns definition changed sql query stmt ###

def storeTblsColsDefChangedSqlQry(dbDataObj,dbName,dbTblsColsDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['tblsColsDefChangedStatusDataObj'] = {};
    statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj'] = {};
    statusDataObj['cntOfColDefChanged'] = 0;
  
    try:
     
        if dbName!="" and len(dbTblsColsDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
           for tblName in dbTblsColsDataObj:
               isDataAvailableInTbl = dbTblsColsDataObj[tblName]['isDataAvailableInTbl'];
               eachTblAllColsDataObj = dbTblsColsDataObj[tblName]['tblAllCols'];
               eachTblAllColsDataObjLen = len(eachTblAllColsDataObj);
               if eachTblAllColsDataObjLen > 0:
                  statusDataObj['tblsColsDefChangedStatusDataObj'][tblName] = 0;
                  updateColsDefAfterDependencyResolvedDataObj = {};
                  for colName in eachTblAllColsDataObj:

                      colDataObj = eachTblAllColsDataObj[colName];
                      qryStatusDataObj = getTblColDefChangedSqlQry(
                            dbDataObj, dbName, tblName, isDataAvailableInTbl, colName, colDataObj, againstSvr
                      );

                      if qryStatusDataObj['qryStmt']!="" :
                         qryStmt = qryStatusDataObj['qryStmt'];
                         isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                             againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                         );
                         statusDataObj['tblsColsDefChangedStatusDataObj'][tblName]+= 1;
                         statusDataObj['cntOfColDefChanged']+= 1;
                      
                      if qryStatusDataObj['updateColDefAfterDependencyResolvedDataObj']!="" :
                         updateColsDefAfterDependencyResolvedDataObj.update(
                               qryStatusDataObj['updateColDefAfterDependencyResolvedDataObj']
                         );

                      if qryStatusDataObj['impRestrictionsContentStr']!="" :
                         impRestrictionsContentStr = qryStatusDataObj['impRestrictionsContentStr'];
                         isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                              againstSvr, dbName, 'importantRestrictions', impRestrictionsContentStr, 'N'
                         ); 


                  if len(updateColsDefAfterDependencyResolvedDataObj)>0:
                     statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj'][tblName] = updateColsDefAfterDependencyResolvedDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y"); 
 
    return statusDataObj;



### store to drop tables colums schemas sql query stmt ###

def storeToDropTblsColsSqlQry(dbDataObj,dbName,dbTblsColsDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['tblsColsDroppedStatusDataObj'] = {};
    statusDataObj['cntOfColDropped'] = 0;
 
    try:

       if dbName!="" and len(dbTblsColsDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
          for tblName in dbTblsColsDataObj:
              eachTblAllColsDataObj = dbTblsColsDataObj[tblName]['tblAllCols'];
              eachTblAllColsDataObjLen = len(eachTblAllColsDataObj);
              if eachTblAllColsDataObjLen > 0:
                 statusDataObj['tblsColsDroppedStatusDataObj'][tblName] = 0;   
                 for colName in eachTblAllColsDataObj:
                     qryStmt = "ALTER TABLE " + dbName + "." + "`" + tblName + "`" + " DROP COLUMN " + "`" +  colName + "`" + ";";
                     if qryStmt!="":
                        isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                             againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                        );
                        statusDataObj['tblsColsDroppedStatusDataObj'][tblName]+= 1;
                        statusDataObj['cntOfColDropped']+= 1;
                       


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return statusDataObj;



### store tables attribute option updation sql query stmt ###

def storeTblsAttrOptnDefChangedSqlQry(dbDataObj,dbName,dbTblsDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['cntOfTblAttrOptnUpdated'] = 0;

    try:

       if dbName!="" and len(dbTblsDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
          for tblName in dbTblsDataObj:

              updatedTblConfigObj = dbTblsDataObj[tblName]['updatedTblConfig'];
              updatedTblDataArr = dbTblsDataObj[tblName]['updatedTblData'];
              updatedTblConfigObjLen = len(updatedTblConfigObj);

              if updatedTblConfigObjLen > 0:

                 characterCollationSetSplittedArr = updatedTblDataArr[4].split("_");
                 defaultCharSet = characterCollationSetSplittedArr[0];
                 charCollationSet = updatedTblDataArr[4];

                 qryStmt = "ALTER TABLE "+dbName+"."+"`"+tblName+"`"+" ENGINE = "+updatedTblDataArr[2]+";"+"\n";
                 qryStmt+= "ALTER TABLE "+dbName+"."+"`"+tblName+"`"+" ROW_FORMAT = "+updatedTblDataArr[3]+";"+"\n"; 
                 qryStmt+= "ALTER TABLE "+dbName+"."+"`"+tblName+"`"+" COMMENT = "+"'"+updatedTblDataArr[5]+"'"+";"+"\n";
                 qryStmt+= "ALTER TABLE "+dbName+"."+"`"+tblName+"`"+" DEFAULT CHARACTER SET "+defaultCharSet;
                 qryStmt+= " COLLATE " + charCollationSet + ";" + "\n";

                 isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                      againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                 );
        
                 statusDataObj['cntOfTblAttrOptnUpdated']+= 1;


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return statusDataObj;



### store tables creation schemas sql query stmt ###

def storeTblsCreationSqlQry(dbDataObj, dbName,dbTblsDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):

    statusDataObj = {};
    statusDataObj['cntOfTblCreated'] = 0;

    try:

       if dbName!="" and len(dbTblsDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
          for tblName in dbTblsDataObj:

              updatedTblConfigObj = dbTblsDataObj[tblName]['updatedTblConfig'];
              updatedTblConfigObjLen = len(updatedTblConfigObj);

              if updatedTblConfigObjLen > 0:

                 dbHOST = updatedTblConfigObj['dbHOST'];
                 dbPORTNO = updatedTblConfigObj['dbPORTNO'];
                 dbUSER = updatedTblConfigObj['dbUSER'];
                 dbPASS = updatedTblConfigObj['dbPASS'];                     
                 copyDbName = updatedTblConfigObj['copyDbName'];

                 if dbHOST!="" and dbUSER!="" and dbPASS!="" and copyDbName!="":  
                    qryStmt = "SHOW CREATE TABLE " + copyDbName + "." + "`" + tblName + "`" + " ; ";
                    dataArr = fetchDataFromDB(dbHOST, dbPORTNO, dbUSER, dbPASS, copyDbName, qryStmt);
                    if len(dataArr) > 0:
                       qryStmt = str(dataArr[0][1]) + ";";
                       qryStmt = qryStmt.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS");
                       qryStmt+= "\n"; 
                       qryStmt+= "TRUNCATE TABLE " + dbName + "." + "`" + tblName + "`" + " ; ";
                       isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                            againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
                       );
                       statusDataObj['cntOfTblCreated']+= 1;  


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return statusDataObj;



### store to drop tables schemas sql query stmt ###

def storeToDropTblsSqlQry(dbDataObj, dbName,dbTblsDataObj,againstSvr,isExecuteChanges,qryStmtChangesType):
 
    statusDataObj = {};
    statusDataObj['cntOfTblDropped'] = 0;

    try:

       if dbName!="" and len(dbTblsDataObj)>0 and againstSvr!="" and isExecuteChanges!="" and qryStmtChangesType!="":
       
          for tblName in dbTblsDataObj:
              qryStmt = "DROP TABLE IF EXISTS " + dbName + "." + "`" + tblName + "`" + ";";
              isSqlQryStored = storeDbLvlChangesSqlQryInFilesLog(
                   againstSvr, dbName, qryStmtChangesType, qryStmt, isExecuteChanges
              );
              statusDataObj['cntOfTblDropped']+= 1;


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return statusDataObj;



### handle processing to prepare and store DB level schemas changes sql queries ###

def handleProcsngToStoreDbLvlSchmsChangesSqlQry(applyChangesOn,dbName,dbDataObj,isExecuteChanges):

    try:
        
        ### variable declare for collecting/extracting adding/updating changes about infoSchemas data ###
 
        dbNewNFKTblsDataObj = {};
        dbNewNFKTblsAttrOptnDataObj = {};
        dbNFKTblsAttrOptnDefChangedDataObj = {};
        dbNFKTblsNewColsDataObj = {};
        dbNFKTblsColsDefChangedDataObj = {};
        dbNFKTblsColsDataTypeChangedDataObj = {};
        dbNFKTblIndxCreationDataObj = {};
        dbNFKTblIndxUpdationDataObj = {};

        dbNewFKAsNFKTblsDataObj = {};
        dbNewFKAsNFKTblsAttrOptnDataObj = {}; 
        dbFKAsNFKTblsAttrOptnDefChangedDataObj = {};
        dbFKAsNFKTblsNewColsDataObj = {};
        dbFKAsNFKTblsColsDefChangedDataObj = {};
        dbFKAsNFKTblsColsDataTypeChangedDataObj = {};
        dbFKAsNFKTblsFKNameColConstraintsCreationDataObj = {};
        dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj = {};
        dbFKAsNFKTblsIndxCreationDataObj = {};
        dbFKAsNFKTblIndxUpdationDataObj = {};

        dbNewFKTblsDataObj = {};
        dbNewFKTblsAttrOptnDataObj = {};
        dbFKTblsAttrOptnDefChangedDataObj = {};
        dbFKTblsNewColsDataObj = {};
        dbFKTblsColsDefChangedDataObj = {};
        dbFKTblsColsDataTypeChangedDataObj = {};
        dbFKTblsFKNameColConstraintsCreationDataObj = {};
        dbFKTblsFKNameColConstraintsUpdationDataObj = {};
        dbFKTblsIndxCreationDataObj = {};
        dbFkTblIndxUpdationDataObj = {};

        dbNewTblsAllTgrNameDataObj = {};
        dbTblsNewTgrNameDataObj = {};
        dbTblsTgrDefChangedDataObj = {};

        dbNewRoutinesTypeDataObj = {};
        dbNewRoutinesNameDataObj = {};
        dbRoutinesNameDefChangedDataObj = {};

        dbNewIndependentViewsDataObj = {};
        dbIndependentViewsDefChangedDataObj = {};
        dbNewInAsDependentViewsDataObj = {};
        dbInAsDependentViewsDefChangedDataObj = {};
        dbNewDependentViewsDataObj = {};
        dbDependentViewsDefChangedDataObj = {};

        updateTblsColsDefAfterDependencyResolvedDataObj = {};


        ### variable declare for collecting/extracting dropping changes about infoSchemas data ###
 
        dbDrpNFKTblsDataObj = {};
        dbDrpNFKTblsNewColsDataObj = {};
        dbDrpNFKTblsAllIndxNameDataObj = {};

        dbDrpFKAsNFKTblsDataObj = {};
        dbDrpFKAsNFKTblsNewColsDataObj = {};
        dbDrpFKAsNFKTblsFKNameColConstraintsDataObj = {};
        dbDrpFKAsNFKTblsAllIndxNameDataObj = {};

        dbDrpFKTblsDataObj = {};
        dbDrpFKTblsNewColsDataObj = {};
        dbDrpFKTblsFKNameColConstraintsDataObj = {};
        dbDrpFKTblsAllIndxNameDataObj = {};

        dbDrpTblsAllTgrNameDataObj = {};
        dbDrpTblsNewTgrNameDataObj = {};

        dbDrpRoutinesTypeDataObj = {};
        dbDrpRoutinesNameDataObj = {};

        dbDrpIndependentViewsDataObj = {};
        dbDrpInAsDependentViewsDataObj = {};
        dbDrpDependentViewsDataObj = {};

        isAnyChangesFoundOnDb = 'N';
  
 
        ### Section related to source server collecting & extracting data ###

        if applyChangesOn == "SrcSvr" or applyChangesOn == "DstSvr" :
             
           ### unique adding/updating changes on Db ###

           ### extracting nfk types tables data ###

           dbNewNFKTblsDataObj = dbDataObj['dbNewNFKTblsDataObj'];
           dbNewNFKTblsAttrOptnDataObj = dbDataObj['dbNewNFKTblsAttrOptnDataObj'];
           dbNFKTblsAttrOptnDefChangedDataObj = dbDataObj['dbNFKTblsAttrOptnDefChangedDataObj'];
           dbNFKTblsNewColsDataObj = dbDataObj['dbNFKTblsNewColsDataObj'];
           dbNFKTblsColsDefChangedDataObj = dbDataObj['dbNFKTblsColsDefChangedDataObj'];
           dbNFKTblsColsDataTypeChangedDataObj = dbDataObj['dbNFKTblsColsDataTypeChangedDataObj'];
           dbNFKTblIndxCreationDataObj = dbDataObj['dbNFKTblIndxCreationDataObj'];
           dbNFKTblIndxUpdationDataObj = dbDataObj['dbNFKTblIndxUpdationDataObj'];

           ### extracting fk as nfk types tables data ###

           dbNewFKAsNFKTblsDataObj = dbDataObj['dbNewFKAsNFKTblsDataObj'];
           dbNewFKAsNFKTblsAttrOptnDataObj = dbDataObj['dbNewFKAsNFKTblsAttrOptnDataObj'];
           dbFKAsNFKTblsAttrOptnDefChangedDataObj = dbDataObj['dbFKAsNFKTblsAttrOptnDefChangedDataObj'];
           dbFKAsNFKTblsNewColsDataObj = dbDataObj['dbFKAsNFKTblsNewColsDataObj'];
           dbFKAsNFKTblsColsDefChangedDataObj = dbDataObj['dbFKAsNFKTblsColsDefChangedDataObj'];
           dbFKAsNFKTblsColsDataTypeChangedDataObj = dbDataObj['dbFKAsNFKTblsColsDataTypeChangedDataObj'];
           dbFKAsNFKTblsFKNameColConstraintsCreationDataObj = dbDataObj['dbFKAsNFKTblsFKNameColConstraintsCreationDataObj'];
           dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj = dbDataObj['dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj'];
           dbFKAsNFKTblsIndxCreationDataObj = dbDataObj['dbFKAsNFKTblsIndxCreationDataObj'];
           dbFKAsNFKTblIndxUpdationDataObj = dbDataObj['dbFKAsNFKTblIndxUpdationDataObj'];

           ### extracting fk types tables data ###

           dbNewFKTblsDataObj = dbDataObj['dbNewFKTblsDataObj'];
           dbNewFKTblsAttrOptnDataObj = dbDataObj['dbNewFKTblsAttrOptnDataObj'];
           dbFKTblsAttrOptnDefChangedDataObj = dbDataObj['dbFKTblsAttrOptnDefChangedDataObj'];
           dbFKTblsNewColsDataObj = dbDataObj['dbFKTblsNewColsDataObj'];
           dbFKTblsColsDefChangedDataObj = dbDataObj['dbFKTblsColsDefChangedDataObj'];
           dbFKTblsColsDataTypeChangedDataObj = dbDataObj['dbFKTblsColsDataTypeChangedDataObj'];
           dbFKTblsFKNameColConstraintsCreationDataObj = dbDataObj['dbFKTblsFKNameColConstraintsCreationDataObj'];
           dbFKTblsFKNameColConstraintsUpdationDataObj = dbDataObj['dbFKTblsFKNameColConstraintsUpdationDataObj'];
           dbFKTblsIndxCreationDataObj = dbDataObj['dbFKTblsIndxCreationDataObj'];
           dbFkTblIndxUpdationDataObj = dbDataObj['dbFkTblIndxUpdationDataObj'];

           ### extracting tables triggers data ###

           dbNewTblsAllTgrNameDataObj = dbDataObj['dbNewTblsAllTgrNameDataObj'];
           dbTblsNewTgrNameDataObj = dbDataObj['dbTblsNewTgrNameDataObj'];
           dbTblsTgrDefChangedDataObj = dbDataObj['dbTblsTgrDefChangedDataObj'];

           ### extracting routines data ###

           dbNewRoutinesTypeDataObj = dbDataObj['dbNewRoutinesTypeDataObj'];
           dbNewRoutinesNameDataObj = dbDataObj['dbNewRoutinesNameDataObj'];
           dbRoutinesNameDefChangedDataObj = dbDataObj['dbRoutinesNameDefChangedDataObj'];

           ### extracting views data ###

           dbNewIndependentViewsDataObj = dbDataObj['dbNewIndependentViewsDataObj'];
           dbIndependentViewsDefChangedDataObj = dbDataObj['dbIndependentViewsDefChangedDataObj'];
           dbNewInAsDependentViewsDataObj = dbDataObj['dbNewInAsDependentViewsDataObj'];
           dbInAsDependentViewsDefChangedDataObj = dbDataObj['dbInAsDependentViewsDefChangedDataObj'];
           dbNewDependentViewsDataObj = dbDataObj['dbNewDependentViewsDataObj'];
           dbDependentViewsDefChangedDataObj = dbDataObj['dbDependentViewsDefChangedDataObj'];

           
           ### dropping changes on DB  ###
           
           ### non fk types tables section  ###
 
           dbDrpNFKTblsDataObj = dbDataObj['dbDrpNFKTblsDataObj'];
           dbDrpNFKTblsNewColsDataObj = dbDataObj['dbDrpNFKTblsNewColsDataObj']; 
           dbDrpNFKTblsAllIndxNameDataObj = dbDataObj['dbDrpNFKTblsAllIndxNameDataObj'];
          
           ### non fk as fk types tables section ###

           dbDrpFKAsNFKTblsDataObj = dbDataObj['dbDrpFKAsNFKTblsDataObj'];
           dbDrpFKAsNFKTblsNewColsDataObj = dbDataObj['dbDrpFKAsNFKTblsNewColsDataObj'];
           dbDrpFKAsNFKTblsFKNameColConstraintsDataObj = dbDataObj['dbDrpFKAsNFKTblsFKNameColConstraintsDataObj'];
           dbDrpFKAsNFKTblsAllIndxNameDataObj = dbDataObj['dbDrpFKAsNFKTblsAllIndxNameDataObj'];

           ### fk types tables section ###

           dbDrpFKTblsDataObj = dbDataObj['dbDrpFKTblsDataObj'];
           dbDrpFKTblsNewColsDataObj = dbDataObj['dbDrpFKTblsNewColsDataObj'];
           dbDrpFKTblsFKNameColConstraintsDataObj = dbDataObj['dbDrpFKTblsFKNameColConstraintsDataObj'];
           dbDrpFKTblsAllIndxNameDataObj = dbDataObj['dbDrpFKTblsAllIndxNameDataObj'];
      
           ### tables triggers section ###
 
           dbDrpTblsAllTgrNameDataObj = dbDataObj['dbDrpTblsAllTgrNameDataObj'];
           dbDrpTblsNewTgrNameDataObj = dbDataObj['dbDrpTblsNewTgrNameDataObj'];
      
           ### routines section ###

           dbDrpRoutinesTypeDataObj = dbDataObj['dbDrpRoutinesTypeDataObj'];
           dbDrpRoutinesNameDataObj = dbDataObj['dbDrpRoutinesNameDataObj'];
      
           ### views section ###

           dbDrpIndependentViewsDataObj = dbDataObj['dbDrpIndependentViewsDataObj'];
           dbDrpInAsDependentViewsDataObj = dbDataObj['dbDrpInAsDependentViewsDataObj'];
           dbDrpDependentViewsDataObj = dbDataObj['dbDrpDependentViewsDataObj'];



        ### section about nfk types tables storing db schemas like dropping/adding/updating etc ###

        ### store to drop all unuse nfk tables schemas sql query stmt ###
        if len(dbDrpNFKTblsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropTblsSqlQry(
                 dbDataObj, dbName, dbDrpNFKTblsDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );

        ### store to drop nfk tables all unuse columns schemas sql query stmt ###
        if len(dbDrpNFKTblsNewColsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropTblsColsSqlQry(
                 dbDataObj, dbName, dbDrpNFKTblsNewColsDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );   
      
        ### store to drop nfk tables all unuse indexes schemas sql query stmt ###
        if len(dbDrpNFKTblsAllIndxNameDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropTblsIndexesSqlQry(
                 dbDataObj, dbName, dbDrpNFKTblsAllIndxNameDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );

        ### store to add all new nfk tables schemas sql query stmt ###
        if len(dbNewNFKTblsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';  
           statusDataObj = storeTblsCreationSqlQry(
                dbDataObj, dbName, dbNewNFKTblsDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );

        ### store to add all new nfk tables attribute option schemas sql query stmt ###
        if len(dbNewNFKTblsAttrOptnDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsAttrOptnDefChangedSqlQry(
                 dbDataObj, dbName, dbNewNFKTblsAttrOptnDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );
 
        ### store to update all nfk tables attribute option schemas sql query stmt ###
        if len(dbNFKTblsAttrOptnDefChangedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsAttrOptnDefChangedSqlQry(
                 dbDataObj, dbName, dbNFKTblsAttrOptnDefChangedDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );

        
        ### store to update nfk tables all columns definition changed schemas sql query stmt ###
        if len(dbNFKTblsColsDefChangedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsColsDefChangedSqlQry(
                 dbDataObj, dbName, dbNFKTblsColsDefChangedDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );
           updateTblsColsDefAfterDependencyResolvedDataObj.update(statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj']);

        ### store to update nfk tables all columns data type changed schemas sql query stmt ###
        if len(dbNFKTblsColsDataTypeChangedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';  
           statusDataObj = storeTblsColsDataTypeChangedSqlQry(
                dbDataObj, dbName, dbNFKTblsColsDataTypeChangedDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );
           updateTblsColsDefAfterDependencyResolvedDataObj.update(statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj']);
 
        ### store to add nfk tables all new columns schemas sql query stmt ###
        if len(dbNFKTblsNewColsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsColsCreationSqlQry(
                 dbDataObj, dbName, dbNFKTblsNewColsDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );
           updateTblsColsDefAfterDependencyResolvedDataObj.update(statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj']);
        
        ### store to add nfk tables all new indexes schemas sql query stmt ###
        if len(dbNFKTblIndxCreationDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsIndexesCreationSqlQry(
                 dbDataObj, dbName, dbNFKTblIndxCreationDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );

        ### store to update nfk tables all indexes schemas sql query stmt ###
        if len(dbNFKTblIndxUpdationDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsIndexUpdationSqlQry(
                 dbDataObj, dbName, dbNFKTblIndxUpdationDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );

        ### store to update nfk tables all columns changed definition schemas sql query stmt after index created/updation ###
        if len(updateTblsColsDefAfterDependencyResolvedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';  
           statusDataObj = storeTblsColsDefAfterDependencyResolvedSqlQry(
                 dbDataObj, dbName, updateTblsColsDefAfterDependencyResolvedDataObj, 
                 applyChangesOn, isExecuteChanges, 'updationChanges'
           );
           updateTblsColsDefAfterDependencyResolvedDataObj = {};

        

        ### section about fk as nfk types tables storing db schemas like dropping/adding/updating etc ###
   
        ### store to drop all unuse fk as nfk tables schemas sql query stmt ###
        if len(dbDrpFKAsNFKTblsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropTblsSqlQry(
                 dbDataObj, dbName, dbDrpFKAsNFKTblsDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );
        
        ### store to drop fk as nfk tables all unuse columns schemas sql query stmt ###
        if len(dbDrpFKAsNFKTblsNewColsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropTblsColsSqlQry(
                 dbDataObj, dbName, dbDrpFKAsNFKTblsNewColsDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );

        ### store to drop fk as nfk tables all unuse indexes schemas sql query stmt ###
        if len(dbDrpFKAsNFKTblsAllIndxNameDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropTblsIndexesSqlQry(
                 dbDataObj, dbName, dbDrpFKAsNFKTblsAllIndxNameDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );

        ### store to drop fk as nfk tables all unuse fkNames schemas sql query stmt ###
        if len(dbDrpFKAsNFKTblsFKNameColConstraintsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y'; 
           statusDataObj =  storeToDropTblsFkConstraintSqlQry(
                 dbDataObj, dbName, dbDrpFKAsNFKTblsFKNameColConstraintsDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );     

        ### store to add all new fk as nfk tables schemas sql query stmt ###
        if len(dbNewFKAsNFKTblsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsCreationSqlQry(
                 dbDataObj, dbName, dbNewFKAsNFKTblsDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );
 
        ### store to add all new fk as nfk tables attributes otpion schemas sql query stmt ###
        if len(dbNewFKAsNFKTblsAttrOptnDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsAttrOptnDefChangedSqlQry(
                 dbDataObj, dbName, dbNewFKAsNFKTblsAttrOptnDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );

        ### store to update all fk as nfk tables attributes otpion schemas sql query stmt ###
        if len(dbFKAsNFKTblsAttrOptnDefChangedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y'; 
           statusDataObj = storeTblsAttrOptnDefChangedSqlQry(
                 dbDataObj, dbName, dbFKAsNFKTblsAttrOptnDefChangedDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );       
        
        ### store to update fk as nfk tables all columns changed definition schemas sql query stmt ###
        if len(dbFKAsNFKTblsColsDefChangedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsColsDefChangedSqlQry(
                 dbDataObj, dbName, dbFKAsNFKTblsColsDefChangedDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );   
           updateTblsColsDefAfterDependencyResolvedDataObj.update(statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj']);

        ### store to update fk as nfk tables all columns data type changed schemas sql query stmt ###
        if len(dbFKAsNFKTblsColsDataTypeChangedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsColsDataTypeChangedSqlQry(
                 dbDataObj, dbName, dbFKAsNFKTblsColsDataTypeChangedDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );
           updateTblsColsDefAfterDependencyResolvedDataObj.update(statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj']); 
       
        ### store to add fk as nfk tables all new columns schemas sql query stmt ###
        if len(dbFKAsNFKTblsNewColsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsColsCreationSqlQry(
                 dbDataObj, dbName, dbFKAsNFKTblsNewColsDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );
           updateTblsColsDefAfterDependencyResolvedDataObj.update(statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj']); 
 
        ### store to add fk as nfk tables all new indexes schemas sql query stmt ###
        if len(dbFKAsNFKTblsIndxCreationDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsIndexesCreationSqlQry(
                 dbDataObj, dbName, dbFKAsNFKTblsIndxCreationDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );
        
        ### store to update fk as nfk all indexes definition changed schemas sql query stmt ###
        if len(dbFKAsNFKTblIndxUpdationDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsIndexUpdationSqlQry(
                 dbDataObj, dbName, dbFKAsNFKTblIndxUpdationDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );  

        ### store to update nfk tables all columns changed definition schemas sql query stmt after index created/updation ###
        if len(updateTblsColsDefAfterDependencyResolvedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsColsDefAfterDependencyResolvedSqlQry(
                 dbDataObj, dbName, updateTblsColsDefAfterDependencyResolvedDataObj, 
                 applyChangesOn, isExecuteChanges, 'updationChanges'
           );
           updateTblsColsDefAfterDependencyResolvedDataObj = {};

        ### store to add fk as nfk tables all new fkNames schemas sql query stmt ###
        if len(dbFKAsNFKTblsFKNameColConstraintsCreationDataObj)>0:
           isAnyChangesFoundOnDb = 'Y'; 
           statusDataObj = storeTblsFkNameColsConstraintsSqlQry(
                 dbDataObj, dbName, dbFKAsNFKTblsFKNameColConstraintsCreationDataObj, 
                 applyChangesOn, isExecuteChanges, 'addingNewChanges'
           ); 
        
        ### store to update fk as nfk tables all fkName constraints schemas sql query stmt ###
        if len(dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj =  storeTblsFkNameColsConstraintsSqlQry(
                 dbDataObj, dbName, dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj, 
                 applyChangesOn, isExecuteChanges, 'updationChanges'
           ); 


     
        ### section about fk types tables storing db schemas like dropping/adding/updating etc ###
 
        ### store to drop all unuse fk tables schemas sql query stmt ###
        if len(dbDrpFKTblsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropTblsSqlQry(
                 dbDataObj, dbName, dbDrpFKTblsDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );

        ### store to drop fk tables all unuse columns schemas sql query stmt ###
        if len(dbDrpFKTblsNewColsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropTblsColsSqlQry(
                 dbDataObj, dbName, dbDrpFKTblsNewColsDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );

        ### store to drop fk tables all unuse indexes schemas sql query stmt ###
        if len(dbDrpFKTblsAllIndxNameDataObj)>0:
           isAnyChangesFoundOnDb = 'Y'; 
           statusDataObj = storeToDropTblsIndexesSqlQry(
                 dbDataObj, dbName, dbDrpFKTblsAllIndxNameDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );

        ### store to drop fk tables all unuse fkNames schemas sql query stmt ###
        if len(dbDrpFKTblsFKNameColConstraintsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropTblsFkConstraintSqlQry(
                 dbDataObj, dbName, dbDrpFKTblsFKNameColConstraintsDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           ); 

        ### store to add all new fk tables schemas sql query stmt ###
        if len(dbNewFKTblsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y'; 
           statusDataObj =  storeTblsCreationSqlQry(
                 dbDataObj, dbName, dbNewFKTblsDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );

        ### store to add all fk tables attributes option schemas sql query stmt ###
        if len(dbNewFKTblsAttrOptnDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsAttrOptnDefChangedSqlQry(
                 dbDataObj, dbName, dbNewFKTblsAttrOptnDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           ); 

        ### store to update all fk tables attributes option schemas sql query stmt ###
        if len(dbFKTblsAttrOptnDefChangedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsAttrOptnDefChangedSqlQry(
                 dbDataObj, dbName, dbFKTblsAttrOptnDefChangedDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );
       
        ### store to update fk tables all columns changed definition schemas sql query stmt ###
        if len(dbFKTblsColsDefChangedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsColsDefChangedSqlQry(
                 dbDataObj, dbName, dbFKTblsColsDefChangedDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );
           updateTblsColsDefAfterDependencyResolvedDataObj.update(statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj']);  

        ### store to update fk tables all columns data type changed schemas sql query stmt ###
        if len(dbFKTblsColsDataTypeChangedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';  
           statusDataObj = storeTblsColsDataTypeChangedSqlQry(
                 dbDataObj, dbName, dbFKTblsColsDataTypeChangedDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );
           updateTblsColsDefAfterDependencyResolvedDataObj.update(statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj']);  

        ### store to add fk tables all new columns schemas sql query stmt ###
        if len(dbFKTblsNewColsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsColsCreationSqlQry(
                 dbDataObj, dbName, dbFKTblsNewColsDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );
           updateTblsColsDefAfterDependencyResolvedDataObj.update(statusDataObj['updateTblsColsDefAfterDependencyResolvedDataObj']);
      
        ### store to add fk tables all indexes names schemas sql query stmt ###
        if len(dbFKTblsIndxCreationDataObj)>0:
           isAnyChangesFoundOnDb = 'Y'; 
           statusDataObj = storeTblsIndexesCreationSqlQry(
                 dbDataObj, dbName, dbFKTblsIndxCreationDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );

        ### store to update fk table indexes schemas sql query stmt ###
        if len(dbFkTblIndxUpdationDataObj)>0:
           isAnyChangesFoundOnDb = 'Y'; 
           statusDataObj = storeTblsIndexUpdationSqlQry(
                 dbDataObj, dbName, dbFkTblIndxUpdationDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );   
       
        ### store to add fk tables all new fkNames schemas sql query stmt ###
        if len(dbFKTblsFKNameColConstraintsCreationDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsFkNameColsConstraintsSqlQry(
                 dbDataObj, dbName, dbFKTblsFKNameColConstraintsCreationDataObj, 
                 applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );
 
        ### store to update fk tables fkName constraints schemas sql query stmt ###
        if len(dbFKTblsFKNameColConstraintsUpdationDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsFkNameColsConstraintsSqlQry(
                 dbDataObj, dbName, dbFKTblsFKNameColConstraintsUpdationDataObj, 
                 applyChangesOn, isExecuteChanges, 'updationChanges'
           ); 

        ### store to update nfk tables all columns changed definition schemas sql query stmt after index created/updation ###
        if len(updateTblsColsDefAfterDependencyResolvedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsColsDefAfterDependencyResolvedSqlQry(
                 dbDataObj, dbName, updateTblsColsDefAfterDependencyResolvedDataObj, 
                 applyChangesOn, isExecuteChanges, 'updationChanges'
           );
           updateTblsColsDefAfterDependencyResolvedDataObj = {};

   

        ### section about table trigger storing schemas like dropping/adding/updating etc ###

        ### store to drop tables all unuse trigger schemas sql query stmt ###
        if len(dbDrpTblsAllTgrNameDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropTblsTgrsSqlQry(
                 dbDataObj, dbName, dbDrpTblsAllTgrNameDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges' 
           );
   
        ### store to drop tables all unuse trigger schemas sql query stmt ###
        if len(dbDrpTblsNewTgrNameDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropTblsTgrsSqlQry(
                 dbDataObj, dbName, dbDrpTblsNewTgrNameDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );  

        ### store to add tables all new trigger schemas sql query stmt ###
        if len(dbNewTblsAllTgrNameDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';  
           statusDataObj = storeTblsTriggersCreationSqlQry(
                 dbDataObj, dbName, dbNewTblsAllTgrNameDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );
         
        ### store to add tables all trigger schemas sql query stmt ###
        if len(dbTblsNewTgrNameDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsTriggersCreationSqlQry(
                 dbDataObj, dbName, dbTblsNewTgrNameDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );   
    
        ### store to update tables trigger definition changed schemas sql query stmt ###
        if len(dbTblsTgrDefChangedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeTblsTriggersCreationSqlQry(
                 dbDataObj, dbName, dbTblsTgrDefChangedDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );

           

        ### section about DB routines storing schemas like dropping/adding/updating etc ###

        ### store to drop all unuse routines types schemas sql query stmt ###
        if len(dbDrpRoutinesTypeDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropRoutinesSqlQry(
                 dbDataObj, dbName, dbDrpRoutinesTypeDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );

        ### store to drop routine types with all unuse routines schemas sql query stmt ###
        if len(dbDrpRoutinesNameDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropRoutinesSqlQry(
                 dbDataObj, dbName, dbDrpRoutinesNameDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );

        ### store to add all new routine types with all new routines schemas sql query stmt ###
        if len(dbNewRoutinesTypeDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeRoutineCreationSqlQry(
                 dbDataObj, dbName, dbNewRoutinesTypeDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           ); 

        ### store to add routine types with all new routines schemas sql query stmt ###
        if len(dbNewRoutinesNameDataObj)>0:
           isAnyChangesFoundOnDb = 'Y'; 
           statusDataObj = storeRoutineCreationSqlQry(
                 dbDataObj, dbName, dbNewRoutinesNameDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           ); 

        ### store to update routine types existing routines changed definition schemas sql query stmt ###
        if len(dbRoutinesNameDefChangedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeRoutineCreationSqlQry(
                 dbDataObj, dbName, dbRoutinesNameDefChangedDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );    

           
        ### section about DB views storing schemas like dropping/adding/updating etc ### 

        ### store to drop db all unuse independent views schemas sql query stmt ###
        if len(dbDrpIndependentViewsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropViewsSqlQry(
                 dbDataObj, dbName, dbDrpIndependentViewsDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           ); 
       
        ### store to drop all new independent as dependent views schemas sql query stmt ###
        if len(dbDrpInAsDependentViewsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropViewsSqlQry(
                 dbDataObj, dbName, dbDrpInAsDependentViewsDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );

        ### store to drop all new dependent views sql query stmt ###
        if len(dbDrpDependentViewsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeToDropViewsSqlQry(
                 dbDataObj, dbName, dbDrpDependentViewsDataObj, applyChangesOn, isExecuteChanges, 'droppedChanges'
           );         
          
        ### store to add all new independent views schemas sql query stmt ###
        if len(dbNewIndependentViewsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeViewsCreationSqlQry(
                 dbDataObj, dbName, dbNewIndependentViewsDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );

        ### store to add independent views changed definition schemas sql query stmt ###
        if len(dbIndependentViewsDefChangedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeViewsCreationSqlQry(
                 dbDataObj, dbName, dbIndependentViewsDefChangedDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );

        ### ### to add all new independent as dependent views schemas sql query stmt ###
        if len(dbNewInAsDependentViewsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj = storeViewsCreationSqlQry(
                 dbDataObj, dbName, dbNewInAsDependentViewsDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );
   
        ### store to add independent as dependent views changed definition sql query stmt ###
        if len(dbInAsDependentViewsDefChangedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';  
           statusDataObj = storeViewsCreationSqlQry(
                 dbDataObj, dbName, dbInAsDependentViewsDefChangedDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );
        
        ### store to add all new dependent views sql query stmt ##
        if len(dbNewDependentViewsDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';
           statusDataObj =  storeViewsCreationSqlQry(
                 dbDataObj, dbName, dbNewDependentViewsDataObj, applyChangesOn, isExecuteChanges, 'addingNewChanges'
           );    

        ### store to add dependent views changed definition sql query stmt ##
        if len(dbDependentViewsDefChangedDataObj)>0:
           isAnyChangesFoundOnDb = 'Y';  
           statusDataObj = storeViewsCreationSqlQry(
                 dbDataObj, dbName, dbDependentViewsDefChangedDataObj, applyChangesOn, isExecuteChanges, 'updationChanges'
           );


        if isAnyChangesFoundOnDb == "N" :
           if applyChangesOn == "SrcSvr" :
              global toStoreSqlQryFilesLogAbtSrcSvrDataObj;
              toStoreSqlQryFilesLogAbtSrcSvrDataObj['schemasDataObj'][dbName] = {};             
           if applyChangesOn == "DstSvr" :
              global toStoreSqlQryFilesLogAbtDstSvrDataObj;
              toStoreSqlQryFilesLogAbtDstSvrDataObj['schemasDataObj'][dbName] = {};  


    except Exception as e:
           handleProcsngAbtErrException("Y");


### handle processing to isNewSchemasKey in Db schemas changes ###

def handleProcsngToAddIsNewSchemaKeyInDbSchemasChanges(dbDataObj):

    try:

        dbNFKTblsNewColsDataObj = {};
        dbNFKTblIndxCreationDataObj = {};
        dbNFKTblIndxUpdationDataObj = {};

        dbFKAsNFKTblsNewColsDataObj = {};   
        dbFKAsNFKTblsFKNameColConstraintsCreationDataObj = {}; 
        dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj = {}; 
        dbFKAsNFKTblsIndxCreationDataObj = {};
        dbFKAsNFKTblIndxUpdationDataObj = {};

        dbFKTblsNewColsDataObj  = {};
        dbFKTblsFKNameColConstraintsCreationDataObj = {};
        dbFKTblsFKNameColConstraintsUpdationDataObj = {};
        dbFKTblsIndxCreationDataObj = {};
        dbFkTblIndxUpdationDataObj = {};


        isDbNFKTblsNewColsDataObjExist = iskeynameExistInDictObj(dbDataObj, 'dbNFKTblsNewColsDataObj');
        if isDbNFKTblsNewColsDataObjExist == True:
           dbNFKTblsNewColsDataObj = dbDataObj['dbNFKTblsNewColsDataObj'];

        isDbNFKTblIndxCreationDataObjExist = iskeynameExistInDictObj(dbDataObj, 'dbNFKTblIndxCreationDataObj');
        if isDbNFKTblIndxCreationDataObjExist == True:
           dbNFKTblIndxCreationDataObj = dbDataObj['dbNFKTblIndxCreationDataObj'];

        isDbNFKTblIndxUpdationDataObjExist = iskeynameExistInDictObj(dbDataObj, 'dbNFKTblIndxUpdationDataObj');
        if isDbNFKTblIndxUpdationDataObjExist == True:
           dbNFKTblIndxUpdationDataObj = dbDataObj['dbNFKTblIndxUpdationDataObj'];

        
        isDbFKAsNFKTblsNewColsDataObjExist = iskeynameExistInDictObj(dbDataObj, 'dbFKAsNFKTblsNewColsDataObj');
        if isDbFKAsNFKTblsNewColsDataObjExist == True:
           dbFKAsNFKTblsNewColsDataObj = dbDataObj['dbFKAsNFKTblsNewColsDataObj'];

        isDbFKAsNFKTblsIndxCreationDataObjExist = iskeynameExistInDictObj(dbDataObj, 'dbFKAsNFKTblsIndxCreationDataObj');
        if isDbFKAsNFKTblsIndxCreationDataObjExist == True:
           dbFKAsNFKTblsIndxCreationDataObj = dbDataObj['dbFKAsNFKTblsIndxCreationDataObj'];

        isDbFKAsNFKTblIndxUpdationDataObjExist = iskeynameExistInDictObj(dbDataObj, 'dbFKAsNFKTblIndxUpdationDataObj');
        if isDbFKAsNFKTblIndxUpdationDataObjExist == True:
           dbFKAsNFKTblIndxUpdationDataObj = dbDataObj['dbFKAsNFKTblIndxUpdationDataObj']; 

        
        isDbFKTblsNewColsDataObjExist = iskeynameExistInDictObj(dbDataObj, 'dbFKTblsNewColsDataObj');
        if isDbFKTblsNewColsDataObjExist == True:
           dbFKTblsNewColsDataObj = dbDataObj['dbFKTblsNewColsDataObj'];

        isDbFKTblsIndxCreationDataObjExist = iskeynameExistInDictObj(dbDataObj, 'dbFKTblsIndxCreationDataObj');
        if isDbFKTblsIndxCreationDataObjExist == True:
           dbFKTblsIndxCreationDataObj = dbDataObj['dbFKTblsIndxCreationDataObj'];

        isDbFkTblIndxUpdationDataObjExist = iskeynameExistInDictObj(dbDataObj, 'dbFkTblIndxUpdationDataObj');
        if isDbFkTblIndxUpdationDataObjExist == True:
           dbFkTblIndxUpdationDataObj = dbDataObj['dbFkTblIndxUpdationDataObj'];

 
        ### Section about nfk types tables data ###

        for tblName in dbNFKTblIndxCreationDataObj:
            isTblExist = iskeynameExistInDictObj(dbNFKTblsNewColsDataObj, tblName);
            if isTblExist == True :
               allIndexesDataObj = dbNFKTblIndxCreationDataObj[tblName];
               for indxName in allIndexesDataObj: 
                   for tblColName in dbNFKTblsNewColsDataObj[tblName]['tblAllCols']: 
                       isTblNewColExistInIndex = iskeynameExistInDictObj(allIndexesDataObj[indxName]['indxAllCols'], tblColName);
                       if isTblNewColExistInIndex == True :
                          allIndexesDataObj[indxName]['indxAllCols'][tblColName]['isNewSchemas'] =  'Y';
                       
               dbNFKTblIndxCreationDataObj[tblName] = allIndexesDataObj;


        for tblName in dbNFKTblIndxUpdationDataObj:
            isTblExist = iskeynameExistInDictObj(dbNFKTblsNewColsDataObj, tblName);
            if isTblExist == True :
               allIndexesDataObj = dbNFKTblIndxUpdationDataObj[tblName];
               for indxName in allIndexesDataObj: 
                   for tblColName in dbNFKTblsNewColsDataObj[tblName]['tblAllCols']: 
                       isTblNewColExistInIndex = iskeynameExistInDictObj(allIndexesDataObj[indxName]['indxAllCols'], tblColName);
                       if isTblNewColExistInIndex == True :
                          allIndexesDataObj[indxName]['indxAllCols'][tblColName]['isNewSchemas'] =  'Y';
                       
               dbNFKTblIndxUpdationDataObj[tblName] = allIndexesDataObj;


        ### Section about fk as nfk types tables data ###

        for tblName in dbFKAsNFKTblsIndxCreationDataObj:
            isTblExist = iskeynameExistInDictObj(dbFKAsNFKTblsNewColsDataObj, tblName);
            if isTblExist == True :
               allIndexesDataObj = dbFKAsNFKTblsIndxCreationDataObj[tblName];
               for indxName in allIndexesDataObj: 
                   for tblColName in dbFKAsNFKTblsNewColsDataObj[tblName]['tblAllCols']: 
                       isTblNewColExistInIndex = iskeynameExistInDictObj(allIndexesDataObj[indxName]['indxAllCols'], tblColName);
                       if isTblNewColExistInIndex == True :
                          allIndexesDataObj[indxName]['indxAllCols'][tblColName]['isNewSchemas'] =  'Y';
                       
               dbFKAsNFKTblsIndxCreationDataObj[tblName] = allIndexesDataObj;

        for tblName in dbFKAsNFKTblIndxUpdationDataObj:
            isTblExist = iskeynameExistInDictObj(dbFKAsNFKTblsNewColsDataObj, tblName);
            if isTblExist == True :
               allIndexesDataObj = dbFKAsNFKTblIndxUpdationDataObj[tblName];
               for indxName in allIndexesDataObj: 
                   for tblColName in dbFKAsNFKTblsNewColsDataObj[tblName]['tblAllCols']: 
                       isTblNewColExistInIndex = iskeynameExistInDictObj(allIndexesDataObj[indxName]['indxAllCols'], tblColName);
                       if isTblNewColExistInIndex == True :
                          allIndexesDataObj[indxName]['indxAllCols'][tblColName]['isNewSchemas'] =  'Y';
                       
               dbFKAsNFKTblIndxUpdationDataObj[tblName] = allIndexesDataObj;


        ### Section about fk types tables data ###

        for tblName in dbFKTblsIndxCreationDataObj:
            isTblExist = iskeynameExistInDictObj(dbFKTblsNewColsDataObj, tblName);
            if isTblExist == True :
               allIndexesDataObj = dbFKTblsIndxCreationDataObj[tblName];
               for indxName in allIndexesDataObj: 
                   for tblColName in dbFKTblsNewColsDataObj[tblName]['tblAllCols']: 
                       isTblNewColExistInIndex = iskeynameExistInDictObj(allIndexesDataObj[indxName]['indxAllCols'], tblColName);
                       if isTblNewColExistInIndex == True :
                          allIndexesDataObj[indxName]['indxAllCols'][tblColName]['isNewSchemas'] =  'Y';
                       
               dbFKTblsIndxCreationDataObj[tblName] = allIndexesDataObj;

        for tblName in dbFkTblIndxUpdationDataObj:
            isTblExist = iskeynameExistInDictObj(dbFKTblsNewColsDataObj, tblName);
            if isTblExist == True :
               allIndexesDataObj = dbFkTblIndxUpdationDataObj[tblName];
               for indxName in allIndexesDataObj: 
                   for tblColName in dbFKTblsNewColsDataObj[tblName]['tblAllCols']: 
                       isTblNewColExistInIndex = iskeynameExistInDictObj(allIndexesDataObj[indxName]['indxAllCols'], tblColName);
                       if isTblNewColExistInIndex == True :
                          allIndexesDataObj[indxName]['indxAllCols'][tblColName]['isNewSchemas'] =  'Y';
                       
               dbFkTblIndxUpdationDataObj[tblName] = allIndexesDataObj;


        ### overwrite keys ###

        dbDataObj['dbNFKTblIndxCreationDataObj'] = dbNFKTblIndxCreationDataObj;
        dbDataObj['dbNFKTblIndxUpdationDataObj'] = dbNFKTblIndxUpdationDataObj;
         
        dbDataObj['dbFKAsNFKTblsIndxCreationDataObj'] = dbFKAsNFKTblsIndxCreationDataObj;
        dbDataObj['dbFKAsNFKTblIndxUpdationDataObj'] = dbFKAsNFKTblIndxUpdationDataObj;

        dbDataObj['dbFKTblsIndxCreationDataObj'] = dbFKTblsIndxCreationDataObj;
        dbDataObj['dbFkTblIndxUpdationDataObj'] = dbFkTblIndxUpdationDataObj;
           

    except Exception as e:
           handleProcsngAbtErrException("Y");   

    return dbDataObj;


### handle processing to extract uniq infoschemas drop changes about Db ###

def handleProcsngToExtractUniqDbSchemasDropChanges(againstSvr, dbDataObj):

    try:
       
        dbDrpNFKTblsDataObj = {}; 
        dbDrpNFKTblsAllIndxNameDataObj = {};
        dbDrpNFKTblsNewIndxNameDataObj = {};
        dbDrpNFKTblIndxNewColsDataObj = {};
        dbNFKTblIndxCreationDataObj = {};
        dbNFKTblIndxUpdationDataObj = {}; 

        dbDrpFKAsNFKTblsDataObj = {};           
        dbDrpFKAsNFKTblsFKNameColConstraintsDataObj = {};
        dbDrpFKAsNFKTblsNewFKNameColConstraintsDataObj = {};
        dbDrpFKAsNFKTblsFKNameNewColsConstraintsDataObj = {};
        dbDrpFKAsNFKTblsAllIndxNameDataObj = {};
        dbDrpFKAsNFKTblsNewIndxNameDataObj = {};
        dbDrpFKAsNFKTblIndxNewColsDataObj = {};
        dbFKAsNFKTblsFKNameColConstraintsCreationDataObj = {}; 
        dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj = {}
        dbFKAsNFKTblsIndxCreationDataObj = {};
        dbFKAsNFKTblIndxUpdationDataObj = {};

        dbDrpFKTblsDataObj = {};
        dbDrpFKTblsFKNameColConstraintsDataObj = {};
        dbDrpFKTblsNewFKNameColConstraintsDataObj = {};
        dbDrpFKTblsFKNameNewColsConstraintsDataObj = {};
        dbDrpFKTblsAllIndxNameDataObj = {};
        dbDrpFKTblsNewIndxNameDataObj = {};
        dbDrpFKTblIndxNewColsDataObj = {};
        dbFKTblsFKNameColConstraintsCreationDataObj = {};
        dbFKTblsFKNameColConstraintsUpdationDataObj = {};
        dbFKTblsIndxCreationDataObj = {};
        dbFkTblIndxUpdationDataObj = {};

  
        ### section related to source server ###
  
        if againstSvr == "SrcSvr" :
           
           
           ### section related to nfk types tables ###
     
           dbDrpNFKTblsDataObj = dbDataObj['srcDbDrpNFKTblsDataObj'];
           dbDrpNFKTblsAllIndxNameDataObj = dbDataObj['srcDbDrpNFKTblsAllIndxNameDataObj'];
           dbDrpNFKTblsNewIndxNameDataObj = dbDataObj['srcDbDrpNFKTblsNewIndxNameDataObj'];
           dbDrpNFKTblIndxNewColsDataObj = dbDataObj['srcDbDrpNFKTblIndxNewColsDataObj'];
           dbNFKTblIndxCreationDataObj = dbDataObj['srcDbNFKTblIndxCreationDataObj'];
           dbNFKTblIndxUpdationDataObj = dbDataObj['srcDbNFKTblIndxUpdationDataObj'];


           ### section related to fk as nfk types tables ###

           dbDrpNFKTblsDataObj = dbDataObj['srcDbDrpNFKTblsDataObj'];
           dbDrpFKAsNFKTblsFKNameColConstraintsDataObj = dbDataObj['srcDbDrpFKAsNFKTblsFKNameColConstraintsDataObj'];
           dbDrpFKAsNFKTblsNewFKNameColConstraintsDataObj = dbDataObj['srcDbDrpFKAsNFKTblsNewFKNameColConstraintsDataObj'];
           dbDrpFKAsNFKTblsFKNameNewColsConstraintsDataObj = dbDataObj['srcDbDrpFKAsNFKTblsFKNameNewColsConstraintsDataObj'];
           dbDrpFKAsNFKTblsAllIndxNameDataObj = dbDataObj['srcDbDrpFKAsNFKTblsAllIndxNameDataObj'];
           dbDrpFKAsNFKTblsNewIndxNameDataObj = dbDataObj['srcDbDrpFKAsNFKTblsNewIndxNameDataObj'];
           dbDrpFKAsNFKTblIndxNewColsDataObj = dbDataObj['srcDbDrpFKAsNFKTblIndxNewColsDataObj'];
           dbFKAsNFKTblsFKNameColConstraintsCreationDataObj = dbDataObj['srcDbFKAsNFKTblsFKNameColConstraintsCreationDataObj'];
           dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj = dbDataObj['srcDbFKAsNFKTblsFKNameColConstraintsUpdationDataObj'];
           dbFKAsNFKTblsIndxCreationDataObj = dbDataObj['srcDbFKAsNFKTblsIndxCreationDataObj'];
           dbFKAsNFKTblIndxUpdationDataObj = dbDataObj['srcDbFKAsNFKTblIndxUpdationDataObj'];

           
           ### section related to fk types tables ###
        
           dbDrpFKTblsDataObj = dbDataObj['srcDbDrpFKTblsDataObj'];     
           dbDrpFKTblsFKNameColConstraintsDataObj = dbDataObj['srcDbDrpFKTblsFKNameColConstraintsDataObj'];
           dbDrpFKTblsNewFKNameColConstraintsDataObj = dbDataObj['srcDbDrpFKTblsNewFKNameColConstraintsDataObj'];
           dbDrpFKTblsFKNameNewColsConstraintsDataObj = dbDataObj['srcDbDrpFKTblsFKNameNewColsConstraintsDataObj'];
           dbDrpFKTblsAllIndxNameDataObj = dbDataObj['srcDbDrpFKAsNFKTblsAllIndxNameDataObj'];
           dbDrpFKTblsNewIndxNameDataObj = dbDataObj['srcDbDrpFKAsNFKTblsNewIndxNameDataObj'];
           dbDrpFKTblIndxNewColsDataObj = dbDataObj['srcDbDrpFKAsNFKTblIndxNewColsDataObj'];
           dbFKTblsFKNameColConstraintsCreationDataObj = dbDataObj['srcDbFKTblsFKNameColConstraintsCreationDataObj'];
           dbFKTblsFKNameColConstraintsUpdationDataObj = dbDataObj['srcDbFKTblsFKNameColConstraintsUpdationDataObj'];
           dbFKTblsIndxCreationDataObj = dbDataObj['srcDbFKTblsIndxCreationDataObj'];
           dbFkTblIndxUpdationDataObj = dbDataObj['srcDbFkTblIndxUpdationDataObj'];


        ### section related to destination server ###

        if againstSvr == "DstSvr" :
           
           ### section related to nfk types table ###
 
           dbDrpNFKTblsDataObj = dbDataObj['dstDbDrpNFKTblsDataObj'];
           dbDrpNFKTblsAllIndxNameDataObj = dbDataObj['dstDbDrpNFKTblsAllIndxNameDataObj'];
           dbDrpNFKTblsNewIndxNameDataObj = dbDataObj['dstDbDrpNFKTblsNewIndxNameDataObj'];
           dbDrpNFKTblIndxNewColsDataObj = dbDataObj['dstDbDrpNFKTblIndxNewColsDataObj'];
           dbNFKTblIndxCreationDataObj = dbDataObj['dstDbNFKTblIndxCreationDataObj'];
           dbNFKTblIndxUpdationDataObj = dbDataObj['dstDbNFKTblIndxUpdationDataObj'];
           
           ### section related to fk as nfk types table ###
        
           dbDrpFKAsNFKTblsDataObj = dbDataObj['dstDbDrpFKAsNFKTblsDataObj']; 
           dbDrpFKAsNFKTblsFKNameColConstraintsDataObj = dbDataObj['dstDbDrpFKAsNFKTblsFKNameColConstraintsDataObj'];
           dbDrpFKAsNFKTblsNewFKNameColConstraintsDataObj = dbDataObj['dstDbDrpFKAsNFKTblsNewFKNameColConstraintsDataObj'];
           dbDrpFKAsNFKTblsFKNameNewColsConstraintsDataObj = dbDataObj['dstDbDrpFKAsNFKTblsFKNameNewColsConstraintsDataObj'];
           dbDrpFKAsNFKTblsAllIndxNameDataObj = dbDataObj['dstDbDrpFKAsNFKTblsAllIndxNameDataObj'];
           dbDrpFKAsNFKTblsNewIndxNameDataObj = dbDataObj['dstDbDrpFKAsNFKTblsNewIndxNameDataObj'];
           dbDrpFKAsNFKTblIndxNewColsDataObj = dbDataObj['dstDbDrpFKAsNFKTblIndxNewColsDataObj'];
           dbFKAsNFKTblsFKNameColConstraintsCreationDataObj = dbDataObj['dstDbFKAsNFKTblsFKNameColConstraintsCreationDataObj'];
           dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj = dbDataObj['dstDbFKAsNFKTblsFKNameColConstraintsUpdationDataObj'];
           dbFKAsNFKTblsIndxCreationDataObj = dbDataObj['dstDbFKAsNFKTblsIndxCreationDataObj'];
           dbFKAsNFKTblIndxUpdationDataObj = dbDataObj['dstDbFKAsNFKTblIndxUpdationDataObj'];

           
           ### section related to fk types table ###

           dbDrpFKTblsDataObj = dbDataObj['dstDbDrpFKTblsDataObj'];
           dbDrpFKTblsFKNameColConstraintsDataObj = dbDataObj['dstDbDrpFKTblsFKNameColConstraintsDataObj'];
           dbDrpFKTblsNewFKNameColConstraintsDataObj = dbDataObj['dstDbDrpFKTblsNewFKNameColConstraintsDataObj'];
           dbDrpFKTblsFKNameNewColsConstraintsDataObj = dbDataObj['dstDbDrpFKTblsFKNameNewColsConstraintsDataObj'];
           dbDrpFKTblsAllIndxNameDataObj = dbDataObj['dstDbDrpFKTblsAllIndxNameDataObj'];
           dbDrpFKTblsNewIndxNameDataObj = dbDataObj['dstDbDrpFKTblsNewIndxNameDataObj'];
           dbDrpFKTblIndxNewColsDataObj = dbDataObj['dstDbDrpFKTblIndxNewColsDataObj'];
           dbFKTblsFKNameColConstraintsCreationDataObj = dbDataObj['dstDbFKTblsFKNameColConstraintsCreationDataObj'];
           dbFKTblsFKNameColConstraintsUpdationDataObj = dbDataObj['dstDbFKTblsFKNameColConstraintsUpdationDataObj'];
           dbFKTblsIndxCreationDataObj = dbDataObj['dstDbFKTblsIndxCreationDataObj'];
           dbFkTblIndxUpdationDataObj = dbDataObj['dstDbFkTblIndxUpdationDataObj'];


        ### collecting nfk types tables unique indexes/foreign keys to drop ###
           
        for tblName in dbDrpNFKTblsNewIndxNameDataObj:
            isTblExist = iskeynameExistInDictObj(dbDrpNFKTblsAllIndxNameDataObj, tblName);
            if isTblExist == False:
               dbDrpNFKTblsAllIndxNameDataObj[tblName] = dbDrpNFKTblsNewIndxNameDataObj[tblName];
            else:
                dbDrpNFKTblsAllIndxNameDataObj[tblName].update(dbDrpNFKTblsNewIndxNameDataObj[tblName]);

        for tblName in dbDrpNFKTblIndxNewColsDataObj:
            isTblExist = iskeynameExistInDictObj(dbDrpNFKTblsAllIndxNameDataObj, tblName);
            if isTblExist == False:
               dbDrpNFKTblsAllIndxNameDataObj[tblName] = dbDrpNFKTblIndxNewColsDataObj[tblName];
            else:
                dbDrpNFKTblsAllIndxNameDataObj[tblName].update(dbDrpNFKTblIndxNewColsDataObj[tblName]);

        ### remove index table name, when whole table is removing ###

        for tblName in dbDrpNFKTblsDataObj:
            isIndxTblExist = iskeynameExistInDictObj(dbDrpNFKTblsAllIndxNameDataObj, tblName);
            if isIndxTblExist == True:
               del dbDrpNFKTblsAllIndxNameDataObj[tblName];
        
  
        ### remove index name, when whole table is not removing ###

        for tblName in dbNFKTblIndxUpdationDataObj:
            isDropIndxTblExist = iskeynameExistInDictObj(dbDrpNFKTblsAllIndxNameDataObj, tblName);
            if isDropIndxTblExist == True:
               updationAllIndexesDataObj = dbNFKTblIndxUpdationDataObj[tblName];
               for indxName in updationAllIndexesDataObj:
                   isDropIndxExist = iskeynameExistInDictObj(dbDrpNFKTblsAllIndxNameDataObj[tblName], indxName);
                   if isDropIndxExist == True:
                      del dbDrpNFKTblsAllIndxNameDataObj[tblName][indxName];
               if len(dbDrpNFKTblsAllIndxNameDataObj[tblName])<=0 :
                  del dbDrpNFKTblsAllIndxNameDataObj[tblName];

  

        ### collecting unique fk as nfk types table indexes/foreign keys to drop ###
           
        for tblName in dbDrpFKAsNFKTblsNewFKNameColConstraintsDataObj:
            isTblExist = iskeynameExistInDictObj(dbDrpFKAsNFKTblsFKNameColConstraintsDataObj, tblName);
            if isTblExist == False:
               dbDrpFKAsNFKTblsFKNameColConstraintsDataObj[tblName] = dbDrpFKAsNFKTblsNewFKNameColConstraintsDataObj[tblName];
            else:
                dbDrpFKAsNFKTblsFKNameColConstraintsDataObj[tblName].update(dbDrpFKAsNFKTblsNewFKNameColConstraintsDataObj[tblName]);

        for tblName in dbDrpFKAsNFKTblsFKNameNewColsConstraintsDataObj:
            isTblExist = iskeynameExistInDictObj(dbDrpFKAsNFKTblsFKNameColConstraintsDataObj, tblName);
            if isTblExist == False:
               dbDrpFKAsNFKTblsFKNameColConstraintsDataObj[tblName] = dbDrpFKAsNFKTblsFKNameNewColsConstraintsDataObj[tblName];
            else:
                dbDrpFKAsNFKTblsFKNameColConstraintsDataObj[tblName].update(dbDrpFKAsNFKTblsFKNameNewColsConstraintsDataObj[tblName]);
   
        for tblName in dbDrpFKAsNFKTblsNewIndxNameDataObj:
            isTblExist = iskeynameExistInDictObj(dbDrpNFKTblsAllIndxNameDataObj, tblName);
            if isTblExist == False:
               dbDrpFKAsNFKTblsAllIndxNameDataObj[tblName] = dbDrpFKAsNFKTblsNewIndxNameDataObj[tblName];
            else:
                dbDrpFKAsNFKTblsAllIndxNameDataObj[tblName].update(dbDrpFKAsNFKTblsNewIndxNameDataObj[tblName]);

        for tblName in dbDrpFKAsNFKTblIndxNewColsDataObj:
            isTblExist = iskeynameExistInDictObj(dbDrpFKAsNFKTblsAllIndxNameDataObj, tblName);
            if isTblExist == False:
               dbDrpFKAsNFKTblsAllIndxNameDataObj[tblName] = dbDrpFKAsNFKTblIndxNewColsDataObj[tblName];
            else:
                dbDrpFKAsNFKTblsAllIndxNameDataObj[tblName].update(dbDrpFKAsNFKTblIndxNewColsDataObj[tblName]);
         
        ### remove index/foreign table name, when whole table is removing ###

        for tblName in dbDrpFKAsNFKTblsDataObj:
            isIndxTblExist = iskeynameExistInDictObj(dbDrpFKAsNFKTblsAllIndxNameDataObj, tblName);
            isFKTblExist = iskeynameExistInDictObj(dbDrpFKAsNFKTblsFKNameColConstraintsDataObj, tblName);
            if isIndxTblExist == True:
               del dbDrpFKAsNFKTblsAllIndxNameDataObj[tblName];
            if isFKTblExist == True:
               del dbDrpFKAsNFKTblsFKNameColConstraintsDataObj[tblName];

        ### remove foreign keys name, when whole table is not removing ###
        
        for tblName in dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj:
            isDropFKTblExist = iskeynameExistInDictObj(dbDrpFKAsNFKTblsFKNameColConstraintsDataObj, tblName);
            if isDropFKTblExist == True:
               updationAllFKDataObj = dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj[tblName];
               for FKName in updationAllFKDataObj:
                   isDropFKExist = iskeynameExistInDictObj(dbDrpFKAsNFKTblsFKNameColConstraintsDataObj[tblName], FKName);
                   if isDropFKExist == True:
                      del dbDrpFKAsNFKTblsFKNameColConstraintsDataObj[tblName][FKName];
               if len(dbDrpFKAsNFKTblsFKNameColConstraintsDataObj[tblName])<=0: 
                  del dbDrpFKAsNFKTblsFKNameColConstraintsDataObj[tblName];


        ### remove indexes name, when whole table is not removing ###
  
        for tblName in dbFKAsNFKTblIndxUpdationDataObj:
            isDropIndxTblExist = iskeynameExistInDictObj(dbDrpFKAsNFKTblsAllIndxNameDataObj, tblName);
            if isDropIndxTblExist == True:
               updationAllIndexesDataObj = dbFKAsNFKTblIndxUpdationDataObj[tblName];
               for indxName in updationAllIndexesDataObj:
                   isDropIndxExist = iskeynameExistInDictObj(dbDrpFKAsNFKTblsAllIndxNameDataObj[tblName], indxName);
                   if isDropIndxExist == True:
                      del dbDrpFKAsNFKTblsAllIndxNameDataObj[tblName][indxName];
               if len(dbDrpFKAsNFKTblsAllIndxNameDataObj[tblName])<=0 :
                  del dbDrpFKAsNFKTblsAllIndxNameDataObj[tblName];



        ### collecting unique fk types table indexes/foreign keys to drop ###
           
        for tblName in dbDrpFKTblsNewFKNameColConstraintsDataObj:
            isTblExist = iskeynameExistInDictObj(dbDrpFKTblsFKNameColConstraintsDataObj, tblName);
            if isTblExist == False:
               dbDrpFKTblsFKNameColConstraintsDataObj[tblName] = dbDrpFKTblsNewFKNameColConstraintsDataObj[tblName];
            else:
                dbDrpFKTblsFKNameColConstraintsDataObj[tblName].update(dbDrpFKTblsNewFKNameColConstraintsDataObj[tblName]);

        for tblName in dbDrpFKTblsFKNameNewColsConstraintsDataObj:
            isTblExist = iskeynameExistInDictObj(dbDrpFKTblsFKNameColConstraintsDataObj, tblName);
            if isTblExist == False:
               dbDrpFKTblsFKNameColConstraintsDataObj[tblName] = dbDrpFKTblsFKNameNewColsConstraintsDataObj[tblName];
            else:
                dbDrpFKTblsFKNameColConstraintsDataObj[tblName].update(dbDrpFKTblsFKNameNewColsConstraintsDataObj[tblName]);
   
        for tblName in dbDrpFKTblsNewIndxNameDataObj:
            isTblExist = iskeynameExistInDictObj(dbDrpFKTblsAllIndxNameDataObj, tblName);
            if isTblExist == False:
               dbDrpFKTblsAllIndxNameDataObj[tblName] = dbDrpFKTblsNewIndxNameDataObj[tblName];
            else:
                dbDrpFKTblsAllIndxNameDataObj[tblName].update(dbDrpFKTblsNewIndxNameDataObj[tblName]);

        for tblName in dbDrpFKTblIndxNewColsDataObj:
            isTblExist = iskeynameExistInDictObj(dbDrpFKTblsAllIndxNameDataObj, tblName);
            if isTblExist == False:
               dbDrpFKTblsAllIndxNameDataObj[tblName] = dbDrpFKTblIndxNewColsDataObj[tblName];
            else:
                dbDrpFKTblsAllIndxNameDataObj[tblName].update(dbDrpFKTblIndxNewColsDataObj[tblName]);

        for tblName in dbDrpFKTblsDataObj:
            isIndxTblExist = iskeynameExistInDictObj(dbDrpFKTblsAllIndxNameDataObj, tblName);
            isFKTblExist = iskeynameExistInDictObj(dbDrpFKTblsFKNameColConstraintsDataObj, tblName);
            if isIndxTblExist == True:
               del dbDrpFKTblsAllIndxNameDataObj[tblName];
            if isFKTblExist == True:
               del dbDrpFKTblsFKNameColConstraintsDataObj[tblName];

        ### remove foreign keys name, when whole table is not removing ###
        
        for tblName in dbFKTblsFKNameColConstraintsUpdationDataObj:
            isDropFKTblExist = iskeynameExistInDictObj(dbDrpFKTblsFKNameColConstraintsDataObj, tblName);
            if isDropFKTblExist == True:
               updationAllFKDataObj = dbFKTblsFKNameColConstraintsUpdationDataObj[tblName];
               for FKName in updationAllFKDataObj:
                   isDropFKExist = iskeynameExistInDictObj(dbDrpFKTblsFKNameColConstraintsDataObj[tblName], FKName);
                   if isDropFKExist == True:
                      del dbDrpFKTblsFKNameColConstraintsDataObj[tblName][FKName];
               if len(dbDrpFKTblsFKNameColConstraintsDataObj[tblName])<=0: 
                  del dbDrpFKTblsFKNameColConstraintsDataObj[tblName];


        ### remove indexes name, when whole table is not removing ###
  
        for tblName in dbFkTblIndxUpdationDataObj:
            isDropIndxTblExist = iskeynameExistInDictObj(dbDrpFKTblsAllIndxNameDataObj, tblName);
            if isDropIndxTblExist == True:
               updationAllIndexesDataObj = dbFkTblIndxUpdationDataObj[tblName];
               for indxName in updationAllIndexesDataObj:
                   isDropIndxExist = iskeynameExistInDictObj(dbDrpFKTblsAllIndxNameDataObj[tblName], indxName);
                   if isDropIndxExist == True:
                      del dbDrpFKTblsAllIndxNameDataObj[tblName][indxName];
               if len(dbDrpFKTblsAllIndxNameDataObj[tblName])<=0 :
                  del dbDrpFKTblsAllIndxNameDataObj[tblName];



        ### section related to source server and overwriting keys ###

        if againstSvr == "SrcSvr" :
            
           dbDataObj['srcDbDrpNFKTblsAllIndxNameDataObj'] = dbDrpNFKTblsAllIndxNameDataObj;
           dbDataObj['srcDbDrpNFKTblsNewIndxNameDataObj'] = {};
           dbDataObj['srcDbDrpNFKTblIndxNewColsDataObj'] = {};

           dbDataObj['srcDbDrpFKAsNFKTblsFKNameColConstraintsDataObj']= dbDrpFKAsNFKTblsFKNameColConstraintsDataObj;
           dbDataObj['srcDbDrpFKAsNFKTblsNewFKNameColConstraintsDataObj'] = {};
           dbDataObj['srcDbDrpFKAsNFKTblsFKNameNewColsConstraintsDataObj'] = {};
           dbDataObj['srcDbDrpFKAsNFKTblsAllIndxNameDataObj'] = dbDrpFKAsNFKTblsAllIndxNameDataObj;
           dbDataObj['srcDbDrpFKAsNFKTblsNewIndxNameDataObj'] = {};
           dbDataObj['srcDbDrpFKAsNFKTblIndxNewColsDataObj'] = {};

           dbDataObj['srcDbDrpFKTblsFKNameColConstraintsDataObj'] = dbDrpFKTblsFKNameColConstraintsDataObj;
           dbDataObj['srcDbDrpFKTblsNewFKNameColConstraintsDataObj'] = {};
           dbDataObj['srcDbDrpFKTblsFKNameNewColsConstraintsDataObj'] = {};
           dbDataObj['srcDbDrpFKTblsAllIndxNameDataObj'] = dbDrpFKTblsAllIndxNameDataObj;
           dbDataObj['srcDbDrpFKAsNFKTblsNewIndxNameDataObj'] = {};
           dbDataObj['srcDbDrpFKAsNFKTblIndxNewColsDataObj'] = {};

 
        ### section related to destination server and overwriting keys ###

        if againstSvr == "DstSvr" :
            
           dbDataObj['dstDbDrpNFKTblsAllIndxNameDataObj'] = dbDrpNFKTblsAllIndxNameDataObj;
           dbDataObj['dstDbDrpNFKTblsNewIndxNameDataObj'] = {};
           dbDataObj['dstDbDrpNFKTblIndxNewColsDataObj'] = {};

           dbDataObj['dstDbDrpFKAsNFKTblsFKNameColConstraintsDataObj']= dbDrpFKAsNFKTblsFKNameColConstraintsDataObj;
           dbDataObj['dstDbDrpFKAsNFKTblsNewFKNameColConstraintsDataObj'] = {};
           dbDataObj['dstDbDrpFKAsNFKTblsFKNameNewColsConstraintsDataObj'] = {};
           dbDataObj['dstDbDrpFKAsNFKTblsAllIndxNameDataObj'] = dbDrpFKAsNFKTblsAllIndxNameDataObj;
           dbDataObj['dstDbDrpFKAsNFKTblsNewIndxNameDataObj'] = {};
           dbDataObj['dstDbDrpFKAsNFKTblIndxNewColsDataObj'] = {};

           dbDataObj['dstDbDrpFKTblsFKNameColConstraintsDataObj'] = dbDrpFKTblsFKNameColConstraintsDataObj;
           dbDataObj['dstDbDrpFKTblsNewFKNameColConstraintsDataObj'] = {};
           dbDataObj['dstDbDrpFKTblsFKNameNewColsConstraintsDataObj'] = {};
           dbDataObj['dstDbDrpFKTblsAllIndxNameDataObj'] = dbDrpFKTblsAllIndxNameDataObj;
           dbDataObj['dstDbDrpFKAsNFKTblsNewIndxNameDataObj'] = {};
           dbDataObj['dstDbDrpFKAsNFKTblIndxNewColsDataObj'] = {};


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return dbDataObj;


### handle processing to extract uniq add/update infoschemas changes about Db ###

def handleProcsngToExtractUniqAddUpdateDbSchemasChanges(againstSvr, dbDataObj):

    try:

        dbNewNFKTblsDataObj = {};
        dbNewNFKTblsAllIndxNameDataObj = {};
        dbNFKTblsNewIndxNameDataObj = {};
        dbNFKTblIndxNewColsDataObj = {};
        dbNFKTblIndxColsChangedDataObj = {};
        dbNFKTblIndxCreationDataObj = {};
        dbNFKTblIndxUpdationDataObj = {};


        dbNewFKAsNFKTblsDataObj = {}; 
        dbNewFKAsNFKTblsFKNameColConstraintsDataObj = {}; 
        dbFKAsNFKTblsNewFKNameColConstraintsDataObj = {};
        dbFKAsNFKTblsFKNameNewColsConstraintsDataObj = {};
        dbFKAsNFKTblsFKNameColConstraintsDefDataObj = {};
        dbFKAsNFKTblsFKNameColConstraintsCreationDataObj = {}; 
        dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj = {}; 
        dbNewFKAsNFKTblsAllIndxNameDataObj = {};
        dbFKAsNFKTblsNewIndxNameDataObj = {};
        dbFKAsNFKTblIndxNewColsDataObj = {};
        dbFKAsNFKTblIndxColsChangedDataObj = {};
        dbFKAsNFKTblsIndxCreationDataObj = {};
        dbFKAsNFKTblIndxUpdationDataObj = {};

        
        dbNewFKTblsDataObj = {}; 
        dbNewFKTblsFKNameColConstraintsDataObj = {}; 
        dbFKTblsNewFKNameColConstraintsDataObj = {};
        dbFKTblsFKNameNewColsConstraintsDataObj = {};
        dbFKTblsFKNameColConstraintsDefDataObj = {};
        dbFKTblsFKNameColConstraintsCreationDataObj = {};
        dbFKTblsFKNameColConstraintsUpdationDataObj = {};
        dbNewFKTblsAllIndxNameDataObj = {};
        dbFKTblsNewIndxNameDataObj = {};
        dbFkTblIndxNewColsDataObj = {};
        dbFkTblIndxColsChangedDataObj = {};
        dbFKTblsIndxCreationDataObj = {};
        dbFkTblIndxUpdationDataObj = {};

   
        ### section related to source server extracting data ###
  
        if againstSvr == "SrcSvr" :

           ### section related to nfk types tables ###

           dbNewNFKTblsDataObj = dbDataObj['srcDbNewNFKTblsDataObj']; 
           dbNewNFKTblsAllIndxNameDataObj = dbDataObj['srcDbNewNFKTblsAllIndxNameDataObj'];
           dbNFKTblsNewIndxNameDataObj = dbDataObj['srcDbNFKTblsNewIndxNameDataObj'];
           dbNFKTblIndxNewColsDataObj = dbDataObj['srcDbNFKTblIndxNewColsDataObj'];
           dbNFKTblIndxColsChangedDataObj = dbDataObj['srcDbNFKTblIndxColsChangedDataObj'];
           dbNFKTblIndxCreationDataObj = dbNewNFKTblsAllIndxNameDataObj;


           ### section related to fk as nfk types tables ###

           dbNewFKAsNFKTblsDataObj = dbDataObj['srcDbNewFKAsNFKTblsDataObj']; 
           dbNewFKAsNFKTblsFKNameColConstraintsDataObj = dbDataObj['srcDbNewFKAsNFKTblsFKNameColConstraintsDataObj'];
           dbFKAsNFKTblsNewFKNameColConstraintsDataObj = dbDataObj['srcDbFKAsNFKTblsNewFKNameColConstraintsDataObj'];
           dbFKAsNFKTblsFKNameNewColsConstraintsDataObj = dbDataObj['srcDbFKAsNFKTblsFKNameNewColsConstraintsDataObj'];
           dbFKAsNFKTblsFKNameColConstraintsDefDataObj = dbDataObj['srcDbFKAsNFKTblsFKNameColConstraintsDefDataObj'];
           dbFKAsNFKTblsFKNameColConstraintsCreationDataObj = dbNewFKAsNFKTblsFKNameColConstraintsDataObj;
           dbNewFKAsNFKTblsAllIndxNameDataObj = dbDataObj['srcDbNewFKAsNFKTblsAllIndxNameDataObj'];
           dbFKAsNFKTblsNewIndxNameDataObj = dbDataObj['srcDbFKAsNFKTblsNewIndxNameDataObj'];
           dbFKAsNFKTblIndxNewColsDataObj = dbDataObj['srcDbFKAsNFKTblIndxNewColsDataObj'];
           dbFKAsNFKTblIndxColsChangedDataObj = dbDataObj['srcDbFKAsNFKTblIndxColsChangedDataObj'];
           dbFKAsNFKTblsIndxCreationDataObj = dbNewFKAsNFKTblsAllIndxNameDataObj; 
           
           ### section related to fk types tables ###
 
           dbNewFKTblsDataObj = dbDataObj['srcDbNewFKTblsDataObj'];
           dbNewFKTblsFKNameColConstraintsDataObj = dbDataObj['srcDbNewFKTblsFKNameColConstraintsDataObj'];
           dbFKTblsNewFKNameColConstraintsDataObj = dbDataObj['srcDbFKTblsNewFKNameColConstraintsDataObj'];
           dbFKTblsFKNameNewColsConstraintsDataObj = dbDataObj['srcDbFKTblsFKNameNewColsConstraintsDataObj'];
           dbFKTblsFKNameColConstraintsDefDataObj = dbDataObj['srcDbFKTblsFKNameColConstraintsDefDataObj'];
           dbFKTblsFKNameColConstraintsCreationDataObj = dbNewFKTblsFKNameColConstraintsDataObj; 
           dbNewFKTblsAllIndxNameDataObj = dbDataObj['srcDbNewFKTblsAllIndxNameDataObj'];
           dbFKTblsNewIndxNameDataObj = dbDataObj['srcDbFKTblsNewIndxNameDataObj'];
           dbFkTblIndxNewColsDataObj = dbDataObj['srcDbFkTblIndxNewColsDataObj'];
           dbFkTblIndxColsChangedDataObj = dbDataObj['srcDbFkTblIndxColsChangedDataObj'];
           dbFKTblsIndxCreationDataObj = dbNewFKTblsAllIndxNameDataObj;


        ### section related to destination server ###
  
        if againstSvr == "DstSvr" :


           ### section related to nfk types tables ###

           dbNewNFKTblsDataObj = dbDataObj['dstDbNewNFKTblsDataObj'];
           dbNewNFKTblsAllIndxNameDataObj = dbDataObj['dstDbNewNFKTblsAllIndxNameDataObj'];
           dbNFKTblsNewIndxNameDataObj = dbDataObj['dstDbNFKTblsNewIndxNameDataObj'];
           dbNFKTblIndxNewColsDataObj = dbDataObj['dstDbNFKTblIndxNewColsDataObj'];
           dbNFKTblIndxColsChangedDataObj = dbDataObj['dstDbNFKTblIndxColsChangedDataObj'];
           dbNFKTblIndxCreationDataObj = dbNewNFKTblsAllIndxNameDataObj;

           ### section related to fk as nfk types tables ###
 
           dbNewFKAsNFKTblsDataObj = dbDataObj['dstDbNewFKAsNFKTblsDataObj'];
           dbNewFKAsNFKTblsFKNameColConstraintsDataObj = dbDataObj['dstDbNewFKAsNFKTblsFKNameColConstraintsDataObj'];
           dbFKAsNFKTblsNewFKNameColConstraintsDataObj = dbDataObj['dstDbFKAsNFKTblsNewFKNameColConstraintsDataObj'];
           dbFKAsNFKTblsFKNameNewColsConstraintsDataObj = dbDataObj['dstDbFKAsNFKTblsFKNameNewColsConstraintsDataObj'];
           dbFKAsNFKTblsFKNameColConstraintsDefDataObj = dbDataObj['dstDbFKAsNFKTblsFKNameColConstraintsDefDataObj'];
           dbFKAsNFKTblsFKNameColConstraintsCreationDataObj = dbNewFKAsNFKTblsFKNameColConstraintsDataObj;
           dbNewFKAsNFKTblsAllIndxNameDataObj = dbDataObj['dstDbNewFKAsNFKTblsAllIndxNameDataObj'];
           dbFKAsNFKTblsNewIndxNameDataObj = dbDataObj['dstDbFKAsNFKTblsNewIndxNameDataObj'];
           dbFKAsNFKTblIndxNewColsDataObj = dbDataObj['dstDbFKAsNFKTblIndxNewColsDataObj'];
           dbFKAsNFKTblIndxColsChangedDataObj = dbDataObj['dstDbFKAsNFKTblIndxColsChangedDataObj'];
           dbFKAsNFKTblsIndxCreationDataObj = dbNewFKAsNFKTblsAllIndxNameDataObj;


           ### section related to fk types tables ###

           dbNewFKTblsDataObj = dbDataObj['dstDbNewFKTblsDataObj'];
           dbNewFKTblsFKNameColConstraintsDataObj = dbDataObj['dstDbNewFKTblsFKNameColConstraintsDataObj'];
           dbFKTblsNewFKNameColConstraintsDataObj = dbDataObj['dstDbFKTblsNewFKNameColConstraintsDataObj'];
           dbFKTblsFKNameNewColsConstraintsDataObj = dbDataObj['dstDbFKTblsFKNameNewColsConstraintsDataObj'];
           dbFKTblsFKNameColConstraintsDefDataObj = dbDataObj['dstDbFKTblsFKNameColConstraintsDefDataObj'];
           dbFKTblsFKNameColConstraintsCreationDataObj = dbNewFKTblsFKNameColConstraintsDataObj;
           dbNewFKTblsAllIndxNameDataObj = dbDataObj['dstDbNewFKTblsAllIndxNameDataObj'];
           dbFKTblsNewIndxNameDataObj = dbDataObj['dstDbFKTblsNewIndxNameDataObj'];
           dbFkTblIndxNewColsDataObj = dbDataObj['dstDbFkTblIndxNewColsDataObj'];
           dbFkTblIndxColsChangedDataObj = dbDataObj['dstDbFkTblIndxColsChangedDataObj'];
           dbFKTblsIndxCreationDataObj = dbNewFKTblsAllIndxNameDataObj;


        ### collecting unqiue nfk types table index to create ###

        for tblName in dbNFKTblsNewIndxNameDataObj:
            isTblExist = iskeynameExistInDictObj(dbNFKTblIndxCreationDataObj, tblName);
            if isTblExist == False:
               dbNFKTblIndxCreationDataObj[tblName] = dbNFKTblsNewIndxNameDataObj[tblName];
            else:
                dbNFKTblIndxCreationDataObj[tblName].update(dbNFKTblsNewIndxNameDataObj[tblName]);
           
        ### collecting unqiue nfk types table index to first drop and recreate ###

        for tblName in dbNFKTblIndxNewColsDataObj:
            isTblExist = iskeynameExistInDictObj(dbNFKTblIndxUpdationDataObj, tblName);
            if isTblExist == False:
               dbNFKTblIndxUpdationDataObj[tblName] = dbNFKTblIndxNewColsDataObj[tblName];
            else:
                dbNFKTblIndxUpdationDataObj[tblName].update(dbNFKTblIndxNewColsDataObj[tblName]);

        for tblName in dbNFKTblIndxColsChangedDataObj:
            isTblExist = iskeynameExistInDictObj(dbNFKTblIndxUpdationDataObj, tblName);
            if isTblExist == False:
               dbNFKTblIndxUpdationDataObj[tblName] = dbNFKTblIndxColsChangedDataObj[tblName];
            else:
                dbNFKTblIndxUpdationDataObj[tblName].update(dbNFKTblIndxColsChangedDataObj[tblName]);


        ### finally collecting unqiue nfk types table index creation/updation ###

        for tblName in dbNewNFKTblsDataObj:
            isIndxCreationTblExist = iskeynameExistInDictObj(dbNFKTblIndxCreationDataObj, tblName);
            isIndxUpdationTblExist = iskeynameExistInDictObj(dbNFKTblIndxUpdationDataObj, tblName);
            if isIndxCreationTblExist == True:
               del dbNFKTblIndxCreationDataObj[tblName];
            if isIndxUpdationTblExist == True:
               del dbNFKTblIndxUpdationDataObj[tblName];
  


        ### collecting unqiue fk as nfk types table index to create ###

        for tblName in dbFKAsNFKTblsNewIndxNameDataObj:
            isTblExist = iskeynameExistInDictObj(dbFKAsNFKTblsIndxCreationDataObj, tblName);
            if isTblExist == False:
               dbFKAsNFKTblsIndxCreationDataObj[tblName] = dbFKAsNFKTblsNewIndxNameDataObj[tblName];
            else:
                dbFKAsNFKTblsIndxCreationDataObj[tblName].update(dbFKAsNFKTblsNewIndxNameDataObj[tblName]);

        ### collecting unqiue fk as nfk types table index to first drop and recreate ###

        for tblName in dbFKAsNFKTblIndxNewColsDataObj:
            isTblExist = iskeynameExistInDictObj(dbFKAsNFKTblIndxUpdationDataObj, tblName);
            if isTblExist == False:
               dbFKAsNFKTblIndxUpdationDataObj[tblName] = dbFKAsNFKTblIndxNewColsDataObj[tblName];
            else:
                dbFKAsNFKTblIndxUpdationDataObj[tblName].update(dbFKAsNFKTblIndxNewColsDataObj[tblName]);

        for tblName in dbFKAsNFKTblIndxColsChangedDataObj:
            isTblExist = iskeynameExistInDictObj(dbFKAsNFKTblIndxUpdationDataObj, tblName);
            if isTblExist == False:
               dbFKAsNFKTblIndxUpdationDataObj[tblName] = dbFKAsNFKTblIndxColsChangedDataObj[tblName];
            else:
                dbFKAsNFKTblIndxUpdationDataObj[tblName].update(dbFKAsNFKTblIndxColsChangedDataObj[tblName]);

        ### collecting unqiue fk as nfk types table foreign keys to create ###

        for tblName in dbFKAsNFKTblsNewFKNameColConstraintsDataObj:
            isTblExist = iskeynameExistInDictObj(dbFKAsNFKTblsFKNameColConstraintsCreationDataObj, tblName);
            if isTblExist == False:
               dbFKAsNFKTblsFKNameColConstraintsCreationDataObj[tblName] = dbFKAsNFKTblsNewFKNameColConstraintsDataObj[tblName];
            else:
                dbFKAsNFKTblsFKNameColConstraintsCreationDataObj[tblName].update(dbFKAsNFKTblsNewFKNameColConstraintsDataObj[tblName]);

        ### collecting unqiue fk as nfk types table foreign keys to first drop and recreate ###

        for tblName in dbFKAsNFKTblsFKNameNewColsConstraintsDataObj:
            isTblExist = iskeynameExistInDictObj(dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj, tblName);
            if isTblExist == False:
               dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj[tblName] = dbFKAsNFKTblsFKNameNewColsConstraintsDataObj[tblName];
            else:
                dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj[tblName].update(dbFKAsNFKTblsFKNameNewColsConstraintsDataObj[tblName]);

        ### collecting unqiue fk as nfk types table foreign keys to first drop and recreate ###

        for tblName in dbFKAsNFKTblsFKNameColConstraintsDefDataObj:
            isTblExist = iskeynameExistInDictObj(dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj, tblName);
            if isTblExist == False:
               dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj[tblName] = dbFKAsNFKTblsFKNameColConstraintsDefDataObj[tblName];
            else:
                dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj[tblName].update(dbFKAsNFKTblsFKNameColConstraintsDefDataObj[tblName]); 
 

        ### finally collecting fk as nfk types table unqiue index/foriegn keys to creation/updation ### 

        for tblName in dbNewFKAsNFKTblsDataObj:
            isIndxCreationTblExist = iskeynameExistInDictObj(dbFKAsNFKTblsIndxCreationDataObj, tblName);
            isIndxUpdationTblExist = iskeynameExistInDictObj(dbFKAsNFKTblIndxUpdationDataObj, tblName);
            isFKCreationTblExist = iskeynameExistInDictObj(dbFKAsNFKTblsFKNameColConstraintsCreationDataObj, tblName);
            isFKUpdationTblExist = iskeynameExistInDictObj(dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj, tblName);
            if isIndxCreationTblExist == True:
               del dbFKAsNFKTblsIndxCreationDataObj[tblName];
            if isIndxUpdationTblExist == True:
               del dbFKAsNFKTblIndxUpdationDataObj[tblName];
            if isFKCreationTblExist == True:
               del dbFKAsNFKTblsFKNameColConstraintsCreationDataObj[tblName];
            if isFKUpdationTblExist == True:
               del dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj[tblName];   
 


        ### collecting unqiue fk types table index to create ###

        for tblName in dbFKTblsNewIndxNameDataObj:
            isTblExist = iskeynameExistInDictObj(dbFKTblsIndxCreationDataObj, tblName);
            if isTblExist == False:
               dbFKTblsIndxCreationDataObj[tblName] = dbFKTblsNewIndxNameDataObj[tblName];
            else:
                dbFKTblsIndxCreationDataObj[tblName].update(dbFKTblsNewIndxNameDataObj[tblName]);
           
        ### collecting unqiue fk types table index to first drop and recreate ###

        for tblName in dbFkTblIndxNewColsDataObj:
            isTblExist = iskeynameExistInDictObj(dbFkTblIndxUpdationDataObj, tblName);
            if isTblExist == False:
               dbFkTblIndxUpdationDataObj[tblName] = dbFkTblIndxNewColsDataObj[tblName];
            else:
                dbFkTblIndxUpdationDataObj[tblName].update(dbFkTblIndxNewColsDataObj[tblName]);

        for tblName in dbFkTblIndxColsChangedDataObj:
            isTblExist = iskeynameExistInDictObj(dbFkTblIndxUpdationDataObj, tblName);
            if isTblExist == False:
               dbFkTblIndxUpdationDataObj[tblName] = dbFkTblIndxColsChangedDataObj[tblName];
            else:
                dbFkTblIndxUpdationDataObj[tblName].update(dbFkTblIndxColsChangedDataObj[tblName]); 

        ### collecting unqiue fk types table foreign keys to create ###

        for tblName in dbFKTblsNewFKNameColConstraintsDataObj:
            isTblExist = iskeynameExistInDictObj(dbFKTblsFKNameColConstraintsCreationDataObj, tblName);
            if isTblExist == False:
               dbFKTblsFKNameColConstraintsCreationDataObj[tblName] = dbFKTblsNewFKNameColConstraintsDataObj[tblName];
            else:
                dbFKTblsFKNameColConstraintsCreationDataObj[tblName].update(dbFKTblsNewFKNameColConstraintsDataObj[tblName]);

        ### collecting unqiue fk types table foreign keys to first drop and recreate ###

        for tblName in dbFKTblsFKNameNewColsConstraintsDataObj:
            isTblExist = iskeynameExistInDictObj(dbFKTblsFKNameColConstraintsUpdationDataObj, tblName);
            if isTblExist == False:
               dbFKTblsFKNameColConstraintsUpdationDataObj[tblName] = dbFKTblsFKNameNewColsConstraintsDataObj[tblName];
            else:
                dbFKTblsFKNameColConstraintsUpdationDataObj[tblName].update(dbFKTblsFKNameNewColsConstraintsDataObj[tblName]);

        ### collecting unqiue fk types table foreign keys to first drop and recreate ###

        for tblName in dbFKTblsFKNameColConstraintsDefDataObj:
            isTblExist = iskeynameExistInDictObj(dbFKTblsFKNameColConstraintsUpdationDataObj, tblName);
            if isTblExist == False:
               dbFKTblsFKNameColConstraintsUpdationDataObj[tblName] = dbFKTblsFKNameColConstraintsDefDataObj[tblName];
            else:
                dbFKTblsFKNameColConstraintsUpdationDataObj[tblName].update(dbFKTblsFKNameColConstraintsDefDataObj[tblName]);


        ### finally collecting fk types table unqiue index/foriegn keys to creation/updation ### 

        for tblName in dbNewFKTblsDataObj:
            isIndxCreationTblExist = iskeynameExistInDictObj(dbFKTblsIndxCreationDataObj, tblName);
            isIndxUpdationTblExist = iskeynameExistInDictObj(dbFkTblIndxUpdationDataObj, tblName);
            isFKCreationTblExist = iskeynameExistInDictObj(dbFKTblsFKNameColConstraintsCreationDataObj, tblName);
            isFKUpdationTblExist = iskeynameExistInDictObj(dbFKTblsFKNameColConstraintsUpdationDataObj, tblName);
            if isIndxCreationTblExist == True:
               del dbFKTblsIndxCreationDataObj[tblName];
            if isIndxUpdationTblExist == True:
               del dbFkTblIndxUpdationDataObj[tblName];
            if isFKCreationTblExist == True:
               del dbFKTblsFKNameColConstraintsCreationDataObj[tblName];
            if isFKUpdationTblExist == True:
               del dbFKTblsFKNameColConstraintsUpdationDataObj[tblName];



        ### section related to source server overwrite keys ###
  
        if againstSvr == "SrcSvr" :

           dbDataObj['srcDbNewNFKTblsAllIndxNameDataObj'] = {};
           dbDataObj['srcDbNFKTblsNewIndxNameDataObj'] = {};
           dbDataObj['srcDbNFKTblIndxNewColsDataObj'] = {};
           dbDataObj['srcDbNFKTblIndxColsChangedDataObj'] = {};
           dbDataObj['srcDbNFKTblIndxCreationDataObj'] = dbNFKTblIndxCreationDataObj;
           dbDataObj['srcDbNFKTblIndxUpdationDataObj'] = dbNFKTblIndxUpdationDataObj;  

           dbDataObj['srcDbNewFKAsNFKTblsFKNameColConstraintsDataObj'] = {};
           dbDataObj['srcDbFKAsNFKTblsNewFKNameColConstraintsDataObj'] = {};
           dbDataObj['srcDbFKAsNFKTblsFKNameNewColsConstraintsDataObj'] = {};
           dbDataObj['srcDbFKAsNFKTblsFKNameColConstraintsDefDataObj'] = {};
           dbDataObj['srcDbFKAsNFKTblsFKNameColConstraintsCreationDataObj'] = dbFKAsNFKTblsFKNameColConstraintsCreationDataObj;
           dbDataObj['srcDbFKAsNFKTblsFKNameColConstraintsUpdationDataObj'] = dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj;

           dbDataObj['srcDbNewFKAsNFKTblsAllIndxNameDataObj'] = {};
           dbDataObj['srcDbFKAsNFKTblsNewIndxNameDataObj'] = {};
           dbDataObj['srcDbFKAsNFKTblIndxNewColsDataObj'] = {};
           dbDataObj['srcDbFKAsNFKTblIndxColsChangedDataObj'] = {};
           dbDataObj['srcDbFKAsNFKTblsIndxCreationDataObj'] = dbFKAsNFKTblsIndxCreationDataObj;
           dbDataObj['srcDbFKAsNFKTblIndxUpdationDataObj'] = dbFKAsNFKTblIndxUpdationDataObj;  
           
           dbDataObj['srcDbNewFKTblsFKNameColConstraintsDataObj'] = {};
           dbDataObj['srcDbFKTblsNewFKNameColConstraintsDataObj'] = {};
           dbDataObj['srcDbFKTblsFKNameNewColsConstraintsDataObj'] = {};
           dbDataObj['srcDbFKTblsFKNameColConstraintsDefDataObj'] = {};
           dbDataObj['srcDbFKTblsFKNameColConstraintsCreationDataObj'] = dbFKTblsFKNameColConstraintsCreationDataObj;
           dbDataObj['srcDbFKTblsFKNameColConstraintsUpdationDataObj'] = dbFKTblsFKNameColConstraintsUpdationDataObj; 
       
           dbDataObj['srcDbNewFKTblsAllIndxNameDataObj'] = {};
           dbDataObj['srcDbFKTblsNewIndxNameDataObj'] = {};
           dbDataObj['srcDbFkTblIndxNewColsDataObj'] = {};
           dbDataObj['srcDbFkTblIndxColsChangedDataObj'] = {};
           dbDataObj['srcDbFKTblsIndxCreationDataObj'] = dbFKTblsIndxCreationDataObj;
           dbDataObj['srcDbFkTblIndxUpdationDataObj'] = dbFkTblIndxUpdationDataObj; 


        ### section related to destination server overwrite keys ###
  
        if againstSvr == "DstSvr" :

           dbDataObj['dstDbNewNFKTblsAllIndxNameDataObj'] = {};
           dbDataObj['dstDbNFKTblsNewIndxNameDataObj'] = {};
           dbDataObj['dstDbNFKTblIndxNewColsDataObj'] = {};
           dbDataObj['dstDbNFKTblIndxColsChangedDataObj'] = {};
           dbDataObj['dstDbNFKTblIndxCreationDataObj'] = dbNFKTblIndxCreationDataObj;
           dbDataObj['dstDbNFKTblIndxUpdationDataObj'] = dbNFKTblIndxUpdationDataObj;  

           dbDataObj['dstDbNewFKAsNFKTblsFKNameColConstraintsDataObj'] = {};
           dbDataObj['dstDbFKAsNFKTblsNewFKNameColConstraintsDataObj'] = {};
           dbDataObj['dstDbFKAsNFKTblsFKNameNewColsConstraintsDataObj'] = {};
           dbDataObj['dstDbFKAsNFKTblsFKNameColConstraintsDefDataObj'] = {};
           dbDataObj['dstDbFKAsNFKTblsFKNameColConstraintsCreationDataObj'] = dbFKAsNFKTblsFKNameColConstraintsCreationDataObj;
           dbDataObj['dstDbFKAsNFKTblsFKNameColConstraintsUpdationDataObj'] = dbFKAsNFKTblsFKNameColConstraintsUpdationDataObj;

           dbDataObj['dstDbNewFKAsNFKTblsAllIndxNameDataObj'] = {};
           dbDataObj['dstDbFKAsNFKTblsNewIndxNameDataObj'] = {};
           dbDataObj['dstDbFKAsNFKTblIndxNewColsDataObj'] = {};
           dbDataObj['dstDbFKAsNFKTblIndxColsChangedDataObj'] = {};
           dbDataObj['dstDbFKAsNFKTblsIndxCreationDataObj'] = dbFKAsNFKTblsIndxCreationDataObj;
           dbDataObj['dstDbFKAsNFKTblIndxUpdationDataObj'] = dbFKAsNFKTblIndxUpdationDataObj;  
           
           dbDataObj['dstDbNewFKTblsFKNameColConstraintsDataObj'] = {};
           dbDataObj['dstDbFKTblsNewFKNameColConstraintsDataObj'] = {};
           dbDataObj['dstDbFKTblsFKNameNewColsConstraintsDataObj'] = {};
           dbDataObj['dstDbFKTblsFKNameColConstraintsDefDataObj'] = {};
           dbDataObj['dstDbFKTblsFKNameColConstraintsCreationDataObj'] = dbFKTblsFKNameColConstraintsCreationDataObj;
           dbDataObj['dstDbFKTblsFKNameColConstraintsUpdationDataObj'] = dbFKTblsFKNameColConstraintsUpdationDataObj; 
       
           dbDataObj['dstDbNewFKTblsAllIndxNameDataObj'] = {};
           dbDataObj['dstDbFKTblsNewIndxNameDataObj'] = {};
           dbDataObj['dstDbFkTblIndxNewColsDataObj'] = {};
           dbDataObj['dstDbFkTblIndxColsChangedDataObj'] = {};
           dbDataObj['dstDbFKTblsIndxCreationDataObj'] = dbFKTblsIndxCreationDataObj;
           dbDataObj['dstDbFkTblIndxUpdationDataObj'] = dbFkTblIndxUpdationDataObj; 


    except Exception as e:
           handleProcsngAbtErrException("Y");   

    return dbDataObj;

 
### get views definition changed between srcDb & dstDb ###

def getViewsDefChangedInfoBtwnDB(srcDbName,srcDbViewsDataObj,dstDbName,dstDbViewsDataObj,againstSvr):

    viewsDataObj = {};

    try:

       if srcDbName!="" and len(srcDbViewsDataObj)>0 and dstDbName!="" and len(dstDbViewsDataObj)>0:

          global inputArgsDataObj;
          uniqInfoSchemaNameArrBtwnSrcAndDstDbSvr = inputArgsDataObj['uniqInfoSchemaNameArrBtwnSrcAndDstDbSvr'];
          searchStrWithReplaceStrDataObj = dict(('`'+element+'`.', '') for element in uniqInfoSchemaNameArrBtwnSrcAndDstDbSvr);
         
          dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
          dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
          dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
          dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
          dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

          ### found all exisiting views data ###
          allViewsDataObj = {
             viewName: dstDbViewsDataObj[viewName] for viewName in dstDbViewsDataObj if viewName in srcDbViewsDataObj
          }; 

          for viewName in allViewsDataObj: 
 
              srcDbViewDataArr = srcDbViewsDataObj[viewName]['updatedViewData'];
              dstDbViewDataArr = dstDbViewsDataObj[viewName]['updatedViewData'];
              srcDbViewDefDataStr = searchStrAndReplaceStr(srcDbViewDataArr[6], searchStrWithReplaceStrDataObj);
              dstDbViewDefDataStr = searchStrAndReplaceStr(dstDbViewDataArr[6], searchStrWithReplaceStrDataObj);
              
              srcDbRefViewsDataObj = srcDbViewsDataObj[viewName]['refViewDataObj']; 
              refViewsDefChangedDataArr = srcDbRefViewsDataObj['viewNameDefChangedDataArr'];
           
              ### not same definition statement ###

              if srcDbViewDefDataStr != dstDbViewDefDataStr:
                 updatedViewConfig = {
                    'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 
                    'copyDbName': dstDbName, 'copyViewName': viewName
                 };
                 refViewsDefChangedDataArr.append({"refViewConfig": updatedViewConfig, "viewDataArr": dstDbViewDataArr});
                 eachViewDefChangedDataObj = {
                     'updatedViewConfig': srcDbViewsDataObj[viewName]['updatedViewConfig'],
                     'updatedViewData': dstDbViewDataArr, 
                     'orgViewData': srcDbViewsDataObj[viewName]['orgViewData'],
                     'refViewDataObj': {
                        'viewNameDefChangedDataArr': refViewsDefChangedDataArr
                     }
                 }; 
                 viewsDataObj[viewName] = eachViewDefChangedDataObj; 
    

    except Exception as e:
           handleProcsngAbtErrException("Y");


    return viewsDataObj;


### get new views between srcDb & dstDb ###

def getNewViewsInfoBtwnDB(srcDbName,srcDbViewsDataObj,dstDbName,dstDbViewsDataObj,againstSvr):

    viewsDataObj = {};

    try:

       if srcDbName!="" and dstDbName!="":

          dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
          dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
          dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
          dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
          dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

          ### found all new views data ###
          allViewsDataObj = {
             viewName: dstDbViewsDataObj[viewName] for viewName in dstDbViewsDataObj if viewName not in srcDbViewsDataObj
          }; 

          for viewName in allViewsDataObj:

              isViewAlreadyCopiedFrmAnotherDb = 'N'; 
              updatedViewConfig = allViewsDataObj[viewName]['updatedViewConfig'];
              updatedViewConfigLen = len(updatedViewConfig);
              if updatedViewConfigLen > 0:
                 isViewAlreadyCopiedFrmAnotherDb = 'Y';
              if isViewAlreadyCopiedFrmAnotherDb == 'Y':
                 viewsDataObj[viewName] = allViewsDataObj[viewName];
              if isViewAlreadyCopiedFrmAnotherDb == 'N':
                 updatedViewConfig = {
                    'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 
                    'copyDbName': dstDbName, 'copyViewName': viewName
                 };
                 allViewsDataObj[viewName]['updatedViewConfig'] = updatedViewConfig;
                 viewsDataObj[viewName] = allViewsDataObj[viewName];
 
        
    except Exception as e:
           handleProcsngAbtErrException("Y");


    return viewsDataObj;

  

### get routine type routine name def changed between srcDb & dstDb ###

def getRTypeRNameDefChangedInfoBtwnDB(srcDbName,srcDbRoutinesDataObj,dstDbName,dstDbRoutinesDataObj,againstSvr):

    routinesDataObj = {};

    try:

       if srcDbName!="" and len(srcDbRoutinesDataObj)>0 and dstDbName!="" and len(dstDbRoutinesDataObj)>0:

          dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
          dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
          dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
          dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
          dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];
  
          ### found all routines type data ###
          allRoutinesTypeDataObj = {
             routineType: dstDbRoutinesDataObj[routineType]['rTypeAllRoutineNames'] for routineType in dstDbRoutinesDataObj if routineType in srcDbRoutinesDataObj
          }; 

          for routineType in allRoutinesTypeDataObj:

              ### found each routine type ka all routine name
              ### issue can be raised ###

              allRoutinesNameDataObj = {
                 routineName: allRoutinesTypeDataObj[routineType][routineName] for routineName in allRoutinesTypeDataObj[routineType] if routineName in srcDbRoutinesDataObj[routineType]['rTypeAllRoutineNames']
              }; 

              eachRTypeExistRNameDefChangedDataObj = {};

              for routineName in allRoutinesNameDataObj: 
               
                  srcDbRoutineNameDataArr = srcDbRoutinesDataObj[routineType]['rTypeAllRoutineNames'][routineName]['updatedRnameData'];
                  dstDbRoutineNameDataArr = dstDbRoutinesDataObj[routineType]['rTypeAllRoutineNames'][routineName]['updatedRnameData'];
                  srcDbRoutineNameDefDataStr = (srcDbRoutineNameDataArr[3]).strip().replace("\r", "");
                  dstDbRoutineNameDefDataStr = (dstDbRoutineNameDataArr[3]).strip().replace("\r", "");
              
                  srcDbRefRnameDataObj = srcDbRoutinesDataObj[routineType]['rTypeAllRoutineNames'][routineName]['refRnameDataObj']; 
                  refRNameDefChangedDataArr = srcDbRefRnameDataObj['rnameDefChangedDataArr'];
           
                  ### not same definition statement ###

                  if srcDbRoutineNameDefDataStr != dstDbRoutineNameDefDataStr:
                     updatedRnameConfig = {
                         'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 
                         'copyDbName': dstDbName, 'copyRoutineType': routineType, 'copyRoutineName': routineName
                     };
                     refRNameDefChangedDataArr.append({"refRNameConfig": updatedRnameConfig, "rNameDataArr": dstDbRoutineNameDataArr});
                     eachRTypeEachRNameDefChangedDataObj = {
                         'updatedRnameConfig': srcDbRoutinesDataObj[routineType]['rTypeAllRoutineNames'][routineName]['updatedRnameConfig'],
                         'updatedRnameData': dstDbRoutineNameDataArr, 
                         'orgRnameData': srcDbRoutinesDataObj[routineType]['rTypeAllRoutineNames'][routineName]['orgRnameData'],
                         'refRnameDataObj': {
                            'rnameDefChangedDataArr': refRNameDefChangedDataArr
                          }
                     }; 
                     eachRTypeExistRNameDefChangedDataObj[routineName] = eachRTypeEachRNameDefChangedDataObj; 
    

              if len(eachRTypeExistRNameDefChangedDataObj) > 0:
                 routinesDataObj[routineType] = {}; 
                 routinesDataObj[routineType]['rTypeAllRoutineNames'] = eachRTypeExistRNameDefChangedDataObj;

        
    except Exception as e:
           handleProcsngAbtErrException("Y");


    return routinesDataObj;


### get routine type all new routine name between srcDb & dstDb ###

def getRoutineTypeNewRoutinesNameInfoBtwnDB(srcDbName,srcDbRoutinesDataObj,dstDbName,dstDbRoutinesDataObj,againstSvr):

    routinesDataObj = {};

    try:

       if srcDbName!="" and len(srcDbRoutinesDataObj)>0 and dstDbName!="" and len(dstDbRoutinesDataObj)>0:

          dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
          dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
          dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
          dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
          dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

          ### found all same routines type data ###
          allRoutinesTypeDataObj = {
             routineType: dstDbRoutinesDataObj[routineType]['rTypeAllRoutineNames'] for routineType in dstDbRoutinesDataObj if routineType in srcDbRoutinesDataObj
          }; 

          for routineType in allRoutinesTypeDataObj:

              ### found each routine type ka all new routine name ###
              ### issue can be raised ###
 
              allRoutinesNameDataObj = {
                 routineName: allRoutinesTypeDataObj[routineType][routineName] for routineName in allRoutinesTypeDataObj[routineType] if routineName not in srcDbRoutinesDataObj[routineType]['rTypeAllRoutineNames']
              }; 

              eachRTypeAllNewRoutinesNameDataObj = {};

              for routineName in allRoutinesNameDataObj:

                 isRoutineNameAlreadyCopiedFrmAnotherDb = 'N'; 
                 updatedRnameConfig = allRoutinesNameDataObj[routineName]['updatedRnameConfig'];
                 updatedRnameConfigLen = len(updatedRnameConfig);
                 if updatedRnameConfigLen > 0:
                    isRoutineNameAlreadyCopiedFrmAnotherDb = 'Y';
                 if isRoutineNameAlreadyCopiedFrmAnotherDb == 'Y':
                    eachRTypeAllNewRoutinesNameDataObj[routineName] = allRoutinesNameDataObj[routineName];
                 if isRoutineNameAlreadyCopiedFrmAnotherDb == 'N':
                    updatedRnameConfig = {
                      'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 
                      'copyDbName': dstDbName, 'copyRoutineType': routineType, 'copyRoutineName': routineName
                    };
                    allRoutinesNameDataObj[routineName]['updatedRnameConfig'] = updatedRnameConfig;
                    eachRTypeAllNewRoutinesNameDataObj[routineName] = allRoutinesNameDataObj[routineName];
 
              if len(eachRTypeAllNewRoutinesNameDataObj) > 0:
                 routinesDataObj[routineType] = {}; 
                 routinesDataObj[routineType]['rTypeAllRoutineNames'] = eachRTypeAllNewRoutinesNameDataObj;

        
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return routinesDataObj;


### get new routines types between srcDb & dstDb ###

def getNewRoutinesTypeInfoBtwnDB(srcDbName,srcDbRoutinesDataObj,dstDbName,dstDbRoutinesDataObj,againstSvr):

    routinesDataObj = {};

    try:

       if srcDbName!="" and dstDbName!="":

          dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
          dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
          dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
          dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
          dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];
 
          ### found all new routines type data ###
          allRoutinesTypeDataObj = {
             routineType: dstDbRoutinesDataObj[routineType] for routineType in dstDbRoutinesDataObj if routineType not in srcDbRoutinesDataObj
          }; 

          for routineType in allRoutinesTypeDataObj:

              isRoutineTypeAlreadyCopiedFrmAnotherDb = 'N'; 
              rTypeConfig = allRoutinesTypeDataObj[routineType]['rTypeConfig'];
              rTypeConfigLen = len(rTypeConfig);
              if rTypeConfigLen > 0:
                 isRoutineTypeAlreadyCopiedFrmAnotherDb = 'Y';
              if isRoutineTypeAlreadyCopiedFrmAnotherDb == 'Y':
                 routinesDataObj[routineType] = allRoutinesTypeDataObj[routineType];
              if isRoutineTypeAlreadyCopiedFrmAnotherDb == 'N':
                 rTypeConfig = {
                    'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 
                    'copyDbName': dstDbName, 'copyRoutineType': routineType
                 };
                 routinesDataObj[routineType] = {
                    'rTypeConfig': rTypeConfig, 
                    'rTypeAllRoutineNames': dstDbRoutinesDataObj[routineType]['rTypeAllRoutineNames']
                 };
 
        
    except Exception as e:
           handleProcsngAbtErrException("Y");


    return routinesDataObj;


### get tables trigger definition changed between srcDb & dstDb ###

def getTblsTriggerDefChangedInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsTgrsDataObj = {};

    try:

        if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0 and againstSvr!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

           ### extracted all same table name with all trigger name data ###
           allTblsDataObj = {tblName: dstTblsDataObj[tblName] for tblName in dstTblsDataObj if tblName in srcTblsDataObj} ;

           for tblName in allTblsDataObj: 
 
               isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);

               ### extracted each same table name with all trigger name data ###
               eachTblAllTgrDataObj = {
                   tgrName: dstTblsDataObj[tblName][tgrName] for tgrName in dstTblsDataObj[tblName] if tgrName in srcTblsDataObj[tblName]
               };

               eachTblAllExistTgrDefChangedDataObj = {};

               for tgrName in eachTblAllTgrDataObj: 
 
                   frmTblTgrNameDataArr = srcTblsDataObj[tblName][tgrName]['updatedTgrNameData'];
                   toTblTgrNameDataArr = dstTblsDataObj[tblName][tgrName]['updatedTgrNameData'];
                   frmTblTgrNameActionTimeStr = frmTblTgrNameDataArr[3];
                   frmTblTgrNameActionEvntStr = frmTblTgrNameDataArr[4];
                   frmTblTgrNameDefinitionStr = (frmTblTgrNameDataArr[7]).strip().replace("\r", "");
                   toTblTgrNameActionTimeStr = toTblTgrNameDataArr[3];
                   toTblTgrNameActionEvntStr = toTblTgrNameDataArr[4];
                   toTblTgrNameDefinitionStr = (toTblTgrNameDataArr[7]).strip().replace("\r", "");
              
                   frmTblRefTgrDataObj = srcTblsDataObj[tblName][tgrName]['refTgrDataObj'];
                   refTgrNameDefChangedDataArr = frmTblRefTgrDataObj['tgrNameDefChangedDataArr'];
           
                   ### not same definition str ###

                   if frmTblTgrNameActionTimeStr != toTblTgrNameActionTimeStr or frmTblTgrNameActionEvntStr != toTblTgrNameActionEvntStr or frmTblTgrNameDefinitionStr != toTblTgrNameDefinitionStr :

                      refTgrDefConfig = {
                         'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 'copyDbName': dstDbName, 
                         'copyTblName': tblName, 'copyTgrName': tgrName
                      }; 
                      refTgrNameDefChangedDataArr.append({"refTgrDefConfig": refTgrDefConfig, "tgrNameDataArr": toTblTgrNameDataArr});
                      eachTblEachTgrDefChangedDataObj = {
                         'isDataAvailableInTbl': isDataAvailableInTbl,
                         'updatedTgrNameConfig': srcTblsDataObj[tblName][tgrName]['updatedTgrNameConfig'],
                         'updatedTgrNameData': toTblTgrNameDataArr, 
                         'orgTgrNameData': srcTblsDataObj[tblName][tgrName]['orgTgrNameData'],
                         'refTgrDataObj': {
                             'tgrNameDefChangedDataArr': refTgrNameDefChangedDataArr
                          }
                      }; 
                      eachTblAllExistTgrDefChangedDataObj[tgrName] = eachTblEachTgrDefChangedDataObj; 
    

               if len(eachTblAllExistTgrDefChangedDataObj) > 0: 
                  tblsTgrsDataObj[tblName] = eachTblAllExistTgrDefChangedDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsTgrsDataObj;



### get tables new trigger name between srcDb & dstDb ###

def getTblsNewTriggersBtwnSrcAndDstDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsTgrsDataObj = {};

    try:

        if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0:

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

           ### extracted all same table name with all trigger name ###
           allTblsDataObj = {toTblName: dstTblsDataObj[toTblName] for toTblName in dstTblsDataObj if toTblName in srcTblsDataObj};
 
           for tblName in allTblsDataObj: 

               isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);

               ### extracted each same table name have some new trigger name ###
               eachTblAllTgrNameDataObj = {
                  tgrName: dstTblsDataObj[tblName][tgrName] for tgrName in dstTblsDataObj[tblName] if tgrName not in srcTblsDataObj[tblName]
               };

               eachTblAllNewTgrNameDataObj = {};

               for tgrName in eachTblAllTgrNameDataObj:
                   isTblTgrAlreadyCopiedFrmAnotherDb = 'N'; 
                   updatedTgrNameConfig = eachTblAllTgrNameDataObj[tgrName]['updatedTgrNameConfig'];
                   updatedTgrNameConfigLen = len(updatedTgrNameConfig);
                   if updatedTgrNameConfigLen > 0:
                      isTblTgrAlreadyCopiedFrmAnotherDb = 'Y';
                   if isTblTgrAlreadyCopiedFrmAnotherDb == 'Y':
                      eachTblAllNewTgrNameDataObj[tgrName] = eachTblAllTgrNameDataObj[tgrName];
                   if isTblTgrAlreadyCopiedFrmAnotherDb == 'N':
                      updatedTgrNameConfig = {
                          'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 
                          'copyDbName': dstDbName, 'copyTblName': tblName, 'copyTgrName': tgrName
                      };
                      eachTblAllTgrNameDataObj[tgrName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                      eachTblAllTgrNameDataObj[tgrName]['updatedTgrNameConfig'] = updatedTgrNameConfig;
                      eachTblAllNewTgrNameDataObj[tgrName] = eachTblAllTgrNameDataObj[tgrName];

               eachTblAllNewTgrNameDataObjLen = len(eachTblAllNewTgrNameDataObj);
               if eachTblAllNewTgrNameDataObjLen > 0:
                  tblsTgrsDataObj[tblName] = eachTblAllNewTgrNameDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsTgrsDataObj;



### get all new tables with all trigger name between srcDb & dstDb ###

def getNewTblsAllTriggerInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsTgrsDataObj = {};

    try:

        if srcDbName!="" and dstDbName!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO']; 
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

           # extracted all new table with all trigger names data
           allTblsDataObj = {toTblName: dstTblsDataObj[toTblName] for toTblName in dstTblsDataObj if toTblName not in srcTblsDataObj};
         
           if len(allTblsDataObj)>0:

              for tblName in allTblsDataObj:
                  isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);  
                  for tgrName in allTblsDataObj[tblName]:
                      allTblsDataObj[tblName][tgrName]['isDataAvailableInTbl'] = isDataAvailableInTbl;

              tblsTgrsDataObj = allTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsTgrsDataObj;



### get tables fkConstraints definition changed between srcDb & dstDb ###

def getTblsFkColConstraintsDefChangedInfoBtwnDB(frmTblFKNameDataArr, toTblFKNameDataArr):

    FKNameDefChangedDataArr = [];

    try:

        if len(frmTblFKNameDataArr)>0 and len(toTblFKNameDataArr)>0:
          
           isTblFKNameDefinitionChanged = 'N';
           frmTblFkConstraintColName = frmTblFKNameDataArr[6];
           toTblFkConstraintColName = toTblFKNameDataArr[6];

           if frmTblFkConstraintColName == toTblFkConstraintColName:

              ### handle case for updateRule action ###
               
              frmTblFkConstraintUpdateRule = frmTblFKNameDataArr[8];
              toTblFkConstraintUpdateRule = toTblFKNameDataArr[8];
              if frmTblFkConstraintUpdateRule != toTblFkConstraintUpdateRule:
                 frmTblFKNameDataArr[8] = toTblFKNameDataArr[8];
                 isTblFKNameDefinitionChanged = 'Y';

         
              ### handle case for deleteRule action ###
               
              frmTblFkConstraintDeleteRule = frmTblFKNameDataArr[9];
              toTblFkConstraintDeleteRule = toTblFKNameDataArr[9];
              if frmTblFkConstraintDeleteRule != toTblFkConstraintDeleteRule:
                 frmTblFKNameDataArr[9] = toTblFKNameDataArr[9];
                 isTblFKNameDefinitionChanged = 'Y';

 
           if isTblFKNameDefinitionChanged == "Y":
              FKNameDefChangedDataArr = frmTblFKNameDataArr;

  
    except Exception as e:
           handleProcsngAbtErrException("Y"); 


    return FKNameDefChangedDataArr;


### get tables new fkConstraints name data between srcDb & dstDb ###

def getTblsFKNameNewColsConstraintsInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsFKNameColConstraintsDataObj = {};

    try:

        if srcDbName!="" and dstDbName!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];


           ### extracted all same table name with all fkConstraints name data ###
           tblsFkNamesDataObj = {
              toTblName: dstTblsDataObj[toTblName] for toTblName in dstTblsDataObj if toTblName in srcTblsDataObj
           };
 
           for tblName in tblsFkNamesDataObj: 

               isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);
 
               ### each table name have some new fkConstraints name data ###
               eachTblEachFKNameAllColConstraintsDataObj = {
                   FKName: dstTblsDataObj[tblName][FKName]['fkAllCols'] for FKName in dstTblsDataObj[tblName] if FKName in srcTblsDataObj[tblName]
               };

               for FKName in eachTblEachFKNameAllColConstraintsDataObj:

                   eachTblEachFKNameNewColsConstraintsDataObj = {
                       FKColName: dstTblsDataObj[tblName][FKName]['fkAllCols'][FKColName] for FKColName in dstTblsDataObj[tblName][FKName]['fkAllCols'] if FKColName not in srcTblsDataObj[tblName][FKName]['fkAllCols']
                   };


                   for FKColName in eachTblEachFKNameNewColsConstraintsDataObj:
                       isTblFKColNameConstraintsAlreadyCopiedFrmAnotherDb = 'N'; 
                       updatedFKColNameConfig = eachTblEachFKNameNewColsConstraintsDataObj[FKColName]['updatedFKColNameConfig'];
                       updatedFKColNameConfigLen = len(updatedFKColNameConfig);
                       if updatedFKColNameConfigLen > 0:
                          isTblFKColNameConstraintsAlreadyCopiedFrmAnotherDb = 'Y';
                       if isTblFKColNameConstraintsAlreadyCopiedFrmAnotherDb == 'Y':
                          eachTblEachFKNameNewColsConstraintsDataObj[FKName] = eachTblEachFKNameNewColsConstraintsDataObj[FKName];
                       if isTblFKColNameConstraintsAlreadyCopiedFrmAnotherDb == 'N':
                          updatedFKColNameConfig = {
                             'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 
                             'copyDbName': dstDbName, 'copyTblName': tblName, 
                             'copyFKName': FKName, 'copyFKColName': FKColName
                          };
                          eachTblEachFKNameNewColsConstraintsDataObj[FKColName]['updatedFKColNameConfig'] = updatedFKColNameConfig;


                   eachTblEachFKNameNewColsConstraintsDataObjLen = len(eachTblEachFKNameNewColsConstraintsDataObj);
                   if eachTblEachFKNameNewColsConstraintsDataObjLen > 0:
                      isTblNameExist = iskeynameExistInDictObj(tblsFKNameColConstraintsDataObj, tblName);
                      if isTblNameExist == True: 
                         tblsFKNameColConstraintsDataObj[tblName][FKName] = {};
                         tblsFKNameColConstraintsDataObj[tblName][FKName] = {
                             'isDataAvailableInTbl': isDataAvailableInTbl,
                             'updatedFKNameConfig': srcTblsDataObj[tblName][FKName]['updatedFKNameConfig'],
                             'fkAllCols': eachTblEachFKNameNewColsConstraintsDataObj
                         };
                      else:
                          tblsFKNameColConstraintsDataObj[tblName] = {};   
                          tblsFKNameColConstraintsDataObj[tblName][FKName] = {
                              'isDataAvailableInTbl': isDataAvailableInTbl,
                              'updatedFKNameConfig': srcTblsDataObj[tblName][FKName]['updatedFKNameConfig'],
                              'fkAllCols': eachTblEachFKNameNewColsConstraintsDataObj
                          };


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsFKNameColConstraintsDataObj;


### get tables new fkConstraints name data between srcDb & dstDb ###

def getTblsNewFKNameColConstraintsInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsFKNameColConstraintsDataObj = {};

    try:

        if srcDbName!="" and dstDbName!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

           ### extracted all same table name with all fkConstraints name data ###
           allTblsDataObj = {
              toTblName: dstTblsDataObj[toTblName] for toTblName in dstTblsDataObj if toTblName in srcTblsDataObj
           };
 
           for tblName in allTblsDataObj: 

               isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);

               ### each table name have some new fkConstraints name data ###
               eachTblAllFKNameColConstraintsDataObj = {
                   FKName: dstTblsDataObj[tblName][FKName] for FKName in dstTblsDataObj[tblName] if FKName not in srcTblsDataObj[tblName]
               };

               eachTblNewFKNameColConstraintsDataObj = {};

               for FKName in eachTblAllFKNameColConstraintsDataObj:
                   isTblFKNameAlreadyCopiedFrmAnotherDb = 'N'; 
                   updatedFKNameConfig = eachTblAllFKNameColConstraintsDataObj[FKName]['updatedFKNameConfig'];
                   updatedFKNameConfigLen = len(updatedFKNameConfig);
                   if updatedFKNameConfigLen > 0:
                      isTblFKNameAlreadyCopiedFrmAnotherDb = 'Y';
                   if isTblFKNameAlreadyCopiedFrmAnotherDb == 'Y':
                      eachTblNewFKNameColConstraintsDataObj[FKName] = eachTblAllFKNameColConstraintsDataObj[FKName];
                   if isTblFKNameAlreadyCopiedFrmAnotherDb == 'N':
                      updatedFKNameConfig = {
                          'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 
                          'copyDbName': dstDbName, 'copyTblName': tblName, 'copyFKName': FKName
                      };
                      eachTblAllFKNameColConstraintsDataObj[FKName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                      eachTblAllFKNameColConstraintsDataObj[FKName]['updatedFKNameConfig'] = updatedFKNameConfig;
                      eachTblNewFKNameColConstraintsDataObj[FKName] = eachTblAllFKNameColConstraintsDataObj[FKName];

               eachTblNewFKNameColConstraintsDataObjLen = len(eachTblNewFKNameColConstraintsDataObj);
               if eachTblNewFKNameColConstraintsDataObjLen > 0:
                  tblsFKNameColConstraintsDataObj[tblName] = eachTblNewFKNameColConstraintsDataObj; 


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsFKNameColConstraintsDataObj;



### get all new tables with all fkName with all cols constraints data between srcDb & dstDb ###

def getNewTblsFkNameColsConstraintsInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsFKNameColConstraintsDataObj = {};

    try:

        if srcDbName!="" and dstDbName!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

           allTblsDataObj = {toTblName: dstTblsDataObj[toTblName] for toTblName in dstTblsDataObj if toTblName not in srcTblsDataObj};
         
           if len(allTblsDataObj)>0:
              
              ### iterating each table data ###
              for tblName in allTblsDataObj:
                  isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);
                  for FKName in allTblsDataObj[tblName]: 
                      allTblsDataObj[tblName][FKName]['isDataAvailableInTbl'] = isDataAvailableInTbl; 
                
              tblsFKNameColConstraintsDataObj = allTblsDataObj;
   
           
    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsFKNameColConstraintsDataObj;


### get tables index column definition changed between srcDb & dstDb ###

def getTblIndexColDefChangedInfoBtwnDB(frmTblIndxColDataArr, toTblIndxColDataArr):

    indxColDefChangedDataArr = [];

    try:

        if len(frmTblIndxColDataArr)>0 and len(toTblIndxColDataArr)>0:
          
           isTblColIndexDefinitionChanged = 'N'; 

           ### handle case for changed unqiue/non-unique col index ###

           frmTblIndxColUniqueNonUniqueNo = frmTblIndxColDataArr[4];
           toTblIndxColUniqueNonUniqueNo = toTblIndxColDataArr[4];
      
           if frmTblIndxColUniqueNonUniqueNo != toTblIndxColUniqueNonUniqueNo:
              frmTblIndxColDataArr[4] = toTblIndxColDataArr[4];
              isTblColIndexDefinitionChanged = 'Y';

        
           ### handle case for changed col index sequence no ###

           frmTblIndxColSeqNo = frmTblIndxColDataArr[5];
           toTblIndxColSeqNo = toTblIndxColDataArr[5];
           frmTblIndxColSeqNoColName = frmTblIndxColDataArr[6];
           toTblIndxColSeqNoColName = toTblIndxColDataArr[6];
      
           if frmTblIndxColSeqNo != toTblIndxColSeqNo:
              frmTblIndxColDataArr[5] = toTblIndxColDataArr[5];
              isTblColIndexDefinitionChanged = 'Y';
           

           ### handle case for changed col index type ###

           frmTblIndxColIndxType = frmTblIndxColDataArr[7];
           toTblIndxColIndxType = toTblIndxColDataArr[7];
      
           if frmTblIndxColIndxType != toTblIndxColIndxType:
              frmTblIndxColDataArr[7] = toTblIndxColDataArr[7];
              isTblColIndexDefinitionChanged = 'Y';
             

           ### handle case for changed col index comment ###

           frmTblIndxColComment = frmTblIndxColDataArr[8];
           toTblIndxColComment = toTblIndxColDataArr[8];
      
           if frmTblIndxColComment == "" and toTblIndxColComment!="":
              frmTblIndxColDataArr[8] = toTblIndxColDataArr[8];
              isTblColIndexDefinitionChanged = 'Y';


           ### handle case for changed col index subpart ###

           frmTblIndxColSubPart = frmTblIndxColDataArr[9];
           toTblIndxColSubPart = toTblIndxColDataArr[9];
      
           if frmTblIndxColSubPart != toTblIndxColSubPart:
              frmTblIndxColDataArr[9] = toTblIndxColDataArr[9];
              isTblColIndexDefinitionChanged = 'Y';

 
           if isTblColIndexDefinitionChanged == "Y":
              indxColDefChangedDataArr = frmTblIndxColDataArr;

  
    except Exception as e:
           handleProcsngAbtErrException("Y"); 


    return indxColDefChangedDataArr;


### get tables index new columns between srcDb & dstDb ###

def getTblsIndexNewColsInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsIndexesDataObj = {};

    try:

        if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0:

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

           ### extracted all same table name with all index name with all columns data ###
           allTblsDataObj = {tblName: dstTblsDataObj[tblName] for tblName in dstTblsDataObj if tblName in srcTblsDataObj};

           for tblName in allTblsDataObj:

               isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName); 

               ### extracted each same table name with same index name with all columns data ###
               eachTblAllIndxDataObj = {
                  indxName: dstTblsDataObj[tblName][indxName]['indxAllCols'] for indxName in dstTblsDataObj[tblName] if indxName in srcTblsDataObj[tblName]
               };
 
               for indxName in eachTblAllIndxDataObj:
   
                   ### found each same table name each same index name have some new column index data ###
                   eachTblEachIndxAllColsDataObj = {
                       indxColName: eachTblAllIndxDataObj[indxName][indxColName] for indxColName in eachTblAllIndxDataObj[indxName] if indxColName not in srcTblsDataObj[tblName][indxName]['indxAllCols']
                   };

                   
                   eachTblEachIndxAllNewColsDataObj = {};

                   for indxColName in eachTblEachIndxAllColsDataObj:
                       isTblIndxColNameAlreadyCopiedFrmAnotherDb = 'N';
                       updatedIndxColConfig = eachTblEachIndxAllColsDataObj[indxColName]['updatedIndxColConfig'];
                       updatedIndxColConfigLen = len(updatedIndxColConfig);
                       if updatedIndxColConfigLen > 0:
                          isTblIndxColNameAlreadyCopiedFrmAnotherDb = 'Y';
                       if isTblIndxColNameAlreadyCopiedFrmAnotherDb == 'Y':
                          eachTblEachIndxAllNewColsDataObj[indxColName] = eachTblEachIndxAllColsDataObj[indxColName];
                       if isTblIndxColNameAlreadyCopiedFrmAnotherDb == 'N':
                          updatedIndxColConfig = {
                            'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 
                            'copyDbName': dstDbName, 'copyTblName': tblName, 
                            'copyIndxName': indxName, 'copyIndxColName': indxColName
                          };
                          eachTblEachIndxAllColsDataObj[indxColName]['updatedIndxColConfig'] = updatedIndxColConfig;
                          eachTblEachIndxAllNewColsDataObj[indxColName] = eachTblEachIndxAllColsDataObj[indxColName];

                   eachTblEachIndxAllNewColsDataObjLen = len(eachTblEachIndxAllNewColsDataObj);
                   if eachTblEachIndxAllNewColsDataObjLen > 0:
                      allNewColsDataObj = copy.deepcopy(eachTblEachIndxAllNewColsDataObj);
                      eachTblEachIndxAllNewColsDataObj.update(srcTblsDataObj[tblName][indxName]['indxAllCols']);
                      tblsIndexesDataObj[tblName] = {};
                      tblsIndexesDataObj[tblName][indxName] = {
                          'isDataAvailableInTbl': isDataAvailableInTbl,
                          'updatedIndxConfig': srcTblsDataObj[tblName][indxName]['updatedIndxConfig'],
                          'dbTblIndxType': srcTblsDataObj[tblName][indxName]['dbTblIndxType'],  
                          'indxAllCols': eachTblEachIndxAllNewColsDataObj,
                          'indxAllNewCols' : allNewColsDataObj   
                      };



    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsIndexesDataObj;



### get tables new index name with all columns data between srcDb & dstDb ###

def getTblsNewIndexesInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsIndexesDataObj = {};

    try:

        if srcDbName!="" and dstDbName!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];


           ### extracted all same table name with all index name with all columns data ###
           allTblsDataObj = {toTblName: dstTblsDataObj[toTblName] for toTblName in dstTblsDataObj if toTblName in srcTblsDataObj};
 
           for tblName in allTblsDataObj: 

               isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);
         
               ### found each same table name have some new index name with all columns data ###
               eachTblAllIndxDataObj = {
                  indxName: dstTblsDataObj[tblName][indxName] for indxName in dstTblsDataObj[tblName] if indxName not in srcTblsDataObj[tblName]
               };

               eachTblAllNewIndxNameDataObj = {};
               
               for indxName in eachTblAllIndxDataObj:
                   isTblIndxNameAlreadyCopiedFrmAnotherDb = 'N'; 
                   updatedIndxConfig = eachTblAllIndxDataObj[indxName]['updatedIndxConfig'];
                   updatedIndxConfigLen = len(updatedIndxConfig);
                   if updatedIndxConfigLen > 0:
                      isTblIndxNameAlreadyCopiedFrmAnotherDb = 'Y';
                   if isTblIndxNameAlreadyCopiedFrmAnotherDb == 'Y':
                      eachTblAllNewIndxNameDataObj[indxName] = eachTblAllIndxDataObj[indxName];
                   if isTblIndxNameAlreadyCopiedFrmAnotherDb == 'N':
                      updatedIndxConfig = {
                          'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 
                          'copyDbName': dstDbName, 'copyTblName': tblName, 'copyIndxName': indxName
                      };
                      eachTblAllIndxDataObj[indxName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                      eachTblAllIndxDataObj[indxName]['updatedIndxConfig'] = updatedIndxConfig;
                      eachTblAllNewIndxNameDataObj[indxName] = eachTblAllIndxDataObj[indxName];

               eachTblAllNewIndxNameDataObjLen = len(eachTblAllNewIndxNameDataObj);
               if eachTblAllNewIndxNameDataObjLen > 0:
                  tblsIndexesDataObj[tblName] = eachTblAllNewIndxNameDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsIndexesDataObj;



### get all new tables with all index name with all columns data between srcDb & dstDb ###

def getNewTblsAllIndexesInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsIndexesDataObj = {};

    try:

        if srcDbName!="" and dstDbName!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

           ### extracted all same table name with all index name with all columns data ###
           allTblsDataObj = {toTblName: dstTblsDataObj[toTblName] for toTblName in dstTblsDataObj if toTblName not in srcTblsDataObj};
         
           if len(allTblsDataObj)>0:

              ### iterating each table data ###
              for tblName in allTblsDataObj:
                  isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);
                  for indxName in allTblsDataObj[tblName]: 
                      allTblsDataObj[tblName][indxName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                
              tblsIndexesDataObj = allTblsDataObj;
             
           
    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsIndexesDataObj;



### get tables columns data type changed between srcDb & dstDb ###

def getTblsColsDataTypeChangedInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsColsDataObj = {};

    try:

        if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0 and againstSvr!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];


           ### extracted all same table name with all columns data ### 
           allTblsDataObj = {tblName: dstTblsDataObj[tblName] for tblName in dstTblsDataObj if tblName in srcTblsDataObj} ;

           for tblName in allTblsDataObj: 

               isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);

               ### extracted each same table name with all same name columns data ###
               eachTblAllColsDataObj = {
                   colName: colName for colName in dstTblsDataObj[tblName]['tblAllCols'] if colName in srcTblsDataObj[tblName]['tblAllCols']
               };

               eachTblAllExistColsDataTypeChangedDataObj = {};

               for colName in eachTblAllColsDataObj: 
 
                   frmTblColDataArr = srcTblsDataObj[tblName]['tblAllCols'][colName]['updatedColData'];
                   toTblColDataArr = dstTblsDataObj[tblName]['tblAllCols'][colName]['updatedColData'];
                   frmTblColDataTypeStr = frmTblColDataArr[3];
                   toTblColDataTypeStr = toTblColDataArr[3];
              
                   frmTblRefColDataObj = srcTblsDataObj[tblName]['tblAllCols'][colName]['refColDataObj']; 
                   refColDefChangedDataArr = frmTblRefColDataObj['colDefChangedDataArr'];
                   refColDataTypeChangedDataArr = frmTblRefColDataObj['colDataTypeChangedDataArr'];
           
                   ### not same data type ###
                   if frmTblColDataTypeStr != toTblColDataTypeStr:
                   
                      ### existing column config data extracted ###
                      existingUpdatedColConfig = srcTblsDataObj[tblName]['tblAllCols'][colName]['updatedColConfig'];
                       
                      ### preparing column config for reference purpose and stored in array as version no concept ###
                      refColConfig = {
                         'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 'copyDbName': dstDbName, 
                         'copyTblName': tblName, 'copyColName': colName
                      }; 
                      refColDataTypeChangedDataArr.append({"refColConfig": refColConfig, "colDataArr": toTblColDataArr});

                      if len(existingUpdatedColConfig)<=0:
                         existingUpdatedColConfig = refColConfig;

                      eachTblEachExistColDataTypeChangedDataObj = {
                         'updatedColConfig': existingUpdatedColConfig,
                         'updatedColData': toTblColDataArr, 
                         'orgColData': srcTblsDataObj[tblName]['tblAllCols'][colName]['orgColData'],
                         'refColDataObj': {
                            'colDefChangedDataArr': refColDefChangedDataArr,
                            'colDataTypeChangedDataArr': refColDataTypeChangedDataArr
                          }
                      }; 
                      eachTblAllExistColsDataTypeChangedDataObj[colName] = eachTblEachExistColDataTypeChangedDataObj; 
    

               if len(eachTblAllExistColsDataTypeChangedDataObj) > 0:
                  tblsColsDataObj[tblName] = {};
                  tblsColsDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                  tblsColsDataObj[tblName]['tblAllCols'] = eachTblAllExistColsDataTypeChangedDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return tblsColsDataObj;



### get tables new colums data between srcDb & dstDb ###

def getTblsNewColsInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsColsDataObj = {};
 
    try:

        if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0 and againstSvr!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];


           ### extracted all same table name with all columns data ###
           allTblsDataObj = {toTblName: dstTblsDataObj[toTblName] for toTblName in dstTblsDataObj if toTblName in srcTblsDataObj};
 
           for tblName in allTblsDataObj: 

               isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);

               ### found existing table name contain some new columns data ###
               eachTblAllColsDataObj = {
                  colName: dstTblsDataObj[tblName]['tblAllCols'][colName] for colName in dstTblsDataObj[tblName]['tblAllCols'] if colName not in srcTblsDataObj[tblName]['tblAllCols']
               };

               eachTblAllNewCols = {};

               for colName in eachTblAllColsDataObj:
                   isTblColConfigAlreadyCopiedFrmAnotherDb = 'N'; 
                   updatedColConfig = eachTblAllColsDataObj[colName]['updatedColConfig'];
                   updatedColConfigLen = len(updatedColConfig);
                   if updatedColConfigLen > 0:
                      isTblColConfigAlreadyCopiedFrmAnotherDb = 'Y';
                   if isTblColConfigAlreadyCopiedFrmAnotherDb=='Y':
                      eachTblAllNewCols[colName] = eachTblAllColsDataObj[colName];
                   if isTblColConfigAlreadyCopiedFrmAnotherDb=='N':
                      updatedColConfig = {
                        'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 'copyDbName': dstDbName, 
                        'copyTblName': tblName, 'copyColName': colName
                      };
                      eachTblAllColsDataObj[colName]['updatedColConfig'] = updatedColConfig;
                      eachTblAllNewCols[colName] = eachTblAllColsDataObj[colName];

                
               eachTblAllNewColsLen = len(eachTblAllNewCols);
               if eachTblAllNewColsLen > 0:
                  tblsColsDataObj[tblName] = {
                      'isDataAvailableInTbl': isDataAvailableInTbl,
                      'updatedTblConfig': dstTblsDataObj[tblName]['updatedTblConfig'], 
                      'tblAllCols': eachTblAllNewCols
                  };


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return tblsColsDataObj;



### get new tables between srcDb & dstDb ###

def getNewTblsInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsDataObj = {};

    try:

        if srcDbName!="" and dstDbName!="" and againstSvr!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

           ### extracting all new tables data ###
           allTblsDataObj = {tblName: dstTblsDataObj[tblName] for tblName in dstTblsDataObj if tblName not in srcTblsDataObj}; 

           ### iterating each new table data ###
           for tblName in allTblsDataObj:
               isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);
               isTblConfigAlreadyCopiedFrmAnotherDb = 'N'; 
               updatedTblConfig = allTblsDataObj[tblName]['updatedTblConfig'];
               updatedTblConfigLen = len(updatedTblConfig);
               if updatedTblConfigLen > 0:
                  isTblConfigAlreadyCopiedFrmAnotherDb = 'Y';
               if isTblConfigAlreadyCopiedFrmAnotherDb=='Y':
                  tblsDataObj[tblName] = allTblsDataObj[tblName];
               if isTblConfigAlreadyCopiedFrmAnotherDb=='N':
                  updatedTblConfig = {
                    'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 
                    'copyDbName': dstDbName, 'copyTblName': tblName
                  };
                  tblsDataObj[tblName] = {
                      'isDataAvailableInTbl' : isDataAvailableInTbl, 
                      'updatedTblConfig': updatedTblConfig, 
                      'tblAllCols': dstTblsDataObj[tblName]['tblAllCols']
                  };
 
        
    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsDataObj;




### get new tables between srcDb & dstDb ###

def getNewTblsAttrOptnInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsDataObj = {};

    try:

        if srcDbName!="" and dstDbName!="" and againstSvr!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

           ### extracting all new tables data ###
           allTblsDataObj = {tblName: dstTblsDataObj[tblName] for tblName in dstTblsDataObj if tblName not in srcTblsDataObj}; 

           ### iterating each new table data ###
           for tblName in allTblsDataObj:

               isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);
 
               isTblConfigAlreadyCopiedFrmAnotherDb = 'N'; 
               updatedTblConfig = allTblsDataObj[tblName]['updatedTblConfig'];
               updatedTblConfigLen = len(updatedTblConfig);
               if updatedTblConfigLen > 0:
                  isTblConfigAlreadyCopiedFrmAnotherDb = 'Y';
               if isTblConfigAlreadyCopiedFrmAnotherDb=='Y':
                  tblsDataObj[tblName] = allTblsDataObj[tblName];
               if isTblConfigAlreadyCopiedFrmAnotherDb=='N':
                  updatedTblConfig = {
                    'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 
                    'copyDbName': dstDbName, 'copyTblName': tblName
                  };
                  tblsDataObj[tblName] = allTblsDataObj[tblName];
                  tblsDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                  tblsDataObj[tblName]['updatedTblConfig'] = updatedTblConfig; 
 
        
    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsDataObj;



### handle bidirectional processing to get views def changed between srcDb and dstDb ###

def handleBidirProcsngToGetViewsDefChangedInfoBtwnDB(srcDbName,srcDbViewsDataObj,dstDbName,dstDbViewsDataObj,isMakeExactDbSchemasCopy):

    viewsDataObj = {};
    viewsDataObj['srcDbViewsDefChangedDataObj'] = {};
    viewsDataObj['srcDbViewsDataObj'] = {}; 
    viewsDataObj['dstDbViewsDefChangedDataObj'] = {};
    viewsDataObj['dstDbViewsDataObj'] = {};

    try:

       if srcDbName!="" and len(srcDbViewsDataObj)>0 and dstDbName!="" and len(dstDbViewsDataObj)>0:

          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];
          isIncludeDbViewsDefComparsion = inputArgsDataObj['isIncludeDbViewsDefComparsion'];

          if isIncludeDbViewsDefComparsion == "Y" :


             ### Case 1: Identify existing views def changed to create for srcDbName ###

             dcSrcDbViewsDataObj1 = copy.deepcopy(srcDbViewsDataObj);
             dcDstDbViewsDataObj1 = copy.deepcopy(dstDbViewsDataObj);

             viewsDefChangedForSrcDbDataObj = getViewsDefChangedInfoBtwnDB(
                  srcDbName, dcSrcDbViewsDataObj1, dstDbName, dcDstDbViewsDataObj1, 'DstSvr'
             );
             if len(viewsDefChangedForSrcDbDataObj) > 0 :
                if applyChangesOn == "SrcSvr" : 
                   for viewName in viewsDefChangedForSrcDbDataObj:
                       srcDbViewsDataObj[viewName].update(viewsDefChangedForSrcDbDataObj[viewName]);

                viewsDataObj['srcDbViewsDefChangedDataObj'] = viewsDefChangedForSrcDbDataObj;
                viewsDataObj['srcDbViewsDataObj'] = srcDbViewsDataObj;
          
  
             ### Case 2: Identify existing views def changed to create for dstDbName ###

             dcDstDbViewsDataObj2 = copy.deepcopy(dstDbViewsDataObj);
             dcSrcDbViewsDataObj2 = copy.deepcopy(srcDbViewsDataObj);
  
             viewsDefChangedForDstDbDataObj = getViewsDefChangedInfoBtwnDB(
                  dstDbName, dcDstDbViewsDataObj2, srcDbName, dcSrcDbViewsDataObj2, 'SrcSvr'
             );
             if len(viewsDefChangedForDstDbDataObj) > 0 :
                if applyChangesOn == "DstSvr": 
                   for viewName in viewsDefChangedForDstDbDataObj:
                       dstDbViewsDataObj[viewName].update(viewsDefChangedForDstDbDataObj[viewName]);

                viewsDataObj['dstDbViewsDefChangedDataObj'] = viewsDefChangedForDstDbDataObj;
                viewsDataObj['dstDbViewsDataObj'] = dstDbViewsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return viewsDataObj;


### handle bidirectional processing to get new views between srcDb and dstDb ###

def handleBidirProcsngToGetNewViewsInfoBtwnDB(srcDbName,srcDbViewsDataObj,dstDbName,dstDbViewsDataObj,isMakeExactDbSchemasCopy):

    viewsDataObj = {};
    viewsDataObj['srcDbNewViewsDataObj'] = {};
    viewsDataObj['srcDbViewsDataObj'] = {}; 
    viewsDataObj['dstDbNewViewsDataObj'] = {};
    viewsDataObj['dstDbViewsDataObj'] = {};

    try:

       if srcDbName!="" and dstDbName!="":
          
          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];
 
          ### Case 1: Identify new views to create for srcDbName ###

          dcSrcDbViewsDataObj1 = copy.deepcopy(srcDbViewsDataObj);
          dcDstDbViewsDataObj1 = copy.deepcopy(dstDbViewsDataObj);

          newViewsForSrcDbDataObj = getNewViewsInfoBtwnDB(
             srcDbName, dcSrcDbViewsDataObj1, dstDbName, dcDstDbViewsDataObj1, 'DstSvr'
          );
          if len(newViewsForSrcDbDataObj) > 0 :
             if applyChangesOn == "SrcSvr":   
                for viewName in newViewsForSrcDbDataObj:
                    srcDbViewsDataObj.update(newViewsForSrcDbDataObj[viewName]);

             viewsDataObj['srcDbNewViewsDataObj'] = newViewsForSrcDbDataObj;
             viewsDataObj['srcDbViewsDataObj'] = srcDbViewsDataObj;

          
          ### Case 2: Identify new views to create for dstDbName ###

          dcDstDbViewsDataObj2 = copy.deepcopy(dstDbViewsDataObj);
          dcSrcDbViewsDataObj2 = copy.deepcopy(srcDbViewsDataObj);

          newViewsForDstDbDataObj = getNewViewsInfoBtwnDB(
             dstDbName, dcDstDbViewsDataObj2, srcDbName, dcSrcDbViewsDataObj2, 'SrcSvr'
          );
          if len(newViewsForDstDbDataObj) > 0 :
             if applyChangesOn == "DstSvr":  
                for viewName in newViewsForDstDbDataObj:
                    dstDbViewsDataObj.update(newViewsForDstDbDataObj[viewName]);

             viewsDataObj['dstDbNewViewsDataObj'] = newViewsForDstDbDataObj;
             viewsDataObj['dstDbViewsDataObj'] = dstDbViewsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return viewsDataObj;


### handle bidirectional processing to get routine type routines name def changed between srcDb and dstDb ###

def handleBidirProcsngToGetRTypeRNameDefChangedInfoBtwnDB(srcDbName,srcDbRoutinesDataObj,dstDbName,dstDbRoutinesDataObj,isMakeExactDbSchemasCopy):

    routinesDataObj = {};
    routinesDataObj['srcDbRoutinesNameDefChangedDataObj'] = {};
    routinesDataObj['srcDbRoutinesDataObj'] = {}; 
    routinesDataObj['dstDbRoutinesNameDefChangedDataObj'] = {};
    routinesDataObj['dstDbRoutinesDataObj'] = {};

    try:

       if srcDbName!="" and len(srcDbRoutinesDataObj)>0 and dstDbName!="" and len(dstDbRoutinesDataObj)>0:

          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];
          isIncludeDbRoutinesDefComparsion = inputArgsDataObj['isIncludeDbRoutinesDefComparsion'];

          if isIncludeDbRoutinesDefComparsion == "Y" :
          
             ### Case 1: Identify routine type routine name def changed to create for srcDbName ###

             dcSrcDbRoutinesDataObj1 = copy.deepcopy(srcDbRoutinesDataObj);
             dcDstDbRoutinesDataObj1 = copy.deepcopy(dstDbRoutinesDataObj);
 
             routinesNameDefChangedForSrcDbDataObj = getRTypeRNameDefChangedInfoBtwnDB(
                srcDbName, dcSrcDbRoutinesDataObj1, dstDbName, dcDstDbRoutinesDataObj1, 'DstSvr'
             );
             if len(routinesNameDefChangedForSrcDbDataObj) > 0 :
                if applyChangesOn == "SrcSvr":
                   for routineType in routinesNameDefChangedForSrcDbDataObj:
                       srcDbRoutinesDataObj[routineType]['rTypeAllRoutineNames'].update(
                          routinesNameDefChangedForSrcDbDataObj[routineType]['rTypeAllRoutineNames']
                       );

                routinesDataObj['srcDbRoutinesNameDefChangedDataObj'] = routinesNameDefChangedForSrcDbDataObj;
                routinesDataObj['srcDbRoutinesDataObj'] = srcDbRoutinesDataObj;
          

             ### Case 2: Identify routine type routine name def changed to create for dstDbName ###

             dcDstDbRoutinesDataObj2 = copy.deepcopy(dstDbRoutinesDataObj);
             dcSrcDbRoutinesDataObj2 = copy.deepcopy(srcDbRoutinesDataObj);

             routinesNameDefChangedForDstDbDataObj = getRTypeRNameDefChangedInfoBtwnDB(
                dstDbName, dcDstDbRoutinesDataObj2, srcDbName, dcSrcDbRoutinesDataObj2, 'SrcSvr'
             );
             if len(routinesNameDefChangedForDstDbDataObj) > 0 :
                if applyChangesOn == "DstSvr":
                   for routineType in routinesNameDefChangedForDstDbDataObj:
                       dstDbRoutinesDataObj[routineType]['rTypeAllRoutineNames'].update(
                          routinesNameDefChangedForDstDbDataObj[routineType]['rTypeAllRoutineNames']
                       );

                routinesDataObj['dstDbRoutinesNameDefChangedDataObj'] = routinesNameDefChangedForDstDbDataObj;
                routinesDataObj['dstDbRoutinesDataObj'] = srcDbRoutinesDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return routinesDataObj;


### handle bidirectional processing to get routine type all new routines name between srcDb and dstDb ###

def handleBidirProcsngToGetRTypeNewRoutinesNameInfoBtwnDB(srcDbName,srcDbRoutinesDataObj,dstDbName,dstDbRoutinesDataObj,isMakeExactDbSchemasCopy):

    routinesDataObj = {};
    routinesDataObj['srcDbNewRoutinesNameDataObj'] = {};
    routinesDataObj['srcDbRoutinesDataObj'] = {}; 
    routinesDataObj['dstDbNewRoutinesNameDataObj'] = {};
    routinesDataObj['dstDbRoutinesDataObj'] = {};

    try:

       if srcDbName!="" and len(srcDbRoutinesDataObj)>0 and dstDbName!="" and len(dstDbRoutinesDataObj)>0:
          
          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];


          ### Case 1: Identify routine type all new routines name to create for srcDbName ###

          dcSrcDbRoutinesDataObj1 = copy.deepcopy(srcDbRoutinesDataObj);
          dcDstDbRoutinesDataObj1 = copy.deepcopy(dstDbRoutinesDataObj);

          newRoutinesNameForSrcDbDataObj = getRoutineTypeNewRoutinesNameInfoBtwnDB(
             srcDbName, dcSrcDbRoutinesDataObj1, dstDbName, dcDstDbRoutinesDataObj1, 'DstSvr'
          );
          if len(newRoutinesNameForSrcDbDataObj) > 0 :
             if applyChangesOn == "SrcSvr": 
                for routineType in newRoutinesNameForSrcDbDataObj:
                    srcDbRoutinesDataObj[routineType]['rTypeAllRoutineNames'].update(
                       newRoutinesNameForSrcDbDataObj[routineType]['rTypeAllRoutineNames']
                    );

             routinesDataObj['srcDbNewRoutinesNameDataObj'] = newRoutinesNameForSrcDbDataObj;
             routinesDataObj['srcDbRoutinesDataObj'] = srcDbRoutinesDataObj;
          

          ### Case 2: Identify routine type all new routines name to create for dstDbName ###
         
          dcDstDbRoutinesDataObj2 = copy.deepcopy(dstDbRoutinesDataObj);
          dcSrcDbRoutinesDataObj2 = copy.deepcopy(srcDbRoutinesDataObj);

          newRoutinesNameForDstDbDataObj = getRoutineTypeNewRoutinesNameInfoBtwnDB(
             dstDbName, dcDstDbRoutinesDataObj2, srcDbName, dcSrcDbRoutinesDataObj2, 'SrcSvr'
          );
          if len(newRoutinesNameForDstDbDataObj) > 0 :
             if applyChangesOn == "DstSvr": 
                for routineType in newRoutinesNameForDstDbDataObj:
                    dstDbRoutinesDataObj[routineType]['rTypeAllRoutineNames'].update(
                        newRoutinesNameForDstDbDataObj[routineType]['rTypeAllRoutineNames']
                    );
                
             routinesDataObj['dstDbNewRoutinesNameDataObj'] = newRoutinesNameForDstDbDataObj;
             routinesDataObj['dstDbRoutinesDataObj'] = dstDbRoutinesDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return routinesDataObj;


### handle bidirectional processing to get new routines between srcDb and dstDb ###

def handleBidirProcsngToGetNewRoutinesTypeInfoBtwnDB(srcDbName,srcDbRoutinesDataObj,dstDbName,dstDbRoutinesDataObj,isMakeExactDbSchemasCopy):

    routinesDataObj = {};
    routinesDataObj['srcDbNewRoutinesTypeDataObj'] = {};
    routinesDataObj['srcDbRoutinesDataObj'] = {}; 
    routinesDataObj['dstDbNewRoutinesTypeDataObj'] = {};
    routinesDataObj['dstDbRoutinesDataObj'] = {};

    try:

       if srcDbName!="" and dstDbName!="":
          
          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];


          ### Case 1: Identify new routines type to create for srcDbName ###
 
          dcSrcDbRoutinesDataObj1 = copy.deepcopy(srcDbRoutinesDataObj);
          dcDstDbRoutinesDataObj1 = copy.deepcopy(dstDbRoutinesDataObj);

          newRoutinesTypeForSrcDbDataObj = getNewRoutinesTypeInfoBtwnDB(
             srcDbName, dcSrcDbRoutinesDataObj1, dstDbName, dcDstDbRoutinesDataObj1, 'DstSvr'
          );
          if len(newRoutinesTypeForSrcDbDataObj) > 0 :
             if applyChangesOn == "SrcSvr":
                srcDbRoutinesDataObj.update(newRoutinesTypeForSrcDbDataObj);
                
             routinesDataObj['srcDbNewRoutinesTypeDataObj'] = newRoutinesTypeForSrcDbDataObj;
             routinesDataObj['srcDbRoutinesDataObj'] = srcDbRoutinesDataObj;

          
          ### Case 2: Identify new routines type to create for dstDbName ###

          dcDstDbRoutinesDataObj2 = copy.deepcopy(dstDbRoutinesDataObj);
          dcSrcDbRoutinesDataObj2 = copy.deepcopy(srcDbRoutinesDataObj);
          
          newRoutinesTypeForDstDbDataObj = getNewRoutinesTypeInfoBtwnDB(
             dstDbName, dcDstDbRoutinesDataObj2, srcDbName, dcSrcDbRoutinesDataObj2, 'SrcSvr'
          );
          if len(newRoutinesTypeForDstDbDataObj) > 0 :
             if applyChangesOn == "DstSvr":
                dstDbRoutinesDataObj.update(newRoutinesTypeForDstDbDataObj);
             
             routinesDataObj['dstDbNewRoutinesTypeDataObj'] = newRoutinesTypeForDstDbDataObj;
             routinesDataObj['dstDbRoutinesDataObj'] = dstDbRoutinesDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return routinesDataObj;



### handle bidirectional processing to get tables trigger definition changed between srcDb and dstDb tables ###

def handleBidirProcsngToGetTblsTriggerDefChangedInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsTgrsDataObj = {};
    tblsTgrsDataObj['srcDbTblsTgrDefChangedDataObj'] = {};
    tblsTgrsDataObj['srcDbTblsTgrDataObj'] = {}; 
    tblsTgrsDataObj['dstDbTblsTgrDefChangedDataObj'] = {};
    tblsTgrsDataObj['dstDbTblsTgrDataObj'] = {};

    try:

       if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0:
        
          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];
          isIncludeTblTrgsDefComparsion = inputArgsDataObj['isIncludeTblTrgsDefComparsion'];

          if isIncludeTblTrgsDefComparsion == "Y" :

             ### Case 1: Identify tables trigger definition changed to create on srcDb ###

             dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
             dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);

             tblsTgrDefChangedForSrcDbDataObj = getTblsTriggerDefChangedInfoBtwnDB(
                 srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr'
             );
             if len(tblsTgrDefChangedForSrcDbDataObj) > 0 :
                if applyChangesOn == "SrcSvr":   
                   for tblName in tblsTgrDefChangedForSrcDbDataObj:
                       srcTblsDataObj[tblName].update(tblsTgrDefChangedForSrcDbDataObj[tblName]);

                tblsTgrsDataObj['srcDbTblsTgrDefChangedDataObj'] = tblsTgrDefChangedForSrcDbDataObj;
                tblsTgrsDataObj['srcDbTblsTgrDataObj'] = srcTblsDataObj;

 
             ### Case 2: Identify tables trigger definition changed to create on dstDb ###

             dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
             dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);

             tblsTgrDefChangedForDstDbDataObj = getTblsTriggerDefChangedInfoBtwnDB(
                 dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr'
             );
             if len(tblsTgrDefChangedForDstDbDataObj) > 0 :
                if applyChangesOn == "DstSvr": 
                   for tblName in tblsTgrDefChangedForDstDbDataObj:
                       dstTblsDataObj[tblName].update(tblsTgrDefChangedForDstDbDataObj[tblName]);

                tblsTgrsDataObj['dstDbTblsTgrDefChangedDataObj'] = tblsTgrDefChangedForDstDbDataObj;
                tblsTgrsDataObj['dstDbTblsTgrDataObj'] = srcTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsTgrsDataObj;



### handle bidirectional processing to get tables new triggers between srcDb and dstDb tables ###

def handleBidirProcsngTogetTblsNewTriggersInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsTgrsDataObj = {};
    tblsTgrsDataObj['srcDbTblsNewTgrNameDataObj'] = {};
    tblsTgrsDataObj['srcDbTblsTgrDataObj'] = {}; 
    tblsTgrsDataObj['dstDbTblsNewTgrNameDataObj'] = {};
    tblsTgrsDataObj['dstDbTblsTgrDataObj'] = {};

    try:

       if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0:
          
          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];
      

          ### Case 1: Identify tables new triggers to create on srcDb ###

          dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
          dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);

          tblsNewTgrNamesForSrcDbDataObj = getTblsNewTriggersBtwnSrcAndDstDB(
              srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr'
          );
          if len(tblsNewTgrNamesForSrcDbDataObj) > 0 :
             if applyChangesOn == "SrcSvr" :
                for tblName in tblsNewTgrNamesForSrcDbDataObj:
                    srcTblsDataObj[tblName].update(tblsNewTgrNamesForSrcDbDataObj[tblName]);
             
             tblsTgrsDataObj['srcDbTblsNewTgrNameDataObj'] = tblsNewTgrNamesForSrcDbDataObj;
             tblsTgrsDataObj['srcDbTblsTgrDataObj'] = srcTblsDataObj;  
               

          ### Case 2: Identify tables new triggers to create on dstDb ###

          dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
          dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);

          tblsNewTgrNamesForDstDbDataObj = getTblsNewTriggersBtwnSrcAndDstDB(
              dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr'
          );
          if len(tblsNewTgrNamesForDstDbDataObj) > 0 :
             if applyChangesOn == "DstSvr" : 
                for tblName in tblsNewTgrNamesForDstDbDataObj:
                    dstTblsDataObj[tblName].update(tblsNewTgrNamesForDstDbDataObj[tblName]);
            
             tblsTgrsDataObj['dstDbTblsNewTgrNameDataObj'] = tblsNewTgrNamesForDstDbDataObj;
             tblsTgrsDataObj['dstDbTblsTgrDataObj'] = dstTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return tblsTgrsDataObj;


### handle bidirectional processing to get all new tables with all trigger names between srcDb and dstDb tables ###

def handleBidirProcsngToGetNewTblsAllTriggersInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsTgrsDataObj = {};
    tblsTgrsDataObj['srcDbTblsNewTgrNameDataObj'] = {};
    tblsTgrsDataObj['srcDbTblsTgrDataObj'] = {}; 
    tblsTgrsDataObj['dstDbTblsNewTgrNameDataObj'] = {};
    tblsTgrsDataObj['dstDbTblsTgrDataObj'] = {};

    try:

       if srcDbName!="" and dstDbName!="":
          
          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];


          ### Case 1: Identify all new tables with all trigger name to create on srcDb ###

          dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
          dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);
  
          newTblsAllTgrNamesForSrcDbDataObj = getNewTblsAllTriggerInfoBtwnDB(
             srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr'
          );
          if len(newTblsAllTgrNamesForSrcDbDataObj) > 0 :
             if applyChangesOn == "SrcSvr" :
                srcTblsDataObj.update(newTblsAllTgrNamesForSrcDbDataObj);
                
             tblsTgrsDataObj['srcDbTblsNewTgrNameDataObj'] = newTblsAllTgrNamesForSrcDbDataObj;
             tblsTgrsDataObj['srcDbTblsTgrDataObj'] = srcTblsDataObj;  
               

          ### Case 2: Identify all new tables with all trigger name to create on dstDb ###

          dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
          dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);
 
          newTblsAllTgrNamesForDstDbDataObj = getNewTblsAllTriggerInfoBtwnDB(
             dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr'
          );
          if len(newTblsAllTgrNamesForDstDbDataObj) > 0 :
             if applyChangesOn == "DstSvr" :
                dstTblsDataObj.update(newTblsAllTgrNamesForDstDbDataObj);
             
             tblsTgrsDataObj['dstDbTblsNewTgrNameDataObj'] = newTblsAllTgrNamesForDstDbDataObj;
             tblsTgrsDataObj['dstDbTblsTgrDataObj'] = dstTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return tblsTgrsDataObj;



### handle processing to get tables index fkConstraints definition changed between srcDb and dstDb ###

def handleProcsngToGetTblsFkNameColConstraintsDefChangedInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    existTblsExistFkColConstraintsDefChangedDataObj = {};

    try:

        if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0 and againstSvr!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

           for tblName in dstTblsDataObj: 
 
               isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);

               ### each table name have some new fkConstraints name data ###
               eachTblEachFKNameAllColConstraintsDataObj = {};
               isTblNameExist = iskeynameExistInDictObj(srcTblsDataObj, tblName);
               if isTblNameExist == True:
                  for FKName in dstTblsDataObj[tblName] :  
                      isFKNameExist = iskeynameExistInDictObj(srcTblsDataObj[tblName], FKName);
                      if isFKNameExist == True:
                         eachTblEachFKNameAllColConstraintsDataObj[FKName] = dstTblsDataObj[tblName][FKName]['fkAllCols'];

               ### iterate each fk name with all column names data ###   
               for FKName in eachTblEachFKNameAllColConstraintsDataObj:
      
                   eachTblEachFKNameAllColsConstraintsDataObj = {};
                   for FKColName in dstTblsDataObj[tblName][FKName]['fkAllCols'] :
                       isFKColNameExist = iskeynameExistInDictObj(srcTblsDataObj[tblName][FKName]['fkAllCols'], FKColName);
                       if isFKColNameExist == True:
                          eachTblEachFKNameAllColsConstraintsDataObj[FKColName] = dstTblsDataObj[tblName][FKName]['fkAllCols'][FKColName];

                   eachTblExistFkColConstraintsDefChangedDataObj = {};
                   for FKColName in eachTblEachFKNameAllColsConstraintsDataObj: 
                      
                       frmTblFKColNameDataArr = srcTblsDataObj[tblName][FKName]['fkAllCols'][FKColName]['updatedFKColNameData'];
                       toTblFKColNameDataArr = dstTblsDataObj[tblName][FKName]['fkAllCols'][FKColName]['updatedFKColNameData'];

                       frmTblRefFKColNameDataObj = srcTblsDataObj[tblName][FKName]['fkAllCols'][FKColName]['refFkColNameDataObj']; 
                       refFKColNameDefChangedDataArr = frmTblRefFKColNameDataObj['fkColNameDefChangedDataArr'];   

                       ### function called ###
                       FKColNameDefChangedDataArr = getTblsFkColConstraintsDefChangedInfoBtwnDB(
                           frmTblFKColNameDataArr, toTblFKColNameDataArr
                       );
                       if len(FKColNameDefChangedDataArr) > 0:
                          updatedFKColNameConfig = srcTblsDataObj[tblName][FKName]['fkAllCols'][FKColName]['updatedFKColNameConfig'];
                          refFKColNameConfig = {
                             'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 
                             'copyDbName':dstDbName, 'copyTblName': tblName, 
                             'copyFKName': FKName, 'copyFKColName': FKColName
                          }; 
                          refFKColNameDefChangedDataArr.append(
                             {"refFKColNameConfig": refFKColNameConfig, "FKColNameDataArr": FKColNameDefChangedDataArr}
                          );
                          eachTblExistFkColConstraintsDefChangedDataObj[FKName] = {
                              'updatedFKColNameConfig': updatedFKColNameConfig, 
                              'updatedFKColNameData': FKColNameDefChangedDataArr,
                              'orgFKColNameData': srcTblsDataObj[tblName][FKName]['fkAllCols'][FKColName]['orgFKColNameData'],
                              'refFkColNameDataObj': {
                                  'fkColNameDefChangedDataArr': refFKColNameDefChangedDataArr
                               }
                          };

       
                   eachTblExistFkColConstraintsDefChangedDataObjLen = len(eachTblExistFkColConstraintsDefChangedDataObj);
                   if eachTblExistFkColConstraintsDefChangedDataObjLen > 0:
                      isTblNameExist = iskeynameExistInDictObj(existTblsExistFkColConstraintsDefChangedDataObj, tblName);
                      if isTblNameExist == True:
                         existTblsExistFkColConstraintsDefChangedDataObj[tblName][FKName] = {
                             'isDataAvailableInTbl': isDataAvailableInTbl,
                             'updatedFKNameConfig': srcTblsDataObj[tblName][FKName]['updatedFKNameConfig'],
                             'fkAllCols': eachTblExistFkColConstraintsDefChangedDataObj
                         };
                      else:
                          existTblsExistFkColConstraintsDefChangedDataObj[tblName] = {};
                          existTblsExistFkColConstraintsDefChangedDataObj[tblName][FKName] = {
                             'isDataAvailableInTbl': isDataAvailableInTbl,
                             'updatedFKNameConfig': srcTblsDataObj[tblName][FKName]['updatedFKNameConfig'],
                             'fkAllCols': eachTblExistFkColConstraintsDefChangedDataObj
                         };  


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return existTblsExistFkColConstraintsDefChangedDataObj;


### handle bidirectional processing to get table fkName col def changed between srcDb and dstDb ###

def handleBidirProcsngToGetTblsFkColNameConstraintsDefChangedInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsFKNameColConstraintsDataObj = {};
    tblsFKNameColConstraintsDataObj['srcDbTblsFKNameColConstraintsDefDataObj'] = {};
    tblsFKNameColConstraintsDataObj['srcDbAllConstraintsDataObj'] = {}; 
    tblsFKNameColConstraintsDataObj['dstDbTblsFKNameColConstraintsDefDataObj'] = {};
    tblsFKNameColConstraintsDataObj['dstDbAllConstraintsDataObj'] = {};

    try:

       if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0:
          
          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];
          isIncludeTblForeignKeysConstraintsComparsion = inputArgsDataObj['isIncludeTblForeignKeysConstraintsComparsion'];
 

          if isIncludeTblForeignKeysConstraintsComparsion == "Y" :

             ### Case 1: Identify table fkConstraints definition changed for srcDbName ###

             dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
             dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);

             tblsFkNameColConstraintsDefChangedForSrcDbDataObj =   handleProcsngToGetTblsFkNameColConstraintsDefChangedInfoBtwnDB(
                 srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr'
             );
             if len(tblsFkNameColConstraintsDefChangedForSrcDbDataObj) > 0 :
                if applyChangesOn == "SrcSvr":  
                   for tblName in tblsFkNameColConstraintsDefChangedForSrcDbDataObj:
                       eachTblAllFkNameConstraintsDataObj = tblsFkNameColConstraintsDefChangedForSrcDbDataObj[tblName];
                       for tblFKName in eachTblAllFkNameConstraintsDataObj:
                           isDataAvailableInTbl = eachTblAllFkNameConstraintsDataObj[tblFKName]['isDataAvailableInTbl'];
                           eachTblEachFKAllColsConstraintsDataObj = eachTblAllFkNameConstraintsDataObj[tblFKName]['fkAllCols'];
                           srcTblsDataObj[tblName][tblFKName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                           srcTblsDataObj[tblName][tblFKName]['fkAllCols'].update(eachTblEachFKAllColsConstraintsDataObj);
                   
                tblsFKNameColConstraintsDataObj['srcDbTblsFKNameColConstraintsDefDataObj'] = tblsFkNameColConstraintsDefChangedForSrcDbDataObj;
                tblsFKNameColConstraintsDataObj['srcDbAllConstraintsDataObj'] = srcTblsDataObj;

          
             ### Case 2: Identify table fkConstraints definition changed for dstDbName ###

             dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
             dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);
 
             tblsFkNameColConstraintsDefChangedForDstDbDataObj = handleProcsngToGetTblsFkNameColConstraintsDefChangedInfoBtwnDB(
                 dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr'
             );
             if len(tblsFkNameColConstraintsDefChangedForDstDbDataObj) > 0 :
                if applyChangesOn == "DstSvr":  
                   for tblName in tblsFkNameColConstraintsDefChangedForDstDbDataObj:
                       eachTblAllFkNameConstraintsDataObj = tblsFkNameColConstraintsDefChangedForDstDbDataObj[tblName];
                       for tblFKName in eachTblAllFkNameConstraintsDataObj:
                           isDataAvailableInTbl = eachTblAllFkNameConstraintsDataObj[tblFKName]['isDataAvailableInTbl'];   
                           eachTblEachFKAllColsConstraintsDataObj = eachTblAllFkNameConstraintsDataObj[tblFKName]['fkAllCols'];
                           dstTblsDataObj[tblName][tblFKName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                           dstTblsDataObj[tblName][tblFKName]['fkAllCols'].update(eachTblEachFKAllColsConstraintsDataObj);

                tblsFKNameColConstraintsDataObj['dstDbTblsFKNameColConstraintsDefDataObj'] = tblsFkNameColConstraintsDefChangedForDstDbDataObj;
                tblsFKNameColConstraintsDataObj['dstDbAllConstraintsDataObj'] = dstTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsFKNameColConstraintsDataObj;



### handle bidirectional processing to get tables fkName with all new cols constraints between srcDb and dstDb tables ###

def handleBidirProcsngToGetTblsFKNameNewColConstraintsInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsFKNameColConstraintsDataObj = {};
    tblsFKNameColConstraintsDataObj['srcDbFKTblsFKNameNewColsConstraintsDataObj'] = {};
    tblsFKNameColConstraintsDataObj['srcDbAllConstraintsDataObj'] = {}; 
    tblsFKNameColConstraintsDataObj['dstDbFKTblsFKNameNewColsConstraintsDataObj'] = {};
    tblsFKNameColConstraintsDataObj['dstDbAllConstraintsDataObj'] = {};

    try:

       if srcDbName!="" and dstDbName!="":
          
          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];
          isIncludeTblForeignKeysConstraintsComparsion = inputArgsDataObj['isIncludeTblForeignKeysConstraintsComparsion'];

          if isIncludeTblForeignKeysConstraintsComparsion == "Y" :

           
             ### Case 1: Identify tables new fkConstraints to create for srcDb ###
            
             dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
             dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);

             tblsFkNameNewColsConstraintsForSrcDbDataObj = getTblsFKNameNewColsConstraintsInfoBtwnDB(
                 srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr'
             );
             if len(tblsFkNameNewColsConstraintsForSrcDbDataObj) > 0 :
                if applyChangesOn == "SrcSvr" : 
                   for tblName in tblsFkNameNewColsConstraintsForSrcDbDataObj:
                       eachTblAllFkNameConstraintsDataObj = tblsFkNameNewColsConstraintsForSrcDbDataObj[tblName];
                       for tblFKName in eachTblAllFkNameConstraintsDataObj:
                           isDataAvailableInTbl = eachTblAllFkNameConstraintsDataObj[tblFKName]['isDataAvailableInTbl'];
                           eachTblFKNameAllColsConstraintsDataObj = eachTblAllFkNameConstraintsDataObj[tblFKName]['fkAllCols'];
                           srcTblsDataObj[tblName][tblFKName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                           srcTblsDataObj[tblName][tblFKName]['fkAllCols'].update(eachTblFKNameAllColsConstraintsDataObj);
             
                tblsFKNameColConstraintsDataObj['srcDbFKTblsFKNameNewColsConstraintsDataObj'] = tblsFkNameNewColsConstraintsForSrcDbDataObj;
                tblsFKNameColConstraintsDataObj['srcDbAllConstraintsDataObj'] = srcTblsDataObj;  
               


          ### Case 2: Identify tables new fkConstraints to create for dstDb ###

          dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
          dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);

          tblsFkNameNewColsConstraintsForDstDbDataObj = getTblsNewFKNameColConstraintsInfoBtwnDB(
              dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr'
          );
          if len(tblsFkNameNewColsConstraintsForDstDbDataObj) > 0 :
             if applyChangesOn == "DstSvr" : 
                for tblName in tblsFkNameNewColsConstraintsForDstDbDataObj:
                    eachTblAllFkNameConstraintsDataObj = tblsFkNameNewColsConstraintsForDstDbDataObj[tblName];
                    for tblFKName in eachTblAllFkNameConstraintsDataObj:
                        isDataAvailableInTbl = eachTblAllFkNameConstraintsDataObj[tblFKName]['isDataAvailableInTbl'];
                        eachTblFKNameAllColsConstraintsDataObj = eachTblAllFkNameConstraintsDataObj[tblFKName]['fkAllCols'];
                        dstTblsDataObj[tblName][tblFKName]['isDataAvailableInTbl'] = isDataAvailableInTbl; 
                        dstTblsDataObj[tblName][tblFKName]['fkAllCols'].update(eachTblFKNameAllColsConstraintsDataObj);
            
             tblsFKNameColConstraintsDataObj['dstDbFKTblsFKNameNewColsConstraintsDataObj'] = tblsFkNameNewColsConstraintsForDstDbDataObj;
             tblsFKNameColConstraintsDataObj['dstDbAllConstraintsDataObj'] = dstTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsFKNameColConstraintsDataObj;



### handle bidirectional processing to get tables new fkName with all new cols constraints between srcDb and dstDb tables ###

def handleBidirProcsngToGetTblsNewFKNameColConstraintsBtwnSrcAndDstDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsFKNameColConstraintsDataObj = {};
    tblsFKNameColConstraintsDataObj['srcDbExistTblsNewFkNameColConstraintsDataObj'] = {};
    tblsFKNameColConstraintsDataObj['srcDbAllConstraintsDataObj'] = {}; 
    tblsFKNameColConstraintsDataObj['dstDbExistTblsNewFkNameColConstraintsDataObj'] = {};
    tblsFKNameColConstraintsDataObj['dstDbAllConstraintsDataObj'] = {};

    try:

       if srcDbName!="" and dstDbName!="":

          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];

          
          ### Case 1: Identify tables new fkConstraints to create for srcDb ###

          dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
          dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);

          tblsNewFkNameColConstraintsForSrcDbDataObj = getTblsNewFKNameColConstraintsInfoBtwnDB(
              srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr'
          );
          if len(tblsNewFkNameColConstraintsForSrcDbDataObj) > 0 :
             if applyChangesOn == "SrcSvr" :   
                for tblName in tblsNewFkNameColConstraintsForSrcDbDataObj:
                    eachTblAllFKNameColConstraintsDataObj = tblsNewFkNameColConstraintsForSrcDbDataObj[tblName]; 
                    srcTblsDataObj[tblName].update(eachTblAllFKNameColConstraintsDataObj);
             
             tblsFKNameColConstraintsDataObj['srcDbExistTblsNewFkNameColConstraintsDataObj'] = tblsNewFkNameColConstraintsForSrcDbDataObj;
             tblsFKNameColConstraintsDataObj['srcDbAllConstraintsDataObj'] = srcTblsDataObj;  
               


          ### Case 2: Identify tables new fkConstraints to create for dstDb ###

          dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
          dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);

          tblsNewFkNameColConstraintsForDstDbDataObj = getTblsNewFKNameColConstraintsInfoBtwnDB(
              dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr'
          );
          if len(tblsNewFkNameColConstraintsForDstDbDataObj) > 0 :
             if applyChangesOn == "DstSvr" :
                for tblName in tblsNewFkNameColConstraintsForDstDbDataObj:
                    eachTblAllFKNameColConstraintsDataObj = tblsNewFkNameColConstraintsForDstDbDataObj[tblName];
                    dstTblsDataObj[tblName].update(eachTblAllFKNameColConstraintsDataObj);
            
             tblsFKNameColConstraintsDataObj['dstDbExistTblsNewFkNameColConstraintsDataObj'] = tblsNewFkNameColConstraintsForDstDbDataObj;
             tblsFKNameColConstraintsDataObj['dstDbAllConstraintsDataObj'] = dstTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsFKNameColConstraintsDataObj;



### handle bidirectional processing to get new tables with all new fkName ###
### with all columns constraints data between srcDb and dstDb tables ###

def handleBidirProcsngToGetNewTblsFkNameColConstraintsInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsFKNameColConstraintsDataObj = {};
    tblsFKNameColConstraintsDataObj['srcDbNewTblsFkNameColConstraintsDataObj'] = {};
    tblsFKNameColConstraintsDataObj['srcDbAllConstraintsDataObj'] = {}; 
    tblsFKNameColConstraintsDataObj['dstDbNewTblsFkNameColConstraintsDataObj'] = {};
    tblsFKNameColConstraintsDataObj['dstDbAllConstraintsDataObj'] = {};

    try:

       if srcDbName!="" and dstDbName!="":
          
          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];


          ### Case 1: Identify new tables with all new constraints names to create for srcDb ###

          dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
          dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);

          newTblsFkNameColConstraintsForSrcDbDataObj = getNewTblsFkNameColsConstraintsInfoBtwnDB(
             srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr'
          );
          if len(newTblsFkNameColConstraintsForSrcDbDataObj) > 0 :
             if applyChangesOn == "SrcSvr" : 
                srcTblsDataObj.update(newTblsFkNameColConstraintsForSrcDbDataObj);

             tblsFKNameColConstraintsDataObj['srcDbNewTblsFkNameColConstraintsDataObj'] = newTblsFkNameColConstraintsForSrcDbDataObj;
             tblsFKNameColConstraintsDataObj['srcDbAllConstraintsDataObj'] = srcTblsDataObj;  
               

          ### Case 2: Identify new tables with all new constraints names to create for dstDb ###

          dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
          dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);

          newTblsFkNameColConstraintsForDstDbDataObj = getNewTblsFkNameColsConstraintsInfoBtwnDB(
             dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr'
          );
          if len(newTblsFkNameColConstraintsForDstDbDataObj) > 0 :
             if applyChangesOn == "DstSvr" : 
                dstTblsDataObj.update(newTblsFkNameColConstraintsForDstDbDataObj);

             tblsFKNameColConstraintsDataObj['dstDbNewTblsFkNameColConstraintsDataObj'] = newTblsFkNameColConstraintsForDstDbDataObj;
             tblsFKNameColConstraintsDataObj['dstDbAllConstraintsDataObj'] = dstTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsFKNameColConstraintsDataObj;



### handle processing to get exist tables exist index exist columns definition changed between srcDb and dstDb ###

def handleProcsngToGetTblsIndexColsDefChangedInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsIndxColsDefChangedDataObj = {};

    try:

        if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0 and againstSvr!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];

           ### extracted all same table name with all index name with all columns data ###
           allTblsDataObj = {};
           for tblName in dstTblsDataObj:
               isTblNameExist = iskeynameExistInDictObj(srcTblsDataObj, tblName);
               if isTblNameExist == True:
                  allTblsDataObj[tblName] = dstTblsDataObj[tblName];
 

           for tblName in allTblsDataObj:
 
               isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);

               ### extracted each same table name with same index name with all columns data ###
               eachTblAllIndxDataObj = {};  
               for indxName in dstTblsDataObj[tblName] :
                   isIndxNameExist = iskeynameExistInDictObj(srcTblsDataObj[tblName], indxName);
                   if isIndxNameExist == True:
                      eachTblAllIndxDataObj[indxName] = dstTblsDataObj[tblName][indxName]['indxAllCols'];
                 
         
               ### iterate each indx of each table ###
               for indxName in eachTblAllIndxDataObj:
         
                   ### found each same table name each same index name same column index data ###
                   eachTblEachIndxAllColsDataObj = {};
                   for indxColName in eachTblAllIndxDataObj[indxName] :
                       isIndxColNameExist = iskeynameExistInDictObj(srcTblsDataObj[tblName][indxName]['indxAllCols'], indxColName);
                       if isIndxColNameExist == True:
                          eachTblEachIndxAllColsDataObj[indxColName] = eachTblAllIndxDataObj[indxName][indxColName];


                   isIndxColDefChangedFound = 'N';
                   eachTblEachIndexAllColsDefChangedDataObj = {};

                   for indxColName in eachTblEachIndxAllColsDataObj:
                         
                       frmTblIndxColDataArr = srcTblsDataObj[tblName][indxName]['indxAllCols'][indxColName]['updatedIndxColData'];
                       toTblIndxColDataArr = dstTblsDataObj[tblName][indxName]['indxAllCols'][indxColName]['updatedIndxColData'];

                       frmTblRefColDataObj = srcTblsDataObj[tblName][indxName]['indxAllCols'][indxColName]['refIndxColDataObj']; 
                       refIndxColDefChangedDataArr = frmTblRefColDataObj['indxColDefChangedDataArr'];
                       
                       ### function called ###
                       indxColDefChangedDataArr = getTblIndexColDefChangedInfoBtwnDB(frmTblIndxColDataArr, toTblIndxColDataArr);
                       if len(indxColDefChangedDataArr) > 0:
                          isIndxColDefChangedFound = 'Y';
                          updatedIndxColConfig = srcTblsDataObj[tblName][indxName]['indxAllCols'][indxColName]['updatedIndxColConfig'];
                          refColConfig = {
                               'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 
                               'copyDbName':dstDbName, 'copyTblName': tblName,
                               'copyIndxName': indxName, 'copyIndxColName': indxColName
                          }; 
                          refIndxColDefChangedDataArr.append({"refColConfig": refColConfig, "colDataArr": indxColDefChangedDataArr});
                          eachTblEachIndexAllColsDefChangedDataObj[indxColName] = {
                               'updatedIndxColConfig': updatedIndxColConfig, 
                               'updatedIndxColData': indxColDefChangedDataArr,
                               'orgIndxColData': srcTblsDataObj[tblName][indxName]['indxAllCols'][indxColName]['orgIndxColData'],
                               'refIndxColDataObj': {
                                  'indxColDefChangedDataArr': refIndxColDefChangedDataArr
                                }
                          };

                       else:

                           eachTblEachIndexAllColsDefChangedDataObj[indxColName] = {
                               'updatedIndxColConfig': srcTblsDataObj[tblName][indxName]['indxAllCols'][indxColName]['updatedIndxColConfig'], 
                               'updatedIndxColData': srcTblsDataObj[tblName][indxName]['indxAllCols'][indxColName]['updatedIndxColData'],
                               'orgIndxColData': srcTblsDataObj[tblName][indxName]['indxAllCols'][indxColName]['orgIndxColData'],
                               'refIndxColDataObj': {
                                  'indxColDefChangedDataArr': refIndxColDefChangedDataArr
                                }
                           };           
                            
                   
                   if isIndxColDefChangedFound == "Y" :    
                      eachTblEachIndexAllColsDefChangedDataObjLen = len(eachTblEachIndexAllColsDefChangedDataObj);
                      if eachTblEachIndexAllColsDefChangedDataObjLen > 0:
                         tblsIndxColsDefChangedDataObj[tblName] = {}; 
                         tblsIndxColsDefChangedDataObj[tblName][indxName] = {
                            'isDataAvailableInTbl': isDataAvailableInTbl,
                            'updatedIndxConfig': srcTblsDataObj[tblName][indxName]['updatedIndxConfig'],
                            'dbTblIndxType': dstTblsDataObj[tblName][indxName]['dbTblIndxType'], 
                            'indxAllCols': eachTblEachIndexAllColsDefChangedDataObj
                         };



    except Exception as e:
           handleProcsngAbtErrException("Y");

    return tblsIndxColsDefChangedDataObj;



### handle bidirectional processing to get exist table indexes changed between srcDb and dstDb ###

def handleBidirProcsngToGetTblsIndexColsDefChangedInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsIndexesDataObj = {};
    tblsIndexesDataObj['srcDbTblIndxColsChangedDataObj'] = {};
    tblsIndexesDataObj['srcDbAllIndexDataObj'] = {}; 
    tblsIndexesDataObj['dstDbTblIndxColsChangedDataObj'] = {};
    tblsIndexesDataObj['dstDbAllIndexDataObj'] = {};

    try:

       if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0:
          
          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];
          isIncludeTblColIndexesComparsion = inputArgsDataObj['isIncludeTblColIndexesComparsion'];

          
          if isIncludeTblColIndexesComparsion == "Y" :

             ### Case 1: Identify table indexes some columns definition changed for srcDbName ###
           
             dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
             dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);

             colsIndexDefChangedForSrcDbDataObj = handleProcsngToGetTblsIndexColsDefChangedInfoBtwnDB(
                 srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr'
             );
             if len(colsIndexDefChangedForSrcDbDataObj) > 0 :
                if applyChangesOn == "SrcSvr":
                   for tblName in colsIndexDefChangedForSrcDbDataObj:
                       tblAllIndxDataObj = colsIndexDefChangedForSrcDbDataObj[tblName];
                       for indxName in tblAllIndxDataObj:
                           srcTblsDataObj[tblName][indxName]['isDataAvailableInTbl'] = tblAllIndxDataObj[indxName]['isDataAvailableInTbl'];
                           srcTblsDataObj[tblName][indxName]['indxAllCols'].update(tblAllIndxDataObj[indxName]['indxAllCols']);
                
                tblsIndexesDataObj['srcDbTblIndxColsChangedDataObj'] = colsIndexDefChangedForSrcDbDataObj;
                tblsIndexesDataObj['srcDbAllIndexDataObj'] = srcTblsDataObj;

  
             ### Case 2: Identify existing table existing indexes some columns definition changed for dstDbName ###

             dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
             dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);

             colsIndexDefChangedForDstDbDataObj = handleProcsngToGetTblsIndexColsDefChangedInfoBtwnDB(
                 dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr'
             );
             if len(colsIndexDefChangedForDstDbDataObj) > 0 :
                if applyChangesOn == "DstSvr":
                   for tblName in colsIndexDefChangedForDstDbDataObj:
                       tblAllIndxDataObj = colsIndexDefChangedForDstDbDataObj[tblName];
                       for indxName in tblAllIndxDataObj:
                           dstTblsDataObj[tblName][indxName]['isDataAvailableInTbl'] = tblAllIndxDataObj[indxName]['isDataAvailableInTbl'];
                           dstTblsDataObj[tblName][indxName]['indxAllCols'].update(tblAllIndxDataObj[indxName]['indxAllCols']);

                tblsIndexesDataObj['dstDbTblIndxColsChangedDataObj'] = colsIndexDefChangedForDstDbDataObj;
                tblsIndexesDataObj['dstDbAllIndexDataObj'] = dstTblsDataObj;

    except Exception as e:
           handleProcsngAbtErrException("Y");

    return tblsIndexesDataObj;


### handle bidirectional processing to get tables index name to include new columns data between srcDb and dstDb ###

def handleBidirProcsngToGetTblsIndexNewColsInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsIndexesDataObj = {};
    tblsIndexesDataObj['srcDbTblIndxNewColsDataObj'] = {};
    tblsIndexesDataObj['srcDbAllIndexDataObj'] = {}; 
    tblsIndexesDataObj['dstDbTblIndxNewColsDataObj'] = {};
    tblsIndexesDataObj['dstDbAllIndexDataObj'] = {};

    try:

       if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0:


          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];
          isIncludeTblColIndexesComparsion = inputArgsDataObj['isIncludeTblColIndexesComparsion'];

          if isIncludeTblColIndexesComparsion == "Y" :  
          
             
             ### Case 1: Identify tables index to include new columns to create for srcDb ###

             dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
             dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);

             tblsIndxNewColsForSrcDbDataObj = getTblsIndexNewColsInfoBtwnDB(
                 srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr'
             );
             if len(tblsIndxNewColsForSrcDbDataObj) > 0 :
                if applyChangesOn == "SrcSvr" :
                   for tblName in tblsIndxNewColsForSrcDbDataObj:
                       tblAllIndxDataObj = tblsIndxNewColsForSrcDbDataObj[tblName];
                       for tblIndxName in tblAllIndxDataObj:
                           isDataAvailableInTbl = tblAllIndxDataObj[tblIndxName]['isDataAvailableInTbl'];
                           if isMakeExactDbSchemasCopy == "Y" :
                              allNewColsDataObj = tblAllIndxDataObj[tblIndxName]['indxAllNewCols'];
                              allNewColsDataObj.update(dstTblsDataObj[tblName][tblIndxName]['indxAllCols']);
                              tblsIndxNewColsForSrcDbDataObj[tblName][tblIndxName]['indxAllCols'] = allNewColsDataObj;
                              srcTblsDataObj[tblName][tblIndxName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                              srcTblsDataObj[tblName][tblIndxName]['indxAllCols'] = allNewColsDataObj;
                           else :
                                srcTblsDataObj[tblName][tblIndxName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                                srcTblsDataObj[tblName][tblIndxName]['indxAllCols'].update(tblAllIndxDataObj[tblIndxName]['indxAllCols']);
             

                tblsIndexesDataObj['srcDbTblIndxNewColsDataObj'] = tblsIndxNewColsForSrcDbDataObj;
                tblsIndexesDataObj['srcDbAllIndexDataObj'] = srcTblsDataObj;


             ### Case 2: Identify tables index to include new columns to create for dstDb ###

             dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
             dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);

             tblsIndxNewColsForDstDbDataObj = getTblsIndexNewColsInfoBtwnDB(
                 dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr'
             );
             if len(tblsIndxNewColsForDstDbDataObj) > 0 :
                if applyChangesOn == "DstSvr" :     
                   for tblName in tblsIndxNewColsForDstDbDataObj:
                       tblAllIndxDataObj = tblsIndxNewColsForDstDbDataObj[tblName];
                       for tblIndxName in tblAllIndxDataObj:
                           isDataAvailableInTbl = tblAllIndxDataObj[tblIndxName]['isDataAvailableInTbl'];
                           if isMakeExactDbSchemasCopy == "Y" :
                              allNewColsDataObj = tblAllIndxDataObj[tblIndxName]['indxAllNewCols'];
                              allNewColsDataObj.update(srcTblsDataObj[tblName][tblIndxName]['indxAllCols']);
                              tblsIndxNewColsForDstDbDataObj[tblName][tblIndxName]['indxAllCols'] = allNewColsDataObj;
                              dstTblsDataObj[tblName][tblIndxName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                              dstTblsDataObj[tblName][tblIndxName]['indxAllCols'] = allNewColsDataObj;
                           else :
                                dstTblsDataObj[tblName][tblIndxName]['isDataAvailableInTbl'] = isDataAvailableInTbl;  
                                dstTblsDataObj[tblName][tblIndxName]['indxAllCols'].update(tblAllIndxDataObj[tblIndxName]['indxAllCols']); 
            
                tblsIndexesDataObj['dstDbTblIndxNewColsDataObj'] = tblsIndxNewColsForDstDbDataObj;
                tblsIndexesDataObj['dstDbAllIndexDataObj'] = dstTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsIndexesDataObj;



### handle bidirectional processing to get tables new indexes names between srcDb and dstDb tables ###

def handleBidirProcsngToGetTblsNewIndexesInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsIndexesDataObj = {};
    tblsIndexesDataObj['srcDbTblsNewIndxNameDataObj'] = {};
    tblsIndexesDataObj['srcDbAllIndexDataObj'] = {}; 
    tblsIndexesDataObj['dstDbTblsNewIndxNameDataObj'] = {};
    tblsIndexesDataObj['dstDbAllIndexDataObj'] = {};

    try:

       if srcDbName!="" and dstDbName!="":
          
          global inputArgsDataObj; 
          applyChangesOn = inputArgsDataObj['applyChangesOn'];


          ### Case 1: Identify tables new indexes to create for srcDb ###

          dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
          dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);
 
          allTblsNewIndexNameForSrcDbDataObj = getTblsNewIndexesInfoBtwnDB(
             srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr'
          );
          if len(allTblsNewIndexNameForSrcDbDataObj) > 0 :
             if applyChangesOn == "SrcSvr" :     
                for tblName in allTblsNewIndexNameForSrcDbDataObj:
                    srcTblsDataObj[tblName].update(allTblsNewIndexNameForSrcDbDataObj[tblName]);
             
             tblsIndexesDataObj['srcDbTblsNewIndxNameDataObj'] = allTblsNewIndexNameForSrcDbDataObj;
             tblsIndexesDataObj['srcDbAllIndexDataObj'] = srcTblsDataObj;  
               

          ### Case 2: Identify tables new indexes to create for dstDb ###

          dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
          dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);

          allTblsNewIndexNameForDstDbDataObj = getTblsNewIndexesInfoBtwnDB(
             dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr'
          );
          if len(allTblsNewIndexNameForDstDbDataObj) > 0 :
             if applyChangesOn == "DstSvr" :
                for tblName in allTblsNewIndexNameForDstDbDataObj:
                    dstTblsDataObj[tblName].update(allTblsNewIndexNameForDstDbDataObj[tblName]);
                    
             tblsIndexesDataObj['dstDbTblsNewIndxNameDataObj'] = allTblsNewIndexNameForDstDbDataObj;
             tblsIndexesDataObj['dstDbAllIndexDataObj'] = dstTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsIndexesDataObj;



### handle bidirectional processing to get new tables with all new indexes names between srcDb and dstDb tables ###

def handleBidirProcsngToGetNewTblsAllIndexesInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsIndexesDataObj = {};
    tblsIndexesDataObj['srcDbTblsNewIndxNameDataObj'] = {};
    tblsIndexesDataObj['srcDbAllIndexDataObj'] = {}; 
    tblsIndexesDataObj['dstDbTblsNewIndxNameDataObj'] = {};
    tblsIndexesDataObj['dstDbAllIndexDataObj'] = {};

    try:

       if srcDbName!="" and dstDbName!="":
          
          global inputArgsDataObj; 
          applyChangesOn = inputArgsDataObj['applyChangesOn'];  


          ### Case 1: Identify new tables with all new indexes names to create for srcDb ###

          dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
          dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);

          allNewTblsAllIndexNameForSrcDbDataObj = getNewTblsAllIndexesInfoBtwnDB(
             srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr'
          );
          if len(allNewTblsAllIndexNameForSrcDbDataObj) > 0 :
             if applyChangesOn == "SrcSvr" : 
                srcTblsDataObj.update(allNewTblsAllIndexNameForSrcDbDataObj);

             tblsIndexesDataObj['srcDbTblsNewIndxNameDataObj'] = allNewTblsAllIndexNameForSrcDbDataObj;
             tblsIndexesDataObj['srcDbAllIndexDataObj'] = srcTblsDataObj;  
               

          ### Case 2: Identify new tables with all new indexes names to create for dstDb ###

          dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
          dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);
 
          allNewTblsAllIndexNameForDstDbDataObj = getNewTblsAllIndexesInfoBtwnDB(
             dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr'
          );
          if len(allNewTblsAllIndexNameForDstDbDataObj) > 0 :
             if applyChangesOn == "DstSvr" : 
                dstTblsDataObj.update(allNewTblsAllIndexNameForDstDbDataObj);

             tblsIndexesDataObj['dstDbTblsNewIndxNameDataObj'] = allNewTblsAllIndexNameForDstDbDataObj;
             tblsIndexesDataObj['dstDbAllIndexDataObj'] = dstTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsIndexesDataObj;



### handle bidirectional processing to get table cols data type changed between srcDb and dstDb ###

def handleBidirProcsngToGetTblsColsDataTypeChangedInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsColsDataTypeChangedDataObj = {};
    tblsColsDataTypeChangedDataObj['srcDbTblsColsDataTypeChangedDataObj'] = {};
    tblsColsDataTypeChangedDataObj['srcDbAllTblsDataObj'] = {}; 
    tblsColsDataTypeChangedDataObj['dstDbTblsColsDataTypeChangedDataObj'] = {};
    tblsColsDataTypeChangedDataObj['dstDbAllTblsDataObj'] = {};

    try:

       if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0:
         
          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];
          isIncludeTblColDataTypeComparsion = inputArgsDataObj['isIncludeTblColDataTypeComparsion'];

          if isIncludeTblColDataTypeComparsion == "Y" :

   
             ### Case 1: Identify table columns data type changed for srcDbName ###

             dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
             dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj)

             colsDataTypeChangedForSrcDbDataObj = getTblsColsDataTypeChangedInfoBtwnDB(
                 srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr'
             );
             if len(colsDataTypeChangedForSrcDbDataObj) > 0 :
                if applyChangesOn == "SrcSvr" :
                   for tblName in colsDataTypeChangedForSrcDbDataObj:
                       isDataAvailableInTbl = colsDataTypeChangedForSrcDbDataObj[tblName]['isDataAvailableInTbl'];
                       srcTblsDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                       srcTblsDataObj[tblName]['tblAllCols'].update(colsDataTypeChangedForSrcDbDataObj[tblName]['tblAllCols']);

                tblsColsDataTypeChangedDataObj['srcDbTblsColsDataTypeChangedDataObj'] = colsDataTypeChangedForSrcDbDataObj;
                tblsColsDataTypeChangedDataObj['srcDbAllTblsDataObj'] = srcTblsDataObj;

          
             ### Case 2: Identify table columns data type changed for dstDbName ###

             dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
             dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);

             colsDataTypeChangedForDstDbDataObj = getTblsColsDataTypeChangedInfoBtwnDB(
                 dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr'
             );
             if len(colsDataTypeChangedForDstDbDataObj) > 0 :
                if applyChangesOn == "DstSvr" :
                   for tblName in colsDataTypeChangedForDstDbDataObj:
                       isDataAvailableInTbl = colsDataTypeChangedForSrcDbDataObj[tblName]['isDataAvailableInTbl'];
                       dstTblsDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                       dstTblsDataObj[tblName]['tblAllCols'].update(colsDataTypeChangedForDstDbDataObj[tblName]['tblAllCols']);

                tblsColsDataTypeChangedDataObj['dstDbTblsColsDataTypeChangedDataObj'] = colsDataTypeChangedForDstDbDataObj;
                tblsColsDataTypeChangedDataObj['dstDbAllTblsDataObj'] = dstTblsDataObj;



    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsColsDataTypeChangedDataObj;



### handle processing to get tables columns definition changed between srcDb and dstDb ###

def handleProcsngToGetTblsColsDefChangedInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsColsDefChangedDataObj = {};

    try:

        if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0 and againstSvr!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];
 
           ### extracted all same table name with all columns data ###
           allTblsDataObj = {};
           for tblName in dstTblsDataObj:
               isTblNameExist = iskeynameExistInDictObj(srcTblsDataObj, tblName);
               if isTblNameExist == True:
                  allTblsDataObj[tblName] = dstTblsDataObj[tblName];

           for tblName in allTblsDataObj: 
               
               isDataAvailableInTbl = configureDbSvrToCheckDataAvailableInTbl(againstSvr, srcDbName, tblName);
  
               ### extracted each same table name with all same name columns data ###
               eachTblAllColsDataObj = {};
               for colName in dstTblsDataObj[tblName]['tblAllCols'] :
                   isColNameExist = iskeynameExistInDictObj(srcTblsDataObj[tblName]['tblAllCols'], colName);
                   if isColNameExist == True:
                      eachTblAllColsDataObj[colName] = colName;

               eachTblAllExistColsDefChangedDataObj = {};

               for colName in eachTblAllColsDataObj:  

                   frmTblColDataArr = srcTblsDataObj[tblName]['tblAllCols'][colName]['updatedColData'];
                   toTblColDataArr = dstTblsDataObj[tblName]['tblAllCols'][colName]['updatedColData'];

                   frmTblRefColDataObj = srcTblsDataObj[tblName]['tblAllCols'][colName]['refColDataObj']; 
                   refColDefChangedDataArr = frmTblRefColDataObj['colDefChangedDataArr'];
                   refColDataTypeChangedDataArr = frmTblRefColDataObj['colDataTypeChangedDataArr'];

                   frmTblColDataTypeStr = frmTblColDataArr[3];
                   toTblColDataTypeStr = toTblColDataArr[3];

                   ### detetcing is col name rename as new name ###
                   frmTblOldColNameStr = "";
                   frmTblColNameAsRenameNewColNameStr = colName;
                   isFrmTblOldColNameRenameAsNewColName = 'N';    
                   isFrmTblOldColNameKeyExist = iskeynameExistInDictObj(srcTblsDataObj[tblName]['tblAllCols'][colName], 'oldColName');
                   if isFrmTblOldColNameKeyExist == True:
                      frmTblOldColNameStr = srcTblsDataObj[tblName]['tblAllCols'][colName]['oldColName'];
                      if frmTblOldColNameStr != frmTblColNameAsRenameNewColNameStr :
                         isFrmTblOldColNameRenameAsNewColName = 'Y';
   
    
                   ### same data type ###
                   if frmTblColDataTypeStr==toTblColDataTypeStr:
                      
                      colDefChangedDataArr = ();
                      if frmTblColDataArr[1:8] != toTblColDataArr[1:8] or isFrmTblOldColNameRenameAsNewColName == "Y" :
                         colDefChangedDataArr = toTblColDataArr;

                      colDefChangedDataArrLen = len(colDefChangedDataArr); 
                      if colDefChangedDataArrLen > 0:

                         ### existing column config data extracted ###  
                         existingUpdatedColConfig = srcTblsDataObj[tblName]['tblAllCols'][colName]['updatedColConfig'];

                         ### preparing column config for reference purpose and stored in array as version no concept ###
                         refColConfig = {
                            'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 'copyDbName': dstDbName, 
                            'copyTblName': tblName, 'copyColName': colName
                         }; 
                         refColDefChangedDataArr.append({"refColConfig": refColConfig, "colDataArr": colDefChangedDataArr});

                         if len(existingUpdatedColConfig)<=0:
                            existingUpdatedColConfig = refColConfig;

                         eachTblAllExistColsDefChangedDataObj[colName] = {
                             'oldColName' : frmTblOldColNameStr,
                             'renameColName' : frmTblColNameAsRenameNewColNameStr,
                             'updatedColConfig': existingUpdatedColConfig, 
                             'updatedColData': colDefChangedDataArr,
                             'orgColData': srcTblsDataObj[tblName]['tblAllCols'][colName]['orgColData'],
                             'refColDataObj': {
                                 'colDefChangedDataArr': refColDefChangedDataArr, 
                                 'colDataTypeChangedDataArr': refColDataTypeChangedDataArr
                             }
                         };


               if len(eachTblAllExistColsDefChangedDataObj) > 0: 
                  tblsColsDefChangedDataObj[tblName] = {};
                  tblsColsDefChangedDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                  tblsColsDefChangedDataObj[tblName]['tblAllCols'] = eachTblAllExistColsDefChangedDataObj;
        

    except Exception as e:
           handleProcsngAbtErrException("Y");

    return tblsColsDefChangedDataObj;



### handle bidirectional processing to get tables cols type def changed between srcDb and dstDb ###

def handleBidirProcsngToGetTblsColsDefChangedInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsColsDefChangedDataObj = {};
    tblsColsDefChangedDataObj['srcDbTblsColsDefChangedDataObj'] = {};
    tblsColsDefChangedDataObj['srcDbAllTblsDataObj'] = {}; 
    tblsColsDefChangedDataObj['dstDbTblsColsDefChangedDataObj'] = {};
    tblsColsDefChangedDataObj['dstDbAllTblsDataObj'] = {};

    try:

       if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0:

          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];
          isIncludeTblColDefComparsion = inputArgsDataObj['isIncludeTblColDefComparsion'];
          
          if isIncludeTblColDefComparsion == "Y" :


             ### Case 1: Identify table columns definition changed for srcDbName ###

             dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
             dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);

             colsDefChangedForSrcDbDataObj = handleProcsngToGetTblsColsDefChangedInfoBtwnDB(
                 srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr'
             );
             if len(colsDefChangedForSrcDbDataObj) > 0 :
                if applyChangesOn == "SrcSvr" :
                   for tblName in colsDefChangedForSrcDbDataObj:
                       isDataAvailableInTbl = colsDefChangedForSrcDbDataObj[tblName]['isDataAvailableInTbl'];
                       srcTblsDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                       srcTblsDataObj[tblName]['tblAllCols'].update(colsDefChangedForSrcDbDataObj[tblName]['tblAllCols']);

                tblsColsDefChangedDataObj['srcDbTblsColsDefChangedDataObj'] = colsDefChangedForSrcDbDataObj;
                tblsColsDefChangedDataObj['srcDbAllTblsDataObj'] = srcTblsDataObj;

          
             ### Case 2: Identify table columns definition changed for dstDbName ###

             dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
             dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);

             colsDefChangedForDstDbDataObj = handleProcsngToGetTblsColsDefChangedInfoBtwnDB(
                 dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr'
             );
             if len(colsDefChangedForDstDbDataObj) > 0 :
                if applyChangesOn == "DstSvr" :
                   for tblName in colsDefChangedForDstDbDataObj:
                       isDataAvailableInTbl = colsDefChangedForDstDbDataObj[tblName]['isDataAvailableInTbl'];
                       dstTblsDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl; 
                       dstTblsDataObj[tblName]['tblAllCols'].update(colsDefChangedForDstDbDataObj[tblName]['tblAllCols']);

                tblsColsDefChangedDataObj['dstDbTblsColsDefChangedDataObj'] = colsDefChangedForDstDbDataObj;
                tblsColsDefChangedDataObj['dstDbAllTblsDataObj'] = dstTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsColsDefChangedDataObj;



### handle bidirectional processing to get tables new columns between srcDb and dstDb ###

def handleBidirProcsngToGetTblsNewColsInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsColsDataObj = {};
    tblsColsDataObj['srcDbTblsNewColsDataObj'] = {};
    tblsColsDataObj['srcDbAllTblsDataObj'] = {}; 
    tblsColsDataObj['dstDbTblsNewColsDataObj'] = {};
    tblsColsDataObj['dstDbAllTblsDataObj'] = {};

    try:


       if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0:

          global inputArgsDataObj; 
          applyChangesOn = inputArgsDataObj['applyChangesOn'];


          ### Case 1: Identify tables new columns to create for srcDb ###

          dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
          dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);

          tblsNewColsForSrcDbDataObj = getTblsNewColsInfoBtwnDB(srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr');
          if len(tblsNewColsForSrcDbDataObj) > 0:
             if applyChangesOn == "SrcSvr" : 
                for tblName in tblsNewColsForSrcDbDataObj:
                    isDataAvailableInTbl = tblsNewColsForSrcDbDataObj[tblName]['isDataAvailableInTbl'];
                    srcTblsDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl; 
                    srcTblsDataObj[tblName]['tblAllCols'].update(tblsNewColsForSrcDbDataObj[tblName]['tblAllCols']);
             
             tblsColsDataObj['srcDbTblsNewColsDataObj'] = tblsNewColsForSrcDbDataObj;
             tblsColsDataObj['srcDbAllTblsDataObj'] = srcTblsDataObj;  
               

          ### Case 2: Identify tables new columns to create for dstDb ###

          dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
          dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);

          tblsNewColsForDstDbDataObj = getTblsNewColsInfoBtwnDB(dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr');
          if len(tblsNewColsForDstDbDataObj) > 0:
             if applyChangesOn == "DstSvr" :
                for tblName in tblsNewColsForDstDbDataObj:
                    isDataAvailableInTbl = tblsNewColsForDstDbDataObj[tblName]['isDataAvailableInTbl'];
                    dstTblsDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl; 
                    dstTblsDataObj[tblName]['tblAllCols'].update(tblsNewColsForDstDbDataObj[tblName]['tblAllCols']);
            
             tblsColsDataObj['dstDbTblsNewColsDataObj'] = tblsNewColsForDstDbDataObj;
             tblsColsDataObj['dstDbAllTblsDataObj'] = dstTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsColsDataObj;



### handle bidirectional processing to get new tables between srcDb and dstDb ###

def handleBidirProcsngToGetNewTblsInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsDataObj = {};
    tblsDataObj['srcDbNewTblsDataObj'] = {};
    tblsDataObj['srcDbAllTblsDataObj'] = {}; 
    tblsDataObj['dstDbNewTblsDataObj'] = {};
    tblsDataObj['dstDbAllTblsDataObj'] = {};

    try:

       if srcDbName!="" and dstDbName!="":
          
          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];


          ### Case 1: Identify new tables to create for srcDbName ###
          
          dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
          dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);
   
          newTblsForSrcDbDataObj = getNewTblsInfoBtwnDB(srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr');
          if len(newTblsForSrcDbDataObj) > 0:
             if applyChangesOn == "SrcSvr" :
                srcTblsDataObj.update(newTblsForSrcDbDataObj);

             tblsDataObj['srcDbNewTblsDataObj'] = newTblsForSrcDbDataObj;
             tblsDataObj['srcDbAllTblsDataObj'] = srcTblsDataObj;


          ### Case 2: Identify new tables to create for dstDbName ###

          dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
          dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);
                
          newTblsForDstDbDataObj = getNewTblsInfoBtwnDB(dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr');
          if len(newTblsForDstDbDataObj) > 0:
             if applyChangesOn == "DstSvr" :
                dstTblsDataObj.update(newTblsForDstDbDataObj);

             tblsDataObj['dstDbNewTblsDataObj'] = newTblsForDstDbDataObj;
             tblsDataObj['dstDbAllTblsDataObj'] = dstTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return tblsDataObj;



### handle processing to get tables attributes options definition changed between srcDb and dstDb ###

def handleProcsngToGetTblsAttrOptnDefChangedInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,againstSvr):

    tblsAttrOptnChangedDataObj = {};

    try:

        if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0 and againstSvr!="":

           dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
           dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
           dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
           dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
           dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];
 
           ### extracted all same table name with all columns data ###
           allTblsDataObj = {};
           for tblName in dstTblsDataObj:
               isTblNameExist = iskeynameExistInDictObj(srcTblsDataObj, tblName);
               if isTblNameExist == True:
                  allTblsDataObj[tblName] = dstTblsDataObj[tblName];


           for tblName in allTblsDataObj: 
               
               frmTblDataArr = srcTblsDataObj[tblName]['updatedTblData'];
               toTblDataArr = dstTblsDataObj[tblName]['updatedTblData'];
               frmTblRefDataObj = srcTblsDataObj[tblName]['refTblDataObj']; 
               refTblDefChangedDataArr = frmTblRefDataObj['tblDefChangedDataArr'];

               if frmTblDataArr[1:6] != toTblDataArr[1:6]:
                  
                  tblDefChangedDataArr = toTblDataArr;
                  
                  ### existing tbl config data extracted ###
                  existingUpdatedTblConfig = srcTblsDataObj[tblName]['updatedTblConfig'];

                  ### preparing column config for reference purpose and stored in array as version no concept ###
                  refTblConfig = {
                    'dbHOST': dbHOST, 'dbPORTNO' : dbPORTNO, 'dbUSER': dbUSER, 'dbPASS': dbPASS, 'copyDbName': dstDbName, 
                    'copyTblName': tblName
                  }; 
                  refTblDefChangedDataArr.append({"refTblConfig": refTblConfig, "tblDataArr": tblDefChangedDataArr});

                  if len(existingUpdatedTblConfig)<=0:
                     existingUpdatedTblConfig = refTblConfig;

                  tblsAttrOptnChangedDataObj[tblName] = {};
                  tblsAttrOptnChangedDataObj[tblName]['isDataAvailableInTbl'] = srcTblsDataObj[tblName]['isDataAvailableInTbl'];  
                  tblsAttrOptnChangedDataObj[tblName]['updatedTblConfig'] = existingUpdatedTblConfig;
                  tblsAttrOptnChangedDataObj[tblName]['updatedTblData'] = tblDefChangedDataArr;
                  tblsAttrOptnChangedDataObj[tblName]['orgTblData'] = dstTblsDataObj[tblName]['orgTblData'];
                  tblsAttrOptnChangedDataObj[tblName]['refTblDataObj'] = refTblDefChangedDataArr;
        

    except Exception as e:
           handleProcsngAbtErrException("Y");

    return tblsAttrOptnChangedDataObj;




### handle bidirectional processing to get tables attributes options def changed between srcDb and dstDb ###

def handleBidirProcsngToGetTblsAttrOptnDefChangedInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsAttrOptnDefChangedDataObj = {};
    tblsAttrOptnDefChangedDataObj['srcDbTblsAttrOptnDefChangedDataObj'] = {};
    tblsAttrOptnDefChangedDataObj['srcDbAllTblsDataObj'] = {}; 
    tblsAttrOptnDefChangedDataObj['dstDbTblsAttrOptnDefChangedDataObj'] = {};
    tblsAttrOptnDefChangedDataObj['dstDbAllTblsDataObj'] = {};

    try:

       if srcDbName!="" and len(srcTblsDataObj)>0 and dstDbName!="" and len(dstTblsDataObj)>0:

          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];
          isIncludeTblAttrOptnComparsion = inputArgsDataObj['isIncludeTblAttrOptnComparsion'];
          
          if isIncludeTblAttrOptnComparsion == "Y" :


             ### Case 1: Identify table attribute option definition changed for srcDbName ###

             dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
             dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);

             attrOptnDefChangedForSrcDbTblDataObj = handleProcsngToGetTblsAttrOptnDefChangedInfoBtwnDB(
                 srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr'
             );
             if len(attrOptnDefChangedForSrcDbTblDataObj) > 0 :
                if applyChangesOn == "SrcSvr" :
                   for tblName in attrOptnDefChangedForSrcDbTblDataObj:
                       srcTblsDataObj[tblName].update(attrOptnDefChangedForSrcDbTblDataObj[tblName]);

                tblsAttrOptnDefChangedDataObj['srcDbTblsAttrOptnDefChangedDataObj'] = attrOptnDefChangedForSrcDbTblDataObj;
                tblsAttrOptnDefChangedDataObj['srcDbAllTblsDataObj'] = srcTblsDataObj;

          
             ### Case 2: Identify table attribute option definition changed for dstDbName ###

             dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
             dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);

             attrOptnDefChangedForDstDbTblDataObj = handleProcsngToGetTblsAttrOptnDefChangedInfoBtwnDB(
                 dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr'
             );
             if len(attrOptnDefChangedForDstDbTblDataObj) > 0 :
                if applyChangesOn == "DstSvr" :
                   for tblName in attrOptnDefChangedForDstDbTblDataObj:
                       dstTblsDataObj[tblName].update(attrOptnDefChangedForDstDbTblDataObj[tblName]);

                tblsAttrOptnDefChangedDataObj['dstDbTblsAttrOptnDefChangedDataObj'] = attrOptnDefChangedForDstDbTblDataObj;
                tblsAttrOptnDefChangedDataObj['dstDbAllTblsDataObj'] = dstTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


    return tblsAttrOptnDefChangedDataObj;



### handle bidirectional processing to get new tables with attributes otpions between srcDb and dstDb ###

def handleBidirProcsngToGetNewTblsAttrOptnInfoBtwnDB(srcDbName,srcTblsDataObj,dstDbName,dstTblsDataObj,isMakeExactDbSchemasCopy):

    tblsDataObj = {};
    tblsDataObj['srcDbNewTblsDataObj'] = {};
    tblsDataObj['srcDbAllTblsDataObj'] = {}; 
    tblsDataObj['dstDbNewTblsDataObj'] = {};
    tblsDataObj['dstDbAllTblsDataObj'] = {};

    try:

       if srcDbName!="" and dstDbName!="":
          
          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];


          ### Case 1: Identify new tables to create for srcDbName ###
          
          dcSrcTblsDataObj1 = copy.deepcopy(srcTblsDataObj);
          dcDstTblsDataObj1 = copy.deepcopy(dstTblsDataObj);
   
          newTblsForSrcDbDataObj = getNewTblsAttrOptnInfoBtwnDB(srcDbName, dcSrcTblsDataObj1, dstDbName, dcDstTblsDataObj1, 'DstSvr');
          if len(newTblsForSrcDbDataObj) > 0:
             if applyChangesOn == "SrcSvr" :
                srcTblsDataObj.update(newTblsForSrcDbDataObj);

             tblsDataObj['srcDbNewTblsDataObj'] = newTblsForSrcDbDataObj;
             tblsDataObj['srcDbAllTblsDataObj'] = srcTblsDataObj;


          ### Case 2: Identify new tables to create for dstDbName ###

          dcDstTblsDataObj2 = copy.deepcopy(dstTblsDataObj);
          dcSrcTblsDataObj2 = copy.deepcopy(srcTblsDataObj);
                
          newTblsForDstDbDataObj = getNewTblsAttrOptnInfoBtwnDB(dstDbName, dcDstTblsDataObj2, srcDbName, dcSrcTblsDataObj2, 'SrcSvr');
          if len(newTblsForDstDbDataObj) > 0:
             if applyChangesOn == "DstSvr" :
                dstTblsDataObj.update(newTblsForDstDbDataObj);

             tblsDataObj['dstDbNewTblsDataObj'] = newTblsForDstDbDataObj;
             tblsDataObj['dstDbAllTblsDataObj'] = dstTblsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return tblsDataObj;




### handle processing schemas comparsion between srcDb and dstDb ###

def handleProcsngSchmsCmpBtwnSrcAndDstDB(inputArgsDataObj,srcDbName,srcDbDataObj,dstDbName,dstDbDataObj,applyChangesOn,isMakeExactDbSchemasCopy):

    diffDBSchmsDataObj = {};

    try:

        if srcDbName!="" and len(srcDbDataObj)>0 and dstDbName!="" and len(dstDbDataObj)>0:
       
           ### variable declare for collecting original setup srcDbName infoSchemas data ###

           diffDBSchmsDataObj[srcDbName] = {};
           diffDBSchmsDataObj[srcDbName]['NFKTblsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['NFKTblsAttrOptnDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['NFKTblsColsRenameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['NFKTblsIndexesDataObj'] = {};  
           diffDBSchmsDataObj[srcDbName]['FKAsNFKTblsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['FKAsNFKTblsAttrOptnDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['FKAsNFKTblsColsRenameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['FKAsNFKTblsConstraintsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['FKAsNFKTblsIndexesDataObj'] = {}; 
           diffDBSchmsDataObj[srcDbName]['FKTblsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['FKTblsAttrOptnDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['FKTblsColsRenameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['FKTblsConstraintsDataObj'] = {};            
           diffDBSchmsDataObj[srcDbName]['FKTblsIndexesDataObj'] = {}; 
           diffDBSchmsDataObj[srcDbName]['triggersDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['routinesDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['independentViewsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['InAsDependentViewsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['dependentViewsDataObj'] = {}; 


           ### variable declare for collecting adding/modification/updation changes on original setup srcDbName infoSchemas data ###

           ### section about nfk types tables data ###

           diffDBSchmsDataObj[srcDbName]['srcDbNewNFKTblsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNewNFKTblsAttrOptnDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsAttrOptnDefChangedDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsNewColsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsColsPositionDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsColsRenameDataObj'] = {}; 
           diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsColsDefChangedDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsColsDataTypeChangedDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNewNFKTblsAllIndxNameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsNewIndxNameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNFKTblIndxNewColsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNFKTblIndxColsChangedDataObj'] = {};


           ### section about fk as nfk types tables data

           diffDBSchmsDataObj[srcDbName]['srcDbNewFKAsNFKTblsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNewFKAsNFKTblsAttrOptnDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsAttrOptnDefChangedDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsNewColsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsColsPositionDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsColsRenameDataObj'] = {}; 
           diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsColsDefChangedDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsColsDataTypeChangedDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNewFKAsNFKTblsFKNameColConstraintsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsNewFKNameColConstraintsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsFKNameNewColsConstraintsDataObj'] = {}; 
           diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsFKNameColConstraintsDefDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNewFKAsNFKTblsAllIndxNameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsNewIndxNameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblIndxNewColsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblIndxColsChangedDataObj'] = {};
         

           ### section about fk types tables data
   
           diffDBSchmsDataObj[srcDbName]['srcDbNewFKTblsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNewFKTblsAttrOptnDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKTblsAttrOptnDefChangedDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKTblsNewColsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKTblsColsPositionDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKTblsColsRenameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKTblsColsDefChangedDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKTblsColsDataTypeChangedDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNewFKTblsFKNameColConstraintsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKTblsNewFKNameColConstraintsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKTblsFKNameNewColsConstraintsDataObj'] = {}; 
           diffDBSchmsDataObj[srcDbName]['srcDbFKTblsFKNameColConstraintsDefDataObj'] = {}; 
           diffDBSchmsDataObj[srcDbName]['srcDbNewFKTblsAllIndxNameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFKTblsNewIndxNameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFkTblIndxNewColsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbFkTblIndxColsChangedDataObj'] = {};


           ### section about tables trigger data

           diffDBSchmsDataObj[srcDbName]['srcDbNewTblsAllTgrNameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbTblsNewTgrNameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbTblsTgrDefChangedDataObj'] = {};


           ### section about DB routines data

           diffDBSchmsDataObj[srcDbName]['srcDbNewRoutinesTypeDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNewRoutinesNameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbRoutinesNameDefChangedDataObj'] = {};


           ### section about DB views data

           diffDBSchmsDataObj[srcDbName]['srcDbNewIndependentViewsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbIndependentViewsDefChangedDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbNewInAsDependentViewsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbInAsDependentViewsDefChangedDataObj'] = {}; 
           diffDBSchmsDataObj[srcDbName]['srcDbNewDependentViewsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDependentViewsDefChangedDataObj'] = {};


           ### variable declare for collecting dropping changes from original setup srcDbName infoSchemas data ###


           ### section about nfk types tables data ###

           diffDBSchmsDataObj[srcDbName]['srcDbDrpNFKTblsDataObj'] = {}; 
           diffDBSchmsDataObj[srcDbName]['srcDbDrpNFKTblsNewColsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpNFKTblsAllIndxNameDataObj'] = {}; 
           diffDBSchmsDataObj[srcDbName]['srcDbDrpNFKTblsNewIndxNameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpNFKTblIndxNewColsDataObj'] = {};


           ### section about fk as nfk types tables data ###
 
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblsDataObj'] = {}; 
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblsNewColsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblsFKNameColConstraintsDataObj'] = {}; 
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblsNewFKNameColConstraintsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblsFKNameNewColsConstraintsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblsAllIndxNameDataObj'] = {}; 
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblsNewIndxNameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblIndxNewColsDataObj'] = {};

  
           ### section about fk types tables data ###

           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKTblsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKTblsNewColsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKTblsFKNameColConstraintsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKTblsNewFKNameColConstraintsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKTblsFKNameNewColsConstraintsDataObj'] = {};   
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKTblsAllIndxNameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFKTblsNewIndxNameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpFkTblIndxNewColsDataObj'] = {};


           ### section about tables triggers data ###

           diffDBSchmsDataObj[srcDbName]['srcDbDrpTblsAllTgrNameDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpTblsNewTgrNameDataObj'] = {};

         
           ### section about DB routines data ###

           diffDBSchmsDataObj[srcDbName]['srcDbDrpRoutinesTypeDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpRoutinesNameDataObj'] = {};  


           ### section about DB views data ###

           diffDBSchmsDataObj[srcDbName]['srcDbDrpIndependentViewsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpInAsDependentViewsDataObj'] = {};
           diffDBSchmsDataObj[srcDbName]['srcDbDrpDependentViewsDataObj'] = {};



           ### variable declare for collecting original setup dstDbName infoSchemas data ###

           diffDBSchmsDataObj[dstDbName] = {};
           diffDBSchmsDataObj[dstDbName]['NFKTblsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['NFKTblsAttrOptnDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['NFKTblsColsRenameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['NFKTblsIndexesDataObj'] = {};  
           diffDBSchmsDataObj[dstDbName]['FKAsNFKTblsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['FKAsNFKTblsAttrOptnDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['FKAsNFKTblsColsRenameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['FKAsNFKTblsConstraintsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['FKAsNFKTblsIndexesDataObj'] = {}; 
           diffDBSchmsDataObj[dstDbName]['FKTblsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['FKTblsAttrOptnDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['FKTblsColsRenameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['FKTblsConstraintsDataObj'] = {};            
           diffDBSchmsDataObj[dstDbName]['FKTblsIndexesDataObj'] = {}; 
           diffDBSchmsDataObj[dstDbName]['triggersDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['routinesDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['independentViewsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['InAsDependentViewsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dependentViewsDataObj'] = {}; 


           ### variable declare for collecting adding/modification/updation changes on original setup dstDbName infoSchemas data ###


           ### section about nfk types tables data ###

           diffDBSchmsDataObj[dstDbName]['dstDbNewNFKTblsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNewNFKTblsAttrOptnDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsAttrOptnDefChangedDataObj'] = {}; 
           diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsNewColsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsColsPositionDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsColsRenameDataObj'] = {}; 
           diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsColsDefChangedDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsColsDataTypeChangedDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNewNFKTblsAllIndxNameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsNewIndxNameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNFKTblIndxNewColsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNFKTblIndxColsChangedDataObj'] = {};  


           ### section about fk as nfk tables data ###

           diffDBSchmsDataObj[dstDbName]['dstDbNewFKAsNFKTblsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNewFKAsNFKTblsAttrOptnDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsAttrOptnDefChangedDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsNewColsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsColsPositionDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsColsRenameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsColsDefChangedDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsColsDataTypeChangedDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNewFKAsNFKTblsFKNameColConstraintsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsNewFKNameColConstraintsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsFKNameNewColsConstraintsDataObj'] = {}; 
           diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsFKNameColConstraintsDefDataObj'] = {};   
           diffDBSchmsDataObj[dstDbName]['dstDbNewFKAsNFKTblsAllIndxNameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsNewIndxNameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblIndxNewColsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblIndxColsChangedDataObj'] = {};  


           ### section about fk types tables data ###

           diffDBSchmsDataObj[dstDbName]['dstDbNewFKTblsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNewFKTblsAttrOptnDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKTblsAttrOptnDefChangedDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKTblsNewColsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKTblsColsPositionDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKTblsColsRenameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKTblsColsDefChangedDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKTblsColsDataTypeChangedDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNewFKTblsFKNameColConstraintsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKTblsNewFKNameColConstraintsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKTblsFKNameNewColsConstraintsDataObj'] = {}; 
           diffDBSchmsDataObj[dstDbName]['dstDbFKTblsFKNameColConstraintsDefDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNewFKTblsAllIndxNameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFKTblsNewIndxNameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFkTblIndxNewColsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbFkTblIndxColsChangedDataObj'] = {};


           ### section about tables triggers data ###

           diffDBSchmsDataObj[dstDbName]['dstDbNewTblsAllTgrNameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbTblsNewTgrNameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbTblsTgrDefChangedDataObj'] = {};


           ### section about DB routines data ###

           diffDBSchmsDataObj[dstDbName]['dstDbNewRoutinesTypeDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNewRoutinesNameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbRoutinesNameDefChangedDataObj'] = {};


           ### section about DB views data ###
        
           diffDBSchmsDataObj[dstDbName]['dstDbNewIndependentViewsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbIndependentViewsDefChangedDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbNewInAsDependentViewsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbInAsDependentViewsDefChangedDataObj'] = {}; 
           diffDBSchmsDataObj[dstDbName]['dstDbNewDependentViewsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDependentViewsDefChangedDataObj'] = {};



           ### variable declare for collecting dropping changes from original setup dstDbName infoSchemas data ###


           ### section about nfk types tables data ###

           diffDBSchmsDataObj[dstDbName]['dstDbDrpNFKTblsDataObj'] = {}; 
           diffDBSchmsDataObj[dstDbName]['dstDbDrpNFKTblsNewColsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpNFKTblsAllIndxNameDataObj'] = {}; 
           diffDBSchmsDataObj[dstDbName]['dstDbDrpNFKTblsNewIndxNameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpNFKTblIndxNewColsDataObj'] = {};


           ### section about fk as nfk types tables data ###
 
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblsDataObj'] = {}; 
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblsNewColsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblsFKNameColConstraintsDataObj'] = {}; 
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblsNewFKNameColConstraintsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblsFKNameNewColsConstraintsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblsAllIndxNameDataObj'] = {}; 
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblsNewIndxNameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblIndxNewColsDataObj'] = {};

  
           ### section about fk types tables data ###

           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblsNewColsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblsFKNameColConstraintsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblsNewFKNameColConstraintsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblsFKNameNewColsConstraintsDataObj'] = {};   
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblsAllIndxNameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblsNewIndxNameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblIndxNewColsDataObj'] = {};


           ### section about tables triggers data ###

           diffDBSchmsDataObj[dstDbName]['dstDbDrpTblsAllTgrNameDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpTblsNewTgrNameDataObj'] = {};

         
           ### section about DB routines data ###

           diffDBSchmsDataObj[dstDbName]['dstDbDrpRoutinesTypeDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpRoutinesNameDataObj'] = {};  


           ### section about DB views data ###

           diffDBSchmsDataObj[dstDbName]['dstDbDrpIndependentViewsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpInAsDependentViewsDataObj'] = {};
           diffDBSchmsDataObj[dstDbName]['dstDbDrpDependentViewsDataObj'] = {};


           ### variable declare for extracting srcDB setup infoSchemas data
           
           srcDbNFKTblsDataObj = {};
           srcDbNFKTblsAttrOptnDataObj = {};
           srcDbNFKTblsIndexesDataObj = {};
           srcDbFKAsNFKTblsDataObj = {};
           srcDbFKAsNFKTblsAttrOptnDataObj = {};
           srcDbFKAsNFKTblsConstraintsDataObj = {};
           srcDbFKAsNFKTblsIndexesDataObj = {};
           srcDbFKTblsDataObj = {};
           srcDbFKTblsAttrOptnDataObj = {};
           srcDbFKTblsConstraintsDataObj = {};
           srcDbFKTblsIndexesDataObj = {};
           srcDbTriggersDataObj = {};
           srcDbRoutinesDataObj = {};
           srcDbIndependentViewsDataObj = {};
           srcDbInAsDependentViewsDataObj = {};
           srcDbDependentViewsDataObj = {};


           ### section about nfk types tables ###

           isSrcDbNFKTblsDataExist = iskeynameExistInDictObj(srcDbDataObj, 'NFKTblsDataObj');
           if isSrcDbNFKTblsDataExist == True:
              srcDbNFKTblsDataObj = srcDbDataObj['NFKTblsDataObj'];

           isSrcDbNFKTblsAttrOptnDataObjExist = iskeynameExistInDictObj(srcDbDataObj, 'NFKTblsAttrOptnDataObj');
           if isSrcDbNFKTblsAttrOptnDataObjExist == True:
              srcDbNFKTblsAttrOptnDataObj = srcDbDataObj['NFKTblsAttrOptnDataObj'];

           isSrcDbNFKTblsColsRenameDataObjExist = iskeynameExistInDictObj(srcDbDataObj, 'NFKTblsColsRenameDataObj');
           if isSrcDbNFKTblsColsRenameDataObjExist == True:
              diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsColsRenameDataObj'] = srcDbDataObj['NFKTblsColsRenameDataObj'];  

           isSrcDbNFKTblsIndexesDataExist = iskeynameExistInDictObj(srcDbDataObj, 'NFKTblsIndexesDataObj');
           if isSrcDbNFKTblsIndexesDataExist == True:
              srcDbNFKTblsIndexesDataObj = srcDbDataObj['NFKTblsIndexesDataObj'];


           ### section about fk as nfk types tables ###

           isSrcDbFKAsNFKTblsDataExist = iskeynameExistInDictObj(srcDbDataObj, 'FKAsNFKTblsDataObj');
           if isSrcDbFKAsNFKTblsDataExist == True:
              srcDbFKAsNFKTblsDataObj = srcDbDataObj['FKAsNFKTblsDataObj'];

           isSrcDbFKAsNFKTblsAttrOptnDataObj = iskeynameExistInDictObj(srcDbDataObj, 'FKAsNFKTblsAttrOptnDataObj');
           if isSrcDbFKAsNFKTblsAttrOptnDataObj == True:
              srcDbFKAsNFKTblsAttrOptnDataObj = srcDbDataObj['FKAsNFKTblsAttrOptnDataObj'];

           isSrcDbFKAsNFKTblsColsRenameDataObjExist = iskeynameExistInDictObj(srcDbDataObj, 'FKAsNFKTblsColsRenameDataObj');
           if isSrcDbFKAsNFKTblsColsRenameDataObjExist == True:
              diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsColsRenameDataObj'] = srcDbDataObj['FKAsNFKTblsColsRenameDataObj'];
 
           isSrcDbFKAsNFKTblsConstraintsDataObjExist = iskeynameExistInDictObj(srcDbDataObj, 'FKAsNFKTblsConstraintsDataObj');
           if isSrcDbFKAsNFKTblsConstraintsDataObjExist == True:
              srcDbFKAsNFKTblsConstraintsDataObj = srcDbDataObj['FKAsNFKTblsConstraintsDataObj'];

           isSrcDbFKAsNFKTblsIndexesDataExist = iskeynameExistInDictObj(srcDbDataObj, 'FKAsNFKTblsIndexesDataObj');
           if isSrcDbFKAsNFKTblsIndexesDataExist == True:
              srcDbFKAsNFKTblsIndexesDataObj = srcDbDataObj['FKAsNFKTblsIndexesDataObj'];
 

           ### section about fk types tables ###
  
           isSrcDbFKTblsDataExist = iskeynameExistInDictObj(srcDbDataObj, 'FKTblsDataObj');
           if isSrcDbFKTblsDataExist == True:
              srcDbFKTblsDataObj = srcDbDataObj['FKTblsDataObj'];

           isSrcDbFKTblsAttrOptnDataObjExist = iskeynameExistInDictObj(srcDbDataObj, 'FKTblsAttrOptnDataObj');
           if isSrcDbFKTblsAttrOptnDataObjExist == True:
              srcDbFKTblsAttrOptnDataObj = srcDbDataObj['FKTblsAttrOptnDataObj'];

           isSrcDbFKTblsColsRenameDataObjExist = iskeynameExistInDictObj(srcDbDataObj, 'FKTblsColsRenameDataObj');
           if isSrcDbFKTblsColsRenameDataObjExist == True:
              diffDBSchmsDataObj[srcDbName]['srcDbFKTblsColsRenameDataObj'] = srcDbDataObj['FKTblsColsRenameDataObj'];  

           isSrcDbFKTblsConstraintsDataObjExist = iskeynameExistInDictObj(srcDbDataObj, 'FKTblsConstraintsDataObj');
           if isSrcDbFKTblsConstraintsDataObjExist == True:
              srcDbFKTblsConstraintsDataObj = srcDbDataObj['FKTblsConstraintsDataObj']; 

           isSrcDbFKTblsIndexesDataExist = iskeynameExistInDictObj(srcDbDataObj, 'FKTblsIndexesDataObj');
           if isSrcDbFKTblsIndexesDataExist == True:
              srcDbFKTblsIndexesDataObj = srcDbDataObj['FKTblsIndexesDataObj'];    


           ### section about tables triggers ###
  
           isSrcDbTriggersDataExist = iskeynameExistInDictObj(srcDbDataObj, 'triggersDataObj');
           if isSrcDbTriggersDataExist == True:
              srcDbTriggersDataObj = srcDbDataObj['triggersDataObj'];

           ### section about routines ###

           isSrcDbRoutinesDataExist = iskeynameExistInDictObj(srcDbDataObj, 'routinesDataObj');
           if isSrcDbRoutinesDataExist == True:
              srcDbRoutinesDataObj = srcDbDataObj['routinesDataObj'];

           ### section about views ###

           isSrcDbIndependentViewsDataExist = iskeynameExistInDictObj(srcDbDataObj, 'independentViewsDataObj');
           if isSrcDbIndependentViewsDataExist == True:
              srcDbIndependentViewsDataObj = srcDbDataObj['independentViewsDataObj'];

           isSrcDbInAsDependentViewsDataExist = iskeynameExistInDictObj(srcDbDataObj, 'InAsDependentViewsDataObj');
           if isSrcDbInAsDependentViewsDataExist == True:
              srcDbInAsDependentViewsDataObj = srcDbDataObj['InAsDependentViewsDataObj'];

           isSrcDbDependentViewsDataExist = iskeynameExistInDictObj(srcDbDataObj, 'dependentViewsDataObj');
           if isSrcDbDependentViewsDataExist == True:
              srcDbDependentViewsDataObj = srcDbDataObj['dependentViewsDataObj'];

       
           ### variable declare for extracting dstDB setup infoSchemas data ###

           dstDbNFKTblsDataObj = {};
           dstDbNFKTblsAttrOptnDataObj = {};
           dstDbNFKTblsIndexesDataObj = {};
           dstDbFKAsNFKTblsDataObj = {};
           dstDbFKAsNFKTblsAttrOptnDataObj = {};
           dstDbFKAsNFKTblsConstraintsDataObj = {};
           dstDbFKAsNFKTblsIndexesDataObj = {};
           dstDbFKTblsDataObj = {};
           dstDbFKTblsAttrOptnDataObj = {};
           dstDbFKTblsConstraintsDataObj = {};
           dstDbFKTblsIndexesDataObj = {};
           dstDbTriggersDataObj = {};
           dstDbRoutinesDataObj = {};
           dstDbIndependentViewsDataObj = {};
           dstDbInAsDependentViewsDataObj = {};
           dstDbDependentViewsDataObj = {};

           ### section about nfk types tables ###
 
           isDstDbNFKTblsDataExist = iskeynameExistInDictObj(dstDbDataObj, 'NFKTblsDataObj');
           if isDstDbNFKTblsDataExist == True:
              dstDbNFKTblsDataObj = dstDbDataObj['NFKTblsDataObj'];

           isDstDbNFKTblsAttrOptnDataObjExist = iskeynameExistInDictObj(dstDbDataObj, 'NFKTblsAttrOptnDataObj');
           if isDstDbNFKTblsAttrOptnDataObjExist == True:
              dstDbNFKTblsAttrOptnDataObj = dstDbDataObj['NFKTblsAttrOptnDataObj'];

           isDstDbNFKTblsColsRenameDataObjExist = iskeynameExistInDictObj(dstDbDataObj, 'NFKTblsColsRenameDataObj');
           if isDstDbNFKTblsColsRenameDataObjExist == True:
              diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsColsRenameDataObj'] = dstDbDataObj['NFKTblsColsRenameDataObj'];

           isDstDbNFKTblsIndexesDataExist = iskeynameExistInDictObj(dstDbDataObj, 'NFKTblsIndexesDataObj');
           if isDstDbNFKTblsIndexesDataExist == True:
              dstDbNFKTblsIndexesDataObj = dstDbDataObj['NFKTblsIndexesDataObj'];


           ### section about fk as nfk types tables ###

           isDstDbFKAsNFKTblsDataExist = iskeynameExistInDictObj(dstDbDataObj, 'FKAsNFKTblsDataObj');
           if isDstDbFKAsNFKTblsDataExist == True:
              dstDbFKAsNFKTblsDataObj = dstDbDataObj['FKAsNFKTblsDataObj'];
 
           isDstDbFKAsNFKTblsAttrOptnDataObjExist = iskeynameExistInDictObj(dstDbDataObj, 'FKAsNFKTblsAttrOptnDataObj');
           if isDstDbFKAsNFKTblsAttrOptnDataObjExist == True:
              dstDbFKAsNFKTblsAttrOptnDataObj = dstDbDataObj['FKAsNFKTblsAttrOptnDataObj'];

           isDstDbFKAsNFKTblsColsRenameDataObjExist = iskeynameExistInDictObj(dstDbDataObj, 'FKAsNFKTblsColsRenameDataObj');
           if isDstDbFKAsNFKTblsColsRenameDataObjExist == True:
              diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsColsRenameDataObj'] = dstDbDataObj['FKAsNFKTblsColsRenameDataObj']; 

           isDstDbFKAsNFKTblsConstraintsDataObjExist = iskeynameExistInDictObj(dstDbDataObj, 'FKAsNFKTblsConstraintsDataObj');
           if isDstDbFKAsNFKTblsConstraintsDataObjExist == True:
              dstDbFKAsNFKTblsConstraintsDataObj = dstDbDataObj['FKAsNFKTblsConstraintsDataObj'];

           isDstDbFKAsNFKTblsIndexesDataExist = iskeynameExistInDictObj(dstDbDataObj, 'FKAsNFKTblsIndexesDataObj');
           if isDstDbFKAsNFKTblsIndexesDataExist == True:
              dstDbFKAsNFKTblsIndexesDataObj = dstDbDataObj['FKAsNFKTblsIndexesDataObj'];
 

           ### section about fk types tables ###
 
           isDstDbFKTblsDataExist = iskeynameExistInDictObj(dstDbDataObj, 'FKTblsDataObj');
           if isDstDbFKTblsDataExist == True:
              dstDbFKTblsDataObj = dstDbDataObj['FKTblsDataObj'];

           isDstDbFKTblsAttrOptnDataObjExist = iskeynameExistInDictObj(dstDbDataObj, 'FKTblsAttrOptnDataObj');
           if isDstDbFKTblsAttrOptnDataObjExist == True:
              dstDbFKTblsAttrOptnDataObj = dstDbDataObj['FKTblsAttrOptnDataObj'];

           isDstDbFKTblsColsRenameDataObjExist = iskeynameExistInDictObj(dstDbDataObj, 'FKTblsColsRenameDataObj');
           if isDstDbFKTblsColsRenameDataObjExist == True:
              diffDBSchmsDataObj[dstDbName]['dstDbFKTblsColsRenameDataObj'] = dstDbDataObj['FKTblsColsRenameDataObj']; 

           isDstDbFKTblsConstraintsDataObjExist = iskeynameExistInDictObj(dstDbDataObj, 'FKTblsConstraintsDataObj');
           if isDstDbFKTblsConstraintsDataObjExist == True:
              dstDbFKTblsConstraintsDataObj = dstDbDataObj['FKTblsConstraintsDataObj']; 

           isDstDbFKTblsIndexesDataExist = iskeynameExistInDictObj(dstDbDataObj, 'FKTblsIndexesDataObj');
           if isDstDbFKTblsIndexesDataExist == True:
              dstDbFKTblsIndexesDataObj = dstDbDataObj['FKTblsIndexesDataObj'];    


           ### section about tables triggers ###
 
           isDstDbTriggersDataExist = iskeynameExistInDictObj(dstDbDataObj, 'triggersDataObj');
           if isDstDbTriggersDataExist == True:
              dstDbTriggersDataObj = dstDbDataObj['triggersDataObj'];

           ### section about routines ###
   
           isDstDbRoutinesDataExist = iskeynameExistInDictObj(dstDbDataObj, 'routinesDataObj');
           if isDstDbRoutinesDataExist == True:
              dstDbRoutinesDataObj = dstDbDataObj['routinesDataObj'];

           
           ### section about views ### 

           isDstDbIndependentViewsDataExist = iskeynameExistInDictObj(dstDbDataObj, 'independentViewsDataObj');
           if isDstDbIndependentViewsDataExist == True:
              dstDbIndependentViewsDataObj = dstDbDataObj['independentViewsDataObj'];

           isDstDbInAsDependentViewsDataExist = iskeynameExistInDictObj(dstDbDataObj, 'InAsDependentViewsDataObj');
           if isDstDbInAsDependentViewsDataExist == True:
              dstDbInAsDependentViewsDataObj = dstDbDataObj['InAsDependentViewsDataObj'];

           isDstDbDependentViewsDataExist = iskeynameExistInDictObj(dstDbDataObj, 'dependentViewsDataObj');
           if isDstDbDependentViewsDataExist == True:
              dstDbDependentViewsDataObj = dstDbDataObj['dependentViewsDataObj'];



           ### Section abt to get new nfk tables infoSchemas data ###

           if isExecuteSchmsCmpOnNewTblsOptns(inputArgsDataObj) == "Y" :

              NewNFKTblsDataObj = handleBidirProcsngToGetNewTblsInfoBtwnDB(
                 srcDbName, srcDbNFKTblsDataObj, dstDbName, dstDbNFKTblsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewNFKTblsDataObj'] = NewNFKTblsDataObj['srcDbNewTblsDataObj'];
              if len(NewNFKTblsDataObj['srcDbAllTblsDataObj']) > 0:
                 srcDbNFKTblsDataObj = NewNFKTblsDataObj['srcDbAllTblsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewNFKTblsDataObj'] = NewNFKTblsDataObj['dstDbNewTblsDataObj'];
              if len(NewNFKTblsDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbNFKTblsDataObj = NewNFKTblsDataObj['dstDbAllTblsDataObj'];


           ### Section abt to get all new nfk tables with attributes option infoSchemas data ###
 
           if isExecuteSchmsCmpOnNewTblsAttrOptns(inputArgsDataObj) == "Y" :

              newNFKTblsAttrOptnDataObj = handleBidirProcsngToGetNewTblsAttrOptnInfoBtwnDB(
                 srcDbName, srcDbNFKTblsAttrOptnDataObj, dstDbName, dstDbNFKTblsAttrOptnDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewNFKTblsAttrOptnDataObj'] = newNFKTblsAttrOptnDataObj['srcDbNewTblsDataObj'];
              if len(newNFKTblsAttrOptnDataObj['srcDbAllTblsDataObj']) > 0:
                 srcDbNFKTblsAttrOptnDataObj = newNFKTblsAttrOptnDataObj['srcDbAllTblsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewNFKTblsAttrOptnDataObj'] = newNFKTblsAttrOptnDataObj['dstDbNewTblsDataObj'];
              if len(newNFKTblsAttrOptnDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbNFKTblsAttrOptnDataObj = newNFKTblsAttrOptnDataObj['dstDbAllTblsDataObj'];

       
           ### Section abt to get nfk tables with all attributes options who definition has been changed infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblsAttrOptns(inputArgsDataObj) == "Y" :

              NFKTblsAttrOptnDefChangedDataObj = handleBidirProcsngToGetTblsAttrOptnDefChangedInfoBtwnDB(
                 srcDbName, srcDbNFKTblsAttrOptnDataObj, dstDbName, dstDbNFKTblsAttrOptnDataObj, isMakeExactDbSchemasCopy
              );

              srcDbNFKTblsAttrOptnDefChangedDataObj = NFKTblsAttrOptnDefChangedDataObj['srcDbTblsAttrOptnDefChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsAttrOptnDefChangedDataObj'] = srcDbNFKTblsAttrOptnDefChangedDataObj;
              if len(NFKTblsAttrOptnDefChangedDataObj['srcDbAllTblsDataObj']) > 0:
                 srcDbNFKTblsAttrOptnDataObj = NFKTblsAttrOptnDefChangedDataObj['srcDbAllTblsDataObj'];

              dstDbNFKTblsAttrOptnDefChangedDataObj = NFKTblsAttrOptnDefChangedDataObj['dstDbTblsAttrOptnDefChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsAttrOptnDefChangedDataObj'] = dstDbNFKTblsAttrOptnDefChangedDataObj;
              if len(NFKTblsAttrOptnDefChangedDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbNFKTblsAttrOptnDataObj = NFKTblsAttrOptnDefChangedDataObj['dstDbAllTblsDataObj'];


           ### Section abt to get nfk tables with all new columns infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblNewColsOptns(inputArgsDataObj) == "Y" :

              newColsNFKTblDataObj = handleBidirProcsngToGetTblsNewColsInfoBtwnDB(
                 srcDbName, srcDbNFKTblsDataObj, dstDbName, dstDbNFKTblsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsNewColsDataObj'] = newColsNFKTblDataObj['srcDbTblsNewColsDataObj'];
              if len(newColsNFKTblDataObj['srcDbAllTblsDataObj']) > 0:    
                 srcDbNFKTblsDataObj = newColsNFKTblDataObj['srcDbAllTblsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsNewColsDataObj'] = newColsNFKTblDataObj['dstDbTblsNewColsDataObj'];
              if len(newColsNFKTblDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbNFKTblsDataObj = newColsNFKTblDataObj['dstDbAllTblsDataObj'];


           ### Section abt to get nfk table with all columns who definition has been changed infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblColDefOptns(inputArgsDataObj) == "Y" :

              existColsDefChangedNFKTblDataObj = handleBidirProcsngToGetTblsColsDefChangedInfoBtwnDB(
                   srcDbName, srcDbNFKTblsDataObj, dstDbName, dstDbNFKTblsDataObj, isMakeExactDbSchemasCopy
              );

              srcDbNFKTblsColsDefChangedDataObj = existColsDefChangedNFKTblDataObj['srcDbTblsColsDefChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsColsDefChangedDataObj'] = srcDbNFKTblsColsDefChangedDataObj;
              if len(existColsDefChangedNFKTblDataObj['srcDbAllTblsDataObj']) > 0:
                 srcDbNFKTblsDataObj = existColsDefChangedNFKTblDataObj['srcDbAllTblsDataObj'];

              dstDbNFKTblsColsDefChangedDataObj = existColsDefChangedNFKTblDataObj['dstDbTblsColsDefChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsColsDefChangedDataObj'] = dstDbNFKTblsColsDefChangedDataObj;
              if len(existColsDefChangedNFKTblDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbNFKTblsDataObj = existColsDefChangedNFKTblDataObj['dstDbAllTblsDataObj'];


           ### Section abt to get nfk table with all columns whose dataType has been changed infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblColDTypeOptns(inputArgsDataObj) == "Y" : 

              existColsDataTypeChangedNFKTblDataObj = handleBidirProcsngToGetTblsColsDataTypeChangedInfoBtwnDB(
                   srcDbName, srcDbNFKTblsDataObj, dstDbName, dstDbNFKTblsDataObj, isMakeExactDbSchemasCopy
              );

              srcDbNFKTblsColsDataTypeChangedDataObj = existColsDataTypeChangedNFKTblDataObj['srcDbTblsColsDataTypeChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsColsDataTypeChangedDataObj'] = srcDbNFKTblsColsDataTypeChangedDataObj;
              if len(existColsDataTypeChangedNFKTblDataObj['srcDbAllTblsDataObj']) > 0:             
                 srcDbNFKTblsDataObj = existColsDataTypeChangedNFKTblDataObj['srcDbAllTblsDataObj'];

              dstDbNFKTblsColsDataTypeChangedDataObj = existColsDataTypeChangedNFKTblDataObj['dstDbTblsColsDataTypeChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsColsDataTypeChangedDataObj'] = dstDbNFKTblsColsDataTypeChangedDataObj;
              if len(existColsDataTypeChangedNFKTblDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbNFKTblsDataObj = existColsDataTypeChangedNFKTblDataObj['dstDbAllTblsDataObj'];

            

           ### Section abt to get all new nfk tables with all indexes infoSchemas data ###
           
           if isExecuteSchmsCmpOnExistTblNewIndexesOptns(inputArgsDataObj) == "Y" : 

              NewNFKTblIndexNameDataObj = handleBidirProcsngToGetNewTblsAllIndexesInfoBtwnDB(
                 srcDbName, srcDbNFKTblsIndexesDataObj, dstDbName, dstDbNFKTblsIndexesDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewNFKTblsAllIndxNameDataObj'] = NewNFKTblIndexNameDataObj['srcDbTblsNewIndxNameDataObj'];
              if len(NewNFKTblIndexNameDataObj['srcDbAllIndexDataObj'])>0: 
                 srcDbNFKTblsIndexesDataObj = NewNFKTblIndexNameDataObj['srcDbAllIndexDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewNFKTblsAllIndxNameDataObj'] = NewNFKTblIndexNameDataObj['dstDbTblsNewIndxNameDataObj'];
              if len(NewNFKTblIndexNameDataObj['dstDbAllIndexDataObj'])>0: 
                 dstDbNFKTblsIndexesDataObj = NewNFKTblIndexNameDataObj['dstDbAllIndexDataObj'];


           ### Section abt to get nfk table with all new indexes infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblNewIndexesOptns(inputArgsDataObj) == "Y" :

              newIndxNameOnNFKTblsDataObj = handleBidirProcsngToGetTblsNewIndexesInfoBtwnDB(
                 srcDbName, srcDbNFKTblsIndexesDataObj, dstDbName, dstDbNFKTblsIndexesDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsNewIndxNameDataObj'] = newIndxNameOnNFKTblsDataObj['srcDbTblsNewIndxNameDataObj'];
              if len(newIndxNameOnNFKTblsDataObj['srcDbAllIndexDataObj']) > 0: 
                 srcDbNFKTblsIndexesDataObj = newIndxNameOnNFKTblsDataObj['srcDbAllIndexDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsNewIndxNameDataObj'] = newIndxNameOnNFKTblsDataObj['dstDbTblsNewIndxNameDataObj'];
              if len(newIndxNameOnNFKTblsDataObj['dstDbAllIndexDataObj']) > 0: 
                 dstDbNFKTblsIndexesDataObj = newIndxNameOnNFKTblsDataObj['dstDbAllIndexDataObj'];


           ### Section abt to get nfk table index with all new columns infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblIndexesDefOptns(inputArgsDataObj) == "Y" :

              existIndxNewColsOnNFKTblsDataObj = handleBidirProcsngToGetTblsIndexNewColsInfoBtwnDB(
                   srcDbName, srcDbNFKTblsIndexesDataObj, dstDbName, dstDbNFKTblsIndexesDataObj, isMakeExactDbSchemasCopy
              );

              srcDbNFKTblIndxNewColsDataObj = existIndxNewColsOnNFKTblsDataObj['srcDbTblIndxNewColsDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbNFKTblIndxNewColsDataObj'] = srcDbNFKTblIndxNewColsDataObj;
              if len(existIndxNewColsOnNFKTblsDataObj['srcDbAllIndexDataObj']) > 0: 
                 srcDbNFKTblsIndexesDataObj = existIndxNewColsOnNFKTblsDataObj['srcDbAllIndexDataObj'];

              dstDbNFKTblIndxNewColsDataObj = existIndxNewColsOnNFKTblsDataObj['dstDbTblIndxNewColsDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbNFKTblIndxNewColsDataObj'] = dstDbNFKTblIndxNewColsDataObj;
              if len(existIndxNewColsOnNFKTblsDataObj['dstDbAllIndexDataObj']) > 0:
                 dstDbNFKTblsIndexesDataObj = existIndxNewColsOnNFKTblsDataObj['dstDbAllIndexDataObj'];
               

           ### Section abt to get nfk table index all columns whose definition has been changed infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblIndexesDefOptns(inputArgsDataObj) == "Y" :

              indxColsDefChangedNFKTblsDataObj = handleBidirProcsngToGetTblsIndexColsDefChangedInfoBtwnDB(
                  srcDbName, srcDbNFKTblsIndexesDataObj, dstDbName, dstDbNFKTblsIndexesDataObj, isMakeExactDbSchemasCopy
              );

              srcDbNFKTblIndxColsChangedDataObj = indxColsDefChangedNFKTblsDataObj['srcDbTblIndxColsChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbNFKTblIndxColsChangedDataObj'] = srcDbNFKTblIndxColsChangedDataObj;
              if len(indxColsDefChangedNFKTblsDataObj['srcDbAllIndexDataObj']) > 0:             
                 srcDbNFKTblsIndexesDataObj = indxColsDefChangedNFKTblsDataObj['srcDbAllIndexDataObj'];

              dstDbNFKTblIndxColsChangedDataObj = indxColsDefChangedNFKTblsDataObj['dstDbTblIndxColsChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbNFKTblIndxColsChangedDataObj'] = dstDbNFKTblIndxColsChangedDataObj;
              if len(indxColsDefChangedNFKTblsDataObj['dstDbAllIndexDataObj']) > 0:
                 dstDbNFKTblsIndexesDataObj = indxColsDefChangedNFKTblsDataObj['dstDbAllIndexDataObj'];


           ### Section abt to get new FKAsNFK tables infoSchemas data ###

           if isExecuteSchmsCmpOnNewTblsOptns(inputArgsDataObj) == "Y" :

              NewFKAsNFKTblsDataObj = handleBidirProcsngToGetNewTblsInfoBtwnDB(
                 srcDbName, srcDbFKAsNFKTblsDataObj, dstDbName, dstDbFKAsNFKTblsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewFKAsNFKTblsDataObj'] = NewFKAsNFKTblsDataObj['srcDbNewTblsDataObj'];
              if len(NewFKAsNFKTblsDataObj['srcDbAllTblsDataObj']) > 0:
                 srcDbFKAsNFKTblsDataObj = NewFKAsNFKTblsDataObj['srcDbAllTblsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewFKAsNFKTblsDataObj'] = NewFKAsNFKTblsDataObj['dstDbNewTblsDataObj'];
              if len(NewFKAsNFKTblsDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbFKAsNFKTblsDataObj = NewFKAsNFKTblsDataObj['dstDbAllTblsDataObj'];


           ### Section abt to get all new fk as nfk tables with attributes option infoSchemas data ###

           if isExecuteSchmsCmpOnNewTblsAttrOptns(inputArgsDataObj) == "Y" :

              newFKAsNFKTblsAttrOptnDataObj = handleBidirProcsngToGetNewTblsAttrOptnInfoBtwnDB(
                 srcDbName, srcDbFKAsNFKTblsAttrOptnDataObj, dstDbName, dstDbFKAsNFKTblsAttrOptnDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewFKAsNFKTblsAttrOptnDataObj'] = newFKAsNFKTblsAttrOptnDataObj['srcDbNewTblsDataObj'];
              if len(newFKAsNFKTblsAttrOptnDataObj['srcDbAllTblsDataObj']) > 0:
                 srcDbFKAsNFKTblsAttrOptnDataObj = newFKAsNFKTblsAttrOptnDataObj['srcDbAllTblsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewFKAsNFKTblsAttrOptnDataObj'] = newFKAsNFKTblsAttrOptnDataObj['dstDbNewTblsDataObj'];
              if len(newFKAsNFKTblsAttrOptnDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbFKAsNFKTblsAttrOptnDataObj = newFKAsNFKTblsAttrOptnDataObj['dstDbAllTblsDataObj'];
 
         
           ### Section abt to get fk as nfk tables with all attributes options who definition has been changed infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblsAttrOptns(inputArgsDataObj) == "Y" :

              FKAsNFKTblsAttrOptnDefChangedDataObj = handleBidirProcsngToGetTblsAttrOptnDefChangedInfoBtwnDB(
                  srcDbName, srcDbFKAsNFKTblsAttrOptnDataObj, dstDbName, dstDbFKAsNFKTblsAttrOptnDataObj, isMakeExactDbSchemasCopy
              );

              srcDbFKAsNFKTblsAttrOptnDefChangedDataObj = FKAsNFKTblsAttrOptnDefChangedDataObj['srcDbTblsAttrOptnDefChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsAttrOptnDefChangedDataObj'] = srcDbFKAsNFKTblsAttrOptnDefChangedDataObj;
              if len(FKAsNFKTblsAttrOptnDefChangedDataObj['srcDbAllTblsDataObj']) > 0:
                 srcDbNFKTblsAttrOptnDataObj = FKAsNFKTblsAttrOptnDefChangedDataObj['srcDbAllTblsDataObj'];

              dstDbFKAsNFKTblsAttrOptnDefChangedDataObj = FKAsNFKTblsAttrOptnDefChangedDataObj['dstDbTblsAttrOptnDefChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsAttrOptnDefChangedDataObj'] = dstDbFKAsNFKTblsAttrOptnDefChangedDataObj;
              if len(FKAsNFKTblsAttrOptnDefChangedDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbNFKTblsAttrOptnDataObj = FKAsNFKTblsAttrOptnDefChangedDataObj['dstDbAllTblsDataObj'];


           ### Section abt to get FKAsNFK tables with all new columns infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblNewColsOptns(inputArgsDataObj) == "Y" :
 
              newColsFKAsNFKTblDataObj = handleBidirProcsngToGetTblsNewColsInfoBtwnDB(
                 srcDbName, srcDbFKAsNFKTblsDataObj, dstDbName, dstDbFKAsNFKTblsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsNewColsDataObj'] = newColsFKAsNFKTblDataObj['srcDbTblsNewColsDataObj'];
              if len(newColsFKAsNFKTblDataObj['srcDbAllTblsDataObj']) > 0:    
                 srcDbFKAsNFKTblsDataObj = newColsFKAsNFKTblDataObj['srcDbAllTblsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsNewColsDataObj'] = newColsFKAsNFKTblDataObj['dstDbTblsNewColsDataObj'];
              if len(newColsFKAsNFKTblDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbFKAsNFKTblsDataObj = newColsFKAsNFKTblDataObj['dstDbAllTblsDataObj'];


           ### Section abt to get FKAsNFK table all columns whose definition has been changed infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblColDefOptns(inputArgsDataObj) == "Y" :
 
              existColsDefChangedFKAsNFKTblDataObj = handleBidirProcsngToGetTblsColsDefChangedInfoBtwnDB(
                   srcDbName, srcDbFKAsNFKTblsDataObj, dstDbName, dstDbFKAsNFKTblsDataObj, isMakeExactDbSchemasCopy
              );

              srcDbFKAsNFKTblsColsDefChangedDataObj = existColsDefChangedFKAsNFKTblDataObj['srcDbTblsColsDefChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsColsDefChangedDataObj'] = srcDbFKAsNFKTblsColsDefChangedDataObj;
              if len(existColsDefChangedFKAsNFKTblDataObj['srcDbAllTblsDataObj']) > 0:
                 srcDbFKAsNFKTblsDataObj = existColsDefChangedFKAsNFKTblDataObj['srcDbAllTblsDataObj'];

              dstDbFKAsNFKTblsColsDefChangedDataObj = existColsDefChangedFKAsNFKTblDataObj['dstDbTblsColsDefChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsColsDefChangedDataObj'] = dstDbFKAsNFKTblsColsDefChangedDataObj;
              if len(existColsDefChangedFKAsNFKTblDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbFKAsNFKTblsDataObj = existColsDefChangedFKAsNFKTblDataObj['dstDbAllTblsDataObj'];


           ### Section abt to get FKAsNFK table all columns whose dataType has been changed infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblColDTypeOptns(inputArgsDataObj) == "Y" :

              colsDataTypeChangedFKAsNFKTblsDataObj = handleBidirProcsngToGetTblsColsDataTypeChangedInfoBtwnDB(
                  srcDbName, srcDbFKAsNFKTblsDataObj, dstDbName, dstDbFKAsNFKTblsDataObj, isMakeExactDbSchemasCopy
              );

              srcDbFKAsNFKTblsColsDataTypeChangedDataObj = colsDataTypeChangedFKAsNFKTblsDataObj['srcDbTblsColsDataTypeChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsColsDataTypeChangedDataObj'] = srcDbFKAsNFKTblsColsDataTypeChangedDataObj;
              if len(colsDataTypeChangedFKAsNFKTblsDataObj['srcDbAllTblsDataObj']) > 0:             
                 srcDbFKAsNFKTblsDataObj = colsDataTypeChangedFKAsNFKTblsDataObj['srcDbAllTblsDataObj'];

              dstDbFKAsNFKTblsColsDataTypeChangedDataObj = colsDataTypeChangedFKAsNFKTblsDataObj['dstDbTblsColsDataTypeChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsColsDataTypeChangedDataObj'] = dstDbFKAsNFKTblsColsDataTypeChangedDataObj;
              if len(colsDataTypeChangedFKAsNFKTblsDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbFKAsNFKTblsDataObj = colsDataTypeChangedFKAsNFKTblsDataObj['dstDbAllTblsDataObj'];


           ### Section about to get all nfk as fk new tables all new indexes infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblNewIndexesOptns(inputArgsDataObj) == "Y" :

              NewFKAsNFKTblIndexNameDataObj = handleBidirProcsngToGetNewTblsAllIndexesInfoBtwnDB(
                 srcDbName, srcDbFKAsNFKTblsIndexesDataObj, dstDbName, dstDbFKAsNFKTblsIndexesDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewFKAsNFKTblsAllIndxNameDataObj'] = NewFKAsNFKTblIndexNameDataObj['srcDbTblsNewIndxNameDataObj'];
              if len(NewFKAsNFKTblIndexNameDataObj['srcDbAllIndexDataObj'])>0: 
                 srcDbFKAsNFKTblsIndexesDataObj = NewFKAsNFKTblIndexNameDataObj['srcDbAllIndexDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewFKAsNFKTblsAllIndxNameDataObj'] = NewFKAsNFKTblIndexNameDataObj['dstDbTblsNewIndxNameDataObj'];
              if len(NewFKAsNFKTblIndexNameDataObj['dstDbAllIndexDataObj'])>0: 
                 dstDbFKAsNFKTblsIndexesDataObj = NewFKAsNFKTblIndexNameDataObj['dstDbAllIndexDataObj'];

           
           ### Section about to get nfk as fk table all new indexes infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblNewIndexesOptns(inputArgsDataObj) == "Y" :
 
              newIndxNameOnFKAsNFKTblsDataObj = handleBidirProcsngToGetTblsNewIndexesInfoBtwnDB(
                 srcDbName, srcDbFKAsNFKTblsIndexesDataObj, dstDbName, dstDbFKAsNFKTblsIndexesDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsNewIndxNameDataObj'] = newIndxNameOnFKAsNFKTblsDataObj['srcDbTblsNewIndxNameDataObj'];
              if len(newIndxNameOnFKAsNFKTblsDataObj['srcDbAllIndexDataObj']) > 0: 
                 srcDbFKAsNFKTblsIndexesDataObj = newIndxNameOnFKAsNFKTblsDataObj['srcDbAllIndexDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsNewIndxNameDataObj'] = newIndxNameOnFKAsNFKTblsDataObj['dstDbTblsNewIndxNameDataObj'];
              if len(newIndxNameOnFKAsNFKTblsDataObj['dstDbAllIndexDataObj']) > 0: 
                 dstDbFKAsNFKTblsIndexesDataObj = newIndxNameOnFKAsNFKTblsDataObj['dstDbAllIndexDataObj'];


           ### Section about to get nfk as fk table index all new columns infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblIndexesDefOptns(inputArgsDataObj) == "Y" :

              existIndxNewColsOnFKAsNFKTblsDataObj = handleBidirProcsngToGetTblsIndexNewColsInfoBtwnDB(
                   srcDbName, srcDbFKAsNFKTblsIndexesDataObj, dstDbName, dstDbFKAsNFKTblsIndexesDataObj, isMakeExactDbSchemasCopy
              );

              srcDbFKAsNFKTblIndxNewColsDataObj = existIndxNewColsOnFKAsNFKTblsDataObj['srcDbTblIndxNewColsDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblIndxNewColsDataObj'] = srcDbFKAsNFKTblIndxNewColsDataObj;
              if len(existIndxNewColsOnFKAsNFKTblsDataObj['srcDbAllIndexDataObj']) > 0: 
                 srcDbFKAsNFKTblsIndexesDataObj = existIndxNewColsOnFKAsNFKTblsDataObj['srcDbAllIndexDataObj'];

              dstDbFKAsNFKTblIndxNewColsDataObj = existIndxNewColsOnFKAsNFKTblsDataObj['dstDbTblIndxNewColsDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblIndxNewColsDataObj'] = dstDbFKAsNFKTblIndxNewColsDataObj;
              if len(existIndxNewColsOnFKAsNFKTblsDataObj['dstDbAllIndexDataObj']) > 0:
                 dstDbFKAsNFKTblsIndexesDataObj = existIndxNewColsOnFKAsNFKTblsDataObj['dstDbAllIndexDataObj'];


           ### Section about to get nfk as fk table index all columns whose definition has been changed ###

           if isExecuteSchmsCmpOnExistTblIndexesDefOptns(inputArgsDataObj) == "Y" :

              indxColsDefChangedFKAsNFKTblsDataObj = handleBidirProcsngToGetTblsIndexColsDefChangedInfoBtwnDB(
                  srcDbName, srcDbFKAsNFKTblsIndexesDataObj, dstDbName, dstDbFKAsNFKTblsIndexesDataObj, isMakeExactDbSchemasCopy
              );

              srcDbFKAsNFKTblIndxColsChangedDataObj = indxColsDefChangedFKAsNFKTblsDataObj['srcDbTblIndxColsChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblIndxColsChangedDataObj'] = srcDbFKAsNFKTblIndxColsChangedDataObj;
              if len(indxColsDefChangedFKAsNFKTblsDataObj['srcDbAllIndexDataObj']) > 0:             
                 srcDbNFKTblsIndexesDataObj = indxColsDefChangedFKAsNFKTblsDataObj['srcDbAllIndexDataObj'];

              dstDbFKAsNFKTblIndxColsChangedDataObj = indxColsDefChangedFKAsNFKTblsDataObj['dstDbTblIndxColsChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblIndxColsChangedDataObj'] = dstDbFKAsNFKTblIndxColsChangedDataObj;
              if len(indxColsDefChangedFKAsNFKTblsDataObj['dstDbAllIndexDataObj']) > 0:
                 dstDbNFKTblsIndexesDataObj = indxColsDefChangedFKAsNFKTblsDataObj['dstDbAllIndexDataObj'];


           ### Section abt to get all new FKAsNFK table with all fkName infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblNewFKOptns(inputArgsDataObj) == "Y" :
 
              NewFKAsNFKTblFkNameColConstraintsDataObj = handleBidirProcsngToGetNewTblsFkNameColConstraintsInfoBtwnDB(
                 srcDbName, srcDbFKAsNFKTblsConstraintsDataObj, dstDbName, dstDbFKAsNFKTblsConstraintsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewFKAsNFKTblsFKNameColConstraintsDataObj'] = NewFKAsNFKTblFkNameColConstraintsDataObj['srcDbNewTblsFkNameColConstraintsDataObj'];
              if len(NewFKAsNFKTblFkNameColConstraintsDataObj['srcDbAllConstraintsDataObj'])>0: 
                 srcDbFKAsNFKTblsConstraintsDataObj = NewFKAsNFKTblFkNameColConstraintsDataObj['srcDbAllConstraintsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewFKAsNFKTblsFKNameColConstraintsDataObj'] = NewFKAsNFKTblFkNameColConstraintsDataObj['dstDbNewTblsFkNameColConstraintsDataObj'];
              if len(NewFKAsNFKTblFkNameColConstraintsDataObj['dstDbAllConstraintsDataObj'])>0: 
                 dstDbFKAsNFKTblsConstraintsDataObj = NewFKAsNFKTblFkNameColConstraintsDataObj['dstDbAllConstraintsDataObj'];


           ### Section abt to get FKAsNFK table with all new fkName infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblNewFKOptns(inputArgsDataObj) == "Y" :
 
              existFKAsNFKTblsNewFkNameColConstraintsDataObj = handleBidirProcsngToGetTblsNewFKNameColConstraintsBtwnSrcAndDstDB(
                   srcDbName, srcDbFKAsNFKTblsConstraintsDataObj, dstDbName, dstDbFKAsNFKTblsConstraintsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsNewFKNameColConstraintsDataObj'] = existFKAsNFKTblsNewFkNameColConstraintsDataObj['srcDbExistTblsNewFkNameColConstraintsDataObj'];
              if len(existFKAsNFKTblsNewFkNameColConstraintsDataObj['srcDbAllConstraintsDataObj']) > 0: 
                 srcDbFKAsNFKTblsConstraintsDataObj = existFKAsNFKTblsNewFkNameColConstraintsDataObj['srcDbAllConstraintsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsNewFKNameColConstraintsDataObj'] = existFKAsNFKTblsNewFkNameColConstraintsDataObj['dstDbExistTblsNewFkNameColConstraintsDataObj'];
              if len(existFKAsNFKTblsNewFkNameColConstraintsDataObj['dstDbAllConstraintsDataObj']) > 0: 
                 dstDbFKAsNFKTblsConstraintsDataObj = existFKAsNFKTblsNewFkNameColConstraintsDataObj['dstDbAllConstraintsDataObj'];



           ### Section abt to get FKAsNFK table fkName with all new cols infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblFKDefOptns(inputArgsDataObj) == "Y" :

              existFKAsNFKTblsExistFkNameNewColConstraintsDataObj = handleBidirProcsngToGetTblsFKNameNewColConstraintsInfoBtwnDB(
                   srcDbName, srcDbFKAsNFKTblsConstraintsDataObj, dstDbName, dstDbFKAsNFKTblsConstraintsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsFKNameNewColsConstraintsDataObj'] = existFKAsNFKTblsExistFkNameNewColConstraintsDataObj['srcDbFKTblsFKNameNewColsConstraintsDataObj'];
              if len(existFKAsNFKTblsExistFkNameNewColConstraintsDataObj['srcDbAllConstraintsDataObj']) > 0: 
                 srcDbFKAsNFKTblsConstraintsDataObj = existFKAsNFKTblsExistFkNameNewColConstraintsDataObj['srcDbAllConstraintsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsFKNameNewColsConstraintsDataObj'] = existFKAsNFKTblsExistFkNameNewColConstraintsDataObj['dstDbFKTblsFKNameNewColsConstraintsDataObj'];
              if len(existFKAsNFKTblsExistFkNameNewColConstraintsDataObj['dstDbAllConstraintsDataObj']) > 0: 
                 dstDbFKAsNFKTblsConstraintsDataObj = existFKAsNFKTblsExistFkNameNewColConstraintsDataObj['dstDbAllConstraintsDataObj'];


           ### Section abt to get FKAsNFK tables fkName all colums whose definition has been changed infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblFKDefOptns(inputArgsDataObj) == "Y" :

              fKAsNFKTblsFkNameColConstraintsDefChangedDataObj = handleBidirProcsngToGetTblsFkColNameConstraintsDefChangedInfoBtwnDB(
                  srcDbName, srcDbFKAsNFKTblsConstraintsDataObj, dstDbName, dstDbFKAsNFKTblsConstraintsDataObj, isMakeExactDbSchemasCopy
              );

              srcDbFKAsNFKTblColConstrntDefChangedDataObj = fKAsNFKTblsFkNameColConstraintsDefChangedDataObj['srcDbTblsFKNameColConstraintsDefDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsFKNameColConstraintsDefDataObj'] = srcDbFKAsNFKTblColConstrntDefChangedDataObj;
              if len(fKAsNFKTblsFkNameColConstraintsDefChangedDataObj['srcDbAllConstraintsDataObj']) > 0:             
                 srcDbFKAsNFKTblsConstraintsDataObj = fKAsNFKTblsFkNameColConstraintsDefChangedDataObj['srcDbAllConstraintsDataObj'];

              dstDbFKAsNFKTblColConstrntDefChangedDataObj = fKAsNFKTblsFkNameColConstraintsDefChangedDataObj['dstDbTblsFKNameColConstraintsDefDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsFKNameColConstraintsDefDataObj'] = dstDbFKAsNFKTblColConstrntDefChangedDataObj;
              if len(fKAsNFKTblsFkNameColConstraintsDefChangedDataObj['dstDbAllConstraintsDataObj']) > 0:
                 dstDbFKAsNFKTblsConstraintsDataObj = fKAsNFKTblsFkNameColConstraintsDefChangedDataObj['dstDbAllConstraintsDataObj'];



           ### Section abt to get new fk tables schemas data ###

           if isExecuteSchmsCmpOnNewTblsOptns(inputArgsDataObj) == "Y" :

              newFKTblsDataObj = handleBidirProcsngToGetNewTblsInfoBtwnDB(
                 srcDbName, srcDbFKTblsDataObj, dstDbName, dstDbFKTblsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewFKTblsDataObj'] = newFKTblsDataObj['srcDbNewTblsDataObj'];
              if len(newFKTblsDataObj['srcDbAllTblsDataObj']) > 0:
                 srcDbFKTblsDataObj = newFKTblsDataObj['srcDbAllTblsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewFKTblsDataObj'] = newFKTblsDataObj['dstDbNewTblsDataObj'];
              if len(newFKTblsDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbFKTblsDataObj = newFKTblsDataObj['dstDbAllTblsDataObj'];

           
          
           ### Section abt to get all fk tables with attributes option infoSchemas data ###

           if isExecuteSchmsCmpOnNewTblsAttrOptns(inputArgsDataObj) == "Y" :
 
              newFKTblsAttrOptnDataObj = handleBidirProcsngToGetNewTblsAttrOptnInfoBtwnDB(
                 srcDbName, srcDbFKTblsAttrOptnDataObj, dstDbName, dstDbFKTblsAttrOptnDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewFKTblsAttrOptnDataObj'] = newFKTblsAttrOptnDataObj['srcDbNewTblsDataObj'];
              if len(newFKTblsAttrOptnDataObj['srcDbAllTblsDataObj']) > 0:
                 srcDbFKTblsAttrOptnDataObj = newFKTblsAttrOptnDataObj['srcDbAllTblsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewFKTblsAttrOptnDataObj'] = newFKTblsAttrOptnDataObj['dstDbNewTblsDataObj'];
              if len(newFKTblsAttrOptnDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbFKTblsAttrOptnDataObj = newFKTblsAttrOptnDataObj['dstDbAllTblsDataObj'];


           ### Section abt to get fk tables with all attributes options who definition has been changed infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblsAttrOptns(inputArgsDataObj) == "Y" :

              FKTblsAttrOptnDefChangedDataObj = handleBidirProcsngToGetTblsAttrOptnDefChangedInfoBtwnDB(
                    srcDbName, srcDbFKTblsAttrOptnDataObj, dstDbName, dstDbFKTblsAttrOptnDataObj, isMakeExactDbSchemasCopy
              );

              srcDbFKTblsAttrOptnDefChangedDataObj = FKTblsAttrOptnDefChangedDataObj['srcDbTblsAttrOptnDefChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbFKTblsAttrOptnDefChangedDataObj'] = srcDbFKTblsAttrOptnDefChangedDataObj;
              if len(FKTblsAttrOptnDefChangedDataObj['srcDbAllTblsDataObj']) > 0:
                 srcDbFKTblsAttrOptnDataObj = FKTblsAttrOptnDefChangedDataObj['srcDbAllTblsDataObj'];

              dstDbFKTblsAttrOptnDefChangedDataObj = FKTblsAttrOptnDefChangedDataObj['dstDbTblsAttrOptnDefChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbFKTblsAttrOptnDefChangedDataObj'] = dstDbFKTblsAttrOptnDefChangedDataObj;
              if len(FKTblsAttrOptnDefChangedDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbFKTblsAttrOptnDataObj = FKTblsAttrOptnDefChangedDataObj['dstDbAllTblsDataObj'];


           ### Section abt to get fk tables with all new columns infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblNewColsOptns(inputArgsDataObj) == "Y" :

              newColsFkTblDataObj = handleBidirProcsngToGetTblsNewColsInfoBtwnDB(
                 srcDbName, srcDbFKTblsDataObj, dstDbName, dstDbFKTblsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbFKTblsNewColsDataObj'] = newColsFkTblDataObj['srcDbTblsNewColsDataObj'];
              if len(newColsFkTblDataObj['srcDbAllTblsDataObj']) > 0:    
                 srcDbFKTblsDataObj = newColsFkTblDataObj['srcDbAllTblsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbFKTblsNewColsDataObj'] = newColsFkTblDataObj['dstDbTblsNewColsDataObj'];
              if len(newColsFkTblDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbFKTblsDataObj = newColsFkTblDataObj['dstDbAllTblsDataObj'];


           ### Section abt to get fk table all columns whose definition has been changed infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblColDefOptns(inputArgsDataObj) == "Y" :
 
              existColsDefChangedFkTblDataObj = handleBidirProcsngToGetTblsColsDefChangedInfoBtwnDB(
                   srcDbName, srcDbFKTblsDataObj, dstDbName, dstDbFKTblsDataObj, isMakeExactDbSchemasCopy
              );

              srcDbFKTblsColsDefChangedDataObj = existColsDefChangedFkTblDataObj['srcDbTblsColsDefChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbFKTblsColsDefChangedDataObj'] = srcDbFKTblsColsDefChangedDataObj;
              if len(existColsDefChangedFkTblDataObj['srcDbAllTblsDataObj']) > 0:
                 srcDbFKTblsDataObj = existColsDefChangedFkTblDataObj['srcDbAllTblsDataObj'];

              dstDbFKTblsColsDefChangedDataObj = existColsDefChangedFkTblDataObj['dstDbTblsColsDefChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbFKTblsColsDefChangedDataObj'] = dstDbFKTblsColsDefChangedDataObj;
              if len(existColsDefChangedFkTblDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbFKTblsDataObj = existColsDefChangedFkTblDataObj['dstDbAllTblsDataObj'];


           ### Section abt to get fk table all columns whose data type has been changed infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblColDTypeOptns(inputArgsDataObj) == "Y" :

              existColsDataTypeChangedFkTblDataObj = handleBidirProcsngToGetTblsColsDataTypeChangedInfoBtwnDB(
                   srcDbName, srcDbFKTblsDataObj, dstDbName, dstDbFKTblsDataObj, isMakeExactDbSchemasCopy
              );

              srcDbFKTblsColsDataTypeChangedDataObj = existColsDataTypeChangedFkTblDataObj['srcDbTblsColsDataTypeChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbFKTblsColsDataTypeChangedDataObj'] = srcDbFKTblsColsDataTypeChangedDataObj; 
              if len(existColsDataTypeChangedFkTblDataObj['srcDbAllTblsDataObj']) > 0:             
                 srcDbFKTblsDataObj = existColsDataTypeChangedFkTblDataObj['srcDbAllTblsDataObj'];

              dstDbFKTblsColsDataTypeChangedDataObj = existColsDataTypeChangedFkTblDataObj['dstDbTblsColsDataTypeChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbFKTblsColsDataTypeChangedDataObj'] = dstDbFKTblsColsDataTypeChangedDataObj;
              if len(existColsDataTypeChangedFkTblDataObj['dstDbAllTblsDataObj']) > 0:
                 dstDbFKTblsDataObj = existColsDataTypeChangedFkTblDataObj['dstDbAllTblsDataObj'];


           ### Section abt to get all new fk table with all indexes infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblNewIndexesOptns(inputArgsDataObj) == "Y" :
 
              newFkTblIndxNameDataObj = handleBidirProcsngToGetNewTblsAllIndexesInfoBtwnDB(
                 srcDbName, srcDbFKTblsIndexesDataObj, dstDbName, dstDbFKTblsIndexesDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewFKTblsAllIndxNameDataObj'] = newFkTblIndxNameDataObj['srcDbTblsNewIndxNameDataObj'];
              if len(newFkTblIndxNameDataObj['srcDbAllIndexDataObj'])>0: 
                 srcDbFKTblsIndexesDataObj = newFkTblIndxNameDataObj['srcDbAllIndexDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewFKTblsAllIndxNameDataObj'] = newFkTblIndxNameDataObj['dstDbTblsNewIndxNameDataObj'];
              if len(newFkTblIndxNameDataObj['dstDbAllIndexDataObj'])>0: 
                 dstDbFKTblsIndexesDataObj = newFkTblIndxNameDataObj['dstDbAllIndexDataObj'];


           ### Section abt to get fk table all new indexes infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblNewIndexesOptns(inputArgsDataObj) == "Y" :

              newIndxNameONFKTblsDataObj = handleBidirProcsngToGetTblsNewIndexesInfoBtwnDB(
                 srcDbName, srcDbFKTblsIndexesDataObj, dstDbName, dstDbFKTblsIndexesDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbFKTblsNewIndxNameDataObj'] = newIndxNameONFKTblsDataObj['srcDbTblsNewIndxNameDataObj'];
              if len(newIndxNameONFKTblsDataObj['srcDbAllIndexDataObj']) > 0: 
                 srcDbFKTblsIndexesDataObj = newIndxNameONFKTblsDataObj['srcDbAllIndexDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbFKTblsNewIndxNameDataObj'] = newIndxNameONFKTblsDataObj['dstDbTblsNewIndxNameDataObj'];
              if len(newIndxNameONFKTblsDataObj['dstDbAllIndexDataObj']) > 0: 
                 dstDbFKTblsIndexesDataObj = newIndxNameONFKTblsDataObj['dstDbAllIndexDataObj'];


           ### Section abt to get fk table index all new columns infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblIndexesDefOptns(inputArgsDataObj) == "Y" :

              existIndxNewColsONFKTblsDataObj = handleBidirProcsngToGetTblsIndexNewColsInfoBtwnDB(
                   srcDbName, srcDbFKTblsIndexesDataObj, dstDbName, dstDbFKTblsIndexesDataObj, isMakeExactDbSchemasCopy
              );

              srcDbFkTblIndxNewColsDataObj = existIndxNewColsONFKTblsDataObj['srcDbTblIndxNewColsDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbFkTblIndxNewColsDataObj'] = srcDbFkTblIndxNewColsDataObj;
              if len(existIndxNewColsONFKTblsDataObj['srcDbAllIndexDataObj']) > 0: 
                 srcDbFKTblsIndexesDataObj = existIndxNewColsONFKTblsDataObj['srcDbAllIndexDataObj'];

              dstDbFkTblIndxNewColsDataObj = existIndxNewColsONFKTblsDataObj['dstDbTblIndxNewColsDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbFkTblIndxNewColsDataObj'] = dstDbFkTblIndxNewColsDataObj;
              if len(existIndxNewColsONFKTblsDataObj['dstDbAllIndexDataObj']) > 0: 
                 dstDbFKTblsIndexesDataObj = existIndxNewColsONFKTblsDataObj['dstDbAllIndexDataObj'];


           ### Section abt to get fk table index all columns whose definition hase been changed infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblIndexesDefOptns(inputArgsDataObj) == "Y" :
  
              indxColsDefChangedFKTblsDataObj = handleBidirProcsngToGetTblsIndexColsDefChangedInfoBtwnDB(
                  srcDbName, srcDbFKTblsIndexesDataObj, dstDbName, dstDbFKTblsIndexesDataObj, isMakeExactDbSchemasCopy
              );

              srcDbFkTblIndxColsChangedDataObj = indxColsDefChangedFKTblsDataObj['srcDbTblIndxColsChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbFkTblIndxColsChangedDataObj'] = srcDbFkTblIndxColsChangedDataObj;
              if len(indxColsDefChangedFKTblsDataObj['srcDbAllIndexDataObj']) > 0:             
                 srcDbFKTblsIndexesDataObj = indxColsDefChangedFKTblsDataObj['srcDbAllIndexDataObj'];

              dstDbFkTblIndxColsChangedDataObj = indxColsDefChangedFKTblsDataObj['dstDbTblIndxColsChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbFkTblIndxColsChangedDataObj'] = dstDbFkTblIndxColsChangedDataObj;
              if len(indxColsDefChangedFKTblsDataObj['dstDbAllIndexDataObj']) > 0:
                 dstDbFKTblsIndexesDataObj = indxColsDefChangedFKTblsDataObj['dstDbAllIndexDataObj'];


           ### Section abt to get all new fk table fkName infoSchemas data ###
        
           if isExecuteSchmsCmpOnExistTblNewFKOptns(inputArgsDataObj) == "Y" :
  
              NewFKTblFkNameColConstraintsDataObj = handleBidirProcsngToGetNewTblsFkNameColConstraintsInfoBtwnDB(
                 srcDbName, srcDbFKTblsConstraintsDataObj, dstDbName, dstDbFKTblsConstraintsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewFKTblsFKNameColConstraintsDataObj'] = NewFKTblFkNameColConstraintsDataObj['srcDbNewTblsFkNameColConstraintsDataObj'];
              if len(NewFKTblFkNameColConstraintsDataObj['srcDbAllConstraintsDataObj'])>0: 
                 srcDbFKTblsConstraintsDataObj = NewFKTblFkNameColConstraintsDataObj['srcDbAllConstraintsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewFKTblsFKNameColConstraintsDataObj'] = NewFKTblFkNameColConstraintsDataObj['dstDbNewTblsFkNameColConstraintsDataObj'];
              if len(NewFKTblFkNameColConstraintsDataObj['dstDbAllConstraintsDataObj'])>0: 
                 dstDbFKTblsConstraintsDataObj = NewFKTblFkNameColConstraintsDataObj['dstDbAllConstraintsDataObj'];



           ### Section abt to get fk table all new fkName infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblNewFKOptns(inputArgsDataObj) == "Y" :

              fKTblsNewFkNameColConstraintsDataObj = handleBidirProcsngToGetTblsNewFKNameColConstraintsBtwnSrcAndDstDB(
                srcDbName, srcDbFKTblsConstraintsDataObj, dstDbName, dstDbFKTblsConstraintsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbFKTblsNewFKNameColConstraintsDataObj'] = fKTblsNewFkNameColConstraintsDataObj['srcDbExistTblsNewFkNameColConstraintsDataObj'];
              if len(fKTblsNewFkNameColConstraintsDataObj['srcDbAllConstraintsDataObj']) > 0: 
                 srcDbFKTblsConstraintsDataObj = fKTblsNewFkNameColConstraintsDataObj['srcDbAllConstraintsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbFKTblsNewFKNameColConstraintsDataObj'] = fKTblsNewFkNameColConstraintsDataObj['dstDbExistTblsNewFkNameColConstraintsDataObj'];
              if len(fKTblsNewFkNameColConstraintsDataObj['dstDbAllConstraintsDataObj']) > 0: 
                 dstDbFKTblsConstraintsDataObj = fKTblsNewFkNameColConstraintsDataObj['dstDbAllConstraintsDataObj'];


           ### Section abt to get fk table fkName all new cols infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblFKDefOptns(inputArgsDataObj) == "Y" :

              fKTblsFkNameNewColConstraintsDataObj = handleBidirProcsngToGetTblsFKNameNewColConstraintsInfoBtwnDB(
                    srcDbName, srcDbFKTblsConstraintsDataObj, dstDbName, dstDbFKTblsConstraintsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbFKTblsFKNameNewColsConstraintsDataObj'] = fKTblsFkNameNewColConstraintsDataObj['srcDbFKTblsFKNameNewColsConstraintsDataObj'];
              if len(fKTblsFkNameNewColConstraintsDataObj['srcDbAllConstraintsDataObj']) > 0: 
                 srcDbFKTblsConstraintsDataObj = fKTblsFkNameNewColConstraintsDataObj['srcDbAllConstraintsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbFKTblsFKNameNewColsConstraintsDataObj'] = fKTblsFkNameNewColConstraintsDataObj['dstDbFKTblsFKNameNewColsConstraintsDataObj'];
              if len(fKTblsFkNameNewColConstraintsDataObj['dstDbAllConstraintsDataObj']) > 0: 
                 dstDbFKTblsConstraintsDataObj = fKTblsFkNameNewColConstraintsDataObj['dstDbAllConstraintsDataObj'];


           ### Section abt to get fk fkName all columns whose definition has been changed infoSchemas data ###

           if isExecuteSchmsCmpOnExistTblFKDefOptns(inputArgsDataObj) == "Y" :

              fKTblsfkNameExistColConstrntDefChangedDataObj = handleBidirProcsngToGetTblsFkColNameConstraintsDefChangedInfoBtwnDB(
                    srcDbName, srcDbFKTblsConstraintsDataObj, dstDbName, dstDbFKTblsConstraintsDataObj, isMakeExactDbSchemasCopy
              );

              srcDbFKTblsFKNameColConstraintsDefDataObj = fKTblsfkNameExistColConstrntDefChangedDataObj['srcDbTblsFKNameColConstraintsDefDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbFKTblsFKNameColConstraintsDefDataObj'] = srcDbFKTblsFKNameColConstraintsDefDataObj;
              if len(fKTblsfkNameExistColConstrntDefChangedDataObj['srcDbAllConstraintsDataObj']) > 0:             
                 srcDbFKTblsConstraintsDataObj = fKTblsfkNameExistColConstrntDefChangedDataObj['srcDbAllConstraintsDataObj'];


              dstDbFKTblsFKNameColConstraintsDefDataObj = fKTblsfkNameExistColConstrntDefChangedDataObj['dstDbTblsFKNameColConstraintsDefDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbFKTblsFKNameColConstraintsDefDataObj'] = dstDbFKTblsFKNameColConstraintsDefDataObj;
              if len(fKTblsfkNameExistColConstrntDefChangedDataObj['dstDbAllConstraintsDataObj']) > 0:
                 dstDbFKTblsConstraintsDataObj = fKTblsfkNameExistColConstrntDefChangedDataObj['dstDbAllConstraintsDataObj'];


           ### Section abt to get all new table with all triggers ###

           if isExecuteSchmsCmpOnExistTblNewTgrOptns(inputArgsDataObj) == "Y" :

              newTblsTgrNameOnTblsDataObj = handleBidirProcsngToGetNewTblsAllTriggersInfoBtwnDB(
                 srcDbName, srcDbTriggersDataObj, dstDbName, dstDbTriggersDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewTblsAllTgrNameDataObj'] = newTblsTgrNameOnTblsDataObj['srcDbTblsNewTgrNameDataObj'];
              if len(newTblsTgrNameOnTblsDataObj['srcDbTblsTgrDataObj']) > 0: 
                 srcDbTriggersDataObj = newTblsTgrNameOnTblsDataObj['srcDbTblsTgrDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewTblsAllTgrNameDataObj'] = newTblsTgrNameOnTblsDataObj['dstDbTblsNewTgrNameDataObj'];
              if len(newTblsTgrNameOnTblsDataObj['dstDbTblsTgrDataObj']) > 0: 
                 dstDbTriggersDataObj = newTblsTgrNameOnTblsDataObj['dstDbTblsTgrDataObj'];
 

           ### Section to get table all new trigger ###

           if isExecuteSchmsCmpOnExistTblNewTgrOptns(inputArgsDataObj) == "Y" :

              newTgrNameOnTblsDataObj = handleBidirProcsngTogetTblsNewTriggersInfoBtwnDB(
                 srcDbName, srcDbTriggersDataObj, dstDbName, dstDbTriggersDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbTblsNewTgrNameDataObj'] = newTgrNameOnTblsDataObj['srcDbTblsNewTgrNameDataObj'];
              if len(newTgrNameOnTblsDataObj['srcDbTblsTgrDataObj']) > 0: 
                 srcDbTriggersDataObj = newTgrNameOnTblsDataObj['srcDbTblsTgrDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbTblsNewTgrNameDataObj'] = newTgrNameOnTblsDataObj['dstDbTblsNewTgrNameDataObj'];
              if len(newTgrNameOnTblsDataObj['dstDbTblsTgrDataObj']) > 0: 
                 dstDbTriggersDataObj = newTgrNameOnTblsDataObj['dstDbTblsTgrDataObj'];


           ### Section abt to get table trigger whose definition hase been changed ###

           if isExecuteSchmsCmpOnExistTblTgrDefOptns(inputArgsDataObj) == "Y" :

              existTgrDefChangedOnTblsDataObj = handleBidirProcsngToGetTblsTriggerDefChangedInfoBtwnDB(
                   srcDbName, srcDbTriggersDataObj, dstDbName, dstDbTriggersDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbTblsTgrDefChangedDataObj'] = existTgrDefChangedOnTblsDataObj['srcDbTblsTgrDefChangedDataObj'];
              if len(existTgrDefChangedOnTblsDataObj['srcDbTblsTgrDataObj']) > 0: 
                 srcDbTriggersDataObj = existTgrDefChangedOnTblsDataObj['srcDbTblsTgrDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbTblsTgrDefChangedDataObj'] = existTgrDefChangedOnTblsDataObj['dstDbTblsTgrDefChangedDataObj'];
              if len(existTgrDefChangedOnTblsDataObj['dstDbTblsTgrDataObj']) > 0: 
                 dstDbTriggersDataObj = existTgrDefChangedOnTblsDataObj['dstDbTblsTgrDataObj'];

          
           ### Section abt to get all new routines types ###

           if isExecuteSchmsCmpOnExistDbNewRoutineOptns(inputArgsDataObj) == "Y" :
 
              newRoutinesTypeOnDbsDataObj = handleBidirProcsngToGetNewRoutinesTypeInfoBtwnDB(
                 srcDbName, srcDbRoutinesDataObj, dstDbName, dstDbRoutinesDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewRoutinesTypeDataObj'] = newRoutinesTypeOnDbsDataObj['srcDbNewRoutinesTypeDataObj'];
              if len(newRoutinesTypeOnDbsDataObj['srcDbRoutinesDataObj']) > 0: 
                 srcDbRoutinesDataObj = newRoutinesTypeOnDbsDataObj['srcDbRoutinesDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewRoutinesTypeDataObj'] = newRoutinesTypeOnDbsDataObj['dstDbNewRoutinesTypeDataObj'];
              if len(newRoutinesTypeOnDbsDataObj['dstDbRoutinesDataObj']) > 0: 
                 dstDbRoutinesDataObj = newRoutinesTypeOnDbsDataObj['dstDbRoutinesDataObj'];


           ### Section abt to get routine type all new routines ###

           if isExecuteSchmsCmpOnExistDbNewRoutineOptns(inputArgsDataObj) == "Y" :

              newRoutinesNameOnDbsDataObj = handleBidirProcsngToGetRTypeNewRoutinesNameInfoBtwnDB(
                 srcDbName, srcDbRoutinesDataObj, dstDbName, dstDbRoutinesDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewRoutinesNameDataObj'] = newRoutinesNameOnDbsDataObj['srcDbNewRoutinesNameDataObj'];
              if len(newRoutinesNameOnDbsDataObj['srcDbRoutinesDataObj']) > 0: 
                 srcDbRoutinesDataObj = newRoutinesNameOnDbsDataObj['srcDbRoutinesDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewRoutinesNameDataObj'] = newRoutinesNameOnDbsDataObj['dstDbNewRoutinesNameDataObj'];
              if len(newRoutinesNameOnDbsDataObj['dstDbRoutinesDataObj']) > 0: 
                 dstDbRoutinesDataObj = newRoutinesNameOnDbsDataObj['dstDbRoutinesDataObj'];


           ### Section abt to get routine type all routines whose definition has been changed ###

           if isExecuteSchmsCmpOnExistDbRoutineDefOptns(inputArgsDataObj) == "Y" :

              existRoutinesNameDefChangedOnDbsDataObj = handleBidirProcsngToGetRTypeRNameDefChangedInfoBtwnDB(
                   srcDbName, srcDbRoutinesDataObj, dstDbName, dstDbRoutinesDataObj, isMakeExactDbSchemasCopy
              );

              srcDbRoutinesNameDefChangedDataObj = existRoutinesNameDefChangedOnDbsDataObj['srcDbRoutinesNameDefChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbRoutinesNameDefChangedDataObj'] = srcDbRoutinesNameDefChangedDataObj;
              if len(existRoutinesNameDefChangedOnDbsDataObj['srcDbRoutinesDataObj']) > 0: 
                 srcDbRoutinesDataObj = existRoutinesNameDefChangedOnDbsDataObj['srcDbRoutinesDataObj'];

              dstDbRoutinesNameDefChangedDataObj = existRoutinesNameDefChangedOnDbsDataObj['dstDbRoutinesNameDefChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbRoutinesNameDefChangedDataObj'] = dstDbRoutinesNameDefChangedDataObj; 
              if len(existRoutinesNameDefChangedOnDbsDataObj['dstDbRoutinesDataObj']) > 0: 
                 dstDbRoutinesDataObj = existRoutinesNameDefChangedOnDbsDataObj['dstDbRoutinesDataObj'];


           ### Section abt to get all independent new views schemas data ###

           if isExecuteSchmsCmpOnExistDbNewViewsOptns(inputArgsDataObj) == "Y" :

              newIndependentViewsOnDbsDataObj = handleBidirProcsngToGetNewViewsInfoBtwnDB(
                 srcDbName, srcDbIndependentViewsDataObj, dstDbName, dstDbIndependentViewsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewIndependentViewsDataObj'] = newIndependentViewsOnDbsDataObj['srcDbNewViewsDataObj'];
              if len(newIndependentViewsOnDbsDataObj['srcDbViewsDataObj']) > 0: 
                 srcDbIndependentViewsDataObj = newIndependentViewsOnDbsDataObj['srcDbViewsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewIndependentViewsDataObj'] = newIndependentViewsOnDbsDataObj['dstDbNewViewsDataObj'];
              if len(newIndependentViewsOnDbsDataObj['dstDbViewsDataObj']) > 0: 
                 dstDbIndependentViewsDataObj = newIndependentViewsOnDbsDataObj['dstDbViewsDataObj'];

           

           ### Section abt to get independent views whose definition has been changed ###

           if isExecuteSchmsCmpOnExistDbViewsDefOptns(inputArgsDataObj) == "Y" :

              existIndependentViewsDefChangedOnDbsDataObj = handleBidirProcsngToGetViewsDefChangedInfoBtwnDB(
                   srcDbName, srcDbIndependentViewsDataObj, dstDbName, dstDbIndependentViewsDataObj, isMakeExactDbSchemasCopy
              );

              srcDbIndependentViewsDefChangedDataObj = existIndependentViewsDefChangedOnDbsDataObj['srcDbViewsDefChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbIndependentViewsDefChangedDataObj'] = srcDbIndependentViewsDefChangedDataObj;
              if len(existIndependentViewsDefChangedOnDbsDataObj['srcDbViewsDataObj']) > 0: 
                 srcDbIndependentViewsDataObj = existIndependentViewsDefChangedOnDbsDataObj['srcDbViewsDataObj'];

              dstDbIndependentViewsDefChangedDataObj = existIndependentViewsDefChangedOnDbsDataObj['dstDbViewsDefChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbIndependentViewsDefChangedDataObj'] = dstDbIndependentViewsDefChangedDataObj;
              if len(existIndependentViewsDefChangedOnDbsDataObj['dstDbViewsDataObj']) > 0: 
                 dstDbIndependentViewsDataObj = existIndependentViewsDefChangedOnDbsDataObj['dstDbViewsDataObj'];

           

           ### Section abt to get all independent as dependent new views schemas data ###

           if isExecuteSchmsCmpOnExistDbNewViewsOptns(inputArgsDataObj) == "Y" :

              newInAsDependentViewsOnDbsDataObj = handleBidirProcsngToGetNewViewsInfoBtwnDB(
                 srcDbName, srcDbInAsDependentViewsDataObj, dstDbName, dstDbInAsDependentViewsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewInAsDependentViewsDataObj'] = newInAsDependentViewsOnDbsDataObj['srcDbNewViewsDataObj'];
              if len(newInAsDependentViewsOnDbsDataObj['srcDbViewsDataObj']) > 0: 
                 srcDbInAsDependentViewsDataObj = newInAsDependentViewsOnDbsDataObj['srcDbViewsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewInAsDependentViewsDataObj'] = newInAsDependentViewsOnDbsDataObj['dstDbNewViewsDataObj'];
              if len(newInAsDependentViewsOnDbsDataObj['dstDbViewsDataObj']) > 0: 
                 dstDbInAsDependentViewsDataObj = newInAsDependentViewsOnDbsDataObj['dstDbViewsDataObj'];
         

           ### Section abt to get independent as dependent views definition changed ###

           if isExecuteSchmsCmpOnExistDbViewsDefOptns(inputArgsDataObj) == "Y" :

              existInAsDependentViewsDefChangedOnDbsDataObj = handleBidirProcsngToGetViewsDefChangedInfoBtwnDB(
                   srcDbName, srcDbInAsDependentViewsDataObj, dstDbName, dstDbInAsDependentViewsDataObj, isMakeExactDbSchemasCopy
              );

              srcDbInAsDependentViewsDefChangedDataObj = existInAsDependentViewsDefChangedOnDbsDataObj['srcDbViewsDefChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbInAsDependentViewsDefChangedDataObj'] = srcDbInAsDependentViewsDefChangedDataObj;
              if len(existInAsDependentViewsDefChangedOnDbsDataObj['srcDbViewsDataObj']) > 0: 
                 srcDbInAsDependentViewsDataObj = existInAsDependentViewsDefChangedOnDbsDataObj['srcDbViewsDataObj'];

              dstDbInAsDependentViewsDefChangedDataObj = existInAsDependentViewsDefChangedOnDbsDataObj['dstDbViewsDefChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbInAsDependentViewsDefChangedDataObj'] = dstDbInAsDependentViewsDefChangedDataObj;
              if len(existInAsDependentViewsDefChangedOnDbsDataObj['dstDbViewsDataObj']) > 0: 
                 dstDbInAsDependentViewsDataObj = existInAsDependentViewsDefChangedOnDbsDataObj['dstDbViewsDataObj'];

           
           ### Section abt to get all dependent new views schemas data ###

           if isExecuteSchmsCmpOnExistDbNewViewsOptns(inputArgsDataObj) == "Y" :

              newDependentViewsOnDbsDataObj = handleBidirProcsngToGetNewViewsInfoBtwnDB(
                 srcDbName, srcDbDependentViewsDataObj, dstDbName, dstDbDependentViewsDataObj, isMakeExactDbSchemasCopy
              );

              diffDBSchmsDataObj[srcDbName]['srcDbNewDependentViewsDataObj'] = newDependentViewsOnDbsDataObj['srcDbNewViewsDataObj'];
              if len(newDependentViewsOnDbsDataObj['srcDbViewsDataObj']) > 0: 
                 srcDbDependentViewsDataObj = newDependentViewsOnDbsDataObj['srcDbViewsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbNewDependentViewsDataObj'] = newDependentViewsOnDbsDataObj['dstDbNewViewsDataObj'];
              if len(newDependentViewsOnDbsDataObj['dstDbViewsDataObj']) > 0: 
                 dstDbDependentViewsDataObj = newDependentViewsOnDbsDataObj['dstDbViewsDataObj'];

 
           ### Section abt to get dependent views definition changed ###

           if isExecuteSchmsCmpOnExistDbViewsDefOptns(inputArgsDataObj) == "Y" :

              existDependentViewsDefChangedOnDbsDataObj = handleBidirProcsngToGetViewsDefChangedInfoBtwnDB(
                   srcDbName, srcDbDependentViewsDataObj, dstDbName, dstDbDependentViewsDataObj, isMakeExactDbSchemasCopy
              );

              srcDbDependentViewsDefChangedDataObj = existDependentViewsDefChangedOnDbsDataObj['srcDbViewsDefChangedDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbDependentViewsDefChangedDataObj'] = srcDbDependentViewsDefChangedDataObj;
              if len(existDependentViewsDefChangedOnDbsDataObj['srcDbViewsDataObj']) > 0: 
                 srcDbDependentViewsDataObj = existDependentViewsDefChangedOnDbsDataObj['srcDbViewsDataObj'];

              dstDbDependentViewsDefChangedDataObj = existDependentViewsDefChangedOnDbsDataObj['dstDbViewsDefChangedDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbDependentViewsDefChangedDataObj'] = dstDbDependentViewsDefChangedDataObj;
              if len(existDependentViewsDefChangedOnDbsDataObj['dstDbViewsDataObj']) > 0: 
                 dstDbDependentViewsDataObj = existDependentViewsDefChangedOnDbsDataObj['dstDbViewsDataObj'];

         

           ### dropping unique schemas changes on srcSvr DB ###
  
           if applyChangesOn == "SrcSvr" and isMakeExactDbSchemasCopy == "Y" :
           

              ### nfk types tables section

              diffDBSchmsDataObj[srcDbName]['srcDbDrpNFKTblsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNewNFKTblsDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbDrpNFKTblsNewColsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsNewColsDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpNFKTblsAllIndxNameDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNewNFKTblsAllIndxNameDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpNFKTblsNewIndxNameDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNFKTblsNewIndxNameDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpNFKTblIndxNewColsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNFKTblIndxNewColsDataObj'];


              ### fkAsNfk types tables section

              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNewFKAsNFKTblsDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblsNewColsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsNewColsDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblsFKNameColConstraintsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNewFKAsNFKTblsFKNameColConstraintsDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblsNewFKNameColConstraintsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsNewFKNameColConstraintsDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblsFKNameNewColsConstraintsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsFKNameNewColsConstraintsDataObj'];


              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblsAllIndxNameDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNewFKAsNFKTblsAllIndxNameDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblsNewIndxNameDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblsNewIndxNameDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKAsNFKTblIndxNewColsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbFKAsNFKTblIndxNewColsDataObj'];
              
      
              ### fk types tables section
               
              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKTblsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNewFKTblsDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKTblsNewColsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbFKTblsNewColsDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKTblsFKNameColConstraintsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNewFKTblsFKNameColConstraintsDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKTblsNewFKNameColConstraintsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbFKTblsNewFKNameColConstraintsDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKTblsFKNameNewColsConstraintsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbFKTblsFKNameNewColsConstraintsDataObj'];
               
              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKTblsAllIndxNameDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNewFKTblsAllIndxNameDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpFKTblsNewIndxNameDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbFKTblsNewIndxNameDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpFkTblIndxNewColsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbFkTblIndxNewColsDataObj'];


              ### tables triggers section
 
              diffDBSchmsDataObj[srcDbName]['srcDbDrpTblsAllTgrNameDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNewTblsAllTgrNameDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbDrpTblsNewTgrNameDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbTblsNewTgrNameDataObj'];

          
              ### routines section

              diffDBSchmsDataObj[srcDbName]['srcDbDrpRoutinesTypeDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNewRoutinesTypeDataObj'];
              diffDBSchmsDataObj[srcDbName]['srcDbDrpRoutinesNameDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNewRoutinesNameDataObj'];

          
              ### views section

              diffDBSchmsDataObj[srcDbName]['srcDbDrpIndependentViewsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNewIndependentViewsDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpInAsDependentViewsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNewInAsDependentViewsDataObj'];

              diffDBSchmsDataObj[srcDbName]['srcDbDrpDependentViewsDataObj'] = diffDBSchmsDataObj[dstDbName]['dstDbNewDependentViewsDataObj'];

      

           ### dropping unique schemas changes on dstSvr DB ###
  
           if applyChangesOn == "DstSvr" and isMakeExactDbSchemasCopy == "Y" :
           

              ### nfk types tables section

              diffDBSchmsDataObj[dstDbName]['dstDbDrpNFKTblsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNewNFKTblsDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbDrpNFKTblsNewColsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsNewColsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbDrpNFKTblsAllIndxNameDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNewNFKTblsAllIndxNameDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbDrpNFKTblsNewIndxNameDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNFKTblsNewIndxNameDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbDrpNFKTblIndxNewColsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNFKTblIndxNewColsDataObj'];


              ### fkAsNfk types tables section

              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNewFKAsNFKTblsDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblsNewColsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsNewColsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblsFKNameColConstraintsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNewFKAsNFKTblsFKNameColConstraintsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblsNewFKNameColConstraintsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsNewFKNameColConstraintsDataObj'] ;

              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblsFKNameNewColsConstraintsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsFKNameNewColsConstraintsDataObj'];


              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblsAllIndxNameDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNewFKAsNFKTblsAllIndxNameDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblsNewIndxNameDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblsNewIndxNameDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKAsNFKTblIndxNewColsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbFKAsNFKTblIndxNewColsDataObj'];
              
      
              ### fk types tables section
               
              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNewFKTblsDataObj'] ;
              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblsNewColsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbFKTblsNewColsDataObj'];
              
              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblsFKNameColConstraintsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNewFKTblsFKNameColConstraintsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblsNewFKNameColConstraintsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbFKTblsNewFKNameColConstraintsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblsFKNameNewColsConstraintsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbFKTblsFKNameNewColsConstraintsDataObj'];
               
              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblsAllIndxNameDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNewFKTblsAllIndxNameDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblsNewIndxNameDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbFKTblsNewIndxNameDataObj'];
     
              diffDBSchmsDataObj[dstDbName]['dstDbDrpFKTblIndxNewColsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbFkTblIndxNewColsDataObj'];


              ### tables triggers section
 
              diffDBSchmsDataObj[dstDbName]['dstDbDrpTblsAllTgrNameDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNewTblsAllTgrNameDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbDrpTblsNewTgrNameDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbTblsNewTgrNameDataObj'];

          
              ### routines section

              diffDBSchmsDataObj[dstDbName]['dstDbDrpRoutinesTypeDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNewRoutinesTypeDataObj'];
              diffDBSchmsDataObj[dstDbName]['dstDbDrpRoutinesNameDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNewRoutinesNameDataObj'];

          
              ### views section

              diffDBSchmsDataObj[dstDbName]['dstDbDrpIndependentViewsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNewIndependentViewsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbDrpInAsDependentViewsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNewInAsDependentViewsDataObj'];

              diffDBSchmsDataObj[dstDbName]['dstDbDrpDependentViewsDataObj'] = diffDBSchmsDataObj[srcDbName]['srcDbNewDependentViewsDataObj'];



           ### finally collected setup infoSchemas between source and destination server DB
   
           diffDBSchmsDataObj[srcDbName]['NFKTblsDataObj'] = srcDbNFKTblsDataObj;
           diffDBSchmsDataObj[srcDbName]['NFKTblsAttrOptnDataObj'] = srcDbNFKTblsAttrOptnDataObj;
           diffDBSchmsDataObj[srcDbName]['NFKTblsIndexesDataObj'] = srcDbNFKTblsIndexesDataObj;
           diffDBSchmsDataObj[srcDbName]['FKAsNFKTblsDataObj'] = srcDbFKAsNFKTblsDataObj;
           diffDBSchmsDataObj[srcDbName]['FKAsNFKTblsAttrOptnDataObj'] = srcDbFKAsNFKTblsAttrOptnDataObj;
           diffDBSchmsDataObj[srcDbName]['FKAsNFKTblsConstraintsDataObj'] = srcDbFKAsNFKTblsConstraintsDataObj;
           diffDBSchmsDataObj[srcDbName]['FKAsNFKTblsIndexesDataObj'] = srcDbFKAsNFKTblsIndexesDataObj;
           diffDBSchmsDataObj[srcDbName]['FKTblsDataObj'] = srcDbFKTblsDataObj;
           diffDBSchmsDataObj[srcDbName]['FKTblsAttrOptnDataObj'] = srcDbFKTblsAttrOptnDataObj;
           diffDBSchmsDataObj[srcDbName]['FKTblsConstraintsDataObj'] = srcDbFKTblsConstraintsDataObj;
           diffDBSchmsDataObj[srcDbName]['FKTblsIndexesDataObj'] = srcDbFKTblsIndexesDataObj;
           diffDBSchmsDataObj[srcDbName]['triggersDataObj'] = srcDbTriggersDataObj;
           diffDBSchmsDataObj[srcDbName]['routinesDataObj'] = srcDbRoutinesDataObj;
           diffDBSchmsDataObj[srcDbName]['independentViewsDataObj'] = srcDbIndependentViewsDataObj;
           diffDBSchmsDataObj[srcDbName]['InAsDependentViewsDataObj'] = srcDbInAsDependentViewsDataObj;
           diffDBSchmsDataObj[srcDbName]['dependentViewsDataObj'] = srcDbDependentViewsDataObj;


           diffDBSchmsDataObj[dstDbName]['NFKTblsDataObj'] = dstDbNFKTblsDataObj;
           diffDBSchmsDataObj[dstDbName]['NFKTblsAttrOptnDataObj'] = dstDbNFKTblsAttrOptnDataObj;
           diffDBSchmsDataObj[dstDbName]['NFKTblsIndexesDataObj'] = dstDbNFKTblsIndexesDataObj;
           diffDBSchmsDataObj[dstDbName]['FKAsNFKTblsDataObj'] = dstDbFKAsNFKTblsDataObj;
           diffDBSchmsDataObj[dstDbName]['FKAsNFKTblsAttrOptnDataObj'] = dstDbFKAsNFKTblsAttrOptnDataObj;
           diffDBSchmsDataObj[dstDbName]['FKAsNFKTblsConstraintsDataObj'] = dstDbFKAsNFKTblsConstraintsDataObj;
           diffDBSchmsDataObj[dstDbName]['FKAsNFKTblsIndexesDataObj'] = dstDbFKAsNFKTblsIndexesDataObj;
           diffDBSchmsDataObj[dstDbName]['FKTblsDataObj'] = dstDbFKTblsDataObj;
           diffDBSchmsDataObj[dstDbName]['FKTblsAttrOptnDataObj'] = dstDbFKTblsAttrOptnDataObj; 
           diffDBSchmsDataObj[dstDbName]['FKTblsConstraintsDataObj'] = dstDbFKTblsConstraintsDataObj;
           diffDBSchmsDataObj[dstDbName]['FKTblsIndexesDataObj'] = dstDbFKTblsIndexesDataObj;
           diffDBSchmsDataObj[dstDbName]['triggersDataObj'] = dstDbTriggersDataObj;
           diffDBSchmsDataObj[dstDbName]['routinesDataObj'] = dstDbRoutinesDataObj;
           diffDBSchmsDataObj[dstDbName]['independentViewsDataObj'] = dstDbIndependentViewsDataObj;
           diffDBSchmsDataObj[dstDbName]['InAsDependentViewsDataObj'] = dstDbInAsDependentViewsDataObj;
           diffDBSchmsDataObj[dstDbName]['dependentViewsDataObj'] = dstDbDependentViewsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return diffDBSchmsDataObj;



### handle processing to get rename table foreign key col names btwn src and dst db ###

def handleProcsngToGetRenameTblFKSColnamesSchemasBtwnSrcAndDstDB(srcTblsDataObj, dstTblsDataObj):

    tblsFKSColsRenameSchemasDataObj = {};    
    
    try:

        if len(srcTblsDataObj)>0 and len(dstTblsDataObj)>0 :

           for srcTblName in srcTblsDataObj : 
               isDstTblNameExist = iskeynameExistInDictObj(dstTblsDataObj, srcTblName);   
               if isDstTblNameExist == True:
                  srcTblAllFKSDataObj = srcTblsDataObj[srcTblName];
                  dstTblAllFKSDataObj = dstTblsDataObj[srcTblName];
                  allFKSColsRenameSchemasDataObj = {};
                  for srcTblFKName in srcTblAllFKSDataObj:
                      isDstTblFKNameExist = iskeynameExistInDictObj(dstTblAllFKSDataObj, srcTblFKName);
                      if isDstTblFKNameExist == True :   
                         srcTblAllColsDataObj = srcTblAllFKSDataObj[srcTblFKName]['fkAllCols'];
                         dstTblAllColsDataObj = dstTblAllFKSDataObj[srcTblFKName]['fkAllCols'];
                         fkColsRenameSchemasDataObj = {};
                         for srcTblOrgColName in srcTblAllColsDataObj :
                             isDstTblSrcOrgColNameExist = iskeynameExistInDictObj(dstTblAllColsDataObj, srcTblOrgColName);
                             if isDstTblSrcOrgColNameExist == False :
                                srcTblOrgColNameAsUpperCase = srcTblOrgColName.upper();
                                srcTblOrgColNameAsLowerCase = srcTblOrgColName.lower();
                                isDstTblUpperCaseColNameExist = iskeynameExistInDictObj(dstTblAllColsDataObj, srcTblOrgColNameAsUpperCase);
                                isDstTblLowerCaseColNameExist = iskeynameExistInDictObj(dstTblAllColsDataObj, srcTblOrgColNameAsLowerCase);
                                if isDstTblUpperCaseColNameExist == True :
                                   jsonToStr = str(json.dumps(dstTblAllColsDataObj[srcTblOrgColNameAsUpperCase]));
                                   jsonToStr = jsonToStr.replace(srcTblOrgColNameAsUpperCase, srcTblOrgColName);
                                   dstTblAllColsDataObj[srcTblOrgColName] = json.loads(jsonToStr);
                                   fkColsRenameSchemasDataObj[srcTblOrgColNameAsUpperCase] = {
                                       'renameColName' : srcTblOrgColName,
                                       'renameColDataObj' :  dstTblAllColsDataObj[srcTblOrgColName]
                                   };
                                   del dstTblAllColsDataObj[srcTblOrgColNameAsUpperCase];
                                   del dstTblAllColsDataObj[srcTblOrgColName];
                                if isDstTblLowerCaseColNameExist == True :
                                   jsonToStr = str(json.dumps(dstTblAllColsDataObj[srcTblOrgColNameAsLowerCase]));
                                   jsonToStr = jsonToStr.replace(srcTblOrgColNameAsLowerCase, srcTblOrgColName);
                                   dstTblAllColsDataObj[srcTblOrgColName] = json.loads(jsonToStr);
                                   fkColsRenameSchemasDataObj[srcTblOrgColNameAsLowerCase] = {
                                       'renameColName' : srcTblOrgColName,
                                       'renameColDataObj' :  dstTblAllColsDataObj[srcTblOrgColName]
                                   };    
                                   del dstTblAllColsDataObj[srcTblOrgColNameAsLowerCase];
                                   del dstTblAllColsDataObj[srcTblOrgColName];
                          
                         if len(fkColsRenameSchemasDataObj)>0:           
                            allFKSColsRenameSchemasDataObj[srcTblFKName] = dstTblAllIndexesDataObj[srcTblFKName];
                            allFKSColsRenameSchemasDataObj[srcTblFKName]['fkAllCols'] = fkColsRenameSchemasDataObj;  

                  if len(allFKSColsRenameSchemasDataObj)>0 :
                     tblsFKSColsRenameSchemasDataObj[srcTblName] = allFKSColsRenameSchemasDataObj;
 

    except Exception as e:
           handleProcsngAbtErrException("Y");

    return tblsFKSColsRenameSchemasDataObj;



### handle processing to get rename table index col names btwn src and dst db ###

def handleProcsngToGetRenameTblIndxColnamesSchemasBtwnSrcAndDstDB(srcTblsDataObj, dstTblsDataObj):

    tblsIndexesColsRenameSchemasDataObj = {};    
    
    try:

        if len(srcTblsDataObj)>0 and len(dstTblsDataObj)>0 :

           for srcTblName in srcTblsDataObj : 
               isDstTblNameExist = iskeynameExistInDictObj(dstTblsDataObj, srcTblName);   
               if isDstTblNameExist == True:
                  srcTblAllIndexesDataObj = srcTblsDataObj[srcTblName];
                  dstTblAllIndexesDataObj = dstTblsDataObj[srcTblName];
                  allIndxColsRenameSchemasDataObj = {};
                  for srcTblIndxName in srcTblAllIndexesDataObj:
                      isDstTblIndxNameExist = iskeynameExistInDictObj(dstTblAllIndexesDataObj, srcTblIndxName);
                      if isDstTblIndxNameExist == True :   
                         srcTblAllColsDataObj = srcTblAllIndexesDataObj[srcTblIndxName]['indxAllCols'];
                         dstTblAllColsDataObj = dstTblAllIndexesDataObj[srcTblIndxName]['indxAllCols'];
                         indxColsRenameSchemasDataObj = {};
                         for srcTblOrgColName in srcTblAllColsDataObj :
                             isDstTblSrcOrgColNameExist = iskeynameExistInDictObj(dstTblAllColsDataObj, srcTblOrgColName);
                             if isDstTblSrcOrgColNameExist == False :
                                srcTblOrgColNameAsUpperCase = srcTblOrgColName.upper();
                                srcTblOrgColNameAsLowerCase = srcTblOrgColName.lower();
                                isDstTblUpperCaseColNameExist = iskeynameExistInDictObj(dstTblAllColsDataObj, srcTblOrgColNameAsUpperCase);
                                isDstTblLowerCaseColNameExist = iskeynameExistInDictObj(dstTblAllColsDataObj, srcTblOrgColNameAsLowerCase);
                                if isDstTblUpperCaseColNameExist == True :
                                   jsonToStr = str(json.dumps(dstTblAllColsDataObj[srcTblOrgColNameAsUpperCase]));
                                   jsonToStr = jsonToStr.replace(srcTblOrgColNameAsUpperCase, srcTblOrgColName);
                                   dstTblAllColsDataObj[srcTblOrgColName] = json.loads(jsonToStr);
                                   indxColsRenameSchemasDataObj[srcTblOrgColNameAsUpperCase] = {
                                       'renameColName' : srcTblOrgColName,
                                       'renameColDataObj' :  dstTblAllColsDataObj[srcTblOrgColName]
                                   };
                                   del dstTblAllColsDataObj[srcTblOrgColNameAsUpperCase];
                                   del dstTblAllColsDataObj[srcTblOrgColName]; 
                                if isDstTblLowerCaseColNameExist == True :
                                   jsonToStr = str(json.dumps(dstTblAllColsDataObj[srcTblOrgColNameAsLowerCase]));
                                   jsonToStr = jsonToStr.replace(srcTblOrgColNameAsLowerCase, srcTblOrgColName);
                                   dstTblAllColsDataObj[srcTblOrgColName] = json.loads(jsonToStr);
                                   indxColsRenameSchemasDataObj[srcTblOrgColNameAsLowerCase] = {
                                       'renameColName' : srcTblOrgColName,
                                       'renameColDataObj' :  dstTblAllColsDataObj[srcTblOrgColName]
                                   };    
                                   del dstTblAllColsDataObj[srcTblOrgColNameAsLowerCase];
                                   del dstTblAllColsDataObj[srcTblOrgColName];
                          
                         if len(indxColsRenameSchemasDataObj)>0:           
                            allIndxColsRenameSchemasDataObj[srcTblIndxName] = dstTblAllIndexesDataObj[srcTblIndxName];
                            allIndxColsRenameSchemasDataObj[srcTblIndxName]['indxAllCols'] = indxColsRenameSchemasDataObj;  

                  if len(allIndxColsRenameSchemasDataObj)>0 :
                     tblsIndexesColsRenameSchemasDataObj[srcTblName] = allIndxColsRenameSchemasDataObj;
 

    except Exception as e:
           handleProcsngAbtErrException("Y");

    return tblsIndexesColsRenameSchemasDataObj;



### handle processing to get rename table col names btwn src and dst db ###

def handleProcsngToGetRenameTblColnamesSchemasBtwnSrcAndDstDB(srcTblsDataObj, dstTblsDataObj):

    tblsColsRenameSchemasDataObj = {};    
    
    try:

        if len(srcTblsDataObj)>0 and len(dstTblsDataObj)>0 :

           for srcTblName in srcTblsDataObj : 
               isDstTblNameExist = iskeynameExistInDictObj(dstTblsDataObj, srcTblName);   
               if isDstTblNameExist == True:
                  srcTblAllColsDataObj = srcTblsDataObj[srcTblName]['tblAllCols'];
                  dstTblAllColsDataObj = dstTblsDataObj[srcTblName]['tblAllCols'];
                  colsRenameSchemasDataObj = {};
                  for srcTblOrgColName in srcTblAllColsDataObj :
                      isDstTblSrcOrgColNameExist = iskeynameExistInDictObj(dstTblAllColsDataObj, srcTblOrgColName);
                      if isDstTblSrcOrgColNameExist == False :
                         srcTblOrgColNameAsUpperCase = srcTblOrgColName.upper();
                         srcTblOrgColNameAsLowerCase = srcTblOrgColName.lower();
                         isDstTblUpperCaseColNameExist = iskeynameExistInDictObj(dstTblAllColsDataObj, srcTblOrgColNameAsUpperCase);
                         isDstTblLowerCaseColNameExist = iskeynameExistInDictObj(dstTblAllColsDataObj, srcTblOrgColNameAsLowerCase);
                         if isDstTblUpperCaseColNameExist == True :
                            jsonToStr = str(json.dumps(dstTblAllColsDataObj[srcTblOrgColNameAsUpperCase]));
                            jsonToStr = jsonToStr.replace(srcTblOrgColNameAsUpperCase, srcTblOrgColName);
                            dstTblAllColsDataObj[srcTblOrgColName] = json.loads(jsonToStr);
                            colsRenameSchemasDataObj[srcTblOrgColNameAsUpperCase] = {
                                'renameColName' : srcTblOrgColName,
                                'renameColDataObj' : dstTblAllColsDataObj[srcTblOrgColName]
                            };
                            del dstTblAllColsDataObj[srcTblOrgColNameAsUpperCase];
                            del dstTblAllColsDataObj[srcTblOrgColName]; 
                         if isDstTblLowerCaseColNameExist == True :
                            jsonToStr = str(json.dumps(dstTblAllColsDataObj[srcTblOrgColNameAsLowerCase]));
                            jsonToStr = jsonToStr.replace(srcTblOrgColNameAsLowerCase, srcTblOrgColName);
                            dstTblAllColsDataObj[srcTblOrgColName] = json.loads(jsonToStr);
                            colsRenameSchemasDataObj[srcTblOrgColNameAsLowerCase] = {
                                'renameColName' : srcTblOrgColName,
                                'renameColDataObj' : dstTblAllColsDataObj[srcTblOrgColName]
                            };
                            del dstTblAllColsDataObj[srcTblOrgColNameAsLowerCase];
                            del dstTblAllColsDataObj[srcTblOrgColName];
                          
                  if len(colsRenameSchemasDataObj)>0:           
                     tblsColsRenameSchemasDataObj[srcTblName] = srcTblsDataObj[srcTblName];
                     tblsColsRenameSchemasDataObj[srcTblName]['tblAllCols'] = colsRenameSchemasDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return tblsColsRenameSchemasDataObj;


def handleProcsngToRenameColnamesBtwnSrcAndDstDB(srcDbName,srcDbDataObj,dstDbName,dstDbDataObj,applyChangesOn,isMakeExactDbSchemasCopy):


    renameColsSchemasStatusDataObj = {};
    renameColsSchemasStatusDataObj['NFKTblsColsRenameDataObj'] = {};
    renameColsSchemasStatusDataObj['FKAsNFKTblsColsRenameDataObj'] = {};
    renameColsSchemasStatusDataObj['FKTblsColsRenameDataObj'] = {}; 

    try:

        if srcDbName!="" and len(srcDbDataObj)>0 and dstDbName!="" and len(dstDbDataObj)>0 :

           if isMakeExactDbSchemasCopy == "Y" :

              srcDbNFKTblsDataObj = srcDbDataObj['NFKTblsDataObj'];
              srcDbNFKTblsIndexesDataObj = srcDbDataObj['NFKTblsIndexesDataObj'];
              srcDbFKAsNFKTblsDataObj = srcDbDataObj['FKAsNFKTblsDataObj'];
              srcDbFKAsNFKTblsConstraintsDataObj = srcDbDataObj['FKAsNFKTblsConstraintsDataObj'];
              srcDbFKAsNFKTblsIndexesDataObj = srcDbDataObj['FKAsNFKTblsIndexesDataObj'];
              srcDbFKTblsDataObj = srcDbDataObj['FKTblsDataObj'];
              srcDbFKTblsConstraintsDataObj = srcDbDataObj['FKTblsConstraintsDataObj']; 
              srcDbFKTblsIndexesDataObj = srcDbDataObj['FKTblsIndexesDataObj'];

              dstDbNFKTblsDataObj = dstDbDataObj['NFKTblsDataObj'];
              dstDbNFKTblsIndexesDataObj = dstDbDataObj['NFKTblsIndexesDataObj'];
              dstDbFKAsNFKTblsDataObj = dstDbDataObj['FKAsNFKTblsDataObj'];
              dstDbFKAsNFKTblsConstraintsDataObj = dstDbDataObj['FKAsNFKTblsConstraintsDataObj'];
              dstDbFKAsNFKTblsIndexesDataObj = dstDbDataObj['FKAsNFKTblsIndexesDataObj'];
              dstDbFKTblsDataObj = dstDbDataObj['FKTblsDataObj'];
              dstDbFKTblsConstraintsDataObj = dstDbDataObj['FKTblsConstraintsDataObj']; 
              dstDbFKTblsIndexesDataObj = dstDbDataObj['FKTblsIndexesDataObj'];


              if applyChangesOn == "DstSvr" :
                 
                 ### section about nfk types table ###

                 dcSrcDbNFKTblsDataObj = copy.deepcopy(srcDbNFKTblsDataObj);
                 dcDstDbNFKTblsDataObj = copy.deepcopy(dstDbNFKTblsDataObj);
                 dcSrcDbNFKTblsIndexesDataObj = copy.deepcopy(srcDbNFKTblsIndexesDataObj);
                 dcDstDbNFKTblsIndexesDataObj = copy.deepcopy(dstDbNFKTblsIndexesDataObj); 

                 NFKTblsColsRenameSchemasDataObj = handleProcsngToGetRenameTblColnamesSchemasBtwnSrcAndDstDB(
                     dcSrcDbNFKTblsDataObj, dcDstDbNFKTblsDataObj
                 );

                 NFKTblsIndexesColsRenameSchemasDataObj = handleProcsngToGetRenameTblIndxColnamesSchemasBtwnSrcAndDstDB(
                     dcSrcDbNFKTblsIndexesDataObj, dcDstDbNFKTblsIndexesDataObj
                 );   

                 if len(NFKTblsColsRenameSchemasDataObj)>0 :
                    for tblName in NFKTblsColsRenameSchemasDataObj :
                        allColsDataObj = NFKTblsColsRenameSchemasDataObj[tblName]['tblAllCols'];
                        for oldColName in allColsDataObj:
                            renameColName = allColsDataObj[oldColName]['renameColName'];
                            renameColDataObj = allColsDataObj[oldColName]['renameColDataObj'];
                            renameColDataObj['oldColName'] = oldColName;
                            renameColDataObj['renameColName'] = renameColName; 
                            dstDbNFKTblsDataObj[tblName]['tblAllCols'][renameColName] = renameColDataObj;  
                            del dstDbNFKTblsDataObj[tblName]['tblAllCols'][oldColName];

                    renameColsSchemasStatusDataObj['NFKTblsDataObj'] = dstDbNFKTblsDataObj;
                    renameColsSchemasStatusDataObj['NFKTblsColsRenameDataObj'] = NFKTblsColsRenameSchemasDataObj;   
 

                 if len(NFKTblsIndexesColsRenameSchemasDataObj)>0 :
                    for tblName in NFKTblsIndexesColsRenameSchemasDataObj :
                        allIndexesDataObj = NFKTblsIndexesColsRenameSchemasDataObj[tblName];
                        for indxName in allIndexesDataObj: 
                            allColsDataObj = allIndexesDataObj[indxName]['indxAllCols']; 
                            for oldColName in allColsDataObj:
                                renameColName = allColsDataObj[oldColName]['renameColName'];
                                renameColDataObj = allColsDataObj[oldColName]['renameColDataObj']; 
                                dstDbNFKTblsIndexesDataObj[tblName][indxName]['indxAllCols'][renameColName] = renameColDataObj;  
                                del dstDbNFKTblsIndexesDataObj[tblName][indxName]['indxAllCols'][oldColName];

                    renameColsSchemasStatusDataObj['NFKTblsIndexesDataObj'] = dstDbNFKTblsIndexesDataObj;


                 ### section about fk as nfk types tables ###
        
                 dcSrcDbFKAsNFKTblsDataObj = copy.deepcopy(srcDbFKAsNFKTblsDataObj);
                 dcDstDbFKAsNFKTblsDataObj = copy.deepcopy(dstDbFKAsNFKTblsDataObj);
                 dcSrcDbFKAsNFKTblsIndexesDataObj = copy.deepcopy(srcDbFKAsNFKTblsIndexesDataObj);
                 dcDstDbFKAsNFKTblsIndexesDataObj = copy.deepcopy(dstDbFKAsNFKTblsIndexesDataObj);
                 dcSrcDbFKAsNFKTblsConstraintsDataObj = copy.deepcopy(srcDbFKAsNFKTblsConstraintsDataObj);
                 dcDstDbFKAsNFKTblsConstraintsDataObj = copy.deepcopy(dstDbFKAsNFKTblsConstraintsDataObj);  
 
                 FKAsNFKTblsColsRenameSchemasDataObj = handleProcsngToGetRenameTblColnamesSchemasBtwnSrcAndDstDB(
                     dcSrcDbFKAsNFKTblsDataObj, dcDstDbFKAsNFKTblsDataObj
                 );

                 FKAsNFKTblsIndexesColsRenameSchemasDataObj = handleProcsngToGetRenameTblIndxColnamesSchemasBtwnSrcAndDstDB(
                     dcSrcDbFKAsNFKTblsIndexesDataObj, dcDstDbFKAsNFKTblsIndexesDataObj
                 );

                 FKAsNFKTblsFKSColsRenameSchemasDataObj = handleProcsngToGetRenameTblFKSColnamesSchemasBtwnSrcAndDstDB(
                     dcSrcDbFKAsNFKTblsConstraintsDataObj, dcDstDbFKAsNFKTblsConstraintsDataObj
                 );
                  
                 if len(FKAsNFKTblsColsRenameSchemasDataObj)>0 :
                    for tblName in FKAsNFKTblsColsRenameSchemasDataObj :
                        allColsDataObj = FKAsNFKTblsColsRenameSchemasDataObj[tblName]['tblAllCols'];
                        for oldColName in allColsDataObj:
                            renameColName = allColsDataObj[oldColName]['renameColName'];
                            renameColDataObj = allColsDataObj[oldColName]['renameColDataObj'];
                            renameColDataObj['oldColName'] = oldColName;
                            renameColDataObj['renameColName'] = renameColName; 
                            dstDbFKAsNFKTblsDataObj[tblName]['tblAllCols'][renameColName] = renameColDataObj;  
                            del dstDbFKAsNFKTblsDataObj[tblName]['tblAllCols'][oldColName];
  
                    renameColsSchemasStatusDataObj['FKAsNFKTblsDataObj'] = dstDbFKAsNFKTblsDataObj;
                    renameColsSchemasStatusDataObj['FKAsNFKTblsColsRenameDataObj'] = FKAsNFKTblsColsRenameSchemasDataObj;                        

                 if len(srcDbFKAsNFKTblsIndexesDataObj)>0 :
                    for tblName in FKAsNFKTblsIndexesColsRenameSchemasDataObj :
                        allIndexesDataObj = FKAsNFKTblsIndexesColsRenameSchemasDataObj[tblName];
                        for indxName in allIndexesDataObj: 
                            allColsDataObj = allIndexesDataObj[indxName]['indxAllCols']; 
                            for oldColName in allColsDataObj:
                                renameColName = allColsDataObj[oldColName]['renameColName'];
                                renameColDataObj = allColsDataObj[oldColName]['renameColDataObj']; 
                                dstDbFKAsNFKTblsIndexesDataObj[tblName][indxName]['indxAllCols'][renameColName] = renameColDataObj;  
                                del dstDbFKAsNFKTblsIndexesDataObj[tblName][indxName]['indxAllCols'][oldColName];
                   
                    renameColsSchemasStatusDataObj['FKAsNFKTblsIndexesDataObj'] = dstDbFKAsNFKTblsIndexesDataObj;
 

                 if len(FKAsNFKTblsFKSColsRenameSchemasDataObj)>0 :
                    for tblName in FKAsNFKTblsFKSColsRenameSchemasDataObj :
                        allFKSDataObj = FKAsNFKTblsFKSColsRenameSchemasDataObj[tblName];
                        for FKName in allFKSDataObj: 
                            allColsDataObj = allFKSDataObj[FKName]['fkAllCols']; 
                            for oldColName in allColsDataObj:
                                renameColName = allColsDataObj[oldColName]['renameColName'];
                                renameColDataObj = allColsDataObj[oldColName]['renameColDataObj']; 
                                dstDbFKAsNFKTblsConstraintsDataObj[tblName][FKName]['fkAllCols'][renameColName] = renameColDataObj;  
                                del dstDbFKAsNFKTblsConstraintsDataObj[tblName][FKName]['fkAllCols'][oldColName];
                    
                    renameColsSchemasStatusDataObj['FKAsNFKTblsConstraintsDataObj'] = dstDbFKAsNFKTblsConstraintsDataObj;
  

                 ### section about fk types tables ###
   
                 dcSrcDbFKTblsDataObj = copy.deepcopy(srcDbFKTblsDataObj);
                 dcDstDbFKTblsDataObj = copy.deepcopy(dstDbFKTblsDataObj);
                 dcSrcDbFKTblsIndexesDataObj = copy.deepcopy(srcDbFKTblsIndexesDataObj);
                 dcDstDbFKTblsIndexesDataObj = copy.deepcopy(dstDbFKTblsIndexesDataObj);
                 dcSrcDbFKTblsConstraintsDataObj = copy.deepcopy(srcDbFKTblsConstraintsDataObj);
                 dcDstDbFKTblsConstraintsDataObj = copy.deepcopy(dstDbFKTblsConstraintsDataObj);

                 FKTblsColsRenameSchemasDataObj = handleProcsngToGetRenameTblColnamesSchemasBtwnSrcAndDstDB(
                     dcSrcDbFKTblsDataObj, dcDstDbFKTblsDataObj
                 );

                 FKTblsIndexesColsRenameSchemasDataObj = handleProcsngToGetRenameTblIndxColnamesSchemasBtwnSrcAndDstDB(
                     dcSrcDbFKTblsIndexesDataObj, dcDstDbFKTblsIndexesDataObj
                 );

                 FKTblsFKSColsRenameSchemasDataObj = handleProcsngToGetRenameTblFKSColnamesSchemasBtwnSrcAndDstDB(
                     dcSrcDbFKTblsConstraintsDataObj, dcDstDbFKTblsConstraintsDataObj
                 );
                  
                 if len(FKTblsColsRenameSchemasDataObj)>0 :
                    for tblName in FKTblsColsRenameSchemasDataObj :
                        allColsDataObj = FKTblsColsRenameSchemasDataObj[tblName]['tblAllCols'];
                        for oldColName in allColsDataObj:
                            renameColName = allColsDataObj[oldColName]['renameColName'];
                            renameColDataObj = allColsDataObj[oldColName]['renameColDataObj'];
                            renameColDataObj['oldColName'] = oldColName;
                            renameColDataObj['renameColName'] = renameColName;
                            dstDbFKTblsDataObj[tblName]['tblAllCols'][renameColName] = renameColDataObj;  
                            del dstDbFKTblsDataObj[tblName]['tblAllCols'][oldColName];
  
                    renameColsSchemasStatusDataObj['FKTblsDataObj'] = dstDbFKTblsDataObj; 
                    renameColsSchemasStatusDataObj['FKTblsColsRenameDataObj'] = FKTblsColsRenameSchemasDataObj;    

                 if len(FKTblsIndexesColsRenameSchemasDataObj)>0 :
                    for tblName in FKTblsIndexesColsRenameSchemasDataObj :
                        allIndexesDataObj = FKTblsIndexesColsRenameSchemasDataObj[tblName];
                        for indxName in allIndexesDataObj: 
                            allColsDataObj = allIndexesDataObj[indxName]['indxAllCols']; 
                            for oldColName in allColsDataObj:
                                renameColName = allColsDataObj[oldColName]['renameColName'];
                                renameColDataObj = allColsDataObj[oldColName]['renameColDataObj']; 
                                dstDbFKTblsIndexesDataObj[tblName][indxName]['indxAllCols'][renameColName] = renameColDataObj;  
                                del dstDbFKTblsIndexesDataObj[tblName][indxName]['indxAllCols'][oldColName];

                    renameColsSchemasStatusDataObj['FKTblsIndexesDataObj'] = dstDbFKTblsIndexesDataObj;                     


                 if len(FKTblsFKSColsRenameSchemasDataObj)>0 :
                    for tblName in FKTblsFKSColsRenameSchemasDataObj :
                        allFKSDataObj = FKTblsFKSColsRenameSchemasDataObj[tblName];
                        for FKName in allFKSDataObj: 
                            allColsDataObj = allFKSDataObj[FKName]['fkAllCols']; 
                            for oldColName in allColsDataObj:
                                renameColName = allColsDataObj[oldColName]['renameColName'];
                                renameColDataObj = allColsDataObj[oldColName]['renameColDataObj']; 
                                dstDbFKTblsConstraintsDataObj[tblName][FKName]['fkAllCols'][renameColName] = renameColDataObj;  
                                del dstDbFKTblsConstraintsDataObj[tblName][FKName]['fkAllCols'][oldColName];
                        
                    renameColsSchemasStatusDataObj['FKTblsConstraintsDataObj'] = dstDbFKTblsConstraintsDataObj;
                   



    except Exception as e:
           handleProcsngAbtErrException("Y"); 

    return renameColsSchemasStatusDataObj;
  


### segregate schemas data of dstSvr db via lookup svrDB schemas ###

def segregateStoredSchemasDataOfDstSvrDBViaLookupSrcSvrDBSchemas(srcDbName,srcDbDataObj,dstDbName,dstDbDataObj):
     
    segregateSchemasDataObj = {}; 
    segregateSchemasDataObj['NFKTblsDataObj'] = {};
    segregateSchemasDataObj['NFKTblsAttrOptnDataObj'] = {}; 
    segregateSchemasDataObj['NFKTblsIndexesDataObj'] = {};
    segregateSchemasDataObj['FKAsNFKTblsDataObj'] = {};
    segregateSchemasDataObj['FKAsNFKTblsAttrOptnDataObj'] = {};  
    segregateSchemasDataObj['FKAsNFKTblsConstraintsDataObj'] = {};
    segregateSchemasDataObj['FKAsNFKTblsIndexesDataObj'] = {};
    segregateSchemasDataObj['FKTblsDataObj'] = {};
    segregateSchemasDataObj['FKTblsAttrOptnDataObj'] = {};
    segregateSchemasDataObj['FKTblsConstraintsDataObj'] = {};
    segregateSchemasDataObj['FKTblsIndexesDataObj'] = {};

    try:

       if srcDbName!="" and len(srcDbDataObj)>0 and dstDbName!="" and len(dstDbDataObj)>0 :


          ### section about srcSvr DB schemas data 
    
          srcDBNFKTblsDataObj = {};
          srcDBNFKTblsAttrOptnDataObj = {};
          srcDBNFKTblsIndexesDataObj = {};
          srcDBFKAsNFKTblsDataObj = {};
          srcDBFKAsNFKTblsAttrOptnDataObj = {};
          srcDBFKAsNFKTblsConstraintsDataObj = {};
          srcDBFKAsNFKTblsIndexesDataObj = {};
          srcDBFKTblsDataObj = {};
          srcDBFKTblsAttrOptnDataObj = {};
          srcDBFKTblsConstraintsDataObj = {};
          srcDBFKTblsIndexesDataObj = {};
        
          if iskeynameExistInDictObj(srcDbDataObj, 'NFKTblsDataObj') == True :
             srcDBNFKTblsDataObj = srcDbDataObj['NFKTblsDataObj'];

          if iskeynameExistInDictObj(srcDbDataObj, 'NFKTblsAttrOptnDataObj') == True :
             srcDBNFKTblsAttrOptnDataObj = srcDbDataObj['NFKTblsAttrOptnDataObj'];

          if iskeynameExistInDictObj(srcDbDataObj, 'NFKTblsIndexesDataObj') == True :
             srcDBNFKTblsIndexesDataObj = srcDbDataObj['NFKTblsIndexesDataObj'];

          if iskeynameExistInDictObj(srcDbDataObj, 'FKAsNFKTblsDataObj') == True :
             srcDBFKAsNFKTblsDataObj = srcDbDataObj['FKAsNFKTblsDataObj'];

          if iskeynameExistInDictObj(srcDbDataObj, 'FKAsNFKTblsAttrOptnDataObj') == True :
             srcDBFKAsNFKTblsAttrOptnDataObj = srcDbDataObj['FKAsNFKTblsAttrOptnDataObj'];

          if iskeynameExistInDictObj(srcDbDataObj, 'FKAsNFKTblsConstraintsDataObj') == True :
             srcDBFKAsNFKTblsConstraintsDataObj = srcDbDataObj['FKAsNFKTblsConstraintsDataObj'];

          if iskeynameExistInDictObj(srcDbDataObj, 'FKAsNFKTblsIndexesDataObj') == True :
             srcDBFKAsNFKTblsIndexesDataObj = srcDbDataObj['FKAsNFKTblsIndexesDataObj'];
 
          if iskeynameExistInDictObj(srcDbDataObj, 'FKTblsDataObj') == True :
             srcDBFKTblsDataObj = srcDbDataObj['FKTblsDataObj'];

          if iskeynameExistInDictObj(srcDbDataObj, 'FKTblsAttrOptnDataObj') == True :
             srcDBFKTblsAttrOptnDataObj = srcDbDataObj['FKTblsAttrOptnDataObj']; 

          if iskeynameExistInDictObj(srcDbDataObj, 'FKTblsConstraintsDataObj') == True :
             srcDBFKTblsConstraintsDataObj = srcDbDataObj['FKTblsConstraintsDataObj'];  

          if iskeynameExistInDictObj(srcDbDataObj, 'FKTblsIndexesDataObj') == True :
             srcDBFKTblsIndexesDataObj = srcDbDataObj['FKTblsIndexesDataObj'];


          ### section about dstSvr DB schemas data 
    
          dstDBNFKTblsDataObj = {};
          dstDBNFKTblsAttrOptnDataObj = {};
          dstDBNFKTblsIndexesDataObj = {};
          dstDBFKAsNFKTblsDataObj = {};
          dstDBFKAsNFKTblsAttrOptnDataObj = {}; 
          dstDBFKAsNFKTblsConstraintsDataObj = {};
          dstDBFKAsNFKTblsIndexesDataObj = {};
          dstDBFKTblsDataObj = {};
          dstDBFKTblsAttrOptnDataObj = {}; 
          dstDBFKTblsConstraintsDataObj = {};
          dstDBFKTblsIndexesDataObj = {};
        
          if iskeynameExistInDictObj(dstDbDataObj, 'NFKTblsDataObj') == True :
             dstDBNFKTblsDataObj = dstDbDataObj['NFKTblsDataObj'];

          if iskeynameExistInDictObj(dstDbDataObj, 'NFKTblsAttrOptnDataObj') == True :
             dstDBNFKTblsAttrOptnDataObj = dstDbDataObj['NFKTblsAttrOptnDataObj'];

          if iskeynameExistInDictObj(dstDbDataObj, 'NFKTblsIndexesDataObj') == True :
             dstDBNFKTblsIndexesDataObj = dstDbDataObj['NFKTblsIndexesDataObj'];

          if iskeynameExistInDictObj(dstDbDataObj, 'FKAsNFKTblsDataObj') == True :
             dstDBFKAsNFKTblsDataObj = dstDbDataObj['FKAsNFKTblsDataObj'];
       
          if iskeynameExistInDictObj(dstDbDataObj, 'FKAsNFKTblsAttrOptnDataObj') == True :
             dstDBFKAsNFKTblsAttrOptnDataObj = dstDbDataObj['FKAsNFKTblsAttrOptnDataObj'];

          if iskeynameExistInDictObj(dstDbDataObj, 'FKAsNFKTblsConstraintsDataObj') == True :
             dstDBFKAsNFKTblsConstraintsDataObj = dstDbDataObj['FKAsNFKTblsConstraintsDataObj'];

          if iskeynameExistInDictObj(dstDbDataObj, 'FKAsNFKTblsIndexesDataObj') == True :
             dstDBFKAsNFKTblsIndexesDataObj = dstDbDataObj['FKAsNFKTblsIndexesDataObj'];
 
          if iskeynameExistInDictObj(dstDbDataObj, 'FKTblsDataObj') == True :
             dstDBFKTblsDataObj = dstDbDataObj['FKTblsDataObj'];

          if iskeynameExistInDictObj(dstDbDataObj, 'FKTblsAttrOptnDataObj') == True :
             dstDBFKTblsAttrOptnDataObj = dstDbDataObj['FKTblsAttrOptnDataObj'];

          if iskeynameExistInDictObj(dstDbDataObj, 'FKTblsConstraintsDataObj') == True :
             dstDBFKTblsConstraintsDataObj = dstDbDataObj['FKTblsConstraintsDataObj'];  

          if iskeynameExistInDictObj(dstDbDataObj, 'FKTblsIndexesDataObj') == True :
             dstDBFKTblsIndexesDataObj = dstDbDataObj['FKTblsIndexesDataObj'];


          ### Section about nfk tables schemas data ###

          for srcDbTblName in srcDBNFKTblsDataObj :

              if iskeynameExistInDictObj(dstDBFKAsNFKTblsDataObj, srcDbTblName) == True :
                 dstDBNFKTblsDataObj[srcDbTblName] = dstDBFKAsNFKTblsDataObj[srcDbTblName];
                 del dstDBFKAsNFKTblsDataObj[srcDbTblName];

              if iskeynameExistInDictObj(dstDBFKTblsDataObj, srcDbTblName) == True : 
                 dstDBNFKTblsDataObj[srcDbTblName] = dstDBFKTblsDataObj[srcDbTblName];
                 del dstDBFKTblsDataObj[srcDbTblName];


          ### Section about fkAsNFK tables schemas data ###

          for srcDbTblName in srcDBFKAsNFKTblsDataObj :

              if iskeynameExistInDictObj(dstDBNFKTblsDataObj, srcDbTblName) == True :
                 dstDBFKAsNFKTblsDataObj[srcDbTblName] = dstDBNFKTblsDataObj[srcDbTblName];
                 del dstDBNFKTblsDataObj[srcDbTblName];

              if iskeynameExistInDictObj(dstDBFKTblsDataObj, srcDbTblName) == True : 
                 dstDBFKAsNFKTblsDataObj[srcDbTblName] = dstDBFKTblsDataObj[srcDbTblName];
                 del dstDBFKTblsDataObj[srcDbTblName];


          ### Section about fk tables schemas data ###

          for srcDbTblName in srcDBFKTblsDataObj :
 
              if iskeynameExistInDictObj(dstDBNFKTblsDataObj, srcDbTblName) == True :
                 dstDBFKTblsDataObj[srcDbTblName] = dstDBNFKTblsDataObj[srcDbTblName];
                 del dstDBNFKTblsDataObj[srcDbTblName];

              if iskeynameExistInDictObj(dstDBFKAsNFKTblsDataObj, srcDbTblName) == True :
                 dstDBFKTblsDataObj[srcDbTblName] = dstDBFKAsNFKTblsDataObj[srcDbTblName];
                 del dstDBFKAsNFKTblsDataObj[srcDbTblName];


          ### Section about nfk tables attributes option schemas data ###

          for srcDbTblName in srcDBNFKTblsAttrOptnDataObj :

              if iskeynameExistInDictObj(dstDBFKAsNFKTblsAttrOptnDataObj, srcDbTblName) == True :
                 dstDBNFKTblsAttrOptnDataObj[srcDbTblName] = dstDBFKAsNFKTblsAttrOptnDataObj[srcDbTblName];
                 del dstDBFKAsNFKTblsAttrOptnDataObj[srcDbTblName];

              if iskeynameExistInDictObj(dstDBFKTblsAttrOptnDataObj, srcDbTblName) == True : 
                 dstDBNFKTblsAttrOptnDataObj[srcDbTblName] = dstDBFKTblsAttrOptnDataObj[srcDbTblName];
                 del dstDBFKTblsAttrOptnDataObj[srcDbTblName];


          ### Section about fkAsNFK tables attributes option schemas data ###

          for srcDbTblName in srcDBFKAsNFKTblsAttrOptnDataObj :

              if iskeynameExistInDictObj(dstDBNFKTblsAttrOptnDataObj, srcDbTblName) == True :
                 dstDBFKAsNFKTblsAttrOptnDataObj[srcDbTblName] = dstDBNFKTblsAttrOptnDataObj[srcDbTblName];    
                 del dstDBNFKTblsAttrOptnDataObj[srcDbTblName];

              if iskeynameExistInDictObj(dstDBFKTblsAttrOptnDataObj, srcDbTblName) == True :
                 dstDBFKAsNFKTblsAttrOptnDataObj[srcDbTblName] = dstDBFKTblsAttrOptnDataObj[srcDbTblName];
                 del dstDBFKTblsAttrOptnDataObj[srcDbTblName];  


          ### Section about fk tables attributes option schemas data ###

          for srcDbTblName in srcDBFKTblsAttrOptnDataObj :
 
              if iskeynameExistInDictObj(dstDBNFKTblsAttrOptnDataObj, srcDbTblName) == True :
                 dstDBFKTblsAttrOptnDataObj[srcDbTblName] = dstDBNFKTblsAttrOptnDataObj[srcDbTblName];
                 del dstDBNFKTblsAttrOptnDataObj[srcDbTblName];

              if iskeynameExistInDictObj(dstDBFKAsNFKTblsAttrOptnDataObj, srcDbTblName) == True :
                 dstDBFKTblsAttrOptnDataObj[srcDbTblName] = dstDBFKAsNFKTblsAttrOptnDataObj[srcDbTblName];
                 del dstDBFKAsNFKTblsAttrOptnDataObj[srcDbTblName]; 


          ### Section about nfk tables indexes schemas data ###

          for srcDbTblName in srcDBNFKTblsIndexesDataObj :

              if iskeynameExistInDictObj(srcDBFKAsNFKTblsIndexesDataObj, srcDbTblName) == True :
                 dstDBNFKTblsIndexesDataObj[srcDbTblName] = srcDBFKAsNFKTblsIndexesDataObj[srcDbTblName];
                 del srcDBFKAsNFKTblsIndexesDataObj[srcDbTblName];

              if iskeynameExistInDictObj(srcDBFKTblsIndexesDataObj, srcDbTblName) == True : 
                 dstDBNFKTblsIndexesDataObj[srcDbTblName] = srcDBFKTblsIndexesDataObj[srcDbTblName];
                 del srcDBFKTblsIndexesDataObj[srcDbTblName];

          
          ### Section about fkAsNFK tables indexes schemas data ###

          for srcDbTblName in srcDBFKAsNFKTblsIndexesDataObj :

              if iskeynameExistInDictObj(dstDBNFKTblsIndexesDataObj, srcDbTblName) == True :
                 dstDBFKAsNFKTblsIndexesDataObj[srcDbTblName] = dstDBNFKTblsIndexesDataObj[srcDbTblName];
                 del dstDBNFKTblsIndexesDataObj[srcDbTblName];

              if iskeynameExistInDictObj(dstDBFKTblsIndexesDataObj, srcDbTblName) == True : 
                 dstDBFKAsNFKTblsIndexesDataObj[srcDbTblName] = dstDBFKTblsIndexesDataObj[srcDbTblName];
                 del dstDBFKTblsIndexesDataObj[srcDbTblName];

  
          ### Section about fk tables indexes schemas data ###

          for srcDbTblName in srcDBFKTblsIndexesDataObj :
 
              if iskeynameExistInDictObj(dstDBNFKTblsIndexesDataObj, srcDbTblName) == True :
                 dstDBFKTblsIndexesDataObj[srcDbTblName] = dstDBNFKTblsIndexesDataObj[srcDbTblName];
                 del dstDBNFKTblsIndexesDataObj[srcDbTblName];

              if iskeynameExistInDictObj(dstDBFKAsNFKTblsIndexesDataObj, srcDbTblName) == True :
                 dstDBFKTblsIndexesDataObj[srcDbTblName] = dstDBFKAsNFKTblsIndexesDataObj[srcDbTblName];
                 del dstDBFKAsNFKTblsIndexesDataObj[srcDbTblName];


          ### Section about fkAsNfk tables constraints schemas data ###

          for srcDbTblName in srcDBFKAsNFKTblsConstraintsDataObj :

              if iskeynameExistInDictObj(dstDBFKTblsConstraintsDataObj, srcDbTblName) == True : 
                   dstDBFKAsNFKTblsConstraintsDataObj[srcDbTblName] = dstDBFKTblsConstraintsDataObj[srcDbTblName];
                   del dstDBFKTblsConstraintsDataObj[srcDbTblName];


          ### Section about fk tables constraints schemas data ###

          for srcDbTblName in srcDBFKTblsConstraintsDataObj :

              if iskeynameExistInDictObj(dstDBFKAsNFKTblsConstraintsDataObj, srcDbTblName) == True : 
                   dstDBFKTblsConstraintsDataObj[srcDbTblName] = dstDBFKAsNFKTblsConstraintsDataObj[srcDbTblName];
                   del dstDBFKAsNFKTblsConstraintsDataObj[srcDbTblName];


          ### overwrite keys data

          segregateSchemasDataObj['NFKTblsDataObj'] = dstDBNFKTblsDataObj;
          segregateSchemasDataObj['NFKTblsAttrOptnDataObj'] = dstDBNFKTblsAttrOptnDataObj;
          segregateSchemasDataObj['NFKTblsIndexesDataObj'] = dstDBNFKTblsIndexesDataObj;
          segregateSchemasDataObj['FKAsNFKTblsDataObj'] = dstDBFKAsNFKTblsDataObj;
          segregateSchemasDataObj['FKAsNFKTblsAttrOptnDataObj'] = dstDBFKAsNFKTblsAttrOptnDataObj;
          segregateSchemasDataObj['FKAsNFKTblsConstraintsDataObj'] = dstDBFKAsNFKTblsConstraintsDataObj;
          segregateSchemasDataObj['FKAsNFKTblsIndexesDataObj'] = dstDBFKAsNFKTblsIndexesDataObj;
          segregateSchemasDataObj['FKTblsDataObj'] = dstDBFKTblsDataObj;
          segregateSchemasDataObj['FKTblsAttrOptnDataObj'] = dstDBFKTblsAttrOptnDataObj;
          segregateSchemasDataObj['FKTblsConstraintsDataObj'] = dstDBFKTblsConstraintsDataObj;
          segregateSchemasDataObj['FKTblsIndexesDataObj'] = dstDBFKTblsIndexesDataObj;

 
    except Exception as e:
           handleProcsngAbtErrException("Y");

    return segregateSchemasDataObj;


### handle processing db level schemas comparsion between source and destination server DBS ###

def handleProcsngDBLvlSchmsCmpBtwnSrcAndDstSvr():

    try:
 
       global srcDbSvrInfoSchemasDataObj;
       global dstDbSvrInfoSchemasDataObj; 
       arr1Length = len(srcDbSvrInfoSchemasDataObj);
       arr2Length = len(dstDbSvrInfoSchemasDataObj);

       if arr1Length <= 0 and arr2Length > 0 :
          msgStr = "\n";
          msgStr+= "SOURCE server given DBS table names schemas data does not exists."; 
          msgStr+= "\n";
          displayMsg('', msgStr);

       elif arr1Length > 0 and arr2Length <= 0 :
          msgStr = "\n";
          msgStr+= "DESTINATION server given DBS table names schemas data does not exists."; 
          msgStr+= "\n";
          displayMsg('', msgStr);

       elif arr1Length > 0 and arr2Length > 0 :

          global inputArgsDataObj;
          applyChangesOn = inputArgsDataObj['applyChangesOn'];
          isMakeExactDbSchemasCopy = inputArgsDataObj['isMakeExactDbSchemasCopy'];
          isExecuteChanges = inputArgsDataObj['isExecuteChanges'];
          srcDbSvrSchemasDataObj = {};
          dstDbSvrSchemasDataObj = {};            

          if iskeynameExistInDictObj(srcDbSvrInfoSchemasDataObj, 'schemasDataObj') == True:
             srcDbSvrSchemasDataObj = srcDbSvrInfoSchemasDataObj['schemasDataObj'];
          if iskeynameExistInDictObj(dstDbSvrInfoSchemasDataObj, 'schemasDataObj') == True:
             dstDbSvrSchemasDataObj = dstDbSvrInfoSchemasDataObj['schemasDataObj']; 
   
          ### iterating source server each db schemas data ###

          for srcDbName in srcDbSvrSchemasDataObj:

              srcDbDataObj = srcDbSvrSchemasDataObj[srcDbName];
              
              ### iterating destination server each db schemas data ###

              for dstDbName in dstDbSvrSchemasDataObj:
                                 
                  dstDbDataObj = dstDbSvrSchemasDataObj[dstDbName];

                  ### segregate dstSvr db schemas data via lookup of srcSvr db schemas for comparsion purpose ###

                  srcDbDataObj1 = copy.deepcopy(srcDbDataObj);
                  dstDbDataObj1 = copy.deepcopy(dstDbDataObj);
                  dstDbSegregateSchemasDataObj = segregateStoredSchemasDataOfDstSvrDBViaLookupSrcSvrDBSchemas(
                      srcDbName, srcDbDataObj1, dstDbName, dstDbDataObj1
                  );
                  if len(dstDbSegregateSchemasDataObj)>0 :
                     dstDbDataObj.update(dstDbSegregateSchemasDataObj);
            

                  ### before db schemas comparsion start overwrite/rename column names 
                  ### from lower to upper case or vice-versa ###

                  renameColsSchemasStatusDataObj = handleProcsngToRenameColnamesBtwnSrcAndDstDB(
                      srcDbName, srcDbDataObj, dstDbName, dstDbDataObj, applyChangesOn, isMakeExactDbSchemasCopy
                  );
                  if len(renameColsSchemasStatusDataObj)>0:
                     if applyChangesOn == "DstSvr" :
                        dstDbDataObj.update(renameColsSchemasStatusDataObj);

                  ### db schemas comparsion is start between srcDbName and dstDbName ###

                  diffDBSchmsDataObj = handleProcsngSchmsCmpBtwnSrcAndDstDB(
                      inputArgsDataObj, srcDbName, srcDbDataObj, dstDbName, dstDbDataObj, applyChangesOn, isMakeExactDbSchemasCopy
                  ); 
                  if len(diffDBSchmsDataObj)>0:
                     
                     srcDiffDBInfoSchemasDataObj = {};
                     dstDiffDBInfoSchemasDataObj = {};
                     diffDBName = '';
                     diffDBInfoSchemasChangesDataObj = {};

                     ### source db schemas data is overwriting ###

                     isSrcDbNameExist = iskeynameExistInDictObj(diffDBSchmsDataObj, srcDbName);
                     if srcDbName == True:
                        srcDiffDBInfoSchemasDataObj = diffDBSchmsDataObj[srcDbName];
                        srcDbDataObj['NFKTblsDataObj'] = srcDiffDBInfoSchemasDataObj['NFKTblsDataObj'];
                        srcDbDataObj['NFKTblsAttrOptnDataObj'] = srcDiffDBInfoSchemasDataObj['NFKTblsAttrOptnDataObj'];
                        srcDbDataObj['NFKTblsIndexesDataObj'] = srcDiffDBInfoSchemasDataObj['NFKTblsIndexesDataObj']; 
                        srcDbDataObj['FKAsNFKTblsDataObj'] = srcDiffDBInfoSchemasDataObj['FKAsNFKTblsDataObj'];
                        srcDbDataObj['FKAsNFKTblsAttrOptnDataObj'] = srcDiffDBInfoSchemasDataObj['FKAsNFKTblsAttrOptnDataObj'];
                        srcDbDataObj['FKAsNFKTblsConstraintsDataObj'] = srcDiffDBInfoSchemasDataObj['FKAsNFKTblsConstraintsDataObj'];
                        srcDbDataObj['FKAsNFKTblsIndexesDataObj'] = srcDiffDBInfoSchemasDataObj['FKAsNFKTblsIndexesDataObj'];
                        srcDbDataObj['FKTblsDataObj'] = srcDiffDBInfoSchemasDataObj['FKTblsDataObj'];
                        srcDbDataObj['FKTblsAttrOptnDataObj'] = srcDiffDBInfoSchemasDataObj['FKTblsAttrOptnDataObj']; 
                        srcDbDataObj['FKTblsConstraintsDataObj'] = srcDiffDBInfoSchemasDataObj['FKTblsConstraintsDataObj'];  
                        srcDbDataObj['FKTblsIndexesDataObj'] = srcDiffDBInfoSchemasDataObj['FKTblsIndexesDataObj'];
                        srcDbDataObj['triggersDataObj'] = srcDiffDBInfoSchemasDataObj['triggersDataObj'];
                        srcDbDataObj['routinesDataObj'] = srcDiffDBInfoSchemasDataObj['routinesDataObj'];
                        srcDbDataObj['independentViewsDataObj'] = srcDiffDBInfoSchemasDataObj['independentViewsDataObj'];
                        srcDbDataObj['InAsDependentViewsDataObj'] = srcDiffDBInfoSchemasDataObj['InAsDependentViewsDataObj'];
                        srcDbDataObj['dependentViewsDataObj'] = srcDiffDBInfoSchemasDataObj['dependentViewsDataObj'];   


                     ### destination db schemas data is overwriting ###

                     isDstDbNameExist = iskeynameExistInDictObj(diffDBSchmsDataObj, dstDbName);
                     if isDstDbNameExist == True:
                        dstDiffDBInfoSchemasDataObj = diffDBSchmsDataObj[dstDbName];
                        dstDbDataObj['NFKTblsDataObj'] = dstDiffDBInfoSchemasDataObj['NFKTblsDataObj'];
                        dstDbDataObj['NFKTblsAttrOptnDataObj'] = dstDiffDBInfoSchemasDataObj['NFKTblsAttrOptnDataObj'];  
                        dstDbDataObj['NFKTblsIndexesDataObj'] = dstDiffDBInfoSchemasDataObj['NFKTblsIndexesDataObj'];
                        dstDbDataObj['FKAsNFKTblsDataObj'] = dstDiffDBInfoSchemasDataObj['FKAsNFKTblsDataObj'];
                        dstDbDataObj['FKAsNFKTblsAttrOptnDataObj'] = dstDiffDBInfoSchemasDataObj['FKAsNFKTblsAttrOptnDataObj'];
                        dstDbDataObj['FKAsNFKTblsConstraintsDataObj'] = dstDiffDBInfoSchemasDataObj['FKAsNFKTblsConstraintsDataObj'];
                        dstDbDataObj['FKAsNFKTblsIndexesDataObj'] = dstDiffDBInfoSchemasDataObj['FKAsNFKTblsIndexesDataObj'];
                        dstDbDataObj['FKTblsDataObj'] = dstDiffDBInfoSchemasDataObj['FKTblsDataObj'];
                        dstDbDataObj['FKTblsAttrOptnDataObj'] = dstDiffDBInfoSchemasDataObj['FKTblsAttrOptnDataObj'];
                        dstDbDataObj['FKTblsConstraintsDataObj'] = dstDiffDBInfoSchemasDataObj['FKTblsConstraintsDataObj'];    
                        dstDbDataObj['FKTblsIndexesDataObj'] = dstDiffDBInfoSchemasDataObj['FKTblsIndexesDataObj'];
                        dstDbDataObj['triggersDataObj'] = dstDiffDBInfoSchemasDataObj['triggersDataObj'];
                        dstDbDataObj['routinesDataObj'] = dstDiffDBInfoSchemasDataObj['routinesDataObj'];
                        dstDbDataObj['independentViewsDataObj'] = dstDiffDBInfoSchemasDataObj['independentViewsDataObj'];
                        dstDbDataObj['InAsDependentViewsDataObj'] = dstDiffDBInfoSchemasDataObj['InAsDependentViewsDataObj'];
                        dstDbDataObj['dependentViewsDataObj'] = dstDiffDBInfoSchemasDataObj['dependentViewsDataObj'];       
                     
                     if applyChangesOn == "SrcSvr" :
                        diffDBName = srcDbName;
                        diffDBInfoSchemasChangesDataObj = srcDiffDBInfoSchemasDataObj;
                     if applyChangesOn == "DstSvr" : 
                        diffDBName = dstDbName; 
                        diffDBInfoSchemasChangesDataObj = dstDiffDBInfoSchemasDataObj;

                
                     ### handle processing to extract db schemas unique adding/updation changes ###

                     dcDiffDBInfoSchemasChangesDataObj2 = copy.deepcopy(diffDBInfoSchemasChangesDataObj);
                     diffDBInfoSchemasUniqAddUpdateChangesDataObj = handleProcsngToExtractUniqAddUpdateDbSchemasChanges(
                         applyChangesOn, dcDiffDBInfoSchemasChangesDataObj2
                     );
                     if len(diffDBInfoSchemasUniqAddUpdateChangesDataObj)>0:
                        diffDBInfoSchemasChangesDataObj.update(diffDBInfoSchemasUniqAddUpdateChangesDataObj);


                     ### handle processing to extract db schemas unique drop changes ###

                     dcDiffDBInfoSchemasChangesDataObj1 = copy.deepcopy(diffDBInfoSchemasChangesDataObj);
                     diffDBInfoSchemasUniqDroppedChangesDataObj = handleProcsngToExtractUniqDbSchemasDropChanges(
                         applyChangesOn, dcDiffDBInfoSchemasChangesDataObj1
                     );
                     if len(diffDBInfoSchemasUniqDroppedChangesDataObj)>0:
                        diffDBInfoSchemasChangesDataObj.update(diffDBInfoSchemasUniqDroppedChangesDataObj);

                     
                     ### replace string ('srcDb => 'db', 'dstDb => 'db') ### 
 
                     diffDBInfoSchemasChangesDataObjStr1 = str(json.dumps(diffDBInfoSchemasChangesDataObj)).replace("srcDb", "db");
                     diffDBInfoSchemasChangesDataObjStr2 = str(json.dumps(diffDBInfoSchemasChangesDataObj)).replace("dstDb", "db");
                     diffDBInfoSchemasChangesDataObj = json.loads(diffDBInfoSchemasChangesDataObjStr2);


                     ### add (isNewSchemas = 'Y/N') key into db infoSchemas data ###
                     addedIsNewSchemasKeyIntoDiffDbSchemasChangesDataObj = handleProcsngToAddIsNewSchemaKeyInDbSchemasChanges(
                            diffDBInfoSchemasChangesDataObj
                     );
                     if len(addedIsNewSchemasKeyIntoDiffDbSchemasChangesDataObj)>0:
                        diffDBInfoSchemasChangesDataObj.update(addedIsNewSchemasKeyIntoDiffDbSchemasChangesDataObj);


                     ### handle processing to store dbSchemas unique dropping/adding/updation changes ###
                     ### compared between source and destination server db ###
                     
                     handleProcsngToStoreDbLvlSchmsChangesSqlQry(
                           applyChangesOn, diffDBName, diffDBInfoSchemasChangesDataObj, isExecuteChanges
                     );

      
    except Exception as e:
           handleProcsngAbtErrException("Y");



### handle processing to update key-value data of dbs btwn source and destination server ###

def handleProcsngToUpdateKeyValueOfDbsInfoSchemasObjBtwnSrcAndDstSvr(againstSvr):

    try:

        infoSchemasDataObj = {};

        if againstSvr == "SrcSvr":
           global dstDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global srcDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        
        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];

        if len(infoSchemasDataObj)>0:
 
           for dbName in infoSchemasDataObj:
             
               dbDataObj = infoSchemasDataObj[dbName];

               NFKTblsDataObj = {};
               NFKTblsAttrOptnDataObj = {};
               NFKTblsIndexesDataObj = {};

               FKAsNFKTblsDataObj = {}; 
               FKAsNFKTblsAttrOptnDataObj = {};
               FKAsNFKTblsConstraintsDataObj = {};
               FKAsNFKTblsIndexesDataObj = {};

               FKTblsDataObj = {};
               FKTblsAttrOptnDataObj = {};
               FKTblsConstraintsDataObj = {};
               FKTblsIndexesDataObj = {};

               allTblsDataObj = {};
               fkConstraintsDataObj = {};
               triggersDataObj = {};
               
               isNFKTblsDataObjExist = iskeynameExistInDictObj(dbDataObj, 'NFKTblsDataObj');
               if isNFKTblsDataObjExist == True :    
                  NFKTblsDataObj = dbDataObj['NFKTblsDataObj'];

               isNFKTblsAttrOptnDataObjExist = iskeynameExistInDictObj(dbDataObj, 'NFKTblsAttrOptnDataObj');
               if isNFKTblsAttrOptnDataObjExist == True :    
                  NFKTblsAttrOptnDataObj = dbDataObj['NFKTblsAttrOptnDataObj'];
 
               isNFKTblsIndexesDataObjExist = iskeynameExistInDictObj(dbDataObj, 'NFKTblsIndexesDataObj');
               if isNFKTblsIndexesDataObjExist == True :    
                  NFKTblsIndexesDataObj = dbDataObj['NFKTblsIndexesDataObj'];

               
               isFKAsNFKTblsDataObjExist = iskeynameExistInDictObj(dbDataObj, 'FKAsNFKTblsDataObj');
               if isFKAsNFKTblsDataObjExist == True :    
                  FKAsNFKTblsDataObj = dbDataObj['FKAsNFKTblsDataObj'];
 
               isFKAsNFKTblsAttrOptnDataObjExist = iskeynameExistInDictObj(dbDataObj, 'FKAsNFKTblsAttrOptnDataObj');
               if isFKAsNFKTblsAttrOptnDataObjExist == True :    
                  FKAsNFKTblsAttrOptnDataObj = dbDataObj['FKAsNFKTblsAttrOptnDataObj'];         
               
               isFKAsNFKTblsConstraintsDataObjExist = iskeynameExistInDictObj(dbDataObj, 'FKAsNFKTblsConstraintsDataObj');
               if isFKAsNFKTblsConstraintsDataObjExist == True :    
                  FKAsNFKTblsConstraintsDataObj = dbDataObj['FKAsNFKTblsConstraintsDataObj'];
  
               isFKAsNFKTblsIndexesDataObjExist = iskeynameExistInDictObj(dbDataObj, 'FKAsNFKTblsIndexesDataObj');
               if isFKAsNFKTblsIndexesDataObjExist == True :    
                  FKAsNFKTblsIndexesDataObj = dbDataObj['FKAsNFKTblsIndexesDataObj'];



               isFKTblsDataObjExist = iskeynameExistInDictObj(dbDataObj, 'FKTblsDataObj');
               if isFKTblsDataObjExist == True :    
                  FKTblsDataObj = dbDataObj['FKTblsDataObj'];

               isFKTblsAttrOptnDataObjExist = iskeynameExistInDictObj(dbDataObj, 'FKTblsAttrOptnDataObj');
               if isFKTblsAttrOptnDataObjExist == True :    
                  FKTblsAttrOptnDataObj = dbDataObj['FKTblsAttrOptnDataObj'];
      
               isFKTblsConstraintsDataObjExist = iskeynameExistInDictObj(dbDataObj, 'FKTblsConstraintsDataObj');
               if isFKTblsConstraintsDataObjExist == True :    
                  FKTblsConstraintsDataObj = dbDataObj['FKTblsConstraintsDataObj'];  
          
               isFKTblsIndexesDataObjExist = iskeynameExistInDictObj(dbDataObj, 'FKTblsIndexesDataObj');
               if isFKTblsIndexesDataObjExist == True :    
                  FKTblsIndexesDataObj = dbDataObj['FKTblsIndexesDataObj'];


               isAllTblsDataObjExist = iskeynameExistInDictObj(dbDataObj, 'allTblsDataObj');
               if isAllTblsDataObjExist == True :    
                  allTblsDataObj = dbDataObj['allTblsDataObj'];
            
               isFKConstraintsDataObjExist = iskeynameExistInDictObj(dbDataObj, 'fkConstraintsDataObj');
               if isFKConstraintsDataObjExist == True :    
                  fkConstraintsDataObj = dbDataObj['fkConstraintsDataObj'];

               isTriggersDataObjExist = iskeynameExistInDictObj(dbDataObj, 'triggersDataObj');
               if isTriggersDataObjExist == True :    
                  triggersDataObj = dbDataObj['triggersDataObj'];

 
               ### section related to nfk type tables ###
         
               for tblName in NFKTblsAttrOptnDataObj:

                   isDataAvailableInTbl = NFKTblsAttrOptnDataObj[tblName]['isDataAvailableInTbl'];

                   if iskeynameExistInDictObj(NFKTblsDataObj, tblName) == True :
                      NFKTblsDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                   if iskeynameExistInDictObj(NFKTblsIndexesDataObj, tblName) == True :
                      for indxName in NFKTblsIndexesDataObj[tblName]:
                          NFKTblsIndexesDataObj[tblName][indxName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                   if iskeynameExistInDictObj(allTblsDataObj, tblName) == True :
                      allTblsDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl;    
                   if iskeynameExistInDictObj(fkConstraintsDataObj, tblName) == True :
                      for FKName in fkConstraintsDataObj[tblName]:
                          fkConstraintsDataObj[tblName][FKName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                   if iskeynameExistInDictObj(triggersDataObj, tblName) == True :
                      for tgrName in triggersDataObj[tblName]:  
                          triggersDataObj[tblName][tgrName]['isDataAvailableInTbl'] = isDataAvailableInTbl;


               ### section related to fk as nfk type tables ###
         
               for tblName in FKAsNFKTblsAttrOptnDataObj:

                   isDataAvailableInTbl = FKAsNFKTblsAttrOptnDataObj[tblName]['isDataAvailableInTbl'];

                   if iskeynameExistInDictObj(FKAsNFKTblsDataObj, tblName) == True :
                      FKAsNFKTblsDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                   if iskeynameExistInDictObj(FKAsNFKTblsConstraintsDataObj, tblName) == True :
                      for FKName in FKAsNFKTblsConstraintsDataObj[tblName]:
                          FKAsNFKTblsConstraintsDataObj[tblName][FKName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                   if iskeynameExistInDictObj(FKAsNFKTblsIndexesDataObj, tblName) == True :
                      for indxName in FKAsNFKTblsIndexesDataObj[tblName]:
                          FKAsNFKTblsIndexesDataObj[tblName][indxName]['isDataAvailableInTbl'] = isDataAvailableInTbl;  
                   if iskeynameExistInDictObj(allTblsDataObj, tblName) == True :
                      allTblsDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl;    
                   if iskeynameExistInDictObj(fkConstraintsDataObj, tblName) == True :
                      for FKName in fkConstraintsDataObj[tblName]:  
                          fkConstraintsDataObj[tblName][FKName]['isDataAvailableInTbl'] = isDataAvailableInTbl; 
                   if iskeynameExistInDictObj(triggersDataObj, tblName) == True :
                      for tgrName in triggersDataObj[tblName]: 
                          triggersDataObj[tblName][tgrName]['isDataAvailableInTbl'] = isDataAvailableInTbl;


               ### section related to fk type tables ###
         
               for tblName in FKTblsAttrOptnDataObj:

                   isDataAvailableInTbl = FKTblsAttrOptnDataObj[tblName]['isDataAvailableInTbl'];

                   if iskeynameExistInDictObj(FKTblsDataObj, tblName) == True :
                      FKTblsDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                   if iskeynameExistInDictObj(FKTblsConstraintsDataObj, tblName) == True :
                      for FKName in FKTblsConstraintsDataObj[tblName]:
                          FKTblsConstraintsDataObj[tblName][FKName]['isDataAvailableInTbl'] = isDataAvailableInTbl;
                   if iskeynameExistInDictObj(FKTblsIndexesDataObj, tblName) == True :
                      for indxName in FKTblsIndexesDataObj[tblName]:
                          FKTblsIndexesDataObj[tblName][indxName]['isDataAvailableInTbl'] = isDataAvailableInTbl;  
                   if iskeynameExistInDictObj(allTblsDataObj, tblName) == True :
                      allTblsDataObj[tblName]['isDataAvailableInTbl'] = isDataAvailableInTbl;    
                   if iskeynameExistInDictObj(fkConstraintsDataObj, tblName) == True :
                      for FKName in fkConstraintsDataObj[tblName]: 
                          fkConstraintsDataObj[tblName][FKName]['isDataAvailableInTbl'] = isDataAvailableInTbl; 
                   if iskeynameExistInDictObj(triggersDataObj, tblName) == True :
                      for tgrName in triggersDataObj[tblName]:  
                          triggersDataObj[tblName][tgrName]['isDataAvailableInTbl'] = isDataAvailableInTbl;


               ### overwrite keys data ###

               infoSchemasDataObj[dbName]['NFKTblsDataObj'] = NFKTblsDataObj; 
               infoSchemasDataObj[dbName]['NFKTblsAttrOptnDataObj'] = NFKTblsAttrOptnDataObj;
               infoSchemasDataObj[dbName]['NFKTblsIndexesDataObj'] = NFKTblsIndexesDataObj;
               infoSchemasDataObj[dbName]['FKAsNFKTblsDataObj'] = FKAsNFKTblsDataObj;
               infoSchemasDataObj[dbName]['FKAsNFKTblsAttrOptnDataObj'] = FKAsNFKTblsAttrOptnDataObj;
               infoSchemasDataObj[dbName]['FKAsNFKTblsConstraintsDataObj'] = FKAsNFKTblsConstraintsDataObj;
               infoSchemasDataObj[dbName]['FKAsNFKTblsIndexesDataObj'] = FKAsNFKTblsIndexesDataObj;
               infoSchemasDataObj[dbName]['FKTblsDataObj'] = FKTblsDataObj;
               infoSchemasDataObj[dbName]['FKTblsAttrOptnDataObj'] = FKTblsAttrOptnDataObj;
               infoSchemasDataObj[dbName]['FKTblsConstraintsDataObj'] = FKTblsConstraintsDataObj;
               infoSchemasDataObj[dbName]['FKTblsIndexesDataObj'] = FKTblsIndexesDataObj; 
               infoSchemasDataObj[dbName]['allTblsDataObj'] = allTblsDataObj;
               infoSchemasDataObj[dbName]['fkConstraintsDataObj'] = fkConstraintsDataObj;
               infoSchemasDataObj[dbName]['triggersDataObj'] = triggersDataObj;
    
           
   
        if againstSvr == "SrcSvr":
           dstDbSvrInfoSchemasDataObj['schemasDataObj'] = infoSchemasDataObj;
        if againstSvr == "DstSvr":
           srcDbSvrInfoSchemasDataObj['schemasDataObj'] = infoSchemasDataObj;
 
    except Exception as e:
           handleProcsngAbtErrException("Y");


### handle processing to add missing key-value to dbs info schemas data ###

def handleProcsngToAddMissingKeyValueToDbsInfoSchemasObjBtwnSrcAndDstSvr(againstSvr):

    try:

        global inputArgsDataObj;
        infoSchemasDataObj = {}; 
        connectionTestedOnDbNameArr = [];
        isExtractDbNamesViaQry = 'N';
        dbSvrSchemaNamesConfigDataObj = getStoredDBSvrConfigData(againstSvr);
        dbHOST = dbSvrSchemaNamesConfigDataObj['dbHOST'];
        dbPORTNO = dbSvrSchemaNamesConfigDataObj['dbPORTNO'];
        dbUSER = dbSvrSchemaNamesConfigDataObj['dbUSER'];
        dbPASS = dbSvrSchemaNamesConfigDataObj['dbPASS'];
        dbBasedTypeStr = '';
        ntDbNamesStr = '';
        defaultKeysExistInInfoSchemasDbNameArr = [];


        if againstSvr == "DstSvr":

           global dstDbSvrInfoSchemasDataObj;

           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;
           if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
              infoSchemasDataObj['schemasDataObj'] = {};
           else :
                infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];
 
           dbBasedTypeStr = inputArgsDataObj['dstDbSvrDbType'];
           defaultKeysExistInInfoSchemasDbNameArr = list(infoSchemasDataObj.keys());
 
           if inputArgsDataObj['canUseSrcDbSvrDbNamesFurtherComparsionAgainstDstDbSvr'] == "N" :
              ntDbNamesStr = inputArgsDataObj['srcDbSvrDbName']; 
           if inputArgsDataObj['dstDbSvrDbNames'] != "all" :
              connectionTestedOnDbNameArr = inputArgsDataObj['dstDbSvrConTestedOnDbNameArr'];
           if inputArgsDataObj['dstDbSvrDbNames'] == "all" :
              isExtractDbNamesViaQry = 'Y';

       
        if isExtractDbNamesViaQry == 'Y' :
           connectionTestedOnDbNameArr = getDbSchemasNamesViaInfoSchemas(dbHOST,dbPORTNO,dbUSER,dbPASS,dbBasedTypeStr,ntDbNamesStr,'');  

           
        if len(connectionTestedOnDbNameArr) > 0 :
           defaultKeysNotExistInInfoSchemasDbNameArr = list(set(connectionTestedOnDbNameArr) - set(defaultKeysExistInInfoSchemasDbNameArr));
           if len(defaultKeysNotExistInInfoSchemasDbNameArr) > 0 :
              for dbName in defaultKeysNotExistInInfoSchemasDbNameArr :
                  infoSchemasDataObj[dbName] = {};
                  infoSchemasDataObj[dbName]['fkConstraintsDataObj'] = {};      
                  infoSchemasDataObj[dbName]['FKTblsNamesDataObj'] = {};
                  infoSchemasDataObj[dbName]['FKAsNFKTblsNamesDataObj'] = {};
                  infoSchemasDataObj[dbName]['indexesDataObj'] = {};
                  infoSchemasDataObj[dbName]['triggersDataObj'] = {};
                  infoSchemasDataObj[dbName]['routinesDataObj'] = {};
                  infoSchemasDataObj[dbName]['viewsDataObj'] = {};
                  infoSchemasDataObj[dbName]['allTblsDataObj'] = {};
                  infoSchemasDataObj[dbName]['tblsAttrOptnDataObj'] = {}; 
                  infoSchemasDataObj[dbName]['NFKTblsDataObj'] = {};
                  infoSchemasDataObj[dbName]['NFKTblsAttrOptnDataObj'] = {};
                  infoSchemasDataObj[dbName]['NFKTblsIndexesDataObj'] = {};
                  infoSchemasDataObj[dbName]['FKAsNFKTblsDataObj'] = {};
                  infoSchemasDataObj[dbName]['FKAsNFKTblsAttrOptnDataObj'] = {};  
                  infoSchemasDataObj[dbName]['FKAsNFKTblsConstraintsDataObj'] = {};
                  infoSchemasDataObj[dbName]['FKAsNFKTblsIndexesDataObj'] = {};
                  infoSchemasDataObj[dbName]['FKTblsDataObj'] = {};
                  infoSchemasDataObj[dbName]['FKTblsAttrOptnDataObj'] = {};  
                  infoSchemasDataObj[dbName]['FKTblsConstraintsDataObj'] = {};
                  infoSchemasDataObj[dbName]['FKTblsIndexesDataObj'] = {};
                  infoSchemasDataObj[dbName]['independentViewsDataObj'] = {};
                  infoSchemasDataObj[dbName]['InAsDependentViewsDataObj'] = {};
                  infoSchemasDataObj[dbName]['dependentViewsDataObj'] = {};

        if againstSvr == "DstSvr" :
           dstDbSvrInfoSchemasDataObj['schemasDataObj'].update(infoSchemasDataObj);  

    except Exception as e:
           handleProcsngAbtErrException("Y");



### segregate stored dbSchemas related to all views data as (independent, dependentAsIndependent, dependent) views ###

def segregateStoredInfoSchemasOfViewsCorrespondingIntoIVAndIVAsDVAndDViewsInfoSchemasData(againstSvr):

    try:

        infoSchemasDataObj = {};
        if againstSvr == "SrcSvr":
           global srcDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global dstDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;

        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];
 
        if len(infoSchemasDataObj)>0:
         
           for dbName in infoSchemasDataObj:

               outerViewsDataObj = {};
               innerViewsDataObj = {};  
               independentViewsDataObj = {};
               InAsDependentViewsDataObj = {};
               dependentViewsDataObj = {};
 
               isViewsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'viewsDataObj');
               if isViewsDataObjExist == True:
                  outerViewsDataObj = infoSchemasDataObj[dbName]['viewsDataObj'];
                  innerViewsDataObj = infoSchemasDataObj[dbName]['viewsDataObj'];


               ### Section to seperate views dbSchemas data ###

               if len(outerViewsDataObj)>0:
                  for outerViewName in outerViewsDataObj:
                      outerViewStmtStr = outerViewsDataObj[outerViewName]['updatedViewData'][2];
                      countOfInnerViewNameFoundInOuterViewStmStr = 0;
                      countOfOuterViewNameFoundInInnerViewStmStr = 0;     
                      for innerViewName in innerViewsDataObj:  
                          if outerViewName!=innerViewName:
                             innerViewStmtStr = innerViewsDataObj[innerViewName]['updatedViewData'][2];
                             findInnerViewNameInOuterVeiwStmtStr = "`"+innerViewName+"`";
                             findInnerViewNameInOuterVeiwStmtStrIndx = outerViewStmtStr.find(findInnerViewNameInOuterVeiwStmtStr);
                             findOuterViewNameInInnerVeiwStmtStr = "`"+outerViewName+"`";
                             findOuterViewNameInInnerVeiwStmtStrIndx = innerViewStmtStr.find(findOuterViewNameInInnerVeiwStmtStr); 
                             if findInnerViewNameInOuterVeiwStmtStrIndx>=0:
                                countOfInnerViewNameFoundInOuterViewStmStr = countOfInnerViewNameFoundInOuterViewStmStr + 1;
                             if findOuterViewNameInInnerVeiwStmtStrIndx>=0:
                                countOfOuterViewNameFoundInInnerViewStmStr = countOfOuterViewNameFoundInInnerViewStmStr + 1;

                      if countOfInnerViewNameFoundInOuterViewStmStr == 0 and countOfOuterViewNameFoundInInnerViewStmStr == 0:
                         independentViewsDataObj[outerViewName] = outerViewsDataObj[outerViewName];
                      elif countOfInnerViewNameFoundInOuterViewStmStr>0 and countOfOuterViewNameFoundInInnerViewStmStr==0:
                         dependentViewsDataObj[outerViewName] = outerViewsDataObj[outerViewName];  
                      else:
                          InAsDependentViewsDataObj[outerViewName] = outerViewsDataObj[outerViewName];  
                  
               ### section finally to store views dbschemas data details ###

               if againstSvr == "SrcSvr":
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['independentViewsDataObj'] = independentViewsDataObj;
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['InAsDependentViewsDataObj'] = InAsDependentViewsDataObj;
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['dependentViewsDataObj'] = dependentViewsDataObj;

               if againstSvr == "DstSvr":
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['independentViewsDataObj'] = independentViewsDataObj;
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['InAsDependentViewsDataObj'] = InAsDependentViewsDataObj;
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['dependentViewsDataObj'] = dependentViewsDataObj;
 

    except Exception as e:
           handleProcsngAbtErrException("Y");



### segregate stored dbSchemas related to NFK, fkActAsNFk, fk tables indexes data ###

def segregateStoredInfoSchemasOfIndexesCorrespondingIntoNFkAndFkActAsNFkAndFkIndexesInfoSchemasData(againstSvr):

    try:

        infoSchemasDataObj = {};
        if againstSvr == "SrcSvr":
           global srcDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global dstDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;

        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];

        if len(infoSchemasDataObj)>0:
         
           for dbName in infoSchemasDataObj:

               NFKTblsDataObj = {};
               FKAsNFKTblsDataObj = {};
               FKTblsDataObj = {};

               NFKTblsIndexesDataObj = {};
               FKAsNFKTblsIndexesDataObj = {};
               FKTblsIndexesDataObj = {};
               
               indexesDataObj = {};
 
               isNFKTblsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'NFKTblsDataObj');
               if isNFKTblsDataObjExist == True:
                  NFKTblsDataObj = infoSchemasDataObj[dbName]['NFKTblsDataObj'];

               isFKAsNFKTblsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'FKAsNFKTblsDataObj');
               if isFKAsNFKTblsDataObjExist == True:
                  FKAsNFKTblsDataObj = infoSchemasDataObj[dbName]['FKAsNFKTblsDataObj'];
 
               isFKTblsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'FKTblsDataObj');
               if isFKTblsDataObjExist == True:
                  FKTblsDataObj = infoSchemasDataObj[dbName]['FKTblsDataObj'];

               isIndexesDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'indexesDataObj');
               if isIndexesDataObjExist == True:
                  indexesDataObj = infoSchemasDataObj[dbName]['indexesDataObj'];


               ### Section to seperate indexes based on NFK, fkActAsNFk, fk table data ###
               if len(indexesDataObj)>0:
                  for tblName in indexesDataObj:

                      isNFKIndxTblNameExist = iskeynameExistInDictObj(NFKTblsDataObj, tblName);
                      if isNFKIndxTblNameExist == True:
                         NFKTblsIndexesDataObj[tblName] = indexesDataObj[tblName];

                      isFKAsNFKIndxTblNameExist = iskeynameExistInDictObj(FKAsNFKTblsDataObj, tblName);
                      if isFKAsNFKIndxTblNameExist == True:
                         FKAsNFKTblsIndexesDataObj[tblName] = indexesDataObj[tblName];   
 
                      isFkIndxTblNameExist = iskeynameExistInDictObj(FKTblsDataObj, tblName);
                      if isFkIndxTblNameExist == True:
                         FKTblsIndexesDataObj[tblName] = indexesDataObj[tblName];

                  
               ### section finally to store indexes dbschemas data details ### 

               if againstSvr == "SrcSvr":
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['NFKTblsIndexesDataObj'] = NFKTblsIndexesDataObj;
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKAsNFKTblsIndexesDataObj'] = FKAsNFKTblsIndexesDataObj;
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKTblsIndexesDataObj'] = FKTblsIndexesDataObj;
               if againstSvr == "DstSvr":
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['NFKTblsIndexesDataObj'] = NFKTblsIndexesDataObj;
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKAsNFKTblsIndexesDataObj'] = FKAsNFKTblsIndexesDataObj;
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKTblsIndexesDataObj'] = FKTblsIndexesDataObj;
 

    except Exception as e:
           handleProcsngAbtErrException("Y"); 



### segregate stored infoSchemas related to fk tables constraints data ###

def segregateStoredInfoSchemasOfFKTblsCorrespondingIntoFKAsNFKTblsConstraintsInfoSchemasData(againstSvr):

    try:

        infoSchemasDataObj = {};
        if againstSvr == "SrcSvr":
           global srcDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global dstDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;

        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];

        if len(infoSchemasDataObj)>0:

           for dbName in infoSchemasDataObj:

               FKTblsDataObj = {};
               fkConstraintsDataObj = {};
               FKTblsConstraintsDataObj = {};

               isFKTblsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'FKTblsDataObj');
               if isFKTblsDataObjExist == True:
                  FKTblsDataObj = infoSchemasDataObj[dbName]['FKTblsDataObj'];

               isFkConstraintsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'fkConstraintsDataObj');
               if isFkConstraintsDataObjExist == True:
                  fkConstraintsDataObj = infoSchemasDataObj[dbName]['fkConstraintsDataObj'];

               if len(fkConstraintsDataObj)>0:
                  for tblName in FKTblsDataObj:
                      isFkTblExists = iskeynameExistInDictObj(fkConstraintsDataObj, tblName);                          
                      if isFkTblExists == True:
                         FKTblsConstraintsDataObj[tblName] = fkConstraintsDataObj[tblName];

                     
               infoSchemasDataObj[dbName]['FKTblsConstraintsDataObj'] = FKTblsConstraintsDataObj;


           ### section finally to store dbschemas data details ### 

           if againstSvr == "SrcSvr":
              srcDbSvrInfoSchemasDataObj['schemasDataObj'] = infoSchemasDataObj;
           if againstSvr == "DstSvr":
              dstDbSvrInfoSchemasDataObj['schemasDataObj'] = infoSchemasDataObj;
               

    except Exception as e:
           handleProcsngAbtErrException("Y");



### segregate stored infoSchemas related to fkActAsNFk tables constraints data ###

def segregateStoredInfoSchemasOfFKAsNFKTblsCorrespondingIntoFKAsNFKTblsConstraintsInfoSchemasData(againstSvr):

    try:

        infoSchemasDataObj = {};
        if againstSvr == "SrcSvr":
           global srcDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global dstDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;

        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];

        if len(infoSchemasDataObj)>0:

           for dbName in infoSchemasDataObj:

               FKAsNFKTblsDataObj = {};
               fkConstraintsDataObj = {};
               FKAsNFKTblsConstraintsDataObj = {};

               isFKAsNFKTblsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'FKAsNFKTblsDataObj');
               if isFKAsNFKTblsDataObjExist == True:
                  FKAsNFKTblsDataObj = infoSchemasDataObj[dbName]['FKAsNFKTblsDataObj'];

               isFkConstraintsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'fkConstraintsDataObj');
               if isFkConstraintsDataObjExist == True:
                  fkConstraintsDataObj = infoSchemasDataObj[dbName]['fkConstraintsDataObj'];

               if len(fkConstraintsDataObj)>0:
                  for tblName in FKAsNFKTblsDataObj:
                      isFKAsNFKTblExists = iskeynameExistInDictObj(fkConstraintsDataObj, tblName);                          
                      if isFKAsNFKTblExists == True:
                         FKAsNFKTblsConstraintsDataObj[tblName] = fkConstraintsDataObj[tblName];

                    
               infoSchemasDataObj[dbName]['FKAsNFKTblsConstraintsDataObj'] = FKAsNFKTblsConstraintsDataObj;


           ### section finally to store dbschemas data details ### 

           if againstSvr == "SrcSvr":
              srcDbSvrInfoSchemasDataObj['schemasDataObj'] = infoSchemasDataObj;
           if againstSvr == "DstSvr":
              dstDbSvrInfoSchemasDataObj['schemasDataObj'] = infoSchemasDataObj;
               

    except Exception as e:
           handleProcsngAbtErrException("Y"); 
     


### segregate stored infoSchemas related to NFK, fkActAsNFk, fk tables data ###

def segregateStoredInfoSchemasOfTblsCorrespondingIntoNFkAndFkActAsNFkAndFKTblsInfoSchemasData(againstSvr):

    try:

        infoSchemasDataObj = {};
        if againstSvr == "SrcSvr":
           global srcDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global dstDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;

        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];

        if len(infoSchemasDataObj)>0:
         
           for dbName in infoSchemasDataObj:

               allTblsDataObj = {}; 
               NFKTblsDataObj = {};
               FKAsNFKTblsDataObj = {};
               FKTblsDataObj = {};
               FKAsNFKTblsNamesDataObj = {}; 
               FKTblsNamesDataObj = {};
               viewsDataObj = {};
               allTblsAttrOptnDataObj = {};
               NFKTblsAttrOptnDataObj = {};
               FKAsNFKTblsAttrOptnDataObj = {};
               FKTblsAttrOptnDataObj = {};  
 
               isAllTblsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'allTblsDataObj');
               if isAllTblsDataObjExist == True:
                  allTblsDataObj = infoSchemasDataObj[dbName]['allTblsDataObj'];

               isFKAsNFKTblsNamesDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'FKAsNFKTblsNamesDataObj');
               if isFKAsNFKTblsNamesDataObjExist == True:
                  FKAsNFKTblsNamesDataObj = infoSchemasDataObj[dbName]['FKAsNFKTblsNamesDataObj'];
 
               isFKTblsNamesDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'FKTblsNamesDataObj');
               if isFKTblsNamesDataObjExist == True:
                  FKTblsNamesDataObj = infoSchemasDataObj[dbName]['FKTblsNamesDataObj'];

               isViewsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'viewsDataObj');
               if isViewsDataObjExist == True:
                  viewsDataObj = infoSchemasDataObj[dbName]['viewsDataObj'];

               isAllTblsAttrOptnDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'allTblsAttrOptnDataObj');
               if isAllTblsAttrOptnDataObjExist == True:
                  allTblsAttrOptnDataObj = infoSchemasDataObj[dbName]['allTblsAttrOptnDataObj']; 


               ### Section to remove views table name from all tables infoSchemas data details ###                 
               if len(viewsDataObj)>0:  
                  for tblName in viewsDataObj:
                      isViewsTblNameExist = iskeynameExistInDictObj(allTblsDataObj, tblName);
                      if isViewsTblNameExist == True:
                         del allTblsDataObj[tblName];
                         
                
               ### Section to seperate fk table act as non-fk table from all tables infoSchemas data details ### 
               if len(FKAsNFKTblsNamesDataObj)>0:
                  for tblName in FKAsNFKTblsNamesDataObj:
                      isTblNameExistInAllTbls = iskeynameExistInDictObj(allTblsDataObj, tblName);
                      isTblNameExistInFKTbls = iskeynameExistInDictObj(FKTblsNamesDataObj, tblName);
                      if isTblNameExistInAllTbls == True and isTblNameExistInFKTbls == True:
                         FKAsNFKTblsDataObj[tblName] = allTblsDataObj[tblName];
                         FKAsNFKTblsAttrOptnDataObj[tblName] = allTblsAttrOptnDataObj[tblName]; 
                         del allTblsDataObj[tblName];
                         del allTblsAttrOptnDataObj[tblName];


               ### Section to seperate fk table from (non-fk, fk act as non-fk tables, all tables) infoSchemas data details ###
               if len(FKTblsNamesDataObj)>0:
                  for tblName in FKTblsNamesDataObj:
                      isTblNameExistInAllTbls = iskeynameExistInDictObj(allTblsDataObj, tblName);
                      isTblNameExistInFKAsNFKTbls = iskeynameExistInDictObj(FKAsNFKTblsNamesDataObj, tblName);
                      if isTblNameExistInAllTbls == True and isTblNameExistInFKAsNFKTbls == False:
                         FKTblsDataObj[tblName] = allTblsDataObj[tblName];
                         FKTblsAttrOptnDataObj[tblName] = allTblsAttrOptnDataObj[tblName];      
                         del allTblsDataObj[tblName];
                         del allTblsAttrOptnDataObj[tblName];


               ### section finally to store dbschemas data details ### 

               if againstSvr == "SrcSvr":
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['NFKTblsDataObj'] = allTblsDataObj;
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKAsNFKTblsDataObj'] = FKAsNFKTblsDataObj;
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKTblsDataObj'] = FKTblsDataObj;
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['viewsDataObj'] = viewsDataObj;
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['NFKTblsAttrOptnDataObj'] = allTblsAttrOptnDataObj;  
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKAsNFKTblsAttrOptnDataObj'] = FKAsNFKTblsAttrOptnDataObj;
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKTblsAttrOptnDataObj'] = FKTblsAttrOptnDataObj;

               if againstSvr == "DstSvr":
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['NFKTblsDataObj'] = allTblsDataObj;
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKAsNFKTblsDataObj'] = FKAsNFKTblsDataObj;
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKTblsDataObj'] = FKTblsDataObj;
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['viewsDataObj'] = viewsDataObj;
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['NFKTblsAttrOptnDataObj'] = allTblsAttrOptnDataObj;  
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKAsNFKTblsAttrOptnDataObj'] = FKAsNFKTblsAttrOptnDataObj;
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKTblsAttrOptnDataObj'] = FKTblsAttrOptnDataObj;   


    except Exception as e:
           handleProcsngAbtErrException("Y"); 



### store info schemas about collected all tbls attributes option data bwtn source and dst svr ###

def storeInfoSchemasAbtTblsAttrOptnBtwnSrcAndDstSvr(dataArrOfArr, againstSvr):

    try:

        infoSchemasDataObj = {};
        if againstSvr == "SrcSvr":
           global srcDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global dstDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;
     
        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];
 
        dataArrOfArrLen = len(dataArrOfArr);     
        for dataArrIndx in range(dataArrOfArrLen): 

            dataArr = list(dataArrOfArr[dataArrIndx]);
            dbName = dataArr[0];      
            dbTblName = dataArr[1];
            dbTblDataRowsCount = dataArr[8];
            isDataAvailableInTbl = 'N';
            isDataStoredIntoAssoArr = False;
            isDbNameExist = iskeynameExistInDictObj(infoSchemasDataObj, dbName);
            if dbTblDataRowsCount>0 : 
               isDataAvailableInTbl = 'Y';

            dbTblDataObj = {
               'isDataAvailableInTbl' : isDataAvailableInTbl,
               'updatedTblConfig': {}, 'updatedTblData': list(dataArr), 'orgTblData': list(dataArr), 
               'refTblDataObj': {'tblDefChangedDataArr': []}
            }; 
            
            if isDbNameExist == True:
               allTblsAttrOptnDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'allTblsAttrOptnDataObj');
               if allTblsAttrOptnDataObjExist == True:
                  isDbTblNameExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName]['allTblsAttrOptnDataObj'], dbTblName);
                  if isDbTblNameExist == False:
                     infoSchemasDataObj[dbName]['allTblsAttrOptnDataObj'][dbTblName] = dbTblDataObj;
                     isDataStoredIntoAssoArr = True;
               elif allTblsAttrOptnDataObjExist == False:
                    infoSchemasDataObj[dbName]['allTblsAttrOptnDataObj'] = {dbTblName: dbTblDataObj};
                    isDataStoredIntoAssoArr = True;
            elif isDbNameExist == False:
                 infoSchemasDataObj[dbName] = {};
                 infoSchemasDataObj[dbName]['allTblsAttrOptnDataObj'] = {dbTblName: dbTblDataObj};
                 isDataStoredIntoAssoArr = True;
        
 
            if isDataStoredIntoAssoArr == True:
               allTblsAttrOptnDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'allTblsAttrOptnDataObj');
               if allTblsAttrOptnDataObjExist == True:
                  allTblsAttrOptnDataObj = infoSchemasDataObj[dbName]['allTblsAttrOptnDataObj'];
                  if againstSvr == "SrcSvr":
                     srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['allTblsAttrOptnDataObj'] = allTblsAttrOptnDataObj;
                     srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['tblsAttrOptnDataObj'] = allTblsAttrOptnDataObj;
                  if againstSvr == "DstSvr":
                     dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['allTblsAttrOptnDataObj'] = allTblsAttrOptnDataObj;
                     dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['tblsAttrOptnDataObj'] = allTblsAttrOptnDataObj;
              

    except Exception as e:
           handleProcsngAbtErrException("Y");



### store info schemas about collected all tbls data bwtn source and destination svr ###

def storeInfoSchemasAbtTblsBtwnSrcAndDstSvr(dataArrOfArr, againstSvr):

    try:

        infoSchemasDataObj = {};
        if againstSvr == "SrcSvr":
           global srcDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global dstDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;
     
        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];
 
        dataArrOfArrLen = len(dataArrOfArr);     
        for dataArrIndx in range(dataArrOfArrLen): 

            dataArr = list(dataArrOfArr[dataArrIndx]);
            dbName = dataArr[0];      
            dbTblName = dataArr[1];
            dbTblColName = dataArr[2];
            isDataStoredIntoAssoArr = False;
            isDbNameExist = iskeynameExistInDictObj(infoSchemasDataObj, dbName);
            dbTblColDataObj = {
               'updatedColConfig': {}, 'updatedColData': list(dataArr), 'orgColData': list(dataArr), 
               'refColDataObj': {'colDefChangedDataArr': [], 'colDataTypeChangedDataArr': []}
            }; 
            dbTblDataObj = {
               'isDataAvailableInTbl' : 'N',
               'updatedTblConfig': {}, 
               'tblAllCols': {
                   dbTblColName: dbTblColDataObj
               }
            };
           
            if isDbNameExist == True:
               isAllTblsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'allTblsDataObj');
               if isAllTblsDataObjExist == True:
                  isDbTblNameExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName]['allTblsDataObj'], dbTblName);
                  if isDbTblNameExist == True:
                     infoSchemasDataObj[dbName]['allTblsDataObj'][dbTblName]['tblAllCols'][dbTblColName] = dbTblColDataObj;
                     isDataStoredIntoAssoArr = True;
                  elif isDbTblNameExist == False:
                       infoSchemasDataObj[dbName]['allTblsDataObj'][dbTblName] = dbTblDataObj;
                       isDataStoredIntoAssoArr = True;
               elif isAllTblsDataObjExist == False:
                    infoSchemasDataObj[dbName]['allTblsDataObj'] = {dbTblName: dbTblDataObj};
                    isDataStoredIntoAssoArr = True;
            elif isDbNameExist == False:
                 infoSchemasDataObj[dbName] = {};
                 infoSchemasDataObj[dbName]['allTblsDataObj'] = {dbTblName: dbTblDataObj};
                 isDataStoredIntoAssoArr = True;
        
 
            if isDataStoredIntoAssoArr == True:
               isAllTblsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'allTblsDataObj');
               if isAllTblsDataObjExist == True:
                  allTblsDataObj = infoSchemasDataObj[dbName]['allTblsDataObj'];  
                  if againstSvr == "SrcSvr":
                     srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['allTblsDataObj'] = allTblsDataObj;
                  if againstSvr == "DstSvr":
                     dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['allTblsDataObj'] = allTblsDataObj;
              

    except Exception as e:
           handleProcsngAbtErrException("Y");



### store info schemas about collected views data bwtn source and destination svr ###

def storeInfoSchemasAbtViewsDataBtwnSrcAndDstSvr(dataArrOfArr, againstSvr):

    try:

        dbHOST = "";
        dbPORTNO = "";
        dbUSER = "";
        dbPASS = ""; 
        infoSchemasDataObj = {};

        if againstSvr == "SrcSvr":
           global srcDbSvrConfigDataObj; 
           global srcDbSvrInfoSchemasDataObj;
           dbHOST = srcDbSvrConfigDataObj['dbHOST'];
           dbPORTNO = srcDbSvrConfigDataObj['dbPORTNO'];
           dbUSER = srcDbSvrConfigDataObj['dbUSER'];
           dbPASS = srcDbSvrConfigDataObj['dbPASS'];
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global dstDbSvrConfigDataObj;
           global dstDbSvrInfoSchemasDataObj;
           dbHOST = dstDbSvrConfigDataObj['dbHOST'];
           dbPORTNO = dstDbSvrConfigDataObj['dbPORTNO']; 
           dbUSER = dstDbSvrConfigDataObj['dbUSER'];
           dbPASS = dstDbSvrConfigDataObj['dbPASS'];
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;

        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];
 
        dataArrOfArrLen = len(dataArrOfArr);     
        for dataArrIndx in range(dataArrOfArrLen): 

            dataArr = list(dataArrOfArr[dataArrIndx]);
            dataArr[2] = "";
            viewDbQuery = "SHOW CREATE VIEW " + dataArr[0] + "." + dataArr[1];
            viewNameStructureDataArr = fetchDataFromDB(dbHOST, dbPORTNO, dbUSER, dbPASS, dataArr[0], viewDbQuery);
            if len(viewNameStructureDataArr)>0:
               dataArr[2] = str(viewNameStructureDataArr[0][1]).replace("\r", " ").replace("\n", " ").replace(" ", " ");

            dbName = dataArr[0];      
            dbViewName = dataArr[1];
            isDataStoredIntoAssoArr = False;
            isDbNameExist = iskeynameExistInDictObj(infoSchemasDataObj, dbName);
            vDataObj = {
               'isDataAvailableInTbl' : 'N', 
               'updatedViewConfig': {}, 'updatedViewData': list(dataArr), 'orgViewData': list(dataArr), 
               'refViewDataObj': {'viewNameDefChangedDataArr': []}
            };

            if isDbNameExist == True:
               isViewsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'viewsDataObj');
               if isViewsDataObjExist == True:
                  isDbViewNameExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName]['viewsDataObj'], dbViewName);
                  if isDbViewNameExist == False:
                     infoSchemasDataObj[dbName]['viewsDataObj'][dbViewName] = vDataObj;
                     isDataStoredIntoAssoArr = True;
               if isViewsDataObjExist == False:
                  infoSchemasDataObj[dbName]['viewsDataObj'] = {dbViewName: vDataObj};
                  isDataStoredIntoAssoArr = True;
            if isDbNameExist == False:
               infoSchemasDataObj[dbName] = {};
               infoSchemasDataObj[dbName]['viewsDataObj'] = {dbViewName: vDataObj};
               isDataStoredIntoAssoArr = True;
   

            if isDataStoredIntoAssoArr == True:
               viewsDataObj = infoSchemasDataObj[dbName]['viewsDataObj'];
               if againstSvr == "SrcSvr":
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['viewsDataObj'] = viewsDataObj;
               if againstSvr == "DstSvr":
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['viewsDataObj'] = viewsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");



### store info schemas about collected routines data bwtn source and destination svr ###

def storeInfoSchemasAbtRoutinesDataBtwnSrcAndDstSvr(dataArrOfArr, againstSvr):

    try:

        dbHOST = "";
        dbPORTNO = "";
        dbUSER = "";
        dbPASS = ""; 
        infoSchemasDataObj = {};

        if againstSvr == "SrcSvr":
           global srcDbSvrConfigDataObj; 
           global srcDbSvrInfoSchemasDataObj;
           dbHOST = srcDbSvrConfigDataObj['dbHOST'];
           dbPORTNO = srcDbSvrConfigDataObj['dbPORTNO'];
           dbUSER = srcDbSvrConfigDataObj['dbUSER'];
           dbPASS = srcDbSvrConfigDataObj['dbPASS'];
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global dstDbSvrConfigDataObj;
           global dstDbSvrInfoSchemasDataObj;
           dbHOST = dstDbSvrConfigDataObj['dbHOST'];
           dbPORTNO = dstDbSvrConfigDataObj['dbPORTNO'];
           dbUSER = dstDbSvrConfigDataObj['dbUSER'];
           dbPASS = dstDbSvrConfigDataObj['dbPASS'];
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;

        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];

        dataArrOfArrLen = len(dataArrOfArr);     
        for dataArrIndx in range(dataArrOfArrLen): 

            dataArr = list(dataArrOfArr[dataArrIndx]);
            
            dataArr[3] = "";
            dataArr[8] = str(dataArr[8]);
            routineDbQuery = "SHOW CREATE " + dataArr[1] + " " + dataArr[0] + "." + dataArr[2];
            routineStructureDataArr = fetchDataFromDB(dbHOST, dbPORTNO, dbUSER, dbPASS, dataArr[0], routineDbQuery);
            if len(routineStructureDataArr)>0:
               dataArr[3] = str(routineStructureDataArr[0][2]);

            dbName = dataArr[0];
            dbRoutineType = dataArr[1]; 
            dbRoutineName = dataArr[2]; 
            isDataStoredIntoAssoArr = False;   
            isDbNameExist = iskeynameExistInDictObj(infoSchemasDataObj, dbName);
            dbRoutineNameDataObj = {
               'updatedRnameConfig': {}, 'updatedRnameData': list(dataArr), 'orgRnameData': list(dataArr), 
               'refRnameDataObj': {'rnameDefChangedDataArr': []}
            };
            dbRoutineTypeDataObj = {
               'isDataAvailableInTbl' : 'N',
               'rTypeConfig': {}, 
               'rTypeAllRoutineNames': {
                   dbRoutineName: dbRoutineNameDataObj
               }
            }; 

            if isDbNameExist == True:
               isRoutinesDataObExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'routinesDataObj');
               if isRoutinesDataObExist == True:
                  isRoutineTypeExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName]['routinesDataObj'], dbRoutineType);
                  if isRoutineTypeExist == True:
                     rTypeAllRoutineNamesDataObj = infoSchemasDataObj[dbName]['routinesDataObj'][dbRoutineType]['rTypeAllRoutineNames'];
                     rTypeAllRoutineNamesDataObj[dbRoutineName] = dbRoutineNameDataObj;
                     infoSchemasDataObj[dbName]['routinesDataObj'][dbRoutineType]['rTypeAllRoutineNames'] = rTypeAllRoutineNamesDataObj;
                     isDataStoredIntoAssoArr = True;   
                  elif isRoutineTypeExist == False:  
                       infoSchemasDataObj[dbName]['routinesDataObj'][dbRoutineType] = dbRoutineTypeDataObj;
                       isDataStoredIntoAssoArr = True;
               elif isRoutinesDataObExist == False:
                    infoSchemasDataObj[dbName]['routinesDataObj'] = {dbRoutineType: dbRoutineTypeDataObj};
                    isDataStoredIntoAssoArr = True;
            elif isDbNameExist == False:
                 infoSchemasDataObj[dbName] = {};
                 infoSchemasDataObj[dbName]['routinesDataObj'] = {dbRoutineType: dbRoutineTypeDataObj};
                 isDataStoredIntoAssoArr = True;


            if isDataStoredIntoAssoArr == True:
               routinesDataObj = infoSchemasDataObj[dbName]['routinesDataObj'];
               if againstSvr == "SrcSvr":
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['routinesDataObj'] = routinesDataObj;
               if againstSvr == "DstSvr":
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['routinesDataObj'] = routinesDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");



### store info schemas about collected triggers data bwtn source and destination svr ###

def storeInfoSchemasAbtTriggersDataBtwnSrcAndDstSvr(dataArrOfArr, againstSvr):

    try:

        dbHOST = "";
        dbPORTNO = "";
        dbUSER = "";
        dbPASS = ""; 
        infoSchemasDataObj = {};

        if againstSvr == "SrcSvr":
           global srcDbSvrConfigDataObj; 
           global srcDbSvrInfoSchemasDataObj;
           dbHOST = srcDbSvrConfigDataObj['dbHOST'];
           dbPORTNO = srcDbSvrConfigDataObj['dbPORTNO'];
           dbUSER = srcDbSvrConfigDataObj['dbUSER'];
           dbPASS = srcDbSvrConfigDataObj['dbPASS'];
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global dstDbSvrConfigDataObj;
           global dstDbSvrInfoSchemasDataObj;
           dbHOST = dstDbSvrConfigDataObj['dbHOST'];
           dbPORTNO = dstDbSvrConfigDataObj['dbPORTNO']; 
           dbUSER = dstDbSvrConfigDataObj['dbUSER'];
           dbPASS = dstDbSvrConfigDataObj['dbPASS'];
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;

        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];

        dataArrOfArrLen = len(dataArrOfArr);     
        for dataArrIndx in range(dataArrOfArrLen): 

            dataArr = list(dataArrOfArr[dataArrIndx]);
            dataArr[5] = "";

            trigggerDbQuery = "SHOW CREATE TRIGGER " + dataArr[0] + "." + dataArr[2];
            triggerNameStructureDataArr = fetchDataFromDB(dbHOST, dbPORTNO, dbUSER, dbPASS, dataArr[0], trigggerDbQuery);
            if len(triggerNameStructureDataArr)>0:
               dataArr[5] = str(triggerNameStructureDataArr[0][2]);

            dbName = dataArr[0];      
            dbTblName = dataArr[1];
            dbTblTgrName = dataArr[2];
            isDataStoredIntoAssoArr = False;
            isDbNameExist = iskeynameExistInDictObj(infoSchemasDataObj, dbName);
            tgrDataObj = {
               'isDataAvailableInTbl' : 'N',
               'updatedTgrNameConfig': {}, 'updatedTgrNameData': list(dataArr), 'orgTgrNameData': list(dataArr), 
               'refTgrDataObj': {'tgrNameDefChangedDataArr': []}
            }; 

            if isDbNameExist == True:
               isTriggersDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'triggersDataObj');
               if isTriggersDataObjExist == True:
                  isDbTblNameExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName]['triggersDataObj'], dbTblName);
                  if isDbTblNameExist == True:
                     infoSchemasDataObj[dbName]['triggersDataObj'][dbTblName][dbTblTgrName] = tgrDataObj;
                  if isDbTblNameExist == False:
                     infoSchemasDataObj[dbName]['triggersDataObj'][dbTblName] = {dbTblTgrName: tgrDataObj};
                     isDataStoredIntoAssoArr = True;
               if isTriggersDataObjExist == False:
                  infoSchemasDataObj[dbName]['triggersDataObj'] = {dbTblName: {dbTblTgrName: tgrDataObj}};
                  isDataStoredIntoAssoArr = True;
            if isDbNameExist == False:
               infoSchemasDataObj[dbName] = {};
               infoSchemasDataObj[dbName]['triggersDataObj'] = {dbTblName: {dbTblTgrName: tgrDataObj}};
               isDataStoredIntoAssoArr = True;
   

            if isDataStoredIntoAssoArr == True:
               triggersDataObj = infoSchemasDataObj[dbName]['triggersDataObj'];
               if againstSvr == "SrcSvr":
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['triggersDataObj'] = triggersDataObj;
               if againstSvr == "DstSvr":
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['triggersDataObj'] = triggersDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");



### store info schemas about collected indexes data bwtn source and destination svr ###

def storeInfoSchemasAbtIndexesDataBtwnSrcAndDstSvr(dataArrOfArr, againstSvr):

    try:

        infoSchemasDataObj = {};

        if againstSvr == "SrcSvr":
           global srcDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global dstDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;

        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];
     
        dataArrOfArrLen = len(dataArrOfArr);     
        for dataArrIndx in range(dataArrOfArrLen): 

            dataArr = list(dataArrOfArr[dataArrIndx]);
            dataArr[7] = str(dataArr[7]).replace("\r", " ").replace("\n", " ").replace("        ", " ");
            dbName = dataArr[0];      
            dbTblName = dataArr[1];
            dbTblIndxName = dataArr[3];
            dbTblIndxType = dataArr[4];
            if dbTblIndxType == 0:
               dbTblIndxType = "UNIQUE";
            else: 
                dbTblIndxType = "";
            dbTblIndxColName = dataArr[6];  
            isDataStoredIntoAssoArr = False;
            isDbNameExist = iskeynameExistInDictObj(infoSchemasDataObj, dbName);
            dbTblIndexDataObj = {
                 'updatedIndxColConfig': {}, 'updatedIndxColData': list(dataArr), 'orgIndxColData': list(dataArr), 
                 'refIndxColDataObj': {'indxColDefChangedDataArr': []}
            };
            dbTblDataObj = {
               dbTblIndxName: {
                 'isDataAvailableInTbl' : 'N', 
                 'updatedIndxConfig': {},
                 'dbTblIndxType': dbTblIndxType,
                 'indxAllCols': {dbTblIndxColName: dbTblIndexDataObj}
               }
            };  

            if isDbNameExist == True:
               isIndxsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'indexesDataObj');
               if isIndxsDataObjExist == True:
                  isDbTblNameExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName]['indexesDataObj'], dbTblName);
                  if isDbTblNameExist == True:
                     isDbTblIndxNameExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName]['indexesDataObj'][dbTblName], dbTblIndxName);
                     if isDbTblIndxNameExist == False:
                        infoSchemasDataObj[dbName]['indexesDataObj'][dbTblName][dbTblIndxName] = dbTblDataObj[dbTblIndxName];
                        isDataStoredIntoAssoArr = True;
                     elif isDbTblIndxNameExist == True:
                          indxAllCols = infoSchemasDataObj[dbName]['indexesDataObj'][dbTblName][dbTblIndxName]['indxAllCols'];
                          indxAllCols[dbTblIndxColName] = dbTblIndexDataObj;
                          infoSchemasDataObj[dbName]['indexesDataObj'][dbTblName][dbTblIndxName]['indxAllCols'] = indxAllCols;
                          isDataStoredIntoAssoArr = True;  
                  elif isDbTblNameExist == False:
                        infoSchemasDataObj[dbName]['indexesDataObj'][dbTblName] = dbTblDataObj;
                        isDataStoredIntoAssoArr = True;
               elif isIndxsDataObjExist == False:
                     infoSchemasDataObj[dbName]['indexesDataObj'] = {dbTblName: dbTblDataObj};
                     isDataStoredIntoAssoArr = True; 
            elif isDbNameExist == False:
                 infoSchemasDataObj[dbName] = {};
                 infoSchemasDataObj[dbName]['indexesDataObj'] = {dbTblName: dbTblDataObj};
                 isDataStoredIntoAssoArr = True;


            if isDataStoredIntoAssoArr == True:
               indexesDataObj = infoSchemasDataObj[dbName]['indexesDataObj'];
               if againstSvr == "SrcSvr":
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['indexesDataObj'] = indexesDataObj;
               if againstSvr == "DstSvr":
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['indexesDataObj'] = indexesDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");



### store info schemas about collected FKAsNFK tables names data bwtn source and destination svr ###

def storeInfoSchemasAbtFKAsNFKTblsNamesDataBtwnSrcAndDstSvr(dataArrOfArr, againstSvr):

    try:

        infoSchemasDataObj = {};

        if againstSvr == "SrcSvr":
           global srcDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global dstDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;
       
        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];
     
        dataArrOfArrLen = len(dataArrOfArr);     
        for dataArrIndx in range(dataArrOfArrLen): 

            dataArr = list(dataArrOfArr[dataArrIndx]);
            dbName = dataArr[0];      
            dbTblName = dataArr[1];
            isDataStoredIntoAssoArr = False;
            isDbNameExist = iskeynameExistInDictObj(infoSchemasDataObj, dbName);

            if isDbNameExist == True:
               isFKAsNFKTblsNamesDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'FKAsNFKTblsNamesDataObj');
               if isFKAsNFKTblsNamesDataObjExist == True:
                  isDbTblNameExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName]['FKAsNFKTblsNamesDataObj'], dbTblName);
                  if isDbTblNameExist == False:
                     infoSchemasDataObj[dbName]['FKAsNFKTblsNamesDataObj'][dbTblName] = "";
                     isDataStoredIntoAssoArr = True;
               elif isFKAsNFKTblsNamesDataObjExist == False:
                    infoSchemasDataObj[dbName]['FKAsNFKTblsNamesDataObj'] = {dbTblName: ""};
                    isDataStoredIntoAssoArr = True;
            elif isDbNameExist == False:
                 infoSchemasDataObj[dbName] = {};
                 infoSchemasDataObj[dbName]['FKAsNFKTblsNamesDataObj'] = {dbTblName: ""};
                 isDataStoredIntoAssoArr = True;

            if isDataStoredIntoAssoArr == True:
               FKAsNFKTblsNamesDataObj = infoSchemasDataObj[dbName]['FKAsNFKTblsNamesDataObj'];
               if againstSvr == "SrcSvr":
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKAsNFKTblsNamesDataObj'] = FKAsNFKTblsNamesDataObj;
               if againstSvr == "DstSvr":
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKAsNFKTblsNamesDataObj'] = FKAsNFKTblsNamesDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


### store info schemas about collected fks tables names data bwtn source and destination svr ###

def storeInfoSchemasAbtFKTblsNamesDataBtwnSrcAndDstSvr(dataArrOfArr, againstSvr):

    try:

        infoSchemasDataObj = {};

        if againstSvr == "SrcSvr":
           global srcDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global dstDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;

        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];
     
        dataArrOfArrLen = len(dataArrOfArr);     
        for dataArrIndx in range(dataArrOfArrLen): 

            dataArr = list(dataArrOfArr[dataArrIndx]);
            dbName = dataArr[3];      
            dbTblName = dataArr[4];
            isDataStoredIntoAssoArr = False; 
            isDbNameExist = iskeynameExistInDictObj(infoSchemasDataObj, dbName)
        
            if isDbNameExist == True:
               isFKTblsNamesDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'FKTblsNamesDataObj');
               if isFKTblsNamesDataObjExist == True:
                  isDbTblNameExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName]['FKTblsNamesDataObj'], dbTblName);
                  if isDbTblNameExist == False:
                     infoSchemasDataObj[dbName]['FKTblsNamesDataObj'][dbTblName] = "";
                     isDataStoredIntoAssoArr = True;
               elif isFKTblsNamesDataObjExist == False:
                    infoSchemasDataObj[dbName]['FKTblsNamesDataObj'] = {dbTblName: ""};
                    isDataStoredIntoAssoArr = True;
            elif isDbNameExist == False:
                 infoSchemasDataObj[dbName] = {};
                 infoSchemasDataObj[dbName]['FKTblsNamesDataObj'] = {dbTblName: ""};
                 isDataStoredIntoAssoArr = True;

            if isDataStoredIntoAssoArr == True:
               FKTblsNamesDataObj = infoSchemasDataObj[dbName]['FKTblsNamesDataObj'];
               if againstSvr == "SrcSvr":
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKTblsNamesDataObj'] = FKTblsNamesDataObj;
               if againstSvr == "DstSvr":
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['FKTblsNamesDataObj'] = FKTblsNamesDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");



### store info schemas about collected all tables with all fks constraints data bwtn source and destination svr ###

def storeInfoSchemasAbtTblsFkConstraintsDataBtwnSrcAndDstSvr(dataArrOfArr, againstSvr):

    try:

        infoSchemasDataObj = {};

        if againstSvr == "SrcSvr":
           global srcDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = srcDbSvrInfoSchemasDataObj;
        if againstSvr == "DstSvr":
           global dstDbSvrInfoSchemasDataObj;
           infoSchemasDataObj = dstDbSvrInfoSchemasDataObj;

        if iskeynameExistInDictObj(infoSchemasDataObj, 'schemasDataObj') == False:
           infoSchemasDataObj['schemasDataObj'] = {};
        else :
             infoSchemasDataObj = infoSchemasDataObj['schemasDataObj'];
     
        dataArrOfArrLen = len(dataArrOfArr);     
        for dataArrIndx in range(dataArrOfArrLen): 

            dataArr = list(dataArrOfArr[dataArrIndx]);
            dbName = dataArr[3];      
            dbTblName = dataArr[4];
            dbTblFKName = dataArr[5];
            dbTblFkColName = dataArr[6]; 
            isDataStoredIntoAssoArr = False;
            isDbNameExist = iskeynameExistInDictObj(infoSchemasDataObj, dbName);
            dbTblFkColNameDataObj = {
              'updatedFKColNameConfig': {}, 'updatedFKColNameData': list(dataArr), 'orgFKColNameData': list(dataArr), 
              'refFkColNameDataObj': {'fkColNameDefChangedDataArr': []}
            };
            dbTblDataObj = {
               dbTblFKName: {
                 'isDataAvailableInTbl' : 'N',
                 'updatedFKNameConfig': {}, 
                 'fkAllCols': {
                     dbTblFkColName: dbTblFkColNameDataObj
                  }
               } 
            };

            if isDbNameExist == True:
               isFkConstraintsDataObjExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName], 'fkConstraintsDataObj');
               if isFkConstraintsDataObjExist == True:
                  isDbTblNameExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName]['fkConstraintsDataObj'], dbTblName);
                  if isDbTblNameExist == True:
                     isDbTblFKNameExist = iskeynameExistInDictObj(infoSchemasDataObj[dbName]['fkConstraintsDataObj'][dbTblName], dbTblFKName);
                     if isDbTblFKNameExist == True:
                        existAllColsDataObj = infoSchemasDataObj[dbName]['fkConstraintsDataObj'][dbTblName][dbTblFKName]['fkAllCols'];
                        existAllColsDataObj[dbTblFkColName] = dbTblFkColNameDataObj;
                        infoSchemasDataObj[dbName]['fkConstraintsDataObj'][dbTblName][dbTblFKName]['fkAllCols'] = existAllColsDataObj;
                        isDataStoredIntoAssoArr = True;
                     elif isDbTblFKNameExist == False:
                          infoSchemasDataObj[dbName]['fkConstraintsDataObj'][dbTblName][dbTblFKName] = dbTblDataObj[dbTblFKName];
                          isDataStoredIntoAssoArr = True;  
                  elif isDbTblNameExist == False:
                       infoSchemasDataObj[dbName]['fkConstraintsDataObj'][dbTblName] = dbTblDataObj;
                       isDataStoredIntoAssoArr = True;
               elif isFkConstraintsDataObjExist == False:
                    infoSchemasDataObj[dbName]['fkConstraintsDataObj'] = {dbTblName: dbTblDataObj};
                    isDataStoredIntoAssoArr = True;
            elif isDbNameExist == False:
                 infoSchemasDataObj[dbName] = {};
                 infoSchemasDataObj[dbName]['fkConstraintsDataObj'] = {dbTblName: dbTblDataObj};
                 isDataStoredIntoAssoArr = True;

            if isDataStoredIntoAssoArr == True:
               fkConstraintsDataObj = infoSchemasDataObj[dbName]['fkConstraintsDataObj'];
               if againstSvr == "SrcSvr":
                  srcDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['fkConstraintsDataObj'] = fkConstraintsDataObj;
               if againstSvr == "DstSvr":
                  dstDbSvrInfoSchemasDataObj['schemasDataObj'][dbName]['fkConstraintsDataObj'] = fkConstraintsDataObj;


    except Exception as e:
           handleProcsngAbtErrException("Y");


### get fk constraints name, column name, cols rules, tables infoSchemas data ###

def handleProcsngToGetInfoSchemasAbtForeignKeysConstraintsData(paramDataObj):

    dataArrOfArr = ();

    try:

        if len(paramDataObj)>0 :
           
           dcParamDataObj = copy.deepcopy(paramDataObj);   
           dataArrOfArr = getInfoSchemasData(dcParamDataObj);
           dataArrOfArr = list(dataArrOfArr);
           dataArrOfArrLen = len(dataArrOfArr);
           if dataArrOfArrLen>0: 
              dcParamDataObj['infoSchemasConfigDataObj'] = dcParamDataObj['fkColsRulesConstraints'];
              del dcParamDataObj['fkColsRulesConstraints'];
              for dataArrIndx in range(dataArrOfArrLen): 
                  dataArr = list(dataArrOfArr[dataArrIndx]);
                  dataArr.insert(8, "");
                  dataArr.insert(9, "");
                  dbName = "'" + dataArr[3] + "'";
                  tblName = "'" + dataArr[4] + "'";
                  FKName = "'" + dataArr[5] + "'";
                  dcParamDataObj['dbNamesStr'] = dbName;
                  dcParamDataObj['dbTblNamesStr'] = tblName;
                  dcParamDataObj['dbTblFKNamesStr'] = FKName;
                  dcParamDataObj['customSearchCondStr'] = '';
                  fkTblFKNameConstraintsRulesDataArrOfArr = getInfoSchemasData(dcParamDataObj);
                  if len(fkTblFKNameConstraintsRulesDataArrOfArr)>0:
                     dataArr[8] = fkTblFKNameConstraintsRulesDataArrOfArr[0][5];
                     dataArr[9] = fkTblFKNameConstraintsRulesDataArrOfArr[0][6];
                     dataArrOfArr[dataArrIndx] = tuple(dataArr);


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return dataArrOfArr;



### handle processing to extract setup information schemas data between srcSvr & dstSvr ###

def handleProcsngToExtractInfoSchemasDataBtwnSrcAndDstSvr(againstSvr):

   try:
     
       ### data extracting from global variable ###

       global inputArgsDataObj, infoSchemasWiseQryDataObj;
       canUseSrcDbSvrDbNamesFurtherComparsionAgainstDstDbSvr = inputArgsDataObj['canUseSrcDbSvrDbNamesFurtherComparsionAgainstDstDbSvr'];   
       ntSchemaNamesConfigDataObj = getDbSysLvlSchemaNamesConfigToNotIncludeInComparsion();
       sysSchemaNamesRegexExpStr = ntSchemaNamesConfigDataObj['sysSchemaNamesRegexExpStr'];
       ntSysSchemasNamesStr = ntSchemaNamesConfigDataObj['ntSysSchemasNamesStr'];
 
       ### local variable declare ###

       dbHOST = "";
       dbPORTNO = "";
       dbUSER = "";
       dbPASS = "";
       dbSvrDbType = "";
       dbNamesStr = "";
       ntDbNamesStr = "";
    
       ### section about source server details ###

       if againstSvr == "SrcSvr":
          global srcDbSvrConfigDataObj;
          dbHOST = srcDbSvrConfigDataObj['dbHOST'];
          dbPORTNO = srcDbSvrConfigDataObj['dbPORTNO'];
          dbUSER = srcDbSvrConfigDataObj['dbUSER'];
          dbPASS = srcDbSvrConfigDataObj['dbPASS'];
          dbSvrDbType = inputArgsDataObj['srcDbSvrDbType'];
          dbNamesStr = inputArgsDataObj['srcDbSvrDbName'];
          
       ### section about destination server details ###
   
       if againstSvr == "DstSvr":
          global dstDbSvrConfigDataObj;
          dbHOST = dstDbSvrConfigDataObj['dbHOST'];
          dbPORTNO = dstDbSvrConfigDataObj['dbPORTNO'];
          dbUSER = dstDbSvrConfigDataObj['dbUSER'];
          dbPASS = dstDbSvrConfigDataObj['dbPASS'];
          dbSvrDbType = inputArgsDataObj['dstDbSvrDbType'];
          dbNamesStr = inputArgsDataObj['dstDbSvrDbNames'];
          if dbNamesStr == "all" :
             dbNamesStr = "";   
          if canUseSrcDbSvrDbNamesFurtherComparsionAgainstDstDbSvr == "N" :
             ntDbNamesStr = inputArgsDataObj['srcDbSvrDbName'];
          

       dbNamesStr = getStringWrappedBySingleQuotes(dbNamesStr);
       ntDbNamesStr = getStringWrappedBySingleQuotes(ntDbNamesStr);
 
       ### section abt get comparsion category data details ###
       
       cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj'];
       cmpCtgryNoStr = int(cmpCtgryDataObj['cmpCtgryNo']);
       
       ### parameter sending variable declare ###

       paramDataObj = {};
       paramDataObj['dbHOST'] = dbHOST;
       paramDataObj['dbPORTNO'] = dbPORTNO;
       paramDataObj['dbUSER'] = dbUSER;
       paramDataObj['dbPASS'] = dbPASS;
       paramDataObj['dbNAME'] = '';
       paramDataObj['ntSysSchemasNamesStr'] = ntSysSchemasNamesStr;
       paramDataObj['sysSchemaNamesRegexExpStr'] = sysSchemaNamesRegexExpStr;
       paramDataObj['dbBasedTypeStr'] = dbSvrDbType;
       paramDataObj['ntDbNamesStr'] = ntDbNamesStr;
       paramDataObj['dbNamesStr'] = dbNamesStr;
       paramDataObj['dbTblNamesStr'] = cmpCtgryDataObj['dbTblNamesStr'];
       paramDataObj['dbTblColNamesStr'] = cmpCtgryDataObj['dbTblColNamesStr'];
       paramDataObj['dbTblIndxNamesStr'] = cmpCtgryDataObj['dbTblIndxNamesStr'];
       paramDataObj['dbTblFKNamesStr'] = cmpCtgryDataObj['dbTblFKNamesStr'];
       paramDataObj['dbTblTgrNamesStr'] = cmpCtgryDataObj['dbTblTgrNamesStr'];
       paramDataObj['dbRoutineNamesStr'] = cmpCtgryDataObj['dbRoutineNamesStr'];
       paramDataObj['dbViewNamesStr'] = cmpCtgryDataObj['dbViewNamesStr'];
       paramDataObj['customSearchCondStr'] = ''; 
       paramDataObj['infoSchemasConfigDataObj'] = {};

   
       ### Section abt tables attributes options information schemas details ###

       if (cmpCtgryNoStr in [1, 2, 4, 5, 9]) == True :
          paramDataObj['infoSchemasConfigDataObj'] = infoSchemasWiseQryDataObj['allTblsAttrOptns'];
          allDbTblsAttrOptnSchemasDataArr = getInfoSchemasData(paramDataObj);
          allDbTblsAttrOptnSchemasDataArrLen = len(allDbTblsAttrOptnSchemasDataArr);
          if allDbTblsAttrOptnSchemasDataArrLen > 0:
             storeInfoSchemasAbtTblsAttrOptnBtwnSrcAndDstSvr(allDbTblsAttrOptnSchemasDataArr, againstSvr);


       ### Section abt tables with columns information schemas details ###

       if (cmpCtgryNoStr in [2, 3, 4, 5, 9]) == True :
          if "3" in cmpCtgryDataObj['customSearchCondStrForCmptCtgryNoArr'] :
             paramDataObj['customSearchCondStr'] = cmpCtgryDataObj['customSearchCondStr'];
          paramDataObj['infoSchemasConfigDataObj'] = infoSchemasWiseQryDataObj['allTbls'];
          allDbTblsSchemasDataArr = getInfoSchemasData(paramDataObj); 
          allDbTblsSchemasDataArrLen = len(allDbTblsSchemasDataArr);
          paramDataObj['customSearchCondStr'] = '';
          if allDbTblsSchemasDataArrLen > 0:
             storeInfoSchemasAbtTblsBtwnSrcAndDstSvr(allDbTblsSchemasDataArr, againstSvr);


       ### Section abt table indexes information schemas details ###
       
       if (cmpCtgryNoStr in [2, 4, 5, 9]) == True :
          if "4" in cmpCtgryDataObj['customSearchCondStrForCmptCtgryNoArr'] :
             paramDataObj['customSearchCondStr'] = cmpCtgryDataObj['customSearchCondStr'];
          paramDataObj['infoSchemasConfigDataObj'] = infoSchemasWiseQryDataObj['indexes'];
          indxDbSchemasDataArr = getInfoSchemasData(paramDataObj); 
          indxDbSchemasDataArrLen = len(indxDbSchemasDataArr);
          paramDataObj['customSearchCondStr'] = ''; 
          if indxDbSchemasDataArrLen > 0:
             storeInfoSchemasAbtIndexesDataBtwnSrcAndDstSvr(indxDbSchemasDataArr, againstSvr); 
     

       ### Section abt table foreigns keys constraints information schemas details ###

       if (cmpCtgryNoStr in [2, 4, 5, 9]) == True :
          if "5" in cmpCtgryDataObj['customSearchCondStrForCmptCtgryNoArr'] :
             paramDataObj['customSearchCondStr'] = cmpCtgryDataObj['customSearchCondStr'];
          paramDataObj['infoSchemasConfigDataObj'] = infoSchemasWiseQryDataObj['fkConstraints'];
          paramDataObj['fkColsRulesConstraints'] = infoSchemasWiseQryDataObj['fkColsRulesConstraints'];
          fkDbSchemasDataArr = handleProcsngToGetInfoSchemasAbtForeignKeysConstraintsData(paramDataObj);
          fkDbSchemasDataArrLen = len(fkDbSchemasDataArr);
          paramDataObj['customSearchCondStr'] = '';
          if fkDbSchemasDataArrLen > 0:
             storeInfoSchemasAbtTblsFkConstraintsDataBtwnSrcAndDstSvr(fkDbSchemasDataArr, againstSvr);
             storeInfoSchemasAbtFKTblsNamesDataBtwnSrcAndDstSvr(fkDbSchemasDataArr, againstSvr);
             storeInfoSchemasAbtFKAsNFKTblsNamesDataBtwnSrcAndDstSvr(fkDbSchemasDataArr, againstSvr);
            

       ### Section abt table triggers information schemas details ###

       if (cmpCtgryNoStr in [6, 9]) == True :
          if "6" in cmpCtgryDataObj['customSearchCondStrForCmptCtgryNoArr'] :
             paramDataObj['customSearchCondStr'] = cmpCtgryDataObj['customSearchCondStr'];  
          paramDataObj['infoSchemasConfigDataObj'] = infoSchemasWiseQryDataObj['triggers'];
          triggersDbSchemasDataArr = getInfoSchemasData(paramDataObj);   
          triggersDbSchemasDataArrLen = len(triggersDbSchemasDataArr);
          paramDataObj['customSearchCondStr'] = '';
          if triggersDbSchemasDataArrLen > 0:
             storeInfoSchemasAbtTriggersDataBtwnSrcAndDstSvr(triggersDbSchemasDataArr, againstSvr);
             
             
       ### Section abt routines information schemas details ###

       if (cmpCtgryNoStr in [7, 9]) == True :
          paramDataObj['infoSchemasConfigDataObj'] = infoSchemasWiseQryDataObj['routines'];
          routinesDbSchemasDataArr = getInfoSchemasData(paramDataObj);
          routinesDbSchemasDataArrLen = len(routinesDbSchemasDataArr);
          paramDataObj['customSearchCondStr'] = '';
          if routinesDbSchemasDataArrLen > 0:
             storeInfoSchemasAbtRoutinesDataBtwnSrcAndDstSvr(routinesDbSchemasDataArr, againstSvr);

 
       ### Section abt views information schemas details ###

       if (cmpCtgryNoStr in [8, 9]) == True :
          paramDataObj['infoSchemasConfigDataObj'] = infoSchemasWiseQryDataObj['views'];
          viewsDbSchemasDataArr = getInfoSchemasData(paramDataObj);
          viewsDbSchemasDataArrLen = len(viewsDbSchemasDataArr);
          paramDataObj['customSearchCondStr'] = '';   
          if viewsDbSchemasDataArrLen > 0:
             storeInfoSchemasAbtViewsDataBtwnSrcAndDstSvr(viewsDbSchemasDataArr, againstSvr);
           
   
       ### section abt to segregate stored all tables infoSchemas ###
       ## corresponding into nFk, FKAsNFK, FK types tables infoSchemas details ###

       segregateStoredInfoSchemasOfTblsCorrespondingIntoNFkAndFkActAsNFkAndFKTblsInfoSchemasData(againstSvr);

       ### section abt to store infoSchemas about fsAsNFk tables columns constraint rules data ###

       segregateStoredInfoSchemasOfFKAsNFKTblsCorrespondingIntoFKAsNFKTblsConstraintsInfoSchemasData(againstSvr);
  
       ### section abt to store infoSchemas about fk tables columns constraint rules data ###

       segregateStoredInfoSchemasOfFKTblsCorrespondingIntoFKAsNFKTblsConstraintsInfoSchemasData(againstSvr);
             
       ### section abt to segregate stored all indexes infoSchemas ###
       ### corresponding into nFk, FKAsNFK, FK types tables infoSchemas details ###

       segregateStoredInfoSchemasOfIndexesCorrespondingIntoNFkAndFkActAsNFkAndFkIndexesInfoSchemasData(againstSvr);

       ### section abt to segregate stored views infoSchemas corresponding ###
       ### into idependent, independentAsDependent, dependent views infoSchemas details ###

       segregateStoredInfoSchemasOfViewsCorrespondingIntoIVAndIVAsDVAndDViewsInfoSchemasData(againstSvr);


   except Exception as e:
          handleProcsngAbtErrException("Y");

   


### handle processing to store all info db schemas name btwn src and dst svr
### collect all uniq dbNames between srcSvr and dstSvr and storing as arr format
### collect all uniq dbNames from srcSvr and storing as arr format
### collect all uniq dbNames from dstSvr and storing as arr format
### overwrite data into collected input arguments corresponding keys

def handleProcsngToStoreAllInfoSchemaNameBtwnSrcAndDstSvr():

    try:

       global inputArgsDataObj;

       inputArgsDataObj['srcDbSvrSetupInfoSchemaNameArr'] = getDbSchemasNamesViaInfoSchemas(
            inputArgsDataObj['srcDbSvrHostName'], inputArgsDataObj['srcDbSvrPortNo'], inputArgsDataObj['srcDbSvrUserName'],
            inputArgsDataObj['srcDbSvrPwd'], inputArgsDataObj['srcDbSvrDbType'], '', ''
       );

       inputArgsDataObj['dstDbSvrSetupInfoSchemaNameArr'] = getDbSchemasNamesViaInfoSchemas(
            inputArgsDataObj['dstDbSvrHostName'], inputArgsDataObj['dstDbSvrPortNo'], inputArgsDataObj['dstDbSvrUserName'],
            inputArgsDataObj['dstDbSvrPwd'], inputArgsDataObj['dstDbSvrDbType'], '', ''
       );

       if len(inputArgsDataObj['srcDbSvrSetupInfoSchemaNameArr'])>0 and len(inputArgsDataObj['dstDbSvrSetupInfoSchemaNameArr'])>0 :
          inputArgsDataObj['uniqInfoSchemaNameArrBtwnSrcAndDstDbSvr'] = list(set(
               inputArgsDataObj['srcDbSvrSetupInfoSchemaNameArr'] + inputArgsDataObj['dstDbSvrSetupInfoSchemaNameArr']
          ));


    except Exception as e:
          handleProcsngAbtErrException("Y");


### store system global variables info data btwn src and dst server details ###

def storeSysGblVblsInfoDataBtwnSrcAndDstSvr():

    try:

       global dstDbSvrInfoSchemasDataObj, dstDbSvrInfoSchemasDataObj;       
       srcDbSvrSystemGlobalVariablesInfoDataObj = srcDbSvrInfoSchemasDataObj['sysGlobalVariablesDataObj'];
       dstDbSvrSystemGlobalVariablesInfoDataObj = dstDbSvrInfoSchemasDataObj['sysGlobalVariablesDataObj'];
       dbQUERY = """SELECT * FROM INFORMATION_SCHEMA.GLOBAL_VARIABLES"""; 
 

       ### handle case for source server ###

       if inputArgsDataObj['srcDbSvrHostName']!="":
          dataArrOfArr1 = fetchDataFromDB(
              inputArgsDataObj['srcDbSvrHostName'], inputArgsDataObj['srcDbSvrPortNo'], inputArgsDataObj['srcDbSvrUserName'], 
              inputArgsDataObj['srcDbSvrPwd'], '', dbQUERY
          ); 
          dataArrOfArr1 = list(dataArrOfArr1);
          dataArrOfArrLen1 = len(dataArrOfArr1);
          if dataArrOfArrLen1>0:   
              for dataArrIndx in range(dataArrOfArrLen1): 
                  dataArr = list(dataArrOfArr1[dataArrIndx]);
                  srcDbSvrSystemGlobalVariablesInfoDataObj[dataArr[0]] = dataArr[1];


       ### handle case for destination server, when source server hostname is same as destination server hostname ###

       if inputArgsDataObj['srcDbSvrHostName']!="" and inputArgsDataObj['dstDbSvrHostName']!="" and inputArgsDataObj['srcDbSvrHostName']==inputArgsDataObj['dstDbSvrHostName']:

          dstDbSvrSystemGlobalVariablesInfoDataObj = srcDbSvrSystemGlobalVariablesInfoDataObj;

      
       ### handle case for destination server, when source server hostname is different ###

       if inputArgsDataObj['srcDbSvrHostName']!=inputArgsDataObj['dstDbSvrHostName']:
          dataArrOfArr2 = fetchDataFromDB(
             inputArgsDataObj['dstDbSvrHostName'], inputArgsDataObj['dstDbSvrPortNo'], inputArgsDataObj['dstDbSvrUserName'], 
             inputArgsDataObj['dstDbSvrPwd'], '', dbQUERY
          ); 
          dataArrOfArr2 = list(dataArrOfArr2);
          dataArrOfArrLen2 = len(dataArrOfArr2);
          if dataArrOfArrLen2>0:   
              for dataArrIndx in range(dataArrOfArrLen2): 
                  dataArr = list(dataArrOfArr2[dataArrIndx]);
                  dstDbSvrSystemGlobalVariablesInfoDataObj[dataArr[0]] = dataArr[1];   


       ### finally overwrite collected input arguments into corresponding keys data ###

       srcDbSvrInfoSchemasDataObj['sysGlobalVariablesDataObj'] = srcDbSvrSystemGlobalVariablesInfoDataObj;
       dstDbSvrInfoSchemasDataObj['sysGlobalVariablesDataObj'] = dstDbSvrSystemGlobalVariablesInfoDataObj;      


    except Exception as e:
           handleProcsngAbtErrException("Y");


### configure destination server db name exist or not status ###

def configureDstDbSvrDbNameExistStatus():

    try:
     
        global inputArgsDataObj;
        global dstDbSvrConfigDataObj;
        isSrcDbSvrDbNameExist = inputArgsDataObj['isSrcDbSvrDbNameExist'];
        dstDbSvrDbNames = inputArgsDataObj['dstDbSvrDbNames'];
        isDstDbSvrDbNameExist = inputArgsDataObj['isDstDbSvrDbNameExist'];

        if isSrcDbSvrDbNameExist == "Y":
           if dstDbSvrDbNames != "all":
              # split the string based on commas (",")
              dbNamesArr = dstDbSvrDbNames.split(",");
              dbNamesArrLength = len(dbNamesArr);
              countOfDbNameExist = 0; 
              for dbNameIndex in range(dbNamesArrLength):
                  eachDbName = dbNamesArr[dbNameIndex];
                  dbHOST = dstDbSvrConfigDataObj['dbHOST'];
                  dbPORTNO = dstDbSvrConfigDataObj['dbPORTNO'];
                  dbUSER = dstDbSvrConfigDataObj['dbUSER'];
                  dbPASS = dstDbSvrConfigDataObj['dbPASS'];
                  isDbNameExist = isDbConnectionLinkCanOpen(dbHOST, dbPORTNO, dbUSER, dbPASS, eachDbName);            
                  if isDbNameExist == "Y":
                     inputArgsDataObj['dstDbSvrConTestedOnDbNameArr'].append(eachDbName);
                     countOfDbNameExist = countOfDbNameExist + 1; 
              if dbNamesArrLength == countOfDbNameExist:
                 isDstDbSvrDbNameExist = "Y";
              else:
                   isDstDbSvrDbNameExist = "N";   
           if dstDbSvrDbNames == "all":
              isDstDbSvrDbNameExist = "Y";
    

           if isDstDbSvrDbNameExist == "N":
              msgStr = "\n";
              msgStr+= dstDbSvrDbNames + " DB not exist on 'DESTINATION' server.";
              msgStr+= "\n";
              displayMsg('', msgStr);
              sys.exit();
           else:
               inputArgsDataObj['isDstDbSvrDbNameExist'] = 'Y';
            
   
    except Exception as e:
           handleProcsngAbtErrException("Y");
 


### configure source server db name exist or not status ###

def configureSrcDbSvrDbNameExistStatus():
 
    try:
        
        global inputArgsDataObj;
        global srcDbSvrConfigDataObj;
        srcDbSvrDbName = inputArgsDataObj['srcDbSvrDbName'];
        isSrcDbSvrDbNameExist = inputArgsDataObj['isSrcDbSvrDbNameExist'];

        dbHOST = srcDbSvrConfigDataObj['dbHOST'];
        dbPORTNO = srcDbSvrConfigDataObj['dbPORTNO'];
        dbUSER = srcDbSvrConfigDataObj['dbUSER'];
        dbPASS = srcDbSvrConfigDataObj['dbPASS'];
        isSrcDbSvrDbNameExist = isDbConnectionLinkCanOpen(dbHOST, dbPORTNO, dbUSER, dbPASS, srcDbSvrDbName);

        if isSrcDbSvrDbNameExist == "N":
           msgStr = "\n";
           msgStr+= srcDbSvrDbName + " DB not exist on 'SOURCE' server.";
           msgStr+= "\n";
           displayMsg('', msgStr);
           sys.exit();
        else:
            inputArgsDataObj['isSrcDbSvrDbNameExist'] = 'Y'; 


    except Exception as e:
           handleProcsngAbtErrException("Y");


 
### store source & destination server db configuration details ###

def storeDbSvrConfigDetails():

    try:

         global inputArgsDataObj;
         global srcDbSvrConfigDataObj;
         global dstDbSvrConfigDataObj;
         
         srcDbSvrConfigDataObj['dbHOST'] = inputArgsDataObj['srcDbSvrHostName'];
         srcDbSvrConfigDataObj['dbPORTNO'] = inputArgsDataObj['srcDbSvrPortNo']; 
         srcDbSvrConfigDataObj['dbUSER'] = inputArgsDataObj['srcDbSvrUserName'];
         srcDbSvrConfigDataObj['dbPASS'] = inputArgsDataObj['srcDbSvrPwd'];
   
         dstDbSvrConfigDataObj['dbHOST'] = inputArgsDataObj['dstDbSvrHostName'];
         dstDbSvrConfigDataObj['dbPORTNO'] = inputArgsDataObj['dstDbSvrPortNo'];
         dstDbSvrConfigDataObj['dbUSER'] = inputArgsDataObj['dstDbSvrUserName'];
         dstDbSvrConfigDataObj['dbPASS'] = inputArgsDataObj['dstDbSvrPwd'];
         

    except Exception as e:
           handleProcsngAbtErrException("Y"); 


### display wait messages before diff db comparsion ###

def displayWaitMsgB4ProcsngDiffDbCmp():

    try:

        msgStr = "\n";
        msgStr+= "Wait till script finish DB comparsion based on given details ...";
        msgStr+= "\n";
        displayMsg('', msgStr);

    except Exception as e:
           handleProcsngAbtErrException("Y");


### handle processing diff db comparsion ###
### between source and destination server ###

def handleProcsngDiffDbComparsionBtwnSrcAndDstSvr():

  try:
      
      displayWaitMsgB4ProcsngDiffDbCmp();
      storeDbSvrConfigDetails();
      configureSrcDbSvrDbNameExistStatus();
      configureDstDbSvrDbNameExistStatus();
      # storeSysGblVblsInfoDataBtwnSrcAndDstSvr();
      handleProcsngToStoreAllInfoSchemaNameBtwnSrcAndDstSvr();
      handleProcsngToExtractInfoSchemasDataBtwnSrcAndDstSvr('SrcSvr');
      handleProcsngToExtractInfoSchemasDataBtwnSrcAndDstSvr('DstSvr');
      handleProcsngToAddMissingKeyValueToDbsInfoSchemasObjBtwnSrcAndDstSvr('DstSvr');
      handleProcsngToUpdateKeyValueOfDbsInfoSchemasObjBtwnSrcAndDstSvr('SrcSvr');
      handleProcsngToUpdateKeyValueOfDbsInfoSchemasObjBtwnSrcAndDstSvr('DstSvr');
      handleProcsngDBLvlSchmsCmpBtwnSrcAndDstSvr();
      handleProcsngExecuteDiffDBChangesBtwnSrcAndDstSvr();
      displayDiffDBCmpSummaryReport();

 
  except Exception as e:
         handleProcsngAbtErrException("Y");


### display error msg related to not given proper inputs arguments ###

def displayErrMsgAbtWrngInputsArguments(msgDataArr):

    try:
       
        if len(msgDataArr)>0:
           displayMsg('', '\n');
           for msgStr in msgDataArr:
               displayMsg('', msgStr);
           displayMsg('', '\n');

    except Exception as e:
           handleProcsngAbtErrException("Y");


### validate accepted input arguments ###

def validateInputArgsBasedOnEnvironmentType():
 
   statusDataObj = {};
   statusDataObj['isValidInputArgCollected'] = False;
   statusDataObj['msgArr'] = [];

   try:

      global inputArgsDataObj;
      countOfInvalidInputArg = 0;
      isInvalidCmpCtgryData = 'Y'; 
       
      ### Section abt source server details ###
      
      if inputArgsDataObj['srcDbSvrHostName'] == "":
         statusDataObj['msgArr'].append("Enter source server DB host name");
         countOfInvalidInputArg = countOfInvalidInputArg + 1;
      if inputArgsDataObj['srcDbSvrPortNo'] == "":
         statusDataObj['msgArr'].append("Enter source server DB host port no");
         countOfInvalidInputArg = countOfInvalidInputArg + 1;
      if inputArgsDataObj['srcDbSvrUserName'] == "":
         statusDataObj['msgArr'].append("Enter source server DB username"); 
         countOfInvalidInputArg = countOfInvalidInputArg + 1;
      if inputArgsDataObj['srcDbSvrPwd'] == "":
         statusDataObj['msgArr'].append("Enter source server DB password"); 
         countOfInvalidInputArg = countOfInvalidInputArg + 1;
      if inputArgsDataObj['srcDbSvrDbName'] == "":
         statusDataObj['msgArr'].append("Enter source server DB name"); 
         countOfInvalidInputArg = countOfInvalidInputArg + 1;
     

      ### Section abt destination server details ###

      if inputArgsDataObj['dstDbSvrHostName'] == "":
         statusDataObj['msgArr'].append("Enter destination server DB host name");
         countOfInvalidInputArg = countOfInvalidInputArg + 1;
      if inputArgsDataObj['dstDbSvrPortNo'] == "":
         statusDataObj['msgArr'].append("Enter destination server DB host port no");
         countOfInvalidInputArg = countOfInvalidInputArg + 1;
      if inputArgsDataObj['dstDbSvrUserName'] == "":
         statusDataObj['msgArr'].append("Enter destination server DB username"); 
         countOfInvalidInputArg = countOfInvalidInputArg + 1;
      if inputArgsDataObj['dstDbSvrPwd'] == "":
         statusDataObj['msgArr'].append("Enter destination server DB password");  
         countOfInvalidInputArg = countOfInvalidInputArg + 1;
      if inputArgsDataObj['dstDbSvrDbNames'] == "":
         statusDataObj['msgArr'].append("Enter destination server DB names"); 
         countOfInvalidInputArg = countOfInvalidInputArg + 1;

      
      ### Section about comparsion category ###

      if len(inputArgsDataObj['cmpCtgryDataObj'])>0 :
         isInvalidCmpCtgryData = 'N';
         cmpCtgryDataObj = inputArgsDataObj['cmpCtgryDataObj']; 
         cmpCtgryNo = cmpCtgryDataObj['cmpCtgryNo'];
         if int(cmpCtgryNo) >= 1 and int(cmpCtgryNo) <= 9 :
            if int(cmpCtgryNo) >= 1 and int(cmpCtgryNo) <= 8 :
               includeMethodsArr = cmpCtgryDataObj['includeMethodsArr'];
               if len(includeMethodsArr)>0 :
                  isInvalidCmpCtgryData = 'N';
         else:
             isInvalidCmpCtgryData = 'Y';
 
      if isInvalidCmpCtgryData == "Y" : 
         statusDataObj['msgArr'].append("Choose any one DB comparsion category");  
         countOfInvalidInputArg = countOfInvalidInputArg + 1;
 
 
      ### Section about checking same hostname but given same DB name at source and destination server ###

      if countOfInvalidInputArg == 0:
         statusDataObj['isValidInputArgCollected'] = True;
         inputArgsDataObj['canUseSrcDbSvrDbNamesFurtherComparsionAgainstDstDbSvr'] = 'Y';
         if inputArgsDataObj['srcDbSvrHostName'] == inputArgsDataObj['dstDbSvrHostName'] :
            ### Case 1.1 ###
            inputArgsDataObj['canUseSrcDbSvrDbNamesFurtherComparsionAgainstDstDbSvr'] = 'N';
            ### Case 1.2 ###
            if inputArgsDataObj['srcDbSvrDbName'] == inputArgsDataObj['dstDbSvrDbNames'] :
               statusDataObj['isValidInputArgCollected'] = False;
               statusDataObj['msgArr'].append("Entered 'SOURCE' and 'DESTINATION' server DB name cannot be same");


   except Exception as e:
          handleProcsngAbtErrException("Y");
    
   
   return statusDataObj;



### collect inputs argument as testing environment ###

def collectInputArgsAsTestingEnvironment():
    
    try:

           global inputArgsDataObj;
 
           inputArgsDataObj['srcDbSvrHostName'] = 'localhost';
           inputArgsDataObj['srcDbSvrPortNo'] = '3306';
           inputArgsDataObj['srcDbSvrUserName'] = 'test';
           inputArgsDataObj['srcDbSvrPwd'] = 'a';
           inputArgsDataObj['srcDbSvrDbName'] = 'db_master1';
           inputArgsDataObj['srcDbSvrDbType'] = '';
           inputArgsDataObj['dstDbSvrHostName'] = 'localhost';
           inputArgsDataObj['dstDbSvrPortNo'] = '3306';
           inputArgsDataObj['dstDbSvrUserName'] = 'test';
           inputArgsDataObj['dstDbSvrPwd'] = 'a';
           
           dstDbNamesStr = "db_testing1";
           inputArgsDataObj['dstDbSvrDbNames'] = dstDbNamesStr.replace(" ", "");
           inputArgsDataObj['dstDbSvrDbType'] = '';

           inputArgsDataObj['cmpCtgryDataObj'] = {
                'cmpCtgryNo' : '9', 
                'includeMethodsArr' : [],
                'excludeMethodsArr' : [],
                'findStr' : '',
                'dbTblNamesStr' : "",
                'dbTblColNamesStr' : "",
                'dbTblIndxNamesStr' : "",
                'dbTblFKNamesStr' : "",
                'dbTblTgrNamesStr' : "",
                'dbRoutineNamesStr' : "",
                'dbViewNamesStr' : "",
                'customSearchCondStr' : "",
                'customSearchCondStrForCmptCtgryNoArr' : []
           };

           inputArgsDataObj['isIncludeSysGlblVariableComparsion'] = 'N';
           inputArgsDataObj['isIncludeTblAttrOptnComparsion'] = 'Y';
           inputArgsDataObj['isRearrangeTblColPos'] = "Y";
           inputArgsDataObj['isIncludeTblColDataTypeComparsion'] = "Y";
           inputArgsDataObj['isIncludeTblColDefComparsion'] = "Y";
           inputArgsDataObj['isIncludeTblColIndexesComparsion'] = "Y";
           inputArgsDataObj['isIncludeTblForeignKeysConstraintsComparsion'] = "Y";
           inputArgsDataObj['isIncludeTblTrgsDefComparsion'] = "Y"; 
           inputArgsDataObj['isIncludeDbRoutinesDefComparsion'] = "Y";
           inputArgsDataObj['isIncludeDbViewsDefComparsion'] = "Y";
           inputArgsDataObj['isMakeExactDbSchemasCopy'] = "Y";
           inputArgsDataObj['isExecuteChanges'] = "Y";


    except Exception as e:
           handleProcsngAbtErrException("Y");


### get collected input arguments via questionaries of db compare ###
### category opting all options ###

def getGvnInputArgsViaQstnarieOfDbCmpCtgryOptingAllOptions(inputArgsDataObj):

    try:

        if len(inputArgsDataObj) <= 0 :
           inputArgsDataObj = {};
           
        inputArgsDataObj['cmpCtgryDataObj'] = {
            'cmpCtgryNo' : '9', 
            'includeMethodsArr' : [],
            'excludeMethodsArr' : [],
            'findStr' : '',
            'dbTblNamesStr' : "",
            'dbTblColNamesStr' : "",
            'dbTblIndxNamesStr' : "",
            'dbTblFKNamesStr' : "",
            'dbTblTgrNamesStr' : "",
            'dbRoutineNamesStr' : "",
            'dbViewNamesStr' : "",
            'customSearchCondStr' : "",
            'customSearchCondStrForCmptCtgryNoArr' :  [] 
        };

        cmpCtrgyNoArr = [];
        arrIndx = 1;
        arrLen = 14;
        while arrIndx <= arrLen :
              cmpCtrgyNoArr.append(str(arrIndx));
              arrIndx = arrIndx + 1;    
       
        Qstn = "\n";
        Qstn+= "Wish to exclude from comparsion [single option allowed] & press ENTER ?" + "\n";
        Qstn+= "1) YES" + "\n";
        Qstn+= "2) NO" + "\n";
        Qstn+= "3) Return to main options" + "\n";  
        optNoChoosedStr = raw_input(Qstn).replace(" ", "");

        if optNoChoosedStr == "3" :
           collectInputArgsAsLiveEnvironment('dbAllCmpCtgry');

        if int(optNoChoosedStr) == 1 :

           Qstn = "\n";
           Qstn+= "Choose option to exclude from comparsion [multiple options allowed seperated by comma] & press ENTER ?" + "\n";
           Qstn+= "E.g (1, 2, 4, 5)" + "\n";
           Qstn+= "1) Creating new table" + "\n";
           Qstn+= "2) Existing table column definition changes" + "\n";
           Qstn+= "3) Existing table column data type changes" + "\n";
           Qstn+= "4) Creating new column in existing table" + "\n";
           Qstn+= "5) Existing table indexes definition changes" + "\n";
           Qstn+= "6) Creating new indexes in existing table" + "\n";
           Qstn+= "7) Existing table foreign key constraints changes" + "\n";
           Qstn+= "8) Creating new foreign key constraints in existing table" + "\n";
           Qstn+= "9) Existing table trigger definition changes" + "\n";
           Qstn+= "10) Creating new trigger in existing table" + "\n";
           Qstn+= "11) Existing routine definition changes" + "\n";
           Qstn+= "12) Creating new routines" + "\n";
           Qstn+= "13) Existing views definition changes" + "\n";
           Qstn+= "14) Creating new views" + "\n";        
           optNoChoosedStr = raw_input(Qstn).replace(" ", "");
           
           if int(optNoChoosedStr) == 0 or int(optNoChoosedStr) >= 15 :
              collectInputArgsAsLiveEnvironment('aboveAllMainCmpCtgry');
 
           elif int(optNoChoosedStr) >= 1 and int(optNoChoosedStr) <= 14 :
     
              if optNoChoosedStr in cmpCtrgyNoArr :

                 excludeMethodsArrArr = [];

                 if "1" not in cmpCtrgyNoArr :
                    excludeMethodsArrArr.append("new-tbls");
                 if "2" not in cmpCtrgyNoArr :
                    excludeMethodsArrArr.append("exist-tbl-col-definition");
                 if "3" not in cmpCtrgyNoArr :
                    excludeMethodsArrArr.append("exist-tbl-col-datatype");
                 if "4" not in cmpCtrgyNoArr :
                    excludeMethodsArrArr.append("exist-tbl-new-cols");
                 if "5" not in cmpCtrgyNoArr :
                    excludeMethodsArrArr.append("exist-tbl-indx-definition");
                 if "6" not in cmpCtrgyNoArr :
                    excludeMethodsArrArr.append("exist-tbl-new-indexes");
                 if "7" not in cmpCtrgyNoArr :
                    excludeMethodsArrArr.append("exist-tbl-fks-definition");
                 if "8" not in cmpCtrgyNoArr :
                    excludeMethodsArrArr.append("exist-tbl-new-fks"); 
                 if "9" not in cmpCtrgyNoArr :
                    excludeMethodsArrArr.append("exist-tbl-tgrs-definition");
                 if "10" not in cmpCtrgyNoArr :
                    excludeMethodsArrArr.append("exist-tbl-new-tgrs");
                 if "11" not in cmpCtrgyNoArr :
                    excludeMethodsArrArr.append("exist-db-routines-definition");
                 if "12" not in cmpCtrgyNoArr :
                    excludeMethodsArrArr.append("exist-db-new-routines");
                 if "13" not in cmpCtrgyNoArr :
                    excludeMethodsArrArr.append("exist-db-views-definition");
                 if "14" not in cmpCtrgyNoArr :
                    excludeMethodsArrArr.append("exist-db-new-views"); 

                 inputArgsDataObj['cmpCtgryDataObj']['excludeMethodsArr'] = excludeMethodsArrArr;              


    except Exception as e:
           handleProcsngAbtErrException("Y");    

    return inputArgsDataObj;



### get collected input arguments via questionaries of db compare ###
### category view options ###

def getGvnInputArgsViaQstnarieOfDbCmpCtgryViewOptions(inputArgsDataObj):

    try:

        if len(inputArgsDataObj) <= 0 :
           inputArgsDataObj = {};
           
        inputArgsDataObj['cmpCtgryDataObj'] = {
            'cmpCtgryNo' : '8', 
            'includeMethodsArr' : [],
            'excludeMethodsArr' : [],
            'findStr' : '',
            'dbTblNamesStr' : "",
            'dbTblColNamesStr' : "",
            'dbTblIndxNamesStr' : "",
            'dbTblFKNamesStr' : "",
            'dbTblTgrNamesStr' : "",
            'dbRoutineNamesStr' : "",
            'dbViewNamesStr' : "",
            'customSearchCondStr' : "",
            'customSearchCondStrForCmptCtgryNoArr' :  [] 
        };

        Qstn = "\n";
        Qstn+= "Choose any one option & press ENTER ?" + "\n";
        Qstn+= "1) Specific existing views definition" + "\n";
        Qstn+= "2) Existing all views definition" + "\n";
        Qstn+= "3) Find all new views in existing DB" + "\n";
        Qstn+= "4) Return to main options" + "\n";
        optNoChoosedStr = raw_input(Qstn).replace(" ", "");

        if optNoChoosedStr == "1" :

           Qstn = "\n";
           Qstn+= "Enter [views name seperated by comma OR Type '99' to 'Return to main options'] & press ENTER" + "\n";
           Qstn+= "E.g (views1, views2 etc)" + "\n"; 
           ansStr = raw_input(Qstn).replace(" ", "");

           if ansStr != "99" :

              ansStr = getStringWrappedBySingleQuotes(ansStr);
              inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-db-views-definition'];
              inputArgsDataObj['cmpCtgryDataObj']['findStr'] = ansStr;
              inputArgsDataObj['cmpCtgryDataObj']['dbViewNamesStr'] = ansStr;

           else :
                collectInputArgsAsLiveEnvironment('viewsMainCmpCtgry');

        elif optNoChoosedStr == "2" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-db-views-definition'];

        elif optNoChoosedStr == "3" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-db-new-views'];
    
        else :
             collectInputArgsAsLiveEnvironment('dbAllCmpCtgry'); 


    except Exception as e:
           handleProcsngAbtErrException("Y");    

    return inputArgsDataObj;


### get collected input arguments via questionaries of db compare ###
### category table routine options ###

def getGvnInputArgsViaQstnarieOfDbCmpCtgryRoutineOptions(inputArgsDataObj):

    try:

        if len(inputArgsDataObj) <= 0 :
           inputArgsDataObj = {};
           
        inputArgsDataObj['cmpCtgryDataObj'] = {
            'cmpCtgryNo' : '7', 
            'includeMethodsArr' : [],
            'excludeMethodsArr' : [],
            'findStr' : '',
            'dbTblNamesStr' : "",
            'dbTblColNamesStr' : "",
            'dbTblIndxNamesStr' : "",
            'dbTblFKNamesStr' : "",
            'dbTblTgrNamesStr' : "",
            'dbRoutineNamesStr' : "",
            'dbViewNamesStr' : "",
            'customSearchCondStr' : "",
            'customSearchCondStrForCmptCtgryNoArr' :  [] 
        };

        Qstn = "\n";
        Qstn+= "Choose any one option & press ENTER ?" + "\n";
        Qstn+= "1) Specific existing routines definition" + "\n";
        Qstn+= "2) Existing all routines definition" + "\n";
        Qstn+= "3) Find all new routines in existing DB" + "\n";
        Qstn+= "4) Return to main options" + "\n";
        optNoChoosedStr = raw_input(Qstn).replace(" ", "");

        if optNoChoosedStr == "1" :

           Qstn = "\n";
           Qstn+= "Enter [routines name seperated by comma OR Type '99' to 'Return to main options'] & press ENTER" + "\n";
           Qstn+= "E.g (r1, r2 etc)" + "\n"; 
           ansStr = raw_input(Qstn).replace(" ", "");

           if ansStr != "99" :

              ansStr = getStringWrappedBySingleQuotes(ansStr);
              inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-db-routines-definition'];
              inputArgsDataObj['cmpCtgryDataObj']['dbRoutineNamesStr'] = ansStr;
              inputArgsDataObj['cmpCtgryDataObj']['findStr'] = ansStr;
        
           else :
                collectInputArgsAsLiveEnvironment('routinesMainCmpCtgry'); 
            
        elif optNoChoosedStr == "2" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-db-routines-definition'];

        elif optNoChoosedStr == "3" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-db-new-routines'];

        else :
             collectInputArgsAsLiveEnvironment('dbAllCmpCtgry');


    except Exception as e:
           handleProcsngAbtErrException("Y");    

    return inputArgsDataObj;


### get collected input arguments via questionaries of db compare ###
### category table triggers options ###

def getGvnInputArgsViaQstnarieOfDbCmpCtgryTblTgrOptions(inputArgsDataObj):

    try:

        if len(inputArgsDataObj) <= 0 :
           inputArgsDataObj = {};
           
        inputArgsDataObj['cmpCtgryDataObj'] = {
            'cmpCtgryNo' : '6', 
            'includeMethodsArr' : [],
            'excludeMethodsArr' : [],
            'findStr' : '',
            'dbTblNamesStr' : "",
            'dbTblColNamesStr' : "",
            'dbTblIndxNamesStr' : "",
            'dbTblFKNamesStr' : "",
            'dbTblTgrNamesStr' : "",
            'dbRoutineNamesStr' : "",
            'dbViewNamesStr' : "",
            'customSearchCondStr' : "",
            'customSearchCondStrForCmptCtgryNoArr' :  [] 
        };

        Qstn = "\n";
        Qstn+= "Choose any one option & press ENTER ?" + "\n";
        Qstn+= "1) Specific existing table trigger definition" + "\n";
        Qstn+= "2) Existing all tables trigger definition" + "\n";
        Qstn+= "3) Creating all new triggers in specific existing table" + "\n";
        Qstn+= "4) Creating all new triggers in existing all tables" + "\n"; 
        Qstn+= "5) Return to main options" + "\n";
        optNoChoosedStr = raw_input(Qstn).replace(" ", "");

        if optNoChoosedStr == "1" :

           Qstn = "\n";
           Qstn+= "Enter [table name : trigger name seperated by comma OR Type '99' to 'Return to main options'] & press ENTER" + "\n";
           Qstn+= "E.g (t1:tgr1, t2:tgr2 etc)" + "\n";
           ansStr = raw_input(Qstn).replace(" ", "");

           if ansStr != "99" :

              inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-tgrs-definition'];
              inputArgsDataObj['cmpCtgryDataObj']['findStr'] = ansStr;
   
              findStrSplittedOnCommasArr = ansStr.split(",");
              splittedStrArrLen = len(findStrSplittedOnCommasArr);
              splittedStrArrIndx = 0;
              customSearchStrCondArr = [];
              while(splittedStrArrIndx < splittedStrArrLen):
                   splittedStrOnColonArr = (findStrSplittedOnCommasArr[splittedStrArrIndx]).split(":");
                   if len(splittedStrOnColonArr) == 2 :
                      keyName = splittedStrOnColonArr[0];
                      keyValue = splittedStrOnColonArr[1];
                      customSearchCondStr = "(t.EVENT_OBJECT_TABLE IN ('"+keyName+"') AND t.TRIGGER_NAME IN ('"+keyValue+"'))"; 
                      customSearchStrCondArr.append(customSearchCondStr);
                      splittedStrArrIndx = splittedStrArrIndx + 1;
                   if len(customSearchStrCondArr) > 0 :
                      findStr = " OR ".join("{0}".format(eachStr) for eachStr in customSearchStrCondArr);
                      findStr = " AND (" + findStr + ") ";
                      inputArgsDataObj['cmpCtgryDataObj']['customSearchCondStr'] = findStr;
                      inputArgsDataObj['cmpCtgryDataObj']['customSearchCondStrForCmptCtgryNoArr'] = ['6'];

           else :
                collectInputArgsAsLiveEnvironment('tblTgrMainCmpCtgry');
  
        elif optNoChoosedStr == "2" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-tgrs-definition'];

        elif optNoChoosedStr == "3" :

             Qstn = "\n";
             Qstn+= "Enter [table name seperated by comma OR Type '99' to 'Return to main options'] & press ENTER" + "\n";
             Qstn+= "E.g (t1, t2 etc)" + "\n";
             ansStr = raw_input(Qstn).replace(" ", "");
       
             if ansStr != "99" :

                ansStr = getStringWrappedBySingleQuotes(ansStr);
                inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-new-tgrs'];
                inputArgsDataObj['cmpCtgryDataObj']['dbTblNamesStr'] = ansStr;
                inputArgsDataObj['cmpCtgryDataObj']['findStr'] = ansStr;

             else :
                  collectInputArgsAsLiveEnvironment('tblTgrMainCmpCtgry');


        elif optNoChoosedStr == "4" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-new-tgrs'];

        else :
             collectInputArgsAsLiveEnvironment('dbAllCmpCtgry');
          

    except Exception as e:
           handleProcsngAbtErrException("Y");    

    return inputArgsDataObj;


### get collected input arguments via questionaries of db compare ###
### category table foreign key constraints options ###

def getGvnInputArgsViaQstnarieOfDbCmpCtgryTblFKOptions(inputArgsDataObj):

    try:

        if len(inputArgsDataObj) <= 0 :
           inputArgsDataObj = {};
           
        inputArgsDataObj['cmpCtgryDataObj'] = {
            'cmpCtgryNo' : '5', 
            'includeMethodsArr' : [],
            'excludeMethodsArr' : [],
            'findStr' : '',
            'dbTblNamesStr' : "",
            'dbTblColNamesStr' : "",
            'dbTblIndxNamesStr' : "",
            'dbTblFKNamesStr' : "",
            'dbTblTgrNamesStr' : "",
            'dbRoutineNamesStr' : "",
            'dbViewNamesStr' : "",
            'customSearchCondStr' : "",
            'customSearchCondStrForCmptCtgryNoArr' :  []
        };

        Qstn = "\n";
        Qstn+= "Choose any one option & press ENTER ?" + "\n";
        Qstn+= "1) Specific existing table foreign key constraints definition" + "\n";
        Qstn+= "2) Existing all table foreign key constraints definition" + "\n";
        Qstn+= "3) Creating all new foreign key constraints in specific existing table" + "\n";
        Qstn+= "4) Creating all new foreign key constraints in exist all tables" + "\n";
        Qstn+= "5) Return to main options" + "\n";
        optNoChoosedStr = raw_input(Qstn).replace(" ", "");

        if optNoChoosedStr == "1" :

           Qstn = "\n";
           Qstn+= "Enter [table name:foreign key constraints name seperated by comma OR Type '99' to 'Return to main options'] & press ENTER";
           Qstn+= "\n";
           Qstn+= "E.g (t1:fkc1, t2:fkc2 etc)" + "\n"; 
           ansStr = raw_input(Qstn).replace(" ", "");

           if ansStr != "99" :
       
              inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-fks-definition'];
              inputArgsDataObj['cmpCtgryDataObj']['findStr'] = ansStr;

              findStrSplittedOnCommasArr = ansStr.split(",");
              splittedStrArrLen = len(findStrSplittedOnCommasArr);
              splittedStrArrIndx = 0;
              customSearchStrCondArr = [];
              while(splittedStrArrIndx < splittedStrArrLen):
                   splittedStrOnColonArr = (findStrSplittedOnCommasArr[splittedStrArrIndx]).split(":");
                   if len(splittedStrOnColonArr) == 2 :
                      keyName = splittedStrOnColonArr[0];
                      keyValue = splittedStrOnColonArr[1];
                      customSearchCondStr = "(kcs.TABLE_NAME IN ('"+keyName+"') AND kcs.CONSTRAINT_NAME IN ('"+keyValue+"'))"; 
                      customSearchStrCondArr.append(customSearchCondStr);
                      splittedStrArrIndx = splittedStrArrIndx + 1;
                   if len(customSearchStrCondArr) > 0 :
                      findStr = " OR ".join("{0}".format(eachStr) for eachStr in customSearchStrCondArr);
                      findStr = " AND (" + findStr + ") ";
                      inputArgsDataObj['cmpCtgryDataObj']['customSearchCondStr'] = findStr;
                      inputArgsDataObj['cmpCtgryDataObj']['customSearchCondStrForCmptCtgryNoArr'] = ['5'];
  
           else :
                collectInputArgsAsLiveEnvironment('tblFKMainCmpCtgry');

        elif optNoChoosedStr == "2" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-fks-definition'];

        elif optNoChoosedStr == "3" :

             Qstn = "\n";
             Qstn+= "Enter [table name seperated by comma OR Type '99' to 'Return to main options'] & press ENTER" + "\n";
             Qstn+= "E.g (t1, t2 etc)" + "\n";
             ansStr = raw_input(Qstn).replace(" ", "");

             if ansStr != "99" :

                ansStr = getStringWrappedBySingleQuotes(ansStr); 
                inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-new-fks'];
                inputArgsDataObj['cmpCtgryDataObj']['dbTblNamesStr'] = ansStr;
                inputArgsDataObj['cmpCtgryDataObj']['findStr'] = ansStr;

             else :
                  collectInputArgsAsLiveEnvironment('tblFKMainCmpCtgry');

        elif optNoChoosedStr == "4" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-new-fks'];

        else :
             collectInputArgsAsLiveEnvironment('dbAllCmpCtgry'); 


    except Exception as e:
           handleProcsngAbtErrException("Y");    

    return inputArgsDataObj;


### get collected input arguments via questionaries of db compare ###
### category table indexes options ###

def getGvnInputArgsViaQstnarieOfDbCmpCtgryTblIndxOptions(inputArgsDataObj):

    try:

        if len(inputArgsDataObj) <= 0 :
           inputArgsDataObj = {};
           
        inputArgsDataObj['cmpCtgryDataObj'] = {
            'cmpCtgryNo' : '4', 
            'includeMethodsArr' : [],
            'excludeMethodsArr' : [],
            'findStr' : '',
            'dbTblNamesStr' : "",
            'dbTblColNamesStr' : "",
            'dbTblIndxNamesStr' : "",
            'dbTblFKNamesStr' : "",
            'dbTblTgrNamesStr' : "",
            'dbRoutineNamesStr' : "",
            'dbViewNamesStr' : "",
            'customSearchCondStr' : "",
            'customSearchCondStrForCmptCtgryNoArr' :  []
        };

        Qstn = "\n";
        Qstn+= "Choose any one option & press ENTER ?" + "\n"; 
        Qstn+= "1) Specific existing table index definition" + "\n";
        Qstn+= "2) Existing all tables index definition" + "\n";
        Qstn+= "3) Creating all new indexes in specific existing table" + "\n";
        Qstn+= "4) Creating all new indexes in existing all tables" + "\n";
        Qstn+= "5) Return to main options" + "\n";
        optNoChoosedStr = raw_input(Qstn).replace(" ", "");

        if optNoChoosedStr == "1" :

           Qstn = "\n";
           Qstn+= "Enter [table name : index name seperated by comma OR Type '99' to 'Return to main options'] & press ENTER" + "\n";
           Qstn+= "E.g (t1:index1, t2:index2 etc)" + "\n";
           ansStr = raw_input(Qstn).replace(" ", "");

           if ansStr != "99" : 

              inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-indx-definition'];
              inputArgsDataObj['cmpCtgryDataObj']['findStr'] = ansStr;
 
              findStrSplittedOnCommasArr = ansStr.split(",");
              splittedStrArrLen = len(findStrSplittedOnCommasArr);
              splittedStrArrIndx = 0;
              customSearchStrCondArr = [];
              while(splittedStrArrIndx < splittedStrArrLen):
                   splittedStrOnColonArr = (findStrSplittedOnCommasArr[splittedStrArrIndx]).split(":");
                   if len(splittedStrOnColonArr) == 2 :
                      keyName = splittedStrOnColonArr[0];
                      keyValue = splittedStrOnColonArr[1];
                      customSearchCondStr = "(s.TABLE_NAME IN ('"+keyName+"') AND s.INDEX_NAME IN ('"+keyValue+"'))"; 
                      customSearchStrCondArr.append(customSearchCondStr);
                      splittedStrArrIndx = splittedStrArrIndx + 1;
                   if len(customSearchStrCondArr) > 0 :
                      findStr = " OR ".join("{0}".format(eachStr) for eachStr in customSearchStrCondArr);
                      findStr = " AND (" + findStr + ") ";
                      inputArgsDataObj['cmpCtgryDataObj']['customSearchCondStr'] = findStr;
                      inputArgsDataObj['cmpCtgryDataObj']['customSearchCondStrForCmptCtgryNoArr'] = ['4'];
 
           else :
                collectInputArgsAsLiveEnvironment('tblIndxMainCmpCtgry');
 
        elif optNoChoosedStr == "2" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-indx-definition'];

        elif optNoChoosedStr == "3" :

             Qstn = "\n";
             Qstn+= "Enter [table name seperated by comma OR Type '99' to 'Return to main options'] & press ENTER" + "\n";
             Qstn+= "E.g (t1, t2 etc)" + "\n"; 
             ansStr = raw_input(Qstn).replace(" ", "");

             if ansStr != "99" :

                ansStr = getStringWrappedBySingleQuotes(ansStr);
                inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-new-indexes'];
                inputArgsDataObj['cmpCtgryDataObj']['dbTblNamesStr'] = ansStr;
                inputArgsDataObj['cmpCtgryDataObj']['findStr'] = ansStr;

             else :
                  collectInputArgsAsLiveEnvironment('tblIndxMainCmpCtgry');
   

        elif optNoChoosedStr == "4" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-new-indexes'];
 
        else :
             collectInputArgsAsLiveEnvironment('dbAllCmpCtgry');  


    except Exception as e:
           handleProcsngAbtErrException("Y");    

    return inputArgsDataObj;



### get collected input arguments via questionaries of db compare ###
### category table columns options ###

def getGvnInputArgsViaQstnarieOfDbCmpCtgryTblColOptions(inputArgsDataObj):

    try:

        if len(inputArgsDataObj) <= 0 :
           inputArgsDataObj = {};
           
        inputArgsDataObj['cmpCtgryDataObj'] = {
            'cmpCtgryNo' : '3', 
            'includeMethodsArr' : [],
            'excludeMethodsArr' : [],
            'findStr' : '',
            'dbTblNamesStr' : "",
            'dbTblColNamesStr' : "",
            'dbTblIndxNamesStr' : "",
            'dbTblFKNamesStr' : "",
            'dbTblTgrNamesStr' : "",
            'dbRoutineNamesStr' : "",
            'dbViewNamesStr' : "",
            'customSearchCondStr' : "",
            'customSearchCondStrForCmptCtgryNoArr' :  []
        };

        Qstn = "\n";
        Qstn+= "Choose any one option & press ENTER ?" + "\n";
        Qstn+= "1) Specific existing table name with column name [based on same data type definition]" + "\n";
        Qstn+= "2) Existing tables all columns [based on same data type definition]" + "\n";
        Qstn+= "3) Specific existing table name with column name [based on different data type]" + "\n";
        Qstn+= "4) Existing table all columns [based on different data type]" + "\n";
        Qstn+= "5) Creating all new column in specific existing tables" + "\n";
        Qstn+= "6) Creating all new column in existing all tables" + "\n";
        Qstn+= "7) Return to main options" + "\n";
        optNoChoosedStr = raw_input(Qstn).replace(" ", "");

        if optNoChoosedStr == "1" :

           Qstn = "\n";
           Qstn+= "Enter [table name : column name seperated by comma OR Type '99' to 'Return to main options'] & press ENTER" + "\n";
           Qstn+= "E.g (t1:c1, t2:c2 etc)" + "\n"; 
           ansStr = raw_input(Qstn).replace(" ", "");

           if ansStr != "99" : 

              inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-col-definition'];
              inputArgsDataObj['cmpCtgryDataObj']['findStr'] = ansStr;

              findStrSplittedOnCommasArr = ansStr.split(",");
              splittedStrArrLen = len(findStrSplittedOnCommasArr);
              splittedStrArrIndx = 0;
              customSearchStrCondArr = [];
              while(splittedStrArrIndx < splittedStrArrLen):
                   splittedStrOnColonArr = (findStrSplittedOnCommasArr[splittedStrArrIndx]).split(":");
                   if len(splittedStrOnColonArr) == 2 :
                      keyName = splittedStrOnColonArr[0];
                      keyValue = splittedStrOnColonArr[1];
                      customSearchCondStr = "(c.TABLE_NAME IN ('"+keyName+"') AND c.COLUMN_NAME IN ('"+keyValue+"'))"; 
                      customSearchStrCondArr.append(customSearchCondStr);
                      splittedStrArrIndx = splittedStrArrIndx + 1;
                   if len(customSearchStrCondArr) > 0 :
                      findStr = " OR ".join("{0}".format(eachStr) for eachStr in customSearchStrCondArr);
                      findStr = " AND (" + findStr + ") ";
                      inputArgsDataObj['cmpCtgryDataObj']['customSearchCondStr'] = findStr;
                      inputArgsDataObj['cmpCtgryDataObj']['customSearchCondStrForCmptCtgryNoArr'] = ['3'];
            
           else :
                collectInputArgsAsLiveEnvironment('tblColMainCmpCtgry');

        elif optNoChoosedStr == "2" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-col-definition'];

        elif optNoChoosedStr == "3" :

             Qstn = "\n";
             Qstn+= "Enter [table name : column name seperated by comma OR Type '99' to 'Return to main options'] & press ENTER" + "\n";
             Qstn+= "E.g (t1:c1, t2:c2 etc)" + "\n"; 
             ansStr = raw_input(Qstn).replace(" ", "");
          
             if ansStr != "99" :

                inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-col-datatype'];
                inputArgsDataObj['cmpCtgryDataObj']['findStr'] = ansStr;

                findStrSplittedOnCommasArr = ansStr.split(",");
                splittedStrArrLen = len(findStrSplittedOnCommasArr);
                splittedStrArrIndx = 0;
                customSearchStrCondArr = [];
                while(splittedStrArrIndx < splittedStrArrLen):
                     splittedStrOnColonArr = (findStrSplittedOnCommasArr[splittedStrArrIndx]).split(":");
                     if len(splittedStrOnColonArr) == 2 :
                        keyName = splittedStrOnColonArr[0];
                        keyValue = splittedStrOnColonArr[1];
                        customSearchCondStr = "(c.TABLE_NAME IN ('"+keyName+"') AND c.COLUMN_NAME IN ('"+keyValue+"'))"; 
                        customSearchStrCondArr.append(customSearchCondStr);
                        splittedStrArrIndx = splittedStrArrIndx + 1;
                     if len(customSearchStrCondArr) > 0 :
                        findStr = " OR ".join("{0}".format(eachStr) for eachStr in customSearchStrCondArr);
                        findStr = " AND (" + findStr + ") ";
                        inputArgsDataObj['cmpCtgryDataObj']['customSearchCondStr'] = findStr;
                        inputArgsDataObj['cmpCtgryDataObj']['customSearchCondStrForCmptCtgryNoArr'] = ['3'];

             else :
                  collectInputArgsAsLiveEnvironment('tblColMainCmpCtgry');
             

        elif optNoChoosedStr == "4" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-col-datatype'];

        elif optNoChoosedStr == "5" :

             Qstn = "\n";
             Qstn+= "Enter [table name seperated by comma OR Type '99' to 'Return to main options'] & press ENTER" + "\n";
             Qstn+= "E.g (t1, t2 etc)" + "\n"; 
             ansStr = raw_input(Qstn).replace(" ", "");

             if ansStr != "99" :
                ansStr = getStringWrappedBySingleQuotes(ansStr);
                inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-new-cols'];
                inputArgsDataObj['cmpCtgryDataObj']['dbTblNamesStr'] = ansStr;
                inputArgsDataObj['cmpCtgryDataObj']['findStr'] = ansStr;
 
             else :
                  collectInputArgsAsLiveEnvironment('tblColMainCmpCtgry');
           
        elif optNoChoosedStr == "6" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbl-new-cols'];

        else :
             collectInputArgsAsLiveEnvironment('dbAllCmpCtgry');


    except Exception as e:
           handleProcsngAbtErrException("Y");    

    return inputArgsDataObj;



### get collected input arguments via questionaries of db compare ###
### category tables options ###

def getGvnInputArgsViaQstnarieOfDbCmpCtgryTblOptions(inputArgsDataObj):

    try:

        if len(inputArgsDataObj) <= 0 :
           inputArgsDataObj = {};
           
        inputArgsDataObj['cmpCtgryDataObj'] = {
            'cmpCtgryNo' : '2', 
            'includeMethodsArr' : [],
            'excludeMethodsArr' : [],
            'findStr' : '',
            'dbTblNamesStr' : "",
            'dbTblColNamesStr' : "",
            'dbTblIndxNamesStr' : "",
            'dbTblFKNamesStr' : "",
            'dbTblTgrNamesStr' : "",
            'dbRoutineNamesStr' : "",
            'dbViewNamesStr' : "",
            'customSearchCondStr' : "",
            'customSearchCondStrForCmptCtgryNoArr' :  []
        };

        Qstn = "\n";
        Qstn+= "Choose any one option & press ENTER ?" + "\n"; 
        Qstn+= "1) Specific existing table" + "\n";
        Qstn+= "2) Existing all tables" + "\n";
        Qstn+= "3) Find all new tables" + "\n";
        Qstn+= "4) Return to main options" + "\n";
        optNoChoosedStr = raw_input(Qstn).replace(" ", "");

        if optNoChoosedStr == "1" :

           Qstn = "\n";
           Qstn+= "Enter [table names seperated by comma OR Type '99' to 'Return to main options'] & press ENTER" + "\n";
           ansStr = raw_input(Qstn).replace(" ", "");

           if ansStr != "99" :

              ansStr = getStringWrappedBySingleQuotes(ansStr);
              inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbls'];
              inputArgsDataObj['cmpCtgryDataObj']['dbTblNamesStr'] = ansStr;
              inputArgsDataObj['cmpCtgryDataObj']['findStr'] = ansStr;

           else : 
                collectInputArgsAsLiveEnvironment('tblMainCmpCtgry'); 

        elif optNoChoosedStr == "2" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbls'];

        elif optNoChoosedStr == "3" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['new-tbls'];

        else :
             collectInputArgsAsLiveEnvironment('dbAllCmpCtgry');


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return inputArgsDataObj;


### get collected input arguments via questionaries of db compare ###
## category tables attributes options ###

def getGvnInputArgsViaQstnarieOfDbCmpCtgryTblAttrOptions(inputArgsDataObj):

    try:

        if len(inputArgsDataObj) <= 0 :
           inputArgsDataObj = {};
           
        inputArgsDataObj['cmpCtgryDataObj'] = {
            'cmpCtgryNo' : '1', 
            'includeMethodsArr' : [],
            'excludeMethodsArr' : [],
            'findStr' : '',
            'dbTblNamesStr' : "",
            'dbTblColNamesStr' : "",
            'dbTblIndxNamesStr' : "",
            'dbTblFKNamesStr' : "",
            'dbTblTgrNamesStr' : "",
            'dbRoutineNamesStr' : "",
            'dbViewNamesStr' : "",
            'customSearchCondStr' : "",
            'customSearchCondStrForCmptCtgryNoArr' :  []
        };

        Qstn = "\n";
        Qstn+= "Choose any one option & press ENTER ?" + "\n";
        Qstn+= "1) Specific existing table" + "\n";
        Qstn+= "2) Existing all tables" + "\n";
        Qstn+= "3) Return to main options" + "\n";
        optNoChoosedStr = raw_input(Qstn).replace(" ", "");

        if optNoChoosedStr == "1" :

           Qstn = "\n";
           Qstn+= "Enter [table names seperated by comma OR Type '99' to 'Return to main options'] & press ENTER" + "\n";
           Qstn+= "E.g (t1, t2 etc)" + "\n";
           ansStr = raw_input(Qstn).replace(" ", "");

           if ansStr != "99" :

              ansStr = getStringWrappedBySingleQuotes(ansStr); 
              inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbls'];
              inputArgsDataObj['cmpCtgryDataObj']['dbTblNamesStr'] = ansStr;
              inputArgsDataObj['cmpCtgryDataObj']['findStr'] = ansStr;

           else :
                collectInputArgsAsLiveEnvironment('tblAttrsMainCmpCtgry'); 

        elif optNoChoosedStr == "2" :
             inputArgsDataObj['cmpCtgryDataObj']['includeMethodsArr'] = ['exist-tbls'];

        else :
             collectInputArgsAsLiveEnvironment('dbAllCmpCtgry');


    except Exception as e:
           handleProcsngAbtErrException("Y");    

    return inputArgsDataObj;



### get questionaries for db comparsion category inclusion ###

def getQstnarieForCollectingDBCmpCtgryInclusionOptions():

    Qstn = "";

    try:

        
        Qstn = "\n";
        Qstn+= "Choose any one option & press ENTER to compare ?" + "\n";
        Qstn+= "1) Table Attributes" + "\n";
        Qstn+= "2) Table Structure [Column data-type / definition, indexes, foreign keys constraints]" + "\n";
        Qstn+= "3) Table Column" + "\n";
        Qstn+= "4) Table Index" + "\n";
        Qstn+= "5) Table Foreign Key Constraints" + "\n";
        Qstn+= "6) Table Trigger" + "\n";
        Qstn+= "7) DB Routine / Event / Procedure / Function" + "\n";
        Qstn+= "8) DB View" + "\n";
        Qstn+= "9) Above All" + "\n";
        

    except Exception as e:
           handleProcsngAbtErrException("Y");    

    return Qstn;
 

### get collected input arguments abt destination server ###
### via asking different questionarie ###

def getGvnInputArgsAbtDstSvrViaQstnarie(inputArgsDataObj):

    try:

        if len(inputArgsDataObj) == 0 :
           inputArgsDataObj = {}; 

        msgStr = "\n";
        msgStr+= "#### Provide information about 'DESTINATION' DB server ####";
        displayMsg('', msgStr);
           
        Qstn = "\n";
        Qstn+= "Enter host name & press ENTER : ";
        inputArgsDataObj['dstDbSvrHostName'] = raw_input(Qstn).replace(" ", "");
           
        Qstn = "\n";  
        Qstn+= "Enter port no & press ENTER : ";
        inputArgsDataObj['dstDbSvrPortNo'] = raw_input(Qstn).replace(" ", "");
           
        Qstn = "\n";
        Qstn+= "Enter username & press ENTER : ";
        inputArgsDataObj['dstDbSvrUserName'] = raw_input(Qstn).replace(" ", "");
           
        Qstn = "\n";
        Qstn+= "Enter password & press ENTER : ";
        inputArgsDataObj['dstDbSvrPwd'] = getpass.getpass(prompt=Qstn).replace(" ", "");
           
        Qstn = "\n";
        Qstn+= "Enter DB names seperated by comma OR Type 'ALL' to include all DB names & press ENTER" + "\n";
        Qstn+= "E.g (db_testing1, db_testing2, all etc)"  + "\n";
        inputArgsDataObj['dstDbSvrDbNames'] = raw_input(Qstn).replace(" ", "");


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return inputArgsDataObj;


### get collected input arguments abt source server ###
### via asking different questionarie ###

def getGvnInputArgsAbtSrcSvrViaQstnarie(inputArgsDataObj):

    try:

        if len(inputArgsDataObj) == 0 :
           inputArgsDataObj = {}; 

        msgStr = "\n";
        msgStr+= "#### Provide information about 'SOURCE' DB server ####";
        displayMsg('', msgStr);
              
        Qstn = "\n";  
        Qstn+= "Enter host name & press ENTER : ";
        inputArgsDataObj['srcDbSvrHostName'] = raw_input(Qstn).replace(" ", "");
           
        Qstn = "\n";  
        Qstn+= "Enter port no & press ENTER : ";
        inputArgsDataObj['srcDbSvrPortNo'] = raw_input(Qstn).replace(" ", "");

        Qstn = "\n";
        Qstn+= "Enter username & press ENTER : ";
        inputArgsDataObj['srcDbSvrUserName'] = raw_input(Qstn).replace(" ", "");
           
        Qstn = "\n";
        Qstn+= "Enter password & press ENTER : ";
        inputArgsDataObj['srcDbSvrPwd'] = getpass.getpass(prompt=Qstn).replace(" ", "");
           
        Qstn = "\n";
        Qstn+= "Enter database name [Single DB name allowed] & press ENTER" + "\n";
        Qstn+= "E.g (db_master1, db_testing1 etc)" + "\n";
        inputArgsDataObj['srcDbSvrDbName'] = raw_input(Qstn).replace(" ", "");


    except Exception as e:
           handleProcsngAbtErrException("Y");

    return inputArgsDataObj;


### collect inputs argument as live environment ###

def collectInputArgsAsLiveEnvironment(typeOfOptnsToShow):
    
    try:

        global inputArgsDataObj;
        cmpCtgryNoStr = '0'; 
 
        if typeOfOptnsToShow == 'All' : 
           inputArgsDataObj = getGvnInputArgsAbtSrcSvrViaQstnarie(inputArgsDataObj); 
           inputArgsDataObj = getGvnInputArgsAbtDstSvrViaQstnarie(inputArgsDataObj);
        
        if typeOfOptnsToShow == 'All' or typeOfOptnsToShow == 'dbAllCmpCtgry' :
           Qstn = getQstnarieForCollectingDBCmpCtgryInclusionOptions();          
           cmpCtgryNoStr = raw_input(Qstn).replace(" ", "");

   
        ### compare ctgry.1 section abt tables attributes options ###
        
        if (cmpCtgryNoStr == "1" and typeOfOptnsToShow == 'All') or typeOfOptnsToShow == 'tblAttrsMainCmpCtgry':
           inputArgsDataObj = getGvnInputArgsViaQstnarieOfDbCmpCtgryTblAttrOptions(inputArgsDataObj);


        ### compare ctgry.2 section abt tables options ###

        elif (cmpCtgryNoStr == "2"  and typeOfOptnsToShow == 'All') or typeOfOptnsToShow == 'tblMainCmpCtgry' :
             inputArgsDataObj = getGvnInputArgsViaQstnarieOfDbCmpCtgryTblOptions(inputArgsDataObj);


        ### compare ctgry.3 section abt table columns options ###

        elif (cmpCtgryNoStr == "3" and typeOfOptnsToShow == 'All') or typeOfOptnsToShow == 'tblColMainCmpCtgry' :
             inputArgsDataObj = getGvnInputArgsViaQstnarieOfDbCmpCtgryTblColOptions(inputArgsDataObj);
          

        ### compare ctgry.4 section abt table indexes options ###

        elif (cmpCtgryNoStr == "4" and typeOfOptnsToShow == 'All') or typeOfOptnsToShow == 'tblIndxMainCmpCtgry' :
             inputArgsDataObj = getGvnInputArgsViaQstnarieOfDbCmpCtgryTblIndxOptions(inputArgsDataObj);
   

        ### compare ctgry.5 section abt table foreign key constraints options ###      

        elif (cmpCtgryNoStr == "5" and typeOfOptnsToShow == 'All') or typeOfOptnsToShow == 'tblFKMainCmpCtgry' :
             inputArgsDataObj = getGvnInputArgsViaQstnarieOfDbCmpCtgryTblFKOptions(inputArgsDataObj);
  

        ### compare ctgry.6 section abt table triggers options ###      
          
        elif (cmpCtgryNoStr == "6" and typeOfOptnsToShow == 'All') or typeOfOptnsToShow == 'tblTgrMainCmpCtgry' :
             inputArgsDataObj = getGvnInputArgsViaQstnarieOfDbCmpCtgryTblTgrOptions(inputArgsDataObj); 
  

        ### compare ctgry.7 section abt db routines options ###       

        elif (cmpCtgryNoStr == "7" and typeOfOptnsToShow == 'All') or typeOfOptnsToShow == 'routinesMainCmpCtgry' :
             inputArgsDataObj = getGvnInputArgsViaQstnarieOfDbCmpCtgryRoutineOptions(inputArgsDataObj);
  

        ### compare ctgry.8 section abt db views options ###

        elif (cmpCtgryNoStr == "8" and typeOfOptnsToShow == 'All') or typeOfOptnsToShow == 'viewsMainCmpCtgry' :
             inputArgsDataObj = getGvnInputArgsViaQstnarieOfDbCmpCtgryViewOptions(inputArgsDataObj);


        ### compare ctgry.9 section abt opting all options ###      

        elif (cmpCtgryNoStr == "9" and typeOfOptnsToShow == 'All') or typeOfOptnsToShow == 'aboveAllMainCmpCtgry':
             inputArgsDataObj = getGvnInputArgsViaQstnarieOfDbCmpCtgryOptingAllOptions(inputArgsDataObj);
          

        Qstn = "\n";
        Qstn+= "Wish to create exact copy (SOURCE => DESTINATION) server DB ?" + "\n";
        Qstn+= "1) YES" + "\n";
        Qstn+= "2) NO" + "\n";
        optNoChoosedStr = raw_input(Qstn).replace(" ", "");
        if optNoChoosedStr == "1" or (optNoChoosedStr).lower() == "yes" :
           inputArgsDataObj['isMakeExactDbSchemasCopy'] = "Y";

        Qstn = "\n";
        Qstn+= "Wish to run changes immediately on 'DESTINATION' server corresponding databases ?" + "\n";
        Qstn+= "1) YES" + "\n";
        Qstn+= "2) NO" + "\n";
        optNoChoosedStr = raw_input(Qstn).replace(" ", "");
        if optNoChoosedStr == "1" or (optNoChoosedStr).lower() == "yes" :
           inputArgsDataObj['isExecuteChanges'] = "Y";


    except Exception as e:
           handleProcsngAbtErrException("Y");

 

### collect inputs arguments via environment type ###

def collectInputArgsViaEnvironmentType(environmentType):

    try:
  
       if environmentType == 'Testing' :
          collectInputArgsAsTestingEnvironment();
       if environmentType == 'Live' :
          collectInputArgsAsLiveEnvironment('All');

    except Exception as e:
           handleProcsngAbtErrException("Y");


### execute diff db script ###

def executeDiffDBScript():
    
    try:
       
        environmentType = 'Live';
        collectInputArgsViaEnvironmentType(environmentType);
        inputArgCollectedValidationStatusDataObj = validateInputArgsBasedOnEnvironmentType();
        isValidInputArgCollected = inputArgCollectedValidationStatusDataObj['isValidInputArgCollected'];
        if isValidInputArgCollected == True:
           handleProcsngDiffDbComparsionBtwnSrcAndDstSvr();
        else:
            msgDataArr = inputArgCollectedValidationStatusDataObj['msgArr'];
            displayErrMsgAbtWrngInputsArguments(msgDataArr);
  
      
    except Exception as e:
           handleProcsngAbtErrException("Y");


executeDiffDBScript();







