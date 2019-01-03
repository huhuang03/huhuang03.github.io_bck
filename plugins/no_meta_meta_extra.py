from nikola.plugin_categories import MetadataExtractor
from nikola.metadata_extractors import MetaCondition
from nikola.metadata_extractors import MetaPriority
from nikola.metadata_extractors import MetaSource
from pathlib import Path
import os
import time
from datetime import datetime
import dateutil.tz
import io


class NoMetaMetadata(MetadataExtractor):
    name = "NoMeta"
    source = MetaSource.filename
    priority = MetaPriority.fallback
    requirements = []

    conditions = [(MetaCondition.config_present, "TH_USE_NO_META_META_EXTRA")]

    def _getNikolaTime(self, ctime):
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

    def _lookup_cate_table(self, origin):
        cate_name_map = self.site.config['CATE_NAME_MAP']
        if cate_name_map and origin in cate_name_map:
            return cate_name_map[origin] 
        return origin

    def _extract_metadata_from_text(self, source_text: str) -> 'typing.Dict[str, str]':
        return []

    def split_metadata_from_text(self, source_text: str) -> (str, str):
        """Split text into metadata and content (both strings)."""
        return source_text

    def extract_filename(self, filename: str, lang: str) -> 'typing.Dict[str, str]':
        """Extract metadata from filename."""
        meta = {}
        meta['date'] = self._getNikolaTime(os.path.getctime(filename))
        w_title = os.path.basename(filename).replace("/", "_", 100).rstrip('.org')
        w_title = w_title.replace(" ", "_", 100)
        meta['w_title'] = w_title

        if 'test' in filename:
            meta['write'] = True

        split = filename.split("/") 
        if len(split) > 2:
            cate = split[1]
            cate = self._lookup_cate_table(cate)
            meta['category'] = cate

        self._manually_write_meta(filename, meta)
        return meta

    def _manually_write_meta(self, path, meta):
        # if 'write' in meta:
            with io.open(path, "r+", encoding="utf8") as fd:
                content = fd.read()
                fd.seek(0)
                fd.write("""#+BEGIN_COMMENT
.. title: {}
.. slug: {}
.. date: {}
.. tags: 
.. category: {}
.. link: 
.. description: 
.. type: text

#+END_COMMENT
""".format(meta['w_title'], meta['w_title'], meta['date'], meta.get('category', '')))
                fd.write("\n")
                fd.write(content) 