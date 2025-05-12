import pygame
import sys
import random

pygame.init()
icon = pygame.image.load("pokeball.png")
pygame.display.set_icon(icon)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# couleurs utiliser
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
PINK = (219, 48, 122)
L_PINK = (255, 182, 193)
pv_RED = (255, 0, 0)
pv_GREEN = (0, 255, 0)
pv_YELLOW = (255, 255, 0)

#classe moule des boutton 
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.Font(None, 32)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, 0, 10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, 10)
        
        text_surface = self.font.render(self.text, True, PINK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
            return True
        else:
            self.current_color = self.color
            return False
            
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

#classe des image de pokemon et nom
class Pokemon:
    def __init__(self, name, image_path, x, y, force=15, type_name="Normal", pv=100):  
        self.name = name
        self.force = force
        self.type_name = type_name
        self.pv = pv
        
        # Essayer de charger l'image (avec gestion des erreurs)
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (120, 120))
        except pygame.error:
            print(f"Impossible de charger l'image: {image_path}")
            
            self.image = pygame.Surface((120, 120))
            self.image.fill((255, 200, 200))  
            
        self.rect = self.image.get_rect(midtop=(x + 60, y))
        
        button_width = 200
        self.button = Button(x + 60 - button_width//2, y + 140, button_width, 40, f"{self.name}", L_PINK, (255, 100, 100))
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.button.draw(screen)
        
    def check_hover(self, mouse_pos):
        return self.button.check_hover(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.button.is_clicked(mouse_pos, mouse_click)

#classe Menu de jeux
class MainMenu:
    def __init__(self):
        self.title = "MENU"
        self.active = True
        self.buttons = [
            Button(300, 200, 200, 50, "Jouer", L_PINK, (255, 100, 100)),
            Button(300, 280, 200, 50, "statistique", L_PINK, (255,100, 100)),
            Button(300, 360, 200, 50, "Quitter", L_PINK, (255, 100, 100))
        ]
        
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        result = None
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.buttons[0].is_clicked(mouse_pos, True):
                    result = "game"
                elif self.buttons[1].is_clicked(mouse_pos, True):
                    result = "settings"
                elif self.buttons[2].is_clicked(mouse_pos, True):
                    result = "quit"
        
        for button in self.buttons:
            button.check_hover(mouse_pos)
            
        return result
    
    def render(self, screen):
        screen.fill(L_PINK)
        
        # ecrire le titre
        font = pygame.font.Font(None, 64)
        title_text = font.render(self.title, True, PINK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, 100))
        screen.blit(title_text, title_rect)
        
        # dessiner le boutton 
        for button in self.buttons:
            button.draw(screen)
    # changer de fenêtre
    def destroy(self):
        self.active = False
        print("Destroying Main Menu")

#classe pour choisire le pokemon
class GameWindow:
    def __init__(self):
        self.title = "Voici les Pokémons disponibles :"
        self.active = True
        self.back_button = Button(20, 20, 120, 40, "Back", L_PINK, (255, 100, 100))
        
        # Calculer l'espacement égal entre les Pokémon
        pokemon_width = 120
        total_pokemon_width = pokemon_width * 3
        spacing = (SCREEN_WIDTH - total_pokemon_width) // 4
        
        pos_x1 = spacing
        pos_x2 = spacing * 2 + pokemon_width
        pos_x3 = spacing * 3 + pokemon_width * 2
        
        # Créer les pokémons 
        self.pokemons = [
            Pokemon("1- Salamèche", "S.png", pos_x1, 250, force=22, type_name="Feu", pv=100), 
            Pokemon("2- Carapuce", "C.png", pos_x2, 250, force=15, type_name="Eau", pv=110),    
            Pokemon("3- Bulbizarre", "B.png", pos_x3, 250, force=18, type_name="Plante", pv=90)   
        ]
        
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        result = None
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.is_clicked(mouse_pos, True):
                    result = "menu"
                # Vérifier si un pokémon est selectionner pour changer de fenêtre 
                for pokemon in self.pokemons:
                    if pokemon.is_clicked(mouse_pos, True):
                        self.selected_pokemon = pokemon
                        result = "combat"
        
        self.back_button.check_hover(mouse_pos)
        for pokemon in self.pokemons:
            pokemon.check_hover(mouse_pos)
        
        return result
    
    def render(self, screen):
        screen.fill(WHITE)  
        
        font = pygame.font.Font(None, 60)
        title_text = font.render(self.title, True, PINK)
        title_rect = title_text.get_rect(midtop=(SCREEN_WIDTH//2, 80))
        screen.blit(title_text, title_rect)
         
        for pokemon in self.pokemons:
            pokemon.draw(screen)
        
        self.back_button.draw(screen)
    
    def destroy(self):
        self.active = False
#classe des statistique
class SettingsWindow:
    def __init__(self):
        self.title = "Statistique"
        self.active = True
        self.back_button = Button(20, 20, 120, 40, "Back", L_PINK, (255, 100, 100))
        self.font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 48)
        
        # Charger les statistiques des Pokémon de fichier
        self.pokemons = self.load_pokemon_stats()
        
    def load_pokemon_stats(self):
        # Fichier pour stocker les statistiques des Pokémon
        try:
            with open('pokemon_stats.txt', 'r') as file:
                pokemons = []
                for line in file:
                    
                    data = line.strip().split(':')
                    pokemon = {
                        "name": data[0],
                        "type": data[1],
                        "force": int(data[2]),
                        "pv": int(data[3]),
                        "victoires": int(data[4])
                    }
                    pokemons.append(pokemon)
                return pokemons
        except FileNotFoundError:
            # Si le fichier n'existe pas, créer un fichier avec les statistiques par défaut
            default_pokemons = [
                {
                    "name": "Salamèche", 
                    "type": "Feu", 
                    "force": 22, 
                    "pv": 100,
                    "victoires": 0
                }, {
                    "name": "Carapuce", 
                    "type": "Eau", 
                    "force": 15, 
                    "pv": 110,
                    "victoires": 0
                }, {
                    "name": "Bulbizarre", 
                    "type": "Plante", 
                    "force": 18, 
                    "pv": 90,
                    "victoires": 0
                }
            ]
            self.save_pokemon_stats(default_pokemons)
            return default_pokemons
        
    def save_pokemon_stats(self, pokemons=None):
        # Si aucun paramètre n'est passé, utiliser self.pokemons
        if pokemons is None:
            pokemons = self.pokemons
        
        # Sauvegarder toutes les statistiques dans le fichier
        with open('pokemon_stats.txt', 'w') as file:
            for pokemon in pokemons:
                # Format : Nom:Type:Force:PV:Victoires
                file.write(f"{pokemon['name']}:{pokemon['type']}:{pokemon['force']}:{pokemon['pv']}:{pokemon['victoires']}\n")
        
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        result = None
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.is_clicked(mouse_pos, True):
                    # Sauvegarder les statistiques avant de quitter
                    self.save_pokemon_stats()
                    result = "menu"
        
        self.back_button.check_hover(mouse_pos)
        return result
    
    def render(self, screen):
        screen.fill(WHITE)
        
        # Afficher le titre
        title_surface = self.title_font.render(self.title, True, PINK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH/2, 80))
        screen.blit(title_surface, title_rect)
        
        pokemon_width = 250  
        total_width = len(self.pokemons) * pokemon_width
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        for i, pokemon in enumerate(self.pokemons):
            
            X_position = start_x + i * pokemon_width
            Y_position = 200  
            
            pokemon_title = self.font.render(pokemon['name'], True, PINK)
            pokemon_title_rect = pokemon_title.get_rect(center=(X_position + pokemon_width//2, Y_position))
            screen.blit(pokemon_title, pokemon_title_rect)
            
            victoires_text = self.font.render(f"Victoires: {pokemon['victoires']}", True, PINK)
            victoires_rect = victoires_text.get_rect(center=(X_position + pokemon_width//2, Y_position + 40))
            screen.blit(victoires_text, victoires_rect)
            
            caracteristiques = [
                f"Type: {pokemon['type']}",
                f"Force: {pokemon['force']}",
                f"PV: {pokemon['pv']}"
            ]
            
            for j, carac in enumerate(caracteristiques):
                carac_surface = self.font.render(carac, True, BLACK)
                carac_rect = carac_surface.get_rect(center=(X_position + pokemon_width//2, Y_position + 100 + j * 40))
                screen.blit(carac_surface, carac_rect)
        
        # Bouton retour
        self.back_button.draw(screen)
    
    def destroy(self):
        self.active = False


# classe du combat pokemon
class combatWindow:
    def __init__(self, dresseur_pokemon):
        self.title = "Combat"
        self.active = True
        self.dresseur_pokemon = dresseur_pokemon
        
        #  liste de tous les pokémons disponibles 
        self.all_pokemons = [
            {"name": "1- Salamèche", "image": "S.png", "force": 22, "type": "Feu", "pv": 100},
            {"name": "2- Carapuce", "image": "C.png", "force": 15, "type": "Eau", "pv": 110},
            {"name": "3- Bulbizarre", "image": "B.png", "force": 18, "type": "Plante", "pv": 90}
        ]
        
        # Filtrer les pokémons non sélectionnés
        self.available_enemies = [p for p in self.all_pokemons if p["name"] != dresseur_pokemon.name]
        
        # Choisir un ennemi aléatoirement
        self.enemy_pokemon_info = random.choice(self.available_enemies)
        
        self.enemy_pokemon = Pokemon(
            self.enemy_pokemon_info["name"], 
            self.enemy_pokemon_info["image"], 
            SCREEN_WIDTH - 200, 
            100,
            force=self.enemy_pokemon_info["force"],
            type_name=self.enemy_pokemon_info["type"],
            pv=self.enemy_pokemon_info["pv"]
        )
        
        #les points de vie 
        self.dresseur_pv = dresseur_pokemon.pv
        self.enemy_pv = self.enemy_pokemon.pv
        self.victory_recorded = False
        #Compteur de soins
        self.heal_count = 0
        
        self.back_button = Button(20, 20, 120, 40, "Back", L_PINK, (255, 100, 100))
        
        #bouton d'attaque
        self.attack_button = Button(SCREEN_WIDTH//2 - 160, 450, 150, 40, "Attaque", L_PINK, (255, 100, 100))
        
        # bouton de soin
        self.heal_button = Button(SCREEN_WIDTH//2 + 10, 450, 150, 40, "Soigner", L_PINK, (255, 100, 100))
    def load_pokemon_stats(self):
        try:
            with open('pokemon_stats.txt', 'r') as file:
                pokemons = []
                for line in file:
                    data = line.strip().split(':')
                    pokemon = {
                        "name": data[0],
                        "type": data[1],
                        "force":int(data[2]),
                        "pv": int(data[3]),
                        "victoires": int(data[4])
                    }
                    pokemons.append(pokemon)
                return pokemons
        except FileNotFoundError:
            return [
                {
                    "name": "1- Salamèche", 
                    "type": "Feu", 
                    "force": 22, 
                    "pv": 100,
                    "victoires": 0
                }, {
                    "name": "2- Carapuce", 
                    "type": "Eau", 
                    "force": 15, 
                    "pv": 110,
                    "victoires": 0
                }, {
                    "name": "3- Bulbizarre", 
                    "type": "Plante", 
                    "force": 18, 
                    "pv": 90,
                    "victoires": 0
                }
            ]
        
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        result = None
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.is_clicked(mouse_pos, True):
                    result = "menu"
                
                # Vérifier si le bouton d'attaque est cliqué
                if self.attack_button.is_clicked(mouse_pos, True):
                    self.process_attack()
                
                # Vérifier si le bouton de soin est cliqué
                if self.heal_button.is_clicked(mouse_pos, True):
                    self.process_heal()
        
        self.back_button.check_hover(mouse_pos)
        self.attack_button.check_hover(mouse_pos)
        
        #Ne pas permettre le hover si le bouton est désactivé
        if self.heal_count < 3:
            self.heal_button.check_hover(mouse_pos)
        
        return result
    
    def process_attack(self):
        # Utiliser la force du Pokémon du dresseur pour l'attaque
        self.enemy_pv = max(0, self.enemy_pv - self.dresseur_pokemon.force)
         # Si l'ennemi n'est pas KO, il contre-attaque avec sa propre force
        if self.enemy_pv > 0:
            self.dresseur_pv = max(0, self.dresseur_pv - self.enemy_pokemon.force)
    
    def process_heal(self):
        # utilisé just 3 soins
        if self.heal_count >= 3:
            return
        
        if self.dresseur_pv > 0:
            self.dresseur_pv = min(100, self.dresseur_pv + 10)
            self.heal_count += 1
            print(f"Votre PV est de {self.dresseur_pv} !")
            
            #Désactiver le bouton après 3 utilisations
            if self.heal_count >= 3:
                self.heal_button.color = GRAY
                self.heal_button.hover_color = GRAY
                self.heal_button.current_color = GRAY
        else:
            print(f"{self.dresseur_pokemon.name} est KO et ne peut pas être soigné !")
    
    def render(self, screen):
        screen.fill(WHITE)

        font = pygame.font.Font(None, 48)
        title_text = font.render(self.title, True, PINK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, 50))
        screen.blit(title_text, title_rect)
        
        screen.blit(self.dresseur_pokemon.image, (100, 150))
        screen.blit(self.enemy_pokemon.image, (SCREEN_WIDTH - 220, 150))
        
        small_font = pygame.font.Font(None, 32)
        dresseur_name = small_font.render(f"{self.dresseur_pokemon.name} (Type: {self.dresseur_pokemon.type_name}, Force: {self.dresseur_pokemon.force})", True, BLACK)
        enemy_name = small_font.render(f"{self.enemy_pokemon.name} (Type: {self.enemy_pokemon.type_name}, Force: {self.enemy_pokemon.force})", True, BLACK)
        
        screen.blit(dresseur_name, (100, 120))
        screen.blit(enemy_name, (SCREEN_WIDTH - 330, 120))  

        # PV du pokemon dresseur
        pygame.draw.rect(screen, GRAY, (100, 270, 100, 20))
        pygame.draw.rect(screen, pv_GREEN, (100, 270, self.dresseur_pv, 20))
        
        # PV de l'ennemi
        pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH - 220, 270, 100, 20))
        pygame.draw.rect(screen, pv_GREEN, (SCREEN_WIDTH - 220, 270, self.enemy_pv, 20))
        
        pv_text_dresseur = small_font.render(f"PV: {self.dresseur_pv}/100", True, BLACK)
        pv_text_enemy = small_font.render(f"PV: {self.enemy_pv}/100", True, BLACK)
        
        screen.blit(pv_text_dresseur, (100, 300))
        screen.blit(pv_text_enemy, (SCREEN_WIDTH - 220, 300))
        
        self.attack_button.draw(screen)
        self.heal_button.draw(screen)
        self.back_button.draw(screen)
        
        # si un des Pokémon est KO
        if self.dresseur_pv == 0 or self.enemy_pv == 0:
            result_text = "Vous avez gagner 😄" if self.enemy_pv == 0 else "Perdu 😵!!"
            result_surface = font.render(result_text, True, PINK)
            result_rect = result_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            
            # un fond transparent
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            #le message de résultat
            screen.blit(result_surface, result_rect)
            
            # Enregistrer la victoire si le joueur a gagné 
            if self.enemy_pv == 0 and not self.victory_recorded:
                self.record_victory()
    
    def record_victory(self):
    
        pokemons = self.load_pokemon_stats()
        
        #incrémenter les victoires du Pokémon
        for pokemon in pokemons:
            if pokemon['name'] == self.dresseur_pokemon.name:
                pokemon['victoires'] += 1
                break
      
        # Sauvegarder les statistiques dans le fichier
        with open('pokemon_stats.txt', 'w') as file:
            for pokemon in pokemons:
                file.write(f"{pokemon['name']}:{pokemon['type']}:{pokemon['force']}:{pokemon['pv']}:{pokemon['victoires']}\n")
        
        self.victory_recorded = True
    
    def destroy(self):
        self.active = False
        print("Destroying Combat Window")


class GameApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jeu Pokémon")  
        self.clock = pygame.time.Clock()
        self.running = True
        
        
        self.menu = MainMenu()
        self.game = None
        self.settings = None
        
        
        self.current_window = self.menu
    
    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            
            result = self.current_window.handle_events(events)
            
           #change de fenêtre et quitter
            if result == "menu":
                self.current_window.destroy()
                if not self.menu or not self.menu.active:
                    self.menu = MainMenu()
                self.current_window = self.menu
                pygame.display.set_caption("Jeu Pokémon - Menu Principal")
                
            elif result == "game":
                self.current_window.destroy()
                self.game = GameWindow()
                self.current_window = self.game
                pygame.display.set_caption("Jeu Pokémon")
                
            elif result == "combat":
                if isinstance(self.current_window, GameWindow) and self.current_window.selected_pokemon:
                    self.current_window.destroy()
                    self.combat = combatWindow(self.current_window.selected_pokemon)
                    self.current_window = self.combat
                    pygame.display.set_caption("Jeu Pokémon - Combat")
                               
            elif result == "settings":
                self.current_window.destroy()
                self.settings = SettingsWindow()
                self.current_window = self.settings
                pygame.display.set_caption("Jeu Pokémon - statistique")
               
            elif result == "quit":
                self.running = False
            self.current_window.render(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = GameApp()
    app.run()