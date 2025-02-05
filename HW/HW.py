import marimo

__generated_with = "0.11.0"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    import panel as pn
    import plotly.express as px
    from plotly.graph_objects import Figure, Scatter, Bar, Choropleth
    from plotly.subplots import make_subplots
    import numpy as np
    return Bar, Choropleth, Figure, Scatter, make_subplots, np, pd, pn, px


@app.cell
def _(pn):
    pn.extension("plotly")
    return


@app.cell
def _(pd):
    df = pd.read_csv('/Users/11nho/Documents/School/690V/HW/data/eduwa.csv')
    df.head()
    return (df,)


@app.cell
def _(df):
    newdf = df[["County","Reduced.Lunch"]]
    reducedLunchCounty = newdf.groupby(['County']).sum().sort_values(by="Reduced.Lunch",ascending=False).reset_index()
    reducedLunchCounty['Cumulative'] = 100 * (reducedLunchCounty["Reduced.Lunch"].cumsum()/reducedLunchCounty["Reduced.Lunch"].sum())
    reducedLunchCounty
    return newdf, reducedLunchCounty


@app.cell
def _(Bar, Figure, Scatter, np, pn, reducedLunchCounty):
    def graph_pareto(dataframe, col):
        df = dataframe.copy()

        data = [
            Bar(
              name = "Count",  
              x = df.County,
              y = df[f'{col}'], 
              marker= {"color": list(np.repeat('rgb(71, 71, 135)', 5)) + list(np.repeat('rgb(112, 111, 211)', len(df.index) - 5))}
            ),
            Scatter(
              line= {
                "color": "rgb(192, 57, 43)", 
                "width": 3
              }, 
              name = "Percentage", 
              x = df.County,
              y = df['Cumulative'], 
              yaxis= "y2",
              mode='lines+markers'
            ),
        ]

        layout = {
          # Title Graph
          "title": {
            'text': "Reduced Lunch by County<br><span style='font-size:15px; color: rgb(100, 100, 100);'>Reduced Lunch Individuals in Schools in Washington State</span>",
            'font': dict(size=30),
          },

          # Source/Caption
          "annotations": [{
            'xref': 'paper',
            'yref': 'paper',
            'x': 1, 
            'y': -0.5,
            'showarrow': False,
            'text': '<span style="font-size:12px; color: gray; font-family: Courier New, monospace;">Source: National Center for Education Statistics</span>',
            'align': 'right'
          }],

          # Font 
          "font": {
            "size": 14, 
            "color": "rgb(44, 44, 84)", 
            "family": "Times New Roman, monospace"
          },

          # Graph Box 
          "margin": {
            "b": 120, 
            "l": 50, 
            "r": 50, 
            "t": 100,
          }, 
          "height": 400, 

          # Graph Box 
          "plot_bgcolor": "rgb(255, 255, 255)", 


          # Settings Legend
          "legend": {
            "x": 0.79, 
            "y": 1.2, 
            "font": {
              "size": 12, 
              "color": "rgb(44, 44, 84)", 
              "family": "Courier New, monospace"
            },
            'orientation': 'h',
          },
          # Xaxis
          "xaxis": {
            "showline": True,
            "linecolor": "rgb(0, 0, 0)",
            "linewidth": 2,
            "ticks": "outside",
            "tickwidth": 2, 
            "tickcolor": 'rgb(0, 0, 0)',
            "range": [(-1),len(reducedLunchCounty.index)]
          },
          # Yaxis 1 position left

          "yaxis": {
            "title": "Count Reduced Lunch",
            "titlefont": {
            "size": 16,
            "color": "rgb(71, 71, 135)", 
            "family": "Courier New, monospace"
            },
            "showline": True,
            "linecolor": "rgb(0, 0, 0)",
            "linewidth": 2,
            "ticks": "outside",
            "tickwidth": 2, 
            "tickcolor": 'rgb(0, 0, 0)',
            #"automargin": True
            #"shift": -1
          }, 


          # Yaxis 2 position right
          "yaxis2": {
            "side": "right",
            "range": [0, 100], 
            "title": "Percentage of Total Reduced Lunch",
            "titlefont": {
              "size": 16, 
              "color": "rgb(71, 71, 135)", 
              "family": "Courier New, monospace"
            },
            "showline": True,
            "linecolor": "rgb(0, 0, 0)",
            "linewidth": 2,
            "overlaying": "y",
            "ticksuffix": " %",
            "ticks": "outside",
            "tickwidth": 2, 
            "tickcolor": 'rgb(0, 0, 0)',
            #"automargin": True
            #"shift": 1
          }, 
        }

        # Build Graph
        fig = Figure(data=data, layout=layout)
        fig.update_layout(autosize=True)
        # Show Graph
        fig.show()


        plotPane = pn.pane.Plotly(fig)
        source_annotation = pn.pane.Markdown(
            '<span style="font-size: 12px; color: gray;">Source: National Center for Education Statistics</span>',
            width=600, height=40, align="start"
        )

        # Combine Plotly graph and source annotation in a layout
        layout = pn.Column(plotPane, pn.Spacer(height=10),source_annotation, styles={"border": "1px solid black"})

        return layout
    lunchfig = graph_pareto(reducedLunchCounty, 'Reduced.Lunch')
    return graph_pareto, lunchfig


@app.cell
def _(pd):
    dfarrests = pd.read_excel('/Users/11nho/Documents/School/690V/HW/data/MSP DFS Arrests 19-20Q1.xlsx', sheet_name='MSP DFS Arrests')
    dfcodes = pd.read_excel('/Users/11nho/Documents/School/690V/HW/data/MSP DFS Arrests 19-20Q1.xlsx', sheet_name='Codes', usecols="A:B", skiprows=74)
    return dfarrests, dfcodes


@app.cell
def _(dfarrests):
    dfarrests_1 = dfarrests[['Arrest Type', 'Age']].dropna()
    dfarrests_1.head()
    return (dfarrests_1,)


@app.cell
def _(dfcodes):
    dfcodes.columns = ['Arrest Type', 'Long Form']
    dfcodes.head()
    return


@app.cell
def _(dfarrests_1, dfcodes):
    mergeddf = dfarrests_1.merge(dfcodes, on='Arrest Type', how='inner')
    mergeddf.head()
    return (mergeddf,)


@app.cell
def _(mergeddf, px):
    figviol = px.violin(
        mergeddf,
        x = "Age",
        y = "Long Form",
        box = True,
        points="all",
        color = "Long Form",
        range_x = [0, None],
        labels = {
            "Long Form" : "Arrest Type",
            "Age" : "Arrestee Age (Years)"
        },
        title = "Felony Arrests are Younger than other Arrests in Massachusetts<br><span style='font-size:12px; color: rgb(100, 100, 100);'>Age Distribution of Arrests in Massachusetts from January 2019 to March 2020 </span>"
    )
    figviol.update_layout(
        showlegend=False
    )
    figviol.show()
    return (figviol,)


@app.cell
def _():
    import json
    def load_json(file):
        with open(file) as f:
            data = json.load(f)
            return data
    return json, load_json


@app.cell
def _(load_json, pd):
    bostondf = pd.read_excel('/Users/11nho/Documents/School/690V/HW/data/BostonContrib.xlsx', dtype={"Zip": str})
    bostonjson = load_json('/Users/11nho/Documents/School/690V/HW/data/zip_codes.json')

    bostondf = bostondf.dropna(subset=['Zip', 'Tender Type Description','Amount'])
    bostondf.head()
    return bostondf, bostonjson


@app.cell
def _(bostondf):
    bostondf['Tender Type Description'].value_counts()
    return


@app.cell
def _(bostondf):
    bostondfFiltered = bostondf.loc[bostondf['Tender Type Description'].isin(['Check','Credit Card'])]
    bostondfFiltered.head()
    return (bostondfFiltered,)


@app.cell
def _(bostondfFiltered):
    print(set(bostondfFiltered['Zip'].values))
    return


@app.cell
def _(bostondfFiltered):
    bostonPiv = bostondfFiltered.pivot_table(index='Zip', columns='Tender Type Description', values='Amount', aggfunc="sum").astype('int')
    bostonPiv['Highest'] = bostonPiv.idxmax(axis=1)
    bostonPiv.columns.name = None
    bostonPiv.index.name = None
    bostonPiv = bostonPiv.rename_axis('Zip').reset_index()
    bostonPiv['Zip'] = bostonPiv['Zip'].astype(str)
    bostonPiv['Check'] = (bostonPiv['Check'] - bostonPiv['Check'].min()) / (bostonPiv['Check'].max() - bostonPiv['Check'].min())
    bostonPiv['Credit Card'] = (bostonPiv['Credit Card'] - bostonPiv['Credit Card'].min()) / (bostonPiv['Credit Card'].max() - bostonPiv['Credit Card'].min())
    bostonPiv.head()
    return (bostonPiv,)


@app.cell
def _(bostonjson):
    print(bostonjson['features'][0]['properties'])
    return


@app.cell
def _(bostonPiv, bostonjson, px):
    figchoro = px.choropleth(
        bostonPiv,
        geojson= bostonjson,
        locations='Zip',
        featureidkey='properties.ZIP5',
        hover_data='Check',
        color='Check',
        color_continuous_scale="Viridis",
        title="Check Contributions"
    )

    figchoro.update_geos(
        projection_type="mercator",
        fitbounds="locations"
    )

    figchoro.update_layout(
        coloraxis_colorbar_title="Relative Contributions",
        margin={"l":1, "r":1}

    )

    figchoro2 = px.choropleth(
        bostonPiv,
        geojson= bostonjson,
        locations='Zip',
        featureidkey='properties.ZIP5',
        hover_data='Credit Card',
        color='Credit Card',
        color_continuous_scale="Viridis",
        title="Credit Card Contributions"
    )

    figchoro2.update_geos(
        projection_type="mercator",
        fitbounds="locations"
    )

    figchoro2.update_layout(
        coloraxis_colorbar_title="Relative Contributions",
        margin={"l":1, "r":1}
    )

    figchoro.show()
    figchoro2.show()
    return figchoro, figchoro2


@app.cell
def _(pn):
    campaignSourceAnnotation = pn.pane.Markdown(
            '<span style="font-size: 12px; color: gray;">Source: Massachusetts Office of Campaign and Political Finance</span>',
            width=600, height=40, align="start"
        )
    return (campaignSourceAnnotation,)


@app.cell
def _(campaignSourceAnnotation, figchoro, figchoro2, pn):
    chorosComb = pn.Row(figchoro, figchoro2, sizing_mode="stretch_height", align="center")

    chorotitle = pn.pane.Markdown(
            '<span style="font-size: 24px; color: black;">Campaign Contribution Amounts Vary Greatly by Tender Type and Location in Boston</span>',
            width=1000, height=40, align="center"
        )
    chorosubtitle = pn.pane.Markdown(
            '<span style="font-size: 12px; color: gray;">Campaign Contributions by Zipcode in Boston Massachusetts</span>',
            width=600, height=40, align="center"
        )
    chorosFull = pn.Column(chorotitle,chorosubtitle,chorosComb,campaignSourceAnnotation, styles={"border": "1px solid black"}, sizing_mode="stretch_height")
    return chorosComb, chorosFull, chorosubtitle, chorotitle


@app.cell
def _(figviol, pn):
    arrestSourceAnnotation = pn.pane.Markdown(
            '<span style="font-size: 12px; color: gray;">Source: Massachusetts Executive Office of Public Safety and Security</span>',
            width=600, height=40, align="start"
        )
    arrestsfig = pn.Column(figviol, pn.Spacer(height=10), arrestSourceAnnotation, styles={"border": "1px solid black"}, height=520)
    return arrestSourceAnnotation, arrestsfig


@app.cell
def _(arrestsfig, chorosFull, lunchfig, pn):
    dashbottom = pn.Row(chorosFull, pn.Spacer(width=10), arrestsfig, sizing_mode="stretch_both")
    dash = pn.Column(lunchfig, pn.HSpacer(), dashbottom,sizing_mode="stretch_width")
    return dash, dashbottom


@app.cell
def _():
    #server = dash.show()
    return


@app.cell
def _(dash):
    from bokeh.resources import INLINE
    from pathlib import Path

    dash.save(f"{Path.home()}/Documents/School/690V/index.html", resources=INLINE, embed=True)
    return INLINE, Path


if __name__ == "__main__":
    app.run()
