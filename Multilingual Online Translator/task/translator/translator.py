import requests
from bs4 import BeautifulSoup


class Translator:
    def __init__(self):
        self.LANGUAGES = {
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

    def menu(self):
        print("Hello, you're welcome to the translator. Translator supports:")
        for k, v in self.LANGUAGES.items():
            print(k + '.', v)

        # Context include word to translate and language itself instead of language code
        context = {'native_lang': self.LANGUAGES[input('Type the number of your language:\n')],
                   'lang': self.LANGUAGES[input('Type the number of language you want to translate to:\n')],
                   'word': input('Type the number of your language:\n')}

        response = self.context_translate(context)
        return self.print_result(response, context)

    def context_translate(self, context):
        url = f"{self.base_url}/{context['native_lang'].lower()}-{context['lang'].lower()}/{context['word']}"
        response = requests.get(url, headers=self.headers)
        return response

    def print_result(self, content, context):
        raw_page = content.content
        soup = BeautifulSoup(raw_page, "html.parser")

        translations_words = soup.find('div', {'id': 'translations-content'}).text.split()
        print(f"\n{context['lang']} Translations:")
        for i in translations_words[:5]:
            print(i)

        print(f"\n{context['lang']} Examples:")

        raw_translate_examples = soup.find('section', {'id': 'examples-content'}).text.split('\n')
        translate_examples = [i.strip() for i in raw_translate_examples if i][:10]

        for i in range(len(translate_examples)):
            if i % 2 == 0:
                print(translate_examples[i] + ':')
            else:
                print(translate_examples[i] + '\n')
        return None


if __name__ == "__main__":
    tr = Translator()
    tr.menu()
