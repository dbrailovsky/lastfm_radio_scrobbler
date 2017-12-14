#!/usr/bin/python
'''
Copyright (C) 2016 Dendrion <deendrion@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import json
import pylast

import re, time, datetime, sys
import urllib2
import argparse

import Tkinter

from os.path import expanduser

# Globals
home = expanduser("~")
path_to_config = home + "/.lastfm_scrobbler/lastfm.json"
root = Tkinter.Tk()
textbox = None
btn = None
swing_url = 'http://109.123.114.172:7115/live'
jazz_url = 'http://radio.jazz.moscow:8000'
#stream_url ='http://listen.radionomy.com/OnlyJazz'
stream_url = swing_url # default

work_mode_cont = "continuously"
work_mode_one = "one_track"

work_mode = work_mode_one



def get_artist_track(stream_url):
    d = dict()
    request = urllib2.Request(stream_url)
    request.add_header('Icy-MetaData', 1)
    response = urllib2.urlopen(request)
    icy_metaint_header = response.headers.get('icy-metaint')

    if icy_metaint_header is not None:
        metaint = int(icy_metaint_header)
        read_buffer = metaint + 255
        content = response.read(read_buffer)
        data = str(content[metaint:])
        #print(data)
        p = re.compile(r'StreamTitle=(?P<track>[^;]+)')
        s = re.search(p, data)
        if (s):
            d = s.groupdict()
        else:
            d = None
    return d



def scrobble(artist, title):
    global path_to_config
    app_info = json.loads(open(path_to_config, 'r').read())
    timestamp = datetime.datetime.now()

    network = pylast.LastFMNetwork(api_key = app_info['api_key'], api_secret =app_info['shared_secret'],
                                   username=app_info['user_name'], password_hash=app_info['password'])
    network.scrobble(artist, title,timestamp)
    '''for art in user.get_library().get_artists():
        print art.get_top_tracks()

    for tr in user.get_loved_tracks():
        print tr.track'''



def do_work(ev):
    a = 0
    stream_url = textbox.get(1.0, Tkinter.END)
    if 'jazz' in stream_url:
        stream_url = 'http://radio.jazz.moscow:8000'
    print "Stream: " + stream_url

    # Scrobble continuously
    if ( work_mode == work_mode_cont):
        track_old = None
        while (a == 0):
            track = get_artist_track(stream_url)
            if (track):
                tr = str(track["track"])
                tr = tr.replace("'", "")
                tr_info = tr.split(" - ")
                if (len(tr_info) < 2):
                    tr_info = ["Unknown", tr]

                if (track_old == track):
                    pass
                else:
                    print tr_info
                    scrobble(tr_info[0], tr_info[1])
                    track_old = track
                time.sleep(1)
    # Scrobble only one track
    else:
        track = get_artist_track(stream_url)
        if (track):
            tr = str(track["track"])
            tr = tr.replace("'", "")
            tr_info = tr.split(" - ")
            if (len(tr_info) < 2):
                tr_info = ["Unknown", tr]
            else:
                print tr_info
                scrobble(tr_info[0], tr_info[1])
            time.sleep(1)



def start_gui():
    global root, textbox, btn

    btn = Tkinter.Button(root,
                 text= "Scroble" ,
                 width=30,height=5,
                 fg="black")

    textbox = Tkinter.Text(root, font='Arial 12')
    textbox.insert(1.0, stream_url)
    btn.bind("<Button-1>", do_work)
    btn.pack()
    textbox.pack()
    root.mainloop()

# parse args
parser = argparse.ArgumentParser(description='Scrobble radio to lastfm.')
parser.add_argument('name',  nargs='?',
                   help='an integer as number of radio')
args = parser.parse_args()
if( not (args.name == None)):
    stream_url = args.name

# Start
start_gui()


