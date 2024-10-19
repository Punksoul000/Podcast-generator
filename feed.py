import yaml
import xml.etree.ElementTree as xml_tree

with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

    rss_element = xml_tree.Element(
        'rss',
        {
            'version': '2.0',
            'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
            'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
        }
    )

    channel_element = xml_tree.SubElement(rss_element, 'channel')

    # Use get to avoid KeyError and provide defaults if needed
    link_prefix = yaml_data.get('link', 'https://default-link.com/')

    xml_tree.SubElement(channel_element, 'title').text = yaml_data.get('title', 'Default Title')
    xml_tree.SubElement(channel_element, 'format').text = yaml_data.get('format', 'audio/mpeg')
    xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data.get('subtitle', 'Default Subtitle')
    xml_tree.SubElement(channel_element, '{http://www.itunes.com/dtds/podcast-1.0.dtd}author').text = yaml_data.get('itunes:author', 'Unknown Author')
    xml_tree.SubElement(channel_element, 'description').text = yaml_data.get('description', 'No Description')
    
    # Fix the image element to not set text
    xml_tree.SubElement(channel_element, '{http://www.itunes.com/dtds/podcast-1.0.dtd}image', {'href': link_prefix + yaml_data.get('image', 'default-image.jpg')})
    
    xml_tree.SubElement(channel_element, 'language').text = yaml_data.get('language', 'en')
    xml_tree.SubElement(channel_element, 'link').text = link_prefix
    xml_tree.SubElement(channel_element, '{http://www.itunes.com/dtds/podcast-1.0.dtd}category', {'text': yaml_data.get('category', 'General')})

    # Use get to avoid KeyError and provide default for items
    items = yaml_data.get('items', [])
    
    for item in items:
        item_element = xml_tree.SubElement(channel_element, 'item')
        xml_tree.SubElement(item_element, 'title').text = item.get('title', 'Untitled Episode')
        xml_tree.SubElement(item_element, '{http://www.itunes.com/dtds/podcast-1.0.dtd}author').text = yaml_data.get('itunes:author', 'Unknown Author')
        xml_tree.SubElement(item_element, 'description').text = item.get('description', 'No Description')
        xml_tree.SubElement(item_element, '{http://www.itunes.com/dtds/podcast-1.0.dtd}duration').text = item.get('itunes:duration', '0:00')
        xml_tree.SubElement(item_element, 'pubDate').text = item.get('published', 'Mon, 01 Jan 2000 00:00:00 GMT')

        enclosure = xml_tree.SubElement(item_element, 'enclosure', {
            'url': link_prefix + str(item.get('file', '')),
            'type': item.get('file_type', 'audio/mpeg'),
            'length': str(item.get('file_size', 0))
        })

    output_tree = xml_tree.ElementTree(rss_element)
    output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)

    
    
