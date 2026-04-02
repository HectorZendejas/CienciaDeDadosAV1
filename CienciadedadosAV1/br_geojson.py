# GeoJSON do Brasil com informações dos estados
# Arquivo de suporte para o mapa cloroplético

# GeoJSON do Brasil - Estados brasileiros válidos para plotly choropleth
# Fonte: Simplificado de dados públicos de limites estaduais

BRASIL_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature", "id": "AC", "properties": {"sigla": "AC", "nome": "Acre"}, "geometry": {"type": "Polygon", "coordinates": [[[[-73.96, -8.76], [-73.96, -11.15], [-66.97, -11.15], [-66.97, -8.76], [-73.96, -8.76]]]]}},
        {"type": "Feature", "id": "AL", "properties": {"sigla": "AL", "nome": "Alagoas"}, "geometry": {"type": "Polygon", "coordinates": [[[[-37.77, -8.73], [-37.77, -10.27], [-35.18, -10.27], [-35.18, -8.73], [-37.77, -8.73]]]]}},
        {"type": "Feature", "id": "AP", "properties": {"sigla": "AP", "nome": "Amapá"}, "geometry": {"type": "Polygon", "coordinates": [[[[-54.67, 0.72], [-54.67, 4.23], [-48.36, 4.23], [-48.36, 0.72], [-54.67, 0.72]]]]}},
        {"type": "Feature", "id": "AM", "properties": {"sigla": "AM", "nome": "Amazonas"}, "geometry": {"type": "Polygon", "coordinates": [[[[-73.99, 1.03], [-73.99, -4.99], [-55.73, -4.99], [-55.73, 1.03], [-73.99, 1.03]]]]}},
        {"type": "Feature", "id": "BA", "properties": {"sigla": "BA", "nome": "Bahia"}, "geometry": {"type": "Polygon", "coordinates": [[[[-49.02, -9.52], [-49.02, -18.36], [-37.76, -18.36], [-37.76, -9.52], [-49.02, -9.52]]]]}},
        {"type": "Feature", "id": "CE", "properties": {"sigla": "CE", "nome": "Ceará"}, "geometry": {"type": "Polygon", "coordinates": [[[[-40.84, -2.8], [-40.84, -7.92], [-37.24, -7.92], [-37.24, -2.8], [-40.84, -2.8]]]]}},
        {"type": "Feature", "id": "DF", "properties": {"sigla": "DF", "nome": "Distrito Federal"}, "geometry": {"type": "Polygon", "coordinates": [[[[-48.28, -15.5], [-48.28, -16.05], [-47.45, -16.05], [-47.45, -15.5], [-48.28, -15.5]]]]}},
        {"type": "Feature", "id": "ES", "properties": {"sigla": "ES", "nome": "Espírito Santo"}, "geometry": {"type": "Polygon", "coordinates": [[[[-41.87, -17.34], [-41.87, -21.31], [-39.5, -21.31], [-39.5, -17.34], [-41.87, -17.34]]]]}},
        {"type": "Feature", "id": "GO", "properties": {"sigla": "GO", "nome": "Goiás"}, "geometry": {"type": "Polygon", "coordinates": [[[[-53.65, -13.12], [-53.65, -19.49], [-46.09, -19.49], [-46.09, -13.12], [-53.65, -13.12]]]]}},
        {"type": "Feature", "id": "MA", "properties": {"sigla": "MA", "nome": "Maranhão"}, "geometry": {"type": "Polygon", "coordinates": [[[[-48.51, -2.5], [-48.51, -10.3], [-42.8, -10.3], [-42.8, -2.5], [-48.51, -2.5]]]]}},
        {"type": "Feature", "id": "MT", "properties": {"sigla": "MT", "nome": "Mato Grosso"}, "geometry": {"type": "Polygon", "coordinates": [[[[-62.31, -8.34], [-62.31, -18.04], [-50.22, -18.04], [-50.22, -8.34], [-62.31, -8.34]]]]}},
        {"type": "Feature", "id": "MS", "properties": {"sigla": "MS", "nome": "Mato Grosso do Sul"}, "geometry": {"type": "Polygon", "coordinates": [[[[-57.6, -19.04], [-57.6, -23.26], [-53.64, -23.26], [-53.64, -19.04], [-57.6, -19.04]]]]}},
        {"type": "Feature", "id": "MG", "properties": {"sigla": "MG", "nome": "Minas Gerais"}, "geometry": {"type": "Polygon", "coordinates": [[[[-51.99, -14.89], [-51.99, -23.32], [-39.54, -23.32], [-39.54, -14.89], [-51.99, -14.89]]]]}},
        {"type": "Feature", "id": "PA", "properties": {"sigla": "PA", "nome": "Pará"}, "geometry": {"type": "Polygon", "coordinates": [[[[-58.76, -1.04], [-58.76, -8.76], [-48.51, -8.76], [-48.51, -1.04], [-58.76, -1.04]]]]}},
        {"type": "Feature", "id": "PB", "properties": {"sigla": "PB", "nome": "Paraíba"}, "geometry": {"type": "Polygon", "coordinates": [[[[-38.76, -6.64], [-38.76, -8.76], [-34.79, -8.76], [-34.79, -6.64], [-38.76, -6.64]]]]}},
        {"type": "Feature", "id": "PR", "properties": {"sigla": "PR", "nome": "Paraná"}, "geometry": {"type": "Polygon", "coordinates": [[[[-54.57, -22.50], [-54.57, -27.59], [-48.08, -27.59], [-48.08, -22.50], [-54.57, -22.50]]]]}},
        {"type": "Feature", "id": "PE", "properties": {"sigla": "PE", "nome": "Pernambuco"}, "geometry": {"type": "Polygon", "coordinates": [[[[-38.73, -7.33], [-38.73, -9.86], [-34.82, -9.86], [-34.82, -7.33], [-38.73, -7.33]]]]}},
        {"type": "Feature", "id": "PI", "properties": {"sigla": "PI", "nome": "Piauí"}, "geometry": {"type": "Polygon", "coordinates": [[[[-45.59, -2.80], [-45.59, -10.90], [-40.20, -10.90], [-40.20, -2.80], [-45.59, -2.80]]]]}},
        {"type": "Feature", "id": "RJ", "properties": {"sigla": "RJ", "nome": "Rio de Janeiro"}, "geometry": {"type": "Polygon", "coordinates": [[[[-44.88, -20.76], [-44.88, -23.88], [-40.51, -23.88], [-40.51, -20.76], [-44.88, -20.76]]]]}},
        {"type": "Feature", "id": "RN", "properties": {"sigla": "RN", "nome": "Rio Grande do Norte"}, "geometry": {"type": "Polygon", "coordinates": [[[[-38.77, -5.25], [-38.77, -6.98], [-34.81, -6.98], [-34.81, -5.25], [-38.77, -5.25]]]]}},
        {"type": "Feature", "id": "RS", "properties": {"sigla": "RS", "nome": "Rio Grande do Sul"}, "geometry": {"type": "Polygon", "coordinates": [[[[-57.59, -27.08], [-57.59, -34.47], [-49.65, -34.47], [-49.65, -27.08], [-57.59, -27.08]]]]}},
        {"type": "Feature", "id": "RO", "properties": {"sigla": "RO", "nome": "Rondônia"}, "geometry": {"type": "Polygon", "coordinates": [[[[-66.28, -8.34], [-66.28, -13.77], [-59.55, -13.77], [-59.55, -8.34], [-66.28, -8.34]]]]}},
        {"type": "Feature", "id": "RR", "properties": {"sigla": "RR", "nome": "Roraima"}, "geometry": {"type": "Polygon", "coordinates": [[[[-64.56, 0.99], [-64.56, 5.55], [-58.11, 5.55], [-58.11, 0.99], [-64.56, 0.99]]]]}},
        {"type": "Feature", "id": "SC", "properties": {"sigla": "SC", "nome": "Santa Catarina"}, "geometry": {"type": "Polygon", "coordinates": [[[[-53.83, -25.69], [-53.83, -29.68], [-48.28, -29.68], [-48.28, -25.69], [-53.83, -25.69]]]]}},
        {"type": "Feature", "id": "SP", "properties": {"sigla": "SP", "nome": "São Paulo"}, "geometry": {"type": "Polygon", "coordinates": [[[[-53.66, -19.87], [-53.66, -25.31], [-43.97, -25.31], [-43.97, -19.87], [-53.66, -19.87]]]]}},
        {"type": "Feature", "id": "SE", "properties": {"sigla": "SE", "nome": "Sergipe"}, "geometry": {"type": "Polygon", "coordinates": [[[[-37.77, -9.5], [-37.77, -11.0], [-36.39, -11.0], [-36.39, -9.5], [-37.77, -9.5]]]]}},
        {"type": "Feature", "id": "TO", "properties": {"sigla": "TO", "nome": "Tocantins"}, "geometry": {"type": "Polygon", "coordinates": [[[[-51.49, -9.46], [-51.49, -14.29], [-48.04, -14.29], [-48.04, -9.46], [-51.49, -9.46]]]]}},
    ]
}

# Coordenadas dos centros dos estados para o mapa
COORDENADAS_ESTADOS = {
    'AC': (-67.855, -9.975),
    'AL': (-36.652, -9.412),
    'AP': (-51.925, 1.414),
    'AM': (-64.856, -3.468),
    'BA': (-44.257, -12.865),
    'CE': (-39.278, -3.731),
    'DF': (-47.863, -15.794),
    'ES': (-40.298, -19.191),
    'GO': (-49.618, -15.899),
    'MA': (-45.244, -2.530),
    'MT': (-55.486, -12.640),
    'MS': (-55.141, -20.510),
    'MG': (-44.864, -19.408),
    'PA': (-51.929, -3.793),
    'PB': (-35.867, -7.140),
    'PR': (-51.168, -24.500),
    'PE': (-37.453, -8.383),
    'PI': (-42.750, -6.587),
    'RJ': (-42.735, -22.906),
    'RN': (-36.585, -5.797),
    'RS': (-51.209, -29.687),
    'RO': (-63.901, -11.784),
    'RR': (-60.693, 2.839),
    'SC': (-49.065, -27.595),
    'SP': (-48.945, -23.550),
    'SE': (-37.071, -10.194),
    'TO': (-48.297, -9.888)
}
