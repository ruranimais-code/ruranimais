# Imports
import webbrowser
import branca.colormap
import numpy as np

import folium
from folium.plugins import HeatMap

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread


# Mapa
class Mapa:

    # Desenha o mapa
    @staticmethod
    def gerar_mapa():
        diretorio_mapa = Path(__file__).resolve().parent
        arquivo_mapa = diretorio_mapa / "footprint.html"

        mapa_ufrpe = folium.Map(location = [-8.01684136482162, -34.94927713266724],
                                 zoom_start = 16, tiles = None)


        # Dados de entrada
        # Adicionar fronteira
        geojson_arquivo = "Ruranimais/assets/ufrpe.geojson"
        estilo = lambda x: {"color": "black",
                            "fillOpacity": 0,
                            "weight": 1}
        folium.GeoJson(geojson_arquivo, style_function=estilo, 
                       name="Campus").add_to(mapa_ufrpe)
        # Dados (tudo inventado >.<)
        frequencia_bichinhos = np.genfromtxt(
            "Ruranimais/assets/frequencia_bichinhos.csv",
            delimiter=",",
            skip_header=1,
            usecols=(0, 1, 2),
        )


        # Paleta de cores
        indices = [0, 0.3, 0.7, 1]

        colormap = branca.colormap.StepColormap(
            ["green", "yellow", "red"],
            index=indices,
            caption="Frequência de bichinhos",
        )
        colormap.scale(0, 100).add_to(mapa_ufrpe)

        gradiente = {
            0.0: "green",
            0.3: "green",
            0.301: "yellow",
            0.7: "yellow",
            0.701: "red",
            1.0: "red",
        }

        # Mapa de calor
        HeatMap(
            data=frequencia_bichinhos,
            name="Frequência",
            min_opacity=0.05,
            radius=6,
            blur=4,
            gradient=gradiente,
        ).add_to(mapa_ufrpe)

        # Controle de camadas
        folium.LayerControl("topleft").add_to(mapa_ufrpe)

        mapa_ufrpe.save(str(arquivo_mapa))

        # Pra conectar com o servidor eba
        servidor = ThreadingHTTPServer(
            ("127.0.0.1", 8765),
            partial(SimpleHTTPRequestHandler, directory=str(diretorio_mapa)),
        )

        Thread(target=servidor.serve_forever, daemon=True).start()
        webbrowser.open("http://127.0.0.1:8765/footprint.html")
        print("Mapa disponível em http://127.0.0.1:8765/footprint.html")
        return servidor

    @staticmethod
    def abrir_mapa():
        servidor = Mapa.gerar_mapa()
        try:
            while True:
                opcao = input("\nDigite 'voltar' ou 'v' para voltar: ").strip().lower()
                if opcao in {"voltar", "v"}:
                    break
                webbrowser.open("http://127.0.0.1:8765/footprint.html")
        finally:
            servidor.shutdown()
            servidor.server_close()
