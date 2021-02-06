from abc import ABC, abstractmethod


class Light:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []
        
    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
    
    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()
    
    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()
        
    def generate_lights(self):
        return self.grid.copy()


class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1 # Источники света
        self.map[5][2] = -1 # Стены
    
    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)
    
    
class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        dim = ()
        dim[1] = len(grid)
        dim[0] = len(grid[0])
        self.adaptee.set_dim(dim)
        lightpos = [()]
        obstaclespos = [()]
        for i in range[dim[1]]:
            for j in range[dim[0]]:
                if grid[i][j] == 1:
                    lightpos.append((j,i))
                elif grid[i][j] == -1:
                    obstaclespos.append((j,i))

        self.adaptee.set_lights(lightpos)
        self.adaptee.set_obstacles(obstaclespos)

        return self.adaptee.generate_lights()

