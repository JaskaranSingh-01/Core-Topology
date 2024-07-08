import pandas as pd
import os
from pelote import tables_to_graph
from ipysigma import Sigma
import plotly.graph_objects as go

import re

# Function to update the HTML content
def update_html_content(content, title, favicon):
    # Define patterns for <title> and <link rel="icon"> tags
    title_pattern = re.compile(r'<title>.*?</title>', re.IGNORECASE)
    favicon_pattern = re.compile(r'<link.*?rel="icon".*?>', re.IGNORECASE)

    # Define the new tags
    new_title_tag = f'<title>{title}</title>'
    new_favicon_tag = f'<link rel="icon" type="image/x-icon" href="{favicon}">'

    # Replace or add the <title> tag
    if title_pattern.search(content):
        content = title_pattern.sub(new_title_tag, content)
    else:
        content = content.replace('<head>', f'<head>\n    {new_title_tag}', 1)

    # Replace or add the <link rel="icon"> tag
    if favicon_pattern.search(content):
        content = favicon_pattern.sub(new_favicon_tag, content)
    else:
        content = content.replace('<head>', f'<head>\n    {new_favicon_tag}', 1)

    return content

# Function to process each HTML file
def process_html_files(directory, title, favicon):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update the HTML content
                new_content = update_html_content(content, title, favicon)
                
                # Write the updated content back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f'Updated {file_path}')

def valid_paths(file_name):
    path_list = {}
    df = pd.read_excel(file_name,engine='openpyxl')
    df = df.astype(str)
    for idx,row in df.iterrows():
        path = row['Path']
        ls=path.split(' -> ')
        for idx in range(len(ls)):
            ls[idx]=ls[idx].replace(' ','')
        start = ls[0]
        end = ls[-1]
        key = (start, end)
        if key not in path_list:
            path_list[key] = []
        path_list[key].append(ls)
    return path_list

def parse_route(file_paths):
    lookup = {}
    for i in os.listdir('templates/files'):
        if i in file_paths:
            i=i
        else:
            lookup[i.split('.')[0]]=i
    return lookup

def remove_duplicates(input_list):
    output = []
    for x in input_list:
        if x not in output:
            output.append(x)
    return output

def set_node_data(node,src,dest):
    if node==src:
        node_data={
            "Node":src,
            "col":'Source'
        }
    elif node==dest:
        node_data={
            "Node":dest,
            "col":'Destination'
        }
    else:
        node_data={
            "Node":node,
            "col":'nodes'
        }
    return node_data

def set_edge_data(src,dest):
    edge_data = {
        "source":src,
        "target":dest
    }
    return edge_data



def chk_files(path):
    script_tag = '<script src="static/script.js" defer></script>'

    for filename in os.listdir(path):
        if filename.endswith('.html'):
            filepath = os.path.join(path, filename)
            with open(filepath, 'r') as file:
                content = file.read()

            if script_tag not in content:
                content = content.replace('</body>', f'{script_tag}\n</body>')
                with open(filepath, 'w') as file:
                    file.write(content)

# def format_title(path)


def find_path(G,src,dest,path_list):
    table_nodes = []
    table_edges = []
    target_pair = (src,dest)
    if target_pair not in path_list:
        return 'Fail'
    else:
        prev='-1'
        for ls in path_list[target_pair]:
            for i in ls:
                if prev != '-1':
                    set_edge_data(prev,i)
                    table_edges.append(edge_data)
                    
                node_data=set_node_data(i,src,dest)
                table_nodes.append(node_data)
                
                for node in G.neighbors(i):
                    node_data = set_node_data(node,src,dest)
                    table_nodes.append(node_data)
                    
                    edge_data = set_edge_data(i,node)
                    table_edges.append(edge_data)
                prev=i
        
        g = tables_to_graph(table_nodes, table_edges, node_col="Node", node_data=["Node",'col'], edge_data=['source', 'target'], directed=True)
        Sigma.write_html(g,"./templates/non_display_files/path.html",fullscreen=True,clickable_edges=True,node_size=g.degree,node_color='col')
        return 'Success'
    
    
    
# def parse_file_u1(path):
#     # path = 'GDC_NPO_CS_DASH_Counter_CNRH_UG_Part1.csv'
#     df = pd.read_csv(path, na_values=['NA', 'N/A', ''])

#     data_lusr = {}
#     data_psr = {}
#     lusr = []
#     for idx,row in df.iterrows():
#         if row['Object Name'] not in data_lusr:
#             data_lusr[row['Object Name']]=[]
#         if pd.isnull(row['LUSR']):
#             row['LUSR']=0;
#         data_lusr[row['Object Name']].append([row['Result Time'],row['LUSR'],row['Paging_Success_Rates']])
#         if row['Object Name'] not in data_psr:
#             data_psr[row['Object Name']]=[]
#         if pd.isnull(row['Paging_Success_Rates']):
#             row['Paging_Success_Rates']=0;
#         data_psr[row['Object Name']].append([row['Result Time'],row['Paging_Success_Rates']])
#     return data_lusr,data_psr

def parse_file_u2(path,obj):
    # path = 'GDC_NPO_CS_DASH_Counter_CNRH_UG_Part1.csv'
    df = pd.read_csv(path, na_values=['NA', 'N/A', ''])
    keys = []
    for k,v in df.items():
        keys.append(k)

    data = {}
    keys_data = []
    
    lusr = []
    label = ['Result Time','Period_start_time','Start Time', 'LUSR','Paging_Success_Rates','Paging_Success_Rate', 'Peak_Processor_Load','Location_Update_Success_Rate' , 'Overall_SMS_suc_rate' ,'Paging_Success_Rate_for_3G_Calls_NBH','ASR_Answer_Seizure_Ratio','SCR_Successful_Call_Rate','Overall_SMS_success_rate_New','LUSR_2G_3G_GSMM','LUSR_3G_UMTS','Contractual Paging Success Rate'] 
    for idx,row in df.iterrows():
        if row[obj] not in data:
            data[row[obj]]=[]
        
        for i in label :
            if i in keys:
                if i not in keys_data: 
                    keys_data.append(i)
                if i == label[0] or i== label[1] or i==label[2]:
                    continue
                if pd.isnull(row[i]):
                    row[i]=0;
        ls = []
        for i in label:
            if i in keys:
                ls.append(row[i])

        data[row[obj]].append(ls)
    return data,keys_data

def plot_data(data,keys,name):
    fig = go.Figure()
    for Name in name:
        for i in range(len(data[Name][0])-1):
            data_list=data[Name]
            x=[]
            y=[]
            for j in data_list:
                print(j)
                y.append(j[0])
                x.append(j[i+1])
            fig.add_trace(go.Scatter(
                x=y,
                y=x,
                name=Name + ' ' +keys[i+1],
            ))

    fig.write_html('./templates/non_display_files/a.html')

    
def plot_data_comp(data, keys,name1,name2):
    fig = go.Figure()
    for i in range(len(data[name1][0])-1):
        data_list=data[name1]

        x=[]
        y=[]
        for j in data_list:
            y.append(j[0])
            x.append(j[i+1])
        fig.add_trace(go.Scatter(
            x=y,
            y=x,
            name=name1 + ' ' +keys[i+1],
        ))

    for i in range(len(data[name1][0])-1):
        data_list=data[name2]

        x=[]
        y=[]
        for j in data_list:
            y.append(j[0])
            x.append(j[i+1])
        fig.add_trace(go.Scatter(
            x=y,
            y=x,
            name=name2+ ' ' +keys[i+1],
        ))

    fig.write_html('./templates/non_display_files/a.html')