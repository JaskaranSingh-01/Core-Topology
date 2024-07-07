import pandas as pd
import networkx as nx
from ipysigma import Sigma
from pyvis.network import Network
import os
# from openpyxl import Workbook

# wb = Workbook() # creates a workbook object.
# ws = wb.active # creates a worksheet object.


def type_of_node(node):
    node_type = ""
    for i in node:
        if i>='A' and i<='Z':
            node_type+=i
            # print(i)
        else:
            break
    return node_type


def dfs(node ,edge_list,path_list,x):
    path_list.append(node)
    if 'BTR' in node:
        # ws.append(path_list) # adds values to cells, each list is a new row.
        # wb.save('File_Name.xlsx') # save to excel file.
        x.append(path_list[:])
    for adjNode in edge_list[node]:
        if adjNode not in path_list:
            dfs(adjNode,edge_list,path_list,x)
    path_list.pop()



def get_all_paths(src,edge_list):
    x = []
    path_list =[]
    dfs(src,edge_list,path_list,x)
    return x

def get_ideal_path(invalid_node,paths):
    x = []
    for item in paths:
        if invalid_node not in item:
            x.append(item)
            break
    return x


def get_data(file):

    df = pd.read_excel(file,engine='openpyxl')
    columns_to_drop = ['Nom Lien IP', 'Site Geo A','Adresse IP A', 'Nom Interface A', 'Site Geo B', 'Adresse IP B', 'Remarks']
    df = df.drop(columns=columns_to_drop)
    df.drop_duplicates()

    edge_list = {}
    source_list = []

    lookup = {
        'XNB' : 'CSG',
        'CSG' : 'CTR',
        'CTR' : 'OAR',
        'OAR' : 'BTR',
        'BTR' : '1'
    }
    
    # Creating adjacency list for each node
    for idx,row in df.iterrows():
        if row['Classe Equipement A'] =='XNB':
            source_list.append(row['Equipement A'])
        if row['Classe Equipement B'] =='XNB':
            source_list.append(row['Equipement B'])

        if row['Classe Equipement A'] not in lookup:
            continue
        if row['Classe Equipement B'] not in lookup:
            continue
        if row['Equipement A'] not in edge_list:
            edge_list[row['Equipement A']] = []
            if row['Classe Equipement B'] == lookup[row['Classe Equipement A']] or row['Classe Equipement A'] == row['Classe Equipement B']:
                edge_list[row['Equipement A']].append(row['Equipement B'])
        else:
            if row['Classe Equipement B'] == lookup[row['Classe Equipement A']] or row['Classe Equipement A'] == row['Classe Equipement B']:
                edge_list[row['Equipement A']].append(row['Equipement B'])

        if row['Equipement B'] not in edge_list:
            edge_list[row['Equipement B']] = []
            if row['Classe Equipement A'] == lookup[row['Classe Equipement B']] or row['Classe Equipement A'] == row['Classe Equipement B']:
                edge_list[row['Equipement B']].append(row['Equipement A'])
        else:
            if row['Classe Equipement A'] == lookup[row['Classe Equipement B']] or row['Classe Equipement A'] == row['Classe Equipement B']:
                edge_list[row['Equipement B']].append(row['Equipement A'])


    for k,v in edge_list.items():
        edge_list[k] = list(set(v))
        similar_nodes = []
        different_nodes = []
        for node in edge_list[k]:
            type_of_key = type_of_node(k)
            type_of_node_in_path= type_of_node(node)
            if type_of_node_in_path == type_of_key:
                similar_nodes.append(node)
            else:
                different_nodes.append(node)
        edge_list[k] = []
        for node in different_nodes:
            edge_list[k].append(node)
        for node in similar_nodes:
            edge_list[k].append(node)
    return edge_list
    # cnt=0
    # for i in source_list:
    #     cnt+=1
    #     print(i)
    #     if(cnt==10):
    #         break
    #     dfs(i,edge_list,pl)

def draw_paths(paths):
    G=nx.MultiDiGraph()
    def format_attributes(data_dict):
        formatted_string = ""
        for key, value in data_dict.items():
            if key=='value':
                formatted_string += f"{'source'}: {value}\n"
            else:
                formatted_string += f"{key}: {value}\n"
        return formatted_string
    color_table = [
        "AliceBlue",
        "AntiqueWhite",
        "Aqua",
        "Aquamarine",
        "Azure",
        "Beige",
        "Bisque",
        "Black",
        "BlanchedAlmond",
        "Blue",
        "BlueViolet",
        "Brown",
        "BurlyWood",
        "CadetBlue",
        "Chartreuse",
        "Chocolate",
        "Coral",
        "CornflowerBlue",
        "Cornsilk",
        "Crimson",
        "Cyan",
        "DarkBlue",
        "DarkCyan",
        "DarkGoldenRod",
        "DarkGray",
        "DarkGreen",
        "DarkKhaki",
        "DarkMagenta",
        "DarkOliveGreen",
        "DarkOrange",
        "DarkOrchid",
        "DarkRed",
        "DarkSalmon",
        "DarkSeaGreen",
        "DarkSlateBlue",
        "DarkSlateGray",
        "DarkTurquoise",
        "DarkViolet",
        "DeepPink",
        "DeepSkyBlue",
        "DimGray",
        "DodgerBlue",
        "FireBrick",
        "FloralWhite",
        "ForestGreen",
        "Fuchsia",
        "Gainsboro",
        "GhostWhite",
        "Gold",
        "GoldenRod"
    ]
    for i in range(len(paths)):
        parent = 'src'
        # print(paths[i])
        for node in paths[i]:
            G.add_node(node)
            if parent != 'src':
                G.add_edge(parent,node,title = i,color=color_table[i%50],Path_Number = i)
            parent = node
    G = nx.relabel_nodes(G, {n: str(n) for n in G.nodes()})
    nt = Network(height="1500px", width="100%",bgcolor="#222222", font_color="white", directed=True, notebook=True, filter_menu=True, cdn_resources='remote')
    nt.from_nx(G)
    nt.force_atlas_2based(gravity=-18950,central_gravity=2.0,spring_length=200,spring_strength=0.5,damping=0.75,overlap=0.5)
    nt.set_edge_smooth('dynamic')
    # Show additional buttons for physics and interaction (optional)
    nt.show_buttons(filter_=['physics', 'interaction'])
    # Generate and save the HTML file
    html_file_path = './templates/non_display_files/bytellldp.html'
    if os.path.exists(html_file_path):
        # Delete the file if it exists
        os.remove(html_file_path)
    # Write the HTML file
    nt.write_html(html_file_path)
    
    
def draw_paths2(paths):
    G=nx.MultiDiGraph()

    for i in range(len(paths)):
        parent = 'src'
        # print(paths[i])
        cnt=0
        for node in paths[i]:
            if cnt==0:
                G.add_node(node,color = 'green')
            elif cnt == len(paths[i])-1:
                G.add_node(node,color = 'red')
            else:
                G.add_node(node)
            if parent != 'src':
                if G.has_edge(parent,node) == False:
                    G.add_edge(parent,node,color="lightblue")
            parent = node
            cnt+=1
    G = nx.relabel_nodes(G, {n: str(n) for n in G.nodes()})
    nt = Network(height="1500px", width="100%",bgcolor="#222222", font_color="white", directed=True, notebook=True, filter_menu=True, cdn_resources='remote')
    nt.from_nx(G)
    nt.force_atlas_2based(gravity=-18950,central_gravity=2.0,spring_length=200,spring_strength=0.5,damping=0.75,overlap=0.5)
    nt.set_edge_smooth('dynamic')
    # Show additional buttons for physics and interaction (optional)
    nt.show_buttons(filter_=['physics', 'interaction'])
    # Generate and save the HTML file
    html_file_path = './templates/non_display_files/bytellldp.html'
    if os.path.exists(html_file_path):
        # Delete the file if it exists
        os.remove(html_file_path)
    # Write the HTML file
    nt.write_html(html_file_path)    