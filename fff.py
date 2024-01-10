from spellchecker import SpellChecker
import language_tool_python
import re

def check_errors(text):

    tool = language_tool_python.LanguageTool('ru-RU')

    spell = SpellChecker(language='ru')


    custom_dictionary_file = "vocab.txt"
    with open(custom_dictionary_file, "r", encoding="utf-8") as file:
        custom_dictionary = set(
            word.strip() for word in file.readlines() if word.strip())

    spell.word_frequency.load_words(custom_dictionary)

    ignored_words = set()
    for word in text.split():
        if word.istitle() or any(c.isdigit() for c in word):
            ignored_words.add(word.lower())

    text = re.sub(r'(?<=\w)([^\w\s]+)', '', text)


    words = [word for word in text.split() if word.lower() not in ignored_words]
    nonexistent_words = spell.unknown(words)


    grammar_errors = tool.check(text)
    filtered_grammar_errors = [error for error in grammar_errors if error.offset not in [m.offset for w in nonexistent_words for m in tool.check(w)]]

    return nonexistent_words, filtered_grammar_errors

def main():
    text = input("Введите текст для проверки: ")

    nonexistent_words, grammar_errors = check_errors(text)

    print("Несуществующие слова:")
    for word in nonexistent_words:
        print(word)

    print("\nГрамматические ошибки:")
    for error in grammar_errors:
        print(error)


main()

