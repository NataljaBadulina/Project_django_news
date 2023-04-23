from django import template
import string

register = template.Library()
bad_words = ["редиска", "пипец"]


@register.filter()
def censor(value):
    text_list = value.split()
    censored_text_list = []

    for word in text_list:
        clean_word = ''.join(c for c in word if c not in string.punctuation)
        if clean_word.lower() in bad_words:
            censored_word = clean_word[0] + (len(clean_word) - 1) * '*'
            censored_text_list.append(word.replace(clean_word, censored_word))
        else:
            censored_text_list.append(word)

    return ' '.join(censored_text_list)


#text = "Слово прекрасное, но вот слово, со знаком препинания, не такое прекрасное!"


#censored_text = censor(text, bad_words)
# С**** п*********, но вот с****, со знаком препинания, не такое п*********!