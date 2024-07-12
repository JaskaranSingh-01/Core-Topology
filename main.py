from flask import Flask, render_template, request , redirect, url_for
import pandas as pd
import networkx as nx
import os
from pelote import tables_to_graph
from ipysigma import Sigma
import module
import path


# Specify the directory, title, and favicon
directory = './templates'  # Change this to your directory path
title = 'Core Topology'
favicon = '/static/favicon.ico'  # Change this to your favicon path
# Process the HTML files
module.process_html_files(directory, title, favicon)


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
edge_data_bytelldp ,critical_nodes = path.get_data(file5)

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


def number_to_digits_string(number):
    # Convert number to string
    num_str = str(number)
    
    # Initialize an empty string to store digits
    digits_string = ""
    
    # Iterate over each character in the string representation of the number
    for char in num_str:
        # Append each character (digit) to the digits_string
        digits_string += char
    
    return digits_string

sheet_num = 0

app = Flask(__name__)
@app.route('/', methods=['GET','POST'])
def ind():
    return render_template('index.html',files=lookup,files_uganda_1 = list_options_u1,files_uganda_2 = list_options_u2,files_zim_1 = list_options_z1,files_zim_2 =list_options_z2)

@app.route('/form1', methods=['GET','POST'])
def form1():
    if request.method == 'POST':
        value=request.form.get('Function')
        if value == 'V':
            module.process_html_files(directory, title, favicon)
            return render_template('files/examplenet.html')
        elif value == 'Find Path':
            src = request.form.get('src')
            dest = request.form.get('des')
            check_progress = module.find_path(G,src,dest,path_list)
            module.chk_files(location2)
            if check_progress == 'Success':
                module.process_html_files(directory, title, favicon)
                return render_template('non_display_files/path.html')
            else:
                return f'No path exists from {src} to {dest}!!'
        elif value == 'all':
            module.process_html_files(directory, title, favicon)
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
        elif value == 'value_of_bytellldp_nx':
            src = request.form.get('bytellldp_source_nx')
            paths = path.get_all_paths(src,edge_data_bytelldp)
            path.draw_paths_nx(paths,critical_nodes)
            module.process_html_files(directory, title, favicon)
            return render_template('non_display_files/bytellldp.html')
        elif value == 'value_of_bytellldp_ipy':
            src = request.form.get('bytellldp_source_ipy')
            paths = path.get_all_paths(src,edge_data_bytelldp)
            path.draw_paths_ipy(paths,critical_nodes)
            module.chk_files('./templates/non_display_files')
            module.process_html_files(directory, title, favicon)
            return render_template('non_display_files/bytellldp.html')
        module.process_html_files(directory, title, favicon)
        return render_template('non_display_files/a.html')
            
    return render_template('index.html',files=lookup,files_uganda_1 = list_options_u1,files_uganda_2 = list_options_u2,files_zim_1 = list_options_z1,files_zim_2 =list_options_z2)

app.config['UPLOAD_FOLDER'] = './uploads'
@app.route('/form2',methods=['GET','POST'])
def form2():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return render_template("index.html")
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            sheet_names = pd.ExcelFile(filepath).sheet_names
            return render_template('select_sheets.html', sheets = sheet_names,filename = file.filename)      
            return redirect(url_for('select_columns', filename=file.filename))
            
@app.route('/setect_sheets/<filename>',methods = ['GET','POST'])
def select_sheets(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    sheet_names = pd.ExcelFile(filepath).sheet_names
    selected_sheets='0'
    if request.method == 'POST':
        selected_sheets = request.form.getlist('sheets')
        num = None
        for sheet in selected_sheets:
            if sheet in sheet_names:
                num = sheet_names.index(sheet)
                break
        
        if num is None:
            return 'Selected sheet not found in file'
        
        return redirect(url_for('select_columns', filename=filename, num=num))
    else:
        return render_template('select_sheets.html', sheets = sheet_names,filename = filename)  


@app.route('/select_columns/<filename>/<num>', methods=['GET', 'POST'])
def select_columns(filename,num):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return 'File not found'
    
    try:
        if filename.endswith('.xlsx'):
            df = pd.read_excel(filepath, sheet_name=int(num), engine='openpyxl')
        else:
            df = pd.read_csv(filepath)
    except Exception as e:
        return str(e)

    df = df.astype(str)
    df = df.drop_duplicates()
    columns = df.columns.tolist()
    
    if request.method == 'POST':
        selected_columns = request.form.getlist('columns')
        lib = request.form.get('lib')
        source = request.form.get('src')
        destination = request.form.get('dest')
        if lib == 'ipy':
            path.draw_ipy_graph(source,destination,df,selected_columns,filename)
        elif lib == 'nx':
            path.draw_nx_graph(source,destination,df,selected_columns,filename)
        module.chk_files('./templates/output')
        module.process_html_files(directory, title, favicon)
        return render_template('output/' + filename.replace(' ', "").replace('-', '').split('.')[0] + '.html', columns=selected_columns)
    return render_template('select_columns.html',columns=columns, filename=filename,num=num)

@app.route('/form3', methods=['GET', 'POST'])
def form3():
    if request.method=='POST':
        value = request.form.get('Function-form-3')
        if value == 'ideal_value_of_bytellldp_nx':
            src = request.form.get('bytellldp_source_ideal_nx');
            invalid = request.form.get('bytellldp_source_invalid_nx');
            paths = path.get_all_paths(src,edge_data_bytelldp)
            ideal_path = path.get_ideal_path(invalid,paths)
            if len(ideal_path) == 0:
                return "No Ideal paht exists"
            path.draw_paths_nx(ideal_path,critical_nodes)
            module.process_html_files(directory, title, favicon)
            return render_template('non_display_files/bytellldp.html')
        elif value == 'ideal_value_of_bytellldp_ipy':
            src = request.form.get('bytellldp_source_ideal_ipy');
            invalid = request.form.get('bytellldp_source_invalid_ipy');
            paths = path.get_all_paths(src,edge_data_bytelldp)
            ideal_path = path.get_ideal_path(invalid,paths)
            if len(ideal_path) == 0:
                return "No Ideal paht exists"
            path.draw_paths_ipy(ideal_path,critical_nodes)
            module.chk_files('./templates/non_display_files')
            module.process_html_files(directory, title, favicon)
            return render_template('non_display_files/bytellldp.html')

@app.route("/form1/process",methods = ['GET','POST'])
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
    module.process_html_files(directory, title, favicon)
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
        module.process_html_files(directory, title, favicon)
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
    app.run(debug=True,host='0.0.0.0',port=6001)