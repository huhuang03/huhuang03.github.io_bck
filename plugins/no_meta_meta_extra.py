from nikola.plugin_categories import MetadataExtractor
from nikola.metadata_extractors import MetaCondition
from nikola.metadata_extractors import MetaPriority
from nikola.metadata_extractors import MetaSource
from pathlib import Path
import os
import time
from datetime import datetime
import dateutil.tz


class NoMetaMetadata(MetadataExtractor):
    name = "NoMeta"
    source = MetaSource.filename
    priority = MetaPriority.fallback
    requirements = []

    conditions = [(MetaCondition.config_present, "TH_USE_NO_META_META_EXTRA")]

    def __getNikolaTime(self, ctime):
        time = datetime.fromtimestamp(ctime)
        tz = dateutil.tz.tzlocal()
        offset = tz.utcoffset(time)
        offset_sec = (offset.days * 24 * 3600 + offset.seconds)
        offset_hrs = offset_sec // 3600
        offset_min = offset_sec % 3600
        tz_str = '{0:+03d}:{1:02d}'.format(offset_hrs, offset_min // 60)
        if offset:
            tz_str = ' UTC{0:+03d}:{1:02d}'.format(offset_hrs, offset_min // 60)
        else:
            tz_str = ' UTC'
        return time.strftime('%Y-%m-%d %H:%M:%S') + tz_str



    def _extract_metadata_from_text(self, source_text: str) -> 'typing.Dict[str, str]':
        print("_extract_metadata_from_text called")

    def split_metadata_from_text(self, source_text: str) -> (str, str):
        """Split text into metadata and content (both strings)."""
        print("split_meta_from_text called")
        if self.split_metadata_re is None:
            return source_text
        else:
            split_result = self.split_metadata_re.split(source_text.lstrip(), maxsplit=1)
            if len(split_result) == 1:
                return split_result[0], split_result[0]
            else:
                # Necessary?
                return split_result[0], split_result[-1]

    def extract_filename(self, filename: str, lang: str) -> 'typing.Dict[str, str]':
        """Extract metadata from filename."""
        meta = {}
        meta['date'] = self.__getNikolaTime(os.path.getctime(filename))
        return meta
