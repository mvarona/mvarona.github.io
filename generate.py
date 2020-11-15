import json
import os
import shutil
import re
from pathlib import Path

STATIC_FOLDERS = ['css', 'images', 'js']
COMPONENTS_FOLDER_NAME = 'components'
COMPONENTS_HTML_FOLDER_NAME = 'html'
WEB_FOLDER_NAME = 'web'
WEB_JSON_FILE_NAME = 'web.json'

def create_folders_for_lans(lans):
	for lan in lans:
		dir = WEB_FOLDER_NAME + os.path.sep + lan
		if os.path.exists(dir):
			shutil.rmtree(dir)
		os.makedirs(dir)
		for folder in STATIC_FOLDERS:
			try:
				shutil.copytree(COMPONENTS_FOLDER_NAME + os.path.sep + folder, WEB_FOLDER_NAME + os.path.sep + folder) 
			except OSError as err:
				if err.errno != 17:
					print("Error:", e)

def populate_independent_vars(file, json_file, lan):
	for var in json_file:
		regex_base_var = ''
		if var.endswith('_' + lan):
			base_var = var[:-(len(lan)+1)]
			regex_base_var = '$' + base_var
		else:
			regex_base_var = '$' + var

		with open(file, 'r+') as f:
			file_content = f.read()

			if not isinstance(regex_base_var, list) and regex_base_var in file_content:
				file_content = file_content.replace(str(regex_base_var), json_file[var])
				file_content = file_content.replace('$lan', lan)
				f.seek(0)
				f.write(file_content)
				f.close()

def make_url_friendly(name):
	url = name.replace("Á", "a").replace("á", "a").replace("ä", "a").replace("Ä", "a")
	url = name.replace("É", "e").replace("é", "e").replace("ë", "e").replace("Ë", "e")
	url = name.replace("Í", "i").replace("í", "i").replace("ï", "i").replace("Ï", "i")
	url = name.replace("Ó", "o").replace("ó", "o").replace("ö", "o").replace("Ö", "o")
	url = name.replace("Ú", "u").replace("ú", "u").replace("ü", "u").replace("Ü", "u")
	url = url.lower()
	return url

def populate_header(file, json_file, active_lan):
	(filename, ext) = os.path.splitext(file.split(os.path.sep)[-1])
	with open(file, 'r+') as f:
		file_content = f.read()

		regex_lans = '{$list_lans}'
		regex_dropdown_sections = '{$dropdown_sections}'
		regex_menu_sections = '{$menu_sections}'

		if regex_lans in file_content:
			component_path = COMPONENTS_FOLDER_NAME + os.path.sep + COMPONENTS_HTML_FOLDER_NAME + os.path.sep + 'nav_lan.html'
			component_new_content = ''
			for lan_json in json_file['lans']:
				with open(component_path, 'r+') as c:
					component_content = c.read()
					component_content = component_content.replace('$lan', lan_json)
					component_content = component_content.replace('$filename', filename)

					if lan_json == active_lan:
						component_content = component_content.replace('$active', 'active')
					else:
						component_content = component_content.replace('$active', '')

					component_new_content = component_new_content + component_content

			file_content = file_content.replace(regex_lans, component_new_content)
			f.seek(0)
			f.write(file_content)
			c.close()

		if regex_dropdown_sections in file_content:
			component_path = COMPONENTS_FOLDER_NAME + os.path.sep + COMPONENTS_HTML_FOLDER_NAME + os.path.sep + 'dropdown_section.html'
			component_new_content = ''
			for section_json in json_file['sections']:
				name_section = section_json["title_" + active_lan]
				with open(component_path, 'r+') as c:
					component_content = c.read()
					component_content = component_content.replace('$section', name_section)
					section_path = make_url_friendly(name_section)
					component_content = component_content.replace('$path_section', section_path)

					if name_section in filename:
						component_content = component_content.replace('$active', 'active')
					else:
						component_content = component_content.replace('$active', '')

					component_new_content = component_new_content + component_content

			file_content = file_content.replace(regex_dropdown_sections, component_new_content)
			f.seek(0)
			f.write(file_content)
			c.close()

		if regex_menu_sections in file_content:
			component_path = COMPONENTS_FOLDER_NAME + os.path.sep + COMPONENTS_HTML_FOLDER_NAME + os.path.sep + 'menu_section.html'
			component_new_content = ''
			for section_json in json_file['sections']:
				name_section = section_json["title_" + active_lan]
				img_section = "../" + section_json["img"]
				alt_img_section = section_json["alt_" + active_lan]
				with open(component_path, 'r+') as c:
					component_content = c.read()
					component_content = component_content.replace('$section', name_section)
					section_path = make_url_friendly(name_section)
					component_content = component_content.replace('$path_section', section_path)
					component_content = component_content.replace('$img_section', img_section)
					component_content = component_content.replace('$alt_img_section', alt_img_section)

					if name_section in filename:
						component_content = component_content.replace('$active', 'active')
					else:
						component_content = component_content.replace('$active', '')

					component_new_content = component_new_content + component_content

			file_content = file_content.replace(regex_menu_sections, component_new_content)
			f.seek(0)
			f.write(file_content)
			c.close()

	f.close()

def populate_section(file, json_file, active_lan, active_section):
	(filename, ext) = os.path.splitext(file.split(os.path.sep)[-1])
	with open(file, 'r+') as f:
		file_content = f.read()

		file_content = file_content.replace('$section', active_section['title_' + active_lan])
		f.seek(0)
		f.write(file_content)

		file_content = file_content.replace('$alt_img_section', active_section['alt_' + active_lan])
		f.seek(0)
		f.write(file_content)

		file_content = file_content.replace('$img_section', '../' + active_section['img'])
		f.seek(0)
		f.write(file_content)

		file_content = file_content.replace('$quote_section', active_section['quote_' + active_lan])
		f.seek(0)
		f.write(file_content)

		file_content = file_content.replace('$author_section', active_section['quote_author_' + active_lan])
		f.seek(0)
		f.write(file_content)

		regex_menu_subsections = '{$menu_subsections}'

		if regex_menu_subsections in file_content:
			component_path = COMPONENTS_FOLDER_NAME + os.path.sep + COMPONENTS_HTML_FOLDER_NAME + os.path.sep + 'menu_section.html'
			component_new_content = ''

			if 'subsections' in active_section:
				for subsection_json in active_section['subsections']:
					name_subsection = subsection_json["title_" + active_lan]
					img_subsection = "../" + subsection_json["img"]
					alt_img_subsection = subsection_json["alt_" + active_lan]
					with open(component_path, 'r+') as c:
						component_content = c.read()
						component_content = component_content.replace('$section', name_subsection)
						subsection_path = make_url_friendly(name_subsection)
						component_content = component_content.replace('$path_section', subsection_path)
						component_content = component_content.replace('$img_section', img_subsection)
						component_content = component_content.replace('$alt_img_section', alt_img_subsection)

						if name_subsection in filename:
							component_content = component_content.replace('$active', 'active')
						else:
							component_content = component_content.replace('$active', '')

						component_new_content = component_new_content + component_content

				file_content = file_content.replace(regex_menu_subsections, component_new_content)
				f.seek(0)
				f.write(file_content)
				c.close()
			else:
				file_content = file_content.replace(regex_menu_subsections, "")
				f.seek(0)
				f.write(file_content)

	f.close()

def populate_subsection(file, json_file, active_lan, active_subsection):
	(filename, ext) = os.path.splitext(file.split(os.path.sep)[-1])
	with open(file, 'r+') as f:
		file_content = f.read()
		link_component_path = COMPONENTS_FOLDER_NAME + os.path.sep + COMPONENTS_HTML_FOLDER_NAME + os.path.sep + 'subsection_links.html'
		gallery_component_path = COMPONENTS_FOLDER_NAME + os.path.sep + COMPONENTS_HTML_FOLDER_NAME + os.path.sep + 'subsection_gallery.html'
		gallery_carousel_component_path = COMPONENTS_FOLDER_NAME + os.path.sep + COMPONENTS_HTML_FOLDER_NAME + os.path.sep + 'subsection_gallery_carousel.html'

		file_content = file_content.replace('$subsection_title', active_subsection['title_' + active_lan])
		f.seek(0)
		f.write(file_content)

		file_content = file_content.replace('$alt_img_subsection', active_subsection['alt_' + active_lan])
		f.seek(0)
		f.write(file_content)

		file_content = file_content.replace('$img_subsection', '../../' + active_subsection['img'])
		f.seek(0)
		f.write(file_content)

		file_content = file_content.replace('$subsection_body', active_subsection['body_' + active_lan])
		f.seek(0)
		f.write(file_content)

		links_component = ''

		if 'link1' in active_subsection:

			with open(link_component_path, 'r+') as link:
				links_component = link.read()
				link.close()

			links_component = links_component.replace('$subsection_link_1', active_subsection['link1'])
			links_component = links_component.replace('$subsection_link_text_1', active_subsection['text_link1_' + active_lan])
			links_component = links_component.replace('$hidden2', 'display-none')
			links_component = links_component.replace('$hidden3', 'display-none')

		if 'link2' in active_subsection:
			links_component = links_component.replace('$subsection_link_2', active_subsection['link2'])
			links_component = links_component.replace('$subsection_link_text_2', active_subsection['text_link2_' + active_lan])
			links_component = links_component.replace('$hidden2', '')
			links_component = links_component.replace('$hidden3', 'display-none')

		if 'link3' in active_subsection:
			links_component = links_component.replace('$subsection_link_3', active_subsection['link3'])
			links_component = links_component.replace('$subsection_link_text_3', active_subsection['text_link3_' + active_lan])
			links_component = links_component.replace('$hidden3', 'display-none')
			

		file_content = file_content.replace('{subsection_links}', links_component)
		f.seek(0)
		f.write(file_content)

	f.close()
				

def create_index_for_lans(lans, json_file):
	for lan in lans:
		index_path = WEB_FOLDER_NAME + os.path.sep + lan + os.path.sep + 'index.html'
		shutil.copy(COMPONENTS_FOLDER_NAME + os.path.sep + COMPONENTS_HTML_FOLDER_NAME + os.path.sep + 'index.html', index_path)
		populate_independent_vars(index_path, json_file, lan)
		populate_header(index_path, json_file, lan)

def create_sections_for_lans(lans, json_file):
	for lan in lans:
		for section in json_file['sections']:
			section_filename = section['title_' + lan].lower()
			section_path = WEB_FOLDER_NAME + os.path.sep + lan + os.path.sep + section_filename + '.html'
			shutil.copy(COMPONENTS_FOLDER_NAME + os.path.sep + COMPONENTS_HTML_FOLDER_NAME + os.path.sep + 'section.html', section_path)
			populate_independent_vars(section_path, json_file, lan)
			populate_header(section_path, json_file, lan)
			populate_section(section_path, json_file, lan, section)
			create_sub_sections_for_lans_and_section(lans, json_file, section, lan)

def create_sub_sections_for_lans_and_section(lans, json_file, section, lan):
	if 'subsections' in section:
		for subsection in section['subsections']:
			section_filename = section['title_' + lan].lower()
			subsection_filename = subsection['title_' + lan].lower()
			section_dir_path = WEB_FOLDER_NAME + os.path.sep + lan + os.path.sep + section_filename
			subsection_path = WEB_FOLDER_NAME + os.path.sep + lan + os.path.sep + section_filename + os.path.sep + subsection_filename + '.html'
			if not os.path.exists(section_dir_path):
				os.mkdir(section_dir_path)
			shutil.copy(COMPONENTS_FOLDER_NAME + os.path.sep + COMPONENTS_HTML_FOLDER_NAME + os.path.sep + 'subsection.html', subsection_path)
			populate_independent_vars(subsection_path, json_file, lan)
			populate_header(subsection_path, json_file, lan)
			populate_subsection(subsection_path, json_file, lan, subsection)
		
def clean_html_files():
	for file in Path(WEB_FOLDER_NAME).rglob('*.html'):
		with open(str(file.parents[0]) + os.path.sep + str(file.name), 'r+') as f:
			file_content = f.read()
			end_pos = file_content.find("</html>")
			if end_pos != -1:
				file_content = file_content[:(end_pos+len("</html>"))]
				f.seek(0)
				f.write(file_content)
				f.truncate()
				
			f.close()

if __name__=="__main__":
	json_file = json.load(open(WEB_JSON_FILE_NAME, 'r'))
	lans = json_file["lans"]
	create_folders_for_lans(lans)
	create_index_for_lans(lans, json_file)
	create_sections_for_lans(lans, json_file)
	clean_html_files()