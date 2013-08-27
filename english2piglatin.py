#!/usr/bin/python

"""
English to Piglatin translator

It takes a word or a whole sentence from stdin, 
lower cases it and transforms it then 
based upon the first character of 
the given string.
"""

"""
detectWords()

Takes a sentence and splits it by searching
for whitespaces.

input arguments:

string - Sentence or word to examine


return values:

words - array of single word strings
"""
def detectWords(string):

	offset 	= 0
	words 	= []

	for idx in range (0, len(string)):

		if string[idx] == " ":

			words.append(string[offset:idx])
			offset = idx + 1

		if idx == len(string) - 1:
			words.append(string[offset:idx + 1])

	#print "Found %d word(s)!" % len(words)
	#print words
	return words			

"""
stripSpecialChars()

Examines a given string for 
special characters, extracts them
and stores them into an extra array.

input arguments:

string - array of word strings


return values:

specialChars - Tuple of essential values [word index, 
	       character index, word length, special character]

strippedWords - Array of words which are stripped from
		special characters
"""
def stripSpecialChars(words):

	specialChars = []
	strippedWords = []
	
	for idx in range (0, len(words)):

		word = words[idx]
		appendAsIs = True
		
		for idx2 in range (0, len(word)):

			if word[idx2] == "!" or word[idx2] == "?" or word[idx2] == "." or word[idx2] == ",":
				
				t = idx, idx2, len(word), word[idx2]	# [pos in sentence, pos in word, len of word, special char]
				specialChars.append(t)
				temp = word[ 0 : idx2 ] + word[ idx2 + 1 : len(word) ]
				strippedWords.append(temp)
				appendAsIs = False
		
		if appendAsIs:
			strippedWords.append(word)
				
	return specialChars, strippedWords

"""
en2pl()

This function takes a word string
and tranforms it into it's piglatin
version. First the word is checked
for correctness, means that it must not
be empty or contain any special characters.
Then, depending on the starting character,
the word gets transformed.

a) If the first char is a vowel, then only
   the pyg extension is appended to the word
   example: "ape" --> "ape-ay"

b) If the first char is a consonant, the first
   char is extracted from the string, reappended
   at the end in addition to the pyg extension
   example: "tiger" --> "iger-t-ay"

input arguments:
string - Word to examine

return values:
new_word - tranformed piglatin word
"""
def en2pl(string):
	#pig extension
	pyg = 'ay'

	#print "Current string is: '" + string + "'"

	#check if it's a valid string. Means not empty and only ASCII chars
	if len(string) > 0 and string.isalpha():
	    
	    #lower case the inout
	    word = string.lower()
	    
	    #print "lower: " + word

	    #get first char
	    first = word[0]
	    
	    #print "First: " + first

	    #check for vowels
	    if first == 'a' or first == 'o' or first == 'e' or first == 'i' or first == 'u':
		
		#just append pig extension in this case
		new_word = string + pyg
		
		#return new word
		return new_word
	    else:
		
		#Take the rest of the word append first char and the
		#the pig extension
		new_word = string[1:len(string)] + first + pyg
		
		#print ne word
		return new_word
	    
	else:
	    #Give warning in this case
	    return '>>Empty or invalid string<<'
 
"""
doConversion()

This function takes all cleaned words and all
extracted special chars and applies the piglatin
conversion, rematches the special chars to the 
converted words, and puts the whole sentence
back together.

input arguments:
specialChars - List of tuple which contains essential information
	       about each special char extracted

strippedWords - List of all bare stripped strings which resemble
		to the sentence in the end
"""
def doConversion(specialChars, strippedWords):
	pl_string 	= ""

	#loop through all words
	for idx in range (0, len(strippedWords)):
		next 	= en2pl(strippedWords[idx])
		next_sp = ""

		#loop through all special chars
		for idx2 in range (0, len(specialChars)):
			#if current word has a special char
			if idx == specialChars[idx2][0]:
				
				#print specialChars[idx2]

				#if special char is at end of word
				if specialChars[idx2][1] == specialChars[idx2][2] - 1:
					next_sp = next + specialChars[idx2][3]

				#if special char is in the middle of the word
				else:
					next_sp = next[0:specialChars[idx2][1]] + specialChars[idx2][3] + next[specialChars[idx2][1]:specialChars[idx2][2] + 1]

		if next_sp == "":
			next_sp = next

		pl_string += next_sp + " "

	return pl_string	


"""
translate()

Wrapper function for easy usage
of the translator.

input arguments:
org_string - Word/sentence to examine

return values:
translated piglatin sentence or word
"""
def translate(org_string):
	words 	= detectWords(org_string)
	raw   	= stripSpecialChars(words)
	return doConversion(raw[0], raw[1])	

"""
main block
"""
original = raw_input('Enter a word or sentence: ')
print "In pig latin this would be: " + translate(original)



