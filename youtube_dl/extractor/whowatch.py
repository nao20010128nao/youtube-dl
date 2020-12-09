# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import ExtractorError


class WhoWatchIE(InfoExtractor):
    _VALID_URL = r'https?://whowatch\.tv/viewer/(?P<id>\d+)/?'

    def _real_extract(self, url):
        video_id = self._match_id(url)

        api_url = 'https://api.whowatch.tv/lives/' + video_id + '/play?referer=https%3A%2F%2Fwhowatch.tv%2F'
        # URL、IDの順で指定する
        live_data = self._download_json(api_url, video_id)

        # デバッグ用: live_dataを表示する
        # self.to_screen(live_data)

        # HLSのURL
        hls_url = live_data.get('hls_url')

        # hls_urlが無ければエラーを投げる
        if not hls_url:
            raise ExtractorError(live_data.get('error_message'), expected=True)

        # とりあえずHLSのフォーマットを検索する
        formats = self._extract_m3u8_formats(
            hls_url, video_id, ext='mp4', entry_protocol='m3u8_native',
            m3u8_id='hls')
        # 並び替える。これによって何も設定しない状態で最高画質をダウンロードするようにする
        self._sort_formats(formats)

        return {
          'id': video_id,
          # 鉤括弧があったので同時に外してしまう
          'title': live_data['share_info']['live_title'][1:-1],
          # フォーマット一覧
          'formats': formats,
          # これは生放送です
          'is_live': True,
        }
