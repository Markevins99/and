from random import choices, randint, randrange, random
from typing import List, Callable, Tuple
from functools import partial
import time
import collections
    
    
Genome = List[int]
Population = List[int]
Fitness_func = Callable[[Genome], int]   
Populate_func = Callable[[], Population]
Selection_func = Callable[[Population, Fitness_func], Tuple[Genome, Genome]]
Crossover_func = Callable[[Genome, Genome], Tuple[Genome, Genome]]
Mutation_func = Callable[[Genome], Genome]
Thing = collections.namedtuple('Thing', ['name', 'value', 'weight'])

things = [
    Thing('Laptop', 500, 2200),
    Thing('Headphones',150,160),
    Thing('Coffee Mug', 60, 350),
    Thing('Notepad', 40,333),
    Thing('Water Bottle', 30, 192)
    ]

def generate_genome(length:int)->Genome:
    return choices([0,1], k=length) 

def generate_population(size:int, genome_length:int)->Population:
    return [generate_genome(genome_length) for _ in range(size)]

def fitness(genome:Genome, things:[Thing], weight_limit:int)->int:
    if len(genome)!=len(things):
        raise ValueError("genome and things must be of the same size")
    weight = 0
    value = 0
    
    for i, thing in enumerate(things):
        if genome[i]==1:
            weight += thing.weight
            value += thing.value
            
            if weight > weight_limit:
                return 0
    return value



def selection_pair(population:Population, fitness_func:Fitness_func)->Population:
    return choices(
        population = population,
        weights=[fitness_func(genome) for genome in population],
        k=2
        )

def single_point_crossover(a: Genome, b:Genome)->Tuple[Genome, Genome]:
    
    if len(a)!=len(b):
        raise ValueError("Genome a and Genome b must be of the same length")
    
    length = len(a)
    if length < 2:
        return a, b
    
    p = randint(1,length-1)
    return a[0:p]+b[p:], b[0:p]+a[p:]

def mutation(genome:Genome, num: int =1, probability:float=0.5)->Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index]=genome[index] if random() > probability else abs(genome[index]-1)
    return genome

def run_evolution(
        populate_func:Populate_func,
        fitness_func:Fitness_func,
        fitness_limit:int,
        selection_func:Selection_func=selection_pair,
        crossover_func:Crossover_func=single_point_crossover,
        mutation_func:Mutation_func = mutation,
        generation_limit:int = 100
        )->Tuple[Population, int]:
    
    population = populate_func()
    
    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)
        
        if fitness_func(population[0])>=fitness_limit:
            break
        
        next_generation = population[0:2]
        
        for j in range(int(len(population)/2 - 1)):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation +=[offspring_a, offspring_b]
            
        population = next_generation
        
    return population, i

start = time.time()
population, generations = run_evolution(
    populate_func=partial(
        generate_population, size=10, genome_length = len(things)), 
    fitness_func = partial(
        fitness, things= things, weight_limit=3000
        ), 
    fitness_limit=740,
    generation_limit=100
    )

end =  time.time()

def genome_to_things(genome:Genome, things:[Thing])->[Thing]:
    result=[]
    for i, things in enumerate((things)):
        if genome[i]==1:
            result+= [things.name]
    return result

print(f"number of generation: {generations}")
print(f"time:{end-start}s")
print(f"best solution: {genome_to_things(population[0],things)}")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    


















