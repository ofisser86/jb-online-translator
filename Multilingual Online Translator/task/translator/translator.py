from time import sleep

import requests
import sys
from bs4 import BeautifulSoup
from tqdm import tqdm


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
        self.total_size= None

    def menu(self):
        from_lang, to_lang, word = sys.argv[1], sys.argv[2], sys.argv[3]
        supported_lang = ['All', 'Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch',
                          'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']
        try:
            supported_lang.index(to_lang.title())
        except ValueError:
            print(f"Sorry, the program doesn't support {to_lang}")
            sys.exit()

        if from_lang != to_lang:
            context = {'from_lang': from_lang,
                       'to_lang': to_lang,
                       'word': word}
            self.context = context
        else:
            raise SystemExit("From and to languages are identical, no reason to translate")

        self.write_to_file()
        self.read_from_file()

        return None

    # make a request to server and get response with raw_data
    def context_translate(self, context):
        url = f"{self.base_url}/{context['from_lang'].lower()}-{context['to_lang'].lower()}/{context['word']}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise SystemExit("Error Connecting:", e)
        except requests.exceptions.HTTPError:
            print(f"Sorry, unable to find {self.context['word']}")
            sys.exit()
        except AttributeError:
            raise SystemExit("Wrong request")

        self.total_size = int(response.headers.get('content-length', 0))
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
            lang_list = [lang for lang in self.LANGUAGES.values() if
                         lang.lower() not in ['all', self.context['from_lang']]]

        if len(lang_list) > 1:
            pbar = tqdm(total=len(lang_list) - 2)
        else:
            pbar = tqdm(total=1)
        with open(f"{self.context['word']}.txt", 'w') as f:
            for i in range(10):
                # sleep(0.1)
                pbar.update(1)
                for language in lang_list:
                    self.context['to_lang'] = language
                    self.context_translate(context=self.context)
                    f.writelines(
                        f"{language.title()} Translations:" + "\n" + "\n".join(self.clean_translations[:5]) + "\n\n" +
                        f"{language.capitalize()} examples:" + "\n" + "".join(self.clean_examples))
            f.close()

    # Print the result from file
    def read_from_file(self):
        with open(f"{self.context['word']}.txt", 'r') as f:
            print(f.read())


if __name__ == "__main__":
    tr = Translator()
    tr.menu()
