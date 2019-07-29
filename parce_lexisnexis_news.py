
##
#The script to parse news articles into a csv form
##
from bs4 import BeautifulSoup
import re
import csv
import os
import path
from pathlib import Path
import pdb

def name_finder(rep_voice):
    '''
    Use regex to extract names and party affiliation.
    '''
    #pattern = re.compile(r"REP.(\s[A-Z]+\s)")
    pattern2 = re.compile(r"REP.\s+([A-Z]+)\s+([A-Z]+)")
    party_pattern = re.compile(r"\([A-Z-]+\)")

    first = []
    last = []
    parties = []
    
    for l in rep_voice:
        match = pattern2.search(l)
        party = party_pattern.search(l)
#         first.append(match.group(1))
#         last.append(match.group(2))
        
        if match:
            first.append(match.group(1))
            last.append(match.group(2))
        if party:
            parties.append(party.group(0))
        else:
            parties.append(None)
            
        
    return first, last, parties


def extract_text(doc_name):
    '''
    return a list of sentences the speakers said 
    and the date of the news
    
    '''
    with open(doc_name, "r") as f:
        soup = BeautifulSoup(f, "lxml")
        
        date = soup.find_all("p", class_= "SS_DocumentInfo")[-1].text
        
        voice = []
        for p in soup.find_all("p"):
            voice.append(p.text)
       # print(voice)

        rep_voice = []
        for l in range(len(voice)):
            if re.search(r"^REP\.\s.+:", voice[l]):
                rep_voice.append(voice[l])
#                 if not re.match(r"^[A-Z]{2:}", voice[l+1]):
#                     rep_voice.append(voice[l+1])

    
    return rep_voice, date


def main():

    # PATH = Path(your_path)
    # file_path = PATH/"pbs_nexis"
    # os.chdir(file_path)

    with open("final.csv", "w") as rf:
        csv_writer = csv.writer(rf)
        csv_writer.writerow(["Firstname", "Lastname", "Party", "Date", "Text"])
        for f in os.listdir():
            if f.endswith("htm"):
                rep_voice, date = extract_text(f)
                #pdb.set_trace()
                first, last, party = name_finder(rep_voice)
                for i in list(zip(first, last, party, [date]*len(rep_voice), rep_voice)):
                    csv_writer.writerow(i)
                    #   print(f"finished {f}")

if __name__ == "__main__":
    main()
