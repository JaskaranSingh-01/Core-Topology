from flask import Flask, render_template, request ,jsonify
import pandas as pd
import networkx as nx
import os
from pelote import tables_to_graph
from ipysigma import Sigma
import module
import path


# store the valid path data
file_name = './Data/filtered_paths.xlsx'
path_list=module.valid_paths(file_name)

# parsing for dynamic routing
file_paths = ["path.html","examplenet.html"] 
lookup = module.parse_route(file_paths)

# reading the graph
G=nx.read_gml('./Data/examplenet.gml')


# Path to the directory containing your HTML files
location1 = 'templates/files'
location2 = 'templates/non_display_files'
# appending a script tag to the .html files
module.chk_files(location1)
module.chk_files(location2)

#  =======uganda file=======
file1 = './Data/GDC_NPO_CS_DASH_Counter_CNRH_UG_Part1.csv'
file2 = './Data/CNRH_NPO.csv'
file3 = './Data/ZM-GDC_Core_KPIs.csv'
file4 = './Data/ZM-CNRH_NPO.csv'
data_u1,keys_u1= module.parse_file_u2(file1 , 'Object Name')
data_u2,keys_u2= module.parse_file_u2(file2 , 'ENSS_name')
data_z1,keys_z1= module.parse_file_u2(file3 , 'NE Location')
data_z2,keys_z2= module.parse_file_u2(file4 , 'ENSS_name')

file5 = './Data/Bytellldp.xlsx'
edge_data_bytelldp = path.get_data(file5)

# storing node names in a list
list_options_u1 = []
for k in data_u1:
    list_options_u1.append(k)

list_options_u2 = []
for k in data_u2:
    list_options_u2.append(k)
    
    
list_options_z1 = []
for k in data_z1:
    list_options_z1.append(k)
    
list_options_z2 = []
for k in data_z2:
    list_options_z2.append(k)


app = Flask(__name__)
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        value=request.form.get('Function')
        if value == 'V':
            return render_template('files/examplenet.html')
        elif value == 'Find Path':
            src = request.form.get('src')
            dest = request.form.get('des')
            check_progress = module.find_path(G,src,dest,path_list)
            module.chk_files(location2)
            if check_progress == 'Success':
                return render_template('non_display_files/path.html')
            else:
                return f'No path exists from {src} to {dest}!!'
        elif value == 'all':
            return render_template('files/ugandabasic.html')
        elif value == 'individual':
            key = request.form.get('option1')
            k = []
            k.append(key)
            module.plot_data(data_u1,keys_u1,k)
        elif value == 'compare':
            key1 = request.form.get('option2')
            key2 = request.form.get('option3')
            module.plot_data_comp(data_u1,keys_u1,key1,key2)
        elif value == 'u2':
            key = request.form.get('option4')
            k = []
            k.append(key)
            module.plot_data(data_u2,keys_u2,k)
        elif value == 'z1':
            key = request.form.get('option5')
            k = []
            k.append(key)
            module.plot_data(data_z1,keys_z1,k)
        elif value == 'z2':
            key = request.form.get('option6')
            k = []
            k.append(key)
            module.plot_data(data_z2,keys_z2,k)
        elif value == 'value_of_bytellldp':
            src = request.form.get('bytellldp_source')
            paths = path.get_all_paths(src,edge_data_bytelldp)
            path.draw_paths2(paths)
            return render_template('non_display_files/bytellldp.html')

        return render_template('non_display_files/a.html')
            
    return render_template('index.html',files=lookup,files_uganda_1 = list_options_u1,files_uganda_2 = list_options_u2,files_zim_1 = list_options_z1,files_zim_2 =list_options_z2)

@app.route("/process",methods = ['GET','POST'])
def process():
    data = request.get_json()
    name_list = []

    if data is not None:
        for k, v in data_u1.items():
            if data['value'] in k:
                name_list.append(k)
    print(data)
    if data is not None:
        module.plot_data(data_u1,keys_u1,name_list)
    return render_template('/non_display_files/a.html')
    #     return jsonify({'data': name_list}), 200
    # else:
    #     print("No data received")
    #     return jsonify({'error': 'No data provided'}), 400



@app.route("/<route_name>")
def dynamic_route(route_name):
    print("Requested route:", route_name)
    if route_name in lookup:
        print("File path found:", lookup[route_name])
        return render_template(f'files/{lookup[route_name]}')
    else:
        print("Route not found:", route_name)
        return f"Route '{route_name}' not found."

# @app.route('/<template_name>',methods=['GET','POST'])
# def dynamic_template(template_name):
#     # Ensure the requested template exists in the templates folder
#     # print(template_name)
#     if os.path.exists(f'./templates/files/{template_name}.html'):
#         return render_template(f'files/{template_name}.html')
#     else:
#         # Return a 404 error if the template does not exist
#         return f"Route not found: {template_name}"
#         # abort(404)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=7000)