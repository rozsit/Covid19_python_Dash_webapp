# Import libraries
from dash import dcc, html, Dash
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import datetime
import skimage.io as io
import os

# Define constants for file paths
DATA_DIR = "C:\\Users\\grant\\022_Covid19 in Europe and Hungary\\data"
EUROPE_FILE = os.path.join(DATA_DIR, "covid19_europe.xlsx")
HUNGARY_FILE = os.path.join(DATA_DIR, "covid19_hungary.xlsx")
AGE_HUNGARY_FILE = os.path.join(DATA_DIR, "age_hungary.xlsx")
COUNTIES_HUNGARY_FILE = os.path.join(DATA_DIR, "counties_hungary_grouped.xlsx")

# Load data
europe = pd.read_excel(EUROPE_FILE)
hungary = pd.read_excel(HUNGARY_FILE)
hungary['Dátum'] = pd.to_datetime(hungary['Dátum'])
age_hungary = pd.read_excel(AGE_HUNGARY_FILE)
age_hungary_filt = age_hungary.drop([0, 1, 2, 3, 10], axis=0)
counties_hungary = pd.read_excel(COUNTIES_HUNGARY_FILE)

# Define Styles
DBC_CSS = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
CARD_STYLE = {'text-indent': '20px'}
CARD_STYLE_2 = {
    'height': '75px',
    'display': 'flex',
    'align-items': 'center',
    'font-size': '17px',
    'justify-content': 'center'
}
CARD_STYLE_3 = {
    'height': '56px',
    'display': 'flex',
    'align-items': 'center',
    'font-size': '17px',
    'justify-content': 'center'
}
RADIO_TAB_OPTIONS = [
    "Összes fertőzött",
    "Összes elhunyt",
    "Teljesen vakcinált",
    "Népesség",
    "Fertőzött/1000fő",
    "Elhunyt/1000fő"
]

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, DBC_CSS])
load_figure_template("cyborg")

# Define app layout
app.layout = dbc.Container([
    dcc.Markdown("#### *Covid19 Európában és Magyarországon*",
                 style={"textAlign": "center"}),
    dcc.Tabs(className="dbc", style={"fontSize": 20}, children=[
        dcc.Tab(label="Európa - 1.oldal", value="tab-1", children=[
            html.H1(id="map-title", style={"text-align": "center"}),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.Br(),
                    dbc.Card([
                        html.Br(),
                        dcc.RadioItems(id="output-radio",
                                       options=[
                                           "Interaktív térkép", "Animáció"],
                                       value="Interaktív térkép", inline=False, className="dbc"),
                        html.Br(),
                    ], style={'text-indent': '80px'}),
                    html.Br(),
                    dbc.Card([
                        html.Br(),
                        dcc.Markdown("###### Időszak: 2020.03.01 -"),
                        dcc.DatePickerSingle(
                            id="date picker",
                            min_date_allowed=europe["Dátum"].min(),
                            max_date_allowed=europe["Dátum"].max(),
                            initial_visible_month=europe["Dátum"].max(),
                            date=europe["Dátum"].max(),
                            className="dbc",
                            display_format="YYYY-MM-DD"
                        ),
                        html.Br(),
                    ], style={"text-align": "center"}),
                    html.Br(),
                    dbc.Card([
                        html.Br(),
                        dcc.Dropdown(
                            options=[
                                {"label": "Összes fertőzött",
                                    "value": "Összes fertőzött"},
                                {"label": "Összes elhunyt",
                                    "value": "Összes elhunyt"},
                                {"label": "Teljesen vakcinált",
                                    "value": "Teljesen vakcinált"},
                                {"label": "Fertőzöttek/1000 fő",
                                    "value": "Fertőzött/1000fő"},
                                {"label": "Elhunytak/1000 fő",
                                    "value": "Elhunyt/1000fő"},
                                {"label": "Vakcináltak/1000 fő",
                                    "value": "Vakcinált/1000fő"}
                            ],
                            value="Összes elhunyt",
                            className="dbc",
                            id="Column Dropdown",
                            style={"min-width": "75%"}
                        ),
                        html.Br()
                    ], style={"align-items": "center"}),
                    html.Br(),
                    dbc.Col([
                        dbc.Card(id="country", style={
                                 'align-items': 'center', 'font-weight': 'bold'}),
                        dbc.Card(id="allInfected", style=CARD_STYLE)
                    ]),
                    dbc.Col([
                        dbc.Card(id="allDied", style=CARD_STYLE),
                        dbc.Card(id="fullyVaccinated", style=CARD_STYLE)
                    ]),
                    dbc.Col([
                        dbc.Card(id="populationDensity", style=CARD_STYLE),
                        dbc.Card(id="population", style=CARD_STYLE)
                    ]),
                ], width=3),
                dbc.Col([
                    dcc.Graph(id="graph", style={"height": "590px"})
                ], width=9)
            ])
        ]),
        dcc.Tab(label="Európa - 2.oldal", value="tab-2", children=[
            html.H1(id="graph-title", style={"text-align": "center"}),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dbc.Card([
                        html.Br(),
                        dcc.Markdown("Válassz X tengelyt"),
                        dcc.RadioItems(id="score-radio",
                                       options=RADIO_TAB_OPTIONS,
                                       value="Összes fertőzött", inline=False, className="dbc"),
                        html.Br(),
                    ], style={'text-indent': '20px'}),
                    html.Br(),
                    dbc.Card([
                        html.Br(),
                        dcc.Markdown("Válassz Y tengelyt"),
                        dcc.RadioItems(id="score-radio2",
                                       options=RADIO_TAB_OPTIONS,
                                       value="Összes elhunyt", inline=False, className="dbc"),
                        html.Br(),
                    ], style={'text-indent': '20px'}),
                ], width=2),
                dbc.Col([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dbc.Card([
                        dcc.Graph(id="cross-filter-scatter", hoverData={'points': [{'customdata': ['Ország']}]},
                                  style={'height': '445px', 'width': '471px'}),
                    ], body=True, style={'height': '492px'})
                ], width=5),
                dbc.Col([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dbc.Card([
                        dcc.Graph(
                            id="x-line", style={'height': '442px', 'width': '471px'})
                    ], body=True, style={'height': '492px', 'width': '525px'})
                ], width=5)
            ])
        ]),
        dcc.Tab(label="Magyarország - 1.oldal", value="tab-3", children=[
            html.H1(id="hungary-title", style={"text-align": "center"}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.RangeSlider(
                            id="date",
                            min=hungary['Dátum'].min().timestamp(),
                            max=hungary['Dátum'].max().timestamp(),
                            # step in seconds (30 days)
                            step=30 * 24 * 60 * 60,
                            value=[pd.Timestamp(
                                '2020-08-20').timestamp(), pd.Timestamp('2021-06-30').timestamp()],
                            marks={int(date.timestamp()): {'label': date.strftime('%Y-%m'), 'style': {'font-size': '14px', 'font-weight': 'bold'}}
                                   for date in pd.date_range(hungary['Dátum'].min(), hungary['Dátum'].max(), freq='MS')}
                        )
                    ]),
                    html.Br(),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="graph_line", style={
                              'height': '300px'}, className="dbc"),
                ]),
                dbc.Col([
                    dcc.Graph(id="graph_area", style={
                              'height': '300px'}, className="dbc"),
                ]),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="graph_scatter", style={
                              'height': '300px'}, className="dbc"),
                ], width=6),
                dbc.Col([
                    dbc.Card(id="tab3Date", style=CARD_STYLE_2),
                    dbc.Card(id="activeInfected", style=CARD_STYLE_2),
                    dbc.Card(id="died", style=CARD_STYLE_2),
                    dbc.Card(id="recovered", style=CARD_STYLE_2),
                ]),
                dbc.Col([
                    dbc.Card(id="activeInfDiff",
                             style=CARD_STYLE_2),
                    dbc.Card(id="dailyInfected", style=CARD_STYLE_2),
                    dbc.Card(id="dailyDied", style=CARD_STYLE_2),
                    dbc.Card(id="dailyRecovered", style=CARD_STYLE_2),
                ]),
            ]),
        ]),
        dcc.Tab(label="Magyarország - 2.oldal", value="tab-4", children=[
            html.H1(id="hungary_2-title", style={"text-align": "center"}),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Card([
                            dcc.Checklist(id="filter",
                                          options=['Férfi', 'Nő'],
                                          value=["Férfi", "Nő"],
                                          inline=True,
                                          className="dbc"
                                          ),
                        ], style={"text-align": "center", "width": "968px", "height": "50px", "justify-content": "center"}),
                    ], style={"justify-content": "center"}),
                    html.Br(),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dcc.Graph(id="graph_pie", className="dbc"),
                            ], style={"height": "500px", "justify-content": "center"}),
                        ]),
                        dbc.Col([
                            dbc.Card([
                                dcc.Graph(id="graph_bar", className="dbc"),
                            ], style={"height": "500px", "justify-content": "center"}),
                        ]),
                    ]),
                ], width=9),
                dbc.Col([
                    dbc.Card([
                        dbc.Table.from_dataframe(
                            age_hungary,
                            striped=True,
                            bordered=True,
                            hover=True,
                            class_name="dbc",
                            style={'height': '580px'}
                        )
                    ]),
                ], width=3),
            ]),
            html.P("Adatok 2020.03.01 és 2021.06.01 között", style={
                   'font-style': 'italic', 'text-align': 'right'}),
        ]),
        dcc.Tab(label="Magyarország - 3.oldal", value="tab-5", children=[
            html.H1(id="hungary_3-title", style={"text-align": "center"}),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(id="graph_sunburst", style={
                                  'height': '700px'}, className="dbc"),
                    ], style={"height": "650px", "justify-content": "center"}),
                ], width=7),
                dbc.Col([
                    dbc.Row([
                        dbc.Card([
                            dcc.Graph(id="graph_img", style={
                                      'height': '380px'}, className="dbc"),
                        ], style={"justify-content": "center"}),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card(id="county5", style=CARD_STYLE_3),
                            dbc.Card(id="allInfected5", style=CARD_STYLE_3),
                            dbc.Card(id="district5", style=CARD_STYLE_3),
                            dbc.Card(id="village5", style=CARD_STYLE_3),
                        ]),
                        dbc.Col([
                            dbc.Card(id="city5", style=CARD_STYLE_3),
                            dbc.Card(id="population5", style=CARD_STYLE_3),
                            dbc.Card(id="area5", style=CARD_STYLE_3),
                            dbc.Card(id="populationDensity5",
                                     style=CARD_STYLE_3),
                        ]),
                    ]),
                ]),
            ]),
            html.P("Térképek: Copyright Zentai László --- Adatok 2020.04.01 és 2021.04.30 között, Budapest nélkül",
                   style={'font-size': 13, 'font-style': 'italic', 'text-align': 'right'}),
        ]),
    ])
])


# App callbacks
# Tab1 callbacks
@app.callback(
    Output("graph", "figure"),
    [Input("date picker", "date"),
     Input("Column Dropdown", "value"),
     Input("output-radio", "value")]
)
def tab1MapChart(date, column, output_option):
    if not date or not column:
        raise PreventUpdate

    df = europe.loc[europe["Dátum"].eq(date)]

    if output_option == "Animáció":
        all_columns = {col: False for col in europe.columns}
        fig = px.choropleth(
            europe.sort_values('Dátum', ascending=True),
            locations="Ország",
            color=column,
            locationmode='country names',
            scope="europe",
            hover_data=all_columns,
            animation_frame='Dátum').update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_colorbar_x=.73,
            paper_bgcolor="black"
        )
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 0.1
    else:
        fig = px.choropleth(
            df,
            locations="Ország",
            color=column,
            locationmode="country names",
            scope="europe",
            hover_data=['Ország'],
            custom_data=["Ország"]
        ).update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_colorbar_x=.77,
            paper_bgcolor="black",
            coloraxis_colorbar=dict(title="")
        )
    return fig


@app.callback(
    [Output("country", "children"),
     Output("allInfected", "children"),
     Output("allDied", "children"),
     Output("fullyVaccinated", "children"),
     Output("populationDensity", "children"),
     Output("population", "children")],
    [Input("graph", "hoverData"),
     Input("date picker", "date")]
)
def tab1ReportCard(hoverData, date):
    tab1_default_values = {
        "country": "Ország: Magyarország",
        "allInfected": "Összes fertőzött: 807,910 fő",
        "allDied": "Összes elhunyt: 29,981 fő",
        "fullyVaccinated": "Teljesen vakcinált: 4,916,927 fő",
        "populationDensity": "Népsűrűség: 108 fő/km2",
        "population": "Népesség: 9,967,304 fő"
    }

    if not hoverData or "points" not in hoverData:
        return list(tab1_default_values.values())

    country_name = hoverData["points"][0].get("customdata", [])[0]
    df_riport = europe.query(
        "Ország == @country_name").loc[europe["Dátum"].eq(date)]

    tab1_updated_values = {
        "country": f"Ország: {country_name}",
        "allInfected": f"Összes fertőzött: {int(df_riport['Összes fertőzött'].max()):,} fő",
        "allDied": f"Összes elhunyt: {int(df_riport['Összes elhunyt'].max()):,} fő",
        "fullyVaccinated": f"Teljesen vakcinált: {int(df_riport['Teljesen vakcinált'].max()):,} fő",
        "populationDensity": f"Népsűrűség: {int(df_riport['Népsűrűség'].max()):,} fő/km2",
        "population": f"Népesség: {int(df_riport['Népesség'].max()):,} fő"
    }

    return list(tab1_updated_values.values())


# Tab2 callbacks
@app.callback(
    Output("cross-filter-scatter", "figure"),
    Input("score-radio", "value"),
    Input("score-radio2", "value")
)
def tab2ScatterChart(x, y):
    max_values = europe.groupby("Ország").max().reset_index()
    fig = px.scatter(
        max_values,
        x=x,
        y=y,
        size=y,
        opacity=.75,
        hover_name="Ország",
        custom_data=["Ország"],
    )
    fig.update_layout(coloraxis_showscale=False)

    return fig


@app.callback(
    Output("x-line", "figure"),
    Input("cross-filter-scatter", "hoverData"),
    Input("score-radio", "value")
)
def tab2LineChart(hoverData, y):

    if hoverData and "points" in hoverData and hoverData["points"][0].get(
            "customdata") == ["Ország"]:
        country = 'Hungary'

    else:
        country = hoverData["points"][0]["customdata"][0]

    df = europe.query("Ország == @country")
    df_filtered = df[df[y] != 0]

    fig = px.line(
        df_filtered,
        x="Dátum",
        y=y,
        title=f"{country.title()}",
        line_shape='hv'
    ).update_xaxes(
        tickfont=dict(size=12),
        tickangle=45,
    )
    fig.update_xaxes(title_text="", showgrid=False, title_standoff=20)
    fig.update_layout(title=dict(x=0.5))

    return fig


# Tab3 callbacks
@app.callback(
    Output('graph_line', 'figure'),
    Output('graph_area', 'figure'),
    Output('graph_scatter', 'figure'),
    Input("date", "value")
)
def tab3Charts(date_range):

    start_date = datetime.datetime.fromtimestamp(date_range[0])
    end_date = datetime.datetime.fromtimestamp(date_range[1])

    hungary_filtered = hungary[(hungary['Dátum'] >= start_date) & (
        hungary['Dátum'] <= end_date)]

    fig = px.line(
        hungary_filtered,
        x='Dátum',
        y=['Napi új gyógyult', 'Napi új fertőzött', 'Aktív fertőzöttek változása'],
        custom_data=['Dátum'],
        hover_data=['Dátum']
    )
    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=1.2,
            xanchor="left",
            x=0.01,
            title="",
            orientation="h"),
        margin=dict(
            l=0,
            r=30,
            t=10,
            b=10))
    fig.update_xaxes(title_text="", showgrid=False)
    fig.update_yaxes(title_text="", showgrid=False)

    fig2 = px.area(
        hungary_filtered,
        x='Dátum',
        y=['Gyógyult', 'Aktív fertőzött'])
    fig2.update_layout(
        legend=dict(
            yanchor="top",
            y=1.2,
            xanchor="left",
            x=0.28,
            title="",
            orientation="h"),
        margin=dict(
            l=0,
            r=30,
            t=10,
            b=10))
    fig2.update_xaxes(title_text="", showgrid=False)
    fig2.update_yaxes(title_text="", showgrid=False)

    fig3 = px.scatter(
        hungary_filtered,
        x='Aktív fertőzött',
        y='Napi új elhunyt',
        opacity=.55,
        color='Napi új elhunyt',
    )
    fig3.update_layout(margin=dict(l=0, r=30, t=20, b=10),
                       coloraxis_showscale=False)

    return fig, fig2, fig3


@app.callback(
    Output("tab3Date", "children"),
    Output("activeInfected", "children"),
    Output("died", "children"),
    Output("recovered", "children"),
    Output("activeInfDiff", "children"),
    Output("dailyDied", "children"),
    Output("dailyRecovered", "children"),
    Output("dailyInfected", "children"),
    Input("graph_line", "hoverData"),
)
def tab3ReportCard(hoverData):

    tab3_default_values = {
        "tab3Date": "2021-06-30",
        "activeInfected": "Aktív fertőzött: 39,354 fő",
        "died": "Elhunyt: 29,992 fő",
        "recovered": "Gyógyult: 738,782 fő",
        "activeInfDiff": "Aktív fertőzöttek változása: -189",
        "dailyDied": "Napi új elhunyt: 1 fő",
        "dailyRecovered": "Napi új gyógyult: 240 fő",
        "dailyInfected": "Napi új fertőzött: 52 fő"
    }

    if hoverData is None or "points" not in hoverData or not hoverData["points"][0].get("customdata"):
        return list(tab3_default_values.values())

    customdata = hoverData["points"][0]["customdata"]
    date = pd.to_datetime(customdata[0])
    hungary_filtered = hungary.loc[hungary['Dátum'] == date]

    tab3_updated_values = {
        "tab3Date": f"Dátum: {date.strftime('%Y-%m-%d')}",
        "activeInfected": f"Aktív fertőzött: {
            int(hungary_filtered['Aktív fertőzött'].max()):,} fő",
        "died": f"Elhunyt: {
            int(hungary_filtered['Elhunyt'].max()):,} fő",
        "recovered": f"Gyógyult: {
            int(hungary_filtered['Gyógyult'].max()):,} fő",
        "activeInfDiff": f"Aktív fertőzöttek változása: {
            int(hungary_filtered['Aktív fertőzöttek változása'].max()):,} fő",
        "dailyDied": f"Napi új elhunyt: {
            int(hungary_filtered['Napi új elhunyt'].max()):,} fő",
        "dailyRecovered": f"Napi új gyógyult: {
            int(hungary_filtered['Napi új gyógyult'].max()):,} fő",
        "dailyInfected": f"Napi új fertőzött: {
            int(hungary_filtered['Napi új fertőzött'].max()):,} fő"
    }

    return list(tab3_updated_values.values())


# Tab4 callbacks
@app.callback(
    Output('graph_pie', 'figure'),
    Output('graph_bar', 'figure'),
    Input("filter", "value")
)
def tab4Charts(selected_genres):
    if not selected_genres:
        raise PreventUpdate

    filtered_data = age_hungary_filt.loc[:,
                                         selected_genres + ['Életkori csoport']]
    pie_data = filtered_data.groupby('Életkori csoport')[
        selected_genres].sum().sum(axis=1).reset_index()

    fig1 = px.pie(pie_data,
                  names='Életkori csoport',
                  values=0,
                  hole=0.5,
                  title="")
    fig1.update_layout(title={
        'text': f"Elhunytak aránya 40-99 életkor között",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        showlegend=False,
    )
    fig1.update_traces(
        textposition='inside',
        textinfo='label+percent',
        insidetextorientation='horizontal',
        textfont_color='white',
        textfont_size=16)
    bar_data = filtered_data.groupby('Életkori csoport')[
        selected_genres].sum().reset_index()

    fig2 = px.bar(bar_data,
                  x='Életkori csoport',
                  y=selected_genres,
                  barmode='group',
                  title="")
    fig2.update_layout(
        yaxis_title='',
        title={
            'text': f"Elhunytak száma életkori csoportok szerint",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        legend=dict(
            title=""))

    return fig1, fig2


# Tab5 callbacks
@app.callback(
    Output('graph_sunburst', 'figure'),
    Input("filter", "value")
)
def tab5Charts(dummy):

    fig = px.sunburst(
        counties_hungary,
        path=['Régió', 'Megyék'],
        values='Összes fertőzött',
        title=""
    )
    fig.update_traces(rotation=90)
    fig.update_layout(margin=dict(t=60, b=10, r=10, l=10),
                      title={
        'text': f"Összes fertőzött megyék, régiók szerint",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
    )
    return fig


@app.callback(
    Output('graph_img', 'figure'),
    Input("graph_sunburst", "hoverData")
)
def tab5Images(hoverData):

    if hoverData is None or "points" not in hoverData:
        county = 'PES'
    else:
        county = hoverData["points"][0]['label']

    # path = 'geo/' + county + '.gif'
    path = 'C:\\Users\\grant\\022_Covid19 in Europe and Hungary\\geo\\' + county + '.gif'

    img = io.imread(path)

    if len(img.shape) == 4:
        img = img[0]
    fig = px.imshow(img)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    return fig


@app.callback(
    Output('county5', 'children'),
    Output('allInfected5', 'children'),
    Output('district5', 'children'),
    Output('village5', 'children'),
    Output('city5', 'children'),
    Output('population5', 'children'),
    Output('area5', 'children'),
    Output('populationDensity5', 'children'),
    Input("graph_sunburst", "hoverData")
)
def tab5ReportCard(hoverData):

    defaultCounty = 'PES'

    if hoverData is None or "points" not in hoverData:
        county = defaultCounty
    else:
        countyLabel = hoverData["points"][0]['label']
        if countyLabel not in counties_hungary['Megyék'].values:
            county = defaultCounty
        else:
            county = countyLabel

    counties_filt = counties_hungary.query("Megyék == @county")

    tab5_updated_values = {
        "county5": f"Megye: {county}",
        "allInfected5": f"Összes fertőzött: {
            int(counties_filt['Összes fertőzött'].max()):,} fő",
        "district5": f"Járások száma: {
            int(counties_filt['Járás'].max()):,}",
        "village5": f"Települések száma: {
            int(counties_filt['Település'].max()):,}",
        "city5": f"Városok száma: {
            int(counties_filt['Város'].max()):,}",
        "population5": f"Népesség: {
            int(counties_filt['Népesség'].max()):,} fő",
        "area5": f"Terület: {
            int(counties_filt['Terület'].max()):,} km2",
        "populationDensity5": f"Népsűrűség: {
            int(counties_filt['Népsűrűség'].max()):,} fő/km2"
    }

    return list(tab5_updated_values.values())


if __name__ == "__main__":
    app.run_server(port=8050)
