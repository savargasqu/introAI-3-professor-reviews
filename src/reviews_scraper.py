from bs4 import BeautifulSoup
from requests import get as req_get
import os.path
import json


def normalize(s):
    """Quita acentos, espacios y capitalizción de cadenas"""
    replacements = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"),
                    ("ñ","n"), ("  "," "), (" ","-") )
    s = s.strip()
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
        s = s.lower()
    return s


def url_maker(departamento, docente):
    """dado un profesor y su departamento retorna la url del profesor en losestudiantes.co"""
    base_url = "https://losestudiantes.co/universidad-nacional/"
    url = "{}{}/profesores/{}".format(base_url, departamento,docente)
    return(url)


def get_urls_artes(url, docentes):
    """Obtener la lista de profesores de la facultad de artes"""
    html_artes = req_get(url).text

    arbol = BeautifulSoup(html_artes, 'html.parser')
    escuelas = arbol.find_all("option")

    for escuela in escuelas:
        docente_dep = []
        new_url = url + "?escuela=" + escuela['value']
        html_artes = req_get(new_url).text
        arbol = BeautifulSoup(html_artes, 'html.parser')
        for i in arbol.find_all("span", {"class":"name"}):
            docente_dep.append(normalize(i.text))
        docentes[normalize(arbol.find("option",selected=True).text)] = docente_dep
    docentes["artes-plasticas-y-visuales"] = docentes.pop("artes-plasticas")
    return docentes


def get_urls_fce(url):
    """Obtener la lista de profesores de la facultad de ciencias economicas"""
    html =  req_get(url).text
    arbol = BeautifulSoup(html, 'html.parser')
    docente_dep = []
    for profesor in arbol.find_all("h4", {"style":"font-size: 16px"}):
        docente_dep.append(normalize(profesor.text))
    return docente_dep


def get_urls_unal():
    url_artes = 'http://www.facartes.unal.edu.co/fa/docentes/index.php'
    url_admin = "http://fce.unal.edu.co/docentesfce/index.php?escuela=1"
    url_econ = "http://fce.unal.edu.co/docentesfce/index.php?escuela=2"

    docentes_unal = {}
    docentes_unal = get_urls_artes(url_artes, docentes_unal)
    docentes_unal["administracion-y-contaduria-publica"] = get_urls_fce(url_admin)
    docentes_unal["economia"] = get_urls_fce(url_econ)
    
    with open("./data/profesors.json", 'w') as write_professors_file:
        json.dump(docentes_unal, write_professors_file)

    urls_unal = []
    for k,v in docentes_unal.items():
        for profesor in v:
            urls_unal.append(url_maker(k, profesor)) # USING URLS LIST
    return urls_unal


def get_urls_uniandes():
    """Obtener la lista de profesores de Uniandes"""
    urls = []
    with open("./data/url_andes.txt","r") as url_andes:
        arbol = BeautifulSoup(url_andes.read(), 'html.parser')
        for a in arbol.find_all("a", {"class":"jsx-633353764"}):
            urls.append("https://losestudiantes.co/" + a['href'])
    print(len(urls))
    return urls


def get_train_data(urls):
    train_data = []
    if os.path.isfile("./data/reviews.json"):
        with open("./data/reviews.json", 'r') as reviews_file:
            train_data = json.load(reviews_file) # Read data from file
    else:
        for url in urls:
            html_review = req_get(url).text
            arbol = BeautifulSoup(html_review, 'html.parser')
            containers = arbol.find_all("li",{"class":"jsx-571610088 post "})
            for container in containers:
        #nota = container.find("span",{"class":"jsx-571610088 numeroStats"}).text
        #nota = round(nota * 2) / 2
                review = container.find("div",{"class":"jsx-571610088 lineBreak"})
                nota = container.find("span",{"class":"jsx-571610088 numeroStats"})
                if nota is None or review is None:
                    continue
                train_data.append((review.text, str(nota.text),url))

        with open("./data/reviews.json", 'w', encoding='utf-8') as write_reviews_file:
            json.dump(train_data, write_reviews_file)
    return train_data


def main():
    urls_unal = get_urls_unal()
    urls_andes = get_urls_uniandes()

    all_urls = urls_andes + urls_unal
    train_data = get_train_data(all_urls)


if __name__ == '__main__':
    main()
