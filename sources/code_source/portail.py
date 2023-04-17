import pygame
from dataclasses import dataclass
from sources.code_source.enigme_code import enigme_sprite,interact_ecrit,dialogue_enigme_setup
from sources.code_source.dialogue import Dialogue

@dataclass
class Stk_porte :
    nom : str
    etat : bool
    condi : list[int]
    dia_fermer : list[str]
    layer : int = 8
    distance_bottom : int = 0
    pas_bouger : bool = False

@dataclass
class Portail :
    monde_origine : str
    poin_origine : str
    monde_arriver : str
    poin_de_sortie : str
    interact : bool

@dataclass
class stk_dialogue :
    name : str
    textes : list[str]
    taille_background : tuple[int]
    position : tuple[int]
    type : str
    reponse : str = None
    tiping : bool = False
    position_txt : tuple[int] = None
    couleur : tuple[int] = (0,0,0)
    cinematique : bool = False
    position_tiping :tuple[int] = ()


@dataclass
class Porte() :
    nom : str
    etat : bool
    condition : list[str]
    sprites : enigme_sprite
    sprite_ombre : enigme_sprite
    rect : pygame.rect.Rect
    rect_ombre : pygame.rect.Rect
    rect_dever : pygame.rect.Rect
    dialogue : Dialogue


class Setup_Porte :
    def __init__(self, tmx_data,group,stk_porte : Stk_porte) :        
        sprite_ouvert_ombre = pygame.image.load(f"sources/map/porte/{stk_porte.nom}_ouvert_ombre.png")
        sprite_fermer_ombre = pygame.image.load(f"sources/map/porte/{stk_porte.nom}_fermer_ombre.png")
        sprite_ouvert = pygame.image.load(f"sources/map/porte/{stk_porte.nom}_ouvert.png")
        sprite_fermer = pygame.image.load(f"sources/map/porte/{stk_porte.nom}_fermer.png")
        sprites = [sprite_ouvert,sprite_fermer]
        sprites_ombre = [sprite_ouvert_ombre , sprite_fermer_ombre]
        for obj in tmx_data.objects :
           
            if obj.name == stk_porte.nom :
                rect_obj = pygame.rect.Rect(obj.x,obj.y,obj.width,obj.height)
                rect = rect_obj
                rect_ombre = pygame.rect.Rect(obj.x,obj.y - sprite_fermer.get_height(),obj.width,obj.height)
        
        for obj in tmx_data.objects :
            if obj.name == stk_porte.nom + "_zonne_deverouillage" :
                rect_dever = pygame.rect.Rect(obj.x ,obj.y ,obj.width ,obj.height)
        
        sprite_ombre = enigme_sprite(rect_ombre, sprites_ombre, 0, group, stk_porte.layer,stk_porte.distance_bottom,True)
        
        dialogueu = stk_dialogue(stk_porte.nom,stk_porte.dia_fermer,(700,100),(200,600),"boite_dialogues")

        dialogue = dialogue_enigme_setup(tmx_data,dialogueu)
        dialogues = dialogue.dialogues

        sprite_porte = enigme_sprite(rect, sprites, 0, group, stk_porte.layer, stk_porte.distance_bottom,stk_porte.pas_bouger)
        
        porte = Porte(stk_porte.nom, stk_porte.etat, stk_porte.condi, sprite_porte, sprite_ombre, rect, rect_ombre, rect_dever, dialogues)
        
        self.porte = porte