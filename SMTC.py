"""SMTC.py is a tool to access and operate SMTC data with WinRT on Windows 10.

Returns:
    A JSON data.
    Like: {"album_artist": "", "album_title": "", "album_track_count": 0, "artist": "Foobar", "genres": [], "playback_type": 1, "subtitle": "", "title": "Foobar", "track_number": 0}
    Thumbnail is removed.


"""

import winrt
from winrt.windows import media
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager, GlobalSystemMediaTransportControlsSessionPlaybackInfo as PlaybackInfo, GlobalSystemMediaTransportControlsSession as SMTCSession
from winrt.windows.applicationmodel import AppDisplayInfo, AppInfo
from winrt.windows.foundation import DateTime, TimeSpan, IReference
import asyncio
import json
import datetime

def object2dict(obj: object):
    result = {song_attr: obj.__getattribute__(song_attr) for song_attr in dir(obj) if song_attr[0] != '_'}
    for key, value in result.items():
        if isinstance(value, TimeSpan):
            result[key] = value.duration
        elif isinstance(value, DateTime):
            result[key] = value.universal_time
        elif isinstance(value, IReference):
            result[key] = value.value
    return result

iref2v = lambda x: None if x is None else x.value

async def get_smtc():
    sessions = await MediaManager.request_async()
    current_session: SMTCSession = sessions.get_current_session()

    if current_session:
        properties = await current_session.try_get_media_properties_async()
        media_info = object2dict(properties)
        playback_info = current_session.get_playback_info()
        playback_info = object2dict(playback_info)
        aumid = current_session.source_app_user_model_id
        timeline_info = current_session.get_timeline_properties()
        timeline_info = object2dict(timeline_info)


        print(type(timeline_info['max_seek_time']))

        # playback_info['auto_repeat_mode'] = iref2v(playback_info.get('auto_repeat_mode'))
        #playback_info['controls'] = object2dict(playback_info.get('controls'))
        # playback_info['is_shuffle_active'] = iref2v(playback_info.get('is_shuffle_active'))
        # playback_info['playback_type'] = iref2v(playback_info.get('playback_type'))

        genres = media_info.get('genres')
        media_info['genres'] = genres.get_many(0, genres.size)[1]
        media_info['playback'] = playback_info
        media_info['timeline'] = timeline_info
        media_info.pop("thumbnail")
        media_info.pop("playback_type")
        return media_info

result = asyncio.run(get_smtc())
print(result)