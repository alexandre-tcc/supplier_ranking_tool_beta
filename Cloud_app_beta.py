#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
import os


# DASH LIB
import dash
from dash import dcc
from dash import html
from dash_table import DataTable
from dash_table import FormatTemplate
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


data = np.random.rand(3, 20)
df_test = pd.DataFrame(data, columns=[f"col_{i}" for i in range(20)])

def clear_database():
    open('save_sup.csv', 'w')
    
def test_length(name_file):
        length=0
        with open(name_file, 'r') as f:         
            datareader = csv.reader(f)
            for row_test in datareader:
                if row_test !=[]:
                    length+=1
        if length>=10:
            return False
        else:
            return True
    
    
def csv_to_df_live(name_file,
                   scf_wt,
                    VMI_wt,
                    critical_wt,
                    inventory_wt,
                    pay_term_wt,
                    lead_time_wt,
                    business_wt,
                    overdue_wt):
    data=[]
    with open(name_file, 'r') as f:         
            datareader = csv.reader(f)
            for row_test in datareader:
                if row_test !=[]:
                    data.append(row_test)
 
    # LET'S HAVE A CREATED DATA WITH SCORE FROM DF_DATA
    data_score=[]
    for row in data:
        row_nk=[]
        row_nk.append(row[0])
        row_nk.append(weighted_total_live(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],scf_wt,
                        VMI_wt,
                        critical_wt,
                        inventory_wt,
                        pay_term_wt,
                        lead_time_wt,
                        business_wt,
                        overdue_wt))
        data_score.append(row_nk)
    

    df = pd.DataFrame(data_score, columns = ['Supplier Name','Rating (out of 10)'])
    sorted_df = df
    sorted_df['Rating (out of 10)'] = sorted_df['Rating (out of 10)'].astype(float)
    sorted_df['ReverseRank']=sorted_df['Rating (out of 10)'].rank(method='max')
    nrows = sorted_df.shape[0]
    max_rank = sorted_df['ReverseRank'].max()
    sorted_df['Rank'] = nrows + 1 - df['ReverseRank']
    sorted_df.pop('ReverseRank')
    sorted_df = sorted_df.sort_values('Rating (out of 10)', ascending=False)
    sorted_df.insert(0, 'Rank', sorted_df.pop('Rank'))


    return sorted_df
    
    
def csv_to_df(name_file):
    data=[]
    with open(name_file, 'r') as f:         
            datareader = csv.reader(f)
            for row_test in datareader:
                if row_test !=[]:
                    data.append(row_test)
 
    # LET'S HAVE A CREATED DATA WITH SCORE FROM DF_DATA
    data_score=[]
    for row in data:
        row_nk=[]
        row_nk.append(row[0])
        row_nk.append(weighted_total(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
        data_score.append(row_nk)
    

    df = pd.DataFrame(data_score, columns = ['Supplier Name','Rating (out of 10)'])
    sorted_df = df
    sorted_df['Rating (out of 10)'] = sorted_df['Rating (out of 10)'].astype(float)
    sorted_df['ReverseRank']=sorted_df['Rating (out of 10)'].rank(method='max')
    nrows = sorted_df.shape[0]
    max_rank = sorted_df['ReverseRank'].max()
    sorted_df['Rank'] = nrows + 1 - df['ReverseRank']
    sorted_df.pop('ReverseRank')
    sorted_df = sorted_df.sort_values('Rating (out of 10)', ascending=False)
    sorted_df.insert(0, 'Rank', sorted_df.pop('Rank'))

    return sorted_df

def csv_to_df_raw(name_file):
    data=[]
    with open(name_file, 'r') as f:         
            datareader = csv.reader(f)
            for row_test in datareader:
                if row_test !=[]:
                    data.append(row_test)
 
    # LET'S HAVE A CREATED DATA WITH SCORE FROM DF_DATA
    data_score=[]
    for row in data:
        row_nk=[]
        row_nk.append(row[0])
        row_nk.append(weighted_total(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
        data_score.append(row_nk)
    

    df = pd.DataFrame(data_score, columns = ['Supplier Name','Rating (out of 10)'])
    '''sorted_df = df
    sorted_df['Rating (out of 10)'] = sorted_df['Rating (out of 10)'].astype(float)
    sorted_df['ReverseRank']=sorted_df['Rating (out of 10)'].rank(method='max')
    nrows = sorted_df.shape[0]
    max_rank = sorted_df['ReverseRank'].max()
    sorted_df['Rank'] = nrows + 1 - df['ReverseRank']
    sorted_df.pop('ReverseRank')
    sorted_df = sorted_df.sort_values('Rating (out of 10)', ascending=False)
    sorted_df.insert(0, 'Rank', sorted_df.pop('Rank'))'''


    return df


def csv_to_df_data(name_file):
    data=[]
    with open(name_file, 'r') as f:         
            datareader = csv.reader(f)
            for row_test in datareader:
                if row_test !=[]:
                    data.append(row_test)
    

    df = pd.DataFrame(data, columns = ['Supplier Name','scf','VMI','critical','inventory','pay_term','lead_time','business','overdue'])

    return df


class Supplier:
    def __init__(self, name_, scf_,
            VMI_,
            critical_,
            inventory_,
            pay_term_,
            lead_time_,
            business_,
            overdue_):
        self.name_=name_
        self.scf_=scf_
        self.VMI_=VMI_
        self.critical_=critical_
        self.inventory_=inventory_
        self.pay_term_=pay_term_
        self.lead_time_=lead_time_
        self.business_=business_
        self.overdue_=overdue_
        
    def add_supplier(self):
        test_length=False
        with open('save_sup.csv', 'r') as f:         
            datareader = csv.reader(f)
            #print(data)
            for row_test in datareader:
                if row_test !=[]:
                    if row_test[0]==self.name_:
                        test_id=True
                        #print('This supplier has already been added (name:'+self.name_+')')
        #Append if not already in the DB                    
        if test_length==False:
            row=[self.name_,self.scf_,self.VMI_,self.critical_,self.inventory_,self.pay_term_,self.lead_time_,self.business_,self.overdue_]
            with open('save_sup.csv', 'a') as f:
                writer=csv.writer(f)
                writer.writerow(row)
                #print('Supplier : '+self.name_+'  Added')



def generate_color_code(value):
    max_=10
    percent = (value - 1) / (max_ - 1) * 100
    # calculate the red and green values based on the percentage
    red = int(255 * (100 - percent) / 100)
    green = int(255 * percent / 100)
    # format the color code as a hex string
    color_code = '#{:02x}{:02x}00'.format(red, green)
    return color_code


def weighted_total(scf_,
                    VMI_,
                    critical_,
                    inventory_,
                    pay_term_,
                    lead_time_,
                    business_,
                    overdue_,):
    
    if any([arg is None for arg in [scf_,
                                    VMI_,
                                    critical_,
                                    inventory_,
                                    pay_term_,
                                    lead_time_,
                                    business_,
                                    overdue_,]]):
        return -1
    
    else:
    
        df_wt = pd.read_csv('param_wt.csv', header=0)
        scf_wt=df_wt['scf'][0]
        VMI_wt=df_wt['VMI'][0]
        critical_wt=df_wt['critical'][0]
        inventory_wt=df_wt['inventory'][0]
        pay_term_wt=df_wt['pay_term'][0]
        lead_time_wt=df_wt['lead_time'][0]
        business_wt=df_wt['business'][0]
        overdue_wt=df_wt['overdue'][0]
        
        if scf_wt+VMI_wt+critical_wt+inventory_wt+pay_term_wt+lead_time_wt+business_wt+overdue_wt>1:
            return -1

        else:
            #----------------------------------------scf
            if scf_=='No':
                scf=10*scf_wt
            else:
                scf=0

            #----------------------------------------VMI
            if VMI_=='No':
                VMI=10*VMI_wt
            else:
                VMI=0

            #----------------------------------------critical
            if critical_=='Yes':
                critical=10*critical_wt
            else:
                critical=0

            #----------------------------------------inventory
            if inventory_=='Yes':
                inventory=10*inventory_wt
            else:
                inventory=0

            #----------------------------------------pay_term
            if pay_term_=='No':
                pay_term=10*pay_term_wt
            else:
                pay_term=0

            #----------------------------------------lead_time
            if lead_time_=='Yes':
                lead_time=10*lead_time_wt
            else:
                lead_time=0

            #----------------------------------------business
            if business_=='Yes':
                business=10*business_wt
            else:
                business=0

            #----------------------------------------overdue
            if overdue_=='Yes':
                overdue=10*overdue_wt
            else:
                overdue=0


            return (scf+VMI+critical+inventory+pay_term+lead_time+business+overdue)
        
        
def weighted_total_live(scf_,
                    VMI_,
                    critical_,
                    inventory_,
                    pay_term_,
                    lead_time_,
                    business_,
                    overdue_,
                    scf_wt,
                    VMI_wt,
                    critical_wt,
                    inventory_wt,
                    pay_term_wt,
                    lead_time_wt,
                    business_wt,
                    overdue_wt):
    
    if any([arg is None for arg in [scf_,
                                    VMI_,
                                    critical_,
                                    inventory_,
                                    pay_term_,
                                    lead_time_,
                                    business_,
                                    overdue_,]]):
        return -1
    
    else:
        totall=scf_wt+VMI_wt+critical_wt+inventory_wt+pay_term_wt+lead_time_wt+business_wt+overdue_wt
        if totall!=100:
            return -1

        else:
            #----------------------------------------scf
            if scf_=='No':
                scf=10*scf_wt/100
            else:
                scf=0

            #----------------------------------------VMI
            if VMI_=='No':
                VMI=10*VMI_wt/100
            else:
                VMI=0

            #----------------------------------------critical
            if critical_=='Yes':
                critical=10*critical_wt/100
            else:
                critical=0

            #----------------------------------------inventory
            if inventory_=='Yes':
                inventory=10*inventory_wt/100
            else:
                inventory=0

            #----------------------------------------pay_term
            if pay_term_=='No':
                pay_term=10*pay_term_wt/100
            else:
                pay_term=0

            #----------------------------------------lead_time
            if lead_time_=='Yes':
                lead_time=10*lead_time_wt/100
            else:
                lead_time=0

            #----------------------------------------business
            if business_=='Yes':
                business=10*business_wt/100
            else:
                business=0

            #----------------------------------------overdue
            if overdue_=='Yes':
                overdue=10*overdue_wt/100
            else:
                overdue=0


            return (scf+VMI+critical+inventory+pay_term+lead_time+business+overdue)

    
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.MINTY,dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP])

add_icon = html.I(className="fa-regular fa-floppy-disk me-2")
clear_icon = html.I(className="fa-solid fa-trash me-2")
change_icon = html.I(className="fa-solid fa-wrench me-2")
warning_icon = html.I(className="fa-solid fa-circle-exclamation me-2")
ok_icon = html.I(className="fa-solid fa-circle-check me-2")
edit_icon = html.I(className="fa-solid fa-pen me-2")

app.layout = html.Div([
    
    
    html.Header(
      children = [   
      html.Br(),
      html.Br(),
      html.Br(),
      html.Br(),
      html.H1(' ', style={'color':'rgb(254, 163, 27)', 'fontSize': 1,
                                          'display':'inline-block'})],
                 style={'width':'100%', 'height':'1px', 'background-repeat':'no-repeat',
                'background-position':'left'}),
    
    
    html.Div(
        children=[
            html.Br(),
            html.H1('TCC - Supplier Rating', style={'color': 'white',#'pading':'50px 0px 50px 0px', 
                                            'textAlign': 'center','font-family':'sans-serif' ,'fontSize': 45,}),
            html.Br(),

        
        ]
        ,style={'background-color': 'rgb(52, 56, 52)'}
                                                  
        ),
    
    
    # Overall Summary
    dcc.Tabs(
        id="tabs_common_summary", value='tab_1',
        className='custom-tabs', vertical=False,
        children=[
            dcc.Tab(label='⚙ Criterias weightage', value='tab_2', className='custom-tab',
                    selected_className='custom-tab--selected',style={'color': 'white','background-color':'rgb(117, 125, 120)','font-family':'sans-serif'}),
            dcc.Tab(label='➲ Rank Suppliers', value='tab_1', className='custom-tab',
                    selected_className='custom-tab--selected',style={'color': 'white','background-color':'rgb(117, 125, 120)','font-family':'sans-serif'}),
            dcc.Tab(label='☷ Ranking', value='tab_3', className='custom-tab',
                    selected_className='custom-tab--selected',style={'color': 'white','background-color':'rgb(117, 125, 120)','font-family':'sans-serif'}),
            dcc.Tab(label='✎ Edit or remove Supplier', value='tab_4', className='custom-tab',
                    selected_className='custom-tab--selected',style={'color': 'white','background-color':'rgb(117, 125, 120)','font-family':'sans-serif'}),
        ], style={'font-family':'sans-serif','fontSize': 25,'color':'red'}),
    
    
    html.Div(children=[
        
        html.Div(id='tab_display'),
        

    
    
    # FOOTER
    html.Footer(
        children=[
            html.Br(),
            html.H1('Trade Capital Corporation © 2022', style={'color': 'white',#'pading':'50px 0px 50px 0px', 
                                            'textAlign': 'center','font-family':'sans-serif' ,'fontSize': 20,}),
            html.Br(),

        
        ]
        ,style={'background-color': 'rgb(52, 56, 52)'}
                                                  
        ),

    # Closing
    ],
    style={'text-align': 'center', 'display': 'inline-block', 'width': '100%',
           'background-color': 'rgb(245, 245, 245)', 'color': 'rgb(79, 79, 79)'})
])


@app.callback(
    Output('tab_display', 'children'),
    Input('tabs_common_summary', 'value'),
    #Input(df_timeline_CF)
)
def update_styles(tab):
    if tab=='tab_1':

        return html.Div(children=[
        
        html.Div(children=[
            
            
            html.H3('Supplier ranking form',style={'color': 'black','font-family':'sans-serif' ,'width':'100%',
                                                                         'fontSize': 32,'verticalAlign': 'top','margin' : '20px 20px 20px 20px',
                                                      'display': 'inline-block','horizontalAlign': 'center'}),

            html.Br(), #---------Name

            html.Div(children=[

                html.H3('Supplier Name:',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dbc.Input(id="name", placeholder="Enter supplier name",type='text',style={'color': 'blue','width':'20%','font-family':'sans-serif',
                                                              'fontSize': 22,'margin' : '10px','width':'250px',
                                                                  'align-items': 'center','flex':1,
                                                                'display': 'flex',  'justify-content':'left'}
                            ),
                ],style={'border': 'px solid orange','background-color':'white', 'display': 'flex',
                         'border-radius': 20,'margin' : '30px', 'flex':'row','horizontalAlign': 'center'},),


            html.Br(),

            html.Br(), #---------SCF

            html.Div(children=[
                html.H3('Does supplier have SCF now via banks?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='scf', options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),


            html.Br(),#---------VMI
            
            html.Div(children=[
                html.H3('Does Supplier currently have VMI agreement with Customer?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='VMI', options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),

            html.Br(),#---------Critical

            html.Div(children=[
                html.H3('Is Supplier  a critical supplier  in Client view?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='critical', options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),


            html.Br(),#---------inventory

            html.Div(children=[
                html.H3('Is Supplier inventory  greater than  20% of Client  total inventory?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='inventory', options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),

            html.Br(),#-----------------------------------------------pay_term

            html.Div(children=[
                html.H3('Is payment terms to supplier 45 days or less?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='pay_term', options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),


            html.Br(),#-----------------------------------------------lead_time

            html.Div(children=[
                html.H3('Is Supplier Lead time  > 90 days?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='lead_time', options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),


            html.Br(),#-----------------------------------------------business

            html.Div(children=[
                html.H3('Is Client business  greater than  20%  of Supplier total business?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='business', options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),

            html.Br(),#-----------------------------------------------overdue

            html.Div(children=[
                html.H3('Are supplier Invoices overdue by 30 days or greater?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='overdue', options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),

            html.Br(),

            html.Br(),

            html.Div(id='supplier_score'),
            
            
        ],style={'width':'75%','border': 'px solid orange',
                 'background-color':'white', 'display': 'inline-block',
                         'border-radius': 20,'margin' : '50px','padding':'50px'}),
        
        html.Br(),])
    
    elif tab=='tab_2':
        return html.Div(id='change_param')
    
    elif tab=='tab_3':
        return html.Div(id='supplier_table')
    
    else:
        df_=csv_to_df_raw('save_sup.csv')
        return html.Div(children=[
            html.H3('Supplier List (in development)',style={'color': 'black','font-family':'sans-serif' ,'width':'300px',
                                                                         'fontSize': 32,'verticalAlign': 'top','margin' : '50px',
                                                      'display': 'inline-block','horizontalAlign': 'center'}),

            html.Br(),

            DataTable(
                id='datatable-modify',
                columns=[
                    {"name": i, "id": i, "selectable": True} for i in df_.columns
                ],
                data=df_.to_dict('records'),
                editable=True,
                style_cell={'padding': '10px','font-family':'sans-serif','fontSize': 24},
                #filter_action="native",
                sort_action="native",
                sort_mode="multi",
                #column_selectable="single",
                row_selectable="single",
                #row_deletable=True,
                #selected_columns=[],
                #selected_rows=[],
                page_action="native",
                page_current= 0,
                page_size= 50,
            ),
            html.Div(id='modify_render')
        ],style={'margin':'50px'})

    
@app.callback(
    Output('modify_render', 'children'),
    Input('datatable-modify', 'selected_rows')
)
def clicks(datatable_modify):
    df_=csv_to_df_data('save_sup.csv')
    if datatable_modify==None:
        return html.Label([warning_icon,'Select to modify'],style={'font-family':'sans-serif' ,'fontSize': 22,'color':'red',
                                                       'width':'500px','display': 'inline-block','verticalAlign':'middle',
                                                        'margin' : '50px'#'height':'40px'
                                                       }),
    else:
        selection_name = list(df_.loc[datatable_modify, 'Supplier Name'])
        selection_scf = list(df_.loc[datatable_modify, 'scf'])
        selection_VMI = list(df_.loc[datatable_modify, 'VMI'])
        selection_inventory = list(df_.loc[datatable_modify, 'inventory'])
        selection_overdue = list(df_.loc[datatable_modify, 'overdue'])
        selection_pay_term = list(df_.loc[datatable_modify, 'pay_term'])
        selection_business = list(df_.loc[datatable_modify, 'business'])
        selection_lead_time = list(df_.loc[datatable_modify, 'lead_time'])
        selection_critical = list(df_.loc[datatable_modify, 'critical'])

        return html.Div(children=[
            
            html.Br(),
            html.Div(children=[
            
            html.H3('Edit: '+selection_name[0],style={'color': 'black','font-family':'sans-serif' ,'width':'500px',
                                                                     'fontSize': 28,'verticalAlign': 'top','margin' : '20px 20px 20px 20px',
                                                  'display': 'inline-block','horizontalAlign': 'center'}),


            html.Br(),

            html.Br(), #---------SCF

            html.Div(children=[
                html.H3('Does supplier have SCF now via banks?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='scf_edit',value=selection_scf[0], options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),


            html.Br(),#---------VMI
            
            html.Div(children=[
                html.H3('Does Supplier currently have VMI agreement with Customer?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='VMI_edit',value=selection_VMI[0], options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),

            html.Br(),#---------Critical

            html.Div(children=[
                html.H3('Is Supplier  a critical supplier  in Client view?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='critical_edit',value=selection_critical[0], options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),


            html.Br(),#---------inventory

            html.Div(children=[
                html.H3('Is Supplier inventory  greater than  20% of Client  total inventory?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='inventory_edit',value=selection_inventory[0], options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),

            html.Br(),#-----------------------------------------------pay_term

            html.Div(children=[
                html.H3('Is payment terms to supplier 45 days or less?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='pay_term_edit',value=selection_pay_term[0], options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),


            html.Br(),#-----------------------------------------------lead_time

            html.Div(children=[
                html.H3('Is Supplier Lead time  > 90 days?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='lead_time_edit',value=selection_lead_time[0], options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),


            html.Br(),#-----------------------------------------------business

            html.Div(children=[
                html.H3('Is Client business  greater than  20%  of Supplier total business?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='business_edit',value=selection_business[0], options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),

            html.Br(),#-----------------------------------------------overdue

            html.Div(children=[
                html.H3('Are supplier Invoices overdue by 30 days or greater?',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 22,'verticalAlign': 'top',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dcc.Dropdown(id='overdue_edit',value=selection_overdue[0], options={'Yes': 'Yes','No': 'No'},searchable=False
                               ,style={'color': 'black','font-family':'sans-serif',
                                      'fontSize': 22,'margin' : '10px','width':'250px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'left'}),
                
                ],style={'border': 'px solid orange','background-color':'#f2f2f2', 'display': 'flex',
                         'border-radius': 20,'margin' : '5px 20px 5px 20px', 'flex':'row','horizontalAlign': 'center'},),

            html.Br(),
                
            
            
            dbc.Button([edit_icon,"Edit"], id='button_edit_sup',color="primary", className="me-1",n_clicks=0,
                      style={'margin' : '20px 20px 20px 20px'}),
            dbc.Button([clear_icon,"Remove"], id='button_del_sup',color="secondary", className="me-1",n_clicks=0,
                      style={'margin' : '20px 20px 20px 20px'}),
            html.Div(id='button-clicks-edit'),
            html.Div(id='button-clicks-del'),
            
        ],style={'width':'50%','border': 'px solid orange','background-color':'white', 'display': 'inline-block',
                 'border-radius': 20,'horizontalAlign': 'center','padding':'50px'},
                       
                       )
        ])

@app.callback(
    Output('supplier_score', 'children'),
    Input('scf','value'),
    Input('VMI','value'),
    Input('critical','value'),
    Input('inventory','value'),
    Input('pay_term','value'),
    Input('lead_time','value'),
    Input('business','value'),
    Input('overdue','value')
)
def sup_score(scf_,
                VMI_,
                critical_,
                inventory_,
                pay_term_,
                lead_time_,
                business_,
                overdue_,):
    #process score:
    score=weighted_total(scf_,
                        VMI_,
                        critical_,
                        inventory_,
                        pay_term_,
                        lead_time_,
                        business_,
                        overdue_,)
    color=generate_color_code(score)
    
    nb_sup=test_length('save_sup.csv')
    if nb_sup==False:
        return html.Div(children=[html.Div(children=[
                html.Label([warning_icon,'You reached the maximum of 10 suppliers in the ranking -- Clear the table or remove some to rank other ones'],style={'font-family':'sans-serif' ,'fontSize': 22,'color':'red',
                                                   'width':'80%','display': 'inline-block','verticalAlign':'middle',
                                                    'margin' : '15px 15px 15px 15px'#'height':'40px'
                                                   })
                    ],style={'border': '0px solid orange','background-color':'#ffebeb', 'display': 'inline-block',
                             'border-radius': 20,'horizontalAlign': 'center','margin' : '15px 15px 15px 15px'}),])
            
    else:

        if score<0:
            return html.Div(children=[html.Div(children=[
                    html.Label([warning_icon,'Please answer all the fields'],style={'font-family':'sans-serif' ,'fontSize': 22,'color':'red',
                                                       'width':'500px','display': 'inline-block','verticalAlign':'middle',
                                                        'margin' : '15px 15px 15px 15px'#'height':'40px'
                                                       }),
                    ],style={'border': '0px solid orange','background-color':'#ffebeb', 'display': 'inline-block',
                     'border-radius': 20,'horizontalAlign': 'center','margin' : '15px 15px 15px 15px'}),])
        else:
            return html.Div(children=[html.Div(children=[
                    html.Label('Supplier score:',style={'font-family':'sans-serif' ,'fontSize': 20,'color':'black',
                                                       'width':'500px','display': 'inline-block','verticalAlign':'middle',#'height':'40px'
                                                       }),
                    html.Div(children=[
                    html.Label(str(score)+'/10',style={'font-family':'sans-serif' ,'fontSize': 20,'color':'blue',
                                                   'display': 'inline-block','verticalAlign':'middle',#'height':'40px'
                                                   }),
                    html.Div(children=[html.H3('.',style={'fontSize': 0}),],
                                                             style={'width': '30px','height': '30px',  'display': 'inline-block','margin' : '0px 5px 0px 5px',
                                                                    'color': 'blue', 'horizontalAlign': 'right','verticalAlign': 'middle',
                                                                    'border': '0px solid orange','border-radius': 30,
                                                                    'font-family':'sans-serif' ,'fontSize': 20,'background-color': color}),
                        ],style={'margin' : '10px 10px 10px 10px'}),

                    #dcc.Location(id='button-clicks', refresh=False),

                    dbc.Button([add_icon,"Save & Rank supplier"], id='button_rank_supplier',
                               color="primary", className="me-1",n_clicks=0,
                          style={'margin' : '20px 20px 20px 20px','fontSize': 16,'font-family':'sans-serif',}),
                    #html.Div(id='button-clicks'),
                    html.Div(id='add_sup_click'),
                    ]),
                    ],style={'border': '0px solid orange','background-color':'#dff7e5', 'display': 'inline-block',
                     'border-radius': 20,'horizontalAlign': 'center','margin' : '15px 15px 15px 15px',
                             'padding' : '15px 15px 15px 15px'})


@app.callback(
    #Output('button_clicks', 'pathname'),
    Output('add_sup_click', 'children'),
    [Input('button_rank_supplier', 'n_clicks'),
     Input('name','value'),
    Input('scf','value'),
    Input('VMI','value'),
    Input('critical','value'),
    Input('inventory','value'),
    Input('pay_term','value'),
    Input('lead_time','value'),
    Input('business','value'),
    Input('overdue','value')])
def clicks(n_clicks,
          name,
           scf_,
            VMI_,
            critical_,
            inventory_,
            pay_term_,
            lead_time_,
            business_,
            overdue_):

    if n_clicks>0:
        sup = Supplier(name,scf_,VMI_,critical_,inventory_,pay_term_,lead_time_,business_,overdue_)
        sup.add_supplier()
        return html.H3([ok_icon,'added -- RELOAD the page to update the ranking or add another supplier'],style={'color': 'green','font-family':'sans-serif' ,
                                                        'fontSize': 18,'verticalAlign': 'top','margin' : '10px',
                                                  'display': 'inline-block','horizontalAlign': 'center'}),


@app.callback(
    Output('supplier_table', 'children'),
    Input('tabs_common_summary', 'value'),
)
def sup_score(tab):
    df_sup=csv_to_df('save_sup.csv')
    if df_sup.empty:
        return html.H3('No supplier is currently ranked, go to --Rank suppliers-- tab to start the ranking',
                       style={'color': '#383838','font-family':'sans-serif' ,
                              'fontSize': 22,'verticalAlign': 'top','margin' : '50px',
                              'display': 'inline-block','horizontalAlign': 'center',
                             'border': '0px solid orange','background-color':'white', 'display': 'inline-block',
                     'border-radius': 20,'horizontalAlign': 'center','padding' : '50px'}),
    else:
        return html.Div([
            html.H3('Supplier Ranking',style={'color': 'black','font-family':'sans-serif' ,'width':'300px',
                                                                         'fontSize': 32,'verticalAlign': 'top','margin' : '50px',
                                                      'display': 'inline-block','horizontalAlign': 'center'}),

            html.Br(),
                DataTable(
                    id='datatable_1',
                    columns=[
                        {"name": i, "id": i, "deletable": True, "selectable": True} for i in df_sup.columns
                    ],
                    data=df_sup.to_dict('records'),
                    #editable=True,
                    #filter_action="disable",
                    sort_action="native",
                    sort_mode="multi",
                    #column_selectable="single",
                    #row_selectable="single",
                    #row_deletable=True,
                    style_cell={'padding': '10px','font-family':'sans-serif','fontSize': 24},
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 50,
                ),
            
            dbc.Button([clear_icon,"Clear table"], id='button_clear_table',
                           color="primary", className="me-1",n_clicks=0,
                      style={'margin' : '20px 20px 20px 20px','fontSize': 16,'font-family':'sans-serif',}),
            
            html.Div(id='clear_table_click')
        
        ],style={'margin':'50px'}),
    

@app.callback(
    Output('supplier_table_2', 'children'),
    [Input('scf_wt','value'),
    Input('VMI_wt','value'),
    Input('critical_wt','value'),
    Input('inventory_wt','value'),
    Input('pay_term_wt','value'),
    Input('lead_time_wt','value'),
    Input('business_wt','value'),
    Input('overdue_wt','value')],
)
def sup_score_2(scf_wt,
            VMI_wt,
            critical_wt,
            inventory_wt,
            pay_term_wt,
            lead_time_wt,
            business_wt,
            overdue_wt):
    
    df_sup=csv_to_df_live('save_sup.csv',
                          scf_wt,
                        VMI_wt,
                        critical_wt,
                        inventory_wt,
                        pay_term_wt,
                        lead_time_wt,
                        business_wt,
                        overdue_wt)
    
    if df_sup.empty:
        pass
    else:
        return html.Div([
            html.H3('Supplier Ranking',style={'color': 'black','font-family':'sans-serif' ,'width':'300px',
                                                                         'fontSize': 32,'verticalAlign': 'top','margin' : '50px',
                                                      'display': 'inline-block','horizontalAlign': 'center'}),

            html.Br(),
                DataTable(
                    id='datatable_2',
                    columns=[
                        {"name": i, "id": i, "deletable": True, "selectable": True} for i in df_sup.columns
                    ],
                    data=df_sup.to_dict('records'),
                    #editable=True,
                    #filter_action="disable",
                    sort_action="native",
                    sort_mode="multi",
                    #column_selectable="single",
                    #row_selectable="single",
                    #row_deletable=True,
                    style_cell={'padding': '10px','font-family':'sans-serif','fontSize': 24},
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 50,
                ),
        
        ],style={'margin':'50px'}),
    
    
@app.callback(
    Output('clear_table_click', 'children'),
    [Input('button_clear_table', 'n_clicks')])
def clicks(n_clicks):
    
    if n_clicks>0:
        clear_database()
        return html.H3([ok_icon,'Ranking cleared -- RELOAD the page'],style={'color': 'grey','font-family':'sans-serif' ,
                                                        'fontSize': 18,'verticalAlign': 'top','margin' : '10px',
                                                  'display': 'inline-block','horizontalAlign': 'center'}),
    
@app.callback(
    Output('change_param', 'children'),
    [Input('tabs_common_summary', 'value')])
def clicks(tab):
    df = pd.read_csv('param_wt.csv', header=0)
    return html.Div(children=[

        html.Div(children=[
        
        html.H3('Edit criterias weightage (must be equal to 100):',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 28,'verticalAlign': 'top','width':'100%',
                                                                       'margin' : '22px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'center'}),
        
        html.Div(children=[

                html.H3('(Does supplier currently have Supply Chain Finance  through banks?) %:',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dbc.Input(id="scf_wt",type='number', min=0, max=100, value=df['scf'][0]*100, step=1,
                        style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),
                ],style={'display': 'flex','margin' : '12px', 'flex':'row','horizontalAlign': 'center'}),
        

        html.Div(children=[

                html.H3('(Does Supplier currently have VMI agreement with Customer?) %:',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dbc.Input(id="VMI_wt",type='number', min=0, max=100, value=df['VMI'][0]*100, step=1,
                        style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),
                ],style={'display': 'flex','margin' : '12px', 'flex':'row','horizontalAlign': 'center'}),

        html.Div(children=[

                html.H3("(Is Supplier a critical supplier in Client's view?) %:",style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dbc.Input(id="critical_wt",type='number', min=0, max=100, value=df['critical'][0]*100, step=1,
                        style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'20px',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),
                ],style={'display': 'flex','margin' : '12px', 'flex':'row','horizontalAlign': 'center'}),
        
        

        html.Div(children=[

                html.H3("(Is Supplier inventory  greater than  20% of Client's  total inventory?) %:",style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dbc.Input(id="inventory_wt",type='number', min=0, max=100, value=df['inventory'][0]*100, step=1,
                        style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),
                ],style={'display': 'flex','margin' : '12px', 'flex':'row','horizontalAlign': 'center'}),
        
        html.Div(children=[

                html.H3('(Is payment terms to supplier 45 days or less?) %:',style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dbc.Input(id="pay_term_wt",type='number', min=0, max=100, value=df['pay_term'][0]*100, step=1,
                        style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),
                ],style={'display': 'flex','margin' : '12px', 'flex':'row','horizontalAlign': 'center'}),
        

        html.Div(children=[

                html.H3("(Is Supplier Lead time  > 90 days?) %:",style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dbc.Input(id="lead_time_wt",type='number', min=0, max=100, value=df['lead_time'][0]*100, step=1,
                        style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),
                ],style={'display': 'flex','margin' : '12px', 'flex':'row','horizontalAlign': 'center'}),

        html.Div(children=[

                html.H3("(Is Client business  greater than 20% of Supplier total business?) %:",style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dbc.Input(id="business_wt",type='number', min=0, max=100, value=df['business'][0]*100, step=1,
                        style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'20px',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),
                ],style={'display': 'flex','margin' : '12px', 'flex':'row','horizontalAlign': 'center'}),
        
        
        html.Div(children=[

                html.H3("(Are supplier Invoices overdue by 30 days or greater?) %:",style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),

                dbc.Input(id="overdue_wt",type='number', min=0, max=100, value=df['overdue'][0]*100, step=1,
                        style={'color': 'black','font-family':'sans-serif',
                                                            'fontSize': 18,'verticalAlign': 'top','width':'40%',
                                                                       'margin' : '10px',
                                                          'align-items': 'center','flex':1,
                                                            'display': 'flex',  'justify-content':'right'}),
                ],style={'display': 'flex','margin' : '12px', 'flex':'row','horizontalAlign': 'center'}),
        
        html.Div(id='wt_engine'),


    
            ],style={'border': 'px solid orange','background-color':'white','width':'75%','horizontalAlign': 'center',
                                 'border-radius': 20,'margin' : '0px','padding' : '20px','display':'inline-block'}),
        
        #html.Div(children=[html.Div(id='supplier_table_2')],style={'width':'30%','display':'inline-block','verticalAlign': 'top',}),

    ],style={'border': 'px solid orange','width':'100%','display':'inline-block',
                     'border-radius': 20,'margin' : '50px','horizontalAlign': 'center'})

@app.callback(
    Output('wt_engine', 'children'),
    [Input('scf_wt','value'),
    Input('VMI_wt','value'),
    Input('critical_wt','value'),
    Input('inventory_wt','value'),
    Input('pay_term_wt','value'),
    Input('lead_time_wt','value'),
    Input('business_wt','value'),
    Input('overdue_wt','value')])
def wt_engine(scf_wt,
            VMI_wt,
            critical_wt,
            inventory_wt,
            pay_term_wt,
            lead_time_wt,
            business_wt,
            overdue_wt):
    if any([arg is None for arg in [scf_wt,
                                    VMI_wt,
                                    critical_wt,
                                    inventory_wt,
                                    pay_term_wt,
                                    lead_time_wt,
                                    business_wt,
                                    overdue_wt,]]):
        return html.Label([warning_icon,'/!\ One param is <Null> - Please change it to <0>'],style={'font-family':'sans-serif' ,'fontSize': 22,'color':'red',
                                                       'width':'500px','display': 'inline-block','verticalAlign':'middle',
                                                        'margin' : '15px 15px 15px 15px'#'height':'40px'
                                                       }),
    
    else:
    
        rslt=scf_wt+VMI_wt+critical_wt+inventory_wt+pay_term_wt+lead_time_wt+business_wt+overdue_wt

        if (rslt/100)==1:
            return html.Div(children=[
                dbc.Button([change_icon,"Edit weightage"], id='button_change_param',
                           color="primary", className="me-1",n_clicks=0,
                      style={'margin' : '20px 20px 20px 20px','fontSize': 16,'font-family':'sans-serif',}),
                html.Div(id='change_param_click'),
            ])
        else:
            return html.Label([warning_icon,'The total should be 100% -- Total is now: '+str(rslt)+'%'],style={'font-family':'sans-serif' ,'fontSize': 22,'color':'red',
                                                       'width':'500px','display': 'inline-block','verticalAlign':'middle',
                                                        'margin' : '15px 15px 15px 15px'#'height':'40px'
                                                       }),
    
    
          


@app.callback(
    Output('change_param_click', 'children'),
    [Input('button_change_param', 'n_clicks'),
    Input('scf_wt','value'),
    Input('VMI_wt','value'),
    Input('critical_wt','value'),
    Input('inventory_wt','value'),
    Input('pay_term_wt','value'),
    Input('lead_time_wt','value'),
    Input('business_wt','value'),
    Input('overdue_wt','value')])
def clicks_param(n_clicks,
          scf_wt,
            VMI_wt,
            critical_wt,
            inventory_wt,
            pay_term_wt,
            lead_time_wt,
            business_wt,
            overdue_wt):
    
    if n_clicks>0:
        data = {'scf':[scf_wt/100],
        'VMI':[VMI_wt/100],
        'critical':[critical_wt/100],
        'inventory':[inventory_wt/100],
        'pay_term':[pay_term_wt/100],
        'lead_time':[lead_time_wt/100],
        'business':[business_wt/100],
        'overdue':[overdue_wt/100]}

        df = pd.DataFrame(data)

        df.to_csv('param_wt.csv', index=False)
        return html.H3([ok_icon,'Weightage updated'],style={'color': 'green','font-family':'sans-serif' ,
                                                        'fontSize': 18,'verticalAlign': 'top','margin' : '10px',
                                                  'display': 'inline-block','horizontalAlign': 'center'}),
    
    
app.run_server(port=8000, use_reloader=False)


# In[ ]:




