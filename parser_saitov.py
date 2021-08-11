import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import sys


class ParserSaitov():

    def parse_url(self, url):
        try:
            response = requests.get(url)
        except:
            """Обработка ошибки с SSL сертификатом (когда на странице одновременно урлы с http и https"""
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.get(url, verify=False)

        if response.status_code == 200:
            return response
        else:
            http_status = 'Ошибка! Ответ сервера' + f' {response.status_code}'
            return print(http_status)


    def load_soup(self, response_from_requests):
        # Строку ниже применяем когда в заголовках не указана кодировка, т.к. по умолчанию ISO-8859-1
        response_from_requests.encoding = response_from_requests.apparent_encoding

        soup = BeautifulSoup(response_from_requests.text, 'html.parser')
        return soup


    def parse_url_load_soup(self, url):
        try:
            response = requests.get(url)
        except:
            """Обработка ошибки с SSL сертификатом (когда на странице одновременно урлы с http и https"""
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.get(url, verify=False)

        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            http_status = 'Ошибка! Ответ сервера' + f' {response.status_code}'
            return print(http_status)


class ParserTables(ParserSaitov):

    def parse_all_tables_in_page(self, soup):
        """Загружаем все таблицы со страницы"""
        tables = soup.find_all('table')
        return tables

    def parse_html_table_for_pandas(self, table):
        """Парсим таблицу и создаем из нее Pandas DataFrame"""
        n_columns = 0
        n_rows = 0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

            # Handle column names if we find them
            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        df = pd.DataFrame(columns=columns,
                          index=range(0, n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker, column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1

        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass

        return df

    def pandas_convert_to_html(self, data):
        """Конвертируем из Pandas DataFrame в HTML"""
        data_html = data.to_html(header=None, border=None, classes=None, index=None)
        return data_html

class ParserMetaTags(ParserSaitov):


    def get_title(self, soup) -> str:
        title = soup.title.string
        return title


    def get_h1(self, soup) -> list:
        h1 = soup.find_all('h1')
        quantity_h1 = len(h1)
        if quantity_h1 == 0:
            return None
        elif quantity_h1 >= 1:
            return h1
        return h1


    def get_h2(self, soup) -> list:
        h2 = soup.find_all('h2')
        quantity_h2 = len(h2)
        if quantity_h2 == 0:
            return None
        elif quantity_h2 >= 1:
            return h2


    def get_description(self, soup) -> str:
        description = soup.find('meta', {'name': 'description'}).attrs['content']
        return description


    def get_keywords(self, soup) -> str:
        keywords = soup.find('meta', {'name': 'keywords'}).attrs['content']
        return keywords


    def get_body(self, soup) -> str:
        body = soup.find('body')
        return body


    def get_all_links(self, soup) -> list:
        links = soup.find_all('a')
        return links


"""
 print(link.get('href')) - получить из ссылки url
 print(stroka.get_text()) - получить текст между тегами

"""







url = 'http://www.splav-kharkov.com/choose_type.php'
url2 = 'http://metallicheckiy-portal.ru/marki_metallov/tit/VT3-1'
url3 = 'https://sterbrust.com/catalog/vertikalno-sverlilnye-stanki-proma/nastolnyy-sverlilnyy-stanok-proma-e-1516b-230-25231501/'


parser = ParserMetaTags()

soup = parser.parse_url_load_soup(url2)

h1 = parser.get_all_links(soup)
for link in h1:


    print(link.get('href'))

