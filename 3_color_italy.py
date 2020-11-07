import sys
import csv
import pprint
import pandas as pd
import geopandas as gpd

# Possible colors input
colors = ['red', 'orange', 'yellow']

regions = ['ABRUZZO', 'BASILICATA', 'CALABRIA', 'CAMPANIA', 'EMILIA-ROMAGNA', 'FRIULI VENEZIA GIULIA', 'LAZIO',
           'LIGURIA', 'LOMBARDIA', 'MARCHE', 'MOLISE', 'PIEMONTE', 'PUGLIA',
           'SARDEGNA', 'SICILIA', 'TOSCANA', 'TRENTINO-ALTO ADIGE/SUDTIROL', 'UMBRIA', 'VALLE AOSTA', 'VENETO']

# Create dict with ajacent regions
adj = {}
adj['ABRUZZO'] = ['MOLISE', 'LAZIO', 'MARCHE']
adj['BASILICATA'] = ['CAMPANIA', 'PUGLIA', 'CALABRIA']
adj['CALABRIA'] = ['BASILICATA']
adj['CAMPANIA'] = ['BASILICATA', 'PUGLIA', 'LAZIO', 'MOLISE']
adj['EMILIA-ROMAGNA'] = ['MARCHE', 'TOSCANA',
                         'LIGURIA', 'PIEMONTE', 'LOMBARDIA', 'VENETO']
adj['FRIULI VENEZIA GIULIA'] = ['VENETO']
adj['LAZIO'] = ['TOSCANA', 'UMBRIA', 'MARCHE', 'ABRUZZO', 'MOLISE', 'CAMPANIA']
adj['LIGURIA'] = ['PIEMONTE', 'EMILIA-ROMAGNA', 'TOSCANA']
adj['LOMBARDIA'] = ['PIEMONTE', 'EMILIA-ROMAGNA',
                    'VENETO', 'TRENTINO-ALTO ADIGE/SUDTIROL']
adj['MARCHE'] = ['EMILIA-ROMAGNA', 'TOSCANA', 'UMBRIA', 'LAZIO', 'ABRUZZO']
adj['MOLISE'] = ['PUGLIA', 'CAMPANIA', 'LAZIO', 'ABRUZZO']
adj['PIEMONTE'] = ['VALLE AOSTA', 'LIGURIA', 'LOMBARDIA', 'EMILIA-ROMAGNA']
adj['PUGLIA'] = ['BASILICATA', 'CAMPANIA', 'MOLISE']
adj['SARDEGNA'] = []
adj['SICILIA'] = []
adj['TOSCANA'] = ['LIGURIA', 'EMILIA-ROMAGNA', 'MARCHE', 'UMBRIA', 'LAZIO']
adj['TRENTINO-ALTO ADIGE/SUDTIROL'] = ['LOMBARDIA', 'VENETO']
adj['UMBRIA'] = ['MARCHE', 'TOSCANA', 'LAZIO']
adj['VALLE AOSTA'] = ['PIEMONTE']
adj['VENETO'] = ['FRIULI VENEZIA GIULIA', 'EMILIA-ROMAGNA',
                 'LOMBARDIA', 'TRENTINO-ALTO ADIGE/SUDTIROL']

# Reverse list for a different solutions
# This is a greedy algorithm, therefore order counts!

# regions = reversed(regions)

region_color = {}

# Assign colour if no adjacent region already has it


def assign_color(state, color):
    for nbr in adj.get(state):
        adj_color = region_color.get(nbr)
        if adj_color == color:
            return False
    return True

# Try to apply the first possible color to a region


def get_region_color(region):
    for color in colors:
        if assign_color(region, color):
            return color


def main():
    for region in regions:
        region_color[region] = get_region_color(region)

    # pp = pprint.PrettyPrinter()
    # pp.pprint(region_color)

    # Export a csv to merge result with a spatial shapefile for the final coloured graph
    with open('result_color.csv', 'w') as f:
        f.write("NOME_REG,color\n")
        for key in region_color.keys():
            f.write("%s,%s\n" % (key, region_color[key]))


# run colouring algorithm
main()

# import shapefile of italian regions
italy = gpd.read_file('italy/italy.shp')

# import csv file with solution to graph coloring
colors = pd.read_csv('./result_color.csv')

# merge tables by region name
merge = italy.merge(colors, on='NOME_REG', how='right')
# Plot region with colours
fig = merge.plot(
    column='color',
    cmap='Oranges',
    legend=True,
    figsize=(15, 30),
).axis('off')
