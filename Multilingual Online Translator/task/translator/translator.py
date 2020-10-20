import requests
from bs4 import BeautifulSoup

invitation = """Type "en" if you want to translate from French into English, or "fr" if you want to translate from 
English into French:\n"""

into_lang = input(invitation)
word = input('Type the word you want to translate:\n')
lang = {'fr': 'French', 'en': 'English'}
print(f'You chose "{into_lang}" as the language to translate "{word}" to.')


def context_translate(to_lang, w):
    lang_pairs = {'en': 'french-english', 'fr': 'english-french'}
    headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'}
    url = f'https://context.reverso.net/translation/{lang_pairs[to_lang]}/{w}'
    response = requests.get(url, headers=headers)
    return response


res = context_translate(into_lang, word)
raw_page = res.content
soup = BeautifulSoup(raw_page, "html.parser")

print(res.status_code, 'OK')
print('\nContext examples:\n')

translations_words = soup.find('div', {'id': 'translations-content'}).text.split()
print(f"{lang[into_lang]} Translations:")
for i in translations_words[:5]:
    print(i)

print()

print(f"{lang[into_lang]} Examples:")

raw_translate_examples = soup.find('section', {'id': 'examples-content'}).text.split('\n')
translate_examples = [i.strip() for i in raw_translate_examples if i][:10]

for i in range(len(translate_examples)):
    if i % 2 == 0:
        print(translate_examples[i] + ':')
    else:
        print(translate_examples[i] + '\n')
