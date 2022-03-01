from re import search
import wikipedia

search_phrase = (wikipedia.search("SZA musician", results = 1))
search_phrase = search_phrase[0]
print(search_phrase)

summary = wikipedia.summary(search_phrase, sentences = 1, auto_suggest=False)
print(summary)

# print(wikipedia.page(search_phrase).content)