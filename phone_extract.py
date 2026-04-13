import phonenumbers
from phonenumbers import geocoder, carrier
import yaml


def build_phone_prefix_table(output_path: str = "phone_location_table.yaml"):
    """提取中国手机号前7位映射：prefix -> {location, operator}"""
    print("[*]正在生成完整7位号段归属地表（1300000-1999999）...")

    prefix_map = {}
    total = 1999999 - 1300000 + 1

    for idx, prefix_num in enumerate(range(1300000, 2000000), start=1):
        prefix = f"{prefix_num:07d}"
        full_num = f"+86{prefix}0000"

        try:
            number = phonenumbers.parse(full_num, "CN")
            if not phonenumbers.is_valid_number_for_region(number, "CN"):
                continue

            location = geocoder.description_for_number(number, "zh")
            operator = carrier.name_for_number(number, "zh")

            if location or operator:
                prefix_map[prefix] = {
                    "location": location or "未知",
                    "operator": operator or "未知",
                }
        except phonenumbers.NumberParseException:
            continue

        if idx % 100000 == 0:
            print(f"[*]进度: {idx}/{total}，当前有效号段 {len(prefix_map)}")

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            prefix_map,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=True,
        )

    print(f"[*]导出完成，共 {len(prefix_map)} 条有效号段")
    print(f"[*]完整表已保存到 {output_path}")


if __name__ == "__main__":
    build_phone_prefix_table()