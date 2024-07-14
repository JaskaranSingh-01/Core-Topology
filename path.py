import pandas as pd
import networkx as nx
from ipysigma import Sigma
from pyvis.network import Network
import os
from pelote import tables_to_graph
# from openpyxl import Workbook

# wb = Workbook() # creates a workbook object.
# ws = wb.active # creates a worksheet object.
hex_codes_for_dark_background = [
    "#00FFFF",  # aqua
    "#F5F5DC",  # beige
    "#7FFF00",  # chartreuse
    "#FF7F50",  # coral
    "#00FFFF",  # cyan
    "#FF00FF",  # fuchsia
    "#FFD700",  # gold
    "#FF69B4",  # hotpink
    "#F0E68C",  # khaki
    "#E6E6FA",  # lavender
    "#ADD8E6",  # lightblue
    "#F08080",  # lightcoral
    "#E0FFFF",  # lightcyan
    "#FAFAD2",  # lightgoldenrodyellow
    "#90EE90",  # lightgreen
    "#FFB6C1",  # lightpink
    "#FFA07A",  # lightsalmon
    "#20B2AA",  # lightseagreen
    "#87CEFA",  # lightskyblue
    "#778899",  # lightslategray
    "#B0C4DE",  # lightsteelblue
    "#FFFFE0",  # lightyellow
    "#00FF00",  # lime
    "#32CD32",  # limegreen
    "#FF00FF",  # magenta
    "#F5FFFA",  # mintcream
    "#FFE4E1",  # mistyrose
    "#FFA500",  # orange
    "#EEE8AA",  # palegoldenrod
    "#98FB98",  # palegreen
    "#AFEEEE",  # paleturquoise
    "#DB7093",  # palevioletred
    "#FFDAB9",  # peachpuff
    "#FFC0CB",  # pink
    "#DDA0DD",  # plum
    "#FA8072",  # salmon
    "#FFF5EE",  # seashell
    "#C0C0C0",  # silver
    "#87CEEB",  # skyblue
    "#FFFAFA",  # snow
    "#00FF7F",  # springgreen
    "#D8BFD8",  # thistle
    "#FF6347",  # tomato
    "#40E0D0",  # turquoise
    "#F5DEB3",  # wheat
    "#FFFFFF",  # white
    "#F5F5F5",  # whitesmoke
    "#FFFF00"   # yellow
]

hex_codes_for_light_background = [
    "#A52A2A",  # brown
    "#0000FF",  # blue
    "#5F9EA0",  # cadetblue
    "#D2691E",  # chocolate
    "#DC143C",  # crimson
    "#00008B",  # darkblue
    "#008B8B",  # darkcyan
    "#B8860B",  # darkgoldenrod
    "#006400",  # darkgreen
    "#8B008B",  # darkmagenta
    "#556B2F",  # darkolivegreen
    "#FF8C00",  # darkorange
    "#9932CC",  # darkorchid
    "#8B0000",  # darkred
    "#E9967A",  # darksalmon
    "#8FBC8F",  # darkseagreen
    "#483D8B",  # darkslateblue
    "#2F4F4F",  # darkslategray
    "#00CED1",  # darkturquoise
    "#9400D3",  # darkviolet
    "#FF1493",  # deeppink
    "#00BFFF",  # deepskyblue
    "#696969",  # dimgray
    "#1E90FF",  # dodgerblue
    "#B22222",  # firebrick
    "#228B22",  # forestgreen
    "#CD5C5C",  # indianred
    "#4B0082",  # indigo
    "#800000",  # maroon
    "#0000CD",  # mediumblue
    "#000000",  # black
    "#BA55D3",  # mediumorchid
    "#9370DB",  # mediumpurple
    "#3CB371",  # mediumseagreen
    "#7B68EE",  # mediumslateblue
    "#00FA9A",  # mediumspringgreen
    "#48D1CC",  # mediumturquoise
    "#C71585",  # mediumvioletred
    "#191970",  # midnightblue
    "#000080",  # navy
    "#808000",  # olive
    "#6B8E23",  # olivedrab
    "#FF4500",  # orangered
    "#800080",  # purple
    "#663399",  # rebeccapurple
    "#FF0000",  # red
    "#4169E1",  # royalblue
    "#8B4513",  # saddlebrown
    "#A0522D",  # sienna
    "#6A5ACD",  # slateblue
    "#708090",  # slategray
    "#4682B4",  # steelblue
    "#008080",  # teal
    "#EE82EE",  # violet
    "#9ACD32"   # yellowgreen
]

all_col =  hex_codes_for_light_background + hex_codes_for_dark_background

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
            x.append(item[:])
            print(x)
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

    critical_nodes = []
    for k,v in edge_list.items():
        edge_list[k] = list(set(v))
        edge_list[k].sort()
        similar_nodes = []
        different_nodes = []
        for node in edge_list[k]:
            type_of_key = type_of_node(k)
            type_of_node_in_path= type_of_node(node)
            if type_of_node_in_path == type_of_key:
                similar_nodes.append(node)
            else:
                different_nodes.append(node)
        if len(different_nodes) < 2:
            critical_nodes.append(k)
        edge_list[k] = []
        for node in different_nodes:
            edge_list[k].append(node)
        for node in similar_nodes:
            edge_list[k].append(node)
    return edge_list,critical_nodes
    # cnt=0
    # for i in source_list:
    #     cnt+=1
    #     print(i)
    #     if(cnt==10):
    #         break
    #     dfs(i,edge_list,pl)

def draw_paths_nx(paths,critical_nodes):
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
                if node in critical_nodes:
                    G.add_node(node,color = 'Gold')
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
    html_file_path = './templates/non_display_files/a.html'
    if os.path.exists(html_file_path):
        # Delete the file if it exists
        os.remove(html_file_path)
    # Write the HTML file
    nt.write_html(html_file_path)

def draw_paths_ipy(paths,critical_nodes):
    G=nx.MultiDiGraph()

    table_nodes = []
    table_edges = []
    
    for i in range(len(paths)):
        parent = 'src'
        # print(paths[i])
        cnt=0
        for node in paths[i]:
            if cnt==0:
                node_data = {
                    "Node": node,
                    "col" :'green'
                }
                table_nodes.append(node_data)
            elif cnt == len(paths[i])-1:
                node_data = {
                    "Node": node,
                    "col" :'red'
                }
                table_nodes.append(node_data)
            else:
                if node in critical_nodes:
                    node_data = {
                    "Node": node,
                    "col" :'Gold'
                    }
                    table_nodes.append(node_data)
                else:
                    node_data = {
                    "Node": node,
                    "col" :'blue'
                    }
                    table_nodes.append(node_data)
            if parent != 'src':
                if G.has_edge(parent,node) == False:
                    edge_data = {
                        'source':parent,
                        'target':node
                    }
                    table_edges.append(edge_data)
            parent = node
            cnt+=1
    g = tables_to_graph(table_nodes, table_edges, node_col="Node", node_data=["Node",'col'], edge_data=['source', 'target'], directed=True)
    Sigma.write_html(g,'./templates/non_display_files/a.html',fullscreen=True,clickable_edges=True,node_size=g.degree,node_color='col')

def draw_ipy_graph(source,destination,df,selected_columns,filename,col_node,col_edge):
    
    g = nx.MultiDiGraph()
    edge_label = []
    for idx in range(len(selected_columns)):
        edge_label.append(selected_columns[idx])
    table_nodes = []
    table_edges = []
    dataOfEdges = ['source', 'target','color']
    for i in range(len(selected_columns)):
        dataOfEdges.append(selected_columns[i])
    for idx, row in df.iterrows():
        if col_node == 'Default':
            node_data = {
                "Node": row[source],
                'col' : 'Default'
            }
        else:
            node_data = {
                "Node": row[source],
                'col' : row[col_node]
            }
        table_nodes.append(node_data)
        if col_node == 'Default':
            node_data = {
                "Node": row[destination],
                'col' : 'Default'
            }
        else:
            node_data = {
            "Node": row[destination],
            'col': row[col_node]
            }
        
        table_nodes.append(node_data)
        
        if col_edge == 'Default':
            edge_data = {
            'source': row[source],
            'target': row[destination],
            'color': 'Default'
            }
        else:
            edge_data = {
            'source': row[source],
            'target': row[destination],
            'color': row[col_edge]
            }
        
        for i in range(len(selected_columns)):
            edge_data[selected_columns[i]] = row[selected_columns[i]]
        table_edges.append(edge_data)
        
    g = tables_to_graph(table_nodes, table_edges, node_col="Node", node_data=["Node",'col'], edge_data=dataOfEdges, directed=True)
    Sigma.write_html(g, './templates/non_display_files/a.html', fullscreen=True, clickable_edges=True, node_size=g.degree, node_color='col', edge_color='color')

def format_attributes(data_dict):
        formatted_string = ""
        for key, value in data_dict.items():
            if key=='value':
                formatted_string += f"{'source'}: {value}\n"
            else:
                formatted_string += f"{key}: {value}\n"
        return formatted_string

def draw_nx_graph(source,destination,df,selected_columns,filename,col_node,col_edge):
    G = nx.MultiDiGraph()
    lookup_light_edge = {}
    lookup_light_node = {}
    ec=[]
    lc=[]
    lookup_light_edge['Default'] = 'lightblue' 
    lookup_light_node['Default'] = 'red' 
    if col_edge!="Default":
        ec  = list(set(df[col_edge]))
    if col_node!="Default":
        lc = list(set(df[col_node]))
    for i in range(len(ec)):
        lookup_light_edge[ec[i]]=hex_codes_for_dark_background[i%len(hex_codes_for_dark_background)];
    for i in range(len(lc)):
        lookup_light_node[lc[i]]=all_col[i%len(all_col)];
    # edge_label = []
    # for idx in range(len(selected_columns)):
    #     edge_label.append(selected_columns[idx])
    # table_nodes = []
    # table_edges = []
    attribute_columns = []
    for i in range(len(selected_columns)):
        attribute_columns.append(selected_columns[i])
    for idx, row in df.iterrows():
        src_name = row[source]
        dest_name = row[destination]
        if col_node=="Default":
            G.add_node(src_name)
            G.add_node(dest_name)
        else:
            G.add_node(src_name,color_node = row[col_node],color = lookup_light_node[row[col_node]])
            G.add_node(dest_name,color_node = row[col_node],color = lookup_light_node[row[col_node]])

        attributes = {col: row[col] for col in attribute_columns}
        attribute_html = format_attributes(attributes)
        if col_edge=="Default":
            G.add_edge(src_name,dest_name, title=r"{}".format(attribute_html), color='lightblue',color_edge='lightblue')
        else:
            G.add_edge(src_name,dest_name, title=r"{}".format(attribute_html), color=lookup_light_edge[row[col_edge]],color_edge = row[col_edge])
    G = nx.relabel_nodes(G, {n: str(n) for n in G.nodes()})
    nt = Network(height="1500px", width="100%",bgcolor="#222222", font_color="white", directed=True, notebook=True, filter_menu=True, cdn_resources='remote')
    nt.from_nx(G)
    nt.force_atlas_2based(gravity=-18950,central_gravity=2.0,spring_length=200,spring_strength=0.5,damping=0.75,overlap=0.5)
    nt.set_edge_smooth('dynamic')
    # Show additional buttons for physics and interaction (optional)
    nt.show_buttons(filter_=['physics', 'interaction'])
    # Generate and save the HTML file
    html_file_path = './templates/non_display_files/a.html'
    if os.path.exists(html_file_path):
        # Delete the file if it exists
        os.remove(html_file_path)
    # Write the HTML file
    nt.write_html(html_file_path)