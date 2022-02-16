import shodan, requests

api = shodan.Shodan("THJcdFCW9L70RcTvD4n6YezZtny45LeP")
query1 = "Server: SQ-WEBCAM"
query2 = 'http.title:"Nordex Control" "Windows 2000 5.0 x86" "Jetty/3.1 (JSP 1.1; Servlet 2.2; java 1.6.0_14)"'
query3 = 'html:Softneta'


def search_exploit(query):
    toret = "No exploits found."
    exploits_api_url = "https://exploits.shodan.io/api/search?query={query}&key={api_key}"
    exploit_query = exploits_api_url.format(query=query, api_key='THJcdFCW9L70RcTvD4n6YezZtny45LeP')
    response = requests.get(exploit_query).json()
    for match in response['matches']:
        if match:
            toret = 'ID: ' + query + '\nExploit: ' + match['description'] + '\n'

    return toret


def shodan_search(query):
    try:
        results = api.search(query)
        filepath = "/home/javier/Escritorio/MUNICS/SIND/Shodan-P1/shodan-results.txt"

        f = open(filepath, "w")
        for result in results['matches']:
            f.write("IP: " + result['ip_str'])
            f.write("\nProducto: " + str(result['http']['server']))
            # f.write("\nInfo: " + str(result['info']))
            f.write("\nSistema Operativo: " + str(result['os']))
            f.write("\nOrganizacion: " + str(result['org']))
            f.write("\nUbicacion: " + result['location']['city'] + ", " + str(result['location']['longitude']) + "/" + str(result['location']['latitude']) + ", " + result['location']['country_name'])
            f.write("\nPuertos abiertos: " + str(result['port']))
            f.write("\nVulnerabilidades: ")
            for vuln in result['vulns']:
                f.write("\n  - " + vuln)
            f.write("\n\n")
        f.close()
        print("Search finished.")

    except shodan.APIError as e:
        print("Error: " + str(e))


shodan_search(query2)
print(search_exploit("Windows 2000 5.0 x86"))
