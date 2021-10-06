from tkinter import Tk
from tkinter.filedialog import askopenfilename

HasMPL=True

try:
    from matplotlib import pyplot

except:
    HasMPL=False
    print("It seems that you do not have matplotlib installed.\nThis means this program will not instantly produce a graph.\n\n")

#START OF FUNCTIONS AND SUBROUTINES:

def SecondsToTime(Seconds):
    Seconds=int(Seconds)
    RealTime=["","",""]
    RealTime[0]=str(Seconds//3600)
    Seconds=Seconds%3600
    RealTime[1]=str(Seconds//60)
    RealTime[2]=str(Seconds%60)
    Index=0
    while Index<=2:
        if len(RealTime[Index])==1:
            RealTime[Index]="0"+RealTime[Index]

        Index+=1

    return RealTime[0]+":"+RealTime[1]+":"+RealTime[2]

def TimeToSeconds(RealTime):
    RealTime=RealTime.split(":")
    return int(RealTime[0])*3600+int(RealTime[1])*60+int(RealTime[2])

def PlotGraph(Muons):
    xTable = []
    yTable = []

    try:
        for key in Muons:
            xTable.append(key)
            yTable.append(Muons[key])

        pyplot.plot(xTable, yTable)
        pyplot.ylim(bottom=0)
        pyplot.show()

    except:
        print("Something went wrong. Please try again.")

#START OF MAIN PROGRAM

input("This program relies on it being the format which HiSPARC has it in from their website.\nIt takes in data which HiSPARC gives when you click: 'Download event summary data'.\nIf your data is not in that format, this program won't work.\nAt best, it'll not run, but at worst, it'll give you incorrect data.\n\nPress enter to continue... ")

#The data must be in order

Tk().withdraw()
Filename = askopenfilename()
print("\nYou selcected:\n{0}\n".format(Filename))
FileData=open(Filename,"r")
Data=FileData.readlines()
FileData.close()

Muons={}
Menu=""
#Truncate Start Time
TST=""

#could add in code to get rid of text

StartTime=Data[29].split("\t")[1]

while TST!="hour" and TST!="minute" and TST!="day" and TST!="n":
    TST=input("Do you want to truncate the start time? (day/hour/minute/n) : ").lower()
    
if TST=="day":
    StartTime=StartTime.split(":")
    for Count in range(0,3):
        StartTime[Count]="00"

elif TST=="hour":
    StartTime=StartTime.split(":")
    for Count in range(1,3):
        StartTime[Count]="00"

elif TST=="minute":
    StartTime=StartTime.split(":")
    StartTime[2]="00"

else:
    StartTime=StartTime.split(":")

Blocks=float(input("What minute blocks would you like to separate it into? : "))*60

Type=""
while Type!="d" and Type!="m":
    Type=input("Would you like to have it show the date and time of the blocks in the output, or\nminutes after the start time? (d/m) : ").lower()
    
if Type=="d":
    Day=Data[29].split("\t")[0]
    VST=StartTime[0]+":"+StartTime[1]+":"+StartTime[2]
    LineIndex=29
    #Format: [Day]; [Start time of block] <= t < [End time of block]
    #This'll then point to how many muons appeared in that time slot.
    Muons={Day+"; "+VST+" <= t < "+SecondsToTime((TimeToSeconds(VST)+Blocks)%86400):0}
    while LineIndex<(len(Data)-1):
        Line=Data[LineIndex]
        if Line.split("\t")[0]!=Day:
            print("Data went over two or more days. Only the first day has been recorded.")
            break
        
        if TimeToSeconds(Line.split("\t")[1])>=TimeToSeconds(VST) and TimeToSeconds(Line.split("\t")[1])<(TimeToSeconds(VST)+Blocks):
            Muons[Day+"; "+VST+" <= t < "+SecondsToTime((TimeToSeconds(VST)+Blocks)%86400)]=Muons[Day+"; "+VST+" <= t < "+SecondsToTime((TimeToSeconds(VST)+Blocks)%86400)]+1

        else:
            VST=SecondsToTime(TimeToSeconds(VST)+Blocks)
            Muons[Day+"; "+VST+" <= t < "+SecondsToTime((TimeToSeconds(VST)+Blocks)%86400)]=0
            LineIndex-=1

        LineIndex+=1

    print("\nIn dictionary format:")
    print(Muons)

    print("\n\nIn .csv format:")
    Output=""
    for Key in Muons:
        Output=Output+"\n"+Key+","+str(Muons[Key])

    Output=Output[1:len(Output)]

    print(Output)

    FileWanted=""
    while FileWanted!="n" and FileWanted!="y":
        FileWanted=input("Do you want a csv file for this? (y/n): ").lower()

    if FileWanted=="y":
        Count=0
        NameFound=False
        while not NameFound:
            if Count==0:
                FileOutput=open("Output.txt","a")
                FileOutput.close()
                FileOutput=open("Output.txt","r")
                CheckingData=FileOutput.readlines()
                FileOutput.close()

            else:
                FileOutput=open("Output"+str(Count)+".txt","a")
                FileOutput.close()
                FileOutput=open("Output"+str(Count)+".txt","r")
                CheckingData=FileOutput.readlines()
                FileOutput.close()
                
            if CheckingData==[]:
                NameFound=True

            else:
                Count+=1

        if Count==0:
            FileOutput=open("Output.txt","w")
            FileOutput.write(Output)
            FileOutput.close()
            print("Your data has been written to Output.txt")

        else:
            FileOutput=open("Output"+str(Count)+".txt","w")
            FileOutput.write(Output)
            FileOutput.close()
            print("Your data has been written to Output{0}.txt".format(str(Count)))

        input("Press enter to continue... ")

elif Type=="m":
    Day=Data[29].split("\t")[0]
    VSS=TimeToSeconds(StartTime[0]+":"+StartTime[1]+":"+StartTime[2])
    StartSeconds=VSS
    LineIndex=29
    #Format: Minutes after start time, Muons
    Muons={((VSS-StartSeconds+Blocks)/60):0}
    while LineIndex<(len(Data)-1):
        Line=Data[LineIndex]
        if Line.split("\t")[0]!=Day:
            print("Data went over two or more days. Only the first day has been recorded.")
            break
        
        if TimeToSeconds(Line.split("\t")[1])>=VSS and TimeToSeconds(Line.split("\t")[1])<(VSS+Blocks):
            Muons[((VSS-StartSeconds+Blocks)/60)]=Muons[((VSS-StartSeconds+Blocks)/60)]+1

        else:
            VSS=VSS+Blocks
            Muons[((VSS-StartSeconds+Blocks)/60)]=0
            LineIndex-=1

        LineIndex+=1

    print("Numbers repesent the end of the block: it's the first value\nwhich is NOT re")

    print("\nIn dictionary format:")
    print(Muons)

    print("\n\nIn .csv format:")
    Output=""
    for Key in Muons:
        Output=Output+"\n"+str(Key)+","+str(Muons[Key])

    Output=Output[1:len(Output)]

    print(Output)

    FileWanted=""
    while FileWanted!="n" and FileWanted!="y":
        FileWanted=input("Do you want a csv file for this? (y/n): ").lower()

    if FileWanted=="y":
        Count=0
        NameFound=False
        while not NameFound:
            if Count==0:
                FileOutput=open("Output.txt","a")
                FileOutput.close()
                FileOutput=open("Output.txt","r")
                CheckingData=FileOutput.readlines()
                FileOutput.close()

            else:
                FileOutput=open("Output"+str(Count)+".txt","a")
                FileOutput.close()
                FileOutput=open("Output"+str(Count)+".txt","r")
                CheckingData=FileOutput.readlines()
                FileOutput.close()
                
            if CheckingData==[]:
                NameFound=True

            else:
                Count+=1

        if Count==0:
            FileOutput=open("Output.txt","w")
            FileOutput.write(Output)
            FileOutput.close()
            print("Your data has been written to Output.txt")

        else:
            FileOutput=open("Output"+str(Count)+".txt","w")
            FileOutput.write(Output)
            FileOutput.close()
            print("Your data has been written to Output{0}.txt".format(str(Count)))

        input("Press enter to continue... ")

    if HasMPL:
        GraphWanted=""
        while GraphWanted!="y" and GraphWanted!="n":
            GraphWanted=input("Do you want a graph for this data? (y/n) : ")

        if GraphWanted=="y":
            xTable = []
            yTable = []

            try:
                for key in Muons:
                    xTable.append(key)
                    yTable.append(Muons[key])

                pyplot.plot(xTable, yTable)
                pyplot.ylim(bottom=0)
                pyplot.show()

            except:
                print("Something went wrong. Please try again.")

else:
    print("Invalid")
