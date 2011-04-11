def string(truc):
    if truc == None : return "?"
    if type(truc) == bool :
        if truc : return str(1.0)
        else    : return str(0.0)
    else : return str(truc)

class ArfFile:
    """
    Vise a la production de ce genre de document :

    % commentaire
    @RELATION face_emotion

    @ATTRIBUTE mouth_width  NUMERIC
    @ATTRIBUTE mouth_height NUMERIC
    @ATTRIBUTE smile        NUMERIC
    @ATTRIBUTE class        {Anger,Disgust,Fear,Happiness,Neutral,Sadness,Surprise}

    @DATA
    1.0, 3.0, ?, Happiness

    Cette classe est donc un automate a 2 etats : specification des attributs, PUIS
    ecritures des instances. On ne peut pas revenir au premier etat a ce jour.
    """
    def __init__(self, nom, relation):
        self.filename = nom + '.arff'
        self.attribut_list = []
        self.relation = relation
        self.no_more_attribute = False
        self.FILE = None
    
    def no_more_data(self) :
        self.FILE.close()

    def add_attribute_bool(self, nom):
        if self.no_more_attribute : 
            raise NameError('Instance has been written' +
                            ',can\'t add attributes anymore.')
        self.attribut_list.append((nom, 'NUMERIC'))
    
    def add_attribute_numeric(self, nom):
        if self.no_more_attribute : 
            raise NameError('Instance has been written' +
                            ',can\'t add attributes anymore')    
        self.attribut_list.append((nom, 'NUMERIC'))
    
    def add_attribute_enum(self, nom, valeurs):
        if self.no_more_attribute : 
            raise NameError('An instance has been written, ' +
                            'can\'t add attributes anymore')

        self.attribut_list.append((nom, valeurs))
    
    def add_instance(self, dictionary) :
        
        def write_instance (dic) :
            # On ecrit l'instance dans le fichier
            stri = string(dic[self.attribut_list[0][0]])
            for i in range(1,len(self.attribut_list))  :
                a = self.attribut_list[i]
                stri = stri + ", " + string(dictionary[a[0]])
            self.FILE.write(stri+"\n")
        
        def write_structure () :
            # On decrit la structure d'une instance dans le fichier
            self.FILE.write("@RELATION\t'" + self.relation + "'\n\n")
            for a in self.attribut_list : # pour chaque attribut
                if type(a[1]) == list : # si c'est une enumeration ...
                    typ = "{" + a[1][0]
                    for i in range(1,len(a[1])) :
                        typ = typ + "," + a[1][i]
                    typ = typ + "}"
                else : # sinon c'est un NUMERIC
                    typ = a[1]
                self.FILE.write("@ATTRIBUTE\t" + a[0] +"\t"+ str(typ) + "\n")
            self.FILE.write("\n@DATA\n")
            self.no_more_attribute = True
        
        if self.FILE == None : self.FILE = open(self.filename,"w")
        if (not self.no_more_attribute) : write_structure ()
        write_instance(dictionary)
            

# TEST :
#print " TEST STRING : "
#print string(None)
#print string(True)
#print string(False)
#print string(3.14)
#print string('blabla')
#print " FIN TEST STRING "
#
#
#arf = ArfFile("test_arf", "relation_test")
#arf.add_attribute_bool("le_bool")
#arf.add_attribute_numeric("le_nombre")
#arf.add_attribute_enum("quoi", ['truc', 'bidule', 'machin', 'chose' , 'meta'])
#
#dic = dict([('le_bool', True),('le_nombre', 3.0), ('quoi', 'bidule')])
#dic1 = dict([('le_bool', True),('le_nombre', 2.0), ('quoi', 'chose')])
#dic2 = dict([('le_bool', False),('le_nombre', 7.0), ('quoi', 'metabidule')])
#arf.add_instance(dic)        
#arf.add_instance(dic1)
#arf.add_instance(dic2)
#arf.no_more_data() # plus propre
#print "regarder dans test_arf"
