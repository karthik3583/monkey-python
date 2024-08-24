import random
from deap import base, creator, tools, algorithms
from deap.benchmarks.tools import hypervolume
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import argparse
from datetime import datetime
import os
import time

# Argument parser for NSGA-II
parser = argparse.ArgumentParser()
parser.add_argument("--url", help="URL to use")
parser.add_argument("--ngen", default=10, help="Number of generations")
parser.add_argument("--npop", default=2, help="Number of populations")
parser.add_argument("--nchromo", default=2, help="Number of chromosomes")
parser.add_argument("--headless", default=1, help="Headless mode; 0 for no, 1 for yes")
args = parser.parse_args()

num_chromosomes = int(args.nchromo)

# DEAP setup
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))
creator.create("TestCase", list, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()

def open_browser(url):
    '''Will open the browser'''
    driver = webdriver.Firefox()
    driver.maximize_window()
    try:
        driver.get(url)
        with open("./gremlins.js") as f:
            driver.execute_script(f.read())
        driver.execute_script("var horde = gremlins.createHorde(); horde.unleash();")
        time.sleep(5)  # Let the gremlins do their thing
    except Exception as e:
        print(e)
    return driver

def evaluate(individual):
    errors = []
    driver = open_browser(args.url)
    if not driver:
        return len(individual), len(errors)
    
    try:
        # Example interaction with the page using individual test cases
        for action in individual:
            # Custom interaction logic here (e.g., sending keys, clicking, etc.)
            pass

        # Collect errors (this is a simplified example)
        for entry in driver.get_log('browser'):
            errors.append(entry)

    except Exception as e:
        print(f"Error during evaluation: {e}")
    finally:
        driver.quit()

    # Return objectives: Length of test case and number of errors
    return len(individual), len(errors)

toolbox.register("attr_generator", lambda: random.choice(['action1', 'action2', 'action3']))
toolbox.register("individual", tools.initRepeat, creator.TestCase, toolbox.attr_generator, n=num_chromosomes)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.5)
toolbox.register("select", tools.selNSGA2)

def main(seed=None):
    random.seed(seed)
    NGEN = int(args.ngen)
    MU = int(args.npop)
    CXPB = 0.9

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "min", "avg", "max"

    pop = toolbox.population(n=MU)
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    pop = toolbox.select(pop, len(pop))
    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    for gen in range(1, NGEN):
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)
                del ind1.fitness.values, ind2.fitness.values

            toolbox.mutate(ind1)
            toolbox.mutate(ind2)

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop = toolbox.select(pop + offspring, MU)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)

    print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))

    return pop, logbook

if __name__ == "__main__":
    pop, stats = main()
    with open("report_{:%B_%d_%Y}.txt".format(datetime.now()), "w") as f:
        for ind in pop:
            f.write(str(ind))
            f.write("\n")
            evaluate(ind)  # Re-evaluate for logging
