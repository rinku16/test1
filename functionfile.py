import nltk
from nltk.corpus import stopwords
#for generating sentence token
from nltk.tokenize import sent_tokenize
#for generating word token
from nltk.tokenize import word_tokenize
# BeautifulSoup for scraping and Requests to make HTTP requests.
from bs4 import BeautifulSoup 
# BeautifulSoup is in bs4 package 
import requests
#Counter class For Getting Most Occured Biwords
from collections import Counter
#FOR MAKING DATA FRAME AND WRITING THE PATENT EXTRACTED DATA TO CSV FILE
from pandas import DataFrame
import pandas as pd
import os
import os.path
from os import path
import re
from datetime import date
import datetime
from datetime import timedelta

import sys 

# Get the length of first claim
# def get_the_length_of_first_claim():

# Get the number of reassignments
# def get_the_number_of_reassignments():

# Get the number of litigations
# def get_the_number_of_litigations():

# CODING REQUIRED
# Get the lowest no. of mention of biwords
# def get_the_lowest_number_of_mention_of_biwords(soup):


# Get the age of the patent
# def get_the_age_of_the_patent():

# Get the forward citations
# def get_the_forward_citations():

# Get the number of classifications
# def get_the_number_of_classifications():

# Get the industrial potential
def get_the_industrial_potential(classificationList, potential_list):

	result = 1
	for x in classificationList: 
		for y in potential_list: 
			# if one common 
			if(x in y):
				result = 1
				return result
	return result

# Get dependents per independent claims
def get_dependents_per_independent_claims(number_of_dependent_claims, number_of_independent_claims):
	dependents_per_independent_claims = number_of_dependent_claims/number_of_independent_claims
	return dependents_per_independent_claims

# Get the size of the family
def get_the_size_of_family(soup):
    applicationCountriesList = []
    applicationText = ""
    liTags = soup.find_all('li', {'itemprop':'application'})
    for liTag in liTags:
        spanTags = liTag.find_all('span')
        for spanTag in spanTags:
            if(spanTag["itemprop"] == "countryCode"):
                applicationCountriesList.append(spanTag.get_text())

    countriesList = Counter(applicationCountriesList)
    countriesListText = str(countriesList)
    countriesListText = countriesListText.lstrip("Counter(")
    countriesListText = countriesListText.rstrip(")")
    countriesListTextName = countriesListText
    numberOfCountries = str(len(countriesList.keys()))
    totalNumberOfApplicationInCountries = str(len(liTags))

    countriesListTextName = countriesListText
    numberOfCountries = str(len(countriesList.keys()))
    totalNumberOfApplicationInCountries = str(len(liTags))

    return totalNumberOfApplicationInCountries

#########################################################
# Parameter 1 start
#########################################################

def get_the_dependent_method_and_system_claim(soup):
	dependentTextList = []
	try:
		Tags = soup.find_all('div', {'class':'claim-dependent'})
		# to find the dependent claims
		for t in Tags:
			dependentText = t.get_text()
			dependentText = re.sub("[^a-zA-Z0-9\s\,\.\(\)\[\]-]+","", dependentText)
			dependentTextList.append(dependentText.strip())

		dependentTextSet = set(dependentTextList)
		numberOfDependentClaims = len(dependentTextList)
	except:
		dependentTextSet = set(dependentTextList)
		numberOfDependentClaims = len(dependentTextList)

	dependentMethodClaimCount = 0
	dependentSystemtClaimCount = 0

	#to print the dependent claims
	for t in dependentTextList:
		if("method" in t):
			dependentMethodClaimCount = dependentMethodClaimCount + 1
		else:
			dependentSystemtClaimCount = dependentSystemtClaimCount + 1

	numberOfDependendentMethodClaims = str(dependentMethodClaimCount)
	numberOfDependentSystemClaims = str(dependentSystemtClaimCount)

	return dependentTextSet, numberOfDependentClaims

def get_the_number_of_independent_claims(soup, dependentTextSet):

	independentTextList = []
	try:
		try:
			Tags = soup.find_all('div', {'class':'claim'})
			#to find the independent claims
			for t in Tags:
				independentText = t.get_text()
				independentText = re.sub("[^a-zA-Z0-9\s\,\.\(\)\[\]-]+","", independentText)
				independentTextList.append(independentText.strip())
		except:
			independentTextList = []

		# to remove the duplicates in list
		independentTextSet = set(independentTextList)
		# to convert the set into list
		independentTextList = list(independentTextSet)
		# to find the symmetric difference between sets having the claims and dependent claims
		independentClaimSet = independentTextSet.symmetric_difference(dependentTextSet)
		# to make the independent claims list
		independentTextList = list(independentClaimSet)
		# to print the number of independent claims
		# print("Number of independent claims: "+str(len(independentTextList)))
		independentClaim = ""
		independentTextList.sort()
		independentMethodClaimCount = 0
		independentSystemtClaimCount = 0
		for t in independentTextList:
			if("method" in t):
				independentMethodClaimCount = independentMethodClaimCount + 1
			else:
				independentSystemtClaimCount = independentSystemtClaimCount + 1
			independentClaim = independentClaim + "\n" + t
		independentClaim = re.sub("[^a-zA-Z0-9\s\,\.\(\)\[\]-]+","",independentClaim)
		independentClaim = re.sub("\s+"," ",independentClaim)

		numberOfIndependentClaims = len(independentTextList)
		numberOfIndependentMethodClaims = str(independentMethodClaimCount)
		numberOfIndependentSystemClaims = str(independentSystemtClaimCount)

		#For length of claim 1
		independentClaim1Text = independentTextList[0]
		tokenizedWordOfClaim1 = word_tokenize(independentClaim1Text)
		lengthOfClaim1 = str(len(tokenizedWordOfClaim1))
	except:
		numberOfIndependentClaims = ""
		numberOfIndependentMethodClaims = ""
		numberOfIndependentSystemClaims = ""
		independentTextList = []
		lengthOfClaim1 = ""
		independentClaim = ""

	return numberOfIndependentClaims

#########################################################

def get_the_length_of_first_claim(soup, dependentTextSet):

	independentTextList = []
	try:
		try:
			Tags = soup.find_all('div', {'class':'claim'})
			#to find the independent claims
			for t in Tags:
				independentText = t.get_text()
				independentText = re.sub("[^a-zA-Z0-9\s\,\.\(\)\[\]-]+","", independentText)
				independentTextList.append(independentText.strip())
		except:
			independentTextList = []

		# to remove the duplicates in list
		independentTextSet = set(independentTextList)
		# to convert the set into list
		independentTextList = list(independentTextSet)
		# to find the symmetric difference between sets having the claims and dependent claims
		independentClaimSet = independentTextSet.symmetric_difference(dependentTextSet)
		# to make the independent claims list
		independentTextList = list(independentClaimSet)
		# to print the number of independent claims
		# print("Number of independent claims: "+str(len(independentTextList)))
		independentClaim = ""
		independentTextList.sort()
		independentMethodClaimCount = 0
		independentSystemtClaimCount = 0
		for t in independentTextList:
			if("method" in t):
				independentMethodClaimCount = independentMethodClaimCount + 1
			else:
				independentSystemtClaimCount = independentSystemtClaimCount + 1
			independentClaim = independentClaim + "\n" + t
		independentClaim = re.sub("[^a-zA-Z0-9\s\,\.\(\)\[\]-]+","",independentClaim)
		independentClaim = re.sub("\s+"," ",independentClaim)

		numberOfIndependentClaims = len(independentTextList)
		numberOfIndependentMethodClaims = str(independentMethodClaimCount)
		numberOfIndependentSystemClaims = str(independentSystemtClaimCount)

		#For length of claim 1
		independentClaim1Text = independentTextList[0]
		tokenizedWordOfClaim1 = word_tokenize(independentClaim1Text)
		lengthOfClaim1 = str(len(tokenizedWordOfClaim1))
	except:
		numberOfIndependentClaims = ""
		numberOfIndependentMethodClaims = ""
		numberOfIndependentSystemClaims = ""
		independentTextList = []
		lengthOfClaim1 = ""
		independentClaim = ""

	return lengthOfClaim1

#########################################################

def get_the_number_of_reassignments(soup):
	assignedList = []
	try:
		assignEventsTags = soup.find_all('dd', {'itemprop':'events'})
		for tag in assignEventsTags:
			assignTags = tag.find_all('span', {'itemprop':'title'})
			for assig in assignTags:
				if("Assign" in assig.get_text() or "assign" in assig.get_text()):
					assignedList.append(assig.get_text())			
	except:
		assignedList = []

	assignedSet = set(assignedList)
	assignedList = list(assignedSet)
	numberOfReassignment = len(assignedList)

	if(numberOfReassignment):
		numberOfReassignment = numberOfReassignment - 1

	return numberOfReassignment

##########################################################

def get_the_number_of_litigations(soup):
	caseList = []
	caseText = ""
	try:
		caseEventsTags = soup.find_all('dd', {'itemprop':'events'})

		for tag in caseEventsTags:
			casesTags = tag.find_all('span', {'itemprop':'title'})
			for case in casesTags:
				if("case" in case.get_text()):
					caseList.append(case.get_text())
					caseText = caseText + ", " + case.get_text()
					# print(case.get_text())

		caseText = caseText.lstrip(", ")

	except:
		caseText = ""
		caseList = []

	numberOfPreviousLitigation = str(len(caseList))
	return numberOfPreviousLitigation

##############################################################

def get_the_prioritydate_of_the_patent(soup):
	extPriorityDate = ""
	try:
		extPriorityDate = soup.find('time', {'itemprop':'priorityDate'}).get_text()
	except:
		extPriorityDate = ""

	return extPriorityDate

def get_the_adjustedexpirationdate_of_the_patent(soup):
	#get the expiry date
	try:
		ddTags = soup.find_all('dd', {'itemprop':'events'})
		for tag in ddTags:
			# print(tag)
			if(tag.find('span', {'itemprop':'title'}).get_text() in "Adjusted expiration"):
				adjustedExpirationDate = tag.find('time', {'itemprop':'date'}).get_text()
			elif(tag.find('span', {'itemprop':'title'}).get_text() in "Anticipated expiration"):
				adjustedExpirationDate = tag.find('time', {'itemprop':'date'}).get_text()
			else:
				adjustedExpirationDate = ""
				# print(adjustedExpirationDate)
	except:
		adjustedExpirationDate = ""
	return adjustedExpirationDate

def get_the_age_of_the_patent(soup, adjustedExpirationDate, extPriorityDate):
	try:
		datetimeFormat = "%Y-%m-%d %H:%M:%S.%f"
		currentDate = datetime.datetime.now()
		currentDate = str(currentDate)[0:11]+" 00:00:00.000"
		extPriorityDate = extPriorityDate+" 00:00:00.000"
		diff = datetime.datetime.strptime(currentDate, datetimeFormat) - datetime.datetime.strptime(extPriorityDate, datetimeFormat)
		patentAge = float(diff.days/365)
	except Exception as err:
		return err

	return patentAge

####################################################################

#  Forward citations numbers
def get_the_forward_citations(soup):

	patentCitedByTextList = []
	try:
		forwardRefTags = soup.find_all('tr', {'itemprop':'forwardReferencesOrig'})
		for tag in forwardRefTags:
			patentNumberTags = tag.find_all('span', {'itemprop':'publicationNumber'})
			for t in patentNumberTags:
				try:
					patentCitedByNumber = t.get_text() + t.parent.find_next_sibling('span').get_text()
					patentCitedByTextList.append(patentCitedByNumber)
				except:
					patentCitedByNumber = t.get_text()
					patentCitedByTextList.append(patentCitedByNumber)

		forwardRefFamilyTags = soup.find_all('tr', {'itemprop':'forwardReferencesFamily'})

		for tag in forwardRefFamilyTags:
			patentNumberTags = tag.find_all('span', {'itemprop':'publicationNumber'})
			for t in patentNumberTags:
				try:
					patentCitedByNumber = t.get_text() + t.parent.find_next_sibling('span').get_text()
					patentCitedByTextList.append(patentCitedByNumber)
				except:
					patentCitedByNumber = t.get_text()
					patentCitedByTextList.append(patentCitedByNumber)

		numberOfForwardCitation = len(patentCitedByTextList)

		patentCitedByText = ""
		for l in patentCitedByTextList:
			patentCitedByText = patentCitedByText + ", " + l
		
		patentCitedByText = patentCitedByText.lstrip(", ")
	except:
		numberOfForwardCitation = ""
		patentCitedByText = ""

	return numberOfForwardCitation

####################################################################
def get_the_number_of_classifications(soup):
	classificationText = ""
	classificationTextList = []
	try:
		Tags = soup.find_all('span',{'itemprop':'Code'})

		for t in Tags:
			if('/' in t.get_text()):
				classificationText = classificationText + ", " + t.get_text()
				classificationTextList.append(t.get_text())

		numberOfClassification = len(classificationTextList)
		classificationText = classificationText.lstrip(", ")
	except:
		classificationText = ""
		classificationTextList = []
	return numberOfClassification, classificationText

#####################################################################
# Functionality for getting lowest number of biwords

def get_dependent_claims(soup):
	dependentTextList = []
	try:
		Tags = soup.find_all('div', {'class':'claim-dependent'})
		# to find the dependent claims
		for t in Tags:
			dependentText = t.get_text()
			dependentText = re.sub("[^a-zA-Z0-9\s\,\.\(\)\[\]-]+","", dependentText)
			dependentTextList.append(dependentText.strip())
		dependentTextSet = set(dependentTextList)
		numberOfDependentClaims = len(dependentTextList)
	except:
		dependentTextSet = set(dependentTextList)
		numberOfDependentClaims = len(dependentTextList)

	return dependentTextList, dependentTextSet

def get_independent_claims(soup, dependentTextSet):
    independentTextList = []
    Tags = soup.find_all('div', {'class':'claim'})
    #to find the independent claims
    for t in Tags:
        independentText = t.get_text()
        independentText = re.sub("[^a-zA-Z0-9\s\,\.\(\)\[\]-]+","", independentText)
        independentTextList.append(independentText.strip())

    # to remove the duplicates in list
    independentTextSet = set(independentTextList)
    # to convert the set into list
    independentTextList = list(independentTextSet)
    # to find the symmetric difference between sets having the claims and dependent claims
    independentClaimSet = independentTextSet.symmetric_difference(dependentTextSet)
    # to make the independent claims list
    independentTextList = list(independentClaimSet)
    return independentTextList

def get_description_text(soup):
    # get the description list
    descriptionHeading = soup.find_all('heading', {'':''})
    descriptionCompleteText = ""
    descriptionTextList = []
    for tag in descriptionHeading:
        if("TECHNICAL FIELD" in tag.get_text() or "FIELD OF THE INVENTION" in tag.get_text() or "FIELD" in tag.get_text() or "BACKGROUND" in tag.get_text() or "CROSS-REFERENCE" in tag.get_text() or "CROSS REFERENCE" in tag.get_text() or "cross reference" in tag.get_text() or "SUMMARY" in tag.get_text() or "BRIEF DESCRIPTION" in tag.get_text() or "DETAILED DESCRIPTION" in tag.get_text()):
            descriptionCompleteText = descriptionCompleteText + " " + tag.parent.get_text()
            descriptionTextList.append(tag.parent.get_text())

    descriptionTextList = list(set(descriptionTextList))
    return descriptionTextList

# Function to get the output string using the list
def get_string(inputlist):
    output_string = ""
    if(len(inputlist)):    
        for ele in inputlist:
            output_string = output_string+" "+ele
    output_string = re.sub("[^a-zA-Z0-9\s\,\.\(\)\[\]-]+","", output_string)
    output_string = re.sub("\s+"," ", output_string)
    return output_string

# Function to return the biwords found in the inputstring
def get_biwords(inputstring):
    #sentence tokenization of all text
    tokenizedTextList = sent_tokenize(inputstring)
    #bigrams list
    bigramsText = [(ele, tex.split()[i+1]) for tex in tokenizedTextList for i,ele in enumerate(tex.split()) if i < len(tex.split())-1]
    #list for filtering the stopwords from biwords  
    biwords_in_string = []
    # get the english stop words 
    stop_words = set(stopwords.words("english"))
    # removing stopwords from the biwords of claims
    for i in range(0, len(bigramsText)):
        if(bigramsText[i][0] not in stop_words):
            if(bigramsText[i][1] not in stop_words):
                biword_to_append = bigramsText[i][0]+" "+bigramsText[i][1].rstrip('.')
                if not ("(" in biword_to_append or ")" in biword_to_append):
                    biwords_in_string.append(biword_to_append)
                    
    # code to remove the biwords of claims having digits
    new_biwords_in_string = [item for item in biwords_in_string if not any(c.isdigit() for c in item)]
    get_biwords_list = []
    get_biwords_set = set()
    #tagging each biword of claims with adjective (JJ) and noun (NN)
    listBiword = nltk.pos_tag(new_biwords_in_string)
    #for extracting only the adjective and noun
    for l in listBiword:
        if(l[1] in 'NN' or l[1] in 'JJ'):
            get_biwords_list.append(l[0])
            get_biwords_set.add(l[0])
    return get_biwords_list

# Function to count number of time occurences of given biwords
def biword_counter(biword, description_list):
    count = 0
    for ele in description_list:
        if(biword in ele):
            count = count + 1
    return count

def get_pos(testword):
    return nltk.pos_tag(list(testword))[0][1]

def get_the_lowest_number_of_mention_of_biwords(soup):

    try:
        dependentTextList, dependentTextSet = get_dependent_claims(soup)
        independentTextList = get_independent_claims(soup, dependentTextSet)
        combined_list = dependentTextList + independentTextList
        combined_claim_string = get_string(combined_list)
        unique_biwords_list = list(set(get_biwords(combined_claim_string)))
        descriptionTextList = get_description_text(soup)
        descriptionTextString = get_string(descriptionTextList) + " " + combined_claim_string
        descriptionSentenceList = sent_tokenize(descriptionTextString)

        # For calculating the frequency
        biword_counter_dictionary = {}

        for ele in unique_biwords_list:
            count = biword_counter(ele, descriptionSentenceList)
            biword_counter_dictionary[ele] = count

        sorted_biword_counter_dict = {}
        sorted_keys = sorted(biword_counter_dictionary, key=biword_counter_dictionary.get) 

        # print("Sorted keys: ")
        # Keys_list = nltk.pos_tag(sorted_keys)

        filtered_dict = {}
        new_dict = {}

        for k in sorted_keys:
            ks = k.split(" ")
            if("," not in ks[0] and "," not in ks[1]):
                if(get_pos(ks[0]) in ('NN') and get_pos(ks[1]) in ('NN')):
                    new_dict[k] = biword_counter_dictionary[k]

        # print(new_dict)
        lowest_number = min(new_dict.values())

    except Exception as err:
        print('Error on line: {}'.format(sys.exc_info()[-1].tb_lineno), type(err).__name__, err)

    return lowest_number, new_dict