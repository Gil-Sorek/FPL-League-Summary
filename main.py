# -*- coding: utf-8 -*-
"""
@author: Gil Sorek

GW Summary for Fantasy Premier-League (FPL)
"""

import requests
import math
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.ticker import MaxNLocator
from PIL import Image, ImageDraw, ImageFont
        
def get_player_webname(id): return players_stats[id]['web_name']
# def get_team_name(id): return team_name[id]
def get_team_name(id): return {4399125:"Avidan", 1606327:"Itamar", 262514:"Ginosar", 6697062:"Amit", 4047743:"Fuji", 957:"Gool", 247071:"Woolf", 2513453:"Talash", 2232819:"Vaknin", 4242417:"Buchris", 5859886:"Adi", 1256987:"Casyopa", 6621645:"Pellinho", 4081730:"Oren", 409287:"Tomer", 4536384:"Gloter", 350212:"Gissin", 7492779:"Asaf", 4703751:"Tal"}[id]
# def get_club(id): return {4399125:"Arsenal", 1606327:"Man Utd", 262514:"Man City", 6697062:"Brighton", 4047743:"Man Utd", 957:"Man City", 247071:"Liverpool", 2513453:"Man City", 2232819:"Arsenal", 4242417:"Tottenham", 5859886:"Liverpool", 1256987:"Chelsea", 6621645:"Tottenham", 4081730:"Arsenal", 409287:"Tomer", 4536384:"Gloter", 350212:"Gissin", 7492779:"Asaf", 4703751:"Tal"}[id]
def get_chip_name(chip): return {'bboost': "Bench-Boost", 'freehit': "Free-Hit", 'wildcard': "Wildcard", '3xc': "Triple-Captain"}[chip]
def element_type_to_pos(type): return {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}[type]
def generate_league_plot():
    def title_box(x1,y1,x2,y2,radius):
        draw.ellipse([(x1, y1), (x1 + 2 * radius, y2)],
                     fill="black", outline="white", width=2)
        draw.ellipse([(x2 - 2 * radius, y1), (x2, y2)],
                     fill="black", outline="white", width=2)
        draw.rectangle([(x1 + radius, y1), (x2 - radius, y2)],
                       fill="black", outline="black", width=2)
        draw.line([(x1 + radius, y1), (x2 - radius, y1)],fill="white", width=2)
        draw.line([(x1 + radius, y2), (x2 - radius, y2)],fill="white", width=2)
    def title_text(text_up,text_down,textbox_x1,textbox_y1,textbox_width,textbox_height,color='white'):
        font_up = ImageFont.truetype("C:/Users/Gil/Documents/FPL/FPL Statistics/Summary/2024-25/Arial Bold.ttf", size=40)
        bbox_up = draw.textbbox((0, 0), text_up, font=font_up)
        text_up_width = bbox_up[2] - bbox_up[0]
        text_up_height = bbox_up[3] - bbox_up[1]
        text_up_x = textbox_x1 + (textbox_width//2) - (text_up_width//2)
        text_up_y = textbox_y1 + (textbox_height//2) - text_up_height - bbox_up[1]
        
        # text_y = row_top + (row1_height//2) - row1_text_height - row1_bbox[1] - (row1_height//10)
        
        # bidi_text = bidi.algorithm.get_display(text_up)
        draw.text((text_up_x, text_up_y), text_up, fill="white", font=font_up)
        font_down = ImageFont.truetype("arial.ttf", size=40)
        bbox_down = draw.textbbox((0, 0), text_down, font=font_down)
        text_down_width = bbox_down[2] - bbox_down[0]
        text_down_x = textbox_x1 + (textbox_width//2) - (text_down_width//2)
        text_down_y = textbox_y1 + (textbox_height//2)
        # bidi_text = bidi.algorithm.get_display(text_down)
        draw.text((text_down_x, text_down_y), text_down, fill=color, font=font_down)
    def image(player,x1,y1,height,width):
        url = f"https://resources.premierleague.com/premierleague/photos/players/250x250/p{players_stats[player]['code']}.png"
        icon = Image.open(BytesIO(requests.get(url).content)).resize((height,width))
        template.paste(icon,(int(x1),int(y1)),icon)
    def shirt(id,x1,y1,height,width):
        team = get_club(id) if id != 'Empty' else 'Empty'
        icon = Image.open(f"shirts/{team}.webp").resize((height,width))
        template.paste(icon,(int(x1),int(y1)),icon)
        if team != 'Empty':
            draw_team_name(id,x1,y1,height,width)
    def icon_image(file,x1,y1,height,width):
        icon = Image.open(f"icons/{file}.png").resize((height,width))
        icon = icon.convert("RGBA")
        template.paste(icon,(int(x1),int(y1)),icon)
    def draw_team_name(id,shirt_x1,shirt_y1,shirt_height,shirt_width):
        name = get_team_name(id)
        x1 = shirt_x1 + (shirt_width//2) - (team_textbox_width//2)
        y1 = shirt_y1 + shirt_height - cat_textbox_height - title_to_picture_padding - team_textbox_height
        x2 = x1 + team_textbox_width
        y2 = y1 + team_textbox_height
        radius = (team_textbox_height//2)
        draw.ellipse([(x1, y1), (x1 + 2 * radius, y2)],
                     fill="white", outline="black", width=2)
        draw.ellipse([(x2 - 2 * radius, y1), (x2, y2)],
                     fill="white", outline="black", width=2)
        draw.rectangle([(x1 + radius, y1), (x2 - radius, y2)],
                       fill="white", outline="black", width=2)
        draw.line([(x1 + radius, y1+2), (x1 + radius, y2-2)],fill="white", width=2)
        draw.line([(x2 - radius, y1+2), (x2 - radius, y2-2)],fill="white", width=3)
        
        font = ImageFont.truetype("arial.ttf", size=30)
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = x1 + (team_textbox_width//2) - (text_width//2)
        text_y = y1 + (team_textbox_height//2) - text_height + bbox[1]
        draw.text((text_x, text_y), name, fill="black", font=font)
    def draw_cat(shirt_x1,shirt_y1,shirt_height,shirt_width,cat='Highest Team Score'):
        x1 = shirt_x1 + (shirt_width//2) - (cat_textbox_width//2)
        y1 = shirt_y1 + shirt_height - cat_textbox_height
        x2 = x1 + cat_textbox_width
        y2 = y1 + cat_textbox_height
        radius = (cat_textbox_height//2)
        draw.ellipse([(x1, y1), (x1 + 2 * radius, y2)],
                     fill="white", outline="black", width=2)
        draw.ellipse([(x2 - 2 * radius, y1), (x2, y2)],
                     fill="white", outline="black", width=2)
        draw.rectangle([(x1 + radius, y1), (x2 - radius, y2)],
                       fill="white", outline="black", width=2)
        draw.line([(x1 + radius, y1+2), (x1 + radius, y2-2)],fill="white", width=2)
        draw.line([(x2 - radius, y1+2), (x2 - radius, y2-2)],fill="white", width=3)
        font = ImageFont.truetype("arial.ttf", size=25)
        if cat == 'Best Captain':
            if len(max_bst_cptn) == 1:
                font = ImageFont.truetype("arial.ttf", size=35)
                text = f"{get_team_name(max_bst_cptn[0])}"
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                text_x = x1 + (cat_textbox_width//2) - (text_width//2)
                text_y = y1 + (cat_textbox_height//2) - text_height + bbox[1]
                draw.text((text_x, text_y), text, fill="black", font=font)
            elif len(max_bst_cptn) == 2:
                font = ImageFont.truetype("arial.ttf", size=30)
                text1 = f"{get_team_name(max_bst_cptn[0])}"
                bbox1 = draw.textbbox((0, 0), text1, font=font)
                text1_width = bbox1[2] - bbox1[0]
                text1_height = bbox1[3] - bbox1[1]
                text1_x = x1 + (cat_textbox_width//2) - (text1_width//2)
                text1_y = y1 + (cat_textbox_height//2) - text1_height - bbox1[1] - 3
                # text_y = row_top + (row1_height//2) - row1_text_height - row1_bbox[1] - (row1_height//10)
                draw.text((text1_x, text1_y), text1, fill="black", font=font)
                text2 = f"{get_team_name(max_bst_cptn[1])}"
                bbox2 = draw.textbbox((0, 0), text2, font=font)
                text2_width = bbox2[2] - bbox2[0]
                text2_height = bbox2[3] - bbox2[1]
                text2_x = x1 + (cat_textbox_width//2) - (text2_width//2)
                text2_y = y1 + (cat_textbox_height//2) - bbox2[1] + 3
                # text_y = row_top + (row1_height//2) - row2_bbox[1] + (row1_height//10)
                draw.text((text2_x, text2_y), text2, fill="black", font=font)
            else:
                font = ImageFont.truetype("arial.ttf", size=30)
                icon_height = 55
                icon_width = icon_height
                icon_y1 = y1 + (cat_textbox_height//2) - (icon_height//2)
                text = f"x {len(max_bst_cptn)}"
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                text_x = x1 + (cat_textbox_width//2)
                text_y = icon_y1 + (icon_height//2) - text_height + bbox[1]
                icon_x1 = text_x - icon_width
                icon_image('person',icon_x1,icon_y1,icon_height,icon_width)
                draw.text((text_x, text_y), text, fill="black", font=font)
        elif cat == 'Highest Team Score':
            rank = format(gw_data[max(gw_points, key=gw_points.get)]['entry_history']['rank'],',d')
            #rank = '123,456'
            icon_height = 60
            icon_width = icon_height
            icon_x1 = x1
            icon_y1 = y1 + (cat_textbox_height//2) - (icon_height//2)
            bbox = draw.textbbox((0, 0), rank, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = icon_x1 + icon_width
            if len(rank) == 9:
                text_x = text_x - 16
            else:
                icon_x1 = icon_x1 + 5
                text_x = text_x - 5
            text_y = icon_y1 + (icon_height//2) - text_height + bbox[1] + 5
            icon_image('location',icon_x1,icon_y1,icon_height,icon_width)
            draw.text((text_x, text_y), rank, fill="black", font=font)
        elif cat == 'Hits':
            font = ImageFont.truetype("arial.ttf", size=30)
            icon_height = 55
            icon_width = icon_height
            icon_y1 = y1 + (cat_textbox_height//2) - (icon_height//2)
            text = f"x {int(max(hits.values())/4)}" if len(hits)>0 else "x 0"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = x1 + (cat_textbox_width//2)
            text_y = icon_y1 + (icon_height//2) - text_height + bbox[1]
            icon_x1 = text_x - icon_width
            icon_image('penalty',icon_x1,icon_y1,icon_height,icon_width)
            draw.text((text_x, text_y), text, fill="black", font=font)
        elif cat == 'Money ITB':
            icon1_height = 60
            icon1_width = icon1_height
            icon2_height = 50
            icon2_width = icon2_height
            icon1_x1 = x1 + (cat_textbox_width//2) - icon1_width
            icon1_y1 = y1 + (cat_textbox_height//2) - (icon1_height//2)
            icon2_x1 = icon1_x1 + icon1_width + 5
            icon2_y1 = icon1_y1
            icon_image('money',icon1_x1,icon1_y1,icon1_height,icon1_width)
            icon_image('bank',icon2_x1,icon2_y1,icon2_height,icon2_width)
        elif cat == 'Green Arrows':
            font = ImageFont.truetype("arial.ttf", size=30)
            icon_height = 50
            icon_width = icon_height
            icon_y1 = y1 + (cat_textbox_height//2) - (icon_height//2)
            text = f"x {max(green_streaks.values())}"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = x1 + (cat_textbox_width//2) + 5
            text_y = icon_y1 + (icon_height//2) - text_height + bbox[1]
            icon_x1 = x1 + (cat_textbox_width//2) - icon_width
            icon_image('green-arrow',icon_x1,icon_y1,icon_height,icon_width)
            draw.text((text_x, text_y), text, fill="black", font=font)
        elif cat == 'Lowest Team Value':
            icon_height = 92
            icon_width = icon_height
            icon_x1 = x1 + (cat_textbox_width//2) - (icon_width//2)
            icon_y1 = y1 + (cat_textbox_height//2) - (icon_height//2)
            icon_image('decrease',icon_x1,icon_y1,icon_height,icon_width)
        elif cat == 'Highest Team Value':
            icon_height = 92
            icon_width = icon_height
            icon_x1 = x1 + (cat_textbox_width//2) - (icon_width//2)
            icon_y1 = y1 + (cat_textbox_height//2) - (icon_height//2) + 1
            icon_image('increase',icon_x1,icon_y1,icon_height,icon_width)
        elif cat == 'Golden Glove':
            icon_height = 60
            icon_width = icon_height
            icon_x1 = x1 + (cat_textbox_width//2) - (icon_width//2)
            icon_y1 = y1 + (cat_textbox_height//2) - (icon_height//2)
            icon_image('golden-glove',icon_x1,icon_y1,icon_height,icon_width)
        elif cat == 'Transfer Gain':
            icon_height = 50
            icon_width = icon_height
            icon1_x1 = x1 + (cat_textbox_width//2) - icon_width
            icon1_y1 = y1 + (cat_textbox_height//2) - (icon_height//2)
            icon2_x1 = icon1_x1 + icon_width + 5
            icon2_y1 = icon1_y1
            icon_image('transfer',icon1_x1,icon1_y1,icon_height,icon_width)
            icon_image('success',icon2_x1,icon2_y1,icon_height,icon_width)
        elif cat == 'Bench Points':
            icon_height = 50
            icon_width = icon_height
            icon1_x1 = x1 + (cat_textbox_width//2) - icon_width
            icon1_y1 = y1 + (cat_textbox_height//2) - (icon_height//2)
            icon2_x1 = icon1_x1 + icon_width + 5
            icon2_y1 = icon1_y1
            icon_image('bench',icon1_x1,icon1_y1,icon_height,icon_width)
            icon_image('trash-can',icon2_x1,icon2_y1,icon_height,icon_width)
        elif cat == 'Substitution Points':
            icon_height = 50
            icon_width = icon_height
            icon1_x1 = x1 + (cat_textbox_width//2) - icon_width
            icon1_y1 = y1 + (cat_textbox_height//2) - (icon_height//2)
            icon2_x1 = icon1_x1 + icon_width + 5
            icon2_y1 = icon1_y1
            icon_image('bench',icon1_x1,icon1_y1,icon_height,icon_width)
            icon_image('success',icon2_x1,icon2_y1,icon_height,icon_width)
        elif cat == 'FWD':
            icon_height = 50
            icon_width = icon_height
            icon1_x1 = x1 + (cat_textbox_width//2) - icon_width
            icon1_y1 = y1 + (cat_textbox_height//2) - (icon_height//2)
            icon2_x1 = icon1_x1 + icon_width + 5
            icon2_y1 = icon1_y1
            icon_image('forward',icon1_x1,icon1_y1,icon_height,icon_width)
            icon_image('king',icon2_x1,icon2_y1,icon_height,icon_width)
        elif cat == 'MID':
            icon_height = 50
            icon_width = icon_height
            icon1_x1 = x1 + (cat_textbox_width//2) - icon_width
            icon1_y1 = y1 + (cat_textbox_height//2) - (icon_height//2)
            icon2_x1 = icon1_x1 + icon_width
            icon2_y1 = icon1_y1
            icon_image('midfielder',icon1_x1,icon1_y1,icon_height,icon_width)
            icon_image('king',icon2_x1,icon2_y1,icon_height,icon_width)
        elif cat == 'DEF':
            icon_height = 50
            icon_width = icon_height
            icon1_x1 = x1 + (cat_textbox_width//2) - icon_width
            icon1_y1 = y1 + (cat_textbox_height//2) - (icon_height//2) + 2
            icon2_x1 = icon1_x1 + icon_width + 5
            icon2_y1 = y1 + (cat_textbox_height//2) - (icon_height//2)
            icon_image('defense',icon1_x1,icon1_y1,icon_height,icon_width)
            icon_image('king',icon2_x1,icon2_y1,icon_height,icon_width)
        elif cat == 'GK':
            icon_height = 50
            icon_width = icon_height
            icon1_x1 = x1 + (cat_textbox_width//2) - icon_width
            icon1_y1 = y1 + (cat_textbox_height//2) - (icon_height//2)
            icon2_x1 = icon1_x1 + icon_width + 5
            icon2_y1 = icon1_y1
            icon_image('goalkeeper',icon1_x1,icon1_y1,icon_height,icon_width)
            icon_image('king',icon2_x1,icon2_y1,icon_height,icon_width)
    def draw_row1(row_top):
        standings_logo_width = 315
        title_width = 1052
        image_padding = 100
        row_padding = 0.5*(template.size[0] - standings_logo_width - title_width - image_padding)
        
        # Standings logo
        standings_icon = Image.open("icons/podium.png").resize((standings_logo_width,row1_height))
        standings_icon = standings_icon.convert("RGBA")
        template.paste(standings_icon,(int(row_padding),int(row_top)),standings_icon)
        font = ImageFont.truetype("arial.ttf", size=35)
        position_textbox_width = 150
        position_textbox_height = 62
        # Position 1
        p1_textbox_x1 = row_padding + (standings_logo_width//2) - (position_textbox_width//2)
        p1_textbox_y1 = row_top - (position_textbox_height//2) - 5
        p1_textbox_x2 = p1_textbox_x1 + position_textbox_width
        p1_textbox_y2 = p1_textbox_y1 + position_textbox_height
        radius = (position_textbox_height//2)
        draw.ellipse([(p1_textbox_x1, p1_textbox_y1), (p1_textbox_x1 + 2 * radius, p1_textbox_y2)],
                     fill="white", outline="black", width=2)
        draw.ellipse([(p1_textbox_x2 - 2 * radius, p1_textbox_y1), (p1_textbox_x2, p1_textbox_y2)],
                     fill="white", outline="black", width=2)
        draw.rectangle([(p1_textbox_x1 + radius, p1_textbox_y1), (p1_textbox_x2 - radius, p1_textbox_y2)],
                       fill="white", outline="black", width=2)
        draw.line([(p1_textbox_x1 + radius, p1_textbox_y1+2), (p1_textbox_x1 + radius, p1_textbox_y2-2)],fill="white", width=2)
        draw.line([(p1_textbox_x2 - radius, p1_textbox_y1+2), (p1_textbox_x2 - radius, p1_textbox_y2-2)],fill="white", width=3)
        p1 = get_team_name(league_data['standings']['results'][0]['entry'])
        bbox = draw.textbbox((0, 0), p1, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = p1_textbox_x1 + (position_textbox_width//2) - (text_width//2)
        text_y = p1_textbox_y1 + (position_textbox_height//2) - text_height + bbox[1]
        draw.text((text_x, text_y), p1, fill="black", font=font)
        
        # Position 2
        p2_textbox_x1 = row_padding + (standings_logo_width//6) - (position_textbox_width//2)
        p2_textbox_y1 = row_top + 37
        p2_textbox_x2 = p2_textbox_x1 + position_textbox_width
        p2_textbox_y2 = p2_textbox_y1 + position_textbox_height
        radius = (position_textbox_height//2)
        draw.ellipse([(p2_textbox_x1, p2_textbox_y1), (p2_textbox_x1 + 2 * radius, p2_textbox_y2)],
                     fill="white", outline="black", width=2)
        draw.ellipse([(p2_textbox_x2 - 2 * radius, p2_textbox_y1), (p2_textbox_x2, p2_textbox_y2)],
                     fill="white", outline="black", width=2)
        draw.rectangle([(p2_textbox_x1 + radius, p2_textbox_y1), (p2_textbox_x2 - radius, p2_textbox_y2)],
                       fill="white", outline="black", width=2)
        draw.line([(p2_textbox_x1 + radius, p2_textbox_y1+2), (p2_textbox_x1 + radius, p2_textbox_y2-2)],fill="white", width=2)
        draw.line([(p2_textbox_x2 - radius, p2_textbox_y1+2), (p2_textbox_x2 - radius, p2_textbox_y2-2)],fill="white", width=3)
        p2 = get_team_name(league_data['standings']['results'][1]['entry'])
        bbox = draw.textbbox((0, 0), p2, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = p2_textbox_x1 + (position_textbox_width//2) - (text_width//2)
        text_y = p2_textbox_y1 + (position_textbox_height//2) - text_height + bbox[1]
        draw.text((text_x, text_y), p2, fill="black", font=font)
        
        # Position 3
        p3_textbox_x1 = row_padding + standings_logo_width - (standings_logo_width//6) - (position_textbox_width//2)
        p3_textbox_y1 = row_top + 81
        p3_textbox_x2 = p3_textbox_x1 + position_textbox_width
        p3_textbox_y2 = p3_textbox_y1 + position_textbox_height
        radius = (position_textbox_height//2)
        draw.ellipse([(p3_textbox_x1, p3_textbox_y1), (p3_textbox_x1 + 2 * radius, p3_textbox_y2)],
                     fill="white", outline="black", width=2)
        draw.ellipse([(p3_textbox_x2 - 2 * radius, p3_textbox_y1), (p3_textbox_x2, p3_textbox_y2)],
                     fill="white", outline="black", width=2)
        draw.rectangle([(p3_textbox_x1 + radius, p3_textbox_y1), (p3_textbox_x2 - radius, p3_textbox_y2)],
                       fill="white", outline="black", width=2)
        draw.line([(p3_textbox_x1 + radius, p3_textbox_y1+2), (p3_textbox_x1 + radius, p3_textbox_y2-2)],fill="white", width=2)
        draw.line([(p3_textbox_x2 - radius, p3_textbox_y1+2), (p3_textbox_x2 - radius, p3_textbox_y2-2)],fill="white", width=3)
        p3 = get_team_name(league_data['standings']['results'][2]['entry'])
        bbox = draw.textbbox((0, 0), p3, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = p3_textbox_x1 + (position_textbox_width//2) - (text_width//2)
        text_y = p3_textbox_y1 + (position_textbox_height//2) - text_height + bbox[1]
        draw.text((text_x, text_y), p3, fill="black", font=font)
        
        # Title
        gw = e['id']
        font_main = ImageFont.truetype("arial.ttf", size=92)
        row1_text = f"Gameweek {gw}"
        row1_bbox = draw.textbbox((0, 0), row1_text, font=font_main)
        row1_text_width = row1_bbox[2] - row1_bbox[0]
        row1_text_height = row1_bbox[3] - row1_bbox[1]
        text_x = row_padding + standings_logo_width + image_padding + (title_width//2) - (row1_text_width//2)
        text_y = row_top + (row1_height//2) - row1_text_height - row1_bbox[1] - (row1_height//10)
        # bidi_text = bidi.algorithm.get_display(row1_text)
        draw.text((text_x, text_y), row1_text, fill="black", font=font_main)
        row2_text = f"{league_data['league']['name']}"
        row2_bbox = draw.textbbox((0, 0), row2_text, font=font_main)
        row2_text_width = row2_bbox[2] - row2_bbox[0]
        text_x = row_padding + standings_logo_width + image_padding + (title_width//2) - (row2_text_width//2)
        text_y = row_top + (row1_height//2) - row2_bbox[1] + (row1_height//10)
        draw.text((text_x, text_y), row2_text, fill="black", font=font_main)
    def draw_row2(row_top):
        row2_title_width = 350
        image_width = image_height
        row_padding = 0.2*(template.size[0]-4*row2_title_width)

        # Panel 1 (Most Captained)
        p1_title_x1 = row_padding
        p1_title_y1 = row_top
        p1_title_x2 = p1_title_x1 + row2_title_width
        p1_title_y2 = p1_title_y1 + title_height
        title_radius = title_height // 2
        title_box(p1_title_x1,p1_title_y1,p1_title_x2,p1_title_y2,title_radius)
        title_text("Most Captained", f"{max(captained.values())} Managers", p1_title_x1, p1_title_y1, row2_title_width, title_height)
        if len(max_captain) == 1:
            p1_image_x1 = p1_title_x1 + (row2_title_width//2) - (image_width//2)
            p1_image_y1 = p1_title_y2 + title_to_picture_padding
            image(max_captain[0],p1_image_x1,p1_image_y1,image_height,image_width)
        else:
            p1_image1_x1 = p1_title_x1 + (row2_title_width//2) - image_width + (image_width//10)
            p1_image1_y1 = p1_title_y2 + title_to_picture_padding
            image(max_captain[0],p1_image1_x1,p1_image1_y1,image_height,image_width)
            p1_image2_x1 = p1_title_x1 + (row2_title_width//2) - (image_width//10)
            p1_image2_y1 = p1_image1_y1
            image(max_captain[1],p1_image2_x1,p1_image2_y1,image_height,image_width)
        
        # Panel 2 (Best Captain)
        p2_title_x1 = p1_title_x1 + row2_title_width + row_padding
        p2_title_y1 = row_top
        p2_title_x2 = p2_title_x1 + row2_title_width
        p2_title_y2 = p2_title_y1 + title_height
        title_box(p2_title_x1,p2_title_y1,p2_title_x2,p2_title_y2,title_radius)
        title_text("Best Captain", f"{max(best_captained.values())} Points", p2_title_x1, p2_title_y1, row2_title_width, title_height,color='#c1ff72')
        if len(bst_cptn_ids) == 1:
            p2_image_x1 = p2_title_x1 + (row2_title_width//2) - (image_width//2)
            p2_image_y1 = p2_title_y2 + title_to_picture_padding
            image(bst_cptn_ids[0],p2_image_x1,p2_image_y1,image_height,image_width)
        else:
            p2_image1_x1 = p2_title_x1 + (row2_title_width//2) - image_width + (image_width//10)
            p2_image1_y1 = p2_title_y2 + title_to_picture_padding
            image(bst_cptn_ids[0],p2_image1_x1,p2_image1_y1,image_height,image_width)
            p2_image2_x1 = p2_title_x1 + (row2_title_width//2) - (image_width//10)
            p2_image2_y1 = p2_image1_y1
            image(bst_cptn_ids[1],p2_image2_x1,p2_image2_y1,image_height,image_width)
        p2_center_x = p2_title_x1 + (row2_title_width//2) - (image_width//2)
        p2_center_y = p2_title_y2 + title_to_picture_padding
        draw_cat(p2_center_x,p2_center_y,image_height,image_width,cat='Best Captain')
        
        # Panel 3 (Most Popular)
        p3_title_x1 = p2_title_x1 + row2_title_width + row_padding
        p3_title_y1 = row_top
        p3_title_x2 = p3_title_x1 + row2_title_width
        p3_title_y2 = p3_title_y1 + title_height
        title_box(p3_title_x1,p3_title_y1,p3_title_x2,p3_title_y2,title_radius)
        title_text("Most Popular", f"{max(selected.values())} Managers", p3_title_x1, p3_title_y1, row2_title_width, title_height)
        if len(max_selected) == 1:
            p3_image_x1 = p3_title_x1 + (row2_title_width//2) - (image_width//2)
            p3_image_y1 = p3_title_y2 + title_to_picture_padding
            image(max_selected[0],p3_image_x1,p3_image_y1,image_height,image_width)
        else:
            p3_image1_x1 = p3_title_x1 + (row2_title_width//2) - image_width + (image_width//10)
            p3_image1_y1 = p3_title_y2 + title_to_picture_padding
            image(max_selected[0],p3_image1_x1,p3_image1_y1,image_height,image_width)
            p3_image2_x1 = p3_title_x1 + (row2_title_width//2) - (image_width//10)
            p3_image2_y1 = p3_image1_y1
            image(max_selected[1],p3_image2_x1,p3_image2_y1,image_height,image_width)
        
        # Panel 4 (Highest Team Score)
        p4_title_x1 = p3_title_x1 + row2_title_width + row_padding
        p4_title_y1 = row_top
        p4_title_x2 = p4_title_x1 + row2_title_width
        p4_title_y2 = p4_title_y1 + title_height
        title_box(p4_title_x1,p4_title_y1,p4_title_x2,p4_title_y2,title_radius)
        title_text("Most Points", f"{max(gw_points.values())} Points", p4_title_x1, p4_title_y1, row2_title_width, title_height, color='#c1ff72')
        if len(max_gw_pts) == 1:
            p4_image_x1 = p4_title_x1 + (row2_title_width//2) - (image_width//2)
            p4_image_y1 = p4_title_y2 + title_to_picture_padding
            shirt(max_gw_pts[0],p4_image_x1,p4_image_y1,image_height,image_width)
        else:
            p4_image1_x1 = p4_title_x1 + (row2_title_width//2) - image_width + (image_width//10)
            p4_image1_y1 = p4_title_y2 + title_to_picture_padding
            shirt(max_gw_pts[0],p4_image1_x1,p4_image1_y1,image_height,image_width)
            p4_image2_x1 = p4_title_x1 + (row2_title_width//2) - (image_width//10)
            p4_image2_y1 = p4_image1_y1
            shirt(max_gw_pts[1],p4_image2_x1,p4_image2_y1,image_height,image_width)
        p4_center_x = p4_title_x1 + (row2_title_width//2) - (image_width//2)
        p4_center_y = p4_title_y2 + title_to_picture_padding
        draw_cat(p4_center_x,p4_center_y,image_height,image_width)
    def draw_row3(row_top):
        row3_title_width = 260
        image_width = image_height
        row_padding = (template.size[0]-5*row3_title_width)/6

        # Panel 1 (Hits)
        p1_title_x1 = row_padding
        p1_title_y1 = row_top
        p1_title_x2 = p1_title_x1 + row3_title_width
        p1_title_y2 = p1_title_y1 + title_height
        title_radius = title_height // 2
        title_box(p1_title_x1,p1_title_y1,p1_title_x2,p1_title_y2,title_radius)
        title_text("Hits", f"-{max(hits.values())} Points" if len(hits)>0 else "0 Points", p1_title_x1, p1_title_y1, row3_title_width, title_height, color='#ff3131')
        if len(max_hits) == 0:
            p1_image_x1 = p1_title_x1 + (row3_title_width//2) - (image_width//2)
            p1_image_y1 = p1_title_y2 + title_to_picture_padding
            shirt('Empty',p1_image_x1,p1_image_y1,image_height,image_width)
        elif len(max_hits) == 1:
            p1_image_x1 = p1_title_x1 + (row3_title_width//2) - (image_width//2)
            p1_image_y1 = p1_title_y2 + title_to_picture_padding
            shirt(max_hits[0],p1_image_x1,p1_image_y1,image_height,image_width)
        elif len(max_hits) == 2:
            p1_image1_x1 = p1_title_x1 + (row3_title_width//2) - image_width + (image_width//10)
            p1_image1_y1 = p1_title_y2 + title_to_picture_padding
            shirt(max_hits[0],p1_image1_x1,p1_image1_y1,image_height,image_width)
            p1_image2_x1 = p1_title_x1 + (row3_title_width//2) - (image_width//10)
            p1_image2_y1 = p1_image1_y1
            shirt(max_hits[1],p1_image2_x1,p1_image2_y1,image_height,image_width)
        else:
            p1_image_x1 = p1_title_x1 + (row3_title_width//2) - (image_width//2)
            p1_image_y1 = p1_title_y2 + title_to_picture_padding
            shirt('Empty',p1_image_x1,p1_image_y1,image_height,image_width)
        p1_center_x = p1_title_x1 + (row3_title_width//2) - (image_width//2)
        p1_center_y = p1_title_y2 + title_to_picture_padding
        draw_cat(p1_center_x,p1_center_y,image_height,image_width,cat='Hits')
        
        # Panel 2 (Money In The Bank)
        p2_title_x1 = p1_title_x1 + row3_title_width + row_padding
        p2_title_y1 = row_top
        p2_title_x2 = p2_title_x1 + row3_title_width
        p2_title_y2 = p2_title_y1 + title_height
        title_box(p2_title_x1,p2_title_y1,p2_title_x2,p2_title_y2,title_radius)
        title_text("Money ITB", f"{max(itb.values())}M £", p2_title_x1, p2_title_y1, row3_title_width, title_height)
        if len(max_itb) == 1:
            p2_image_x1 = p2_title_x1 + (row3_title_width//2) - (image_width//2)
            p2_image_y1 = p2_title_y2 + title_to_picture_padding
            shirt(max_itb[0],p2_image_x1,p2_image_y1,image_height,image_width)
        else:
            p2_image1_x1 = p2_title_x1 + (row3_title_width//2) - image_width + (image_width//10)
            p2_image1_y1 = p2_title_y2 + title_to_picture_padding
            shirt(max_itb[0],p2_image1_x1,p2_image1_y1,image_height,image_width)
            p2_image2_x1 = p2_title_x1 + (row3_title_width//2) - (image_width//10)
            p2_image2_y1 = p2_image1_y1
            shirt(max_itb[1],p2_image2_x1,p2_image2_y1,image_height,image_width)
        p2_center_x = p2_title_x1 + (row3_title_width//2) - (image_width//2)
        p2_center_y = p2_title_y2 + title_to_picture_padding
        draw_cat(p2_center_x,p2_center_y,image_height,image_width,cat='Money ITB')
        
        # Panel 3 (Green Arrows)
        p3_title_x1 = p2_title_x1 + row3_title_width + row_padding
        p3_title_y1 = row_top
        p3_title_x2 = p3_title_x1 + row3_title_width
        p3_title_y2 = p3_title_y1 + title_height
        title_box(p3_title_x1,p3_title_y1,p3_title_x2,p3_title_y2,title_radius)
        title_text("Rising Star", f"{max(green_streaks.values())} GWs", p3_title_x1, p3_title_y1, row3_title_width, title_height, color='#c1ff72')
        if len(max_greens) == 1:
            p3_image_x1 = p3_title_x1 + (row3_title_width//2) - (image_width//2)
            p3_image_y1 = p3_title_y2 + title_to_picture_padding
            shirt(max_greens[0],p3_image_x1,p3_image_y1,image_height,image_width)
        else:
            p3_image1_x1 = p3_title_x1 + (row3_title_width//2) - image_width + (image_width//10)
            p3_image1_y1 = p3_title_y2 + title_to_picture_padding
            shirt(max_greens[0],p3_image1_x1,p3_image1_y1,image_height,image_width)
            p3_image2_x1 = p3_title_x1 + (row3_title_width//2) - (image_width//10)
            p3_image2_y1 = p3_image1_y1
            shirt(max_greens[1],p3_image2_x1,p3_image2_y1,image_height,image_width)
        p3_center_x = p3_title_x1 + (row3_title_width//2) - (image_width//2)
        p3_center_y = p3_title_y2 + title_to_picture_padding
        draw_cat(p3_center_x,p3_center_y,image_height,image_width,cat='Green Arrows')
        
        # Panel 4 (Lowest Team Value)
        p4_title_x1 = p3_title_x1 + row3_title_width + row_padding
        p4_title_y1 = row_top
        p4_title_x2 = p4_title_x1 + row3_title_width
        p4_title_y2 = p4_title_y1 + title_height
        title_box(p4_title_x1,p4_title_y1,p4_title_x2,p4_title_y2,title_radius)
        title_text("Going Down", f"{min(team_value.values())}M £", p4_title_x1, p4_title_y1, row3_title_width, title_height, color='#ff3131')
        if len(min_team_value) == 1:
            p4_image_x1 = p4_title_x1 + (row3_title_width//2) - (image_width//2)
            p4_image_y1 = p4_title_y2 + title_to_picture_padding
            shirt(min_team_value[0],p4_image_x1,p4_image_y1,image_height,image_width)
        else:
            p4_image1_x1 = p4_title_x1 + (row3_title_width//2) - image_width + (image_width//10)
            p4_image1_y1 = p4_title_y2 + title_to_picture_padding
            shirt(min_team_value[0],p4_image1_x1,p4_image1_y1,image_height,image_width)
            p4_image2_x1 = p4_title_x1 + (row3_title_width//2) - (image_width//10)
            p4_image2_y1 = p4_image1_y1
            shirt(min_team_value[1],p4_image2_x1,p4_image2_y1,image_height,image_width)
        p4_center_x = p4_title_x1 + (row3_title_width//2) - (image_width//2)
        p4_center_y = p4_title_y2 + title_to_picture_padding
        draw_cat(p4_center_x,p4_center_y,image_height,image_width,cat='Lowest Team Value')
        
        # Panel 5 (Highest Team Value)
        p5_title_x1 = p4_title_x1 + row3_title_width + row_padding
        p5_title_y1 = row_top
        p5_title_x2 = p5_title_x1 + row3_title_width
        p5_title_y2 = p5_title_y1 + title_height
        title_box(p5_title_x1,p5_title_y1,p5_title_x2,p5_title_y2,title_radius)
        title_text("Going Up", f"{max(team_value.values())}M £", p5_title_x1, p5_title_y1, row3_title_width, title_height, color='#c1ff72')
        if len(max_team_value) == 1:
            p5_image_x1 = p5_title_x1 + (row3_title_width//2) - (image_width//2)
            p5_image_y1 = p5_title_y2 + title_to_picture_padding
            shirt(max_team_value[0],p5_image_x1,p5_image_y1,image_height,image_width)
        else:
            p5_image1_x1 = p5_title_x1 + (row3_title_width//2) - image_width + (image_width//10)
            p5_image1_y1 = p5_title_y2 + title_to_picture_padding
            shirt(max_team_value[0],p5_image1_x1,p5_image1_y1,image_height,image_width)
            p5_image2_x1 = p5_title_x1 + (row3_title_width//2) - (image_width//10)
            p5_image2_y1 = p5_image1_y1
            shirt(max_team_value[1],p5_image2_x1,p5_image2_y1,image_height,image_width)
        p5_center_x = p5_title_x1 + (row3_title_width//2) - (image_width//2)
        p5_center_y = p5_title_y2 + title_to_picture_padding
        draw_cat(p5_center_x,p5_center_y,image_height,image_width,cat='Highest Team Value')
    def draw_row4(row_top):
        row4_title_width = 320
        image_width = image_height
        row_padding = (template.size[0]-4*row4_title_width)/5

        # Panel 1 (Golden Glove)
        p1_title_x1 = row_padding
        p1_title_y1 = row_top
        p1_title_x2 = p1_title_x1 + row4_title_width
        p1_title_y2 = p1_title_y1 + title_height
        title_radius = title_height // 2
        title_box(p1_title_x1,p1_title_y1,p1_title_x2,p1_title_y2,title_radius)
        title_text("Golden Glove", f"{max(correct_gk.values())}% Success", p1_title_x1, p1_title_y1, row4_title_width, title_height, color='#c1ff72')
        if len(max_correct_gk) == 0:
            p1_image_x1 = p1_title_x1 + (row4_title_width//2) - (image_width//2)
            p1_image_y1 = p1_title_y2 + title_to_picture_padding
            shirt('Empty',p1_image_x1,p1_image_y1,image_height,image_width)
        elif len(max_correct_gk) == 1:
            p1_image_x1 = p1_title_x1 + (row4_title_width//2) - (image_width//2)
            p1_image_y1 = p1_title_y2 + title_to_picture_padding
            shirt(max_correct_gk[0],p1_image_x1,p1_image_y1,image_height,image_width)
        elif len(max_correct_gk) == 2:
            p1_image1_x1 = p1_title_x1 + (row4_title_width//2) - image_width + (image_width//10)
            p1_image1_y1 = p1_title_y2 + title_to_picture_padding
            shirt(max_correct_gk[0],p1_image1_x1,p1_image1_y1,image_height,image_width)
            p1_image2_x1 = p1_title_x1 + (row4_title_width//2) - (image_width//10)
            p1_image2_y1 = p1_image1_y1
            shirt(max_correct_gk[1],p1_image2_x1,p1_image2_y1,image_height,image_width)
        else:
            p1_image_x1 = p1_title_x1 + (row4_title_width//2) - (image_width//2)
            p1_image_y1 = p1_title_y2 + title_to_picture_padding
            shirt('Empty',p1_image_x1,p1_image_y1,image_height,image_width)
        p1_center_x = p1_title_x1 + (row4_title_width//2) - (image_width//2)
        p1_center_y = p1_title_y2 + title_to_picture_padding
        draw_cat(p1_center_x,p1_center_y,image_height,image_width,cat='Golden Glove')
        
        # Panel 2 (Transfer Gain)
        p2_title_x1 = p1_title_x1 + row4_title_width + row_padding
        p2_title_y1 = row_top
        p2_title_x2 = p2_title_x1 + row4_title_width
        p2_title_y2 = p2_title_y1 + title_height
        title_box(p2_title_x1,p2_title_y1,p2_title_x2,p2_title_y2,title_radius)
        title_text("Transfer Gain", f"{max(transfers_gain.values())} Points", p2_title_x1, p2_title_y1, row4_title_width, title_height, color='#c1ff72')
        if len(max_transfers_gain) == 1:
            p2_image_x1 = p2_title_x1 + (row4_title_width//2) - (image_width//2)
            p2_image_y1 = p2_title_y2 + title_to_picture_padding
            shirt(max_transfers_gain[0],p2_image_x1,p2_image_y1,image_height,image_width)
        else:
            p2_image1_x1 = p2_title_x1 + (row4_title_width//2) - image_width + (image_width//10)
            p2_image1_y1 = p2_title_y2 + title_to_picture_padding
            shirt(max_transfers_gain[0],p2_image1_x1,p2_image1_y1,image_height,image_width)
            p2_image2_x1 = p2_title_x1 + (row4_title_width//2) - (image_width//10)
            p2_image2_y1 = p2_image1_y1
            shirt(max_transfers_gain[1],p2_image2_x1,p2_image2_y1,image_height,image_width)
        p2_center_x = p2_title_x1 + (row4_title_width//2) - (image_width//2)
        p2_center_y = p2_title_y2 + title_to_picture_padding
        draw_cat(p2_center_x,p2_center_y,image_height,image_width,cat='Transfer Gain')
        
        # Panel 3 (Bench Points)
        p3_title_x1 = p2_title_x1 + row4_title_width + row_padding
        p3_title_y1 = row_top
        p3_title_x2 = p3_title_x1 + row4_title_width
        p3_title_y2 = p3_title_y1 + title_height
        title_box(p3_title_x1,p3_title_y1,p3_title_x2,p3_title_y2,title_radius)
        title_text("Bench Points", f"{max(bench_pts.values())} Points", p3_title_x1, p3_title_y1, row4_title_width, title_height, color='#ff3131')
        if len(max_bench_pts) == 1:
            p3_image_x1 = p3_title_x1 + (row4_title_width//2) - (image_width//2)
            p3_image_y1 = p3_title_y2 + title_to_picture_padding
            shirt(max_bench_pts[0],p3_image_x1,p3_image_y1,image_height,image_width)
        else:
            p3_image1_x1 = p3_title_x1 + (row4_title_width//2) - image_width + (image_width//10)
            p3_image1_y1 = p3_title_y2 + title_to_picture_padding
            shirt(max_bench_pts[0],p3_image1_x1,p3_image1_y1,image_height,image_width)
            p3_image2_x1 = p3_title_x1 + (row4_title_width//2) - (image_width//10)
            p3_image2_y1 = p3_image1_y1
            shirt(max_bench_pts[1],p3_image2_x1,p3_image2_y1,image_height,image_width)
        p3_center_x = p3_title_x1 + (row4_title_width//2) - (image_width//2)
        p3_center_y = p3_title_y2 + title_to_picture_padding
        draw_cat(p3_center_x,p3_center_y,image_height,image_width,cat='Bench Points')
        
        # Panel 4 (Substitution Points)
        p4_title_x1 = p3_title_x1 + row4_title_width + row_padding
        p4_title_y1 = row_top
        p4_title_x2 = p4_title_x1 + row4_title_width
        p4_title_y2 = p4_title_y1 + title_height
        title_box(p4_title_x1,p4_title_y1,p4_title_x2,p4_title_y2,title_radius)
        title_text("Subs Points", f"{max(subs_pts.values())} Points", p4_title_x1, p4_title_y1, row4_title_width, title_height, color='#c1ff72')
        if len(max_subs_pts) == 1:
            p4_image_x1 = p4_title_x1 + (row4_title_width//2) - (image_width//2)
            p4_image_y1 = p4_title_y2 + title_to_picture_padding
            shirt(max_subs_pts[0],p4_image_x1,p4_image_y1,image_height,image_width)
        else:
            p4_image1_x1 = p4_title_x1 + (row4_title_width//2) - image_width + (image_width//10)
            p4_image1_y1 = p4_title_y2 + title_to_picture_padding
            shirt(max_subs_pts[0],p4_image1_x1,p4_image1_y1,image_height,image_width)
            p4_image2_x1 = p4_title_x1 + (row4_title_width//2) - (image_width//10)
            p4_image2_y1 = p4_image1_y1
            shirt(max_subs_pts[1],p4_image2_x1,p4_image2_y1,image_height,image_width)
        p4_center_x = p4_title_x1 + (row4_title_width//2) - (image_width//2)
        p4_center_y = p4_title_y2 + title_to_picture_padding
        draw_cat(p4_center_x,p4_center_y,image_height,image_width,cat='Substitution Points')
    def draw_row5(row_top):
        font = ImageFont.truetype("arial.ttf", size=35)
        chip_image_width = chip_image_height
        text_padding = 20
        image_padding = 20
        total_chips_width = 0
        for chip in chips:
            if bool(chips[chip]):
                text = ','.join(list(map(get_team_name, chips[chip])))
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                #text_height = bbox[3] - bbox[1]
                total_chips_width += (2*text_padding + text_width + image_padding + chip_image_width)
        num_of_chips = sum(bool(values) for values in chips.values())
        row_padding = (template.size[0] - total_chips_width) / (num_of_chips+1)
        
        pointer_x1 = row_padding
        for chip in chips:
            if bool(chips[chip]):
                text = ','.join(list(map(get_team_name, chips[chip])))
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                textbox_x1 = pointer_x1
                textbox_y1 = row_top + (chip_image_height//2) - (chip_textbox_height//2)
                textbox_x2 = textbox_x1 + 2*text_padding + text_width
                textbox_y2 = textbox_y1 + chip_textbox_height
                radius = (chip_textbox_height//2)
                draw.ellipse([(textbox_x1, textbox_y1), (textbox_x1 + 2 * radius, textbox_y2)],
                             fill="white", outline="black", width=2)
                draw.ellipse([(textbox_x2 - 2 * radius, textbox_y1), (textbox_x2, textbox_y2)],
                             fill="white", outline="black", width=2)
                draw.rectangle([(textbox_x1 + radius, textbox_y1), (textbox_x2 - radius, textbox_y2)],
                               fill="white", outline="black", width=2)
                draw.line([(textbox_x1 + radius, textbox_y1+2), (textbox_x1 + radius, textbox_y2-2)],fill="white", width=2)
                draw.line([(textbox_x2 - radius, textbox_y1+2), (textbox_x2 - radius, textbox_y2-2)],fill="white", width=3)
                text_x = textbox_x1 + text_padding
                text_y = textbox_y1 + (chip_textbox_height//2) - text_height + bbox[1]
                draw.text((text_x, text_y), text, fill="black", font=font)
                chip_x1 = textbox_x2 + image_padding
                chip_y1 = row_top
                if chip == 'bboost':
                    chip_name = 'bench'
                elif chip == 'freehit':
                    chip_name = 'free'
                elif chip == 'wildcard':
                    chip_name = 'wildcard'
                else:
                    chip_name = 'cap'
                icon_image(chip_name,chip_x1,chip_y1,chip_image_height,chip_image_width)
                pointer_x1 = chip_x1 + chip_image_width + row_padding
    def draw_row6(row_top):
        row6_title_width = 310
        image_width = image_height
        row_padding = (template.size[0]-4*row6_title_width)/5

        # Panel 1 (FWD)
        p1_title_x1 = row_padding
        p1_title_y1 = row_top
        p1_title_x2 = p1_title_x1 + row6_title_width
        p1_title_y2 = p1_title_y1 + title_height
        title_radius = title_height // 2
        title_box(p1_title_x1,p1_title_y1,p1_title_x2,p1_title_y2,title_radius)
        title_text("Top FWD", f"{max(pos_total_points['FWD'].values())} Points", p1_title_x1, p1_title_y1, row6_title_width, title_height, color='#c1ff72')
        max_fwd = pts_by_positions[3][1]
        if len(max_fwd) == 1:
            p1_image_x1 = p1_title_x1 + (row6_title_width//2) - (image_width//2)
            p1_image_y1 = p1_title_y2 + title_to_picture_padding
            shirt(max_fwd[0],p1_image_x1,p1_image_y1,image_height,image_width)
        else:
            p1_image1_x1 = p1_title_x1 + (row6_title_width//2) - image_width + (image_width//10)
            p1_image1_y1 = p1_title_y2 + title_to_picture_padding
            shirt(max_fwd[0],p1_image1_x1,p1_image1_y1,image_height,image_width)
            p1_image2_x1 = p1_title_x1 + (row6_title_width//2) - (image_width//10)
            p1_image2_y1 = p1_image1_y1
            shirt(max_fwd[1],p1_image2_x1,p1_image2_y1,image_height,image_width)
        p1_center_x = p1_title_x1 + (row6_title_width//2) - (image_width//2)
        p1_center_y = p1_title_y2 + title_to_picture_padding
        draw_cat(p1_center_x,p1_center_y,image_height,image_width,cat='FWD')
        
        # Panel 2 (MID)
        p2_title_x1 = p1_title_x1 + row6_title_width + row_padding
        p2_title_y1 = row_top
        p2_title_x2 = p2_title_x1 + row6_title_width
        p2_title_y2 = p2_title_y1 + title_height
        title_box(p2_title_x1,p2_title_y1,p2_title_x2,p2_title_y2,title_radius)
        title_text("Top MID", f"{max(pos_total_points['MID'].values())} Points", p2_title_x1, p2_title_y1, row6_title_width, title_height, color='#c1ff72')
        max_mid = pts_by_positions[2][1]
        if len(max_mid) == 1:
            p2_image_x1 = p2_title_x1 + (row6_title_width//2) - (image_width//2)
            p2_image_y1 = p2_title_y2 + title_to_picture_padding
            shirt(max_mid[0],p2_image_x1,p2_image_y1,image_height,image_width)
        else:
            p2_image1_x1 = p2_title_x1 + (row6_title_width//2) - image_width + (image_width//10)
            p2_image1_y1 = p2_title_y2 + title_to_picture_padding
            shirt(max_mid[0],p2_image1_x1,p2_image1_y1,image_height,image_width)
            p2_image2_x1 = p2_title_x1 + (row6_title_width//2) - (image_width//10)
            p2_image2_y1 = p2_image1_y1
            shirt(max_mid[1],p2_image2_x1,p2_image2_y1,image_height,image_width)
        p2_center_x = p2_title_x1 + (row6_title_width//2) - (image_width//2)
        p2_center_y = p2_title_y2 + title_to_picture_padding
        draw_cat(p2_center_x,p2_center_y,image_height,image_width,cat='MID')
        
        # Panel 3 (DEF)
        p3_title_x1 = p2_title_x1 + row6_title_width + row_padding
        p3_title_y1 = row_top
        p3_title_x2 = p3_title_x1 + row6_title_width
        p3_title_y2 = p3_title_y1 + title_height
        title_box(p3_title_x1,p3_title_y1,p3_title_x2,p3_title_y2,title_radius)
        title_text("Top DEF", f"{max(pos_total_points['DEF'].values())} Points", p3_title_x1, p3_title_y1, row6_title_width, title_height, color='#c1ff72')
        max_def = pts_by_positions[1][1]
        if len(max_def) == 1:
            p3_image_x1 = p3_title_x1 + (row6_title_width//2) - (image_width//2)
            p3_image_y1 = p3_title_y2 + title_to_picture_padding
            shirt(max_def[0],p3_image_x1,p3_image_y1,image_height,image_width)
        else:
            p3_image1_x1 = p3_title_x1 + (row6_title_width//2) - image_width + (image_width//10)
            p3_image1_y1 = p3_title_y2 + title_to_picture_padding
            shirt(max_def[0],p3_image1_x1,p3_image1_y1,image_height,image_width)
            p3_image2_x1 = p3_title_x1 + (row6_title_width//2) - (image_width//10)
            p3_image2_y1 = p3_image1_y1
            shirt(max_def[1],p3_image2_x1,p3_image2_y1,image_height,image_width)
        p3_center_x = p3_title_x1 + (row6_title_width//2) - (image_width//2)
        p3_center_y = p3_title_y2 + title_to_picture_padding
        draw_cat(p3_center_x,p3_center_y,image_height,image_width,cat='DEF')
        
        # Panel 4 (GK)
        p4_title_x1 = p3_title_x1 + row6_title_width + row_padding
        p4_title_y1 = row_top
        p4_title_x2 = p4_title_x1 + row6_title_width
        p4_title_y2 = p4_title_y1 + title_height
        title_box(p4_title_x1,p4_title_y1,p4_title_x2,p4_title_y2,title_radius)
        title_text("Top GK", f"{max(pos_total_points['GK'].values())} Points", p4_title_x1, p4_title_y1, row6_title_width, title_height, color='#c1ff72')
        max_gk = pts_by_positions[0][1]
        if len(max_gk) == 1:
            p4_image_x1 = p4_title_x1 + (row6_title_width//2) - (image_width//2)
            p4_image_y1 = p4_title_y2 + title_to_picture_padding
            shirt(max_gk[0],p4_image_x1,p4_image_y1,image_height,image_width)
        else:
            p4_image1_x1 = p4_title_x1 + (row6_title_width//2) - image_width + (image_width//10)
            p4_image1_y1 = p4_title_y2 + title_to_picture_padding
            shirt(max_gk[0],p4_image1_x1,p4_image1_y1,image_height,image_width)
            p4_image2_x1 = p4_title_x1 + (row6_title_width//2) - (image_width//10)
            p4_image2_y1 = p4_image1_y1
            shirt(max_gk[1],p4_image2_x1,p4_image2_y1,image_height,image_width)
        p4_center_x = p4_title_x1 + (row6_title_width//2) - (image_width//2)
        p4_center_y = p4_title_y2 + title_to_picture_padding
        draw_cat(p4_center_x,p4_center_y,image_height,image_width,cat='GK')
    # Load the template
    template = Image.open("misc/template.png")

    title_to_picture_padding = 5
    row1_height = 350
    title_height = 106
    image_height = 211
    chip_image_height = 115
    chip_textbox_height = 65
    team_textbox_height = 34
    team_textbox_width = 166
    cat_textbox_height = 63
    cat_textbox_width = team_textbox_width

    #Calculate padding
    if any(bool(values) for values in chips.values()):
        padding = (template.size[1] - (row1_height + 4*title_height + 4*image_height + chip_image_height)) / 7
        row1_top = padding
        row2_top = row1_top + row1_height + padding
        row3_top = row2_top + title_height + image_height + padding
        row4_top = row3_top + title_height + image_height + padding
        row5_top = row4_top + title_height + image_height + padding
        row6_top = row5_top + chip_image_height + padding
    else:
        padding = (template.size[1] - (row1_height + 4*title_height + 4*image_height)) / 6
        row1_top = padding
        row2_top = row1_top + row1_height + padding
        row3_top = row2_top + title_height + image_height + padding
        row4_top = row3_top + title_height + image_height + padding
        row6_top = row4_top + title_height + image_height + padding

    draw = ImageDraw.Draw(template)
    draw_row1(row1_top)
    draw_row2(row2_top)
    draw_row3(row3_top)
    draw_row4(row4_top)
    if any(bool(values) for values in chips.values()):
        draw_row5(row5_top)
    draw_row6(row6_top)

    template.save(f"GW{e['id']}_Highlights.png")

# Settings
league_id = '416585'
highlight_keys = {}

# Pull FPL data
league_data = requests.get(f'https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/').json()
fpl_data = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/').json()
e = next(event for event in fpl_data['events'] if event['is_current'])
gw = e['id']
weekly_stats = {}
gw_data = {}
weekly_picks = {}
for manager in league_data['standings']['results']:
    id = manager['entry']
    weekly_stats[id] = requests.get(f'https://fantasy.premierleague.com/api/entry/{id}/history/').json()
    gw_data[id] = requests.get(f'https://fantasy.premierleague.com/api/entry/{id}/event/{gw}/picks/').json()
    weekly_picks[id] = {i: requests.get(f'https://fantasy.premierleague.com/api/entry/{id}/event/{i}/picks/').json()['picks'] for i in range(1,gw+1)}

# Setup datasets
team_name, total_points, rank, rank_chg, value_gain, green_streaks, pos_total_points = {}, {}, {}, {}, {}, {}, {pos: {} for pos in ['GK','DEF','MID','FWD']}
for manager in league_data['standings']['results']:
    id = manager['entry']
    team_name[id] = manager['entry_name']
    total_points[id] = manager['total']
    rank[id] = manager['rank']
    rank_chg[id] = manager['last_rank'] - manager['rank']
    value_gain[id] = (weekly_stats[id]['current'][-1]['value'] - weekly_stats[id]['current'][-2]['value']) / 10
    for pos in pos_total_points:
        pos_total_points[pos][id] = 0

all_gws_players_stats = {i: {player['id']: player['stats'] for player in requests.get(f'https://fantasy.premierleague.com/api/event/{i}/live/').json()['elements']} for i in range(1,gw+1)}
players_stats = {element['id']: element for element in fpl_data['elements']}
selected = {key: 0 for key in all_gws_players_stats[gw].keys()}
captained = {key: 0 for key in all_gws_players_stats[gw].keys()}

gw_points, team_value, hits, bench_pts, best_captained, captains, transfers_gain, subs_pts, itb, correct_gk = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
chips = {chip: [] for chip in ['bboost', 'freehit', 'wildcard', '3xc']}

for id in gw_data:
    gw_points[id] = gw_data[id]['entry_history']['points']
    team_value[id] = gw_data[id]['entry_history']['value'] / 10
    if gw_data[id]['entry_history']['event_transfers_cost'] > 0:
         hits[id] = gw_data[id]['entry_history']['event_transfers_cost']
    if gw_data[id]['entry_history']['points_on_bench'] != 0:
        bench_pts[id] = gw_data[id]['entry_history']['points_on_bench']
    itb[id] = gw_data[id]['entry_history']['bank'] / 10
    if gw_data[id]['active_chip'] is not None:
        chips[gw_data[id]['active_chip']].append(id)
    for p in gw_data[id]['picks']:
        selected[p['element']] += 1
        if p['is_captain'] is True:
            captained[p['element']] += 1
        if p['multiplier'] > 1:
            captains[id] = p['element']
            best_captained[id] = players_stats[p['element']]['event_points'] * p['multiplier']
    for i in range(gw-1,0,-1):
        if weekly_stats[id]['current'][i]['overall_rank'] < weekly_stats[id]['current'][i-1]['overall_rank']:
            green_streaks[id] = green_streaks[id] + 1 if id in green_streaks.keys() else 1
        else:
            break
    if gw_data[id]['entry_history']['event_transfers'] > 0:
            this_picks = [player['element'] for player in gw_data[id]['picks']]
            prev_json = requests.get(f'https://fantasy.premierleague.com/api/entry/{id}/event/{gw-1}/picks/').json()
            if prev_json['active_chip'] != 'freehit':
                last_picks = [player['element'] for player in prev_json['picks']]
            else:
                last_picks = [player['element'] for player in requests.get(f'https://fantasy.premierleague.com/api/entry/{id}/event/{gw-2}/picks/').json()['picks']]
            transfers_gain[id] = sum(players_stats[value]['event_points'] for value in list(set(this_picks) - set(last_picks))) - sum(players_stats[value]['event_points'] for value in list(set(last_picks) - set(this_picks))) - gw_data[id]['entry_history']['event_transfers_cost']
    if len(gw_data[id]['automatic_subs']) > 0:
        subs_pts[id] = sum(players_stats[value]['event_points'] for value in [sub['element_in'] for sub in gw_data[id]['automatic_subs']])
    gk_count = 0
    for week in range(1,gw+1):
        if all_gws_players_stats[week][weekly_picks[id][week][0]['element']]['total_points'] >= all_gws_players_stats[week][weekly_picks[id][week][11]['element']]['total_points']:
            gk_count += 1
        for pick in weekly_picks[id][week]:
            if pick['multiplier'] > 0:
                pos_total_points[element_type_to_pos(players_stats[pick['element']]['element_type'])][id] += all_gws_players_stats[week][pick['element']]['total_points']*pick['multiplier']
    correct_gk[id] = (gk_count/gw)*100
        
# Prepare data for summary
max_gw_pts = [key for key, value in gw_points.items() if value == max(gw_points.values())]
max_team_value = [key for key, value in team_value.items() if value == max(team_value.values())]
min_team_value = [key for key, value in team_value.items() if value == min(team_value.values())]
max_selected = [key for key, value in selected.items() if value == max(selected.values())]
max_captain = [key for key, value in captained.items() if value == max(captained.values())]
max_hits = [key for key, value in hits.items() if value == max(hits.values())]
max_bench_pts = [key for key, value in bench_pts.items() if value == max(bench_pts.values())]
max_greens = [key for key, value in green_streaks.items() if value == max(green_streaks.values())]
max_transfers_gain = [key for key, value in transfers_gain.items() if value == max(transfers_gain.values())]
max_subs_pts = [key for key, value in subs_pts.items() if value == max(subs_pts.values())]
max_itb = [key for key, value in itb.items() if value == max(itb.values())]
max_correct_gk = [key for key, value in correct_gk.items() if value == max(correct_gk.values())]
pts_by_positions = [(pos, [key for key, value in pos_total_points[pos].items() if value == max(pos_total_points[pos].values())]) for pos in ['GK','DEF','MID','FWD']]
max_bst_cptn = [key for key, value in best_captained.items() if value == max(best_captained.values())]
bst_cptn_ids = list(set([captains[id] for id in max_bst_cptn]))

league_summary = ""
league_summary += f"** {league_data['league']['name']} GW {gw}:\n"
league_summary += "Standings: " + ' '.join([f"({item['rank']}) {get_team_name(item['entry'])}" for item in league_data['standings']['results'][0:3]]) + "\n------------------------------\n"
if max(gw_points.values()) > 0:
    league_summary += "Most Points: " + ' & '.join(list(map(get_team_name, max_gw_pts))) + " (" + str(gw_points[max(gw_points, key=gw_points.get)]) + " Points, Overall GW Rank: " + format(gw_data[max(gw_points, key=gw_points.get)]['entry_history']['rank'],',d') + ")\n"
league_summary += "Most Selected: " + ' & '.join(list(map(get_player_webname, max_selected))) + " (" + str(selected[max(selected, key=selected.get)]) + " Teams)" + "\n"
league_summary += "Captained Best: " + ' & '.join(list(map(get_team_name, max_bst_cptn))) + " (" + ' & '.join(list(map(get_player_webname, bst_cptn_ids))) + ", " + str(max(best_captained.values())) + " Points)" + "\n"
league_summary += "Most Captained: " + ' & '.join(list(map(get_player_webname, max_captain))) + " (" + str(captained[max(captained, key=captained.get)]) + " Teams)" + "\n------------------------------\n"
league_summary += "Highest Team Value: " + ' & '.join(list(map(get_team_name, max_team_value))) + " (" + str(team_value[max(team_value, key=team_value.get)]) + "M £)" + "\n"
league_summary += "Lowest Team Value: " + ' & '.join(list(map(get_team_name, min_team_value))) + " (" + str(team_value[min(team_value, key=team_value.get)]) + "M £)" + "\n"
league_summary += "Going Up: " + ' & '.join(list(map(get_team_name, max_greens))) + " (" + str(green_streaks[max(green_streaks, key=green_streaks.get)]) + " Greens)" + "\n"
league_summary += "Highest Money in the Bank: " + ' & '.join(list(map(get_team_name, max_itb))) + " (" + str(itb[max(itb, key=itb.get)]) + "M £)" + "\n"
if len(max_hits) > 0:
    league_summary += "Most Hits: " + ' & '.join(list(map(get_team_name, max_hits))) + " (-" + str(hits[max(hits, key=hits.get)]) + " Points" + ")\n------------------------------\n"
else:
    league_summary += "Most Hits: None\n------------------------------\n"
if len(max_subs_pts) > 0:
    league_summary += "Highest Substitutes Points: " + ' & '.join(list(map(get_team_name, max_subs_pts))) + " (" + str(subs_pts[max(subs_pts, key=subs_pts.get)]) + " Points)" + "\n"
if max(bench_pts.values()) > 0:
    league_summary += "Most Points on Bench: " + ' & '.join(list(map(get_team_name, max_bench_pts))) + " (" + str(bench_pts[max(bench_pts, key=bench_pts.get)]) + " Points" + ")\n"
if len(max_transfers_gain) > 0:
    league_summary += "Highest Transfers Gain: " + ' & '.join(list(map(get_team_name, max_transfers_gain))) + " (" + str(transfers_gain[max(transfers_gain, key=transfers_gain.get)]) + " Points)" + "\n"
league_summary += "Correct GK: " + ' & '.join(list(map(get_team_name, max_correct_gk))) + " (" + str(round(correct_gk[max(correct_gk, key=correct_gk.get)],2)) + "%)" + "\n------------------------------\n"
for chip in chips:
    if len(chips[chip]) > 0:
        league_summary += f"{get_chip_name(chip)} Used: " + ' & '.join(list(map(get_team_name, chips[chip]))) + "\n"
league_summary += "------------------------------\n"
league_summary += "".join(f"Most {pos} Points: " + ' & '.join(list(map(get_team_name, max_points))) + f" ({str(pos_total_points[pos][max(pos_total_points[pos], key=pos_total_points[pos].get)])} Points)\n" for pos, max_points in pts_by_positions)
print(league_summary)

# Graphics
dict_list = [total_points, gw_points, team_value, hits, bench_pts, best_captained, green_streaks, transfers_gain, subs_pts, itb, correct_gk, pos_total_points['GK'], pos_total_points['DEF'], pos_total_points['MID'], pos_total_points['FWD']]
dict_list_sorted = [dict(sorted(d.items(), key=lambda item: item[1], reverse=False)) for d in dict_list]
dict_list_sorted[0] = {key: total_points[key] for key in sorted(rank, key=lambda x: (rank[x], x), reverse=True)}
titles = [
    "Total Points", "Gameweek Points", "Team Value", "Hits Taken", "Bench Points", 
    "Captain Points", "Green Streaks", "Transfers Gain", "Substitution Points", "In The Bank", 
    "Correct Goalkeeper", "Goalkeeper Total Points", "Defender Total Points", "Midfielder Total Points", "Forward Total Points"
]
# Total Points
tp_lower = math.ceil((min(total_points.values())-200) / 100) * 100
# Team Value
tv_lower = math.ceil(min(team_value.values())-4)
# Position Points
gk_lower = math.ceil((min(pos_total_points['GK'].values())-10) / 10) * 10
def_lower = math.ceil((min(pos_total_points['DEF'].values())-10) / 10) * 10
mid_lower = math.ceil((min(pos_total_points['MID'].values())-10) / 10) * 10
fwd_lower = math.ceil((min(pos_total_points['FWD'].values())-10) / 10) * 10
fig, axes = plt.subplots(nrows=3, ncols=5, figsize=(22, 13.2))
axes = axes.flatten()
for i, (ax, data_dict) in enumerate(zip(axes, dict_list_sorted)):
    if not data_dict:
        ax.set_title(titles[i])
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        continue
    keys = [get_team_name(key) for key in data_dict.keys()]
    values = list(data_dict.values())
    colors = [highlight_keys[key] if key in highlight_keys else 'skyblue' for key in data_dict.keys()]
    bars = ax.barh(keys, values, color=colors)  
    ax.set_title(titles[i])
    max_value = max(values)
    min_value = min(values)
    label_length_factor = 0.02
    for bar in bars:
        width = bar.get_width()
        if width != 0:
            if i+1==1:
                key_id = list(data_dict.keys())[bars.index(bar)]
                player_rank = rank.get(key_id, 0)
                player_chg = rank_chg.get(key_id, 0)
                bar_label = f'Rank: {player_rank} (+{player_chg})' if player_chg > 0 else f'Rank: {player_rank} ({player_chg})' if player_chg != 0 else f'Rank: {player_rank}'
                ax.text(tp_lower/2+width/2, bar.get_y() + bar.get_height()/2, bar_label, 
                        va='center', ha='center' if width > 0 else 'right', color='black', fontsize=10) 
                ax.text(width, bar.get_y() + bar.get_height()/2, f'{width}', 
                    va='center', ha='left' if width > 0 else 'right', color='black', fontsize=10) 
            elif i+1==3:
                key_id = list(data_dict.keys())[bars.index(bar)]
                value = team_value.get(key_id, 0)
                value_change = value_gain.get(key_id, 0)
                bar_value = f'{value} (+{value_change})' if value_change > 0 else f'{value} ({value_change})' if value_change != 0 else f'{value}'
                ax.text(tv_lower/2+width/2, bar.get_y() + bar.get_height()/2, bar_value, 
                        va='center', ha='center' if width > 0 else 'right', color='black', fontsize=10) 
            elif i+1==4:
                ax.text(width, bar.get_y() + bar.get_height()/2, f'-{width}', 
                    va='center', ha='left' if width > 0 else 'right', color='black', fontsize=10)
            elif i+1==11:
                ax.text(width/2, bar.get_y() + bar.get_height()/2, f'{width:.2f}%', 
                    va='center', ha='center' if width > 0 else 'right', color='black', fontsize=10)
            else:
                ax.text(width, bar.get_y() + bar.get_height()/2, f'{width}', 
                    va='center', ha='left' if width > 0 else 'right', color='black', fontsize=10) 
        else:
            if min_value < 0:
                ax.text(width, bar.get_y() + bar.get_height()/2, f'{width}', 
                    va='center', ha='left' if width > 0 else 'right', color='black', fontsize=10) 
    if i+1==4:
        x_ticks = ax.get_xticks()
        ax.set_xticklabels([f'-{int(tick)}' if tick != 0 else '0' for tick in x_ticks])
    if i+1 in [5,6,7,8,9]:
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if i+1==1:
        buffer = (max_value-tp_lower) * 0.05 + label_length_factor * len(str(max_value)) * (max_value-tp_lower)
        ax.set_xlim(tp_lower, max_value+buffer)
    elif i+1==3:
        ax.set_xlim(tv_lower, 0.05*(max_value-min_value) + max_value)
    elif i+1 in [5,6,8]:
        max_buffer = (max_value-min_value) * 0.05 + label_length_factor * len(str(max_value)) * (max_value-min_value)
        min_buffer = (min_value-max_value) * 0.05 + label_length_factor * len(str(min_value)) * (min_value-max_value)
        if min_value < 0:
            ax.set_xlim(min_value+min_buffer, max_value+max_buffer)
        else:
            ax.set_xlim(0, max_value+max_buffer)
    elif i+1==9:
        if min_value < 0:
            max_buffer = (max_value-min_value) * 0.05 + label_length_factor * len(str(max_value)) * (max_value-min_value)
            min_buffer = (min_value-max_value) * 0.05 + label_length_factor * len(str(min_value)) * (min_value-max_value)
            ax.set_xlim(min_value+min_buffer, max_value+max_buffer)
        else:
            buffer = max_value * 0.05 + label_length_factor * len(str(max_value)) * max_value
            ax.set_xlim(0, max_value + buffer)
    elif i+1==11:
        ax.set_xlim(0, 105)
        ax.set_xticks([0, 20, 40, 60, 80, 100])
        ax.set_xticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])
    elif i+1==12:
        buffer = (max_value-gk_lower) * 0.05 + label_length_factor * len(str(max_value)) * (max_value-gk_lower)
        ax.set_xlim(gk_lower, max_value+buffer)
    elif i+1==13:
        buffer = (max_value-def_lower) * 0.05 + label_length_factor * len(str(max_value)) * (max_value-def_lower)
        ax.set_xlim(def_lower, max_value+buffer)
    elif i+1==14:
        buffer = (max_value-mid_lower) * 0.05 + label_length_factor * len(str(max_value)) * (max_value-mid_lower)
        ax.set_xlim(mid_lower, max_value+buffer)
    elif i+1==15:
        buffer = (max_value-fwd_lower) * 0.05 + label_length_factor * len(str(max_value)) * (max_value-fwd_lower)
        ax.set_xlim(fwd_lower, max_value+buffer)
    else:
        buffer = max_value * 0.05 + label_length_factor * len(str(max_value)) * max_value
        ax.set_xlim(0, max_value + buffer)
for j in range(len(dict_list_sorted), len(axes)):
    fig.delaxes(axes[j])
plt.suptitle(f"{league_data['league']['name']} - Gameweek {gw}", fontsize=24)
plt.tight_layout()
plt.savefig(f"GW{gw}.png", format="png", bbox_inches="tight")
