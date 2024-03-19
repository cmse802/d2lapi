#!/usr/bin/env python 
# Very simple script to convert multiple line summary D2L data to a single entry.  

import pandas as pd
import argparse

def parsedata(filename='ISB204 Consents SS24.csv', outfile="ISB204_output.csv"):
    print(filename)
    df = pd.read_csv(filename)
    df.columns
    
    currentuser = {}
    users = {}
    for index, row in df.iterrows():
        if type(row['Section #']) == str: # First row of section. Save previous student and start a new one.
            if len(currentuser) > 0:
                if currentuser['id'] in users:
                    if not currentuser['Consent'] == users[currentuser['id']]['Consent']:
                        print(f"REPEAT: Student {row['Name']} Consents do not match")
                    else:
                        print(f"REPEAT: Consent Matches")
                    currentuser['Consent'] = currentuser['Consent'] and users[currentuser['id']]['Consent'] # Logical or will always be False if one is False
                else:
                    users[currentuser['id']] = currentuser
                currentuser = {}
            currentuser['Name'] = row['Section #']
            currentuser['Consent'] = False
            currentuser['id'] = ''
        else: # Use if statements to differentiate each row question. 
            if "protect your privacy" in row['Q Text']:
                currentuser['id'] = row['Answer Match']
            if type(row['Answer']) == str:
                if "Yes, I voluntarily" in row['Answer']:
                    if row['# Responses'] == 1.0:
                        currentuser['Consent'] = True
    
    
    
    new_df = pd.DataFrame.from_dict(users, orient='index')
    new_df
    
    new_df.to_csv(f"ISB204_output.csv")
    
if __main__ == "main":
    argparse parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument('filename')           # positional argument
    parser.add_argument('-c', '--count')      # option that takes a value
    parser.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag
    parsedata(filename,outfile)

