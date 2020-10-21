import requests
import sys
from bs4 import BeautifulSoup


class Translator:
    def __init__(self):
        self.LANGUAGES = {
            '0': 'all',
            '1': 'Arabic',
            '2': 'German',
            '3': 'English',
            '4': 'Spanish',
            '5': 'French',
            '6': 'Hebrew',
            '7': 'Japanese',
            '8': 'Dutch',
            '9': 'Polish',
            '10': 'Portuguese',
            '11': 'Romanian',
            '12': 'Russian',
            '13': 'Turkish'
        }
        self.base_url = 'https://context.reverso.net/translation'
        self.headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'}
        self.clean_translations = None
        self.clean_examples = None
        self.context = None

    def menu(self):
        # print("Hello, you're welcome to the translator. Translator supports:")
        # for k, v in self.LANGUAGES.items():
        #     print(k + '.', v)

        # Context include word to translate and language itself instead of language code
        # self.LANGUAGES[input('Type the number of your language:\n')
        # self.LANGUAGES[input("Type the number of language you want to translate to or '0' to "
        #                                                    "translate to all languages:\n")
        # input('Type the word you want to translate:\n')
        context = {'from_lang': sys.argv[1],
                   'to_lang': sys.argv[2],
                   'word': sys.argv[3]}

        self.context = context
        self.write_to_file()
        self.read_from_file()

        return None

    # make a request to server and get response with raw_data
    def context_translate(self, context):
        url = f"{self.base_url}/{context['from_lang'].lower()}-{context['to_lang'].lower()}/{context['word']}"
        response = requests.get(url, headers=self.headers)
        self.cleaning_data(response)
        return None

    # cleaning raw data
    def cleaning_data(self, content):
        raw_page = content.content
        soup = BeautifulSoup(raw_page, "html.parser")
        self.clean_translations = soup.find('div', {'id': 'translations-content'}).text.split()
        raw_translate_examples = soup.find('section', {'id': 'examples-content'}).text.split('\n')
        self.clean_examples = [i.strip() + '\n' for i in raw_translate_examples if i][:10]
        for i in range(len(self.clean_examples)):
            if i % 2 == 0:
                self.clean_examples[i] = self.clean_examples[i].replace('\n', ':\n')
            else:
                self.clean_examples[i] = self.clean_examples[i].replace('\n', '\n\n')
        return None

    # Create file and write to it all scrapped data
    def write_to_file(self):
        # Prepare target list languages, protect from translation - from_lang-from_lang (english-english) and delete
        # "all" from LANGUAGE
        lang_list = [self.context['to_lang']]
        if self.context['to_lang'] == 'all':
            lang_list = [lang for lang in self.LANGUAGES.values() if lang.lower() not in ['all', self.context['from_lang']]]
        with open(f"{self.context['word']}.txt", 'w') as f:
            for language in lang_list:
                self.context['to_lang'] = language
                self.context_translate(context=self.context)
                f.writelines(f"{language.title()} Translations:" + "\n" + "\n".join(self.clean_translations[:5]) + "\n\n" +
                             f"{language.capitalize()} examples:" + "\n" + "".join(self.clean_examples))
            f.close()

    # Print the result from file
    def read_from_file(self):
        with open(f"{self.context['word']}.txt", 'r') as f:
            print(f.read())


if __name__ == "__main__":
    tr = Translator()
    tr.menu()
