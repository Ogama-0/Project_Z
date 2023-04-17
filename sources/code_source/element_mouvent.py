import pygame

class sprite_mouvent_screen() :
    def __init__(self, nom : str, nombre_de_sprite : int , screen : pygame.display , position : list[int], frame_decalage : int):
        """ hyp créé un object pour géré plus facilement  l'affichage sur le screen (non sur la map) d'élément mouvants """
        self.nom = nom
        self.curent_image = 0
        self.path = f"sources/sprite/autre/autre/{nom}{self.curent_image}.png"
        self.screen = screen
        self.image = pygame.image.load(self.path)
        self.frame_decalage = frame_decalage
        self.position = position
        self.nombre_de_sprite = nombre_de_sprite
        self.descente = False
        self.frame = 0 
        self.images = []
        for i in range (nombre_de_sprite) :
            self.path = f"sources/sprite/autre/autre/{self.nom}{i}.png"
            self.image = pygame.image.load(self.path)
            self.images.append(self.image)
        
    def image_suivante(self) :
        self.frame +=1
        if self.frame/self.frame_decalage ==  self.frame//self.frame_decalage :

            if self.curent_image >= self.nombre_de_sprite -1 :
                self.descente = True
            if self.curent_image <= 0 :
                self.descente = False

            if self.nombre_de_sprite > self.curent_image and self.descente :
                self.curent_image -= 1
            elif self.nombre_de_sprite > self.curent_image and self.descente == False :
                self.curent_image +=1
    
        if self.frame > 1000000 :
            self.frame = 0

        self.image = self.images[self.curent_image]

        

    def afficher(self):
        self.screen.blit(self.image,self.position)
    
    def afficher_sprite(self) : 
        self.afficher()
        self.image_suivante()