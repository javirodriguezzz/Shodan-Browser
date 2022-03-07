import requests
import shodan
import threading
import random

api = shodan.Shodan("YOUR_SHODAN_API_KEY")
query1 = "Server: SQ-WEBCAM"
query2 = 'http.title:"Nordex Control" "Windows 2000 5.0 x86" "Jetty/3.1 (JSP 1.1; Servlet 2.2; java 1.6.0_14)"'
query3 = 'html:Softneta'
queries = [query1, query2, query3]


def search_exploit(query):
    toret = "No exploits found."
    exploits_api_url = "https://exploits.shodan.io/api/search?query={query}&key={api_key}"
    exploit_query = exploits_api_url.format(query=query, api_key='THJcdFCW9L70RcTvD4n6YezZtny45LeP')
    response = requests.get(exploit_query).json()
    print('ID: ' + query)
    for match in response['matches']:
        if match:
            print('\nExploit: ' + match['description'])
            print('Author: ' + match['author'])
            print('Port: ' + str(match['port']))
            print('Source: ' + match['source'])


def shodan_search(query, filepath):
    try:
        results = api.search(query)

        f = open(filepath, "w")
        for result in results['matches']:
            vuln_index = 0
            f.write("IP: " + result['ip_str'])
            f.write("\nProducto: " + str(result['http']['server']))
            # f.write("\nInfo: " + str(result['info']))
            f.write("\nSistema Operativo: " + str(result['os']))
            f.write("\nOrganizacion: " + str(result['org']))
            f.write("\nUbicacion: " + result['location']['city'] + ", " + str(result['location']['longitude']) + "/" + str(result['location']['latitude']) + ", " + result['location']['country_name'])
            f.write("\nPuertos abiertos: " + str(result['port']))
            f.write("\nVulnerabilidades: ")
            try:
                for vuln in result['vulns']:
                    f.write("\n  - " + vuln)
                    if vuln_index != 3:
                        exploits_api_url = "https://exploits.shodan.io/api/search?query={query}&key={api_key}"
                        exploit_query = exploits_api_url.format(query=vuln,
                                                                api_key='THJcdFCW9L70RcTvD4n6YezZtny45LeP')
                        response = requests.get(exploit_query)
                        try:
                            response_json = response.json()
                            if len(response_json['matches']) > 0:
                                for match in response_json['matches']:
                                    f.write('\nExploit: ' + match['description'] + '\nAuthor: ' + match[
                                        'author'] + '\nSource: ' +
                                            match['source'])
                                    print('¡Exploit encontrado! IP: ' + result['ip_str'])
                        except ValueError:
                            print('Exploits no encontrados para el dispositivo ' + result['ip_str'])

                    vuln_index = vuln_index + 1
            except KeyError:
                pass

            f.write("\n\n")
        f.close()
        print("Busqueda finalizada para la consulta: " + query)

    except shodan.APIError as e:
        print("Error: " + str(e))


# shodan_search(query1, "/home/javier/Escritorio/MUNICS/SIND/Shodan-P1/query1-results.txt")
# shodan_search(query2, "/home/javier/Escritorio/MUNICS/SIND/Shodan-P1/query2-results.txt")
# search_exploit("Windows 2000 5.0 x86")


def main(queries):

    def worker(query):
        shodan_search(query, "/home/javier/Escritorio/MUNICS/SIND/Shodan-P1/query-" + str(random.randint(1, 1000)) +
                      "results.txt")

    for q in queries:
        t = threading.Thread(target=worker, args=(q,))
        t.start()


main(queries)
