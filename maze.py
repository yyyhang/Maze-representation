import copy
import sys

class MazeError(Exception):
    def __init__(self,*arg):
        pass

class Maze(object):
    def __init__(self,name):
        self.name = name
        self.number = self.__check_valid()
        if self.number:
            self.__valid_maze()
            self.exit_way = []
            self.cul_de_sacs_points = []
            self.maze_grid = self.__convert_map()
            self.paths = self.__joint_path()
            self.gates_cnt , self.gates_map = self.__gates()
            self.cnt_inner_points , self.cnt_accessible_area , self.cnt_cul_de_sacs, self.cnt_entry_exit, self.points_cul, self.entry_exit_paths = self.__areas()
            self.points_cul = sorted(self.points_cul, key=lambda x:(x[1],x[0]))
            self.entry_exit_paths = sorted(self.entry_exit_paths, key=lambda x:(x[1],x[0]))
        else:
            raise MazeError('Incorrect input.')

    def __aze(self):
        with open(self.name,'r') as f:
            inp_list =[]
            for line in f:
                inp = ''.join(line.split())
                if inp:
                    inp_list.append(inp)
        return inp_list

    def __check_valid(self):
        inp_list = self.__aze()
        lenth_row, lenth_col = len(inp_list[0]), len(inp_list)
        result, number = 1 , []
        if lenth_row >= 2 and lenth_col >= 2:
            for each in inp_list:
                if each.isdigit():
                        number.append([int(x) for x in each if 0 <= int(x) <4])
                else:
                    result = 0
                    break
            if number:
                for each in number:
                    if len(each) != len(number[0]):
                        result = 0
                        break
                if len(number[0]) > 31 or len(number) > 41:
                        result = 0
        return number if result else number.clear()

    def __valid_maze(self):
        value = 1
        for each in self.number:
            if each[-1] == 1 or each[-1] == 3:
                value = 0
                break
        for e in self.number[-1]:
            if e == 2 or e == 3:
                value = 0
                break
        if not value:
            raise MazeError('Input does not represent a maze.')

    def __convert_map(self):
        '''
        To generate the original number to a maze by 1s and 0s
        '''
        holder,row,col = [],[],[]
        for i in self.number:
            for e in i:
                if e == 0:
                    one,two ='30','00'
                    row.append(one)
                    col.append(two)
                elif e == 1:
                    one,two ='11','00'
                    row.append(one)
                    col.append(two)
                elif e == 2:
                    one,two ='10','10'
                    row.append(one)
                    col.append(two)
                elif e == 3:
                    one,two ='11','10'
                    row.append(one)
                    col.append(two)
            holder.append(''.join(row))
            holder.append(''.join(col))
            pol = [[int(x) for x in i] for i in holder]
            row,col = [],[]
        return pol

    def __gates(self):
        '''
        A function return the number of gates and a map marked with all gates as 5
        '''
        gates_map = copy.deepcopy(self.maze_grid)
        first_row, last_row, check_row  = gates_map[0], gates_map[-3], gates_map[-2]
        cnt = 0
        # If the gate has been count, then another point which came from a same number need to be marked as 2
        for x in range(1,len(first_row)-2):   # Start from 1. No need to count last two colunms
            if first_row[x] == 0:
                first_row[x] = 5
                cnt += 1
                if int(x) % 2 == 0:
                    first_row[x+1] = 2
        for x in range(1,len(last_row)-2):    #  Start from 1. No need to count last two colunms
            if last_row[x] == 0 and check_row[x] == 0:
                last_row[x] = 5
                cnt += 1
                if int(x) % 2 == 0:
                    last_row[x+1] = 2
        for y in range(1,len(gates_map)-2):   # Start from 1. No need to count last two rows
            if gates_map[y][0] == 0:
                gates_map[y][0] = 5
                cnt += 1
                if int(y) % 2 == 0:
                    gates_map[y+1][0] = 2
        for y in range(1,len(gates_map)-2):   # Start from 1. No need to count last two rows
            if gates_map[y][-2] == 0:
                gates_map[y][-2] = 5
                cnt += 1
                if int(y) % 2 == 0:
                    gates_map[y+1][-2] = 2
        for i in range(len(gates_map)):        # Change marked 2s back to zero
            for j in range(len(gates_map[i])):
                if gates_map[i][j] == 2:
                    gates_map[i][j] = 3
        return cnt,gates_map

    def __walls(self):
        same_wall, walls = [] , []
        temp_grid = copy.deepcopy(self.maze_grid)
        for x in range(len(temp_grid)):
            for y in range(len(temp_grid[x])):
                holder = []
                if temp_grid[x][y] == 1:
                    temp_grid[x][y] = 0
                    holder.append((x,y))
                    same_wall.append((x,y))
                    while same_wall:
                        point = same_wall[0]
                        r, c = point [0], point [1]
                        same_wall.remove(point)
                        if c - 1 >= 0:  #left
                            if temp_grid[r][c-1] == 1:
                                temp_grid[r][c-1] = 0
                                same_wall.append((r,c-1))
                                holder.append((r,c-1))
                        if c + 2 <= len(temp_grid[x]):  #right
                            if temp_grid[r][c+1] == 1:
                                temp_grid[r][c+1] = 0
                                same_wall.append((r,c+1))
                                holder.append((r,c+1))
                        if r - 1 >= 0:  #up
                            if temp_grid[r-1][c] == 1:
                                temp_grid[r-1][c] = 0
                                same_wall.append((r-1,c))
                                holder.append((r-1,c))
                        if r + 2 <= len(temp_grid): #down
                            if temp_grid[r+1][c] == 1:
                                temp_grid[r+1][c] = 0
                                same_wall.append((r+1,c))
                                holder.append((r+1,c))
                        if c + 2 <= len(temp_grid[x]) and r - 1 >= 0:   # right-up
                            if temp_grid[r-1][c+1] == 1:
                                temp_grid[r-1][c+1] = 0
                                same_wall.append((r-1,c+1))
                                holder.append((r-1,c+1))
                        if r + 2 <= len(temp_grid) and c - 1 >= 0:  #left-down
                            if temp_grid[r+1][c-1] == 1:
                                temp_grid[r+1][c-1] = 0
                                same_wall.append((r+1,c-1))
                                holder.append((r+1,c-1))
                if holder:
                    walls.append(holder)
        return len(walls)

    def __joint_path(self):
        '''
        To return all sets of joint path
        '''
        same_path, paths = [], []
        temp_path = [[x for x in i[0:-1]] for i in copy.deepcopy(self.maze_grid)[0:-2]]
        for x in range(len(temp_path)):
            for y in range(len(temp_path[x])):
                holder = []
                if temp_path[x][y] == 0:
                    temp_path[x][y] = 1
                    holder.append((x,y))
                    same_path.append((x,y))
                    while same_path:
                        point = same_path[0]
                        r, c = point [0], point [1]
                        same_path.remove(point)
                        if c - 1 >= 0:  #left
                            if temp_path[r][c-1] == 0:
                                temp_path[r][c-1] = 1
                                same_path.append((r,c-1))
                                holder.append((r,c-1))
                        if c + 2 <= len(temp_path[x]):  #right
                            if temp_path[r][c+1] == 0:
                                temp_path[r][c+1] = 1
                                same_path.append((r,c+1))
                                holder.append((r,c+1))
                        if r - 1 >= 0:  #up
                            if temp_path[r-1][c] == 0:
                                temp_path[r-1][c] = 1
                                same_path.append((r-1,c))
                                holder.append((r-1,c))
                        if r + 2 <= len(temp_path): # if r + 1 <= len(temp_path): down
                            if temp_path[r+1][c] == 0:
                                temp_path[r+1][c] = 1
                                same_path.append((r+1,c))
                                holder.append((r+1,c))
                if holder:
                    paths.append(holder)
        return paths

    def __areas(self):
        '''
        Counting inaccessible inner points, accessible areas and accessible cul-de-sacs
        '''
        entry_exit_paths, cnt_inner_points, cnt_accessible_area, cnt_entry_exit, cnt_cul_de_sacs= [], 0, 0, 0, 0
        points_cul = set()
        for path in self.paths:
            flag,gates = 0,0
            for point in path:                  # counting the number of gates in one joint path
                x,y = point[0], point[1]
                if self.gates_map[x][y] == 5:
                    gates += 1
            if gates == 0:
                inner_points = self.__end_road(path)
                cnt_inner_points += inner_points
            else:
                cnt_accessible_area += 1
                checker = self.__start_go(path)
                if gates == 2 and self.__if_same_way(): # get the entry-exit path if only have 2 gates
                    cnt_entry_exit += 1
                    entry_exit_paths.append([x for e in self.exit_way for x in e])
                cul_de_sacs = self.__delete_same_points(path)
                divid = self.__joint_cul(cul_de_sacs)
                cnt_cul = len(divid)
                cnt_cul_de_sacs += cnt_cul
                cul_de_sacs = self.__point_cul(cul_de_sacs)
                points_cul = points_cul|cul_de_sacs
        entry_exit_paths = self.__point_exit(entry_exit_paths)
        return cnt_inner_points , cnt_accessible_area , cnt_cul_de_sacs, cnt_entry_exit, points_cul, entry_exit_paths

    def __end_road(self,path):
        '''
        Counting inner points in one closed area
        '''
        temp_path = copy.deepcopy(path)
        cnt_closed_point = 0
        while temp_path:
            point = temp_path[0]
            x, y = point[0], point[1]
            cnt_closed_point += 1
            if x % 2 == 0:
                xone, xtwo = x, x+1  
            else:
                xone, xtwo = x-1, x
            if y % 2 == 0:
                yone, ytwo = y, y+1 
            else:
                yone, ytwo = y-1, y           
            temp_check = [(m,n) for m in [xone,xtwo] for n in [yone,ytwo]]
            for element in path:
                if element in temp_check:
                    temp_path.remove(element)
        return cnt_closed_point

    def __start_go(self,path):
        '''
        for one path, find the start point, and find the entry-exit ways
        ''' 
        checker = set()
        temp_gates_map = copy.deepcopy(self.gates_map)
        self.exit_way.clear()
        for coordinate in path:
            x, y = coordinate[0], coordinate[1]
            point = temp_gates_map[x][y]
            if point == 5:
                path_holder, dirction, flag = [], 'e', 0
                self.__DFS(coordinate,path_holder,temp_gates_map,dirction,checker)
                return checker

    def __DFS(self,coordinate,path_holder,temp_gates_map,dirction,checker):
        '''
        In order to build exit_way list
        ''' 
        x = coordinate[0]
        y = coordinate[1]
        if (temp_gates_map[x][y] == 5 or temp_gates_map[x][y] == -1) and dirction != 'e':
        # if reach to gate or a point has been walked, means it is an exit way
            if temp_gates_map[x][y] == 5:
                path_holder.append(coordinate)
            copy_holder = copy.deepcopy(path_holder)
            self.exit_way.append(copy_holder)
            temp_set = {e for e in copy_holder}
            checker = checker|temp_set
            if temp_gates_map[x][y] == -1:
                return checker
        if (x,y) in checker and temp_gates_map[x][y] != 5: # no need to record the point has been walked
            return checker
        if temp_gates_map[x][y] == 0 or temp_gates_map[x][y] == 5:
            if temp_gates_map[x][y] == 0 :
                temp_gates_map[x][y] = -1
                path_holder.append(coordinate)
            elif dirction == 'e':
                path_holder.append(coordinate)
            if x + 1 <= len(temp_gates_map) - 3 and dirction != 'u': #down
                if temp_gates_map[x+1][y] != 1 and temp_gates_map[x+1][y] != 3:# and (x+1,y) not in checker:
                    new_dirction = 'd'
                    checker = self.__DFS((x+1,y),path_holder,temp_gates_map,new_dirction,checker)
            if y - 1 >= 0 and dirction != 'r':    #left
                if temp_gates_map[x][y-1] != 1 and temp_gates_map[x][y-1] != 3:#  and (x,y-1) not in checker:
                    new_dirction = 'l'
                    checker = self.__DFS((x,y-1),path_holder,temp_gates_map,new_dirction,checker)
            if x - 1 >= 0 and dirction != 'd':    #up
                if temp_gates_map[x-1][y] != 1 and temp_gates_map[x-1][y] != 3:#  and (x-1,y) not in checker:
                    new_dirction = 'u'
                    checker = self.__DFS((x-1,y),path_holder,temp_gates_map,new_dirction,checker)
            if y + 1 <= len(temp_gates_map[x]) - 2 and dirction != 'l': #right
                if temp_gates_map[x][y+1] != 1 and temp_gates_map[x][y+1] != 3:#  and (x,y+1) not in checker:
                    new_dirction = 'r'
                    checker = self.__DFS((x,y+1),path_holder,temp_gates_map,new_dirction,checker)
        if temp_gates_map[x][y] == -1:
            temp_gates_map[x][y] = 0
        if path_holder:
            path_holder.pop()
        return checker

    def __if_same_way(self):
        temp = []
        for i in self.exit_way:
            if i not in temp:
                temp.append(i)
        return True if len(temp) == 1 else False

    def __delete_same_points(self,path):
        '''
        delete some points which are not walked but come from a same number with points in exit_way
        '''
        temp_path = copy.deepcopy(path)
        temp_exit_way = copy.deepcopy(self.exit_way)
        temp_exit_way = list(set(sum(temp_exit_way,[])))
        while temp_exit_way:
            point = temp_exit_way[0]
            x, y = point[0], point[1]
            if x % 2 == 0:
                xone, xtwo = x, x+1  
            else:
                xone, xtwo = x-1, x
            if y % 2 == 0:
                yone, ytwo = y, y+1 
            else:
                yone, ytwo = y-1, y
            temp_check = [(m,n) for m in [xone,xtwo] for n in [yone,ytwo]]
            while temp_check:
                if temp_check[0] in temp_path:
                    temp_path.remove(temp_check[0])
                if temp_check[0] in temp_exit_way:
                    temp_exit_way.remove(temp_check[0])
                temp_check.pop(0)
        return temp_path

    def __joint_cul(self,cul_de_sacs):
        '''
        To divid joint cul_de_sacs in a group for a path
        '''
        t_de = copy.deepcopy(cul_de_sacs)
        divid = []
        while t_de:
            holder = []
            one = t_de[0]
            temp =[one]
            while temp:
                element = temp[0]
                x, y = element[0], element[1]
                if element in t_de:
                    t_de.remove(element)
                holder.append(element)
                checker = [(x,n) for n in [y+1,y-1]] + [(m,y) for m in [x+1,x-1]]
                for point in t_de:
                    if point in checker:
                        temp.append(point)
                temp.pop(0)
            divid.append(holder)
        return divid

    def __point_cul(self,cul_de_sacs):
        temp = set()
        for each in cul_de_sacs:
            r,c = each[0],each[1]
            if c < len(self.gates_map[0]) - 2:
                x, y = c//2, r//2
                temp.add((x,y))
        return temp

    def __point_exit(self,entry_exit_paths):
        temp = set()
        for each in entry_exit_paths:
            for one in each:
                r,c = one[0],one[1]
                if c < len(self.gates_map[0]):
                    x, y = c//2, r//2
                    temp.add((x,y))
        return temp

    def analyse(self):
        walls_cnt = self.__walls()
        if self.gates_cnt == 1:
            print('The maze has a single gate.')
        elif self.gates_cnt > 1:
            print('The maze has %d gates.' % self.gates_cnt)
        else:
            print('The maze has no gate.')
            
        if walls_cnt == 1:
            print('The maze has walls that are all connected.')
        elif walls_cnt > 1:
            print('The maze has %d sets of walls that are all connected.' %walls_cnt)
        else:
            print('The maze has no wall.')

        if self.cnt_inner_points == 1:
            print('The maze has a unique inaccessible inner point.')
        elif self.cnt_inner_points > 1:
            print('The maze has %d inaccessible inner points.' % self.cnt_inner_points)
        else:
            print('The maze has no inaccessible inner point.')

        if self.cnt_accessible_area == 1:
            print('The maze has a unique accessible area.')
        elif self.cnt_accessible_area > 1:
            print('The maze has %d accessible areas.' % self.cnt_accessible_area)
        else:
            print('The maze has no accessible area.')

        if self.cnt_cul_de_sacs == 1:
            print('The maze has accessible cul-de-sacs that are all connected.')
        elif self.cnt_cul_de_sacs > 1:
            print('The maze has %d sets of accessible cul-de-sacs that are all connected.' % self.cnt_cul_de_sacs)
        else:
            print('The maze has no accessible cul-de-sac.')

        if self.cnt_entry_exit == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        elif self.cnt_entry_exit > 1:
            print('The maze has %d entry-exit paths with no intersections not to cul-de-sacs.' % self.cnt_entry_exit)
        else:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')

    def display(self):
        name = self.name[:-3] + 'tex'
        with open(name, 'w') as latex_file:
            latex_file.write('\\documentclass[10pt]{article}\n'
                    '\\usepackage{tikz}\n'
                    '\\usetikzlibrary{shapes.misc}\n'
                    '\\usepackage[margin=0cm]{geometry}\n'
                    '\\pagestyle{empty}\n'
                    '\\tikzstyle{every node}=[cross out, draw, red]\n'
                    '\n'
                    '\\begin{document}\n'
                    '\n'
                    '\\vspace*{\\fill}\n'
                    '\\begin{center}\n'
                    '\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n'
                    '% Walls\n'
                )

            draw = []
            number = self.number
            for r in range(len(number)):
                for c in range(len(number[r])):
                    if number[r][c] == 1 or number[r][c] == 3:
                        draw.append(c)
                        continue
                    if draw:
                        latex_file.write('    \\draw (%d,%d) -- (%d,%d);\n' %(draw[0],r,draw[-1]+1,r))
                    draw.clear()
            for c in range(len(number[0])):
                for r in range(len(number)):
                    if number[r][c] == 2 or number[r][c] == 3:
                        draw.append(r)
                        continue
                    if draw:
                        latex_file.write('    \\draw (%d,%d) -- (%d,%d);\n' %(c,draw[0],c,draw[-1]+1))
                    draw.clear()    

            latex_file.write('% Pillars\n')
            if number[0][0] == 0:
                latex_file.write('    \\fill[green] (0,0) circle(0.2);\n')
            for r in range(len(number)):
                for c in range(len(number[r])):
                    if number[r][c] == 0:
                        if r >= 1 and c >= 1:
                            if (number[r-1][c] == 0 or number[r-1][c] == 1) and (number[r][c-1] == 0 or number[r][c-1] == 2):
                                latex_file.write('    \\fill[green] (%d,%d) circle(0.2);\n' %(c,r))
                        elif r >= 1:
                            if number[r-1][c] == 0 or number[r-1][c] == 1:
                                latex_file.write('    \\fill[green] (%d,%d) circle(0.2);\n' %(c,r))
                        elif c >= 1:
                            if number[r][c-1] == 0 or number[r][c-1] == 2:
                                latex_file.write('    \\fill[green] (%d,%d) circle(0.2);\n' %(c,r))

            latex_file.write('% Inner points in accessible cul-de-sacs\n')
            for i in self.points_cul:
                latex_file.write('    \\node at (%.1f,%.1f) {};\n' %(i[0]+0.5,i[1]+0.5))

            latex_file.write('% Entry-exit paths without intersections\n')
            temp = self.entry_exit_paths[:]
            holder = []
            for e in self.entry_exit_paths:
                x, y = e[0], e[1]
                end = 0
                if (x,y) not in holder:
                    if x == 0 and (number[y][x] == 0 or number[y][x] == 1):
                        start,end = -0.5, 0.5
                    else:
                        start = x + 0.5
                    while (x+1,y) in self.entry_exit_paths and (x+1,y) not in holder and number[y][x+1] != 3 and number[y][x+1] != 2:
                        end = x + 1.5
                        holder.append((x,y))
                        x += 1
                    if end:
                        latex_file.write('    \\draw[dashed, yellow] (%.1f,%.1f) -- (%.1f,%.1f);\n'%(start,y+0.5,end,y+0.5))
            holder.clear()
            for e in sorted(self.entry_exit_paths):
                x, y = e[0], e[1]
                end = 0
                if x < len(number[0])-1 and (x,y) not in holder:
                    if y == 0 and number[y][x] != 1 and number[y][x] != 3:
                        start,end = -0.5, 0.5
                    elif y == len(number)-2 and number[y+1][x] == 0:
                        start,end = y + 0.5, y + 1.5
                    else:
                        start = y + 0.5
                    while (x,y+1) in self.entry_exit_paths and (x,y+1) not in holder and number[y+1][x] != 3 and number[y+1][x] != 1:
                        end = y + 1.5
                        holder.append((x,y+1))
                        y += 1
                    if y == len(number)-2 and number[y+1][x] == 0:
                        end = len(number) - 0.5
                        holder.append((x,y))
                    if end:
                        latex_file.write('    \\draw[dashed, yellow] (%.1f,%.1f) -- (%.1f,%.1f);\n'%(x+0.5,start,x+0.5,end))
            latex_file.write('\\end{tikzpicture}\n'
                    '\\end{center}\n'
                    '\\vspace*{\\fill}\n'
                    '\n'
                    '\\end{document}\n'
                    )
