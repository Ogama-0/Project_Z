import pygame
class Player(pygame.sprite.Sprite) :

    def __init__(self, x ,y):
        super().__init__()
        #self.feuille_perso = pygame.image.load('image de tout les sprite')
        #self.image = self.get_image(0,0) #Image avec la feuille de perso
        self.image = pygame.image.load('sources/sprite/sprite nanit/sprite nanit face/nanit_face_yeux_ouverts.png').convert_alpha() #Image sans la feuille de perso
        self.deplacement = [0,0] #pour géré le deplacement (velocité*vitesse)
        self.position = [x,y]#position actuelle du joueurs
        self.sprint = 0
        self.rect = self.image.get_rect(x=self.position[0] , y=self.position[1] )# position et hitbox qui est get de l'image par pygame et que on associe a la position de notre personnage
        
        self.vitesse = 2 #vitesse du perso (2 c'est random t'a capter)
        
        self.layer = 7
        
        
        self.velocite =[0,0] #la velocyté c'est de cb1 le person vas se deplacer en [x,y] en 1 frame(multiplier a self.vitesse)
        # -------------- clefs ----------- #


        
        # ------------------- Collision ---------------------------#

        self.position_pour_les_colision = pygame.Rect(0,0,  self.rect.width*0.70, 15)
        self.old_position = self.position.copy()
        

        self.move_back_var = False
        

        

        # ------------------- Graphiquement ------------------------#
        self.animation = 0
        self.animation_yeux = 0
        self.etat_regard_yeux_nanit = { 'etat_regard' : 0 }#dictionnaire sur l'etat de nanit en fonction de la ou le joueur vas
        # -------------------IMAGE NANIT --------------------------#
        self.image_droite_yeux_fermer = pygame.image.load("sources/sprite/sprite nanit/sprite nanit droite/nanit_droite_yeux_fermer.png").convert_alpha()
        self.image_droite_yeux_ouvert = pygame.image.load("sources/sprite/sprite nanit/sprite nanit droite/nanit_droite_yeux_ouver.png").convert_alpha()
        self.image_gauche_yeux_fermer = pygame.image.load("sources/sprite/sprite nanit/sprite nanit gauche/nanit_gauche_yeux_fermer.png").convert_alpha()
        self.image_gauche_yeux_ouvert = pygame.image.load("sources/sprite/sprite nanit/sprite nanit gauche/nanit_gauche_yeux_ouver.png").convert_alpha()
        self.image_face_yeux_fermer = pygame.image.load("sources/sprite/sprite nanit/sprite nanit face/nanit_face_yeux_fermé.png").convert_alpha()
        self.image_face_yeux_ouvert = pygame.image.load("sources/sprite/sprite nanit/sprite nanit face/nanit_face_yeux_ouverts.png").convert_alpha()
        self.image_dos = pygame.image.load("sources/sprite/sprite nanit/sprite nanit dos/nanit_dos_base.png").convert_alpha()
        self.image_dos_gauche = pygame.image.load("sources/sprite/sprite nanit/sprite nanit dos/nanit_dos_gauche.png").convert_alpha()
        self.image_dos_droite = pygame.image.load("sources/sprite/sprite nanit/sprite nanit dos/nanit_dos_droite.png").convert_alpha()
        # ------------------- debugage ---------------------------#
        self.test_1_colision = 0
        self.test_image = pygame.image.load("sources/sprite/sprite nanit/sprite nanit dos/nanit_dos_droite.png").convert_alpha()



    

    #--------------- update  ---------------#
    
    def update(self) :
        self.rect.midbottom = self.position.midbottom
        self.position_pour_les_colision.midbottom = self.position.midbottom

    #---------------------------- Animation ---------------------------#
    
    def Animation(self,a) :
        """gere toutes les animation du perso"""


        self.animbouger()
        if a == 2 :
            self.animation_yeuxfonc()
            #self.Animation_actif()
        


    def animbouger(self) :
        if self.etat_regard_yeux_nanit['etat_regard'] == 4 : #nanit vas en bas
            self.image = self.image_face_yeux_ouvert
        if self.etat_regard_yeux_nanit['etat_regard'] == 1 : #nanit vas a gauche
            self.image = self.image_gauche_yeux_ouvert
        if self.etat_regard_yeux_nanit['etat_regard'] == 2 : #nanit vas a droite
            self.image = self.image_droite_yeux_ouvert
        if self.etat_regard_yeux_nanit['etat_regard'] == 3 : #nanit vas en haut
            self.image = self.image_dos
        if self.etat_regard_yeux_nanit['etat_regard'] == 5 : #nanit vas en haut a droite
            self.image = self.image_dos_droite
        if self.etat_regard_yeux_nanit['etat_regard'] == 6 : #nanit vas en haut a droite
            self.image = self.image_dos_gauche

    def animation_yeuxfonc(self) :
        self.animation_yeux += 1
        if self.animation_yeux >= 301 :
            self.animation_yeux = 0
        if self.animation_yeux >= 250 :
            if self.etat_regard_yeux_nanit['etat_regard'] == 4 : #nanit vas en bas
              self.image = self.image_face_yeux_fermer
            if self.etat_regard_yeux_nanit['etat_regard'] == 1 : #nanit vas a gauche
               self.image = self.image_gauche_yeux_fermer
            if self.etat_regard_yeux_nanit['etat_regard'] == 2 : #nanit vas a droite
               self.image = self.image_droite_yeux_fermer
            

    def Animation_actif(self):
        self.animation += 1
        if self.animation >= 40 :
            self.animation = 0
        if self.animation == 20 :
            self.position[1] += 1 
        if self.animation == 39 :
            self.position[1] -= 1