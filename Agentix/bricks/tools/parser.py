import re
from agentix import tool


@tool
def parser(opening_tag, ending_tag) -> callable:
    """
    Parses text enclosed between specified opening and ending tags.

    Args:
        opening_tag (str): The opening tag to look for.
        ending_tag (str): The ending tag to look for.

    Returns:
        callable: A function that takes a string and returns a list of parsed segments.
    """
    def parse(text: str):

        segments = text.split(opening_tag)
        results = []
        for segment in segments[1:]:
            end_idx = segment.find(ending_tag)
            if end_idx != -1:
                results.append(segment[:end_idx].strip())
        return results
    return parse


@tool
def xml_parser(tag_name):
    def parse(xml_string):
        from copy import deepcopy
        result = {}
        # Regex to find <tag ...>content</tag>, capturing attributes and content
        tag_pattern = f'<{tag_name}(.*?)>(.*?)</{tag_name}>'
        tags = re.findall(tag_pattern, xml_string, re.DOTALL)

        for attrs, content in tags:
            # Extract all attributes
            attr_dict = dict(re.findall(r'(\w+)="([^"]+)"', attrs))

            foulard = deepcopy(attr_dict)
            for attr_to_dump in ['format', 'name']:
                if attr_to_dump in foulard:
                    del foulard[attr_to_dump]
            attr_dict['kwargs'] = foulard

            # Add content to the attribute dictionary
            attr_dict['content'] = content.strip()

            # Use the 'name' attribute as the key in the result dictionary if it exists
            name = attr_dict.get('name', f'unnamed_{len(result)}')

            # Store the raw XML string
            raw_xml = f'<{tag_name}{attrs}>{content}</{tag_name}>'
            attr_dict['raw'] = raw_xml.strip()

            result[name] = attr_dict
        return result
    return parse
