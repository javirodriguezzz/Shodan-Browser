import random
import requests
import shodan
import threading
import optparse
import time

API_KEY = "YOUR SHODAN KEY"
api = shodan.Shodan(API_KEY)
filepath = "FILEPATH"
# Example queries
query1 = "Server: SQ-WEBCAM"
query2 = 'http.title:"Nordex Control" "Windows 2000 5.0 x86" "Jetty/3.1 (JSP 1.1; Servlet 2.2; java 1.6.0_14)"'
query3 = 'html:Softneta'
queries = []

parser = optparse.OptionParser()
parser.add_option("-f", "--file", dest="file", help="Search from a file with a list of queries", default="")
parser.add_option("-q", "--query", dest="query", help="Search a defined query", default="")
options, args = parser.parse_args()


def search_exploit(query):
    toret = "No exploits found."
    exploits_api_url = "https://exploits.shodan.io/api/search?query={query}&key={api_key}"
    exploit_query = exploits_api_url.format(query=query, api_key=API_KEY)
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
            f.write("\nProduct: " + str(result['http']['server']))
            # f.write("\nInfo: " + str(result['info']))
            f.write("\nOS: " + str(result['os']))
            f.write("\nOrganization: " + str(result['org']))
            f.write("\nUbication: " + result['location']['city'] + ", " + str(result['location']['longitude']) + "/" + str(result['location']['latitude']) + ", " + result['location']['country_name'])
            f.write("\nOpen ports: " + str(result['port']))
            f.write("\nVulnerabilities: ")
            try:
                for vuln in result['vulns']:
                    f.write("\n  - " + vuln)
                    if vuln_index != 3:
                        exploits_api_url = "https://exploits.shodan.io/api/search?query={query}&key={api_key}"
                        exploit_query = exploits_api_url.format(query=vuln,
                                                                api_key=API_KEY)
                        response = requests.get(exploit_query)
                        try:
                            response_json = response.json()
                            if len(response_json['matches']) > 0:
                                for match in response_json['matches']:
                                    f.write('\nExploit: ' + match['description'])
                                    print('¡Exploit found! IP: ' + result['ip_str'])
                        except ValueError:
                            print('No exploits found for device ' + result['ip_str'] + "(" + vuln + ")")

                    vuln_index = vuln_index + 1
            except KeyError:
                pass

            f.write("\n\n")
            time.sleep(1)
        f.close()
        print("Search finished for query: " + query)

    except shodan.APIError as e:
        print("Error: " + str(e))


def main(queries):

    def worker(query):
        shodan_search(query, filepath + str(random.randint(1, 1000)) +
                      "results.txt")

    for q in queries:
        t = threading.Thread(target=worker, args=(q,))
        t.start()


if options.file != "" and options.query != "":
    print("Wrong commands usage.")

if options.file != "":
    queries_file = open(options.file)

    for query in queries_file.readlines():
        queries.append(query)
    main(queries)
    queries_file.close()

if options.query != "":
    shodan_search(options.query, filepath + str(random.randint(1, 1000)) + "results.txt")

