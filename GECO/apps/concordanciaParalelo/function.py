import re

from django.utils.safestring import mark_safe

#Read a text
def read_text_txt(path):
    input_file = open(path, 'r', encoding='utf8')
    input_file.seek(0)
    input_text = input_file.read().splitlines()
    input_file.close()
    return input_text

#Read n-texts
def read_txt_files(files):
    files_list=[]
    for f in files:
        files_list.append(read_text_txt(f[0]))
    return files_list

'''
 Modificador 	Descripción 	Ejemplo petición
    1. Sin modificador  	Forma concreta 	Avión
    2. Corchetes 	Buscar lema 	[vivir]
    3. Signos menor y mayor qué 	Buscar etiqueta POS 	<VMIS3S0>
    4. Asterisco 	Comodín, varias letras 	*ito
    5. Asterisco 	Comodín, varias letras 	clean*
    6. Asterisco 	Comodín, una palabra 	de * y *
    7. Signo de interrogación 	Comodín, una letra 	p?lo
    8. Llaves     Buscar en una distancia de X palabras     se {2} como
    9. Llaves     Buscar en una distancia de X a Y palabras     se {1-5} como
    10. Comillas  Busca las diferentes variantes de escribir la palabra en ciertas lenguas   avion   ávíón, avïón, ävíòn
'''

#Identify type of search 
def type_search(search_p):
    pattern_i = r'^'
    pattern_f = r'$'
    #pattern0 = r'\b'
    #pattern_w = r'[A-Za-záéíóúÁÉÍÓÚñÑäëïöüÄËÏÖÜàèìòùÀÈÌÒÙÂÊÎÔÛâêîôÃÕãõÅåæÆØøÇçĀĒĪŪƗāēīūɨ]*'
    #pattern_w1 = r'\w+'
    pattern_w1 = r'[^\d\W]+'
    # /\b[^\d\W]+\b/g
    pattern_c1 = r'\['
    pattern_c2 = r'\]'
    pattern_a = r'\*'
    pattern_e = r'\s'
    pattern_s = r'\?'
    pattern_d = r'{\d*}'
    pattern_ds = r'{\d*-\d*}'
    pattern_c = r'"'
    
    pattern1 = pattern_i+pattern_w1+pattern_f
    pattern2 = pattern_i+pattern_c1+pattern_w1+pattern_c2+pattern_f
    pattern3 = r'(?:<\w*>)'
    pattern4 = pattern_i+pattern_a+pattern_w1+pattern_f
    pattern5 = pattern_i+pattern_w1+pattern_a+pattern_f
    pattern6 = pattern_i+pattern_w1+pattern_e+pattern_a+pattern_e+pattern_w1+pattern_e+pattern_a+pattern_f
    pattern7 = pattern_i+pattern_w1+pattern_s+pattern_w1+pattern_f
    pattern8 = pattern_i+pattern_w1+pattern_e+pattern_d+pattern_e+pattern_w1+pattern_f
    pattern9 = pattern_i+pattern_w1+pattern_e+pattern_ds+pattern_e+pattern_w1+pattern_f
    pattern10 = pattern_c+pattern_w1+pattern_c+pattern_f
    
    dicc_search = dict()
    
    if re.search(pattern10, search_p):
        r = re.split(pattern_c, search_p, 2)
        word1 = r[1]
        dicc_search.update({'condiction':'condiction10'})
        dicc_search.update({'word1':word1})
        print(dicc_search)
    
    elif re.search(pattern9, search_p):
        r = re.split(pattern_e+pattern_ds+pattern_e, search_p, 1)
        word1 = r[0]
        word2 = r[1]
        intervalo = (re.findall(r'\d*-\d*', search_p)[0]).split('-')
        if int(intervalo[0]) <= int(intervalo[1]):
            dicc_search.update({'condiction':'condiction9'})
            dicc_search.update({'word1':word1})
            dicc_search.update({'word2':word2})
            dicc_search.update({'X':int(intervalo[0])})
            dicc_search.update({'Y':int(intervalo[1])})
            print(dicc_search)
        else:
            print('No cumple X < Y')
    
    elif re.search(pattern8, search_p):
        r = re.split(pattern_e+pattern_d+pattern_e, search_p, 1)
        word1 = r[0]
        word2 = r[1]
        n = int(re.findall(r'\d+', search_p)[0])
        dicc_search.update({'condiction':'condiction8'})
        dicc_search.update({'word1':word1})
        dicc_search.update({'word2':word2})
        dicc_search.update({'distance':n})
        print(dicc_search)

    elif re.search(pattern7, search_p):
        r = re.split(pattern_s, search_p, 1)
        word1 = r[0]
        word2 = r[1]
        dicc_search.update({'condiction':'condiction7'})
        dicc_search.update({'word1':word1})
        dicc_search.update({'word2':word2})
        print(dicc_search)

    elif re.search(pattern6, search_p):
        r = re.split(pattern_a, search_p, 2)
        word1 = r[0].strip()
        word2 = r[1].strip()
        dicc_search.update({'condiction':'condiction6'})
        dicc_search.update({'word1':word1})
        dicc_search.update({'word2':word2})
        print(dicc_search)
        
    elif re.search(pattern5, search_p):
        r = re.split(pattern_a, search_p, 1)
        word1 = r[0]
        dicc_search.update({'condiction':'condiction5'})
        dicc_search.update({'word1':word1})
        print(dicc_search)
    
    elif re.search(pattern4, search_p):
        r = re.split(pattern_a, search_p, 1)
        word1 = r[1]
        dicc_search.update({'condiction':'condiction4'})
        dicc_search.update({'word1':word1})
        print(dicc_search)
    
    elif re.search(pattern3, search_p):
        pos = re.findall(r'\w+', search_p)[0]
        dicc_search.update({'condiction':'condiction3'})
        dicc_search.update({'word1':pos})
        print(dicc_search)

    elif re.search(pattern2, search_p):
        lemma = re.findall(r'\w+', search_p)[0]
        dicc_search.update({'condiction':'condiction2'})
        dicc_search.update({'word1':lemma})
        print(dicc_search)

    elif re.search(pattern1, search_p):
        dicc_search.update({'condiction':'condiction1'})
        dicc_search.update({'word1':search_p})
        print(dicc_search)
    
    return dicc_search

#Find type of search in text
def search_pattern(dic):
    pattern1 = r'\b'
    pattern2 = r'\w*'
    pattern3 = r'\s\w*\s'
    pattern4 = r'\w*\s'
    
    word1 = dic['word1'].lower()
    list_pattern = []
    search = False
    
    #búsqueda sin modificador - forma concreta
    if dic['condiction']=='condiction1':        
        pattern = pattern1+word1+pattern1
        if re.search(pattern, dic['line']):
            list_pattern.append(pattern)
            dic.update( {'pattern' : list_pattern} )
            search = True
        word1 = word1.capitalize()
        pattern_other = pattern1+word1+pattern1
        if re.search(pattern_other, dic['line']):
            list_pattern.append(pattern_other)
            dic.update( {'pattern' : list_pattern} )
            search = True
    
    #búsqueda aterisco - comodín varias letras
    elif dic['condiction']=='condiction4':        
        pattern = pattern1+pattern2+word1+pattern1
        if re.search(pattern, dic['line']):
            list_pattern.append(pattern)
            dic.update( {'pattern' : list_pattern} )
            search = True

    #búsqueda aterisco - comodín varias letras
    elif dic['condiction']=='condiction5':
        pattern = pattern1+word1+pattern2+pattern1
        if re.search(pattern, dic['line']):
            list_pattern.append(pattern)
            dic.update( {'pattern' : list_pattern} )
            search = True
        word1 = word1.capitalize()
        pattern_other = pattern1+word1+pattern2+pattern1
        if re.search(pattern_other, dic['line']):
            list_pattern.append(pattern_other)
            dic.update( {'pattern' : list_pattern} )
            search = True
    
    #búsqueda aterisco - comodín una palabra
    elif dic['condiction']=='condiction6':
        word2 = dic['word2'].lower()
        pattern = pattern1+word1+pattern1+pattern3+pattern1+word2+pattern1+pattern3
        if re.search(pattern, dic['line']):
            list_pattern.append(pattern)
            dic.update( {'pattern' : list_pattern} )
            search = True
        word1 = word1.capitalize()
        pattern_other = pattern1+word1+pattern1+pattern3+pattern1+word2+pattern1+pattern3
        if re.search(pattern_other, dic['line']):
            list_pattern.append(pattern_other)
            dic.update( {'pattern' : list_pattern} )
            search = True
    
    #búsqueda Signo de interrogación - comodín, una letra
    elif dic['condiction']=='condiction7':
        word2 = dic['word2'].lower()
        pattern = pattern1+word1+pattern2+word2+pattern1
        if re.search(pattern, dic['line']):
            list_pattern.append(pattern)
            dic.update( {'pattern' : list_pattern} )
            search = True
        word1 = word1.capitalize()
        pattern_other = pattern1+word1+pattern2+word2+pattern1
        if re.search(pattern_other, dic['line']):
            list_pattern.append(pattern_other)
            dic.update( {'pattern' : list_pattern} )
            search = True
    
    #búsqueda Llaves - Buscar en una distancia de hasta X palabras
    elif dic['condiction']=='condiction8':
        pattern0 = ''
        for i in range(dic['distance']):
            if i==0:
                pattern0 += pattern3
            else:
                pattern0 += pattern4
        word2 = dic['word2'].lower()
        pattern = pattern1+word1+pattern0+word2+pattern1        
        if re.search(pattern, dic['line']):
            list_pattern.append(pattern)
            dic.update( {'pattern' : list_pattern} )
            search = True
        word1 = word1.capitalize()
        pattern_other = pattern1+word1+pattern0+word2+pattern1
        if re.search(pattern_other, dic['line']):
            list_pattern.append(pattern_other)
            dic.update( {'pattern' : list_pattern} )
            search = True
    
    #búsqueda Llaves - Buscar en una distancia de X-Y palabras
    elif dic['condiction']=='condiction9':
        pattern0 = ''
        x = dic['X']
        y = dic['Y']
        for i in range(x):
            if i==0:
                pattern0 += pattern3
            else:
                pattern0 += pattern4
        word2 = dic['word2'].lower()
        while x<=y:
            pattern = pattern1+word1+pattern0+word2+pattern1        
            if re.search(pattern, dic['line']):
                list_pattern.append(pattern)
                dic.update( {'pattern' : list_pattern} )
                search = True
            word1 = word1.capitalize()
            pattern_other = pattern1+word1+pattern0+word2+pattern1
            if re.search(pattern_other, dic['line']):
                list_pattern.append(pattern_other)
                dic.update( {'pattern' : list_pattern} )
                search = True
            pattern0 += pattern4
            word1 = word1.lower()
            x+=1    
            
    elif dic['condiction']=='condiction10':
        word = letter_change(dic['language'], word1)
        pattern = pattern1+word+pattern1
        if re.search(pattern, dic['line']):
            list_pattern.append(pattern)
            dic.update( {'pattern' : list_pattern} )
            search = True
        
        word1 = word1.capitalize()
        word = letter_change(dic['language'], word1)
        pattern_other = pattern1+word+pattern1
        if re.search(pattern_other, dic['line']):
            list_pattern.append(pattern_other)
            dic.update( {'pattern' : list_pattern} )
            search = True
    
    return search

def letter_change(language, busq):
    
    dicc = {'CHL': [('ty', "[ty|Ty|T'|t']"), ('Ty', "[ty|Ty|T'|t']"),('c', "[C|c|K|k|Q|q]"), ('C', "[C|c|K|k|Q|q]"), ('k', "[C|c|K|k|Q|q]"), 
                    ('K', "[C|c|K|k|Q|q]"), ('j', "[J|j|H|h|y|Y]"), ('J', "[J|j|H|h|y|Y]"), ('y', "[J|j|y|Y]"), ('Y', "[J|j|y|Y]"), 
                    ('a', "[A|a|Ʌ|ʌ]"), ('A', "[A|a|Ʌ|ʌ]"), ('ä', "[Ʌ|ʌ|ä|Ä]"), ('Ä', "[Ʌ|ʌ|ä|Ä]"), ('ö', "[Ʌ|ʌ|ö|Ö]"), ('Ö', "[Ʌ|ʌ|ö|Ö]"),
                    ('u', "[u|U|Ʌ|ʌ]"), ('U', "[u|U|Ʌ|ʌ]")],
               
            'MY': [],
            
            'MAZ': [('i', "[i|I|í|ì|ǐ|î|ī|i̠|į|i̜|i̹|í̠|į́|į̀|į̌|į̂|į̄|ï|ḯ|ï̀|ï̠|ɨ|ɨ́|ɨ̀|ɨ̌|ɨ̂|ɨ̄|ɨ̠|ɨ̜|ɨ̹|ɨ̠́]"),
                    ('I', "[i|I|í|ì|ǐ|î|ī|i̠|į|i̜|i̹|í̠|į́|į̀|į̌|į̂|į̄|ï|ḯ|ï̀|ï̠|ɨ|ɨ́|ɨ̀|ɨ̌|ɨ̂|ɨ̄|ɨ̠|ɨ̜|ɨ̹|ɨ̠́]"),
                    ('e', "[e|E|é|è|ě|ê|ē|e̠|ę|e̜|e̹|é̠|ę́|ę̀|ę̌|ę̂|ę̄|ë|ë́|ë̀|ë̌|ë̂|ë̠|ɛ|ɛ́|ɛ̀|ɛ̌|ɛ̂|ɛ̄|ɛ̠|ɛ̨|ξ|ɛ̠́|ɛ̨́|ɛ̜̌|ɛ̨̂|æ|ǽ|æ̀|æ̌|æ̂|ǣ|æ̠|æ̜|æ̹|ǽ̠|ǽ̜|æ̜̌|æ̜̂|ǣ̜]"),
                    ('E', "[e|E|é|è|ě|ê|ē|e̠|ę|e̜|e̹|é̠|ę́|ę̀|ę̌|ę̂|ę̄|ë|ë́|ë̀|ë̌|ë̂|ë̠|ɛ|ɛ́|ɛ̀|ɛ̌|ɛ̂|ɛ̄|ɛ̠|ɛ̨|ξ|ɛ̠́|ɛ̨́|ɛ̜̌|ɛ̨̂|æ|ǽ|æ̀|æ̌|æ̂|ǣ|æ̠|æ̜|æ̹|ǽ̠|ǽ̜|æ̜̌|æ̜̂|ǣ̜]"),
                    ('a', "[a|A|á|à|ǎ|â|ā|a̠|ą|a̜|a̹|á̠|ą́|ą̀|ą̌|ą̂|ą̄|ä|ä́|æ|ǽ|æ̀|æ̌|æ̂|ǣ|æ̠|æ̜|æ̹|ǽ̠|ǽ̜|æ̜̌|æ̜̂|ǣ̜]"),
                    ('A', "[a|A|á|à|ǎ|â|ā|a̠|ą|a̜|a̹|á̠|ą́|ą̀|ą̌|ą̂|ą̄|ä|ä́|æ|ǽ|æ̀|æ̌|æ̂|ǣ|æ̠|æ̜|æ̹|ǽ̠|ǽ̜|æ̜̌|æ̜̂|ǣ̜]"),
                    ('o', "[o|O|ó|ò|ǒ|ô|ō|o̠|ǫ|o̜|o̹|ó̠|ǫ́|ǫ̀|ǫ̌|ǫ̂|ǭ|ö|ö́|ö̀|ö̠]"), ('O', "[o|O|ó|ò|ǒ|ô|ō|o̠|ǫ|o̜|o̹|ó̠|ǫ́|ǫ̀|ǫ̌|ǫ̂|ǭ|ö|ö́|ö̀|ö̠]"),
                    ('u', "[u|U|ú|ù|ǔ|û|ū|u̠|ų|u̜|u̹|ú̠|ų́|ų̀|ų̌|ų̂|ų̄|ü|ǘ|ǜ|ü̠|ʉ|ʉ́|ʉ̀|ʉ̌|ʉ̂|ʉ̄|ʉ̠|ʉ̜|ʉ̹|ʉ̠́]"),
                    ('U', "[u|U|ú|ù|ǔ|û|ū|u̠|ų|u̜|u̹|ú̠|ų́|ų̀|ų̌|ų̂|ų̄|ü|ǘ|ǜ|ü̠|ʉ|ʉ́|ʉ̀|ʉ̌|ʉ̂|ʉ̄|ʉ̠|ʉ̜|ʉ̹|ʉ̠́]"),
                    ('ch', "[ch|Ch|č|Č]"), ('Ch', "[ch|Ch|č|Č]"), ('ts', "[ts|Ts|¢]"), ('Ts', "[ts|Ts|¢]"), ('sh', "[sh|Sh|x|X]"), ('Sh', "[sh|Sh|x|X]"),
                    ('b', "[b|B|b̜|b̠]"), ('B', "[b|B|b̜|b̠]"), ('ku', "[ku|Ku|kw|Kw]"), ('Ku', "[ku|Ku|kw|Kw]"), ('c', "[c|C|k|K]"), ('C', "[c|C|k|K]"),
                    ('k', "[k|K|c|C]"), ('K', "[k|K|c|C]"), ('n', "[n|N|ⁿ]"), ('N', "[n|N|ⁿ]"), ("'", "['|ʔ|ˀ]"), ('h', "[j|J|h|H]"), 
                    ('H', "[j|J|h|H]"), ('j', "[j|J|x|X|h|H]"), ('J', "[j|J|x|X|h|H]")],
            
            'MX': [('a', "[a|A|á|ā|a̠|à]"), ('A', "[a|A|á|ā|a̠|à]"), ('e', "[e|E|é|ē|e̠|è]"), ('E', "[e|E|é|ē|e̠|è]"), ('i', "[i|I|í|ī|i̠|ì|i|ɨ|ɨ̄|ɨ̠]"), 
                   ('I', "[i|I|í|ī|i̠|ì|i|ɨ|ɨ̄|ɨ̠]"), ('o', "[o|O|ó|ō|o̠|ò]"), ('O', "[o|O|ó|ō|o̠|ò]"), ('u', "[u|U|ú|ū|u̠|ù]"), ('U', "[u|U|ú|ū|u̠|ù]"),
                   ('ch', "[ch|Ch|ty]"), ('ty', "[ty|Ty|ch]"), ('k', "[k|K|c|C|q|Q]"), ('c', "[k|K|c|C|q|Q]"), ('q', "[q|c|k]"), ('h', "[h|H|']"), ("'", "[h|H|']"),
                   ('Ch', "[ch|Ch|ty]"), ('Ty', "[ty|Ty|ch]"), ('K', "[k|K|c|C|q|Q]"), ('C', "[k|K|c|C|q|Q]"), ('Q', "[k|K|c|C|q|Q]"), ('H', "[h|H|']"), ("'", "[h|H|']")],
            
            'NAH': [('a', "[a|A|Ā|ā|A̱|a̱]"), ('A', "[a|A|Ā|ā|A̱|a̱]"), ('e', "[e|E|Ē|ē|E̱|e̱|ɛ]"), ('E', "[e|E|Ē|ē|E̱|e̱|ɛ]"), 
                    ('i', "[i|I|Ī|ī|I̱|i̱]"), ('I', "[i|I|Ī|ī|I̱|i̱]"), ('o', "[o|O|Ō|ō|Ö|ö|O̱|o̱]"), ('O', "[o|O|Ō|ō|Ö|ö|O̱|o̱]"), 
                    ('kw', "[kw|Kw|ku|Ku|Cu|cu]"), ('Kw', "[kw|Kw|ku|Ku|Cu|cu]"), ('k', "[k|K|C|c|Qu|qu]"), ('K', "[k|K|C|c|Qu|qu]"), 
                    ('h', "[h|H|j|J]"), ('H', "[h|H|j|J]"), ('ts', "[ts|Ts|tz|Tz]"), ('Ts', "[ts|Ts|tz|Tz]"), 
                    ('s', "[s|S|c|C|z|Z]"), ('S', "[s|S|c|C|z|Z]"), ('w', "[w|W|Hu|hu|uh]"), ('W', "[w|W|Hu|hu|uh]")],
            
            'OT': [('a', "[a|A|a̱|á̠|à̠|ā|ą̌|ą̌|ą|ą́|ä̱|ą̀|á̧|à̜|a̜|a̹|à|ǎ|ă|ą̂|â|A̱|Ą́|Ą|Ă|A̜]"), ('A', "[aa|A|̱|á̠|à̠|ā|ą̌|ą̌|ą|ą́|ä̱|ą̀|á̧|à̜|a̜|a̹|à|ǎ|ă|ą̂|â|A̱|Ą́|Ą|Ă|A̜]"),
                   ('ä', "[ä|Ä|ą|a̱]"), ('Ä', "[ä|Ä|ą|a̱]"), ('bb', "[bb|b]"), ('b', "[b|B|b̠]"), ('B', "[b|B|b̠]"), 
                   ('cc', "[cc|k]"), ('c', "[c|C|ɔ̀|ɔ|ɔ̌]"), ('C', "[c|C|ɔ̀|ɔ|ɔ̌]"), ('dy', "[dy|y|j]"), 
                   ('ö', "[ö|Ö|ɔ|ɵ́|o̱|ø|Ø]"), ('Ö', "[ö|Ö|ɔ|ɵ́|o̱|ø|Ø]"),
                   ('hu', "[hu|w]"), ('h', "[h|H|j|J|w|W|J̌|ǰ|Ĵ|ĵ|ʰ]"), ('H', "[h|H|j|J|w|W|J̌|ǰ|Ĵ|ĵ|ʰ]"), 
                   ('e', "[e|E|E̱|e̱|é̱|è|ē|ę|ę́|ḝ|ę̌|ȩ|e̜|e̹|Ě|ě|ë̂|ë̌|ê|Ĕ|ĕ|è|ḝ|é̠|ɛ|ɛ̜|ɛ̠|Ɛ|Ɛ̌|ɛ̌|ɛ̂|ɛ́|ɛ̀|ɛ̜̌|ɛ̨̂|ɛ̜́|ξ|ξ́]"),
                   ('E', "[e|E|E̱|e̱|é̱|è|ē|ę|ę́|ḝ|ę̌|ȩ|e̜|e̹|Ě|ě|ë̂|ë̌|ê|Ĕ|ĕ|è|ḝ|é̠|ɛ|ɛ̜|ɛ̠|Ɛ|Ɛ̌|ɛ̌|ɛ̂|ɛ́|ɛ̀|ɛ̜̌|ɛ̨̂|ɛ̜́|ξ|ξ́]"), 
                   ('ë', "[ë|Ë|ɛ|Ɛ]"), ('Ë', "[ë|Ë|ɛ|Ɛ]"), ('gu', "[g|gu|w]"),
                   ('i', "[i|I|I̱|i̱|í̠|Į́|Į́|í̧|ī|Į|į|i̧|í̹|í̜|ǐ|į̌|Ĭ|ĭ|į́|į̀|ì|i̜|ï̀|ï̌|î|į̂]"), ('I', "[i|I|I̱|i̱|í̠|Į́|Į́|í̧|ī|Į|į|i̧|í̹|í̜|ǐ|į̌|Ĭ|ĭ|į́|į̀|ì|i̜|ï̀|ï̌|î|į̂]"),
                   ('k', "[k|K|c|C|qu|cc|qu]"), ('K', "[k|K|c|C|qu|cc|qu]"), ('m', "[m|m̠]"), 
                   ('o', "[o|O|O̱|o̱|ó̠|ó|ō|Ǒ|ǒ|Ŏ|ŏ|Ǫ|ǫ|o̧|ò|ɵ|ɵ̂|ɵ̌|ɵ́|ɵ̀|Ɵ̀|Ɵ|Ø|ø|Ǿ|ǿ|ö́]"),
                   ('O', "[o|O|O̱|o̱|ó̠|ó|ō|Ǒ|ǒ|Ŏ|ŏ|Ǫ|ǫ|o̧|ò|ɵ|ɵ̂|ɵ̌|ɵ́|ɵ̀|Ɵ̀|Ɵ|Ø|ø|Ǿ|ǿ|ö́]"), ('p', "[p̄]"), 
                   ('s', "[s|S|Ŝ|ŝ|z̄]"), ('S', "[s|S|Ŝ|ŝ|z̄]"), ('tz', "[tz|s|z]"),
                   ('u', "[u|U|U̱|u̱|ú̱|ų̄|ú̧|ų̀|u̧|Ų|ų|ų́|u̜|u̹|ū|Ʉ|ʉ|Ʉ́|ʉ́|ʉ̜́|Ʉ̄|ʉ̠|ʉ̌|Ǔ|ǔ|ų̌|ų̂|ʉ̀]"), 
                   ('U', "[u|U|U̱|u̱|ú̱|ų̄|ú̧|ų̀|u̧|Ų|ų|ų́|u̜|u̹|ū|Ʉ|ʉ|Ʉ́|ʉ́|ʉ̜́|Ʉ̄|ʉ̠|ʉ̌|Ǔ|ǔ|ų̌|ų̂|ʉ̀]"),
                   ('w', "[w|W|hu|gu]"), ('W', "[w|W|hu|gu]"), ('x', "[x|X|Š|š|sho]"), ('X', "[x|X|Š|š|sho]"), 
                   ('y', "[y|dy]"), ('j', "[j|dy]"), ('z', "[z|s]")]
            }
    
    if language in dicc.keys():
        array = dicc[language]
        for a in array:
            if a[0] in busq:
                busq = re.sub(a[0], a[1], busq)
    print('MIRANDO LA BUSQUEDA  -  ', busq)
    return busq
    

#Return the search according to parameters
def search_request(path_search, path_files, v_metadata, languages, dicc_search, window, result, result_m):
    input_text_search = read_text_txt(path_search[0])
    files_list = read_txt_files(path_files)
    
    if len(languages)==0 or languages[0]!= path_search[1]:
        languages.insert(0, path_search[1])
        
    array_result = [''] * len(languages)
    array_tmp = array_result.copy() 
    
    for line in input_text_search:
        dicc_search.update( {'line' : line} )
        #tuple_search = search_pattern(dicc_search)        
        #if tuple_search[0]:
        if search_pattern(dicc_search):
            list_pattern = dicc_search['pattern']
            
            if window == 'Vertical' or window == 'Horizontal':
                text = line
                for pattern in list_pattern:                
                    it = re.finditer(pattern, dicc_search['line'])                
                    while iter(it):
                        try:
                            match = next(it)
                            text = re.sub(r'\b'+line[match.start():match.end()]+r'\b', '<strong>'+line[match.start():match.end()]+'</strong>', text)
                            text = mark_safe(text)
                        except:
                            break  
                
                if window == 'Vertical':
                    array_tmp[0]=text
                    #array_tmp[0]=line
                elif window == 'Horizontal':
                    array_tmp[0]=(languages[0], text)
                    #array_tmp[0]=(languages[0], line)
                
                for j,file in enumerate(files_list):
                    
                    #result = [ [lang1, lang2, lang3, ..], [line1, line2, line3, ...], ...]
                    if window == 'Vertical':
                        array_tmp[languages.index(path_files[j][1])] = file[input_text_search.index(line)]
                    
                    #result = [ [(lang1, line1), (lang2, line2), (lang3, line3), ...], [], ...]
                    elif window == 'Horizontal':
                        array_tmp[languages.index(path_files[j][1])] = (path_files[j][1],
                                                                        file[input_text_search.index(line)])
                        for k,x in enumerate(array_tmp):
                            if '' in x:
                                array_tmp[k]= (languages[k], '')
                
                result.append(array_tmp)
                result_m.append(v_metadata)
                array_tmp = array_result.copy()
            
            #result = [ [(lang1, [izq, cen, der]), (lang2, line2), (lang3, line3), ...], [], ...]
            elif window == 'KWIC':                
                #list_pattern = dicc_search['pattern']
                
                for pattern in list_pattern:                
                    it = re.finditer(pattern, dicc_search['line'])                
                    while iter(it):
                        try:
                            match = next(it)
                            array_KWIC = []
                            array_KWIC.insert(0, line[:match.start()])
                            array_KWIC.insert(1, line[match.start():match.end()])
                            array_KWIC.insert(2, line[match.end():])
                            array_tmp[0]=(languages[0], array_KWIC)
                            for j,file in enumerate(files_list):
                                array_tmp[languages.index(path_files[j][1])] = (path_files[j][1],
                                                                                file[input_text_search.index(line)])

                            for k,x in enumerate(array_tmp):
                                if '' in x:
                                    array_tmp[k]= (languages[k], '')

                            result.append(array_tmp)
                            result_m.append(v_metadata)
                            array_tmp = array_result.copy()

                        except:
                            break     
          
    if window == 'Vertical' and len(result)!=0 and result[0]!=languages:
        result.insert(0, languages)                             

    return result, result_m
