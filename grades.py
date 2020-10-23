from discord.ext import commands

french = ['2-3', '3-4', '4', '4+', '5a', '5b', '6a', '6a+', '6b', '6b+', '6c', '6c+', '7a', '7a+', '7b', '7b+', '7c', '7c+', '8a', '8a+', '8b', '8b+', '8c', '8c+', '9a', '9a+', '9b', '9b+', '9c']
uk = ['HVD', 'MS', 'S', 'VS', 'HVS', 'E1 5a/HVS 5b', 'E1 5b', 'E2 5c', 'E3 5c/6a', 'E3 6a', 'E4 6a', 'E4 6b/E5 6a', 'E5 6b', 'E5 6c/E6 6b', 'E6 6b', 'E6 6b/6c', 'E6 6c/E7 6c', 'E7 7a', 'E7 7a/E8 6c', 'E8 6c', 'E8 7a/E9 7a', 'E9 7b/E10 7a', 'E10 7a', 'E10 7b', 'E10 7c/E11 7a', 'E11 7b', 'fuck off mate', 'get out u fuckin nonce', 'oi you got a loicense for that grade?']
yds = ['5.2-3', '5.4-5', '5.6', '5.7', '5.8', '5.9', '5.10a', '5.10b', '5.10c', '5.10d', '5.11a', '5.11b', '5.11c/d', '5.12a', '5.12b', '5.12c', '5.12d', '5.13a', '5.13b', '5.13c', '5.13d', '5.14a', '5.14b', '5.14c', '5.14d', '5.15a', '5.15b', '5.15c', '5.15d']
hueco = ['VB', 'VB', 'VB', 'VB', 'VB', 'V0-', 'V0', 'V0+', 'V1', 'V2', 'V3', '', 'V4', '', 'V5', '', 'V6', 'V7', 'V8', '', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17']
font = ['3', '3', '3', '3', '3', '4-', '4', '4+', '5', '5+', '6A', '6A+', '6B', '6B+', '6C', '6C+', '7A', '7A+', '7B', '7B+', '7C', '7C+', '8A', '8A+', '8B', '8B+', '8C', '8C+', '9A']

def convert_grade(source, destination, grade):
    source_scale = get_scales(source)
    dest_scale = get_scales(destination)

    if grade in source_scale:
        original = source_scale.index(grade)
        return dest_scale[original]
    else:
        raise ValueException('Not a valid scale')

def get_scales(system):
    return {
        'french':french,
        'sport':french,
        'french sport':french,
        'fr':french,
        'france':french,
        'eu':french,
        'euro':french,
        'francia':french,
        'uk':uk,
        'british':uk,
        'british tech':uk,
        'brit tech':uk,
        'british trad':uk,
        'gb':uk,
        'uk tech':uk,
        'yds':yds,
        'yosemite':yds,
        'us':yds,
        'hueco':hueco,
        'v':hueco,
        'vermin':hueco,
        'font':font,
        'fontainebleau':font
    }[system]