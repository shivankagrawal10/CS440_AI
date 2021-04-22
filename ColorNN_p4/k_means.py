import numpy as np
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits import mplot3d
import plotly.express as px

class k_means:

    def __init__(self, num_clusters : int, original_rbg : np.array):
        self.centroids = [(0,0,0) for i in range(num_clusters)]
        self.centroids_dict = dict()
        self.original_rbg = original_rbg
        self.num_clusters = num_clusters
        for i in range(num_clusters):
            rand = original_rbg[random.randint(0,original_rbg.shape[0]-1),random.randint(0,original_rbg.shape[1]-1),:] 
            self.centroids[i]= (rand[0],rand[1],rand[2])
        self.init_dict()
        self.converge = 0
        self.clustered_rbg = np.zeros(self.original_rbg.shape)

    def run(self):
        print(first.centroids)
        while(True):
            first.partition()
            first.recenter()
            print(first.centroids)
            if(self.converge == 1): break
            #print("continue?")
            #inp = input()
            #if(inp == "no"): break
        #print(self.centroids_dict)
        self.create_clustered_img()
        '''
        #plotly option
        fig = px.scatter_3d(x= first.original_rbg[:,:,0].flatten(),y= first.original_rbg[:,:,1].flatten(), z= first.original_rbg[:,:,2].flatten())#, color='species')
        fig.show()
        '''
        '''
        #matplotlib option
        fig = plt.figure(figsize = (10, 7))
        ax = plt.axes(projection ="3d")
        my_cmap = plt.get_cmap('viridis')
        # Creating plot
        ax.scatter3D(first.original_rbg[:,:,0], first.original_rbg[:,:,1], first.original_rbg[:,:,2], alpha = 0.8,cmap = my_cmap,marker="^")
        plt.title("simple 3D scatter plot")

        # show plot
        plt.show()
        '''

    def init_dict(self):
        self.centroids_dict = dict()
        for i in self.centroids:
            self.centroids_dict[i]=np.empty((0,5))

    def partition(self):
        self.init_dict()
        for i in range(self.original_rbg.shape[0]):
            for j in range(self.original_rbg.shape[1]):
                current_rbg = list(self.original_rbg[i,j,:])
                current_rbg.append(i)
                current_rbg.append(j)
                for k in range(self.num_clusters):
                    current_rbg_dist = self.distance(current_rbg,k)
                    if(k == 0 or current_rbg_dist < min_dist):
                        min_dist = current_rbg_dist
                        min_ind = k
                self.centroids_dict[self.centroids[min_ind]] = np.append(self.centroids_dict[self.centroids[min_ind]], np.array([current_rbg]),axis = 0)
    
    def distance(self, current_coord, centroids_ind):
        distance = 0
        for i in range(3):
            #print(f"{current_coord} and {self.centroids[centroids_ind]}")
            distance += (current_coord[i] - self.centroids[centroids_ind][i])**2
        distance = math.sqrt(distance)
        return distance

    def recenter(self):
        self.centroids = []
        del_key = {}
        same_count = 0
        for key in self.centroids_dict:
            val = self.centroids_dict[key]
            length = len(val[:,0])
            self.centroids.append((round(sum(val[:,0])/length),round(sum(val[:,1])/length),round(sum(val[:,2])/length)))
            if(self.centroids[-1] == key): same_count+=1
            del_key[key] = self.centroids[-1]
        
        for key in del_key:
            self.centroids_dict[del_key[key]] = self.centroids_dict.pop(key) 
            #print(f"removing {key}")
        #    del(self.centroids_dict[key])
        if(same_count > 2): 
            self.converge = 1

    def create_clustered_img(self):
        for color in self.centroids_dict:
            for coordinate in self.centroids_dict[color]:
                for i in range(3):
                    #print(coordinate[3])
                    self.clustered_rbg[int(coordinate[3]),int(coordinate[4]),i] = int(color[i])
        self.clustered_rbg = self.clustered_rbg.astype(int)
        print(self.clustered_rbg)
#img1 = plt.imread('dog.jpg') #[(193, 156, 109), (93, 69, 25), (26, 25, 10), (150, 114, 67), (207, 193, 170)]
img1 = plt.imread('scenery.jpg')
#img1 = plt.imread('mountains.jpg') # [(55, 67, 66), (177, 229, 234), (35, 131, 169), (183, 185, 36), (111, 177, 195)]
print(img1.shape)
first = k_means(5,img1)
first.run()
plt.imshow(first.clustered_rbg)
plt.show()