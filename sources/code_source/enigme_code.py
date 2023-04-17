from dataclasses import dataclass
import pygame,pytmx

class enigme_setup :

    def __init__(self, tmx_data, name_enigme, name_map, nombre_de_sprite, group, curent_sprite_enigme = 0 ):

        self.enigmes = {}
        sprite_enigme = []
        k = 0
        for nom_enigme in name_enigme :
            
            self.enigme_detect = []
            for enigm in tmx_data.objects :
                if enigm.name == 'zonne de detection '+ nom_enigme :
                    enigme_detect = pygame.Rect(enigm.x,enigm.y,enigm.width,enigm.height)
                if enigm.name == 'zonne de colision '+ nom_enigme :
                    rect_sprite = pygame.rect.Rect(enigm.x,enigm.y,enigm.width,enigm.height)

            

            for i in range(1,nombre_de_sprite[k]+1) :
                
                chemain_enigme = f'sources/sprite/sprint_enigme/{nom_enigme}/{nom_enigme}{i}.jpg'
                sprite = pygame.image.load(chemain_enigme)
                if nom_enigme == 'horloge' : 
                    sprite = pygame.transform.scale(sprite,(34,128)) #ici on redimationise l'image enigme par enigme pour que se soit plus bo
                
                sprite_enigme.append(sprite)
               

            sprite = enigme_sprite(rect_sprite, sprite_enigme, curent_sprite_enigme, group, nom = name_enigme)
            self.enigmes[nom_enigme] = enigme_caracteristique(nom_enigme, name_map, enigme_detect, sprite , "enigme_"+ nom_enigme)
            k=+1


class enigme_sprite():
    
    def __init__(self, rect, sprites , sprite_actuel : int , group, layer : int = 6, distance_bottom = 0,pas_bouger = False, nom = [""]):

        self.nombre_enigme = len(sprites)
        self.sprites = sprites
        self.sprite_actuel = sprite_actuel
        self.sprite = pygame.sprite.Sprite()
        self.sprite.sprite_actuel = sprite_actuel
        self.sprite.rect = rect
        self.sprite.image = sprites[self.sprite_actuel]
        self.sprite.distance_bottom = distance_bottom
        self.sprite.pas_bouger = pas_bouger
        self.rect_image = []
        for image in sprites :
            r = pygame.rect.Rect(self.sprite.rect.x,self.sprite.rect.y,image.get_width(),image.get_height())
            r.midbottom = self.sprite.rect.midbottom
            self.rect_image.append(r)
        self.sprite.layer = layer
        self.delet = 1
        self.frame = 0
        self.D = False
        if nom[0] == "Docteur_Z" :
            self.delet = 1 
            self.D = True
        self.debut = False


        
        group.add(self.sprite)
        
    def update(self):
        if self.D :
            self.update_D()
        else :
            
                
            if len(self.sprites) < self.sprite_actuel :
                self.sprite_actuel += 1
            else : 
                while len(self.sprites)-1 < self.sprite_actuel :
                    self.sprite_actuel -= 1
                self.sprite.rect = self.rect_image[self.sprite_actuel]
        self.sprite.image = self.sprites[self.sprite_actuel]

    def update_D(self) :
        """update du docteur Z (c'est a la rache pk c'est la fin et je n'ai plus le temps)"""
        self.frame += 1
        if  self.frame/60 < self.delet:
            self.sprite_actuel = 1
        else :
            self.sprite_actuel = 0
        if self.frame > 360 :
            self.frame = 0



@dataclass
class enigme_caracteristique : 
    nom : str
    monde : str
    zone_de_detection : pygame.Rect
    sprite_enigme : enigme_sprite
    monde_de_enigme : str
    spawn = 'spawn'

@dataclass
class interact_ecrit :
    position :list[int]
    nom : str
    nom_dialogue : str
    texts : list[str]
    zone_de_detection : pygame.Rect
    background : pygame.Surface
    lettre : bool
    tiping :bool
    reponse : str
    position_text : list[int]
    couleur : tuple[int] = (0,0,0)
    cinematique : bool = False
    recurence : bool = True
    doit_afficher : bool = True
    position_tiping : tuple[int] = ()

class dialogue_enigme_setup :

    def __init__(self, tmx_data : pytmx.TiledMap, dialogue ): 
        """fait tout pour que le dialogue puisse etra afficher"""

        
        zonne_de_detect_dialogue = []
        for obj in tmx_data.objects :
            if obj.name == dialogue.name :
                zonne_de_detect_dialogue.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        if dialogue.name == "lettre" :
            
            lettre = True
            position_txt =  (dialogue.position[0]+35,dialogue.position[1]+28)
        else : 
            lettre = False
        
            if dialogue.position_txt == None :

                position_txt =  (dialogue.position[0]+25,dialogue.position[1]+26)
            else :
                position_txt = dialogue.position_txt

        if dialogue.type == "boite_dialogues" :
            background_dialogue = pygame.image.load("sources/sprite/sprint_enigme/boite_dialogues/enigme_porte_entrer.png").convert_alpha()
            background_dialogue = pygame.transform.scale(background_dialogue,dialogue.taille_background)
            
        else :
            background_dialogue = pygame.image.load(f"sources/sprite/sprint_enigme/{dialogue.type}/enigme_{dialogue.name}.png").convert_alpha()
            background_dialogue = pygame.transform.scale(background_dialogue,dialogue.taille_background)
        self.dialogues = interact_ecrit(dialogue.position,dialogue.name,dialogue.name,dialogue.textes,zonne_de_detect_dialogue , background_dialogue,lettre,dialogue.tiping,dialogue.reponse,position_txt,dialogue.couleur,dialogue.cinematique, not dialogue.cinematique,True,dialogue.position_tiping)
        