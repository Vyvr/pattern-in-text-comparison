import matplotlib.pyplot as plt
import string, random


random.seed(random.randint(1, 1000000000))

counter_sunday = 0
counter_naive = 0
counter_KMP = 0


#========================NAIVE===============================================

# ----Finds if pattern matches text, starting from index----#
def matchesAtNaive(text, index, pattern):
    global counter_naive
    if len(text) < len(pattern):
        return False
    for i in range(0, len(pattern)):
        counter_naive += 1
        if text[index + i] != pattern[i]:
            return False
    return True

# ----Adds to array indexes where pattern matches text----#
def report(index, matchedIndexes):
    matchedIndexes.append(index)


#----Naive algorithm----#
def naiveAlgorithm(text, pattern):
    matchedIndexes = []
    global counter_naive
    for i in range(0, (len(text) - len(pattern)) + 1):
        counter_naive += 1
        if matchesAtNaive(text, i, pattern):
            report(i, matchedIndexes) 

    return matchedIndexes

#==============================Sunday=========================================

# ----Finds if pattern matches text, starting from index----#
def matchesAtSunday(text, index, pattern):
    global counter_sunday
    if len(text) < len(pattern):
        return False
    for i in range(0, len(pattern)):
        counter_sunday += 1
        if text[index + i] != pattern[i]:
            return False
    return True

# ----Adds to array indexes where pattern matches text----#
def reportSuccess(index, matchedIndexes):
    matchedIndexes.append(index)

#----Creates dictionary of last indexes of letters----#
def createPatternLettersDictionary(pattern, patternChars):
    for index, letter in enumerate(reversed(pattern)):
        if letter not in patternChars:
            patternChars[letter] = str(index + 1)
    return patternChars

#----Preprocesses text and patern, returns shift number, if letter not in dictionary return number longer than pattern----#
def preprocess(patternChars, letter, pattern):
    if letter not in patternChars:
        return len(pattern) + 1
    return int(patternChars[letter])

#----Sunday algorithm----#
def sundayAlgorithm(text, pattern):
    patternChars = {}
    startingPos = 0
    matchedIndexes = []
    global counter_sunday

    createPatternLettersDictionary(pattern, patternChars)

    while startingPos < len(text) - len(pattern) + 1:
        counter_sunday += 1
        if matchesAtSunday(text, startingPos, pattern):
            reportSuccess(startingPos, matchedIndexes)

        if (len(pattern) + startingPos) >= len(text):
            break
        startingPos += preprocess(patternChars,
                                  text[len(pattern) + startingPos], pattern)
    return matchedIndexes

#==============================KMP=========================================

#----Creates KMPnext array----#
def KMPArray(pattern):  # returns KMP list of indexes
    indexing = [-1] * (len(pattern) + 1)
    pred = -1

    for i in range(1, len(pattern) + 1):
        while pred > -1 and pattern[pred] != pattern[i - 1]:
            pred = indexing[pred]

        pred += 1

        if i != len(pattern) and pattern[i] == pattern[pred]:
            indexing[i] = indexing[pred]
        else:
            indexing[i] = pred

    return indexing

#----KMP algorithm----#
def KMPAlgorithm(text, pattern):
    patIndex = 0
    indexing = KMPArray(pattern)
    matchedIndexes = []
    global counter_KMP

    for textIndex, char in enumerate(text):
        counter_KMP += 1
        while patIndex > -1 and pattern[patIndex] != char:
            counter_KMP += 1
            patIndex = indexing[patIndex]
        
        patIndex += 1

        if patIndex == len(pattern):
            matchedIndexes.append(textIndex - len(pattern) + 1)
            patIndex = 0

    return matchedIndexes

#=================word and pattern creation==============================

def createText(text, alphabet, size, mode):
    if mode == 'append':
        for _ in range(size):
            text += alphabet[random.randint(0, 1000000) % len(alphabet)]
    elif mode == 'new':
        text = ''
        for _ in range(size):
            text += alphabet[random.randint(0, 1000000) % len(alphabet)]
    else:
        print('fun createText: wrong mode\nAvailable modes:\n-new --> new text\n-append --> appends new letter to exsisting text\n')
    return text


def createSearchedWord(text, size):
    if size >= len(text):
        modulo = len(text)
    else:
        modulo = len(text) - size
    random_starting_point = random.randint(0, 1000000) % (modulo)
    return text[random_starting_point : random_starting_point + size]

#==============================Program=========================================
print("Choose chart type: ")
print("[stts] Speed to text size")
print("[stsw] Speed to searched word size")
print("[stas] Speed to alphabet size")
chartType = input("Chart type: ")

alphabet = string.ascii_letters + string.digits
T = ''
W = ''

speed_to_text_size_chart = True
speed_to_searched_word_size_chart = False
speed_to_alphabet_size_chart = False

match chartType:
    case "stts":
        naive_counter_list = []
        sunday_counter_list = []
        kmp_counter_list = []
        text_length_list = []
        current_text_size = 0
        while current_text_size <= 1000:
            current_text_size += 1
            T = createText(T, alphabet, 1, 'append')
            W = createSearchedWord(T, 3)

            counter_naive, counter_sunday, counter_KMP = 0, 0, 0
            naiveAlgorithm(T, W)
            sundayAlgorithm(T, W)
            KMPAlgorithm(T, W)

            naive_counter_list.append(counter_naive)
            sunday_counter_list.append(counter_sunday)
            kmp_counter_list.append(counter_KMP)

            text_length_list.append(len(T))

        plt.title("Speed to text size")
        plt.plot(text_length_list, naive_counter_list, 'green', label='Naive algorithm')
        plt.plot(text_length_list, sunday_counter_list, 'red', label='Sunday algorithm')
        plt.plot(text_length_list, kmp_counter_list, 'blue', label='KMP algorithm')
        plt.legend(loc='upper left')
        fig = plt.gcf()
        fig.set_size_inches(16, 9)
        fig.savefig('speed_to_text_size_chart.png', dpi=300)

    case "stsw":
        naive_counter_list = []
        sunday_counter_list = []
        kmp_counter_list = []
        searched_word_length_list = []
        current_searched_size = 0
        T = createText(T, alphabet, 10_000, 'new')
        while current_searched_size <= 1_000:
            current_searched_size += 1
            W = createSearchedWord(T, current_searched_size)

            counter_naive, counter_sunday, counter_KMP = 0, 0, 0
            naiveAlgorithm(T, W)
            sundayAlgorithm(T, W)
            KMPAlgorithm(T, W)

            naive_counter_list.append(counter_naive)
            sunday_counter_list.append(counter_sunday)
            kmp_counter_list.append(counter_KMP)
            searched_word_length_list.append(len(W))

        plt.title("Speed to searched word size")
        plt.plot(searched_word_length_list, naive_counter_list, 'green', label='Naive algorithm')
        plt.plot(searched_word_length_list, sunday_counter_list, 'red', label='Sunday algorithm')
        plt.plot(searched_word_length_list, kmp_counter_list, 'blue', label='KMP algorithm')
        plt.legend(loc='upper left')
        fig = plt.gcf()
        fig.set_size_inches(16, 9)
        fig.savefig('speed_to_searched_word_size_chart.png', dpi=300)
    
    case "stas":
        naive_counter_list = []
        sunday_counter_list = []
        kmp_counter_list = []
        alphabet_length_list = []
        current_alphabet_size = 20

        while current_alphabet_size <= len(alphabet):
            current_alphabet_size += 1
            current_alphabet = alphabet[0 : current_alphabet_size]

            T = createText(T, alphabet, 500, 'new')
            W = createSearchedWord(T, 5)

            counter_naive, counter_sunday, counter_KMP = 0, 0, 0
            naiveAlgorithm(T, W)
            sundayAlgorithm(T, W)
            KMPAlgorithm(T, W)

            naive_counter_list.append(counter_naive)
            sunday_counter_list.append(counter_sunday)
            kmp_counter_list.append(counter_KMP)
            alphabet_length_list.append(len(current_alphabet))

        plt.title("Speed to alphabet size")
        plt.plot(alphabet_length_list, naive_counter_list, 'green', label='Naive algorithm')
        plt.plot(alphabet_length_list, sunday_counter_list, 'red', label='Sunday algorithm')
        plt.plot(alphabet_length_list, kmp_counter_list, 'blue', label='KMP algorithm')
        plt.legend(loc='upper left')
        fig = plt.gcf()
        fig.set_size_inches(16, 9)
        fig.savefig('speed_to_alphabet_size_chart.png', dpi=300)