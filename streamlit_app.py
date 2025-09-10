import streamlit as st
from pathlib import Path
import tempfile

import avstamning_Rental as avm   # <-- byt namn om din fil heter annorlunda

st.set_page_config(page_title="Avstämning", page_icon="📊", layout="centered")
st.title("📊 Avstämning – K1…K6 med K5X")
st.write("Ladda upp kontoutdrag och bokföring (CSV/XLSX). Appen matchar K1–K6 och ger en Excel att ladda ner.")

st.caption(f"Laddad modul: {getattr(avm, '__file__', 'okänd')}")

col1, col2 = st.columns(2)
with col1:
    bank_file = st.file_uploader("Kontoutdrag (Bank)", type=["csv","xlsx","xls"])
with col2:
    bokf_file = st.file_uploader("Bokföring", type=["csv","xlsx","xls"])

go = st.button("Kör avstämning", type="primary", disabled=not (bank_file and bokf_file))

if go:
    try:
        with tempfile.TemporaryDirectory() as td:
            b_path = Path(td) / ("bank" + Path(bank_file.name).suffix or ".xlsx")
            f_path = Path(td) / ("bokf" + Path(bokf_file.name).suffix or ".xlsx")
            b_path.write_bytes(bank_file.getbuffer())
            f_path.write_bytes(bokf_file.getbuffer())

            with st.spinner("Bearbetar…"):
                xlsx_bytes = avm.build_output_excel_bytes(str(b_path), str(f_path))

        st.success("Klar! Ladda ner resultatet:")
        st.download_button(
            "⬇️ Ladda ner output_avstamning.xlsx",
            xlsx_bytes,
            file_name="output_avstamning.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception as e:
        st.error(f"Något gick fel: {e}")
