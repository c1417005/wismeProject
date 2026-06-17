# 既存テストは test_legacy.py に分割した。
# `python manage.py test wisme.tests.WordSearchCacheTest` のような
# クラス名直接指定を維持するため、ここで再エクスポートする。
from wisme.tests.test_legacy import *  # noqa: F401,F403
