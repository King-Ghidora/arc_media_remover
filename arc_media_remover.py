import xmltodict
import json
import os

def file_search(dir, uuid_list, func):
    files = os.listdir(dir)
    for file in files:
        fullname_file = os.path.join(dir, file)
        if os.path.isdir(fullname_file):
            file_search(fullname_file, uuid_list, func)
        else:
            func(dir, file, uuid_list)

def check_and_delete(dir, file, uuid_list):
    if file not in uuid_list:
        os.remove(os.path.join(dir, file))
        #print(f'- file {os.path.join(dir, file)} shall be deleted:')
        
    
data_dir = './'

game_file_name = data_dir + 'games.xml'
game_list = None
with open(game_file_name, 'r', encoding='utf8') as game_file:
    xml_data = xmltodict.parse(game_file.read())
    game_list = xml_data['abedata']['entry']

if game_list == None:
    raise Exception('No game data found...')

used_asset_list = list()
for game_data in game_list:
    data = game_data['data']
    hidden = True
    asset_uuid = None
    for item in data:
        if item['@key'] == 'name':
            name = item['#text']
        elif item['@key'] == 'hidden' and item['#text'] == 'false':
            hidden = False
        elif item['@key'] == 'assetUUID':
            asset_uuid = item['#text']
    if hidden == False and asset_uuid != None:
        used_asset_list.append(asset_uuid)
        
artwork_dir = data_dir + "artwork"
file_search(artwork_dir, used_asset_list, check_and_delete)

