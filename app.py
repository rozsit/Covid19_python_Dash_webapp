# import libraries
from dash import dcc, html, Dash
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import datetime
from datetime import date
import plotly.graph_objects as go
import skimage.io as io

# read necessary files
europe = pd.read_excel(
    "C:\\Users\\grant\\022_Covid19 in Europe and Hungary\\data\\covid19_europe.xlsx")
hungary = pd.read_excel(
    "C:\\Users\\grant\\022_Covid19 in Europe and Hungary\\data\\covid19_hungary.xlsx")
hungary['Dátum'] = pd.to_datetime(hungary['Dátum'])
age_hungary = pd.read_excel(
    "C:\\Users\\grant\\022_Covid19 in Europe and Hungary\\data\\age_hungary.xlsx")
age_hungary_filt = age_hungary.drop([0, 1, 2, 3, 10], axis=0)
counties_hungary = pd.read_excel(
    "C:\\Users\\grant\\022_Covid19 in Europe and Hungary\\data\\counties_hungary_grouped.xlsx")

# define css style
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# start Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, dbc_css])

# define styles
load_figure_template("CYBORG")
card_style = {'text-indent': '20px'}
card_style_2 = {'height': '75px', 'display': 'flex',
                'align-items': 'center', 'font-size': '17px', 'justify-content': 'center'}
card_style_3 = {'height': '56px', 'display': 'flex',
                'align-items': 'center', 'font-size': '17px', 'justify-content': 'center'}
radio_tab_options = ["Összes fertőzött", "Összes elhunyt", "Teljesen vakcinált",
                     "Népesség", "Fertőzött/1000fő", "Elhunyt/1000fő"]

# app layout
app.layout = dbc.Container([
    dcc.Markdown("#### * Covid19 Európában és Magyarországon *",
                 style={"textAlign": "center"}),
    dcc.Tabs(className="dbc", style={"fontSize": 20},
             children=[
        # -------------------- TAB 1 layout start --------------------
        dcc.Tab(label="Európa - 1.oldal", value="tab-1",
                children=[html.H1(id="map-title", style={"text-align": "center"}),
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
                                      dcc.Markdown(
                                          "###### Időszak: 2020.03.01 -"),
                                      dcc.DatePickerSingle(
                                          id="Date Picker",
                                          min_date_allowed=europe["Dátum"].min(
                                          ),
                                          max_date_allowed=europe["Dátum"].max(
                                          ),
                                          initial_visible_month=europe["Dátum"].max(
                                          ),
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
                                          options=[{"label": "Összes fertőzött", "value": "Összes fertőzött"},
                                                   {"label": "Összes elhunyt",
                                                    "value": "Összes elhunyt"},
                                                   {"label": "Teljesen vakcinált",
                                                    "value": "Teljesen vakcinált"},
                                                   {"label": "Fertőzöttek/1000 fő",
                                                    "value": "Fertőzött/1000fő"},
                                                   {"label": "Elhunytak/1000 fő",
                                                    "value": "Elhunyt/1000fő"},
                                                   {"label": "Vakcináltak/1000 fő", "value": "Vakcinált/1000fő"}],
                                          value="Összes elhunyt",
                                          className="dbc",
                                          id="Column Dropdown",
                                          style={"min-width": "75%"}
                                      ),
                                      html.Br()
                                  ], style={
                                      "align-items": "center"}),
                                  html.Br(),
                                  dbc.Col([
                                      dbc.Card(id="Ország", style={
                                          'align-items': 'center', 'font-weight': 'bold'}),
                                      dbc.Card(id="Összes_fertőzött",
                                               style=card_style)
                                  ]),
                                  dbc.Col([
                                      dbc.Card(id="Összes_elhunyt",
                                               style=card_style),
                                      dbc.Card(id="Teljesen_vakcinált",
                                               style=card_style)
                                  ]),
                                  dbc.Col([
                                      dbc.Card(id="Népsűrűség",
                                               style=card_style),
                                      dbc.Card(id="Népesség", style=card_style)
                                  ]),
                              ], width=3),
                              dbc.Col([
                                  dcc.Graph(id="graph", style={"height": "590px"})], width=9)
                          ])
                          ]
                ),
        # -------------------- TAB 1 layout end ----------------------
        # -------------------- TAB 2 layout start --------------------
        dcc.Tab(label="Európa - 2.oldal", value="tab-2",
                children=[html.H1(id="graph-title", style={"text-align": "center"}),
                          dbc.Row([
                              dbc.Col([
                                  html.Br(),
                                  html.Br(),
                                  html.Br(),
                                  dbc.Card([
                                      html.Br(),
                                      dcc.Markdown("Válassz X tengelyt"),
                                      dcc.RadioItems(id="score-radio",
                                                     options=radio_tab_options,
                                                     value="Összes fertőzött", inline=False, className="dbc"),
                                      html.Br(),
                                  ], style={'text-indent': '20px'}),
                                  html.Br(),
                                  dbc.Card([
                                      html.Br(),
                                      dcc.Markdown("Válassz Y tengelyt"),
                                      dcc.RadioItems(id="score-radio2",
                                                     options=radio_tab_options,
                                                     value="Összes elhunyt", inline=False, className="dbc"),
                                      html.Br(),
                                  ], style={'text-indent': '20px'}),
                              ], width=2),
                              dbc.Col([
                                  html.Br(),
                                  html.Br(),
                                  html.Br(),
                                  dbc.Card([
                                      dcc.Graph(id="cross-filter-scatter", hoverData={'points': [
                                          {'customdata': ['Ország']}]}, style={'height': '475px', 'width': '505px'}),
                                  ], body=True, style={'height': '492px'})
                              ], width=5),
                              dbc.Col([
                                  html.Br(),
                                  html.Br(),
                                  html.Br(),
                                  dbc.Card([
                                      dcc.Graph(
                                          id="x-line", style={'height': '472px', 'width': '507px'})
                                  ], body=True, style={'height': '492px', 'width': '525px'})
                              ], width=5)
                          ])
                          ]
                ),
        # -------------------- TAB 2 layout end --------------------
        # -------------------- TAB 3 layout start ------------------
        dcc.Tab(label="Magyarország - 1.oldal", value="tab-3",
                children=[html.H1(id="hungary-title", style={"text-align": "center"}),
                          dbc.Row([  # 1.sor
                              dbc.Col([
                                  dbc.Card([
                                      dcc.RangeSlider(
                                          id="date",
                                          min=hungary['Dátum'].min(
                                          ).timestamp(),
                                          max=hungary['Dátum'].max(
                                          ).timestamp(),
                                          # step in seconds (30 days)
                                          step=30*24*60*60,
                                          value=[pd.Timestamp(
                                              '2020-08-20').timestamp(), pd.Timestamp('2021-06-30').timestamp()],
                                          marks={int(date.timestamp()): {'label': date.strftime('%Y-%m'), 'style': {'font-size': '14px', 'font-weight': 'bold'}}
                                                 for date in pd.date_range(hungary['Dátum'].min(), hungary['Dátum'].max(), freq='MS')}
                                      )
                                  ]
                                  ),
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
                                  dbc.Card(id="Dátum", style=card_style_2),
                                  dbc.Card(id="Aktív_fertőzött",
                                           style=card_style_2),
                                  dbc.Card(id="Elhunyt",
                                           style=card_style_2),
                                  dbc.Card(id="Gyógyult",
                                           style=card_style_2),
                              ]),
                              dbc.Col([
                                  dbc.Card(
                                      id="Aktív_fertőzöttek_változása", style=card_style_2),
                                  dbc.Card(id="Napi_új_fertőzött",
                                           style=card_style_2),
                                  dbc.Card(id="Napi_új_elhunyt",
                                           style=card_style_2),
                                  dbc.Card(id="Napi_új_gyógyult",
                                           style=card_style_2),
                              ]),
                          ]),
                          ]),
        # -------------------- TAB 3 layout end --------------------
        # -------------------- TAB 4 layout start ------------------
        dcc.Tab(label="Magyarország - 2.oldal", value="tab-4",
                children=[html.H1(id="hungary_2-title", style={"text-align": "center"}),
                          html.Br(),
                          html.Br(),
                          dbc.Row([
                              dbc.Col([
                                  dbc.Row([
                                      dbc.Card([
                                          dcc.Checklist(id="filter",
                                                        options=[
                                                            'Férfi', 'Nő'],
                                                        value=["Férfi", "Nő"],
                                                        inline=True,
                                                        className="dbc"
                                                        ),
                                      ], style={"text-align": "center",
                                                "width": "968px",
                                                "height": "50px",
                                                "justify-content": "center"}),
                                  ], style={"justify-content": "center"}),
                                  html.Br(),
                                  html.Br(),
                                  dbc.Row([
                                      dbc.Col([
                                          dbc.Card([
                                              dcc.Graph(id="graph_pie",
                                                        className="dbc"),
                                          ], style={"height": "500px", "justify-content": "center"}),
                                      ]),
                                      dbc.Col([
                                          dbc.Card([
                                              dcc.Graph(id="graph_bar",
                                                        className="dbc"),
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
                          ],
                ),
                    html.P("Adatok 2020.03.01 és 2021.06.01 között", style={
                        'font-style': 'italic', 'text-align': 'right'}),
                ]),
        # -------------------- TAB 4 layout end --------------------
        # -------------------- TAB 5 layout start ------------------
        dcc.Tab(label="Magyarország - 3.oldal", value="tab-5",
                children=[html.H1(id="hungary_3-title", style={"text-align": "center"}),
                          html.Br(),
                          dbc.Row([
                              dbc.Col([
                                  dbc.Card([
                                      dcc.Graph(id="graph_sunburst",
                                                style={'height': '700px'},
                                                className="dbc"),
                                  ], style={
                                      "height": "650px",
                                      "justify-content": "center"}),
                              ], width=7),
                              dbc.Col([
                                  dbc.Row([
                                      dbc.Card([
                                          dcc.Graph(id="graph_img",
                                                    style={
                                                        'height': '380px'},
                                                    className="dbc"),
                                      ], style={
                                          "justify-content": "center"}),
                                  ]),
                                  html.Br(),
                                  dbc.Row([
                                      dbc.Col([
                                          dbc.Card(
                                              id="Megye", style=card_style_3),
                                          dbc.Card(id="Összes_fert",
                                                   style=card_style_3),
                                          dbc.Card(
                                              id="Járás", style=card_style_3),
                                          dbc.Card(id="Település",
                                                   style=card_style_3),
                                      ]),
                                      dbc.Col([
                                          dbc.Card(
                                              id="Város", style=card_style_3),
                                          dbc.Card(
                                              id="Népes", style=card_style_3),
                                          dbc.Card(id="Terület",
                                                   style=card_style_3),
                                          dbc.Card(id="Népsűrű",
                                                   style=card_style_3),
                                      ]),
                                  ]),
                              ]),
                          ]),
                          html.P("Térképek: Copyright Zentai László --- Adatok 2020.04.01 és 2021.04.30 között, Budapest nélkül",
                                 style={'font-size': 13, 'font-style': 'italic', 'text-align': 'right'}),
                          ]),
        # -------------------- TAB 5 layout end --------------------
    ]
    )
])
# app callbacks
# -------------------- TAB 1 callback start --------------------


@app.callback(
    Output("graph", "figure"),
    Input("Date Picker", "date"),
    Input("Column Dropdown", "value"),
    Input("output-radio", "value"),
)
def plot_europe(date, column, output_option):
    if not date and column:
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
            plot_bgcolor="black",
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
            plot_bgcolor="black",
            paper_bgcolor="black",
            coloraxis_colorbar=dict(title="")
        )
    return fig


@app.callback(
    Output("Ország", "children"),
    Output("Összes_fertőzött", "children"),
    Output("Összes_elhunyt", "children"),
    Output("Teljesen_vakcinált", "children"),
    Output("Népsűrűség", "children"),
    Output("Népesség", "children"),
    Input("graph", "hoverData"),
    Input("Date Picker", "date")
)
def report_card(hoverData, date):

    if hoverData is None or "points" not in hoverData:
        return "Ország: Hungary", "Összes fertőzött: 807,910", "Összes elhunyt: 29,981", "Teljesen vakcinált: 4,916,927", "Népsűrűség: 108", "Népesség: 9,967,304"

    orszag = hoverData["points"][0]["customdata"][0]
    df_report = europe.query("Ország == @orszag").loc[europe["Dátum"].eq(date)]

    Ország = f"Ország: {orszag}"
    Összes_fertőzött = f"Összes fertőzött: {
        int(df_report['Összes fertőzött'].max()):,} fő"
    Összes_elhunyt = f"Összes elhunyt: {
        int(df_report['Összes elhunyt'].max()):,} fő"
    Teljesen_vakcinált = f"Teljesen vakcinált: {
        int(df_report['Teljesen vakcinált'].max()):,} fő"
    Népsűrűség = f"Népsűrűség: {int(df_report['Népsűrűség'].max()):,} fő/km2"
    Népesség = f"Népesség: {int(df_report['Népesség'].max()):,} fő"

    return Ország, Összes_fertőzött, Összes_elhunyt, Teljesen_vakcinált, Népsűrűség, Népesség
# -------------------- TAB 1 callback end ---------------------
# -------------------- TAB 2 callback start --------------------


@app.callback(
    Output("cross-filter-scatter", "figure"),
    Input("score-radio", "value"),
    Input("score-radio2", "value")
)
def score_scatter(x, y):
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
def update_line(hoverData, y):

    if hoverData and "points" in hoverData and hoverData["points"][0].get("customdata") == ["Ország"]:
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
# -------------------- TAB 2 callback end --------------------
# -------------------- TAB 3 callback start ------------------


@app.callback(
    Output('graph_line', 'figure'),
    Output('graph_area', 'figure'),
    Output('graph_scatter', 'figure'),
    Input("date", "value")
)
def charts(date_range):

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
    fig.update_layout(legend=dict(yanchor="top", y=1.2, xanchor="left", x=0.01, title="", orientation="h"),
                      margin=dict(l=0, r=30, t=10, b=10))
    fig.update_xaxes(title_text="", showgrid=False)
    fig.update_yaxes(title_text="", showgrid=False)

    fig2 = px.area(
        hungary_filtered,
        x='Dátum',
        y=['Gyógyult', 'Aktív fertőzött'])
    fig2.update_layout(legend=dict(yanchor="top", y=1.2, xanchor="left", x=0.28, title="", orientation="h"),
                       margin=dict(l=0, r=30, t=10, b=10))
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
    Output("Dátum", "children"),
    Output("Aktív_fertőzött", "children"),
    Output("Elhunyt", "children"),
    Output("Gyógyult", "children"),
    Output("Aktív_fertőzöttek_változása", "children"),
    Output("Napi_új_elhunyt", "children"),
    Output("Napi_új_gyógyult", "children"),
    Output("Napi_új_fertőzött", "children"),
    Input("graph_line", "hoverData"),
)
def report_card(hoverData):

    if hoverData is None or "points" not in hoverData or not hoverData["points"][0].get("customdata"):
        Dátum = "2021-06-30"
        Aktív_fertőzött = "Aktív fertőzött: 39,354"
        Elhunyt = "Elhunyt: 29,992"
        Gyógyult = "Gyógyult: 738,782"
        Aktív_fertőzöttek_változása = "Aktív fertőzöttek változása: -189"
        Napi_új_elhunyt = "Napi új elhunyt: 1"
        Napi_új_gyógyult = "Napi új gyógyult: 240"
        Napi_új_fertőzött = "Napi új fertőzött: 52"

    else:
        customdata = hoverData["points"][0]["customdata"]
        date = pd.to_datetime(customdata[0])
        hungary_filtered = hungary.loc[hungary['Dátum'] == date]

        Dátum = f"Dátum: {date.strftime('%Y-%m-%d')}"
        Aktív_fertőzött = f"Aktív fertőzött: {
            int(hungary_filtered['Aktív fertőzött'].max()):,} fő"
        Elhunyt = f"Elhunyt: {int(hungary_filtered['Elhunyt'].max()):,} fő"
        Gyógyult = f"Gyógyult: {int(hungary_filtered['Gyógyult'].max()):,} fő"
        Aktív_fertőzöttek_változása = f"Aktív fertőzöttek változása: {
            int(hungary_filtered['Aktív fertőzöttek változása'].max()):,} fő"
        Napi_új_elhunyt = f"Napi új elhunyt: {
            int(hungary_filtered['Napi új elhunyt'].max()):,} fő"
        Napi_új_gyógyult = f"Napi új gyógyult: {
            int(hungary_filtered['Napi új gyógyult'].max()):,} fő"
        Napi_új_fertőzött = f"Napi új fertőzött: {
            int(hungary_filtered['Napi új fertőzött'].max()):,} fő"

    return Dátum, Aktív_fertőzött, Elhunyt, Gyógyult, Aktív_fertőzöttek_változása, Napi_új_elhunyt, Napi_új_gyógyult, Napi_új_fertőzött
# -------------------- TAB 3 callback end --------------------
# -------------------- TAB 4 callback start ------------------


@app.callback(
    Output('graph_pie', 'figure'),
    Output('graph_bar', 'figure'),
    Input("filter", "value")
)
def update_graphs(selected_genres):
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
    fig2.update_layout(yaxis_title='',
                       title={
                           'text': f"Elhunytak száma életkori csoportok szerint",
                           'y': 0.95,
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'},
                       legend=dict(title=""))

    return fig1, fig2
# -------------------- TAB 4 callback end --------------------
# -------------------- TAB 5 callback start ------------------


@app.callback(
    Output('graph_sunburst', 'figure'),
    Input("filter", "value")
)
def sun_graph(dummy):

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
def img_graph(hoverData):

    if hoverData is None or "points" not in hoverData:
        county = 'PES'
    else:
        county = hoverData["points"][0]['label']

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
    Output('Megye', 'children'),
    Output('Összes_fert', 'children'),
    Output('Járás', 'children'),
    Output('Település', 'children'),
    Output('Város', 'children'),
    Output('Népes', 'children'),
    Output('Terület', 'children'),
    Output('Népsűrű', 'children'),
    Input("graph_sunburst", "hoverData")
)
def img_graph(hoverData):

    default_county = 'PES'

    if hoverData is None or "points" not in hoverData:
        county = default_county

    else:
        county_label = hoverData["points"][0]['label']

        if county_label not in counties_hungary['Megyék'].values:
            county = default_county

        else:
            county = county_label

    counties_filt = counties_hungary.query("Megyék == @county")

    Megye = f"Megye: {county}"
    Összes_fert = f"Összes fertőzött: {
        int(counties_filt['Összes fertőzött'].max()):,} fő"
    Járás = f"Járások száma: {int(counties_filt['Járás'].max()):,}"
    Település = f"Települések száma: {int(counties_filt['Település'].max()):,}"
    Város = f"Városok száma: {int(counties_filt['Város'].max()):,}"
    Népes = f"Népesség: {int(counties_filt['Népesség'].max()):,} fő"
    Terület = f"Terület: {int(counties_filt['Terület'].max()):,} km2"
    Népsűrű = f"Népsűrűség: {int(counties_filt['Népsűrűség'].max()):,} fő/km2"

    return Megye, Összes_fert, Járás, Település, Város, Népes, Terület, Népsűrű


# -------------------- TAB 5 callback end --------------------
if __name__ == "__main__":
    app.run_server(port=8050)
