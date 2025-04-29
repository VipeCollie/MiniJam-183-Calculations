import pygame
import sys
import random
import os

# Initialisation
pygame.init()



# 1.  chemin du dossier du script (main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. chemin complet vers  police
font_path = os.path.join(current_dir, "assets", "fonts", "PressStart2P-Regular.ttf")

# 3. Charger la police
try:
    my_font = pygame.font.Font(font_path, 15)
except FileNotFoundError:
    print("Erreur : fichier de police non trouvé :", font_path)
    pygame.quit()
    exit()


police = my_font

# Son de tir
son_laser = pygame.mixer.Sound(os.path.join(current_dir, "assets", "sounds", "laser.wav"))

# Fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Math Blaster - Équations en ligne")

# Couleurs
NOIR = (0, 0, 0)
BLEU = (0, 150, 255)
ROUGE = (255, 50, 50)
BLANC = (255, 255, 255)

# Joueur
joueur_largeur = 50
joueur_hauteur = 30
joueur_x = largeur // 2 - joueur_largeur // 2
joueur_y = hauteur - 60
joueur_vitesse = 7

# Lasers
lasers = []
laser_vitesse = 10
laser_largeur = 4
laser_hauteur = 15

# Équations
equations = []
equation_vitesse = 1
frequence_spawn = 190
ligne_y = 100  # Hauteur des équations

def generer_equation():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    op = random.choice(["+", "-"])
    result = a + b if op == "+" else a - b
    faux = random.choice([True, False])
    if faux:
        result += random.choice([-2, -1, 1, 2])
    texte = f"{a} {op} {b} = {result}"
    return {"x": 0, "y": ligne_y, "texte": texte, "faux": faux}

# Horloge
clock = pygame.time.Clock()
en_cours = True
frame_count = 0
score = 0
bravo_timer = 0
oops_timer = 0
game_over = False
victoire = False

def afficher_ecran_depart():
    attente = True
    while attente:
        fenetre.fill(NOIR)
        titre = police.render("Welcome in  Blast for Maths", True, BLANC)
        explication = police.render( "Destroy bad results to mark points.", True, BLANC)
        consigne = police.render("Touch a good result and you loose a point", True, ROUGE)
        consigne2 = police.render("Flèche gauche et droite pour se déplacer", True, BLANC)
        consigne3 = police.render("Touche Espace pour tirer", True, BLANC)
        bouton = pygame.Rect(largeur // 2 - 60, hauteur // 2 + 40, 120, 40)
        pygame.draw.rect(fenetre, BLEU, bouton)
        texte_bouton = police.render("Begin", True, NOIR)
        fenetre.blit(titre, (largeur // 1.9 - 180, 100))
        fenetre.blit(explication, (largeur // 2.4 - 180, 150))
        fenetre.blit(consigne, (largeur // 2.6 - 180, 180))
        fenetre.blit(consigne2, (largeur // 2.7 - 180, 210))
        fenetre.blit(consigne3, (largeur // 2 - 180, 230))
        fenetre.blit(texte_bouton, (largeur // 2 - 30, hauteur // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and bouton.collidepoint(event.pos):
                attente = False

# Afficher l'écran de départ avant de commencer la boucle principale
afficher_ecran_depart()

while en_cours:
    if game_over or victoire:
        fenetre.fill(NOIR)
        if game_over:
            message = police.render("Nooo... Game Over", True, ROUGE)
        else:
            message = police.render("Victory! You're the Best", True, BLANC)
        fenetre.blit(message, (largeur // 2 - 60, hauteur // 2))
        pygame.display.flip()
        pygame.time.wait(6000)
        break

    clock.tick(60)
    fenetre.fill(NOIR)

    # Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

    # Contrôles
    touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT] and joueur_x > 0:
        joueur_x -= joueur_vitesse
    if touches[pygame.K_RIGHT] and joueur_x < largeur - joueur_largeur:
        joueur_x += joueur_vitesse
    if touches[pygame.K_SPACE]:
        lasers.append(pygame.Rect(joueur_x + joueur_largeur // 2 - laser_largeur // 2,
                                  joueur_y, laser_largeur, laser_hauteur))
        son_laser.play()

    # Déplacement lasers
    for laser in lasers:
        laser.y -= laser_vitesse
    lasers = [l for l in lasers if l.y > 0]

    # Apparition des équations
    frame_count += 1
    if frame_count % frequence_spawn == 0:
        equations.append(generer_equation())

    # Déplacement horizontal des équations
    for eq in equations:
        eq["x"] += equation_vitesse

    # Collision
    new_equations = []
    lasers_a_supprimer = []

    for eq in equations:
        eq_rect = pygame.Rect(eq["x"], eq["y"], 120, 30)
        touche = False
        for laser in lasers:
            if eq_rect.colliderect(laser):
                if eq["faux"]:
                    print("Nice shot !")
                    score += 1
                    if score >= 10:
                        victoire = True
                    bravo_timer = 60  # Affiche Bravo pendant 1 seconde (60 frames)
                else:
                    print("Oops...")
                    bravo_timer = 0  # Ne pas afficher "Bravo !" en cas d'erreur
                    score -= 1
                    if score <= -3:
                        game_over = True
                    oops_timer = 60  # Affiche "Oops !" pendant 1 seconde
                lasers_a_supprimer.append(laser)
                touche = True
                break
        if not touche:
            new_equations.append(eq)

    lasers = [l for l in lasers if l not in lasers_a_supprimer]
    equations = new_equations

    # Affichage joueur
    pygame.draw.rect(fenetre, BLEU, (joueur_x, joueur_y, joueur_largeur, joueur_hauteur))
    pygame.draw.polygon(fenetre, ROUGE, [
        (joueur_x + joueur_largeur // 2, joueur_y - 15),
        (joueur_x + joueur_largeur - 10, joueur_y),
        (joueur_x + 10, joueur_y)
    ])

    # Affichage lasers
    for laser in lasers:
        pygame.draw.rect(fenetre, ROUGE, laser)

    # Affichage équations
    for eq in equations:
        texte_surface = police.render(eq["texte"], True, BLANC)
        fenetre.blit(texte_surface, (eq["x"], eq["y"]))

    # Affichage du score
    score_surface = police.render(f"Score : {score}", True, BLANC)
    fenetre.blit(score_surface, (10, 10))

    # Affichage de "Bravo" temporaire
    if bravo_timer > 0:
        bravo_surface = police.render("Bravo !", True, BLANC)
        fenetre.blit(bravo_surface, (largeur // 2 - 50, 40))
        bravo_timer -= 1

    # Affichage de "Oops" temporaire
    if oops_timer > 0:
        oops_surface = police.render("Oops !", True, BLANC)
        fenetre.blit(oops_surface, (largeur // 2 - 50, 70))
        oops_timer -= 1

    pygame.display.flip()

pygame.quit()
sys.exit()