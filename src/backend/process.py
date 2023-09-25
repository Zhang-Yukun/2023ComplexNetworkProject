from src.backend.parser.parser import parse_novel_text
import os
current_path = os.path.dirname(__file__)
def parse_novel(label):
    parse_novel_text(label)


def process_csv(file, label):
    names = []
    with open(file, 'r', encoding='utf8') as f:
        for ed in f.readlines()[1:]:
            ed = ed.split(",")
            n1 = ed[0].strip()
            n2 = ed[1].strip()
            if n1 not in names:
                names.append(n1)
            if n2 not in names:
                names.append(n2)
    with open(current_path+ "/data/parsed/" + label + "/names.txt", 'w',encoding='utf8') as f:
        for name in names:
            f.write(name + "\n")
    pairs = {}
    with open(file, 'r',encoding='utf8') as f:
        for ed in f.readlines()[1:]:
            ed = ed.split(",")
            n1 = ed[1].strip() if ed[0].strip() > ed[1].strip() else ed[0].strip()
            n2 = ed[0].strip() if ed[0].strip() > ed[1].strip() else ed[1].strip()
            if (n1, n2) not in pairs:
                pairs[(n1, n2)] = 0.0
            pairs[(n1, n2)] += float(ed[2].strip())
    with open(current_path + "/data/parsed/" + label + '/edges.txt', 'w',encoding='utf8') as f:
        for (e1, e2), weight in pairs.items():
            f.write("{};{};{}\n".format(e1, e2, weight))


def generate_novel_graph(label):
    parse_novel(label)
    process_csv("backend/data/parsed/{}/{}.csv".format(label, label), label)

current_path = os.path.dirname(__file__)
paths = current_path+ "/data/parsed/rail/rail.csv"
label = "rail"
process_csv(paths, label)