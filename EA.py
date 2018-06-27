#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 08:48:24 2017

@author: julian
"""

import math
import random
import matplotlib.pyplot as plt

pi = math.pi

def create_population(cities, size):
    population = []
    for i in range(size):
        tour = cities[:]
        random.shuffle(tour)
        
        member = {
                "tour" : tour,
                "fitness" : fitness_function(tour)
                }
        
        population.append(member)
    return population

def get_cities():
    with open("/home/julian/cities.txt", "r") as input:
        
        cities = []
        for line in input:
            cities.append(line.split())
    
        input.close()
    
        return cities

def great_circle_distance(city_1, city_2):
    lat_city_1 = pi * (float(city_1[1]) / 1000) / 180.0
    long_city_1 = pi * (float(city_1[2]) / 1000) / 180.0
    lat_city_2 = pi * (float(city_2[1]) / 1000) / 180.0
    long_city_2 = pi * (float(city_2[2]) / 1000) / 180.0
    
    q1 = math.cos(lat_city_2) * math.sin(long_city_1 - long_city_2)
    q3 = math.sin((long_city_1-long_city_2) / 2.0)
    q4 = math.cos((long_city_1-long_city_2) / 2.0)
    q2 = math.sin(lat_city_1 + lat_city_2)*q3*q3-math.sin(lat_city_1 - lat_city_2)*q4*q4
    q5 = math.cos(lat_city_1 - lat_city_2)*q4*q4-math.cos(lat_city_1 + lat_city_2)*q3*q3
    return (int(6378388.0 * math.atan2(math.sqrt(q1*q1+q2*q2),q5) + 1.0) / 1000)

def fitness_function(member_of_population):
    fitness = 0
    for i in range(len(member_of_population)):
        if i+1 < len(member_of_population):
            
            fitness += great_circle_distance(member_of_population[i],member_of_population[i+1])
        elif i+1 == len(member_of_population):
            
            fitness += great_circle_distance(member_of_population[i],member_of_population[0])
    
    return fitness

def mutate(member_of_population):

    random_index_1 = random.randint(0, len(population) - 1)
    random_index_2 = random.randint(0, len(population) - 1)
    
       
    #if no mutation try again
    
    if random_index_1 == random_index_2:
        return mutate(member_of_population)
    
    city_1 = member_of_population["tour"][random_index_1]
    city_2 = member_of_population["tour"][random_index_2]
    
    
    mutant = {}
    
    mutant["tour"] = member_of_population["tour"][:]
    mutant["tour"][random_index_1] = city_2
    mutant["tour"][random_index_2] = city_1
    
    mutant["fitness"] = fitness_function(mutant["tour"])
    
    return mutant

def fittest_in_population(population):
    fittest_member = population[0]
    for member in population:
        
        if member["fitness"] < fittest_member["fitness"]:
            fittest_member = member
            
        
    
    return fittest_member

def tournament_selection(population, tournament_size):
    
    tournament = []
    for i in range(tournament_size):
        random_index = random.randint(0, len(population) - 1)
        tournament.append(population[random_index])
        
    
    winner = fittest_in_population(tournament)
    
    
    return winner

def remove_weakest_in_population(population):
    weakest_member = population[0]

    for member in population:
        
        if member["fitness"] > weakest_member["fitness"]:
            weakest_member = member
        
    population.remove(weakest_member)

"""
Example experiment:
"""
        
    

population = create_population(get_cities(),900)

resultChartX = []
resultChartY = []

for i in range(10000):
    if i % 500 == 0:
        fitness_right_now = fitness_function(fittest_in_population(population)["tour"])
        print(i)
        print(fitness_right_now)
        resultChartX.append(i)
        resultChartY.append(fitness_right_now)
    Parent = tournament_selection(population, 10)
    Child = mutate(Parent)
    remove_weakest_in_population(population)
    population.append(Child)
    
solution = fittest_in_population(population)

print(fitness_function(solution["tour"]))
    
plt.plot(resultChartX,resultChartY)
plt.ylabel("Fitness")
plt.xlabel("Number of Generations")
plt.show()
