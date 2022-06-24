import requests
from bs4 import BeautifulSoup
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize as token
from numpy.core.numeric import False_

# Acquire movie scripts from IMSDb using Beautifulsoup
# Remove punctuaion as well as stopword
# Tokenization

#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('wordnet')
#************************script section**************************
url = "https://imsdb.com/scripts/Devil-Wears-Prada,-The.html"
page = requests.get(url)

if page.status_code == requests.codes.ok:
    soup = BeautifulSoup(page.text, 'html.parser')
    script = soup.find('tr', class_="scrtext")
    script = soup.find('pre')

    file = open("script.txt", 'r+')
    file.truncate(0)
    file.close()
#*************************preprocessing**************************
    stop_list = set(stopwords.words('english'))
    scene_text = ["MUSIC", "UP", "FADE", "OUT", "CONTINUED", "OMITTED", "FADE", "IN", "EXT", "CONTD", "INT", "TH"
    , "In", "Progress", "nd", "th", "The", "Devil", "Wears", "Prada", "Blue"]

    for script_text in script:
        if script_text.name != 'b':
            script_text = re.sub(r'[,.:"&�\'\(\)\/\-\d]', '', script_text)
            script_text = re.sub(r'\s+([A-Z][A-Z]?)\s+', ' ', script_text)
            script_text = re.sub(r'\s+', ' ', script_text)
            tokenized_script = token(script_text)
            valid = False
            for word in tokenized_script:
                if word not in scene_text:
                    valid = True
                    file = open("script.txt", 'a')
                    file.write(word + ' ')
                    file.close()

            if valid:
                file = open("script.txt", 'a')
                file.write('\n')
                file.close()

        else:
            script_text.string = re.sub(r'[,.:"#&�\'\(\)\/\-\d]', '', script_text.string)
            script_text.string = re.sub(r'\s+', ' ', script_text.string)
            tokenized_script = token(script_text.string)
            for word in tokenized_script:
                if word not in scene_text:
                    file = open("script.txt", 'a')
                    file.write(word + ' ')
                    file.close()
#****************************************************************

