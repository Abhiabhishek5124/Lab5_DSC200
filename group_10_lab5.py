# Lab4-DSC200
# Nathan Reed Abhishek Shrestha
# Write a program that reads data from a pdf a list of child abuse events for several countries
# and write the data into a csv file.

# import libraries for opening pdf and csv files
import PyPDF2
import csv

# Define a list of category names that will be used later
categoryNames = ["Child Labour Total", "Child Labour Male", "Child Labour Female", "Child marriage <15",
                 "Child Marriage <18", "Birth Registration Total", "FGM Prevalence Women",
                 "FGM Prevalence Girls", "FGM Support", "Wife Beating Justification Male",
                 "Wife Beating Justification Female", "Violent Discipline Total", "Violent Discipline Male",
                 "Violent Discipline Female"]
# Open the pdf and assign pointer
with (open("Table9.pdf", "rb") as pdf_ptr):
    # Create a reader object for pdf
    pdf_file_object = PyPDF2.PdfReader(pdf_ptr)
    # list to hold content of pages
    page_content = []
    # loop through pages
    for pageNum in range(len(pdf_file_object.pages)):
        # for each page extract the text and add it to the page content.
        page_content += pdf_file_object.pages[pageNum].extract_text()
    # close the pdf
    pdf_ptr.close()
    # join the page contents (individual characters)
    page_content = "".join(page_content)
    # Remove the phrase TABLE 9
    page_content = page_content.replace("TABLE 9", "")
    # This joins the countries in the table where the name is across two lines
    page_content = page_content.replace(" \n", " ")
    # Replace en dashes with 0
    page_content = page_content.replace("–", "0")
    # Move the page content into a list where each line is a row in the list
    inputList = page_content.split("\n")
    # second input list for filtered data
    inputList2 = []
    for i, item in enumerate(inputList):
        # Each word in the input list will be split
        inputList[i] = inputList[i].split(" ")
        # Filter out all single character items
        inputList[i] = list(filter(lambda item2: item2.isnumeric() or len(item2) > 1, inputList[i]))

        # set all numeric values to integers
        for index, subItem in enumerate(inputList[i]):
            if subItem.isnumeric():
                inputList[i][index] = int(inputList[i][index])
        # save only the rows that represent a country
        if sum(isinstance(x, int) for x in inputList[i]) == 14:
            inputList2.append(inputList[i])
    # output list will hold what's actually outputted
    outputList = [["CountryName", "CategoryName", "CategoryTotal"]]
    # iterate through the values representing countries
    for data in inputList2:
        # outputLine will hold a collapsed version of data from inputList2
        outputLine = [""]
        # start variable to signify if value to be added is country name
        start = True
        for i, value in enumerate(data):
            # If the country name is multiple strings, combine into first item in outputLine
            # after country name is added, append the integer values to the outputLine
            if isinstance(value, str) and start:
                if outputLine[0] == "":
                    outputLine[0] += value
                else:
                    outputLine[0] += " "+value
            else:
                start = False
                if isinstance(value, int):
                    outputLine.append(value)
        # for each amount in the output line add the appropriate "event" to the outputList
        for ind, amount in enumerate(outputLine[1:]):
            if amount != 0:
                outputList.append([outputLine[0], categoryNames[ind], amount])
        # The last country in the pdf is Zimbabwe, so we stop to prevent adding summary info
        if outputLine[0] == "Zimbabwe":
            break

# Open a CSV file named "group10Lab5.csv" for writing
fptr = open("group10Lab5.csv", "w", newline="")
writer = csv.writer(fptr)
# Write the data from outputList to the CSV file.
writer.writerows(outputList)
fptr.close()

# Open the CSV file "group10Lab5.csv" for reading.
fptr2 = open("group10Lab5.csv", "r")
# Print the number of rows in the CSV file (counting the number of lines).
print(sum(1 for row in fptr2))
# Close the CSV file.
fptr2.close()
