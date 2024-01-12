
from spellchecker import SpellChecker
import language_tool_python
import re
import emoji

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
                                u"\U00000000-\U00000009"
                                u"\U0000000B-\U0000001F"
                                u"\U00000080-\U00000400"
                                u"\U00000402-\U0000040F"
                                u"\U00000450-\U00000450"
                                u"\U00000452-\U0010FFFF"
                                "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r' ээ ',text)

def check_errors(text1):
    text = deEmojify(text1)
    if re.fullmatch(r'(\w){0,1}(\W){0,}', text):
        return True



    ignored_words = set()
    for word in text.split():
        if any(c.isdigit() for c in word):
            ignored_words.add(word.lower())

    lowercased_text = ' '.join(word.lower() if not word[0].isupper() else word for word in text.split())

    words = [word for word in lowercased_text.split() if word.lower() not in ignored_words]


    text = re.sub(r'(?<=\w)([^\w\s]+)', ' ', text)

    words = [word for word in text.split() if word.lower() not in ignored_words]

    nonexistent_words = [word for word in words if not spell.correction(word)]

    text1 = text

    return nonexistent_words

def result(text, custom_dictionary):

    nonexistent_words= check_errors(text)

    if nonexistent_words:
        return True
    return False






import os.path
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DB:
    def __init__(self):
        self.conn = psycopg2.connect(host='ЗАМЕНИТЬ',
                                     port='ЗАМЕНИТЬ',
                                     user='ЗАМЕНИТЬ',
                                     password='ЗАМЕНИТЬ',
                                     dbname='ЗАМЕНИТЬ',
                                     sslmode='require')
        self.cur = self.conn.cursor()

    def execute(self, query):
        self.cur.execute(query)

    def fetch_all(self):
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()

conn = DB()
query = """select
guides.id, guides.question_answer
from guides
where question_name in (
    'answer_long_text_37961122'
    ) 
AND guides.question_answer notnull
;"""
conn.execute(query)
data = conn.fetch_all()

spell = SpellChecker(language='ru')

custom_dictionary_file = "vocab.txt"
with open(custom_dictionary_file, "r", encoding="utf-8") as file:
    custom_dictionary = set(
        word.strip() for word in file.readlines() if word.strip())
spell.word_frequency.load_words(custom_dictionary)



for row in data:
    id = row[0]
    text = row[1]
    if result(text, custom_dictionary):
        print(id, ' ', text)


conn.close()


