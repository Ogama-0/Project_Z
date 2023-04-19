import pytmx, pygame, pyscroll
from sources.code_source.dialogue import inforamtion,Dialogue
from dataclasses import dataclass
from sources.code_source.enigme_code import enigme_sprite, enigme_setup, dialogue_enigme_setup,interact_ecrit
from sources.code_source.element_mouvent import sprite_mouvent_screen
from sources.code_source.portail import Setup_Porte , Portail, stk_dialogue, Stk_porte,Porte


# ----------------------------- OBJECTS -------------------------- #

class Stockage :
    def __init__(self):
        """ j'utilise Stockage pour stocker des variable globale que j'usitilise sur tout l'ensembre du programe"""
        self.musique_Manoir = pygame.mixer.Sound("sources/musique/manoir/Mansion_music.wav")
        self.musique_defaut = self.musique_Manoir
        self.musique_futur = pygame.mixer.Sound("sources/musique/future/musique futur.wav")
        self.musiques = {}
        self.musiques["futur"] = self.musique_futur
        self.musiques["Manoir"] = self.musique_Manoir
        self.curent_musique = "Manoir"
        self.musique = True
        self.volume_musique = 0.25
        self.pause = False
        self.curent_degrader = False
        self.contre_curent_degrader = False
        self.curent_tiping = False
        self.chec_reponse = False
        self.preimer_pass_ciné = True
        self.curent_fin = False
        self.dialogue_afficher = False
        self.Fin = False
        self.decrechendo = False
        self.Fin_backgrounds =  [pygame.transform.scale(pygame.image.load("sources/sprite/autre/menu/Fin1.png"),(1080,720)),pygame.transform.scale(pygame.image.load("sources/sprite/autre/menu/Fin2.png"),(1080,720)),pygame.transform.scale(pygame.image.load("sources/sprite/autre/menu/Fin3.png"),(1080,720))]

@dataclass
class Map :
    type : str #"exterieur" = exterrieur "interieur" = "interieur" "enigme + nom_énigme " = enigme
    name : str
    murs : list[pygame.Rect]
    group : pyscroll.PyscrollGroup
    tmx_data : pytmx.TiledMap
    spawn : list[int]
    portails : list[Portail]
    nom_enigme : list[str]
    enigmes : dict[enigme_sprite]
    Dialogue : dict[Dialogue]
    element_mouvant_screen : list[sprite_mouvent_screen]
    zonne_afficher_info : dict[int:list[pygame.Rect]]
    list_porte : dict
    clefs : dict[str,bool]
    musique : str


    

# ---------------------------------------------- MAP MANAGER ---------------------------------------------------#

class Map_manager :

    def __init__(self,screen : pygame.surface.Surface, player):
        self.premier_passage_Globale = True
        noir = (0,0,0)
        blanc = (255,255,255)
        self.stockage_valeur = Stockage()


        

        self.maps = dict() #création d'un dico avec tt les maps avec {nom : donné de la classe Map}
        self.curent_map = "Manoir"# map du spawn
        self.player = player # defini du joueur de game
        self.screen = screen #definition du screen
        self.curent_dialogue = "start"
        self.curent_sprite_enigme = 0 #le sprite acutelle de l'énigme en question
        position_dialogue = (200,600) # la position du dialogue
        text_spawn = ["???   :    bzz ... ","???    :    Nanit ?","???    :    ...","??? :     Tu m'entends ?","??? :    Tu vas bien ?","??? :    bzz...","??? :    C'est moi Xini!, Ton ami !","Xini :    Quelqu'un semble t'avoir envoyé dans le passé...","Xini :    Il faut vite que tu trouves un moyen de retourner dans notre ere et que tu retrouves ton créateur","Xini :    ... bzz ... ","Xini :    Si la plante que tu as sur la tête grandit trop, elle risque de détruire ta carte mere !", "Xini :    ...  bzz ... ","Xini :    Je capte de mo.. en moins bi..bzzt..","Xini :    Tu dois parcourir... dans... bzz...siecles... Trouv... machine... voyager... bzzt... temps!...","Xini :     ...bip ...bip ...bip."]
        dialogue_actuelle = stk_dialogue("start",text_spawn,(700,100),position_dialogue,"boite_dialogues")
        

        self.premier_passage = True
        self.stockage = ""
        self.frame = 0 
        self.curent_tiping = False
        self.premier_passage_dialogue = False

        self.clefs = {}
        

    #----------------------------- Portail --------------------------------#    
    #Portail("","","","")

        portail_manoir_moyen_test1 =    [Portail("Manoir","sortie porte principal manoir","couloir_fin","spawn",False)
                                        ]

        portail_enigme_horloge =       [Portail("enigme_horloge","sortie  labyrhinte","Manoir","sortie horloge_labyrhinte", True),
                                        Portail("enigme_horloge","sortie_enigme_horloge","Manoir","sortie  horloge",True)
                                        ]
        
        portail_map_futur =            [Portail("futur","enigme_portail","enigme_portail","spawn",False),
                                        Portail("futur","entrer_chimie","chimie","entrer_chimie",False),
                                        Portail("futur","entrer_tableau","tableau","spawn",False),
                                        Portail("futur","enigme_goblet","enigme_goblet","spawn",False)
                                        ]
        portail_couloir_fin =          [Portail("couloir_fin","direction_manoir","Manoir","entrer manoir porte principale",False),
                                        Portail("couloir_fin","zonne de detection machine_temps","futur","spawn",True)
                                        ]
        portail_enigme_portail =       [Portail("enigme_portail","un","enigme_portail","2",True),
                    
                                        Portail("enigme_portail","deux","enigme_portail","3",True),
                                        Portail("enigme_portail","moin_deux","enigme_portail","perdu",True),
                                        Portail("enigme_portail","perdu_2","enigme_portail","perdu",True),
                                        
                                        Portail("enigme_portail","trois","enigme_portail","4",True),
                                        Portail("enigme_portail","moin_trois","enigme_portail","2",True),
                                        Portail("enigme_portail","perdu_3","enigme_portail","perdu",True),

                                        Portail("enigme_portail","quatre","enigme_portail","6",True),
                                        Portail("enigme_portail","moin_quatre","enigme_portail","3",True),
                                        Portail("enigme_portail","perdu_4","enigme_portail","perdu",True),

                                        Portail("enigme_portail","ez","enigme_portail","fin",True),
                                        Portail("enigme_portail","moin_sixe","enigme_portail","4",True),
                                        Portail("enigme_portail","perdu_6","enigme_portail","perdu",True),
                                        
                                        Portail("enigme_portail","sortie_enigme_portail","futur","clef_enigme_portail",False),
                                        Portail("enigme_portail","sortie_portail","futur","sortie_portail_",False)
                                        ]
        portail_chimie =               [Portail("chimie","sortie_chime","futur","sortie_chime",False)
                                        ]
        portail_tableau =              [Portail("tableau","sortie_tableau","futur","sortie_tableau",False)
                                        ]
        portail_goblet =               [Portail("enigme_goblet","sortie_goblet","futur","retour_goblet",False)
                                        ]
    # ----------------------------- Porte -------------------------------- #
        porte_sortie_condi = ["horloge","Grosse_Dame","armure"]

        portes_manoir = [Stk_porte("porte_entrer",False,porte_sortie_condi,["cette porte a 3 serrures !"],8,-1)
                        ]
        self.clefs_sans_dialogue = ["portail","tableau_enigme","chimie_","goblet_"]
        condi_porte_principale_futur = ["code"]
        porte_petit_futur_condi_portail = ["portail"]
        porte_petit_futur_condi_tableau = ["tableau_enigme"]
        porte_petit_futur_condi_chimie = ["chimie_"]
        porte_petit_futur_condi_goblet = ["goblet"]


        portes_futures = [Stk_porte("principale",False,condi_porte_principale_futur,["entrez le mot de passe dans le terminal situer a votre gauche"],8,22),
                          Stk_porte("petit_futur_portail",False,porte_petit_futur_condi_portail,["le badge pour ouvrir la piece ne doit pas être tres loin."],8,2),
                          Stk_porte("petit_futur_tableau",False,porte_petit_futur_condi_tableau,["le badge pour ouvrir la piece ne doit pas être tres loin"],8,2),
                          Stk_porte("petit_futur_chimie",False,porte_petit_futur_condi_chimie,["le badge pour ouvrir la piece ne doit pas être tres loin"],8,2),
                          Stk_porte("petit_futur_goblet",False,porte_petit_futur_condi_goblet,["le badge pour ouvrir la piece ne doit pas être tres loin"],8,2)
                          ]
        clefs_manoir = {}
        clefs_future = {}

        self.porte_rect = []
    # -------------------- Clefs -------------------- #
        for porteM in portes_manoir :
            for condiM in porteM.condi :
                clefs_manoir[condiM] = False
        
        for porteF in portes_futures :
            for condiF in porteF.condi :
                clefs_future[condiF] = False
        
        


        
    #------------------------------ enigme ------------------------------- #
        énigme_nom = {}
        nombre_sprite_enigme = {} 
        égnime_de_manoir_moyen_test1 =  ["Manoir","horloge",5]
        enigme_couloir_fin = ["couloir_fin","machine_temps",3]
        enimge_futur = ["futur","Docteur_Z",2]
        enimges = [enigme_couloir_fin,égnime_de_manoir_moyen_test1,enimge_futur]
        
        for enigme in enimges :
            for i in range(0,len(enigme),3) :
                énigme_nom[enigme[i]] = []
                nombre_sprite_enigme [enigme[i]] = []

            for i in range(0,len(enigme),3) :
                énigme_nom[enigme[i]].append(enigme[i+1])
                nombre_sprite_enigme [enigme[i]].append(enigme[i+2])
        self.sprite_enigme_descente = False

        self.frame_ = 0

        
#-----------------------------------------dialogue-----------------------------------------#
        
        #dialogue_de_manoir_moyen_test1 = ['nom',["text",mettre "entrer votre reponse"a l'endroit ou il faut que le joueur ecrive],taille_background,dialogue_enigme_position]
        #pour la zonne de colision  on fait un get obj by name == dialogue_de_manoir_moyen_test1[i] (donc la par exemple 'lettre')
        

        texte_lettre = ["Il y a de cela fort longtemps, une armure de fer tronait dans son manoir. Se dressant fierement au coeur de l'armurerie, elle protégeait le plus précieux des trésors : la clé de la liberté. Cependant, personne ne savait ou elle se trouvait.Plus loin dans la grande salle, isolée de tous, se tenait une horloge a pendule qui égrenait les secondes avec une régularité effrayante. On racontait que si l'on parvenait à déchiffrer les mystérieux messages que l'horloge transmettait, alors on trouverait la clé. Piece maitresse du couloir des arts, les yeux du portrait de la grande dame semblaient suivre tous les mouvements dans la piece, comme si elle était à la recherche de quelque chose ou de quelqu'un. On disait que si l'on parvenait à comprendre le regard de la dame, on trouverait la clé. Ainsi, la légende raconte que seul celui qui résoudrait les énigmes de l'armure de fer, horloge à pendule et du portrait de la grande dame découvrirait la clé cachée et se libérerait du sommeil éternel de ce manoir.                                                                                                                                                                                                                                                                                                                                             Mais attention, car ceux qui se trompaient                                        n'en ressortaient jamais…"]
        texte_livre = ""
        texte_entrer_futur = ["Xini   :      fiou! tu es enfin de retour chez nous!","Xini   :      Vite la fleur sur ta tête grandit de plus en plus, va retrouver Docteur Z dans son laboratoire !", "Xini   :      Docteur Z se trouve derrière la grande porte au fond de la salle.","Xini   :      Je crois qu'il s'est enfermé à l'intérieur. Il faut un code à 4 lettre pour entrer dans son bureau.","Xini   :      le connaisant je suis sur qu'il sera en rapport avec l'informatique !","Xini   :      J'ai entendu dire qu'il avait noté chaque lettre du code sur un post-It dans chacune des salles. Va vite les fouiller" ]
        texte_dialogue_final = ["Docteur Z   :   Te voila enfin Nanit, je t'attendais.","Docteur Z   :      Vient ici Nanit, j'ai quelque chose à t'avouer.","Docteur Z   :      C'est moi qui t'ai envoyé dans le passé","Docteur Z   :      Je comprends ton incompréhension, mais j'ai eu une bonne raison d'avoir fait ça.","Docteur Z   :      Je me fais vieux et ma jeunesse s'est déjà envolée depuis bien longtemps.","Docteur Z   :      Cela fait depuis que j'ai mis les pieds dans cette ville, que je travaille jour et nuit sur le projet de ma vie ","Docteur Z   :      Le Project Z !","Docteur Z   :       c'est une machine à remonter dans le temps !! ","Docteur Z   :      Et c'est seulement après 70 ans de travail acharné que Le Projet Z arriva enfin à terme.","Docteur Z   :      Mais j'ai peur qu'après ma mort, d'autres scientifiques mal intentionné chercheront à me le  voler.","Docteur Z   :      J'ai donc besoin de quelqu'un de confiance qui saura protéger mon projet ","Docteur Z   :      et ce quelqu'un, c'est toi. Mais j'avais besoin de juger si tu étais prêt pour cette lourde tâche,","Docteur Z   :      et c'est pour cela que je t'ai envoyé voyager dans le passé. ","Docteur Z   :      Et ne t'inquiètes pas pour la plante, elle n'avait que pour but de t'apprendre à gérer ton temps.","Docteur Z   :      Elle est inoffensive, je te la retirerai plus tard.","Docteur Z   :      Maintenant suis moi, ton enseignement de gardien du temps est loin d'être terminé ..."]
        texte_B = ["Sur le post It il est écrit : 'B'"]
        texte_I = ["Sur le post-It il est écrit : 'I'"]
        texte_T = ["Sur le post-It il est écrit :  'T'"]
        texte_S = ["Sur le post-It vous arrivez a dechiffrer : 'S'"]
        
        position_livre = (310,50)
        dimmention_livre = (450,650)
        position_tableaux = (210,50)
        dimmentrion_tableaux = (600,600)
        position_txt_tableaux = (255,610)
        position_tiping_tableaux = (285,610)

        dimmention_dialogue = (700,100)

        dialogue_de_manoir_moyen_test1 = [dialogue_actuelle,
                                          stk_dialogue("lettre",texte_lettre,(600,650),(270,50),"lettre"),
                                          stk_dialogue("livre_force",texte_livre,dimmention_livre,position_livre,"livre"),
                                          stk_dialogue("livre_heure",texte_livre,dimmention_livre,position_livre,"livre"),
                                          stk_dialogue("livre_s",texte_livre,dimmention_livre,position_livre,"livre"),
                                          stk_dialogue("livre_banquet",texte_livre,dimmention_livre,position_livre,"livre"),
                                          stk_dialogue("livre_le_parfum",texte_livre,dimmention_livre,position_livre,"livre"),
                                          stk_dialogue("livre_le_monde",texte_livre,dimmention_livre,position_livre,"livre"),
                                          stk_dialogue("livre_gargantua",texte_livre, dimmention_livre,position_livre,"livre"),
                                          stk_dialogue("Grosse_Dame",["mon tout est un batiment","entrer votre reponse","Dans les livres tu trouveras le mot caché"],dimmention_dialogue,position_dialogue,"tiping","forteresse",True),
                                          stk_dialogue("armure",["nombre a 3 chiffres"," "],(600,500),(240,110),"tiping","993",True,(315,350), position_tiping = (500,410))
                                          ]
        dialogue_furur =                [stk_dialogue("code",[" ","CODE INCORRECT"],(600,600),(240,50),"tiping","BITS",True,(395,380),position_tiping = (490,380)),
                                         stk_dialogue("debut",texte_entrer_futur,dimmention_dialogue,position_dialogue,"boite_dialogues",cinematique = True),
                                         stk_dialogue("dialogue_final",texte_dialogue_final,dimmention_dialogue,position_dialogue,"boite_dialogues",cinematique = True),
                                         stk_dialogue("B",texte_B,dimmention_dialogue,position_dialogue,"boite_dialogues"),
                                         stk_dialogue("I",texte_I,dimmention_dialogue,position_dialogue,"boite_dialogues"),
                                         stk_dialogue("T",texte_T,dimmention_dialogue,position_dialogue,"boite_dialogues"),
                                         stk_dialogue("S",texte_S,dimmention_dialogue,position_dialogue,"boite_dialogues"),
                                         stk_dialogue("murs_invi_D",["Xini   :      Il y a des murs invisible !!!","Xini   :      j'ai repéré un post it en haut a gauche de la salle."],dimmention_dialogue,position_dialogue,"boite_dialogues",cinematique = True)
                                       ]
        
        dialogue_tableau =              [stk_dialogue("Turing",["' j'ai inventé l'ordinateur et je suis le pionner de l'AI '","entrez le nom de famille de cette personne, : ", " ","non ! , seulement la premiere lettre est en majuscule ex : De La Fontaine"],dimmentrion_tableaux,position_tableaux,"tiping","Turing",True,position_txt_tableaux,noir,False,position_tiping_tableaux),
                                         stk_dialogue("De Vinci",["'j'ai peint la Joconde'","entrez le nom de famille de cette personne, : ", " ","non ! , seulement la premiere lettre est en majuscule ex : De La Fontaine"],dimmentrion_tableaux,position_tableaux,"tiping","De Vinci",True,position_txt_tableaux,noir,False,position_tiping_tableaux),
                                         stk_dialogue("Lovelace",["' j'ai écrit le tout premier programme informatique '","entrez le nom de famille de cette personne, : ", " ","non ! , seulement la premiere lettre est en majuscule ex : De La Fontaine"],dimmentrion_tableaux,position_tableaux,"tiping","Lovelace",True,position_txt_tableaux,noir,False,position_tiping_tableaux),
                                         stk_dialogue("Von Neumann",["' j'ai créé un modele de mon nom pour l'architecture des ordinateurs '","entrez le nom de famille de cette personne, : ", " ","non ! , seulement la premiere lettre est en majuscule ex : De La Fontaine"],dimmentrion_tableaux,position_tableaux,"tiping","Von Neumann",True,position_txt_tableaux,noir,False,position_tiping_tableaux)
                                        ]
        dialogue_couloir_fin =          [stk_dialogue("1",["Xini   :      brrr ce couloir est angoissant ! "],dimmention_dialogue,position_dialogue,"boite_dialogues",cinematique = True),
                                         stk_dialogue("2",["Xini   :      vite part ce couloir m'angoisse !"],dimmention_dialogue,position_dialogue,"boite_dialogues",cinematique = True),
                                         stk_dialogue("3",["Xini   :      Voila la machine a voyager dans le temps !"],dimmention_dialogue,position_dialogue,"boite_dialogues",cinematique = True)
                                         ]
        dialogue_enigme_chimie =        [stk_dialogue("chimie_",["ajouter les lettres entre elles pour crée la solution dans l'ordre alphabetique exemple : ACD"," ","Perdu ! "],(600,600),(240,60),"tiping","BCD",True,(300,570))
                                        ]
        dialogues_enigme_goblet =       [stk_dialogue("goblet_",["entrer un lettre en majuscule ,","entrer votre reponse"],(600,600),position_livre,"tiping","D",True,(346,574))

        ]
        clef_enigme_goblet = {}
        clef_enigme_goblet["goblet_"] = False

        clef_enigme_tableau = {}
        for dia in dialogue_tableau :
            clef_enigme_tableau[dia.reponse] = False


# ---------------------------------- élément mouvant screen ----------------------------- #
        # [nom : str, nombre_de_sprite : int, position : tuple(x,y), cb1 de frame entre les images : int ]
        sprite_mouvement_horloge = ['premier_plan',10,(0,0), 6 ]

# ---------------------------------inforamtion --------------------------------------------- #
        self.info = ['e pour examiner','TAB','SHIFT','e pour sortir',""]

        self.infos_manoir = {}
        for i in self.info :
            self.infos_manoir[i] = (inforamtion(self.screen,f"{i}"))
# ------------------------------------- musique --------------------------------------------#
        self.musique_debaze = self.stockage_valeur.musique_defaut
        musique_manoir = "Manoir"
        musique_future = "futur"
       

   
#------------------------------------------suite---------------------------------------------#


        self.enregistrer_une_map("interieur","Manoir",portail_manoir_moyen_test1,portes_manoir, énigme_nom["Manoir"], nombre_sprite_enigme["Manoir"], dialogue_de_manoir_moyen_test1,clefs = clefs_manoir, musique = musique_manoir)
        self.enregistrer_une_map("enigme_inquietant","enigme_horloge",portail_enigme_horloge,[],sprite_en_mouvent_screen = sprite_mouvement_horloge,musique = musique_manoir) 
        self.enregistrer_une_map("interieur", "futur",portail_map_futur,portes_futures,énigme_nom["futur"],nombre_sprite_enigme["futur"], dialogue_furur,clefs = clefs_future,musique = musique_future)
        self.enregistrer_une_map("interieur","couloir_fin",portail_couloir_fin,[],énigme_nom["couloir_fin"],nombre_sprite_enigme["couloir_fin"],dialogue_couloir_fin,musique = musique_manoir)
        self.enregistrer_une_map("interieur","enigme_portail", portail_enigme_portail,musique = musique_future)
        self.enregistrer_une_map("interieur","chimie", portail_chimie,liste_dialogues = dialogue_enigme_chimie,musique = musique_future)
        self.enregistrer_une_map("interieur","tableau",portail_tableau,liste_dialogues = dialogue_tableau, clefs = clef_enigme_tableau,musique = musique_future)
        self.enregistrer_une_map("interieur","enigme_goblet",portail_goblet,liste_dialogues= dialogues_enigme_goblet,clefs = clef_enigme_goblet , musique = musique_future)
        self.tp_joueur('spawn',True)
        self.changer_musique(self.curent_map,True)
        self.chec_enigme_clefs()
        self.premier_passage_Globale = False

    

    #--------------------------------------------- Fonction ---------------------------------------------------#


    def enregistrer_une_map(self, map_type : str , name_map : str, list_portail : list[Portail], list_porte : list[Stk_porte] = []  , name_enigme = [], nombre_sprite_enigme = 0 ,liste_dialogues : list[stk_dialogue] = [] , sprite_en_mouvent_screen = [],clefs = {},musique = None) : #nom_enigme est une list avec le nom de l'enigme
        """fonction qui créé la map avec tout les paramettres, la stock dans un dictionaire avec le nom de la map en key et un object Map en value"""
        
        tmx_data = pytmx.util_pygame.load_pygame(f"sources/map/map_data/{name_map}.tmx")#on charge la bonne map Kappa
        map_data = pyscroll.data.TiledMapData(tmx_data)
        
        #afficher ce tmx sur le screen
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())


        
        info = self.info 
        dialogues_final = {}

        for dialogue in liste_dialogues :

            dialogue_data = dialogue_enigme_setup(tmx_data,dialogue)
            dialogues_final[dialogue.name] = Dialogue(self.screen,dialogue_data.dialogues)
        


            
        
        #gerer le zoom de la cam :
        if map_type == "exterieur" :
            map_layer.zoom = 1.5
        elif map_type == "enigme_inquietant":
            map_layer.zoom = 2
        elif map_type == "interieur" :
            map_layer.zoom = 2.15
        elif map_type == "test" :
            map_layer.zoom = 2

        self.spawn = tmx_data.get_object_by_name('spawn')
        
        self.spawn = [self.spawn.x,self.spawn.y]

        #il faut donc dessiner le groupde de calque (différentes couche du jeu pour afficher )
        
        
            # ------------------ Colisions ----------------- #
        self.murs = []
        for obj in tmx_data.objects :
            if obj.type == 'collision' :
                self.murs.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        
        
        group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 5)
        group.add(self.player)
        
       

        # -------------------------- enigme ----------------------------- #
        enigme_ = enigme_setup(tmx_data, name_enigme, name_map, nombre_sprite_enigme, group)

        # ------------------ sprite_mouvent_screen ---------------#
        sprites_mouvant = []
        for i in range(0,len(sprite_en_mouvent_screen),4) :
            sprites_mouvant.append(sprite_mouvent_screen(sprite_en_mouvent_screen[i],sprite_en_mouvent_screen[i+1],self.screen,sprite_en_mouvent_screen[i+2],sprite_en_mouvent_screen[i+3]))
        
        # ------------------------- info ------------------------------- #
        zonne_afficher_info = {}

        for i in info :
            zonne_collision = []

            for obj in tmx_data.objects :
                

                if obj.type == f'zonne_collsions_{i}' :

                    zonne_collision.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))
            zonne_afficher_info[i] = zonne_collision
        
        # --------------------------- porte ---------------------------- #

        list_Portes = {}
        for stk_porte in list_porte :
            porte = Setup_Porte(tmx_data,group,stk_porte)
            d = porte.porte.dialogue

            porte.porte.dialogue =  Dialogue(self.screen,d)
            list_Portes[porte.porte.nom] = porte.porte
            dialogues_final[porte.porte.nom] = porte.porte.dialogue

                
        #on crée un object Map 
        self.maps[name_map] = Map(map_type, name_map, self.murs, group, tmx_data, self.spawn, list_portail, name_enigme, enigme_.enigmes,dialogues_final , sprites_mouvant ,zonne_afficher_info,list_Portes,clefs,musique) 
        
        
    
    def get_map(self,n = None) -> Map : 
        if n == None :
            return self.maps[self.curent_map]
        else : 
            return self.maps[n]
    def get_group(self,name_map = None) -> pyscroll.group.PyscrollGroup : return self.get_map(name_map).group
    def get_murs(self,name_map = None) -> list[pygame.rect.Rect] : return self.get_map(name_map).murs 
    def get_object(self, name,name_map = None)-> pytmx.TiledObject : return self.get_map(name_map).tmx_data.get_object_by_name(str(name))
    def get_tmx_data(self,name_map = None)-> pytmx.TiledMap : return self.get_map(name_map).tmx_data
    def get_enigme(self,nom, name_map = None)  : return self.get_map(name_map).enigmes[nom]
    def get_cara_sprite_enigme(self,nom,name_map = None)-> enigme_sprite :  return self.get_enigme(nom,name_map).sprite_enigme
    def get_sprite_nombre_enigme(self,nom,name_map = None)-> int : return self.get_cara_sprite_enigme(nom,name_map).nombre_enigme
    def get_Dialogues(self,nom_map = None)-> dict : return self.get_map(nom_map).Dialogue
    def get_Dialogue(self,name = None,nom_map = None) -> Dialogue: 
        if name == None :
            return self.get_map(nom_map).Dialogue[self.curent_dialogue]
        return self.get_map(nom_map).Dialogue[name]
    def get_element_mouvant_screen(self,nom_map = None) -> list[sprite_mouvent_screen]: return self.get_map(nom_map).element_mouvant_screen
    def get_collision_info(self,name_map = None)-> dict: return self.get_map(name_map).zonne_afficher_info
    def get_rect_info(self,touche,name_map = None) : return self.get_collision_info(name_map)[touche]
    def get_tiping(self) -> bool : return self.get_Dialogue().inte.tiping
    def get_position_tiping(self) -> tuple[int] : return self.get_Dialogue().position_tiping
    def get_inte(self,name = None) -> interact_ecrit : return self.get_Dialogue(name).inte
    def get_portes(self,nom_map = None) -> dict : return self.get_map(nom_map).list_porte
    def get_porte(self,nom,nom_map = None) -> Porte : return self.get_portes(nom_map)[nom]
    def get_clefs(self,name_map = None) -> dict : return self.get_map(name_map).clefs
    def get_name_maps(self) -> list[str] :
        liste_nom = []
        for map in self.maps.values() :
            liste_nom.append(map.name)
        return liste_nom
    def get_sound(self, nom_map : str = None) -> pygame.mixer.Sound : return self.get_stockage().musiques[self.get_map(nom_map).musique]
    def get_stockage(self) -> Stockage : return self.stockage_valeur
    def get_affichagation(self)-> bool :
        for d in list(self.get_Dialogues().keys()) :
            if self.get_Dialogue(d).affichagation : return True 
        else : return False


    def tp_joueur(self, point_de_tp,debut = False)  :
        """ teléporte le joueur a un endroit donner ( poin de tp)"""
        if point_de_tp == list[int] :
            point = point_de_tp
            self.player.position = pygame.Rect(point[0], point[1],self.player.rect.width,self.player.rect.height)
        else :
            point = self.get_object(point_de_tp)
            self.player.position = pygame.Rect(point.x, point.y,self.player.rect.width,self.player.rect.height)
    


    
    def chect_collison(self,touches) : 
        """fonction qui verifie tout les collitsion : dialogue,portail, porte ect"""
        self.chec_colision_mur(self.player.deplacement)
        # ---------- portail ---------- #
        for portail in self.get_map().portails :
            if portail.monde_origine == self.curent_map :
                poin = self.get_object(portail.poin_origine)
                rect = pygame.Rect(poin.x,poin.y,poin.width,poin.height)

                if self.player.position_pour_les_colision.colliderect(rect) and not portail.interact :
                    copy_portail = portail
                    if copy_portail.monde_arriver != self.curent_map :
                        self.changer_musique(copy_portail.monde_arriver)
                    self.curent_map = portail.monde_arriver
                    if portail.poin_de_sortie == "clef_enigme_portail" :
                        self.get_map("futur").clefs["portail"] = True
                    self.tp_joueur(copy_portail.poin_de_sortie)
                    
                elif self.player.position_pour_les_colision.colliderect(rect) and portail.interact :
                    if touches[pygame.K_e] :
                        copy_portail = portail
                        if copy_portail.monde_arriver != self.curent_map :
                            self.changer_musique(copy_portail.monde_arriver)
                        self.curent_map = portail.monde_arriver
                        if portail.poin_de_sortie == "sortie horloge_labyrhinte" :
                            self.get_map("Manoir").clefs["horloge"] = True
                        
                        self.tp_joueur(copy_portail.poin_de_sortie)
                        
                

        # ----------- enigme ------------ #
        for enigme in self.get_map().nom_enigme :
            enigme = self.get_enigme(enigme)
            if enigme.monde == self.curent_map :
                detect = enigme.zone_de_detection
                rect = pygame.Rect(detect.x,detect.y,detect.width,detect.height)
                if self.player.position_pour_les_colision.colliderect(rect) :
                    if touches[pygame.K_e] :
                        copy_enigme = enigme
                        self.curent_map = enigme.monde_de_enigme
                        self.tp_joueur(copy_enigme.spawn)
        


        # ---------- dialogue ---------- #
        for name in self.get_Dialogues().keys() :
            if not self.recherche(name,self.get_portes().keys()) :
                dialogue = self.get_Dialogue(name)
                if dialogue.inte.doit_afficher :

                    list_detect = dialogue.inte.zone_de_detection
                    for detect in list_detect :
                        rect = pygame.Rect(detect.x,detect.y,detect.width,detect.height)
                        
                        if self.player.position_pour_les_colision.colliderect(rect) : 
                            
                            if dialogue.inte.cinematique :
                                if self.stockage_valeur.preimer_pass_ciné :
                                    self.curent_dialogue = dialogue.nom
                                    dialogue.affichagation = True
                                    self.stockage_valeur.preimer_pass_ciné = False
                            else :
                                if touches[pygame.K_e] :
                                    self.curent_dialogue = dialogue.nom
                                    dialogue.affichagation = True
                        else : self.stockage_valeur.preimer_pass_ciné = True
                                    
        



    def update_vitesse(self) :
        """ met a jour la vitersse du jour en fonction du type de curent_map"""
        if self.get_map().type == "exterieur" :
            self.player.vitesse = 2
        elif self.get_map().type == "interieur" :
            self.player.vitesse = 3
            
        elif self.get_map().type == "enigme_inquietant" :
            self.player.vitesse = 4
        elif self.get_map().type == "test" :
            self.player.vitesse = 6
    
    def changer_musique(self,map_musique,debut = False) :
        """ change la musique en la definisant sur celle de la map mis dans map_musique"""
        if debut :
            self.get_sound().play(9000,0,5000)
            self.get_stockage().volume_musique = 0.25
        else :

            if self.get_sound() != None and self.get_sound() != self.get_sound(map_musique) :
                self.get_sound().stop()
                self.get_sound(map_musique).play(9000,0,5000)
                self.get_stockage().volume_musique = 0.25
            

    
    
    def verifier_enigme(self,reponse_entrer : str) :
        """verifie si la reponse_entrer est la bonne """
        if self.get_inte().reponse == reponse_entrer :
            if self.get_Dialogue().nom == "chimie_" :
                self.get_map("futur").clefs["chimie_"] = True
            if self.get_Dialogue().nom == "goblet_" :
                self.get_map("futur").clefs["goblet"] = True
            else :
                self.get_clefs()[self.get_Dialogue().nom] = True
            self.stockage =  self.get_inte().texts[len(self.get_inte().texts)-1]
            self.get_inte().texts[len(self.get_inte().texts)-1] = "bonne réponse voici la clef"
            self.premier_passage_dialogue = True
        
        
        
        
        if self.premier_passage_dialogue :
            if not self.get_tiping() :
                self.premier_passage_dialogue = False
                self.get_inte.texts[len(self.get_inte().texts)-1] = self.stockage
        self.stockage_valeur.chec_reponse = False
        self.curent_tiping = False

        return True

    def dessier_la_carte(self, frame):
        """ afficher le group pyscroll de la map"""
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)
        
        
        if self.get_map().type == "enigme_inquietant" :
            self.dessier_element_mouvant_screen()
        self.afficher_elements_fixe_map_mouvant(frame)
        self.chec_info()

    


    
    def dessier_element_mouvant_screen(self):
        for element in self.get_element_mouvant_screen() :
            element.afficher_sprite()


    def update(self,touche,touches_une_fois_e):
        """on update tous ce qui est sur la map"""
        self.get_group().update()
        self.update_porte(touches_une_fois_e)
        self.chect_collison(touche)
        self.update_dialogue()
        self.update_vitesse()
        
        
    
    def update_dialogue(self) :
        """update les clefs"""
        for k in self.get_clefs().keys():
            if k != "horloge" : #rajouter pour les autres énigmes
                if not self.recherche(k,self.get_name_maps()) and not self.recherche(k,self.clefs_sans_dialogue) and self.recherche(k,self.get_Dialogues().keys()) :
                    if self.get_clefs()[k] :
                        self.get_inte(k).texts = ["Bravo !"]


    def recherche(self,k : str ,liste : list[str]) -> bool :
        """retrurn True si la list liste contien k"""
        for ka in liste :
            if ka == k :
                return True
        return False

        

    def collide(self,rects : list[pygame.Rect] , rect : pygame.Rect) -> list[pygame.Rect]:
        """
        Cette fonction sert à lister les rectangles qui touche la hitbox du joueur
        """
        collided = []

        for collider in rects:
            if collider.colliderect(rect):
                collided.append(collider)
        
        return collided
    
    def chec_colision_mur(self,mouvement) :
        """
    Résolution des collisions
    Nous séparons le mouvement x et y , car cela peut engendrer des problemes
    """
    
        rect = self.player.position_pour_les_colision.copy()
        movement = mouvement
        
        rect.x += movement[0]
        colliders = self.collide(self.get_murs() , rect)

        for name in self.get_portes().keys() :
            if not self.get_porte(name).etat :
                for porte_rect in self.collide(self.porte_rect , rect) :
                    colliders.append(porte_rect)


        for collider in colliders:
            if(movement[0] < 0):
                rect.left = collider.right
            elif(movement[0] > 0):
                rect.right = collider.left
        
        rect.y += movement[1]
        colliders = self.collide(self.get_murs() , rect)
        for name in self.get_portes().keys() :
            if not self.get_porte(name).etat :
                for porte_rects in self.collide(self.porte_rect , rect) :
                    colliders.append(porte_rects)

        for collider in colliders:
            if(movement[1] < 0):
                rect.top = collider.bottom
            elif(movement[1] > 0):
                rect.bottom = collider.top
        
        self.player.position = pygame.Rect(rect.x, rect.y,rect.width,rect.height)
    
    def afficher_elements_fixe_map_mouvant(self,frame):
        """affiche les élémens qui sont senser etre sur la map.
        """

        for nom_enigme in self.get_map().nom_enigme :
            nombre_de_sprite = self.get_sprite_nombre_enigme(nom_enigme)
            self.suivant(frame, nombre_de_sprite, nom_enigme)

            self.get_cara_sprite_enigme(nom_enigme).update()
            
            
    
    def suivant(self, frame, nombre_de_sprite, nom) :
        """ met le sprite suivant avec get_cara_sprite_enigme() """
        self.frame = frame
        
        if frame == 0 or frame == 8 or frame == 17 or frame == 26 or frame == 34 or frame == 43 or frame == 51 :
            if self.sprite_enigme_descente :
                self.get_cara_sprite_enigme(nom).sprite_actuel -= 1
            else : 
                self.get_cara_sprite_enigme(nom).sprite_actuel += 1
            if self.get_cara_sprite_enigme(nom).sprite_actuel >= nombre_de_sprite - 1 :
                self.sprite_enigme_descente = True
            if self.get_cara_sprite_enigme(nom).sprite_actuel <= 0 :
                self.sprite_enigme_descente = False

    
    def chec_info(self) :
        """ et a jour et chec les collisison pour afficher les information en bas a gauche"""
        for i in self.info :
            if self.get_rect_info(i) != [] :
                for rect in self.get_rect_info(i) :
                    if self.player.position_pour_les_colision.colliderect(rect) :
                        self.infos_manoir[i].afficher_information(self.get_stockage().curent_tiping,self.get_stockage().dialogue_afficher)
    

    def update_porte(self,touches_une_fois_e) :
        """met a jour les portes"""
        self.porte_rect = []
        for name in self.get_portes().keys() :
            chec = 0
            for clef in self.get_porte(name).condition :
                if self.get_clefs()[clef] :
                    chec +=1
            if touches_une_fois_e :

                if self.player.position_pour_les_colision.colliderect(self.get_porte(name).rect_dever) :
                    if chec == len(self.get_porte(name).condition) :
                        if self.get_porte(name).etat :
                            self.get_porte(name).etat = False
                        else :
                            self.get_porte(name).etat = True
                            
                        
                    else :
                        self.get_Dialogue(name).affichagation = True
                        self.curent_dialogue = name

            if self.get_porte(name).etat : 
                self.get_porte(name).sprites.sprite_actuel = 0
                self.get_porte(name).sprite_ombre.sprite_actuel = 0
            else : 
                self.get_porte(name).sprites.sprite_actuel = 1
                self.get_porte(name).sprite_ombre.sprite_actuel = 1
            self.get_porte(name).sprites.update()
            self.get_porte(name).sprite_ombre.update()

            if not self.get_porte(name).etat :
                self.porte_rect.append(self.get_porte(name).rect)
        self.passer_devant()
        self.chec_enigme_clefs()



    def passer_devant(self) :
        """regle le layer des information de la map """
        for i in range(15) :
            if i != 7 : 
                for sprite in self.get_group().get_sprites_from_layer(i) :

                    if not sprite.pas_bouger :
                        if self.player.position_pour_les_colision.bottom < sprite.rect.bottom - sprite.distance_bottom  :
                            self.get_group().change_layer(sprite,10)
                        elif self.player.position_pour_les_colision.bottom >= sprite.rect.bottom - sprite.distance_bottom :
                            self.get_group().change_layer(sprite,6)


    def chec_enigme_clefs(self) :
        """voie si les enigmes sont réaliser et donc attribuer les bonne clefs"""
        for name_map in self.maps.keys() :
            chec = 0
            for clef in self.get_clefs(name_map).values() :
                if clef :
                    chec += 1
            if chec == len(self.get_clefs(name_map))- 1 and chec != 0 :
                self.get_clefs(name_map)[name_map] = True
            else :
                self.get_clefs(name_map)[name_map] = False

        self.update_clefs_globale()
        if not self.premier_passage_Globale :
            self.chec_clef_tableaux()
            self.chec_clef_tableaux()
            
    
    def update_clefs_globale(self):
        """met a jour l'attibut self.clefs"""
        for name_map in self.maps.keys() :
            
            for K in self.get_map(name_map).clefs.keys() :
                V = self.get_map(name_map).clefs[K]
                self.clefs[K] = V

    
    def chec_clef_tableaux(self) :
        """regarde si self.clefs["tableau"] : et met la clef du futur ecorrespondante a True """
        if self.clefs["tableau"] :
            self.get_map("futur").clefs["tableau_enigme"] = True

    def chec_clef_goblet(self) :
        if self.clefs["goblet_"] :
            self.get_map("futur").clefs["goblet"] = True
