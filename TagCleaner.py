"""
清除掉没什么鸟用的标签，留下有用的。
避免标签过多。
请使用标签分类功能，并填写分类名称。只会对该分类中的标签进行清理。
"""
import os.path
import sqlite3
from loguru import logger

DB_PATH = r"/mnt/e/Onedrive/图片/Billfish/.bf/billfish.db"

conn = None
threshold = 5  # 至少出现 5 次以上标签才保留
tag_group_name = "pixiv_tags"

log_path = os.path.split(os.path.abspath(__file__))[0]
# 日志写入
logger.add(
    os.path.join(log_path, "tag_{time}.log"),
    encoding="utf-8",
    enqueue=True,
)


try:
    conn = sqlite3.connect(DB_PATH)
    gid = conn.execute(f"SELECT id FROM bf_tag_group WHERE name='{tag_group_name}'").fetchone()[0]
    print(f"Group GID:{gid}")
    conn.execute(f"DELETE FROM bf_tag WHERE id IN (SELECT tag_id FROM bf_tag_join_file GROUP BY tag_id HAVING COUNT(tag_id) < {threshold}) AND name NOT LIKE 'Artist:%' AND id IN (SELECT tag_id FROM bf_tag_join_group WHERE gid='{gid}')")
    conn.execute(f"DELETE FROM bf_tag WHERE id NOT IN (SELECT tag_id FROM bf_tag_join_file GROUP BY tag_id) AND id IN (SELECT tag_id FROM bf_tag_join_group WHERE gid='{gid}')")
    conn.execute(r"DELETE FROM bf_tag_join_file WHERE tag_id NOT IN (SELECT id FROM bf_tag)")
    conn.commit()
    conn.close()
    logger.info("Finished.")
except Exception as e:
    logger.error(f"Exception:{e}")
