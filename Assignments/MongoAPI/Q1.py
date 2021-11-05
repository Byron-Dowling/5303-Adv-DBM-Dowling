import json
#create custom object of json object sample 
MyCustomObject = {
        "Col": "",
        "Crn": "",
        "Subj": "",
        "Crse": "",
        "Sect": "",
        "Title": "",
        "PrimaryInstructor": "",
        "Max": 0,
        "Curr": 0,
        "Aval": 0,
        "Days": " ",
        "Begin": " ",
        "End":" ",
        "Bldg": " ",
        "Room": " ",
        "Year": 0,
        "Semester": " "
}
#open file 
f = open('jsondata.json')
#read json
data = json.load(f)
#loop on json strings
for i in data:      
    #not all the json objects are same just year and Semester are present in every object so if's on all the variables
    if("Col" in i):
        MyCustomObject['Col'] = i['Col']
    if("Crn" in i):
        MyCustomObject['Crn'] = i['Crn']
    if("Subj" in i):
        MyCustomObject['Subj'] = i['Subj']
    if("Crse" in i):
        MyCustomObject['Crse'] = i['Crse']
    if("Sect" in i):
        MyCustomObject['Sect'] = i['Sect']
    if("Title" in i):
        MyCustomObject['Title'] =  i['Title']
    if("PrimaryInstructor" in i):
        MyCustomObject['PrimaryInstructor'] =  i['PrimaryInstructor']
    if("Max" in i):
        MyCustomObject['Max'] = i['Max']
    if("Curr" in i):
        MyCustomObject['Curr'] = i['Curr']
    if("Aval" in i):
        MyCustomObject['Aval'] = i['Aval']
    if("Days" in i):
        MyCustomObject['Days'] = i['Days']
    if("Begin" in i):
        MyCustomObject['Begin'] =  i['Begin']
    if("End" in i):
        MyCustomObject['End'] =  i['End']
    if("Bldg" in i):
        MyCustomObject['Bldg'] =  i['Bldg']
    if("Room" in i):
        MyCustomObject['Room'] = i['Room']
    MyCustomObject['Year'] = i['Year']
    MyCustomObject['Semester'] = i['Semester']
    #promt nay variable value of this
    print(MyCustomObject['Bldg'])   
