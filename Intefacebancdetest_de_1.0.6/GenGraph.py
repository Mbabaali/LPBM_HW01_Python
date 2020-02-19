# -*- coding: utf8 -*-
"""
    module permetttant la genration automatisé de graph dans le cadre du LPBM
"""
#fdff
from kivy.logger import Logger
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import sys
#import pandas as pd

plt.rcParams["figure.figsize"] = (70,12)

def generer_graph(chemin, chemin_graph='',
                  y_low_min=0.02, y_low_max=0.12,
                  y_high_min=600, y_high_max=1000, format_graph=0):
    """
        Permet de generer un graph diviser en deux suivant les paramètres données
    """

    if format_graph == 0 :
        plt.rcParams["figure.figsize"] = (50,12)
    elif format_graph == 1 :
        plt.rcParams["figure.figsize"] = (80,12)
    else :
        plt.rcParams["figure.figsize"] = (300,12)

    #On règle la dimension du graph en fonction du paramètre "format_graph" reçu (0 par défaut)



    Logger.warning('generer graph: chemin : {}'.format(chemin))
    if chemin_graph == "":
        nom_graph = chemin[:-3:]+'png'
        #Si le chemin n'est pas précisé, on prend le meme nom que le fichier .csv associé (on remplace le .csv par un .png)
    else:
        nom_graph = chemin_graph+".png"
    Logger.warning('generer_graph: nom_graph : {}'.format(nom_graph))
    #sns.set_style("darkgrid")

    dataframe = pd.read_csv(chemin, sep=';') 

    ordonnee = dataframe['Value']

    abcisse = dataframe['date-time']
    abcisse = pd.to_datetime(dataframe['date-time'], 
                             format='%Y-%m-%d %H:%M:%S.%f').astype(datetime)
    try:
        plt.plot(abcisse, ordonnee, marker=',')
    except AttributeError:
        Logger.warning('plt plot: impossible de generer un graph, fichier vide')
        exit()
    

    func, (ax, ax2) = plt.subplots(2, 1, sharex=True)
    ax.plot(abcisse, ordonnee, linewidth=1) #graphe du haut
    ax2.plot(abcisse, ordonnee, linewidth=1) #graphe du bas

    # zoom-in / limit the view to different portions of the data
    ax.set_ylim(float(y_high_min), float(y_high_max))  # outliers only
    ax2.set_ylim(float(y_low_min), float(y_low_max))  # most of the data

    # rotate and align the tick labels so they look better
    func.autofmt_xdate()


    ax2.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=60))

    # use a more precise date string for the x axis locations in the
    # toolbar
    ax2.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d/%m  %H:%M'))

    # hide the spines between ax and ax2
    ax.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax.xaxis.tick_top()
    ax.tick_params(labeltop='off')  # don't put tick labels at the top
    ax2.xaxis.tick_bottom()

    diag = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((-diag, +diag), (-diag, +diag), **kwargs)        # top-left diagonal
    ax.plot((1 - diag, 1 + diag), (-diag, +diag), **kwargs)  # top-right diagonal
    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((-diag, +diag), (1 - diag, 1 + diag), **kwargs)  # bottom-left diagonal
    ax2.plot((1 - diag, 1 + diag), (1 - diag, 1 + diag), **kwargs)  # bottom-right diagonal
    func.suptitle(str(chemin))
    plt.xlabel('Date')
    plt.ylabel('Conso (en mA)')
    plt.savefig(nom_graph)

if __name__ == "__main__":
    
    """
    Fonction main, pour lancer le script gengraph directement depuis le terminal
    """
    if(len(sys.argv) != 2) and (len(sys.argv) != 3) and (len(sys.argv) != 7):
        Logger.warning(
        'ERROR: Nombre d\'argument invalide : nombre d\'argument : {}'
        .format(len(sys.argv))) 
    elif len(sys.argv) == 2:    
        CHEMIN = sys.argv[1]
        generer_graph(CHEMIN)  
    elif len(sys.argv) == 3:
        CHEMIN = sys.argv[1]
        CHEMIN_GRAPH = sys.argv[2]
        generer_graph(CHEMIN, CHEMIN_GRAPH)
    elif len(sys.argv) == 7:
        generer_graph(sys.argv[1], sys.argv[2], sys.argv[3], 
                      sys.argv[4], sys.argv[5], sys.argv[6])







    
