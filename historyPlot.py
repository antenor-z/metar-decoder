import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import timedelta
import numpy as np
import pandas as pd

from DB.Getter import get_all_icao, latest_n_metars_parsed


def plot_metar_data(
                    page: int,
                    icao: str,
                    metar_data: list[dict],
                    data_name1: str,
                    label_name1: str,
                    unit1: str,
                    label_color1: str,
                    data_name2: str,
                    label_name2: str,
                    unit2: str,
                    label_color2: str
                    ):

    with plt.rc_context({'axes.edgecolor':'white', 'xtick.color':'white', 'ytick.color':'green', 'figure.facecolor':'#33333b'}):    
        timestamps = [(data["timestamp"] - timedelta(hours=3)).strftime("%H:%M (%d/%m)") for data in metar_data if data]
        data1 = [data[data_name1] or np.nan for data in metar_data if data]
        data2 = [data[data_name2] or np.nan for data in metar_data if data]

        for i in range(len(timestamps)):
            if i == 0 or i == len(timestamps) - 1:
                continue
            timestamps[i] = timestamps[i].split(" ")[0]

        fig, ax1 = plt.subplots()
        fig.set_size_inches(12, 4)
        ax1.set_facecolor('#222')

        ax1.set_ylabel(label_name1, color=f'{label_color1}')
        ax1.plot(timestamps, data1, 'o-', color=f'{label_color1}', label=label_name1)
        ax1.tick_params(axis='y', color='white', labelcolor=f'{label_color1}')

        for i, value in enumerate(data1):
            ax1.annotate(f'{value} {unit1}', xy=(timestamps[i], value), xytext=(0, 5), textcoords='offset points',
                         ha='center', color=label_color1, fontsize=9)

        ax2 = ax1.twinx()
        ax2.set_ylabel(label_name2, color=label_color2)
        ax2.plot(timestamps, data2, 's-', color=label_color2, label=label_name2)
        ax2.tick_params(axis='y', color='white', labelcolor=label_color2)

        for i, value in enumerate(data2):
            ax2.annotate(f'{value} {unit2}', xy=(timestamps[i], value), xytext=(0, -12), textcoords='offset points',
                         ha='center', color=label_color2, fontsize=9)

        # ax1.grid(True)

        fig.tight_layout()
        filename = f"static/plots/{icao}-{data_name1}-{data_name2}-{page+1}.svg"
        plt.savefig(filename, dpi=600)
        plt.close(fig)
        print(f"Plot saved as {filename}")


def plot(icao, metar_data, page=1):
    BLUE = "#008ae6"
    YELLOW = "#d5a810"
    plot_metar_data(page, icao, metar_data, "temperature", "Temperatura (°C)", "°C", BLUE, "dew_point", "Ponto de orvalho (°C)", "°C", YELLOW)
    plot_metar_data(page, icao, metar_data, "wind_speed", "Velocidade do vento (kt)", "kt", BLUE, "wind_direction", "Direção do vento (graus)", "°", YELLOW)
    plot_metar_data(page, icao, metar_data, "qnh", "Ajuste altímetro (hectopascal)", "hPa", BLUE, "visibility", "Visibilidade (metros)", "m", YELLOW)


def update_images(n_pages=5):
    for page in range(n_pages):
        for icao in get_all_icao():
            latest = latest_n_metars_parsed(icao=icao, n=12, offset=12*page)
            plot(icao=icao, metar_data=latest, page=page)
            #print(icao, latest, "page", page)


def update_df():
    for icao in get_all_icao():
        df = pd.DataFrame(latest_n_metars_parsed(icao=icao, n=500))
   
        try:
            df['timestamp'] = df['timestamp'].dt.tz_localize(None)
        except KeyError:
            continue

        FILENAME = f"static/datasets/dataset_{icao}.xlsx"
        df.to_excel(FILENAME, index=False, sheet_name=icao)
