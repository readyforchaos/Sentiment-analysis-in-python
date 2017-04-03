# The script MUST contain function: azureml_main which works as the entry point for this module.

# Import pandas, regular expression and porter2 for stemming 
import pandas as pd
import re
from porter2 import stem

# Removing stop words and other words which are not useful
words_to_ignore = ['.', ',', ':', ';', '(', ')', '?', '!', 'hei', '@', '...', "''", '-', '``', '-.', '&', 'nbsp', '--', '{', '}', '[', ']', '/', '%', '*', '+', '<', '>', 'og', 'i', 'jeg', 'det', 'at', 'en', 'et', 'den', 'til', 'er', 'som', 'på', 'de', 'med', 'han', 'av', 'ikk', 'ikkj', 'der', 'så', 'var', 'meg', 'seg', 'men', 'ett', 'har', 'om', 'vi', 'min', 'mitt', 'ha', 'hadd', 'hun', 'nå', 'over', 'da', 'ved', 'fra', 'du', 'ut', 'sin', 'dem', 'oss', 'opp', 'man', 'kan', 'han', 'hvor', 'ell', 'hva', 'skal', 'selv', 'sjøl', 'her', 'all', 'vil', 'bli', 'ble', 'blei', 'blitt', 'kunn', 'inn', 'når', 'vær', 'kom', 'noen', 'noe', 'vill', 'der', 'som', 'der', 'kun', 'ja', 'ett', 'ned', 'skull', 'denn', 'for', 'deg', 'si', 'sin', 'sitt', 'mot', 'å', 'meg', 'hvorfor', 'dett', 'diss', 'uten', 'hvordan', 'ing', 'din', 'ditt', 'blir', 'samm', 'hvilk', 'hvilk', 'sånn', 'inni', 'mellom', 'vår', 'hver', 'hvem', 'vor', 'hvis', 'båd', 'bar', 'enn', 'fordi', 'før', 'mang', 'også', 'slik', 'vært', 'vær', 'båe', 'begg', 'sid', 'dykk', 'dykk', 'dei', 'deir', 'deir', 'deim', 'di', 'då', 'eg', 'ein', 'eit', 'eitt', 'ell', 'honom', 'hjå', 'ho', 'hoe', 'henn', 'henn', 'henn', 'hoss', 'hoss', 'ikkj', 'ingi', 'inkj', 'korleis', 'korso', 'kva', 'kvar', 'kvarhelst', 'kven', 'kvi', 'kvifor', 'me', 'medan', 'mi', 'min', 'mykj', 'no', 'nokon', 'nok', 'nokor', 'noko', 'nokr', 'si', 'sia', 'sidan', 'so', 'somt', 'somm', 'um', 'upp', 'ver', 'vor', 'vert', 'vort', 'vart', 'vart']

# Replacing certain patterns with keywords (emails, urls, twitter, numbers)
patterns = []
patterns.append(('EMAILADR', [r'\S+@\S+[.]\w+']))
patterns.append(('TWITTERADR', [r'#\S+', r'@\S+']))
patterns.append(('URLADR', [r'(http(s)?://)\S+', r'(www)\S+']))
patterns.append(('NUMBER', [r'\d+.\d+\s?(kr)', r'\d+.?']))

# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame
def azureml_main(df_message = None, df_features = None):
    # Merging the header and the message body        
    heading = df_message.Heading.iloc[0]
    if not heading:
        heading = ''
    
    content = df_message.Content.iloc[0]
    org_message = heading.lower() + " " + content.lower()
    
    feature_vec = list(df_features.iloc[0,:])
    
    # PREPROCESSING
    #--------------------
    # Replace various patterns    
    message = org_message
    for key, pattern_list in patterns:
        for p in pattern_list:
            message = re.sub(p, key, message) 
    
    message.replace('kjempe', '')
    message.replace('mega', '')
    message.replace('super', '')
    
    message = re.split('\W+', message)
    message = [w for w in message if w not in words_to_ignore]

    message = [stem(w) for w in message]
    
    # FIND FEATURES IN MESSAGE
    #-----------------------------
    # For each message, count the features which occurs in that particular message
    message_features = [0]*len(feature_vec)
    for idx, feat in enumerate(feature_vec):
        message_features[idx] = message.count(feat)
    
    d = {'0': message_features}
    df_output = pd.DataFrame().from_dict(d, orient='index')
    df_output.columns = df_features.columns
    
    # Return value must be of a sequence of pandas.DataFrame
    return df_output,