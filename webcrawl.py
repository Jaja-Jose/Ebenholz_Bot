#This file is dedicated to web searching on Gamepress 

from bs4 import BeautifulSoup
import requests


def find_name(char_name):
    global operator_info
    if char_name in operator_info.keys():
        return True
    else: 
        return False


def find_stats(char_name):
    global operator_info
    stats = operator_info[char_name]
    return stats

def find_e1art(char_name):
    global operator_info
    starting_url = "https://gamepress.gg"
    operator_html = operator_info[char_name][6]
    new_html = starting_url + operator_html
    response = requests.get(new_html)
    print("Here is the status response for gamepress:", response.status_code)
    op_soup = BeautifulSoup(response.content, "html.parser")
    all_images = op_soup.find_all("div", {"id": "image-tab-2"})
    return all_images[0].a["href"]


def find_e2art(char_name):

    global operator_info

    if int(operator_info[char_name][0]) < 4:
        return f"{char_name} does not have an e2 splash art."

    else:
        starting_url = "https://gamepress.gg"
        operator_html = operator_info[char_name][6]
        new_html = starting_url + operator_html
        response = requests.get(new_html)
        print("Here is the status response for gamepress:", response.status_code)
        op_soup = BeautifulSoup(response.content, "html.parser")
        all_images = op_soup.find_all("div", {"id": "image-tab-3"})

        return all_images[0].a["href"]


def find_desc(char_name):
    global operator_info
    starting_url = "https://gamepress.gg"
    operator_html = operator_info[char_name][6]
    new_html = starting_url + operator_html
    response = requests.get(new_html)
    print("Here is the status response for gamepress:", response.status_code)
    op_soup = BeautifulSoup(response.content, "html.parser")


    # This finds the operator's archetype
    op_arch_link = op_soup.find("a", {"class": "archetype-img-link"})
    op_archetype = op_arch_link.span.string

    # This finds misc. info about the operator
    all_info = op_soup.find("div", {"class": "profile-cell"})
    small_info = all_info.find_all("a", {"hreflang": "en"})
    info_list = []

    for each_info in small_info:
        info_list.append(each_info.string)

    #info_list has a list consisting of the following:
    # [illustrator, [VA(s)], gender, race]
    # IMPORTANT: The second element is NOT a list. There can be any number of VAs between
    # illustrator and gender. So the list could be at least four elements long or even
    # 7 elements long as some characters have 4 VAs

    #Here are the objects in this list: [Rarity, Class, Archetype, illustrator, gender, race]
    description = [operator_info[char_name][0], operator_info[char_name][5], op_archetype, info_list[0], info_list[-2], info_list[-1]]
    return description



url = "https://gamepress.gg/arknights/tools/interactive-operator-list#tags=null##cn##stats"
response = requests.get(url)
print("Here is the status response for gamepress:", response.status_code)

soup = BeautifulSoup(response.content, "html.parser")

alldivs = soup.find_all("tr", {"class": "operators-row"})
testing = []
operator_info = {}


# Here is the dictionary format for each operator
# {operator name : [rarity, hp, attack, def, res, class, link to personal html page]}
for each_operator in alldivs:
    operator_info[each_operator["data-name"]] = [each_operator["data-rarity"], each_operator["data-hp-trust"], each_operator["data-atk-trust"], each_operator["data-def-trust"], each_operator["data-res"], each_operator["data-profession"], each_operator.div.a["href"] ] 
