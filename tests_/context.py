import datetime


config = {
    'name':             'The Seminar',
    'database':         './data/database.csv',
    'poster_css':       './data/poster/css/poster.css',
    'dir_abstract':     './data/abstract/',
    'dir_poster':       './data/poster/',
    'dir_slide':        './data/slide/',
    'tba_date':         'TBA date',
    'tba_begin_time':   'TBA begin time',
    'tba_end_time':     'TBA end time',
    'tba_place':        'TBA place',
    'tba_speaker':      'TBA speaker',
    'tba_affiliation':  'TBA affiliation',
    'tba_title':        'TBA title',
    'tba_abstract':     'TBA abstract',
}


absent = {
    'database':         'absent.csv',
    'poster_css':       'absent.css',
    'dir_abstract':     './absent/',
    'dir_poster':       './absent/',
    'dir_slide':        './absent/',
}


with open('./data/abstract/alice.txt') as f:
    abstract_A = f.read()
with open('./data/abstract/bob.txt') as f:
    abstract_B = f.read()
with open('./data/abstract/charlie.txt') as f:
    abstract_C = f.read()


dict_seminar_A = {
    'date':             datetime.date(2019, 1, 1),
    'begin time':       datetime.time(12, 0),
    'end time':         datetime.time(13, 0),
    'place':            '101A',
    'speaker':          'Alice Speaker',
    'affiliation':      'Alabama University',
    'title':            'Apple Effect',
    'abstract file':    'alice.txt',
    'slide file':       'alice.pdf',
    'abstract':         abstract_A,
}


dict_seminar_B = {
    'date':             datetime.date(2019, 2, 2),
    'begin time':       datetime.time(12, 30),
    'end time':         datetime.time(13, 30),
    'place':            '102B',
    'speaker':          'Bob Talker',
    'affiliation':      'Boston University',
    'title':            'Banana Effect',
    'abstract file':    'bob.txt',
    'slide file':       'bob.pdf',
    'abstract':         abstract_B,
}


dict_seminar_C = {
    'date':             datetime.date(2019, 3, 3),
    'begin time':       datetime.time(13, 0),
    'end time':         datetime.time(14, 0),
    'place':            '103B',
    'speaker':          'Charlie Chatter',
    'affiliation':      'Chicago University',
    'title':            'Cherry Effect',
    'abstract file':    'charlie.txt',
    'slide file':       'charlie.pdf',
    'abstract':         abstract_C,
}


dict_seminar_n = {
    'date':             None,
    'begin time':       None,
    'end time':         None,
    'place':            None,
    'speaker':          None,
    'affiliation':      None,
    'title':            None,
    'abstract file':    None,
    'slide file':       None,
    'abstract':         None,
}
