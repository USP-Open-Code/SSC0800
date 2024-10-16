import copy
import time

class Canvas:
    def __init__(self, DIMENSIONS, PARTICLES):
        self.PARTICLES = PARTICLES
        self.DIMENSIONS = DIMENSIONS
        self.matrix = [[PARTICLES["AIR"] 
                        for y in range(DIMENSIONS[0])] 
                        for x in range(DIMENSIONS[1])]


    def compose_output(self, with_edges=False):
        output = []
        if with_edges:
            output.append("@"*(self.DIMENSIONS[1]+2))

            for line in self.matrix:
                out_line = "@"
                for particle in line:
                    out_line += particle
                out_line += "@"
                output.append(out_line)
            output.append("@"*(self.DIMENSIONS[1]+2))
        else:
            for line in self.matrix:
                out_line = ""
                for particle in line:
                    out_line += particle
                output.append(out_line)
        return output


    def print_canvas(self, current_frame, with_edges=False, txt_output=False):
        current_frame = str(current_frame)
        output_list = self.compose_output(with_edges=with_edges)

        if txt_output:
            with open(txt_output+".txt", "a") as file:
                print("frame:" + current_frame, file=file)
                for line in output_list:
                    print(line, file=file)
        else:
            print("frame:" + current_frame)
            for line in output_list:
                print(line)


    def add(self,  pos, particle):
        self.matrix[pos[0]][pos[1]] = particle
    

    def atualize_physics(self):
        future = copy.deepcopy(self.matrix)
        for x in range(self.DIMENSIONS[1]):
            for y in range(self.DIMENSIONS[0]):
                pos = (x,y)
                if self.matrix[pos[0]][pos[1]] == self.PARTICLES["SAND"]:
                    future = self.run_sand(future,pos)
                if self.matrix[pos[0]][pos[1]] == self.PARTICLES["WATER"]:
                    future = self.run_water(future,pos)
        return future


    def run_sand(self, future, pos):
        directions = [(1,0), (1,-1), (1,1)]
        for dx, dy in directions:
            
            if 0 <= pos[0] + dx < self.DIMENSIONS[1] and 0 <= pos[1] + dy < self.DIMENSIONS[0]:
                try: 
                    running_sand = self.matrix[pos[0]+dx][pos[1]+dy] != self.PARTICLES["SAND"]
                except IndexError: 
                    running_sand = False

                if running_sand:
                    future[pos[0]][pos[1]] = self.matrix[pos[0]+dx][pos[1]+dy]
                    future[pos[0]+dx][pos[1]+dy] = self.matrix[pos[0]][pos[1]]
                    return future
        return future


    def run_water(self, future, pos):
        directions = [(1,0), (1,-1), (1,1), (0,-1), (0,1)]
        for dx, dy in directions:

            if 0 <= pos[0] + dx < self.DIMENSIONS[1] and 0 <= pos[1] + dy < self.DIMENSIONS[0]:
                try: 
                    running_water = self.matrix[pos[0]+dx][pos[1]+dy] == self.PARTICLES["AIR"]
                except IndexError: 
                    running_water = False
                if running_water:
                    if future[pos[0]+dx][pos[1]+dy] == self.PARTICLES["WATER"]:
                        return future
                    future[pos[0]+dx][pos[1]+dy] = self.matrix[pos[0]][pos[1]]
                    future[pos[0]][pos[1]] = self.matrix[pos[0]+dx][pos[1]+dy]
                    return future
        return future


def init():
    DIMENSIONS = [64,32]
    PARTICLES = {"AIR":" ", "SAND": "#", "WATER": "~"}
    canvas = Canvas(DIMENSIONS,PARTICLES)
    total_frames = int(input().strip())
    return canvas, total_frames


def process_input(raw_input):
    list_input = raw_input.split()
    frame = int(list_input[0][:-1])
    pos = (int(list_input[2]), int(list_input[1]))
    particle = list_input[3]
    return frame, pos, particle


def run_frames(canvas, total_frames):
    current_frame = 0
    frame = 0
    finished_inputs = False
    inputs = []

    while True:
        try:
            raw_input = input().strip()
            frame, pos, particle = process_input(raw_input)
            inputs.append(tuple([frame,pos,particle]))
        except EOFError:
            break
    
    i = 0
    while current_frame<total_frames:
        while i<len(inputs) and inputs[i][0] == current_frame:
            canvas.add(inputs[i][1], inputs[i][2])
            i+=1
        else:
            current_frame += 1
            canvas.print_canvas(current_frame)
            canvas.matrix = canvas.atualize_physics()

            time.sleep(.5)


def main():
    canvas, total_frame = init()
    run_frames(canvas, total_frame)

if __name__ == "__main__":
    # rodar com <N>.in como input
    # e.g. 
    # python3 pedro_tonso.py < dados/1.in
    main()