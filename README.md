# Simulation of Ecosystem in Rossumøya Island
***
## Exam Project Jan 2023 INF200
***
### Authors: Navneet Sharma and Sushant Kumar Srivastava
***

### Description
***
***Background***

The package contains population dynamics simulation on Rossumøya Island's ecosystem.
The ecosystem contains different landscapes types, such as Lowland,Highland,Desert 
and Water.The Island's fauna consists of two different species:Herbivores which eat 
plants and Carnivores who are predators and hunt on herbivores.The Simulation is about
finding the survival of the species in the long run for a given number of years.During the 
Simulation one can analyze the number of years that has been simulated along with total 
number of animals on the island per species,their fitness,age and weight distribution 
plotted on a histogram and their distribution on the island by heatmaps.

The Exam Sheet containing the details and rules could be found here:
[BioSim_Jan_Sheet](https://gitlab.com/nmbu.no/emner/inf200/h2022/january-block-teams/a36_navneet_sushant/biosim-a36-navneet-sushant/-/blob/main/INF200_H22_BioSimJan_v1.pdf)

***Installation***
***
```
The BioSim project supports python 3.6+.
It requires some libraries and packages in order to run such as 

    *matplotlib
    *numpy
    *os
    *textwrap
    *subprocess
    *random
    *mpl_toolkits
```
**Notes**
***
1. All the test simulations in reference_examples are running as expected
1. Test files under tests directory are able to check most of the simulation possibilities
1. Plots are displaying, getting saved and movie is being created successfully
1. flake8 src tests examples : passed
1. tox : passed
1. make html : passed
1. make epub : passed


***Contents***
***
```
-examples
    *testing_01.py
    *testing_02.py
    *testing_03.py
    *testing_04.py
-src/biosim
    *fauna.py
    *landscape.py
    *map.py
    *simulation.py
    *visualization.py
-tests
    *test_fauna.py
    *test_landscape.py
    *test_map.py
    *test_simulation.py
```

Project design:
```
src/biosim/
```

Presentation:
```
Exam/
```

***Simulation Results:***
***
```
reference_examples/results/
```
![](/Exam/sample.gif)

***References:***
***

1. Anders, & Peters. (n.d.). GitHub - pkhetland/BioSim_G03_anders_Petter: Team repository for 
   “Advanced Python Programming” class exam project (Biosimulation).
2. S, F. (n.d.). GitHub - fabiorodp/NMBU_BioSim_project: Project for the Msc in data analysis, 
   course INF200, at NMBU University.


