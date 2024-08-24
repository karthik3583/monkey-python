# monkey-python
Monkey testing with gremlins.js using python

Run the monkey using command :

python browser.py 

Requirements:

1. Selenium
2. Python 3.6
3. Gecko driver - For Mozilla Firefox
4. Chrome driver - For Google Chrome

5. Description of the NSGA-II Algorithm and Selenium Script Integration
NSGA-II Algorithm Overview
NSGA-II (Non-dominated Sorting Genetic Algorithm II) is a popular evolutionary algorithm used for solving multi-objective optimization problems. It operates by simulating the process of natural selection, evolving a population of candidate solutions over multiple generations to optimize multiple objectives simultaneously. The key features of NSGA-II include:

Population Initialization: A population of candidate solutions (individuals) is randomly generated.
Fitness Evaluation: Each individual is evaluated based on multiple objectives, which determine how "fit" or optimal it is.
Selection: Individuals are selected for reproduction based on their fitness and their ability to "dominate" other solutions (i.e., being better in all objectives).
Crossover and Mutation: Selected individuals undergo crossover (recombination of genes) and mutation (random alterations) to produce offspring.
Non-dominated Sorting and Crowding Distance: Individuals are ranked into different levels of non-dominance (Pareto fronts), and a crowding distance metric is used to maintain diversity in the population.
Elitism: The best individuals (based on rank and crowding distance) are carried over to the next generation to ensure the population improves over time.
Termination: The process repeats for a predefined number of generations or until a convergence criterion is met.
Integration with Selenium for Web Application Testing
In this script, the NSGA-II algorithm is integrated with Selenium to automate web application testing. Selenium is a popular tool for automating web browsers, and it is used here to simulate user interactions with a web application. The integration works as follows:

Test Case Generation: Each individual in the population represents a sequence of test cases, where each test case consists of a series of user interactions with the web application (e.g., clicks, form submissions).
Web Interaction Using Selenium: The evaluate function in the NSGA-II framework opens a web browser using Selenium, performs the test cases represented by the individual, and interacts with the web application.
Error Collection: During the interaction, any JavaScript errors or other issues encountered are logged and counted.
Fitness Evaluation: The fitness of each individual is determined by two objectives: the length of the test case sequence (to minimize complexity) and the number of errors encountered (to maximize reliability).
Evolutionary Process: The NSGA-II algorithm uses these fitness values to evolve the population, aiming to find the optimal set of test cases that balance thoroughness (longer sequences) with reliability (fewer errors).
Script Breakdown
Argument Parsing: The script accepts command-line arguments to configure the URL, number of generations, population size, and other parameters.
Selenium Setup: The open_browser function initializes a Firefox browser, navigates to the specified URL, and injects a script (e.g., Gremlins.js) to perform random actions on the page.
NSGA-II Integration: The evaluate function uses Selenium to run the test cases and collect errors, returning these as the objectives for the genetic algorithm.
Main Loop: The main loop of the NSGA-II algorithm runs for a specified number of generations, evolving the population by selecting, mating, and mutating individuals based on their fitness.
Reporting: After the evolutionary process is complete, the script generates a report detailing the best-performing test cases and their corresponding errors.
Summary
This script combines the NSGA-II algorithm with Selenium to automate the process of optimizing web application test cases. The goal is to find a set of test cases that thoroughly exercise the application while minimizing errors, thereby improving the application's robustness and reliability. The NSGA-II algorithm efficiently searches the space of possible test cases, while Selenium provides a powerful tool for automating and evaluating those test cases in a real web environment.
