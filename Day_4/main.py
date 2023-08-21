import requests
from bs4 import BeautifulSoup
import lxml
import json
from tqdm import tqdm


headers = {
    'user-agent': '',
}


def get_data(url):
    r = requests.get(url=url, headers=headers)
    bs = BeautifulSoup(r.text, 'lxml')
    items: list[BeautifulSoup] = bs.find('div', class_='fixedContent').find_all('a', class_='mntl-card-list-items')
    data = {}

    for item in tqdm(items):
        recipe_url = item.get('href')
        ir = requests.get(url=recipe_url, headers=headers)
        ibs = BeautifulSoup(ir.text, 'lxml')

        recipe_name = ibs.find('h1').text.strip()
        try:
            ingredients_list = ibs.find(class_='mntl-structured-ingredients__list').find_all('li')
        except Exception:
            ingredients_list = []
        recipe_ingredients = [ingr.text.strip() for ingr in ingredients_list]

        data[recipe_name] = recipe_ingredients
        

    return data


def main():
    url = input('Enter the url from "allrecipes.com" with a list of items: ')
    data = get_data(url)
    
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
