import pygame 
class Bouton  :
    def __init__(self,screen : pygame.Surface , sprites : pygame.surface.Surface ,position :tuple[int],nom : str,cliquable : bool = False) :
        if cliquable :
            self.image_cliqued = [pygame.image.load(f"sources/sprite/autre/menu/{nom}_cliqued_bouton.png"),pygame.image.load(f"sources/sprite/autre/menu/{nom}_cliqued_bouton_appuyer.png")]
            self.cliquable = True
        else : self.cliquable = False
        self.current_sprite = 0
        sprite = sprites[self.current_sprite]
        hauteur = sprite.get_width()
        largeur = sprite.get_height()
        self.sprites = []
        self.nom = nom
        self.sprites = sprites
            
        self.rect = pygame.Surface.get_rect(self.sprites[self.current_sprite])
        self.rect.topleft = position
        self.cliqued = False
        self.screen = screen
        self.premier_passage = False
        self.premier_passage_souris = True
    
    def update(self):
        self.premier_passage = True
    
    def afficher(self,cliqued) :
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) :
            if cliqued :
                
                if self.premier_passage : 
                    self.premier_passage = False
                    if self.cliquable :
                        if self.cliqued : self.cliqued = False
                        else : self.cliqued = True
                    self.premier_passage = False
                    return True
                
            else :
                self.current_sprite = 1
                self.premier_passage = True
        else :
            self.current_sprite = 0
        if not self.cliqued :
            image = self.sprites[self.current_sprite]
        else : image = self.image_cliqued[self.current_sprite]
        self.screen.blit(image,(self.rect.x,self.rect.y))
    

        


class Menu :
    def __init__(self,screen,boutons,background) :
        self.screen = screen
        self.boutons = {}
        for stk_bouton in boutons :
            images_bouton = [pygame.image.load(f"sources/sprite/autre/menu/{stk_bouton.nom}_bouton.png"),pygame.image.load(f"sources/sprite/autre/menu/{stk_bouton.nom}_bouton_appuyer.png")]
            self.boutons[stk_bouton.nom] = Bouton(screen,images_bouton,stk_bouton.position,stk_bouton.nom,stk_bouton.cliquable)

        self.curent_bck = 0
        self.bckgrnds = background
        self.decsante = False
        self.frame = 0
    
    def afficher(self,cliqued : bool) :
        "afficher le menue "
        self.afficher_bckgrnd()
        for name in self.boutons.keys() :
            if self.boutons[name].afficher(cliqued) :
                return name
        
        self.suivant_bckgrnd()
    
    def afficher_bckgrnd(self) :
        self.screen.blit(self.bckgrnds[self.curent_bck],(0,0))
        
    
    def suivant_bckgrnd(self) :
        "pass au background pour faire une animation"
        self.frame +=1
        if self.frame/15 == self.frame //15 :
            if self.curent_bck == len(self.bckgrnds)-1 :
                self.decsante = True
            elif self.curent_bck <= 0 :
                self.decsante = False
            
            if self.decsante :
                self.curent_bck -= 1
            else :
                self.curent_bck += 1

class Degrader :
    def __init__(self, screen : pygame.surface.Surface) :
        self.sprite = []
        self.screen = screen 
        self.curent_sprite = 0
        self.dessante = False
        self.curent_degrader = False
        self.time = 0
        self.contre_curent_degrader = False
        for i in range(1,22) :
            self.sprite.append(pygame.image.load(f"sources/sprite/autre/degrader/degrader_{i}.png"))
        self.contre_curent_sprite = len(self.sprite)-1
        
        
    def afficher(self) :
        if self.curent_degrader :
            self.screen.blit(self.sprite[self.curent_sprite],(0,0))
            self.suivant()
        
    def afficher_contre(self) :
        if self.contre_curent_degrader :
            self.screen.blit(self.sprite[self.contre_curent_sprite],(0,0))
            self.contre_suivant()


        
    def contre_suivant(self) :
        self.time +=1
        if self.time//2 == self.time/2 : 
            self.contre_curent_sprite -= 1
            if self.contre_curent_sprite == -1 :
                self.contre_curent_degrader = False
                self.contre_curent_sprite = len(self.sprite)-1

    def suivant(self) :
        self.time +=1

        if self.time//2 == self.time/2 : 
            self.curent_sprite += 1
            if self.curent_sprite > len(self.sprite)-1 :
                self.curent_degrader = False
                self.curent_sprite = 0
