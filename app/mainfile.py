# Import function file as referenc to use defined python functions
import functionfile as f
import sys 
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
from datetime import datetime, timedelta
from datetime import date

import math

# Function to get the input arguments from the nodejs file
patent_number = sys.argv[1]
print("Processing patent number: "+sys.argv[1])

# variables
number_of_independent_claims = 0.0
number_of_dependent_per_independent_claims = 0.0
length_of_firstclaim = 0.0
number_of_reassignments = 0.0
number_of_litigations = 0.0
lowest_number_of_mention_of_biwords = 0.0
size_of_family = 0.0
age_of_patent = 0.0
number_of_forward_citations = 0.0
industrial_potential_of_the_patent = 0.0
number_of_classifications = 0.0

# independendent claim
min_independent_claim = 1
max_independent_claim = 6
w1_independent_claim = 7.970895408

# dependent per independent claim
min_dependent_per_independent_claim = 0
max_dependent_per_independent_claim = 8
w2_dependent_per_independent_claim = 7.59352409

# length of first claim
# min_length_of_first_claim = 10
# max_length_of_first_claim = 40
w3_length_of_first_claim = 17.23925653

# No. of reassignments
min_assignment_value = 0
max_assignment_value = 4
w4_assignment = 3.423171116

# No. of litigation
min_no_of_litigation = 0
max_no_of_litigation = 15
w5_litigation = 10.28223147

# Lowest number of biwords
min_no_of_biwords = 0
max_no_of_biwords = 8
w6_no_of_biwords = 11.30111881

# size of familty
min_no_of_size_family = 0
max_no_of_size_family = 8
w7_no_of_size_family = 5.011335261

# Age of patent
min_no_of_age_patent = 0
max_no_of_age_patent = 20
w8_no_of_age_patent = 8.288146129

# forward citations
min_no_of_citations = 0
max_no_of_citations = 40
w9_no_of_citations = 19.14373452

# industry potential
min_industrial_potential = 0
max_industrial_potential = 1
w10_industrial_potential = 7.00898949

# Number of classifications
min_number_of_classifications = 1
max_number_of_classifications = 8
w11_number_of_classifications = 3.838035323

contribution_list = []

def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

def check_bound(value, min, max):
    if(float(value) > float(max)):
        value = float(max)
    elif(float(value) < float(min)):
        value = float(min)
    return value

def get_normalized(value, min, max):
    normalized = (float(value) - min)/(max - min)
    normalized = float(normalized)
    return normalized

def add_contribution(value, weight):
    contri = float(value) * weight
    contribution_list.append(contri)

def get_final_score(contribution_list):
    sum = 0.0
    for c in contribution_list:
        sum = sum + c
    if(sum):
        score = ( sum / 101.100438147 )*100
    return score

# Function used to remove the repeated elements in the classification list
def substringSieve(string_list):
    string_list.sort(key=lambda s: len(s), reverse=True)
    out = []
    for s in string_list:
        if not any([s in o for o in out]):
            out.append(s)
    return out

# ur = "https://patents.google.com/patent/"+patent_number

if(patent_number[0:2].isalpha()):
    ur = "https://patents.google.com/patent/"+patent_number
else:
    ur = "https://patents.google.com/patent/US"+patent_number

# ur = ur.strip()

def main():
    headers = requests.utils.default_headers()
    headers.update({
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
	})
    content = requests.get(ur, headers=headers)
    #######################################################################
    # get the soup of tags in html page
    #######################################################################

    print("<html><head><title>PodRank</title></head><body>")

    soup = BeautifulSoup(content.text,'html.parser')
    if(soup.title.get_text() in "Error 404 (Not Found)!!1"):
        print("<p>Not found Patent Number: "+ur+"</p>")
    else:
        print()
        print("<p>---------------------------------------------</p>")
        print("<p>Patent - <a href="+ur+">"+ur+"</a></p>")

    try:
        dependentTextSet, number_of_dependent_claims = f.get_the_dependent_method_and_system_claim(soup)
        number_of_independent_claims = f.get_the_number_of_independent_claims(soup, dependentTextSet)
        # print("<p>---------------------------------------------</p>")
        print("<p>Number of independent claim: "+str(number_of_independent_claims)+"</p>")
        number_of_independent_claims = check_bound(number_of_independent_claims, min_independent_claim, max_independent_claim)
        # print("<p>Number of independent claim with check bound: "+str(number_of_independent_claims)+"</p>")
        normalized_number_of_independent_claims = get_normalized(number_of_independent_claims, min_independent_claim, max_independent_claim)
        # print("<p>Normalized number of independent claim: "+str(normalized_number_of_independent_claims)+"</p>")
        add_contribution(normalized_number_of_independent_claims, w1_independent_claim)
    except Exception as err:
        pass
        # print('Exception occurred in the function, Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err).__name__, err)

    # coding required 
    try:    
        number_of_dependent_per_independent_claims = f.get_dependents_per_independent_claims(number_of_independent_claims, number_of_dependent_claims)
        # print("<p>---------------------------------------------</p>")
        print("<p>Number of dependent per independent claim: "+str(number_of_dependent_per_independent_claims)+"</p>")
        number_of_dependent_per_independent_claims = check_bound(number_of_dependent_per_independent_claims, min_dependent_per_independent_claim, max_dependent_per_independent_claim)
        # print("<p>Number of independent claim with check bound: "+str(number_of_dependent_per_independent_claims)+"</p>")
        normalized_number_of_dependent_per_independent_claims = get_normalized(number_of_dependent_per_independent_claims, min_dependent_per_independent_claim, max_dependent_per_independent_claim)
        # print("<p>Normalized number of independent claim: "+str(normalized_number_of_dependent_per_independent_claims)+"</p>")
        add_contribution(normalized_number_of_independent_claims, w2_dependent_per_independent_claim)
    except Exception as err:
        pass
        # print('Exception occurred in the function, Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err).__name__, err)

    # print("<p>---------------------------------------------</p>")
    try:    
        length_of_firstclaim = f.get_the_length_of_first_claim(soup, dependentTextSet)
        print("<p>length of first claim: "+str(length_of_firstclaim)+"</p>")
        length_of_firstclaim = float(1 / length_of_firstclaim)
        # length_of_firstclaim = check_bound(length_of_firstclaim, min_length_of_first_claim, max_length_of_first_claim)
        # print("<p>length of first claim with check bound: "+str(length_of_firstclaim)+"</p>")
        # normalized_length_of_firstclaim = get_normalized(length_of_firstclaim, min_length_of_first_claim, max_length_of_first_claim)
        # print("<p>Normalized length of first claim: "+str(normalized_length_of_firstclaim)+"</p>")
        add_contribution(length_of_firstclaim, w3_length_of_first_claim)
    except Exception as err:
        pass
        # print('Exception occurred in the function, Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err).__name__, err)

    # print("<p>---------------------------------------------</p>")
    try:    
        number_of_reassignments = f.get_the_number_of_reassignments(soup)
        print("<p>Number of reassignments: "+str(number_of_reassignments)+"</p>")
        number_of_reassignments = check_bound(number_of_reassignments, min_assignment_value, max_assignment_value)
        # print("<p>Number of reassignments with check bound: "+str(number_of_reassignments)+"</p>")
        normalized_number_of_reassignments = get_normalized(number_of_reassignments, min_assignment_value, max_assignment_value)
        # print("<p>Normalized number of reassignments: "+str(normalized_number_of_reassignments)+"</p>")
        add_contribution(normalized_number_of_reassignments, w4_assignment)
    except Exception as err:
        pass
        # print('Exception occurred in the function, Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err).__name__, err)

    # print("<p>---------------------------------------------</p>")
    try:    
        number_of_litigations = f.get_the_number_of_litigations(soup)
        print("<p>Number of litigations: "+str(number_of_litigations)+"</p>")
        number_of_litigations = check_bound(number_of_litigations, min_no_of_litigation, max_no_of_litigation)
        # print("<p>Number of litigations with check bound: "+str(number_of_litigations)+"</p>")
        normalized_number_of_litigations = get_normalized(number_of_litigations, min_no_of_litigation, max_no_of_litigation)
        # print("<p>Normalized number of litigations: "+str(normalized_number_of_litigations)+"</p>")
        add_contribution(normalized_number_of_litigations, w5_litigation)
    except Exception as err:
        pass
        # print('Exception occurred in the function, Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err).__name__, err)

    # coding required 
    # print("<p>---------------------------------------------</p>")
    try:
        return_tupple = f.get_the_lowest_number_of_mention_of_biwords(soup)
        lowest_number_of_mention_of_biwords = return_tupple[0]
        biwords_found = return_tupple[1]
        print("<p>Lowest number of biwords: "+str(lowest_number_of_mention_of_biwords)+"</p>")
        lowest_number_of_mention_of_biwords = check_bound(lowest_number_of_mention_of_biwords, min_no_of_biwords, max_no_of_biwords)
        # print("<p>Lowest number of biwords with check bound: "+str(lowest_number_of_mention_of_biwords)+"</p>")
        normalized_number_of_biwords = get_normalized(lowest_number_of_mention_of_biwords, min_no_of_biwords, max_no_of_biwords)
        # print("<p>Normalized number of biwords: "+str(normalized_number_of_biwords)+"</p>")
        # print("<p>Biwords found: "+str(biwords_found)+"</p>")
        add_contribution(normalized_number_of_biwords, w6_no_of_biwords)
    except Exception as err:
        pass
        # print('Exception occurred in the function, Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err).__name__, err)

    # coding required
    # print("<p>---------------------------------------------</p>")
    try:    
        size_of_family = f.get_the_size_of_family(soup)
        print("<p>Size of family: "+str(size_of_family)+"</p>")
        size_of_family = check_bound(size_of_family, min_no_of_size_family, max_no_of_size_family)
        # print("<p>Size of family with check bound: "+str(size_of_family)+"</p>")
        normalized_size_of_family = get_normalized(size_of_family, min_no_of_size_family, max_no_of_size_family)
        # print("<p>Normalized number of forward citations: "+str(normalized_size_of_family)+"</p>")
        add_contribution(normalized_size_of_family, w7_no_of_size_family)
    except Exception as err:
        pass
        # print('Exception occurred in the function, Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err).__name__, err)

    # print("<p>---------------------------------------------</p>")
    try:    
        adjustedExpirationDate = f.get_the_adjustedexpirationdate_of_the_patent(soup)
        extPriorityDate = f.get_the_prioritydate_of_the_patent(soup)
        age_of_patent = f.get_the_age_of_the_patent(soup, adjustedExpirationDate, extPriorityDate)
        print("<p>Age of patent (in Years): "+str(age_of_patent)+"</p>")
        age_of_patent = check_bound(age_of_patent, min_no_of_age_patent, max_no_of_age_patent)
        # print("<p>Age of patent with check bound (in Years): "+str(age_of_patent)+"</p>")
        normalized_age_of_patent = get_normalized(age_of_patent, min_no_of_age_patent, max_no_of_age_patent)
        # print("<p>Normalized age of patent: "+str(normalized_age_of_patent)+"</p>")
        add_contribution(normalized_age_of_patent, w8_no_of_age_patent)
    except Exception as err:
        pass
        # print(age_of_patent)
        # print('Exception occurred in the function, Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err).__name__, err)

    # print("<p>---------------------------------------------</p>")
    try:    
        number_of_forward_citations = f.get_the_forward_citations(soup)
        print("<p>Number of forward citations: "+str(number_of_forward_citations)+"</p>")
        number_of_forward_citations = check_bound(number_of_forward_citations, min_no_of_citations, max_no_of_citations)
        # print("<p>Number of forward citations with check bound: "+str(number_of_forward_citations)+"</p>")
        normalized_number_of_forward_citations = get_normalized(number_of_forward_citations, min_no_of_citations, max_no_of_citations)
        # print("<p>Normalized number of forward citations: "+str(normalized_number_of_forward_citations)+"</p>")
        add_contribution(normalized_number_of_forward_citations, w9_no_of_citations)
    except Exception as err:
        pass
        # print('Exception occurred in the function, Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err).__name__, err)

    # print("<p>---------------------------------------------</p>")
    try:
        classificationTextList = []    
        number_of_classifications, classificationText = f.get_the_number_of_classifications(soup)
        # print("Classification found: ")
        classificationTextList = classificationText.split(',')
        classificationTextList = list(set(classificationTextList))
        classificationTextList = substringSieve(classificationTextList)
        # print(classificationTextList)
        print("<p>Number of classifications: "+str(len(classificationTextList))+"</p>")
        number_of_classifications = check_bound(len(classificationTextList), min_number_of_classifications, max_number_of_classifications)
        # print("<p>Number of classifications with check bound: "+str(len(classificationTextList))+"</p>")
        normalized_number_of_classifications = get_normalized(len(classificationTextList), min_number_of_classifications, max_number_of_classifications)
        # print("<p>Normalized number of classifications: "+str(normalized_number_of_classifications)+"</p>")
        add_contribution(normalized_number_of_classifications, w11_number_of_classifications)
    except Exception as err:
        pass
        # print('Exception occurred in the function, Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err).__name__, err)

    # coding required
    potential_list = ['H06F01']
    # print("<p>---------------------------------------------</p>")
    try:    
        industrial_potential = f.get_the_industrial_potential(potential_list, classificationTextList)
        print("<p>Industrial potential: "+str(industrial_potential)+"</p>")
        industrial_potential = check_bound(industrial_potential, min_industrial_potential, max_industrial_potential)
        # print("<p>Industrial potential with check bound: "+str(industrial_potential)+"</p>")
        normalized_industrial_potential = get_normalized(industrial_potential, min_industrial_potential, max_industrial_potential)
        # print("<p>Normalized industrial potential: "+str(normalized_industrial_potential)+"</p>")
        add_contribution(normalized_industrial_potential, w10_industrial_potential)
    except Exception as err:
        pass
        # print('Exception occurred in the function, Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err).__name__, err)

    # Calling rank calculator function
    podrank = get_final_score(contribution_list)
    print("<p>---------------------------------------------</p>")
    print("<p><b>Calculated score of the patent: "+str(truncate(podrank, 4))+"</b></p>")
    print("<p><a href='./'>click here to check another patent</a></p>")
    print("</body></html>")

main()