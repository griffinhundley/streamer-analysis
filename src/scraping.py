from src import credentials
import requests, json, time
from bs4 import BeautifulSoup
####################
class TwApi:
    def __init__(self):
        self.client_id = credentials.client_id
        self.secret = credentials.secret
        self.token = self.get_token()

# To make requests in Python, use the `requests` library
# The json library is used to parse the response
# the URL base 
    def get_token(self):
        '''
        Returns an OAuth client credentials flow App token for an associated client id.
        Prints the status code (200 = success, 400 = failure).
        Prints the token expiration.
        '''
        auth_url = 'https://id.twitch.tv/oauth2/token'
        # parameters for token request with credentials
        auth_params = {'client_id': self.client_id,
                       'client_secret': self.secret,
                       'grant_type': 'client_credentials',
                       'scope':''}
        # Request response, using the url base and params to structure the request
        auth_response = requests.post(auth_url, params = auth_params)
        # Status code 200 means the request was successful
        print(f'Status code: {auth_response.status_code}')
        # Get the expiration time of token in seconds, divide by 3600 to get hours
        exp_time = round(auth_response.json()['expires_in'] / 3600, 2)
        print(f'This token expires in {exp_time} hours')
        token = auth_response.json()['access_token']
        return token


# takes the query type (users, channels, games, streams etc)
# the argument being searched for (id, login, display_name) etc
# and the channel (ie: gmhikaru (for login), 103268673 (for id))
    def request_it(self, query, fields):
        '''
        Makes a GET request from the Twitch.tv helix API.
        Receives a string for the query ex: users, games/top, search/categories...,
        and a dict for the field parameter ex: {'login': 'gmhikaru'}
        '''
        # the base url for making api requests
        base_url = 'https://api.twitch.tv/helix/'
        # authorization information
        headers = {'client-id': self.client_id,
                   'Authorization': f'Bearer {self.token}'}
        # type of query, users gets the 
        response = requests.get(base_url + query,
                                headers = headers,
                                params = fields)
        print(f'Status code: {response.status_code}')
#         print(f'Request URL: {response.url}')
        return response.json()


    def unwrap_list_of_lists(self, list_of_lists):
        '''
        Unwraps list of list structures.
        Receives a nested list structure [list0, list1, list2, ...].
        Returns each of the elements from each of the lists as an unnested list.
        '''
        lst = []
        for i in range(len(list_of_lists)):
            for j in range(len(list_of_lists[i])):
                lst.append(list_of_lists[i][j])
#             print(len(lst))
        return lst


    def get_stream_list(self, n_pages = 1):
        '''
        Gets the top 100 currently live streams per page, sorted by viewer count.
        The argument is n_pages, number of pages to be queried.
        Prints the status code (200 = success, 400 = failure) per request.
        Prints the request URL per page.
        Prints the number of elements per page.
        '''
        pages = []
        cursor = ''
        for i in range(n_pages):
            response = self.request_it('streams', {'first': 100,
                                              'after': cursor})
            pages.append(response['data'])
            try:
                cursor = response['pagination']['cursor']
            except:
                break
        return self.unwrap_list_of_lists(pages)
    
#################################################################
#################################################################
#################################################################

from fake_useragent import UserAgent
ua = UserAgent()
def scrape(user_names):
    url_base = 'https://twitchtracker.com/'
    i = 0
    proxies = get_proxies()
    proxy_rotator = cycle(proxies)
    proxy = next(proxy_rotator)
    for user in user_names:
        error_count = 0
        while True:
            try:
                if error_count > len(proxies):
                    proxies = get_proxies()
                    proxy_rotator = cycle(proxies)
                    proxy = next(proxy_rotator)
                if error_count > 5:
                    proxy = next(proxy_rotator)
                real_user_agent = ua.random
                headers = {'User-Agent': real_user_agent}
                temp_soup = BeautifulSoup(
                    requests.get(
                        url_base + user + '/statistics',
                        headers=headers,
                        proxies={"http": proxy, "https": proxy},
                        timeout=2
                    ).text, 
                    'html.parser')
                if '404' in temp_soup.title.text:
                    print('Page not found')
                    i += 1
                    time.sleep(5)
                    break
                if '403 Forbidden' in temp_soup.title.text:
                    print('Proxy blocked-retrying')
                    proxy = next(proxy_rotator)
                    continue
                if 'Attention Required' in temp_soup.title.text:
                    print('Captcha needed-retrying')
                    proxy = next(proxy_rotator)
                    continue
                if 'Access Denied' in temp_soup.title.text:
                    print('Proxy blocked')   
                    proxy = next(proxy_rotator)
                    continue
                text_file = open(f"./html2/twitchtracker-{user}.html", "w")
                text_file.write(f'{temp_soup}')
                text_file.close()
                print(f'Success: {i} {user} {proxy}')
                i += 1
                time.sleep(4)
            except:
                print('Failed')
                error_count += 1
                continue
            break
    return
    
    
def soup_parser(soup):
    try:
        dict_labels = [
            'Hours streamed',
            'Average viewers' ,
            'Peak viewers',
            'Days of activity',
            'Total games streamed',
            'Daily broadcast time',
            'hours watched daily',
            'followers per stream',
            'views per stream',
            'followers per hour',
            'views per hour']
        span = soup.findAll('span', {'class': 'to-number'})
        data_dict = dict(zip(dict_labels, [i.get_text() for i in span]))
        data_dict['login'] = soup.findAll('div', {'id' : 'app-title'})[0].get_text().strip('\n')
        data_dict['Hours Watched'] = soup.findAll('span', {'class': 'to-number-lg'})[2].get_text()
        td = soup.findAll('td')
        data_dict2 = dict(zip([i.get_text() for i in td][::2], [i.get_text().replace('\n','') for i in td][1::2]))
        data_dict.update(data_dict2)
        return data_dict
    except:
        return


    
import requests
from bs4 import BeautifulSoup
from itertools import cycle
def get_proxies():
    url_base = 'https://free-proxy-list.net/'
    real_user_agent = ua.random
    headers = {'User-Agent': real_user_agent}
    soup = BeautifulSoup(requests.get(url_base,
                                           headers=headers).text,
                              'html.parser')
    rows=[]
    for row in soup.findAll("tr"):
        rows.append(row)
    valid_ips = []
    for row in rows:
        i = row.findAll('td')
        try:
            if i[4].text == 'elite proxy' and i[6].text == 'yes':
                valid_ips.append(i[0].text + ':' + i[1].text)
        except:
            continue
    return valid_ips