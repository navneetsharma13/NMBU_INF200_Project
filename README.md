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
The BioSim project supports python 3.6+.
It requires some libraries and packages in order to run such as 
    *matplotlib
    *numpy
    *os
    *textwrap
    *subprocess
    *random
    *mpl_toolkits

To install biosim via pip :
```
    pip install biosim-a36-navneet-sushant
```
Alternatively,you can manually pull this repository and run setup.py:

```
git clone git@gitlab.com:nmbu.no/emner/inf200/h2022/january-block-teams/a36_navneet_sushant/biosim-a36-navneet-sushant.git
cd biosim-a36-navneet-sushant
python setup.py
```

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
To run the simulation:
```
python reference_examples/check_sim.py
```

Simulation Results:
```
reference_examples/results/
```
![](https://gitlab.com/nmbu.no/emner/inf200/h2022/january-block-teams/a36_navneet_sushant/biosim-a36-navneet-sushant/-/blob/main/Exam/sample.gif)



