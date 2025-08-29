import streamlit as st
from pathlib import Path
import tempfile
import avstamning_master_kombinerad as avm

st.set_page_config(page_title="Avstämning", page_icon="📊")
st.title("📊 Avstämning – webapp")
st.write("Ladda upp kontoutdrag och bokföringslista (CSV/XLSX).")

col1, col2 = st.columns(2)
with col1:
    bank_file = st.file_uploader("Kontoutdrag (Bank)", type=["csv","xlsx","xls"])
with col2:
    bokf_file = st.file_uploader("Bokföring", type=["csv","xlsx","xls"])

if st.button("Kör avstämning", type="primary", disabled=not (bank_file and bokf_file)):
    try:
        with tempfile.TemporaryDirectory() as td:
            b_path = Path(td) / ("bank" + Path(bank_file.name).suffix)
            f_path = Path(td) / ("bokf" + Path(bokf_file.name).suffix)
            b_path.write_bytes(bank_file.getbuffer())
            f_path.write_bytes(bokf_file.getbuffer())
            st.info("Bearbetar...")
            xlsx_bytes = avm.build_output_excel_bytes(str(b_path), str(f_path))
        st.success("Klar! Ladda ner resultatet:")
        st.download_button("⬇️ Ladda ner output_avstamning.xlsx", xlsx_bytes,
                           file_name="output_avstamning.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"Något gick fel: {e}")
