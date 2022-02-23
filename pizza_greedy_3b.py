#!/usr/bin/env python3
# Author: Javier Gatón Herguedas.
# Pizza Hash Code Answer using a greedy approach.
# It saves the clients that collide with less clients.

from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Client():
    def __init__(self, id: str, client_likes: List[str], client_dislikes: List[str], num_collisions: int, collided_clients: List[int]):
        self.id = id
        self.client_likes = client_likes
        self.client_dislikes = client_dislikes
        self.num_collisions = num_collisions
        self.collided_clients = collided_clients

@dataclass
class Solution():
    def __init__(self, puntuacion: int, ingredients: List[str]):
        self.puntuacion = puntuacion
        self.ingredients = ingredients

def input_data() -> Tuple[Dict[str, List[int]], Dict[str, List[int]], List[Client]]:
    num_clients = int(input())
    likes: Dict[str, List] = {}
    dislikes: Dict[str, List] = {}
    clients: List[Client] = []

    for id in range(num_clients):
        like_line = input().split()
        n_likes = int(like_line[0])
        client_likes = []

        dislike_line = input().split()
        n_dislikes = int(dislike_line[0])
        client_dislikes = []

        num_collisions = 0
        collided_clients = []

        # Check that its not a troll client
        troll = False
        for i in range(n_likes):
            food = like_line[i+1]
            for j in range(n_dislikes):
                dfood = dislike_line[j+1]
                if dfood == food:
                    troll = True
                    break
            if troll:
                break
        if troll:
            continue

        for i in range(n_likes):
            food = like_line[i+1]
            client_likes.append(food)
            if food in likes:
                likes[food].append(id)
            else:
                likes[food] = [id]
            if food in dislikes:
                ds = dislikes[food]
                for j in ds:
                    if j not in collided_clients:
                        collided_clients.append(j)
                        num_collisions += 1
                        clients[j].collided_clients.append(id)
                        clients[j].num_collisions += 1
        for i in range(n_dislikes):
            food = dislike_line[i+1]
            client_dislikes.append(food)
            if food in dislikes:
                dislikes[food].append(id)
            else:
                dislikes[food] = [id]
            if food in likes:
                ls = likes[food]
                for j in ls:
                    if j not in collided_clients:
                        collided_clients.append(j)
                        num_collisions += 1
                        clients[j].collided_clients.append(id)
                        clients[j].num_collisions += 1
        clients.append(Client(id, client_likes, client_dislikes, num_collisions, collided_clients))
    return likes, dislikes, clients

def get_non_collision_ingredients(likes: Dict[str, List], dislikes: Dict[str, List]) -> List[str]:
    foods = []
    for food in likes.keys():
        if not food in dislikes or len(dislikes[food]) == 0:
            foods.append(food)
    return foods

def get_factor_others_collisions(clients: List[Client], index: int) -> int:
    n_colls = []
    for i in clients[index].collided_clients:
        n_colls.append(-clients[i].num_collisions)
    n_colls.sort()
    return n_colls

def delete_client(id: int, likes: Dict[str, List[int]], dislikes: Dict[str, List[int]], clients: List[Client],
                  order_clients: List[Tuple[int, int, int]]):
    indexes_id = [i for i,v in enumerate(order_clients) if v[2]==id]
    deleting_id = order_clients.pop(indexes_id[0])[2]
    lik_foods = clients[deleting_id].client_likes
    for food in lik_foods:
        likes[food].remove(deleting_id)
        if food in dislikes:
            for j in dislikes[food]:
                if deleting_id in clients[j].collided_clients:
                    clients[j].num_collisions -= 1
                    clients[j].collided_clients.remove(deleting_id)
    dis_foods = clients[deleting_id].client_dislikes
    for food in dis_foods:
        dislikes[food].remove(deleting_id)
        if food in likes:
            for j in likes[food]:
                if deleting_id in clients[j].collided_clients:
                    clients[j].num_collisions -= 1
                    clients[j].collided_clients.remove(deleting_id)

def main():
    likes, dislikes, clients = input_data()
    order_clients = [(clients[i].num_collisions, get_factor_others_collisions(clients, i), i) for i in range(len(clients))]
    order_clients.sort()
    puntuacion = sum(1 for c in clients if c.num_collisions == 0)
    ingredients = get_non_collision_ingredients(likes, dislikes)
    best_solution = Solution(puntuacion, ingredients)
    while order_clients:
        if not order_clients:
            print("Impossible!")
            break
        indexes_id = [i for i,v in enumerate(order_clients) if clients[v[2]].num_collisions!=0]
        if not indexes_id:
            #print("Fin")
            break
        keeping_id = order_clients[indexes_id[0]][2]
        lik_foods = clients[keeping_id].client_likes
        for food in lik_foods:
            if food in dislikes:
                for j in dislikes[food]:
                    if keeping_id in clients[j].collided_clients:
                        delete_client(j, likes, dislikes, clients, order_clients)
        dis_foods = clients[keeping_id].client_dislikes
        for food in dis_foods:
            if food in likes:
                for j in likes[food]:
                    if keeping_id in clients[j].collided_clients:
                        delete_client(j, likes, dislikes, clients, order_clients)
        order_clients = [(clients[oc[2]].num_collisions, get_factor_others_collisions(clients, oc[2]), oc[2]) for oc in order_clients]
        order_clients.sort()
        puntuacion = sum(1 for c in clients if c.num_collisions == 0)
        if puntuacion > best_solution.puntuacion:
            ingredients = get_non_collision_ingredients(likes, dislikes)
            best_solution = Solution(puntuacion, ingredients)
        #DO NOT DELETE THE CLIENT THAT WOULD BREAK IT
    print(puntuacion)
    print(len(best_solution.ingredients), *best_solution.ingredients)

if __name__ == "__main__":
    main()