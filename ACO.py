#
# Algorithme de colonies de fourmis
#
# @author Zhao ZHANG
# @email  zo.zhang@gmail.com
# @website https://zozhang.github.io
#

import random
import tkinter
import threading
from functools import reduce


class Aco(object):

    # Initialise les paramètres
    def __init__(self):
        self.initialise_data()
        self.initialise_canvas()
        self.initialise_position()
        self.initialise_events()
        self.cout_search()
        self.tkinter.mainloop()

    # initialise donnée
    def initialise_data(self):
        self.round = 6
        self.ant_num = 50
        self.iterator = 0
        self.width = 800
        self.height = 400
        self.running = False
        self.current_ant = None
        self.thread_lock = threading.RLock()

        # initialise les donées dynamique de fourmi
        self.ants = {
            "court": [],
            "long": []
        }

        # initialise les donées statiques de ville
        self.citys = {
            "court": {
                "title": " 2 chemins de même longueur",
                "path": [
                    {"x": 75, "y": 200, "nest": True, "food": False},
                    {"x": 377, "y": 150, "nest": False, "food": False},
                    {"x": 680, "y": 200, "nest": False, "food": True},
                    {"x": 377, "y": 300, "nest": False, "food": False},
                    {"x": 75, "y": 200, "nest": True, "food": False}
                ]
            },
            "long": {
                "title": " 2 chemins de longueurs inégales",
                "path": [
                    {"x": 75, "y": 230, "nest": True, "food": False},
                    {"x": 200, "y": 150, "nest": False, "food": False},
                    {"x": 377, "y": 90, "nest": False, "food": False},
                    {"x": 530, "y": 150, "nest": False, "food": False},
                    {"x": 680, "y": 230, "nest": False, "food": True},
                    {"x": 377, "y": 330, "nest": False, "food": False},
                    {"x": 75, "y": 230, "nest": True, "food": False}
                ]
            }
        }

    # initialise canvas
    def initialise_canvas(self):
        self.tkinter = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.tkinter,
            width=self.width,
            height=self.height,
            bg="#FFF",
            xscrollincrement=1,
            yscrollincrement=1
        )

        #self.ant_gif = tkinter.PhotoImage(file='images/ant.png')
        self.canvas.pack()

    # création les lignes sur cavancs
    def initialise_lines(self, type):

        self.clear_canvans()
        # initialise title du canvas
        self.tkinter.title("ACO Simulateur - " + self.citys[type]['title'])

        # initialise les texts du keyboard
        self.canvas.create_text(120, 25, text='c: recherche court chemin', font=("Purisa", 18), fill='black')
        self.canvas.create_text(360, 25, text='l: recherche longueur chemin', font=("Purisa", 18), fill='black')
        self.canvas.create_text(580, 25, text='s: arrête le recherche', font=("Purisa", 18), fill='black')
        self.canvas.create_text(720, 25, text='q: quitte', font=("Purisa", 18), fill='black')

        # initialise un cavans
        for pos in self.citys[type]['path']:
            # initialise les couleur de nid/nourriture
            if pos['nest']:
                fill_text = '#0d6af7'
            elif pos['food']:
                fill_text = '#43c70e'
            else:
                fill_text = '#ff0000'

            # création les lignes entre les villes
            x, y = pos['x'], pos['y']
            self.canvas.create_oval(x - self.round, y - self.round, x + self.round, y + self.round, fill=fill_text,
                                    outline="#000000")
            self.canvas.create_text(x, y - 25, text='(' + str(x) + ',' + str(y) + ')', fill='black')

            if pos['nest']:
                self.canvas.create_text(x, y + 20, text='Nid', fill='black')
            elif pos['food']:
                self.canvas.create_text(x, y + 20, text='Nourriture', fill='black')

        # designe les lignes
        reduce(self.create_line, self.citys[type]['path'], self.citys[type]['path'][-1])

    # génére les lignes entre les villes
    def create_line(self, current, next):
        self.canvas.create_line((current['x'], current['y']), (next['x'], next['y']), fill="#000000")
        return next

    # nettoie le cavancs
    def clear_canvans(self):
        # clear les lignes de ville
        for item in self.canvas.find_all():
            self.canvas.delete(item)

    # initialise les events par keyboard
    def initialise_events(self):
        self.tkinter.bind("c", self.cout_search)
        self.tkinter.bind("l", self.long_search)
        self.tkinter.bind("s", self.stop_search)
        self.tkinter.bind("q", self.quite_search)

    # génére les positions dans le cavans
    def initialise_position(self):
        for type in self.citys:
            self.ants[type] = {}

            # Initialise les états de villes
            for i in range(len(self.citys[type]['path'])):
                self.citys[type]['path'][i]['index'] = i
                self.citys[type]['path'][i]['pheromone'] = 1.0

                # Initialise les distences x de villes
                curr_idx = i
                next_idx = i + 1
                if next_idx > len(self.citys[type]['path']) - 1:
                    next_idx = i

                # la distence de ville vers ville suivante
                if curr_idx == len(self.citys[type]['path']) - 1:
                    diff_pos = self.citys[type]['path'][curr_idx]['x'] - self.citys[type]['path'][curr_idx - 1]['x']
                else:
                    diff_pos = self.citys[type]['path'][next_idx]['x'] - self.citys[type]['path'][curr_idx]['x']

                self.citys[type]['path'][i]['distance'] = float(abs(diff_pos))

            # initialise les états défauts pour tous les fourmis
            for i in range(self.ant_num):
                self.ants[type][i] = {}
                self.ants[type][i]['count'] = 0
                self.ants[type][i]['opposite'] = False
                self.ants[type][i]['current_id'] = i
                self.ants[type][i]['current_path'] = []
                self.ants[type][i]['is_stop'] = False
                self.ants[type][i]['is_food'] = False
                self.ants[type][i]['next_city'] = None
                self.ants[type][i]['current_city'] = None
                self.ants[type][i]['total_distence'] = 0.0

    # recherche le meilleur chemin
    def search_path(self, type):

        for i in self.ants[type]:
            if not self.ants[type][i]['is_stop']:
                self.cacule_next_city(type, i)
                self.move_next_city(type, i)

        self.iterator += 1

    # calcule le pheromone du chemin
    def cacule_chemin_pheromone(self, type, ant_index, nourriture_index):
        first_chemin_pheromone = []
        last_chemin_pheromone = []
        longeureu_chemin = len(self.citys[type]['path'])

        # initialise l'index par le nombre de pheromone par chemin defaut
        if self.ants[type][ant_index]['current_city'] is None:
            for i in range(longeureu_chemin):
                if i < nourriture_index - 1:
                    first_chemin_pheromone.append(self.citys[type]['path'][i]['pheromone'])
                if i > nourriture_index + 1:
                    last_chemin_pheromone.append(self.citys[type]['path'][i]['pheromone'])

            # count le nombre de pheromone sur un chemin
            if sum(first_chemin_pheromone) > sum(last_chemin_pheromone):
                idx = first_chemin_pheromone.index(max(first_chemin_pheromone))
            else:
                idx = last_chemin_pheromone.index(max(last_chemin_pheromone))

        # update les pheromones des chemin passés
        else:
            if self.ants[type][ant_index]['opposite']:
                for i in range(self.ants[type][ant_index]['current_city']['index'], len(self.citys[type]['path'])):
                    last_chemin_pheromone.append(self.citys[type]['path'][i]['pheromone'])
            else:
                for i in range(0, nourriture_index + 1):
                    first_chemin_pheromone.append(self.citys[type]['path'][i]['pheromone'])

            # compare les deux chemin des pheromones
            if sum(first_chemin_pheromone) > sum(last_chemin_pheromone):
                idx = nourriture_index - 1
                self.ants[type][ant_index]['opposite'] = False
            else:
                idx = nourriture_index + 1
                self.ants[type][ant_index]['opposite'] = True

        return self.citys[type]['path'][idx]

    # calcule le chemin par le maximum phéromone de villes
    def cacule_next_city(self, type, ant_index):

        # le pheromone par chemin
        self.total_pheromone = []
        longeureu_chemin = len(self.citys[type]['path'])

        # défini l'index de nourriture
        for i in range(len(self.citys[type]['path'])):
            if self.citys[type]['path'][i]['food']:
                nourriture_index = i
                break

        # initialise la ville départi
        start_end_pos = [0, longeureu_chemin - 1]
        if self.ants[type][ant_index]['current_city'] is None:

            # initialise les deux premire fourmis
            if ant_index % 2 == 0:
                self.ants[type][ant_index]['current_city'] = self.citys[type]['path'][
                    start_end_pos[random.randint(0, 1)]]
            else:
                # cacule le pheromone par chemin
                self.ants[type][ant_index]['current_city'] = self.cacule_chemin_pheromone(type, ant_index,
                                                                                          nourriture_index)

        # print("nourriture_index", nourriture_index, "opposite", self.ants[type][ant_index]['opposite'])

        # vérification la nourriture trouvé
        elif self.ants[type][ant_index]['current_city']['food']:
            self.ants[type][ant_index]['is_food'] = True
            self.ants[type][ant_index]['next_city'] = self.cacule_chemin_pheromone(type, ant_index, nourriture_index)
            return

        if not self.ants[type][ant_index]['is_food']:
            # parcourir par l'order du chemin par defaut
            if self.ants[type][ant_index]['current_city']['index'] > nourriture_index:
                self.ants[type][ant_index]['opposite'] = True
            else:
                self.ants[type][ant_index]['opposite'] = False
        else:
            self.ants[type][ant_index]['opposite'] = not self.ants[type][ant_index]['opposite']

        # défini la région de recherche
        if self.ants[type][ant_index]['opposite']:
            idx = self.ants[type][ant_index]['current_city']['index'] - 1
        else:
            idx = self.ants[type][ant_index]['current_city']['index'] + 1

        self.ants[type][ant_index]['next_city'] = self.citys[type]['path'][idx]

        # vérification le retour du nid
        if self.ants[type][ant_index]['next_city']['nest'] and self.ants[type][ant_index]['count'] > 0:
            self.ants[type][ant_index]['is_stop'] = True
            # self.ants[type][ant_index]['next_city'] = self.ants[type][ant_index]['next_city']
            return

    # deplace les fourmis sur les donnée dynamiques
    def move_next_city(self, type, ant_index):

        current_city_index = self.ants[type][ant_index]['current_city']['index']
        current_city = self.citys[type]['path'][current_city_index]

        if self.ants[type][ant_index]['is_stop']:
            # update path visited
            self.update_path(type, self.ants[type][ant_index]['current_city'], ant_index)
            self.update_path(type, self.ants[type][ant_index]['next_city'], ant_index)
            print('Itération:', self.iterator, 'Chemins du fourmi -', self.ants[type][ant_index]['current_id'], ': ',
                  self.ants[type][ant_index]['current_path'], 'Pheromone:',
                  self.citys[type]['path'][current_city_index]['pheromone'])

            self.stop_search()
            return

        # update pheromone
        if self.ants[type][ant_index]['next_city']['food']:
            self.ants[type][ant_index]['total_distence'] += self.ants[type][ant_index]['next_city']['distance']
            if self.ants[type][ant_index]['opposite']:
                for i in range(self.ants[type][ant_index]['next_city']['index'], len(self.citys[type]['path'])):
                    self.citys[type]['path'][i]['pheromone'] += self.citys[type]['path'][i]['distance']
            else:
                for i in range(0, self.ants[type][ant_index]['next_city']['index'] + 1):
                    self.citys[type]['path'][i]['pheromone'] += self.citys[type]['path'][i]['distance']

        # update path visited
        self.update_path(type, current_city, ant_index)
        self.ants[type][ant_index]['current_city'] = self.ants[type][ant_index]['next_city']
        self.ants[type][ant_index]['next_city'] = None
        self.ants[type][ant_index]['count'] += 1

        print('Itération:', self.iterator, 'Chemins du fourmi -', self.ants[type][ant_index]['current_id'], ': ',
              self.ants[type][ant_index]['current_path'], 'Pheromone:',
              self.citys[type]['path'][current_city_index]['pheromone'])

    # update path visited
    def update_path(self, type, current_city, ant_index):
        # self.ants[type][ant_index]['canvas'] = self.canvas.create_image((x, y), image=self.ant_gif)
        # dx, dy = self.ants[type][ant_index]['next_city']['x'], self.ants[type][ant_index]['next_city']['y']
        # self.canvas.move(self.ants[type][ant_index]['canvas'], dx, dy)
        self.ants[type][ant_index]['current_path'].append((current_city['x'], current_city['y']))

    # quitte le recherche
    def quite_search(self, evt=None):
        self.thread_lock.acquire()
        self.running = False
        self.thread_lock.release()
        self.tkinter.destroy()

    # commence à la recherche par les chemins même longeure
    def cout_search(self, evt=None):
        self.initialise_lines('court')
        self.start_search('court')

    # commence à la recherche par les chemins longeure inégales
    def long_search(self, evt=None):
        self.initialise_lines('long')
        self.start_search('long')

    # arrête le recherche actuelle
    def stop_search(self, evt=None):
        self.thread_lock.acquire()
        self.running = False
        self.thread_lock.release()

    # commence à la recherche par le type du chemin
    def start_search(self, type):
        self.thread_lock.acquire()
        self.running = True
        self.thread_lock.release()
        self.initialise_position()

        print("Commence à rechercher par le chemin:", type)
        print("Nombre de fourmi à rechercher:", self.ant_num)
        print("Tous les chemins:", self.citys[type]['path'])

        while self.running:
            self.search_path(type)

if __name__ == '__main__':
    Aco()
