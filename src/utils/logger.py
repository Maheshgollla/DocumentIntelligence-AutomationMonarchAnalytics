import logging
import sys

class EmojiSafeStreamHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            super().emit(record)
        except UnicodeEncodeError:
            record.msg = record.msg.encode("utf-8", errors="replace").decode("utf-8")
            super().emit(record)

logger = logging.getLogger("doc_intelligence")
logger.setLevel(logging.INFO)

handler = EmojiSafeStreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


