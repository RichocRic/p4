from tinydb import TinyDB, Query



db = TinyDB('../bdd/database.json')
joueurs_table = db.table('joueurs')
tournois_table = db.table('tournois')
match_table = db.table('match')
tour_table = db.table('tour')

def aparaige(idtournois):
    
    """ """
    element= Query()

    result = match_table.search(element['id tournois'] == idtournois)

    tourEnCours = len(result)//4+1   

    liste_anciens_matchs = list(map(lambda x:[x['id du joueur1'],x['id du joueur2']],result))

    result = tournois_table.search(element['id du tournois'] == idtournois)

    liste_joueurs = result[0]['id des joueurs']

    liste_joueurs =  list(map(lambda x: joueurs_table.search(element['Identifiant du joueur'] == x)[0],liste_joueurs))

    liste_joueurs.sort(key=lambda x:x["Classement du joueur"],reverse=True)
    liste_joueurs.sort(key=lambda x:x["Score du joueur"],reverse=True)
    liste_joueurs=list(map(lambda x:x["Identifiant du joueur"],liste_joueurs))



    #print(liste_joueurs)

    #liste_joueurs=["a","b","c","d","e","f","g","h"]
    d=liste_joueurs

    #liste_anciens_matchs=[["a","b"],["b","c"],["e","h"],["a","g"]]
    d1=liste_anciens_matchs

    d2=[]
    for i in range(8):
        for j in range(i+1,8):
            if [d[i],d[j]] not in d1:
                d2.append([d[i],d[j],i+j])

    d2.sort(key=lambda x:x[2],reverse=True)
    list_1=[]
    list_1.append(d2[0])
    list_1.append(d2[7])
    
    
    def check_player_exist(list_matchs,match):
        
        for i in list_matchs:
            if match[0]==i[0] or match[0]==i[1] or match[1]==i[0] or match[1]==i[1]:
                return False
        return True
    
    def add_elem(big_list,indexy,small_list):
        for j in range(indexy+1,len(big_list)):
            if (len(small_list)>indexy):small_list.pop()
            if check_player_exist(small_list,big_list[j]):
                small_list.append(big_list[j])
                if len(small_list)==4:
                    return small_list
        return add_elem(big_list)
                
    def list_comb(list_comb):
        list2=[]
        for i in range(len(list_comb)):
                if len(list2)>0:list2.pop()
                list2.append(list_comb[i])
                for j in range(i+1,len(list_comb)):
                    if (len(list2)>1):list2.pop()
                    if check_player_exist(list2,list_comb[j]):
                        list2.append(list_comb[j])
                        for k in range(j+1,len(list_comb)):
                                if (len(list2)>2):list2.pop()
                                if check_player_exist(list2,list_comb[k]):
                                    list2.append(list_comb[k])
                                    for l in range(k+1,len(list_comb)):
                                            if (len(list2)>3):list2.pop()
                                            if check_player_exist(list2,list_comb[l]):
                                                list2.append(list_comb[l])
                                                return list2                          
        return -1
    
    if tourEnCours > 4:
        return -1

    if tourEnCours > 1:
        lstCombi = list(map(lambda x : [x[0], x[1]], list_comb(d2)))
    else:
        lstCombi = list(map(lambda x : [liste_joueurs[x], liste_joueurs[x+4]], range(4)))
        
    return lstCombi

#print(aparaige("52a055c2-0349-11ed-9461-acde48001122"))