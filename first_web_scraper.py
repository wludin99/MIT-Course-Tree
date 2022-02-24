import requests
from bs4 import BeautifulSoup
import boolean_alg
import draw_graph

## representation of courses as directed graph with and/or gates
class LogicTree():
    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.taken = {}
        self.taking = {}
        self.reqs = {}

    def add_node(self, node, reqs):
        self.nodes.add(node)
        self.taken[node] = False
        self.taking[node] = False
        self.reqs[node] = reqs

    def add_edge(self, start, end):
        self.edges[start].add(end)

    def add_taken(self, courses):
        for course in courses:
            self.taken[course] = True

    def add_taking(self, classes):
        for course in courses:
            self.taking[courses] = True

    def cantake(self, course):
        prereqs = self.reqs[course]['Prereqs']
        coreqs = self.reqs[course]['Coreqs']
        if prereqs.eval(taken) and coreqs.eval(taken, taking):
            return True
        else:
            return False

    def find_classes(self):
        return [course for course in self.nodes if self.cantake(course)]

    def path_to_class(self, course):
        pass


## build network from courses and prereqs
def build_network(course_elems):
    network = LogicTree()
    for course in course_elems:
        course_number, course_name = course.find('strong').text.lower().split(maxsplit=1)
        ## get reqs
        course_reqs = course.find('span', class_="courseblockprereq").text
        prereqs, coreqs = (None, None)
        try:
            coreqs = course_reqs.split(' Coreq: ')[1]
            prereqs = course_reqs.split(' Coreq: ')[0].split('Prereq: ')[1]
        except:
            prereqs = course_reqs.split(': ')[1]
        prereq_formulas = boolean_alg.sym(prereqs)
        coreq_formulas = boolean_alg.sym(coreqs)

        network.add_node(course_number.strip(), {'Prereqs': prereq_formulas, 'Coreqs': coreq_formulas})

        ##add edges to network
        antecedents = []
        if boolean_alg.tokenize(prereqs) != None:
            antecedents += boolean_alg.tokenize(prereqs)
        if boolean_alg.tokenize(coreqs) != None:
            antecedents += boolean_alg.tokenize(coreqs)
        # print(antecedents)
        edges = [(req, course_number) for req in antecedents if req in network.nodes]
        if 'calculusi' in antecedents:
            edges.append(('18.01', course_number))
        if 'calculusii' in antecedents:
            edges.append(('18.02', course_number))
        network.edges = network.edges.union(set(edges))
    return network


## draw graph from courses
def visualize(network):
    G = draw_graph.build_graph(network.nodes, network.edges)
    draw_graph.draw(G)



if __name__ == '__main__':
    ## get webpage data
    URL = 'http://catalog.mit.edu/subjects/18/'
    page = requests.get(URL)

    ## parse as html and find relevant contents
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id="sc_sccoursedescs")
    course_elems = results.find_all('div', class_='courseblock')

    nw = build_network(course_elems)
    visualize(nw)
