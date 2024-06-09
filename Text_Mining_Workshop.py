import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# Download NLTK stopwords data
import nltk
nltk.download('stopwords')

# Load Excel file into Pandas DataFrame
xlsx_file_path = "Text_Mining_Workshop_Data.xlsx"  # Replace with your actual file path
df = pd.read_excel(xlsx_file_path)

# Tokenize, clean the text using NLTK, remove stopwords, and perform stemming
word_freq = {}

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    text = row['Text']
    language = row['Language']

    # Tokenize the text into words
    tokens = word_tokenize(text)
    # Remove non-alphabetic characters and convert to lowercase
    tokens = [word.lower() for word in tokens if word.isalpha()]
    
    # Remove stopwords based on language
    ##stop_words = set(stopwords.words(language.lower()))
    ##tokens = [word for word in tokens if word not in stop_words]

    # Perform stemming based on language
    ##stemmer = SnowballStemmer(language.lower())
    ##tokens = [stemmer.stem(word) for word in tokens]

    # Update the word frequency distribution for the language
    if language not in word_freq:
        word_freq[language] = FreqDist()

    word_freq[language].update(tokens)

# Create a new Pandas DataFrame for the word frequency results
word_freq_df = pd.DataFrame.from_dict(word_freq, orient='index')
word_freq_df = word_freq_df.transpose()

# Display top 15 word frequencies for each language with percentage
for language in word_freq_df.columns:
    print(f"\nTop 15 word frequencies after removing stopwords and stemming for {language}:\n")
    freq_dist = word_freq[language]
    
    # Sort the frequencies in descending order and get the top 15
    top_15_words = sorted(freq_dist.items(), key=lambda x: x[1], reverse=True)[:15]

    total_words = sum(freq_dist.values())

    # Print each word along with its count and percentage
    for word, count in top_15_words:
        percentage = (count / total_words) * 100
        print(f"{word}: {count} ({percentage:.2f}%)")
