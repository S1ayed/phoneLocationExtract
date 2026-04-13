import os
import pickle
import re
import yaml


def _script_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))

def _yaml_loader():
    return getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def load_phone_table(file_path: str = "phone_location_table.yaml"):
    table_path = os.path.join(_script_dir(), file_path)
    cache_path = os.path.join(_script_dir(), "phone_location_table.pkl")

    if not os.path.exists(table_path):
        raise FileNotFoundError(f"[*]未找到映射文件: {table_path}")

    yaml_mtime = os.path.getmtime(table_path)
    if os.path.exists(cache_path) and os.path.getmtime(cache_path) >= yaml_mtime:
        print("[*]正在加载本地缓存...", flush=True)
        with open(cache_path, "rb") as f:
            return pickle.load(f) or {}

    print("[*]正在加载 YAML 映射表（首次可能较慢）...", flush=True)
    with open(table_path, "r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=_yaml_loader()) or {}

    print("[*]正在建立本地缓存...", flush=True)
    with open(cache_path, "wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

    return data


def normalize_record(record):
    """兼容两种格式：
    1) 新格式: {location: xx, operator: xx}
    2) 旧格式: "地点 运营商"
    """
    if isinstance(record, dict):
        location = record.get("location", "未知")
        operator = record.get("operator", "未知")
        return location, operator

    if isinstance(record, str):
        text = record.strip()
        if not text:
            return "未知", "未知"
        parts = text.split()
        if len(parts) >= 2:
            operator = parts[-1]
            location = " ".join(parts[:-1])
            return location, operator
        return text, "未知"

    return "未知", "未知"


def is_valid_7digit_phone_prefix(text: str) -> bool:
    return bool(re.fullmatch(r"\d{7}", text))


def main():
    try:
        table = load_phone_table()
    except FileNotFoundError as e:
        print(str(e))
        print("[*]请先运行 phone_extract.py 生成 phone_location_table.yaml")
        return

    print("[*]手机号前7位查询已启动。")
    print("[*]请输入7位手机号前缀（示例: 1300010），输入 q 或 quit 退出。")

    while True:
        user_input = input("> ").strip()

        if user_input.lower() in {"q", "quit", "exit"}:
            print("[*]已退出查询。")
            break

        if not is_valid_7digit_phone_prefix(user_input):
            print("[*]输入格式错误：请输入7位纯数字。")
            continue

        record = table.get(user_input)
        if not record:
            print(f"[*]未找到号段 {user_input} 的映射信息。")
            continue

        location, operator = normalize_record(record)
        print(f"号段: {user_input}")
        print(f"运营商: {operator}")
        print(f"IP属地: {location}")


if __name__ == "__main__":
    main()
