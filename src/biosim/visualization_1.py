import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import random
from src.biosim.map import Map

class Plotting:

    def __init__(self, island_map, cmax=None, ymax=None, hist_specs=None):
        self.island = Map(island_map)
        self.img_base = None
        self.img_ctr = 0

        self.y_herb = None
        self.y_carn = None
        self.herb_line = None
        self.carn_line = None
        self.herb_fitness_list = None
        self.carn_fitness_list = None
        self.ax_main = None
        self.ax_weight = None
        self.ax_fitness = None
        self.ax_age = None
        self.weight_hist = None
        self.fitness_hist = None
        self.age_hist = None
        self.axhm_herb = None
        self.imax_herb = None
        self.axhm_carn = None
        self.imax_carn = None
        self.ax_im = None
        self.ax_lg = None

        self.ymax = ymax
        self.cmax = cmax

        if self.cmax is None:
            self.cmax = {"Herbivore": 200, "Carnivore": 50}

        self.cmax_herb = self.cmax["Herbivore"]
        self.cmax_carn = self.cmax["Carnivore"]

        if hist_specs is None:
            self.hist_specs = {
                "weight": {"max": 80, "delta": 2},
                "fitness": {"max": 1.0, "delta": 0.05},
                "age": {"max": 80, "delta": 2},
            }
        else:
            self.hist_specs = hist_specs

        self.ax_carn=None
    def plot_map(self, island_str,total_years=0):

        """Author: Hans E. Plasser
        :param map_str: Multi-line string containing letters symbolizing the landscape
        :type map_str: str
        """
        rgb_value = {
            "W": (0.0, 0.0, 1.0),  # blue
            "L": (0.0, 0.6, 0.0),  # dark green
            "H": (0.5, 1.0, 0.5),  # light green
            "D": (1.0, 1.0, 0.5),  # light yellow
        }

        plot_rgb = [[rgb_value[column] for column in row.strip()] for row in island_str.splitlines()]

        fig = plt.figure(constrained_layout=True)

        gs = GridSpec(3,3,figure=fig)

        self.ax_im = fig.add_subplot(gs[0,0])
        self.axt=fig.add_subplot(gs[0,1])
        self.ax_carn = fig.add_subplot(gs[0,-1])
        self.ax_hm_herb = fig.add_subplot(gs[1,0])
        self.ax_hm_carn = fig.add_subplot(gs[1,-1])
        self.ax_fitness = fig.add_subplot(gs[-1,0])
        self.ax_age=fig.add_subplot(gs[-1,1])
        self.ax_weight=fig.add_subplot(gs[-1,-1])



        # self.ax5 = fig.add_subplot(2, 3, 6)


        #self.ax_im = fig.add_axes([0.05, 0.2, 0.6, 0.6])  # llx, lly, w, h

        self.ax_im.imshow(plot_rgb)
        self.ax_im.set_xticks(range(len(plot_rgb[0])))
        self.ax_im.set_xticklabels(range(1, 1 + len(plot_rgb[0])))

        self.ax_im.set_yticks(range(len(plot_rgb)))
        self.ax_im.set_yticklabels(range(1, 1 + len(plot_rgb)))

        self.ax_im.axis("off") #for removing the axes coordinates
        for label in self.ax_im.xaxis.get_ticklabels()[1::28]:
            label.set_visible(False)

        self.ax_lg = fig.add_axes([0.01,0.7, 0.04, 0.4])  # llx, lly, w, h
        self.ax_lg.axis('off') #for removing the axe coordinates

        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            self.ax_lg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                               edgecolor='none',
                                               facecolor=rgb_value[name[0]]))
            self.ax_lg.text(0.35, ix * 0.2, name, transform=self.ax_lg.transAxes)

        num_year=total_years
        self.ax_carn.set_title("Animal Count")
        self.ax_carn.set_xlim(0,num_year)
        self.ax_carn.set_ylim(0,20000)


        self.ax_hm_herb.set_title('Herbivore Distribution')
        self.ax_hm_carn.set_title('Carnivore Distribution')
        self.ax_weight.set_title('Weight')
        self.ax_fitness.set_title('Fitness')
        self.ax_age.set_title('Age')


        step_size=1
        linestyle='b-'
        carn_xdata=np.arange(0,num_year,step_size)
        self.line1 = self.ax_carn.plot(carn_xdata,np.full_like(carn_xdata, np.nan, dtype=float), linestyle)[0]    #for defining the line and its properties for herb
        self.line2 = self.ax_carn.plot(carn_xdata,np.full_like(carn_xdata, np.nan, dtype=float), linestyle,c='r')[0]  #for defining the line and its properties for carn


        #self.axt = fig.add_axes([0.3, 0.82, 0.2, 0.2])  # llx, lly, w, h
        self.axt.axis('off')  # turn off coordinate system
        self.template = 'Year: {:5d}'
        self.txt = self.axt.text(0.5, 0.5, self.template.format(0),horizontalalignment='center',verticalalignment='center',transform=self.axt.transAxes)


    def plot_population(self,pop_herb=0,pop_carn=0,years=0,step_size=1,current_year=0,pop_matrix_herb=None,pop_matrix_carn=None,weight_dict=None,age_dict=None,fitness_dict=None):

        self.txt.set_text(self.template.format(current_year))

        n=current_year
        #print(current_year)
        idx= int(n/step_size)
        #print(idx)
        #self.ax_carn.set_ylim(0,pop_herb+5000)
        ydata=self.line1.get_ydata()#plotting of ydata for herb
        ydata[idx]=pop_herb
        self.line1.set_ydata(ydata)




        y1data=self.line2.get_ydata()#plotting of ydata for carn
        y1data[idx]=pop_carn
        self.line2.set_ydata(y1data)


        #print(ydata)
        plt.pause(0.01)

        self.heatmap_plot_herbivore(pop_matrix_herb=pop_matrix_herb)
        self.heatmap_plot_carnivore(pop_matrix_carn=pop_matrix_carn)

        self.plot_fauna_weight(weight_dict=weight_dict)
        self.plot_fauna_age(age_dict=age_dict)
        self.plot_fauna_fitness(fitness_dict=fitness_dict)


    def close_plot(self):
        plt.close()
    def heatmap_plot_herbivore(self,pop_matrix_herb):
        self.ax_hm_herb.imshow(pop_matrix_herb,cmap='viridis',interpolation='nearest')

    def heatmap_plot_carnivore(self,pop_matrix_carn):
        self.ax_hm_carn.imshow(pop_matrix_carn,cmap='cividis',interpolation='nearest')

    def plot_fauna_weight(self,weight_dict):
        herb_dict=weight_dict['Herbivore']
        carn_dict=weight_dict['Carnivore']
        self.ax_weight.hist(herb_dict,color='b',histtype='step')
        self.ax_weight.hist(carn_dict,color='r',histtype='step')

    def plot_fauna_age(self,age_dict):
        herb_dict=age_dict['Herbivore']
        carn_dict=age_dict['Carnivore']
        self.ax_age.hist(herb_dict,color='b',histtype='step')
        self.ax_age.hist(carn_dict,color='r',histtype='step')

    def plot_fauna_fitness(self,fitness_dict):
        herb_dict=fitness_dict['Herbivore']
        carn_dict=fitness_dict['Carnivore']
        self.ax_fitness.hist(herb_dict,color='b',histtype='step')
        self.ax_fitness.hist(carn_dict,color='r',histtype='step')

    def show_plot(self):
        plt.show()