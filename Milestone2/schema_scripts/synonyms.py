from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

def save_synonyms(lines): 
    new_lines = []
    for line in lines:
        word = line.split(',')[-1].replace("\n", "")
        line = line.replace(f",{word}", "")
        new_line = f"{line} => {word}\n"
        new_lines.append(new_line)

    my_synonyms = "great,fantast,amaz,like,excel,superb,positi,good => good\nholidai,vacat,voyag,trip => vacation\ndull,lifeless,monoton,tediou,bore =>  boring\nheavi,hard,strenuou,tough,difficult => difficult\nlengthi,endless,long => long\n"

    new_lines.insert(0, my_synonyms)

    with open('./new_synonyms.txt', 'w') as f:
        for line in new_lines:
            f.write(line)


    



def main(): 
    with open('./online_synonyms.txt', 'r') as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        line = line.replace("\n", "")
        words = line.split(',')
        new_words = []
        # slice the last word
        for word in words[0:len(words)]: 
            # apply stemming
            ps = PorterStemmer()
            stemmed_word = ps.stem(word)
            new_words.append(stemmed_word)
        new_line = ",".join(new_words + [words[-1]])
        new_lines.append(new_line)


    save_synonyms(new_lines)


if __name__ == "__main__":
    main()