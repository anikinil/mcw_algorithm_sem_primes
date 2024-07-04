from wordfreq import top_n_list, zipf_frequency
from PyMultiDictionary import MultiDictionary, DICT_EDUCALINGO

# define dictionary
dict = MultiDictionary()

## util
def disp_progress(count, total): return str(count) + '/' + str(total) + ' --'

# save most common words for each from_lang
def save_mcws():
    
    # for each from_lang
    for from_lang in from_langs:

        print(from_lang, '--', 'saving', str(mcw_limit), 'mcws')

        # get top words
        from_list_top = top_n_list(from_lang, mcw_limit)

        # write to file (in lower case)
        f = open(mcws_path + from_lang + '.txt', 'w')
        f.write('\n'.join(from_list_top).lower())
        f.close()

# for each mcw in mcw files save its synonyms 
def save_synonyms():

    # for each from_lang
    for from_lang in from_langs:

        # read mcws from file
        f = open(mcws_path + from_lang + '.txt', 'r')
        mcws = f.read().split('\n')
        f.close()

        # clear syn file
        f = open(syn_path + from_lang + '.txt', 'w')
        f.write('')
        f.close()

        # open cleared syn file
        f = open(syn_path + from_lang + '.txt', 'a')

        # for each mcw append mcw + its synonyms to syn file (in lower case)
        count = 1
        total = len(mcws)
        for mcw in mcws:
            syns = dict.synonym(from_lang, mcw)[:syn_limit]
            print(from_lang, disp_progress(count, total), 'saving synonyms of', '\'' + mcw +'\':', ', '.join(syns))
            write_str = mcw
            # if no syns, only append '\n' to mcw, else append syns + '\n'
            write_str += ';' + ';'.join(syns).lower() + '\n' if syns != [] else '\n'
            f.write(write_str)
            count += 1
        f.close()

# save translations of all words in synonyms/ in translations/
def save_translations():
    
    # for each from_lang
    for from_lang in from_langs:

        # read all mcws and synonyms of from_lang (as single str)
        f = open(syn_path + from_lang + '.txt', 'r')
        source_file_as_str = f.read()

        # clear translation file
        f = open(transl_path + from_lang + '_' + to_lang + '.txt', 'w')
        f.write('')
        f.close()

        # open cleared translation file
        f = open(transl_path + from_lang + '_' + to_lang + '.txt', 'a')

        # if words are not already in desired language
        if from_lang != to_lang:
            # split words and syns into a 2D array
            word_groups = [g.split(';') for g in source_file_as_str.split('\n')]
            # translate each word in each group and save row wise in translation file (in lower case)
            for group in word_groups:
                group_translations = []
                for word in group:
                    translation = dict.translate(from_lang, word, to_lang)
                    translated_word = [w for (l, w) in translation if l == to_lang][0].lower()
                    group_translations.append(translated_word)
                f.write(';'.join(group_translations) + '\n')
        # if words are already in desired language, just write the whole source string into the trainslation file
        else:
            f.write(source_file_as_str)

        # close translation file
        f.close()

mcw_limit = 10
syn_limit = 3

from_langs = ['en', 'de', 'ru']
to_lang = 'en'

mcws_path = 'mcws/'
syn_path = 'synonyms/'
transl_path = 'translations/'

# save_mcws()
# save_synonyms()
save_translations()


# TODO think about using antonyms too