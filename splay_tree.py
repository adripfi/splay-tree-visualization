from tkinter import *
import random

class Node:
    def __init__(self, key, data=None, left=None, right=None, p=None):
        self.key = key
        self.left = left
        self.right = right
        self.p = p
        self.data = data


class SplayTree:
    def __init__(self, key, data=None):
        self.root = Node(int(key), data)

    def getnodelevels(self):
        # create empty node as placeholder for missing children
        emptynode = Node(None, None, None, None)
        returnlevel= [[self.root]]
        stack = [self.root]
        whilelist = [emptynode]
        # create list with nodes on each level by adding children of node to level list, starting from root
        # children are added to "stack" and are porecessed the same way in next iteration
        # If there is a missing child the placeholder node "emptynode" is added, otherwise there wont be a Node on the
        # next level because "None" Type hast no childen
        while whilelist:
            level =[]
            for elem in stack:
                if elem.left:
                    level.append(elem.left)
                else:
                    level.append(emptynode)
                if elem.right:
                    level.append(elem.right)
                else:
                    level.append(emptynode)
            # check if there are "real" children left
            whilelist = [c for c in level if c.key]
            if whilelist:
                returnlevel.append(level)
            stack = level
        return returnlevel

    # draw nodes on canvas object c
    def draw(self, c, xoffset=0):
        if xoffset != 0:
            xoffset -= 10
        levelednodes = self.getnodelevels()
        x_first_node = 20
        x_gap = 40
        for i in range(len(levelednodes)-1,-1,-1):
            y = i * 60 + 10
            x = x_first_node
            for elem in levelednodes[i]:
                if elem.key:
                    self.create_node(elem, x-xoffset, y, c)
                    elem.bottomdock = [x-xoffset, y+40]
                    elem.topdock = [x-xoffset, y]
                x += x_gap
            x_first_node = x_first_node + x_gap/2
            x_gap *= 2
        self.create_lines(c)

    def create_lines(self,c):
        nodes = self.find_nodes()
        for elem in nodes:
            if elem.p:
                c.create_line(elem.topdock[0], elem.topdock[1], elem.p.bottomdock[0], elem.p.bottomdock[1], fill="grey77")

    # create node, x, y are top left corner coord. of node
    def create_node(self,node,x,y,c):
        c.create_oval(x-20,y,x+20,y+40, outline="grey77", width=1)
        c.create_text(x, y+20, text=str(node.key), fill="grey77")

    def search(self, key):
        # start search at root
        x = self.root
        while x and int(key) != int(x.key):
            a = x
            if int(key) < int(x.key):
                x = x.left
            else:
                x = x.right
        if not x:
            self.Splay(a)
            return None
        else:
            self.Splay(x)
            return x
        # key was found, splay and return node


    def insert(self, key, data=None):
        node = Node(int(key), data)
        y = None
        x = self.root
        # find place of inserted node by comparing its key
        while x:
            y = x
            if int(key) < int(x.key):
                x = x.left
            else:
                x = x.right
        # found node to attach inserted node, decide wether node goes left or right
        node.p = y
        if not y:

            self.root = node
        elif int(key) < int(y.key):
            y.left = node
        else:
            y.right = node
        # Splay Node
        self.Splay(node)


    def delete(self, key):
        z = self.search(int(key))
        # If Tree only contains one Node, raise Error
        if not self.root or (not self.root.left and not self.root.right):
            return
        # If Tree contains Node, Node is now root, delete root and find predecesor
        if not z:
            return None
        if self.root.key == int(key):
            if not z.left:
                self.transplant(z, z.right)
            elif not z.right:
                self.transplant(z, z.left)
            else:
                y = self.treemin(z.right)
                if y.p != z:
                    self.transplant(y, y.right)
                    y.right = z.right
                    y.right.p = y
                self.transplant(z, y)
                y.left = z.left
                y.left.p = y
        else:
            return None

    # treemin method from lecture,
    def treemin(self, x):
        while x.left:
            x = x.left
        return x

    # transplant method from lecture
    def transplant(self, u, v):
        if not u.p:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        if v:
            v.p = u.p

    # Rotation Algorithm taken from lecture
    def rotleft(self, x):
        self.root.p = None
        y = x.right
        if not x.p:
            self.root = y
        elif x.p.left == x:
            x.p.left = y
        else:
            x.p.right = y
        y.p = x.p
        x.right = y.left
        if x.right:
            x.right.p = x
        y.left = x
        x.p = y

    def rotright(self, x):
        self.root.p = None
        y = x.left
        if not x.p:
            self.root = y
        elif x.p.left == x:
            x.p.left = y
        else:
            x.p.right = y
        y.p = x.p
        x.left = y.right
        if x.left:
            x.left.p = x
        y.right = x
        x.p = y

    # Calculate Node Potential
    def nodepot_rek(self, nodeobj):
        nodes = self.find_nodes(nodeobj)
        return len(nodes)

    def find_nodes(self, nodeobj=0):
        if nodeobj == 0:
            nodeobj = self.root
        stack = [nodeobj]
        visited = []
        while stack:
            nodeobj = stack.pop(-1)
            if nodeobj not in visited:
                if not nodeobj.right and not nodeobj.left:
                    pass
                elif nodeobj.right and not nodeobj.left:
                    stack.append(nodeobj.right)
                elif nodeobj.left and not nodeobj.right:
                    stack.append(nodeobj.left)
                else:
                    stack.append(nodeobj.left)
                    stack.append(nodeobj.right)
            visited.append(nodeobj)
        return visited

    def treepot_rek(self):
        nodes = self.find_nodes()
        treep = 1
        while nodes:
            treep *= self.nodepot_rek(nodes.pop(-1))
        return treep


    def Splay(self, x):
        self.root.p = None
        print("Splay an Knoten", x.key)
        # calculate start potential, nodepotential and rootpotential
        potential_start = self.treepot_rek()
        nodepot = self.nodepot_rek(x)
        rootpot = self.nodepot_rek(self.root)
        # rotate node x until x is root, count rotations
        rotations = 0
        while x.p:
            self.root.p = None
            rotations += self.SplayStep(x)
        # calculate epotential after splay then calculate and print all paramters
        potential_end = self.treepot_rek()
        print("2^Rotationen: " + str(2 ** rotations))
        print("2^Potential vorher: " + str(potential_start))
        print("2^Potential nachher: " + str(potential_end))
        print("2^amortisierte Rotationen: " + str((2**rotations*potential_end)) + "/" + str(potential_start))
        print("2^obere Schranke: " + str(2 * (rootpot ** 3)) + "/" + str(nodepot ** 3))


    # SplayStep Algorithm taken from lecture
    def SplayStep(self, x):
        self.root.p = None
        if not x.p:
            return 0
        # 1a Zick
        elif not x.p.p and x == x.p.left:
            self.rotright(x.p)
            return 1
        # 1b Zick
        elif not x.p.p and x == x.p.right:
            self.rotleft(x.p)
            return 1
        # Fall 2a Zick Zick
        elif x == x.p.left and x.p == x.p.p.left:
            self.rotright(x.p.p)
            self.rotright(x.p)
            return 2
        # Fall 2b Zick Zick
        elif x == x.p.right and x.p == x.p.p.right:
            self.rotleft(x.p.p)
            self.rotleft(x.p)
            return 2
        # Fall 3a Zick Zack
        elif x == x.p.left and x.p == x.p.p.right:
            self.rotright(x.p)
            # ????? evtl fehler
            self.rotleft(x.p)
            return 2
        # Fall 3b Zick Zack
        else:
            self.rotleft(x.p)
            # ????? evtl fehler
            self.rotright(x.p)
            return 2


class TreeVisualizer:
    # constructor prints window for creating graph root
    def __init__(self, root):
        self.tree = False
        # setup tkinter
        root.configure(background='grey17')
        self.root = root
        # create frames for placing buttons and entry fields
        topframekey = Frame(root, background='grey17')
        topframekey.pack(side=TOP)

        topframedata = Frame(root, background='grey17')
        topframedata.pack(side=TOP)

        self.canvas_frame = Frame(root, background='grey17')
        self.canvas_frame.pack(side=BOTTOM)

        self.button_frame = Frame(root, background='grey17')
        self.button_frame.pack(side=BOTTOM)

        # Create Labels for entry fields
        self.label1 = Label(topframekey, text='Key  ', background='grey17', fg='grey77')
        self.label1.pack(side='left')
        self.label2 = Label(topframedata, text='Data', background='grey17', fg='grey77')
        self.label2.pack(side='left')

        # Create entry field for key and node data
        self.keyfield = Entry(topframekey, highlightbackground='grey17', highlightcolor='grey77')
        self.datafield = Entry(topframedata, highlightbackground='grey17', highlightcolor='grey77')
        self.keyfield.pack(side="left")
        self.datafield.pack(side="left")

        # create "construct" button, which creates canvas with root node
        self.first_button = Button(self.button_frame, text='construct', command=self.constructtree)
        self.first_button.configure(highlightbackground='grey17', highlightcolor='grey77', bg='grey77')
        self.first_button.pack(side='left')

    # Cunstruct Tree for the first time and display GUI for inserting, deleting and searching nodes
    def constructtree(self):
        # create SplayTree Object and displaying Tree by calling "draw" method
        self.tree = SplayTree(self.keyfield.get(), self.datafield.get())
        self.w = Canvas(self.canvas_frame, width=1400, height=770, highlightthickness=0, name='canvas')
        self.w.configure(background='grey17')
        self.tree.draw(self.w)
        self.w.pack(side='bottom')

        # Create insert, delete and search button which call corelated methods
        self.first_button.configure(text='insert', command=self.insert)
        self.second_button = Button(self.button_frame, text='search', command=self.search)
        self.second_button.configure(highlightbackground='grey17', highlightcolor='grey77', bg='grey77')
        self.second_button.pack(side='left')
        self.second_button = Button(self.button_frame, text='delete', command=self.delete)
        self.second_button.configure(highlightbackground='grey17', highlightcolor='grey77', bg='grey77')
        self.second_button.pack(side='left')
        self.second_button = Button(self.button_frame, text='Calc. Pot.', command=self.calcnodepot)
        self.second_button.configure(highlightbackground='grey17', highlightcolor='grey77', bg='grey77')
        self.second_button.pack(side='left')

    # search node with given key and update tree
    def search(self):
        self.tree.search(self.keyfield.get())
        self.upadte_canvas()

    # insert node with given key, data and update tree
    def insert(self):
        self.tree.insert(self.keyfield.get(), self.datafield.get())
        self.upadte_canvas()

    # delete node with given key and update tree
    def delete(self):
        self.tree.delete(self.keyfield.get())
        self.upadte_canvas()

    # delete outdated canvas and update canvas with new tree
    def upadte_canvas(self):
        self.w.destroy()
        self.w = Canvas(self.canvas_frame, width=1400, height=770, highlightthickness=0, name='canvas')
        self.w.configure(background='grey17')
        self.tree.draw(self.w)
        cordinates = []
        for elem in self.w.find_all():
            cordinates.append(self.w.bbox(elem)[0])
        self.w.delete("all")
        self.tree.draw(self.w, min(cordinates))
        self.w.pack()
        self.w.pack(side='bottom')

    def calcnodepot(self):
        nodes = self.tree.find_nodes()
        key = self.keyfield.get()
        for elem in nodes:
            if elem.key == key:
                print("Potential of", str(key)+":", self.tree.nodepot_rek(elem))



#                   TEST AREA
###############################
def show_nodes(tree):
    nodes = tree.find_nodes()
    for elem in nodes:
        print("Key:", elem.key, end='')
        if elem.left:
            print(" l:", elem.left.key, end='')
        else:
            print(" l:", "N",  end='')
        if elem.right:
            print(" r:", elem.right.key,  end='')
        else:
            print(" r:", "N",  end='')
        if elem.p:
            print(" p:", elem.p.key)
        else:
            print(" p:", "N")
"""

root = Tk()
a = TreeVisualizer(root)
root.mainloop()


# Svens Test Corner
print("\nloeschen eines nicht vorh. keys")
T.delete(420)
print("suchen eines nicht vorh. keys")
print(T.search(420))
print("suchen eines vorhandenen keys")
print(T.search(10).key)

root = Tk()
a = TreeVisualizer(root)
root.mainloop()

# delete funktion nach vl folien
#ii) insert: 6, 9
#   delete: 9

#iii) a) insert: 2, 9, 6, 5
#        delete: 5
#     b) insert: 7 6 2 9 5
#        delete : 5
10

"""

root = Tk()
a = TreeVisualizer(root)
root.mainloop()

