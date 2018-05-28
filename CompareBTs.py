import optparse
import os 
#from Gen_Perf_Stats_2to3_WithConfig import Gen_Headers, Gen_Html_Data, Gen_Html_End
import Gen_Perf_Stats_2to3_WithConfig as HTMLFile

def Gen_Html_Top_Local():
    html='''<!DOCTYPE html>
<html>
<head>
<style>
table#t01 {
border: 1px solid gray;
margin: 5px;
}
table#t01 tr:nth-child(even) {
background-color: #eee;
}
table#t01 tr:nth-child(odd) {
        background-color:#fff;
}
table#t01 th {
background-color: LightSkyBlue;
color: black;
text-align: left;
}

</style>
</head>
<body>
<p><b>NS & ND Transactions Comparision</b></p>
'''
    with open('PerfStats.html',  'w+') as HT:
        HT.write(html + "\n")
    return




def Get_NStx(TestRunPath):
  NSTxDic = {}
  NSTxFilePath = os.path.join(TestRunPath + "/trans_detail.dat")
  if not os.path.exists(NSTxFilePath):
    print("ERROR :-> Transaction details file is not present = {0} ".format(NSTxFilePath))
    return "FALSE"
  with open (NSTxFilePath, "r") as NStxFile:
    for line in NStxFile:
      SplittedVal = line.split("|")
      TxName = SplittedVal[0]
      TotalRequest = SplittedVal[5]
      if (TxName == "Transaction Name") or (TxName == "ALL"):
        pass
      else:
        NSTxDic[TxName] = TotalRequest
  
  return NSTxDic


def Get_BTtx(Controller_Name, TestRunNumber):
  BTTxDic = {}
  cmd = "/home/netstorm/{0}/bin/ndi_db_get_flowpath_data --testrun {1} --group url | cut -d '|' -f1,3".format(Controller_Name, TestRunNumber)
  CmdOutput = os.popen(cmd).read()
  if (CmdOutput == ""):
    print("ERROR :-> Query Not giving output --> {}".format(cmd))
    return
  else:
    for line in CmdOutput.splitlines():
      SplittedVal = line.split("|")
      TxName = SplittedVal[0]
      Count = SplittedVal[1]
      if (TxName == "URLName"):
        pass
      else:
        BTTxDic[TxName] = Count
  return BTTxDic


def CompareTX(NStxDic,BTTxDic):
  Gen_Html_Top_Local()
  Headers = ["Transaction"]
  NSTxVal = ["NS"]
  BTTxVal = ["ND"]
  #print(NStxDic)
  #print(BTTxDic)
  for NSkey, NSvalue in NStxDic.items():
    Headers.append(NSkey)
    NSTxVal.append(NSvalue)
    #for NDKey, NDValue in BTTxDic.items():
      #if (NDKey == NSkey):
        #BTTxVal.append(NDValue)
    try:
      BTTxVal.append(BTTxDic[NSkey])
    except:
      BTTxVal.append('NA')
  with open("PerfStats.html", "a") as HT:
    HT.write('<table id="t01" style="width:100%">' + "\n")
  #print(Headers)
  #print(NSTxVal)
  #print(BTTxVal)
  HTMLFile.Gen_Headers(Headers)
  HTMLFile.Gen_Html_Data(NSTxVal)
  HTMLFile.Gen_Html_Data(BTTxVal)
  with open("PerfStats.html", "a") as HT:
    HT.write("</table>" + "\n")
  HTMLFile.Gen_Html_End()  
    
  return



def main():
  parser = optparse.OptionParser("Usage %prog" + " -T <TestRunNumber> " + " -C <ControllerName> ")
  parser.add_option("-T", dest="TestRunNumber", type="string", help="Provide valid TestRun Number")
  parser.add_option("-C", dest="Controller_Name", type="string", help="Provide exact controller name")
  (options, args) = parser.parse_args()
  TestRunNumber = str(options.TestRunNumber)
  Controller_Name = str(options.Controller_Name)
  TestRunPath = ""
  if (TestRunNumber == "None") or (Controller_Name == "None"):
    print("Usage --> python CompareBTs.py -T <TestRunNumber> -C <ControllerName> ")
  else:
    TestRunPath = os.path.join("/home/netstorm/" + Controller_Name + "/logs/TR" + TestRunNumber)
    if not os.path.exists(TestRunPath):
      print("Test Run path is not valid = {0} ".format(TestRunPath))
    else:
      NSTxDic = Get_NStx(TestRunPath) 
      if (NSTxDic == "FALSE"):
        print("ERROR :-> AS There is not Transaction information Hence returning")
        return
      BTTxDic = Get_BTtx(Controller_Name, TestRunNumber)
      #print(BTTxDic)
      CompareTX(NSTxDic,BTTxDic)
  return


if __name__ == "__main__":
  main()
