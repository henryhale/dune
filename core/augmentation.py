import random
import pandas
from nltk.corpus import wordnet

# download wordnet
# >> import nltk
# >> nltk.download('wordnet')



def synonym_augment(text_str, num_replacements=2):
    words = text_str.split()
    for _ in range(num_replacements):
        idx = random.randint(0, len(words) - 1)
        word = words[idx]
        synsets = wordnet.synsets(word)
        if synsets:
            synonym = random.choice(synsets).lemmas()[0].name()
            words[idx] = synonym
    return " ".join(words)


def augment_data(df:pandas.DataFrame):
    augmented = []
    for i in range(len(df['input_variation'])):
        text = df["input_variation"][i]
        label = df["output_class"][i]
        augmented.append({text, label})
        for _ in range(4):  # generate 4 variations per sample
            augmented.append((synonym_augment(text), label))
    return pandas.DataFrame(augmented)