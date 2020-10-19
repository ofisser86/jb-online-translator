invitation = """Type "en" if you want to translate from French into English, or "fr" if you want to translate from 
English into French: """
fr = input(invitation)
word = input('Type the word you want to translate:')
print(f'You chose "{fr}" as the language to translate "{word}" to.')
