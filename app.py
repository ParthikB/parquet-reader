#import pandas as pd
#pd.set_option('display.max_colwidth', -1) #to disable string truncation
#data = pd.read_parquet('test.parquet', engine='pyarrow')

from flask import Flask
import pandas as pd
import dash_table
import dash
import dash_core_components as dcc
import dash_html_components as html
import io, base64


server = Flask(__name__)

# @server.route('/')
# def hello_world():
    # return 'Hello World!'

df = pd.read_parquet('test.parquet', engine='pyarrow')

data_dict = {}
for col in df.columns:
    data_dict[col] = df[col]
    
app = dash.Dash(
                __name__,
                server=server,
                routes_pathname_prefix='/dash/')

app.layout = html.Div([

            dcc.Upload(
            id="upload",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
                    },
            multiple=False,
            ),

            dcc.Dropdown(
                        id     = 'dropdown',
                        options= [{'label': s, 'value': s} for s in data_dict.keys()],
                        value  = [s for s in data_dict.keys()],
                        multi  = True
                        ),
            
            dash_table.DataTable(
                        id          = "table",
                        data        = df.to_dict('records'),
                        columns     = [{'id': c, 'name': c} for c in df.columns],
                        page_action = 'none',
                        style_table = {'height': '300px', 'overflowY': 'auto'}
                        ),
                        
            html.Div(id='input')
                                    
            ])            


@app.callback(
    dash.dependencies.Output('table', 'data'),
    dash.dependencies.Output('table', 'columns'),
    [dash.dependencies.Input('dropdown', 'value')])
def select_col(values):
    df_filtered = df[values]
    data        = df_filtered.to_dict(orient='records')
    columns     = [{'id': c, 'name': c} for c in df_filtered.columns]
    return data, columns
    
@app.callback(
    dash.dependencies.Output('input', 'children'),
    [dash.dependencies.Input('upload', 'contents')])
def upload_csv(contents):
    if contents:
        content_type, content_string = contents.split(',')
        print(content_type)
        df = pd.read_parquet(io.StringIO(base64.b64decode(content_string).decode('utf-8')), engine='pyarrow')

    
    
    
app.run_server(debug=True)


