import html
from datetime import date

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="血液検査所見フォーマッター",
    page_icon="🧪",
    layout="wide",
)


# =========================
# 検査項目マスタ
# =========================
LAB_GROUPS = {
    "血算": [
        ("WBC", "/μL"),
        ("RBC", "×10⁴/μL"),
        ("Hb", "g/dL"),
        ("Ht", "%"),
        ("Plt", "×10⁴/μL"),
        ("Neut", "%"),
        ("Lym", "%"),
        ("Mono", "%"),
        ("Eos", "%"),
        ("Bas", "%"),
    ],
    "生化学": [
        ("TP", "g/dL"),
        ("Alb", "g/dL"),
        ("T-Bil", "mg/dL"),
        ("D-Bil", "mg/dL"),
        ("AST", "U/L"),
        ("ALT", "U/L"),
        ("LDH", "U/L"),
        ("ALP", "U/L"),
        ("γ-GTP", "U/L"),
        ("CK", "U/L"),
        ("BUN", "mg/dL"),
        ("Cre", "mg/dL"),
        ("eGFR", "mL/min/1.73m²"),
        ("Na", "mmol/L"),
        ("K", "mmol/L"),
        ("Cl", "mmol/L"),
        ("Ca", "mg/dL"),
        ("CRP", "mg/dL"),
        ("Glu", "mg/dL"),
        ("HbA1c", "%"),
        ("Amy", "U/L"),
        ("Lipase", "U/L"),
    ],
    "凝固": [
        ("PT-INR", ""),
        ("PT", "%"),
        ("APTT", "sec"),
        ("Fib", "mg/dL"),
        ("FDP", "μg/mL"),
        ("D-dimer", "μg/mL"),
        ("AT-III", "%"),
    ],
    "動脈血液ガス": [
        ("pH", ""),
        ("PaCO₂", "mmHg"),
        ("PaO₂", "mmHg"),
        ("HCO₃⁻", "mmol/L"),
        ("BE", "mmol/L"),
        ("Lac", "mmol/L"),
        ("SaO₂", "%"),
    ],
    "腫瘍マーカー": [
        ("CEA", "ng/mL"),
        ("CA19-9", "U/mL"),
        ("AFP", "ng/mL"),
        ("PIVKA-II", "mAU/mL"),
        ("CYFRA", "ng/mL"),
        ("ProGRP", "pg/mL"),
        ("SCC", "ng/mL"),
        ("NSE", "ng/mL"),
    ],
}


def input_lab_group(group_name: str, items: list[tuple[str, str]]) -> dict:
    st.subheader(group_name)
    values = {}
    cols = st.columns(3)
    for i, (name, unit) in enumerate(items):
        with cols[i % 3]:
            label = f"{name} ({unit})" if unit else name
            values[name] = st.text_input(label, key=f"{group_name}_{name}")
    return values


def format_item(name: str, value: str, unit: str, unit_space: bool = True) -> str:
    value = value.strip()
    if not value:
        return ""
    space = " " if unit_space and unit else ""
    return f"{name} {value}{space}{unit}"


def build_report(values_by_group: dict, style: str, delimiter: str, unit_space: bool) -> str:
    lines = []
    for group_name, items in LAB_GROUPS.items():
        formatted_items = []
        for name, unit in items:
            value = values_by_group.get(group_name, {}).get(name, "")
            formatted = format_item(name, value, unit, unit_space)
            if formatted:
                formatted_items.append(formatted)

        if formatted_items:
            if style == "グループ名あり":
                lines.append(f"{group_name}：{delimiter.join(formatted_items)}")
            else:
                lines.append(delimiter.join(formatted_items))

    if not lines:
        return ""

    if style == "本文形式":
        all_items = []
        for line in lines:
            if "：" in line:
                all_items.append(line.split("：", 1)[1])
            else:
                all_items.append(line)
        return "血液検査所見：" + delimiter.join(all_items) + "。"

    return "\n".join(lines)


def html_copy_button(text: str):
    escaped_text = html.escape(text).replace("\n", "<br>")
    raw_text_js = text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    html_content = f"""
    <div>
      <button onclick="copyRichText()" style="
        background-color:#f0f2f6;
        border:1px solid #ccc;
        border-radius:6px;
        padding:8px 12px;
        cursor:pointer;
        font-size:14px;">
        Times New Roman形式でコピー
      </button>
      <span id="copyStatus" style="margin-left:10px; color:green;"></span>
    </div>

    <script>
    async function copyRichText() {{
      const htmlText = `<div style="font-family:'Times New Roman', serif; font-size:12pt; line-height:1.4;">{escaped_text}</div>`;
      const plainText = `{raw_text_js}`;
      try {{
        const item = new ClipboardItem({{
          "text/html": new Blob([htmlText], {{type: "text/html"}}),
          "text/plain": new Blob([plainText], {{type: "text/plain"}})
        }});
        await navigator.clipboard.write([item]);
        document.getElementById("copyStatus").innerText = "コピーしました";
      }} catch (err) {{
        await navigator.clipboard.writeText(plainText);
        document.getElementById("copyStatus").innerText = "通常テキストとしてコピーしました";
      }}
    }}
    </script>
    """
    components.html(html_content, height=55)


# =========================
# UI
# =========================
st.title("血液検査所見フォーマッター")
st.caption("検査値だけ入力すると、単位つきの症例報告・論文用テキストを作成します。")

with st.sidebar:
    st.header("出力設定")
    style = st.radio(
        "出力形式",
        ["グループ名あり", "本文形式", "グループ名なし"],
        index=0,
    )
    delimiter = st.radio(
        "区切り",
        ["，", ", ", "、", " / "],
        index=0,
    )
    unit_space = st.checkbox("数値と単位の間に半角スペースを入れる", value=True)

    st.markdown("---")
    st.caption("Wordに貼り付けた後、必要に応じてTimes New Roman、12 ptにしてください。HTMLコピーでは可能な範囲で書式を保持します。")

tabs = st.tabs(list(LAB_GROUPS.keys()))
values_by_group = {}

for tab, (group_name, items) in zip(tabs, LAB_GROUPS.items()):
    with tab:
        values_by_group[group_name] = input_lab_group(group_name, items)

report_text = build_report(values_by_group, style, delimiter, unit_space)

st.markdown("---")
st.header("出力")

if report_text:
    st.text_area("Word貼り付け用テキスト", report_text, height=220)
    html_copy_button(report_text)

    st.download_button(
        label="txtでダウンロード",
        data=report_text.encode("utf-8"),
        file_name=f"lab_report_{date.today().isoformat()}.txt",
        mime="text/plain",
    )
else:
    st.info("検査値を入力すると、ここに出力されます。")


with st.expander("表示例"):
    st.code(
        "血算：WBC 7200 /μL，Hb 13.4 g/dL，Plt 22.1 ×10⁴/μL\n"
        "生化学：AST 24 U/L，ALT 18 U/L，BUN 12 mg/dL，Cre 0.82 mg/dL，CRP 0.12 mg/dL\n"
        "凝固：PT-INR 1.02，APTT 28.4 sec，D-dimer 0.5 μg/mL",
        language="text",
    )
