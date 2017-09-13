#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import requests
from bs4 import BeautifulSoup


def text(strings):
    while(1):
        que = input(strings)
        if "Enter" in strings and que == '':
            print("Please,", strings.lower()[:-2])
            continue
        elif ("Choose" in strings) and ((que == '') or (not que.isdigit())):
            print("Please,", strings.lower()[2:-2])
            continue
        else:
            break
    return que


def main():
    main_site   = 'https://tempr.email/en'
    
    local_part  = text("Enter email name: ") 

    soup        = BeautifulSoup(requests.get(main_site).text, 'html.parser')
    domain_name = {i:[q.text,q['value']] for i,q in enumerate(soup.find_all('option', \
            {'class':"", 'disabled':""})) if q['value'].isdigit()}

    for key, value in domain_name.items():
        print('| {0:2d} | {1:25}'.format(key,value[0]), end='')
        if key % 3 == 0:
            print('')

    domain_id   = text("\n\nChoose your domain: ")

    if "(PW)" in domain_name[int(domain_id)][0]:
        pw = input("\nInput password for email, if necessary: ")
    else:
        pw = ''

    headers = {'user-agent': 'Mozilla/5.0'}
    payload = {'LocalPart': '{}'.format(local_part), \
                'DomainType': 'public', \
                'DomainId': '{}'.format(domain_name[int(domain_id)][1]), \
                'Password': '{}'.format(pw), \
                'LoginButton': ''}

    session = requests.Session()
    site    = session.post(main_site,headers=headers,data=payload)
    soup    = BeautifulSoup(site.text, 'html.parser')

    try:
        head = [(q.a['href'],q.get_text("\n\t")) for q in soup.find('div', \
            attrs={'id':"Inbox"}).find_all('div', attrs={'class': "Head"})]
        date = [q.text for q in soup.find('div', \
            attrs={'id':"Inbox"}).find_all('div', attrs={'class' : "Date"})]
        options = [q.a['href'] for q in soup.find('div', \
            attrs={'id':"Inbox"}).find_all('div', attrs={'class' : "Options"})]
            
        while(1):
            for key,value in enumerate(list(head)):
                if key <= 10:
                    print('\n',key,value[1],'\n\t',date[key])
            print('\n{:-^27}'.format(''))
            print('|{:^25}|'.format('Usage'))
            print('{:-^27}'.format(''))
            print('|{} |'.format(' view   - View message   |\n| delete - Delete message |\n| exit   - Exit          '))
            print('{:-^27}'.format(''))

            query = input("\nWhat's next? ")

            if query == "view":
                choice  = text("Choose message: ")
                try:
                    message = BeautifulSoup(session.get('%s-mailVersion=plain.htm' % (head[int(choice)][0][:-4])).text,'html.parser')
                except:
                    os.system("clear")
                    print("\nSorry, this message was deleted\n")
                    continue
                message.script.decompose()
                message.style.decompose()
                message.a.decompose()
                with open("/tmp/mess", "w") as f:
                    f.write(message.find('div', attrs={'id': "MessageContent"}).get_text("\n"))
                os.system('less /tmp/mess')

            if query == "delete":
                choice = text("Choose message: ")
                session.get('{}'.format(options[int(choice)]))
                head[int(choice)] = ('', "Empty")
                date[int(choice)] = ''
                os.system("clear")
                print("\nSuccessfully deleted\n")

            if query == "exit":
                os.system("clear")
                print("Thank you for being with us")
                break
            elif query == '':
                os.system("clear")
                print("\nCommands does not exist")

    except AttributeError:
        print("\nInbox is empty")

    except KeyboardInterrupt:
        pass

    except:
        print("\nCritical error")


if __name__ == '__main__':
    main()
