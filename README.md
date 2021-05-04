## Algorithme de colonies de fourmis - Système complexe

### Simulateur ACO

#### Introduction

Construire un programme afin de simuler `Algorithme de colonies de fourmis` avec 2 chemins de même longueur et 2 chemins de longueurs inégales pour observer les trajectoires des fourmis qui chercher la nourriture et retourner son nid sur les chemins différents

#### Utilisation

Lance ce simulateur dans le terminal avec la line de commande suivante. 

Ps;il faut d'abord installer des bibliothèques `tkinter` 、 `threading`, `reduce`.

```
python3 aco-simulateur.py
```

Par défaut, il y a 50 fourmis qui partent de nid à chercher la nourriture sur le chemin `court` ou `long`, cela dépende de type de recherche.
Le programme support deux type de recherche `recherche court chemin` et `recherche longueur chemin`.
Par défaut en mode `recherche court chemin`, cela peut changer par le clé du clavier `c` ou `l`.

#### Résolution

##### Construire des chemins différents
<div style="text-align:center;width:80%;margin:0 auto;">
<img src="https://imgur.com/KErPYl6.png" width="80%"/><br/>
<p>(2 chemins de même longueur)</p>
<img src="https://imgur.com/8dvnra7.png" width="80%"/><br/>
<p>(2 chemins de longueurs inégales)</p>
</div>
<br/>
<br/>
En utilisant les positions (x,y) de fenêtre actuelle avec les données spécifiques.

Ps; il y a un position réitératif sur les données nid, c'est pour faciliter de calculer le chemin inversement au niveau programme.

```
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
```

##### Initialise les paramètres
 
```
...
self.ant_num = 50
self.iterator = 0
self.running = False
...

# initialise les donées dynamique de fourmi
self.ants = {
    "court": [],
    "long": []
}

```
Initialise les paramètres et données afin d'utiliser pendant l'exécution du programme.

```
# Initialise les états de villes
for i in range(len(self.citys[type]['path'])):
    self.citys[type]['path'][i]['index'] = i
    self.citys[type]['path'][i]['pheromone'] = 1.0
```

Initialise l'état de chaque ville, Notamment sur la quantité de pheromone. par défaut, chaque ville de pheromone est identique.

```    
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
```

Initialise tous l'états de fourmi par défaut.

<br/>

##### Processus de la recherche

1) par défaut, le programme commence à la recherche sur les 2 même longueur du chemins. il boucle toujours s'il n'est pas en état terminé.

```
 while self.running:
    self.search_path(type)
```

En suite, il boucle toutes les fourmis par le type sélectif qui n'ont pas trouvé de nourriture lorsque toutes les fourmis bougent un pas, l'itération s'augmente de 1.

```
 # parcourir toutes les fourmis vers chaque chemin
 def search_path(self, type):
    for i in self.ants[type]:
        if not self.ants[type][i]['is_stop']:
            self.cacule_next_city(type, i)
            self.move_next_city(type, i)
    
    self.iterator += 1
```

À chaque pas, les fourmis entrent dans ce boucle.

Premièrement, il initialise la ville de départ si le position de ville de fourmi est vide en deux modes  ci-dessous:

Il y a deux situations sur la ville départ: 
                                                                                   
1) Génère aléatoirement une ville départ entre le premier chemin et le deuxième chemin avec une taux de 50% 

```
 if self.ants[type][ant_index]['current_city'] is None:
    # initialise les deux premire fourmis
    if ant_index % 2 == 0:
        self.ants[type][ant_index]['current_city'] = self.citys[type]['path'][
            start_end_pos[random.randint(0, 1)]]
   ........
```

2) Calcule le maximum pheromone sur le premier chemin et le deuxième chemin avec une taux de 50%

```
# cacule le pheromone par chemin
self.ants[type][ant_index]['current_city'] = self.cacule_chemin_pheromone(type, ant_index,nourriture_index)
```

```
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
```

Il va retourner la maximum pheromone de ville départ entre le premier chemin et le deuxième chemin

Exemple du chemin même longueur avec 2 cas:
```
{'x': 75, 'y': 200, 'nest': True, 'food': False, 'index': 0, 'pheromone': 1.0, 'distance': 302.0}
Itération: 0 Chemins du fourmi - 1 :  [(75, 200)] Pheromone: 1.0
{'x': 75, 'y': 200, 'nest': True, 'food': False, 'index': 4, 'pheromone': 1.0, 'distance': 302.0}
Itération: 0 Chemins du fourmi - 2 :  [(75, 200)] Pheromone: 1.0
```

En suite, lorsque le fourmi a une ville départ, il va vérifier si le fourmi a trouvé la nourriture. 

```
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
```

Si non, il va retourner la ville prochaine avec sa direction 

Exemple du chemin même longueur:
```
{'x': 377, 'y': 150, 'nest': False, 'food': False, 'index': 1, 'pheromone': 1.0, 'distance': 303.0}
Itération: 1 Chemins du fourmi - 1 :  [(75, 200), (377, 150)] Pheromone: 304.0
{'x': 377, 'y': 300, 'nest': False, 'food': False, 'index': 3, 'pheromone': 303.0, 'distance': 302.0}
Itération: 1 Chemins du fourmi - 2 :  [(75, 200), (377, 300)] Pheromone: 605.0
```

`opposite` permet d'indiquer la direction de marche par défaut, il est `False`. lorsque le fourmi trouve la nourriture, il va être `True` afin de calculer le chemin retour via son nid.

```
 # défini la région de recherche
    if self.ants[type][ant_index]['opposite']:
        idx = self.ants[type][ant_index]['current_city']['index'] - 1
    else:
        idx = self.ants[type][ant_index]['current_city']['index'] + 1

    self.ants[type][ant_index]['next_city'] = self.citys[type]['path'][idx]
```

Si oui, il marque dans sa propriété `is_food` sur le fourmi actuelle.

Exemple du chemin même longueur:
```
{'count': 2, 'opposite': False, 'current_id': 1, 'current_path': [(75, 200), (377, 150)], 'is_stop': False, 'is_food': True, 'next_city': {'x': 377, 'y': 150, 'nest': False, 'food': False, 'index': 1, 'pheromone': 11818.0, 'distance': 303.0}, 'current_city': {'x': 680, 'y': 200, 'nest': False, 'food': True, 'index': 2, 'pheromone': 15151.0, 'distance': 303.0}, 'total_distence': 303.0}
Itération: 2 Chemins du fourmi - 1 :  [(75, 200), (377, 150), (680, 200)] Pheromone: 15151.0
{'count': 2, 'opposite': True, 'current_id': 2, 'current_path': [(75, 200), (377, 300)], 'is_stop': False, 'is_food': True, 'next_city': {'x': 377, 'y': 300, 'nest': False, 'food': False, 'index': 3, 'pheromone': 3323.0, 'distance': 302.0}, 'current_city': {'x': 680, 'y': 200, 'nest': False, 'food': True, 'index': 2, 'pheromone': 15151.0, 'distance': 303.0}, 'total_distence': 303.0}
Itération: 2 Chemins du fourmi - 2 :  [(75, 200), (377, 300), (680, 200)] Pheromone: 15151.0
```

Ensuite, il calcule le maximum pheromone de chemin retourné avec sa direction de marche

```
# calcule le pheromone du chemin
    def cacule_chemin_pheromone(self, type, ant_index, nourriture_index):
    
    ..................................
    
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
```

Lorsque le fourmi a une ville suivante, il va déplace et mise à jour le phéromone du chemin avec la distance de ville et note le position du chemin dans sa propriété  `current_path` et le programme continue.

```
# deplace les fourmis  
    def move_next_city(self, type, ant_index):
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
```

Lorsque le fourmi retourne son nid, il marque dans sa propriété `is_stop` qui permet de s'arrêter le recherche en cours.

```
  # vérification le retour du nid
        if self.ants[type][ant_index]['next_city']['nest'] and self.ants[type][ant_index]['count'] > 0:
            self.ants[type][ant_index]['is_stop'] = True
            # self.ants[type][ant_index]['next_city'] = self.ants[type][ant_index]['next_city']
            return
```

Exemple retourné au nid avec chemin même longueur:
```
{'count': 3, 'opposite': True, 'current_id': 1, 'current_path': [(75, 200), (377, 150), (680, 200), (377, 150), (75, 200)], 'is_stop': True, 'is_food': True, 'next_city': {'x': 75, 'y': 200, 'nest': True, 'food': False, 'index': 0, 'pheromone': 11779.0, 'distance': 302.0}, 'current_city': {'x': 377, 'y': 150, 'nest': False, 'food': False, 'index': 1, 'pheromone': 11818.0, 'distance': 303.0}, 'total_distence': 303.0}
Itération: 3 Chemins du fourmi - 1 :  [(75, 200), (377, 150), (680, 200), (377, 150), (75, 200)] Pheromone: 11818.0
{'count': 3, 'opposite': False, 'current_id': 2, 'current_path': [(75, 200), (377, 300), (680, 200), (377, 300), (75, 200)], 'is_stop': True, 'is_food': True, 'next_city': {'x': 75, 'y': 200, 'nest': True, 'food': False, 'index': 4, 'pheromone': 3323.0, 'distance': 302.0}, 'current_city': {'x': 377, 'y': 300, 'nest': False, 'food': False, 'index': 3, 'pheromone': 3323.0, 'distance': 302.0}, 'total_distence': 303.0}
Itération: 3 Chemins du fourmi - 2 :  [(75, 200), (377, 300), (680, 200), (377, 300), (75, 200)] Pheromone: 3323.0
```

Exemple retourné au nid avec chemin longueur inégales:
```
{'count': 4, 'opposite': False, 'current_id': 1, 'current_path': [(75, 230), (200, 150), (377, 90), (530, 150)], 'is_stop': False, 'is_food': False, 'next_city': None, 'current_city': {'x': 680, 'y': 230, 'nest': False, 'food': True, 'index': 4, 'pheromone': 3940.0, 'distance': 303.0}, 'total_distence': 303.0}
Itération: 3 Chemins du fourmi - 1 :  [(75, 230), (200, 150), (377, 90), (530, 150)] Pheromone: 301.0
{'count': 3, 'opposite': False, 'current_id': 2, 'current_path': [(75, 230), (377, 330), (680, 230), (377, 330), (75, 230)], 'is_stop': True, 'is_food': True, 'next_city': {'x': 75, 'y': 230, 'nest': True, 'food': False, 'index': 6, 'pheromone': 3323.0, 'distance': 302.0}, 'current_city': {'x': 377, 'y': 330, 'nest': False, 'food': False, 'index': 5, 'pheromone': 3323.0, 'distance': 302.0}, 'total_distence': 303.0}
Itération: 3 Chemins du fourmi - 2 :  [(75, 230), (377, 330), (680, 230), (377, 330), (75, 230)] Pheromone: 3323.0
```

#### Conclusion

Après avoir comparé les résultats avec les chemins différents (même longueur et longueurs inégales).

On peut bien voir le recherche sur le chemin longueurs inégales qui s'arrête lorsqu'il y a un fourmi à retourner son nid.

Si on utilise pas l'évaporation de pheromone lorsque un fourmi a retourné. on a obtenu toujours un résultat limité.
C'est à dir qu'on ne peut que trouver un meilleur chemin dans une petite partie au lieu d'avoir un meilleur chemin dans touts les chemins.

Parce que après les deux premiers fourmis marchent sur les villes. toutes les fourmis restes choisissent probablement un chemin passé qui a le pheromone maximum.

Si on veut toutes les fourmis à trouver la nourriture, il faut utiliser l'évaporation de pheromone.

C'est pour ça qu'on fait la deuxième partie pour résoudre le problème du voyage.

### Travelling Salesman Problem (TSP)

<div style="text-align:center">
 <img src="https://imgur.com/pt4cRSE.png" style="width:80%;margin:0 auto;" text-align:center;/>
<p style="width:80%;margin:0 auto;text-align:center;">(Travelling Salesman Problem)</p>

 </div>     
