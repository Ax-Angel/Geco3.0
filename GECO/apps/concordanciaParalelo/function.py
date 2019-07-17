import re

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
    
    pattern1 = pattern_i+pattern_w1+pattern_f
    pattern2 = pattern_i+pattern_c1+pattern_w1+pattern_c2+pattern_f
    pattern3 = r'(?:<\w*>)'
    pattern4 = pattern_i+pattern_a+pattern_w1+pattern_f
    pattern5 = pattern_i+pattern_w1+pattern_a+pattern_f
    pattern6 = pattern_i+pattern_w1+pattern_e+pattern_a+pattern_e+pattern_w1+pattern_e+pattern_a+pattern_f
    pattern7 = pattern_i+pattern_w1+pattern_s+pattern_w1+pattern_f
    pattern8 = pattern_i+pattern_w1+pattern_e+pattern_d+pattern_e+pattern_w1+pattern_f
    pattern9 = pattern_i+pattern_w1+pattern_e+pattern_ds+pattern_e+pattern_w1+pattern_f
    
    dicc_search = dict()
    
    if re.search(pattern9, search_p):
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
    
    return search

#Return the search according to parameters
def search_request(path_search, path_files, languages, dicc_search, window, result):
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
            
            if window == 'Vertical' or window == 'Horizontal':
                if window == 'Vertical':
                    array_tmp[0]=line
                elif window == 'Horizontal':
                    array_tmp[0]=(languages[0], line)
                
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
                array_tmp = array_result.copy()
            
            #result = [ [(lang1, [izq, cen, der]), (lang2, line2), (lang3, line3), ...], [], ...]
            elif window == 'KWIC':                
                list_pattern = dicc_search['pattern']
                
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
                            array_tmp = array_result.copy()

                        except:
                            break     
          
    if window == 'Vertical' and len(result)!=0 and result[0]!=languages:
        result.insert(0, languages)                             

    return result
