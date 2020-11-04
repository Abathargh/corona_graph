## corona_graph

Un semplice script che genera grafici relativi ai casi di Covid-19 regione per regione, basandosi sui dati forniti dalla
 [repository ufficiale](https://github.com/pcm-dpc/COVID-19) della Protezione Civile.


A simple script that plots the number of italian Covid-19 cases by region based on the data offered by the [official 
    repository](https://github.com/pcm-dpc/COVID-19) of the Italian civil Protection Department.
    
### Utilizzo/Usage

Per utilizzare lo script è necessario avere installato git e matplotlib.

To use the script you need to have git and matplotlib.

```bash
pip3 install -r requirements.txt
python3 corona_graph.py 
```

In alternativa, è possibile utilizzare un'immagine Docker. In questo caso è consigliabile eseguire lo script con il flag
 -s, per salvare le immagini in un volume.

You could also use a Docker image. If you do, you may want to execute the script with the -s flag, in order to save the 
images inside a volume.

```bash
docker build -t corona-graph .
docker run --rm -v $(pwd)/imgs:/app/imgs -it corona-graph bash 

python corona_graph.py -s
```

--help

```bash
usage: Plot generator for COVID-19 data by the Italian Department of Civil Protection; day_0 = 24/02/2020.
                     [-h] [--regione REGIONE [REGIONE ...]] [--data DATA] [--last LAST]                                                                                                                                                                       
optional arguments:                                                                                                       
    -h, --help            show this help message and exit                                                                   
    --regione REGIONE [REGIONE ...], -r REGIONE [REGIONE ...]                                                                                     
                        Name(s) of one or more region to plot. By default data from every region is plotted.              
    --data DATA, -d DATA  Plot graph(s) up to the passed date; date in the y-m-d format.                                    
    --last LAST, -l LAST  Plot graph(s) using the last n data samples (using data from the [today -n; today] interval)
                        with 0 <= n <= # days form day_0 
    --save, -s            Saves the img instead of plotting it
