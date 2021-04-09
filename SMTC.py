"""SMTC.py is a CLI program to get global SMTC info for Windows 10 with WinRT.

Returns:
    A JSON data.
    Like: {"album_artist": "", "album_title": "", "album_track_count": 0, "artist": "Foobar", "genres": [], "playback_type": 1, "subtitle": "", "title": "Foobar", "track_number": 0}
    Thumbnail is removed.


"""

from sys import platform
import winrt
from winrt.windows import media
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager, GlobalSystemMediaTransportControlsSessionPlaybackInfo as PlaybackInfo, GlobalSystemMediaTransportControlsSession as SMTCSession
import asyncio
import json

def object2dict(obj: object):
    return {song_attr: obj.__getattribute__(song_attr) for song_attr in dir(obj) if song_attr[0] != '_'}

iref2v = lambda x: x.value

async def get_smtc():
    sessions = await MediaManager.request_async()
    current_session: SMTCSession = sessions.get_current_session()

    if current_session:
        properties = await current_session.try_get_media_properties_async()
        media_info = object2dict(properties)
        playback_info = current_session.get_playback_info()
        playback_info = object2dict(playback_info)

        playback_info['auto_repeat_mode'] = iref2v(playback_info.get('auto_repeat_mode'))
        playback_info['controls'] = object2dict(playback_info.get('controls'))
        playback_info['is_shuffle_active'] = iref2v(playback_info.get('is_shuffle_active'))
        playback_info['playback_type'] = iref2v(playback_info.get('playback_type'))

        genres = media_info.get('genres')
        media_info['genres'] = genres.get_many(0, genres.size)[1]
        media_info['playback'] = playback_info
        media_info.pop("thumbnail")
        media_info.pop("playback_type")
        return media_info

result = asyncio.run(get_smtc())
print(result)