import PyPDF2
import csv

categoryNames = ["Child Labour Total", "Child Labour Male", "Child Labour Female", "Child marriage <15",
                 "Child Marriage <18", "Birth Registration Total", "FGM Prevalence Women",
                 "FGM Prevalence Girls", "FGM Support", "Wife Beating Justification Male",
                 "Wife Beating Justification Female", "Violent Discipline Total", "Violent Discipline Male",
                 "Violent Discipline Female"]
outputList = []

with (open("Table9.pdf", "rb") as pdf_ptr):
    pdf_file_object = PyPDF2.PdfReader(pdf_ptr)
    page_content = []
    for i in range(len(pdf_file_object.pages)):
        page_content += pdf_file_object.pages[i].extract_text()
    page_content = "".join(page_content)
    page_content = page_content.replace("TABLE 9", "")
    page_content = page_content.replace("CHILD PROTECTION", "")
    page_content = page_content.replace("CHILD PROTECTION >>", "")
    page_content = page_content.replace("–", "0")
    inputList = page_content.split("\n")
    inputList2 = []
    for i, item in enumerate(inputList):
        inputList[i] = inputList[i].split(" ")
        inputList[i] = list(filter(lambda item2: item2.isnumeric() or len(item2) > 1, inputList[i]))
        for index, x in enumerate(inputList[i]):
            if x.isnumeric():
                inputList[i][index]  = int(inputList[i][index])
        if len(inputList[i]) >= 15 and sum(isinstance(x, int) for x in inputList[i]) == 14:
            inputList2.append(inputList[i])

    print(inputList2)
    holderList = []
    outputList = []
    for data in inputList2:
        outputLine = [""]
        for i, value in enumerate(data):
            if isinstance(value, str):
                if outputLine[0] == "":
                    outputLine[0] += value
                else:
                    outputLine[0] += " "+value
            else:
                outputLine.append(value)
        for ind, amount in enumerate(outputLine[1:]):
            if amount!=0:
                outputList.append([outputLine[0], categoryNames[ind], amount])
        if outputLine[0] == "Zimbabwe":
            break
    pdf_ptr.close()

    # Open a CSV file named "group10Lab4.csv" for writing
    fptr = open("group10Lab5.csv", "w", newline="")
    writer = csv.writer(fptr)
    # Write the data from outputList to the CSV file.
    writer.writerows(outputList)
    fptr.close()

    # Open the CSV file "group10Lab4.csv" for reading.
    fptr2 = open("group10Lab4.csv", "r")
    # Print the number of rows in the CSV file (counting the number of lines).
    print(sum(1 for row in fptr2))
    # Close the CSV file.
    fptr2.close()
