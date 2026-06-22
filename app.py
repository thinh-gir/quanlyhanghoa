import streamlit as st
import json
import os
from datetime import datetime, date

# ==========================================
# 1. CAU HINH VA KHOI TAO HE THONG SMART-HUB HONG PHAT
# ==========================================
st.set_page_config(page_title="He thong Quan ly Smart-Hub Hong Phat", layout="wide")

DB_FILE = "dulieu_kho_hongphat_smarthub.json"

ROLE_LABELS = {
    "1_creator": "CREATOR (DONG SANG LAP)",
    "2_owner": "BOSS (CHU CHO)",
    "3_admin": "ADMIN (QUAN LY)",
    "4_staff": "STAFF (NHAN VIEN)"
}

def luu_du_lieu_he_thong():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump({"users": st.session_state.users, "kho_hang": st.session_state.kho_hang}, f, ensure_ascii=False, indent=4)

def loai_bo_dau_tieng_viet(chuoi_chu):
    co_dau = "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ"
    khong_dau = "aaaaaaaaaaaaaaaaaeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyd"
    bang_chuyen = str.maketrans(co_dau, khong_dau)
    return chuoi_chu.translate(bang_chuyen).lower()

if not os.path.exists(DB_FILE):
    du_lieu_goc = {
        "users": {"Zeroizerd": {"name": "Dong Sang Lap Zeroizerd", "password": "13723@", "active": True, "role": "1_creator"}},
        "kho_hang": [
            {"ten": "CHOCOMONT BANH GAU", "ma_vach": "1111", "ngay_sx": "2026-01-01", "ngay_hh": "2026-06-30", "vi_tri": "Khu A - Ke 01 - Tang 2"},
            {"ten": "CHAO CHONG DINH", "ma_vach": "2222", "ngay_sx": "2026-01-01", "ngay_hh": "2028-01-01", "vi_tri": "Khu A - Ke 02 - Tang 1"}
        ]
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(du_lieu_goc, f, ensure_ascii=False, indent=4)

if 'users' not in st.session_state or 'kho_hang' not in st.session_state:
    with open(DB_FILE, "r", encoding="utf-8") as f:
        tep_du_lieu = json.load(f)
        st.session_state.users = tep_du_lieu.get("users", {})
        st.session_state.kho_hang = tep_du_lieu.get("kho_hang", [])

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# ==========================================
# 2. GIAO DIEN DANG NHAP
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #0088cc;'>HE THONG BAO MAT SMART-HUB HONG PHAT</h2>", unsafe_allow_html=True)
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.subheader("DANG NHAP")
        u_in = st.text_input("Ten tai khoan:", key="u_in").strip()
        p_in = st.text_input("Mat khau bao mat:", type="password", key="p_in")
        if st.button("DANG NHAP SYSTEM", type="primary", use_container_width=True):
            if u_in in st.session_state.users:
                u_info = st.session_state.users[u_in]
                if u_info["password"] == p_in:
                    if u_info["active"]:
                        st.session_state.logged_in = True
                        st.session_state.current_user = u_in
                        st.rerun()
                    else:
                        st.error("Tai khoan chua duoc kich hoat quyen!")
                else:
                    st.error("Mat khau khong chinh xac!")
            else:
                st.error("Tai khoan khong ton tai!")
    with col_l2:
        st.subheader("DANG KY TAI KHOAN MOI")
        r_user = st.text_input("Ten dang nhap moi (viet lien):", key="r_user").strip()
        r_name = st.text_input("Ho va ten that nhan su:", key="r_name").strip()
        r_pass = st.text_input("Tao mat khau truy cap:", type="password", key="r_pass")
        if st.button("GUI YEU CAU DANG KY", use_container_width=True):
            if not r_user or not r_name or not r_pass:
                st.error("Vui long dien day du thong tin!")
            elif r_user in st.session_state.users:
                st.error("Ten tai khoan nay la da co nguoi su dung!")
            else:
                st.session_state.users[r_user] = {"name": r_name, "password": r_pass, "active": False, "role": "4_staff"}
                luu_du_lieu_he_thong()
                st.success("Dang ky thanh cong! Hay cho cap tren phe duyet.")

# ==========================================
# 3. DASHBOARD DIEU HANH CHINH THUC
# ==========================================
else:
    u_now = st.session_state.users[st.session_state.current_user]
    role_now = u_now["role"]
    col_hd1, col_hd2 = st.columns(2)
    with col_hd1:
        st.markdown("<h2 style='color: #0088cc; margin:0;'>SMART-HUB DIEU HANH - HONG PHAT</h2>", unsafe_allow_html=True)
        st.write(f"Nguoi truc: {u_now['name']} | Chuc vu: {ROLE_LABELS[role_now]}")
    with col_hd2:
        if st.button("DANG XUAT", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()
    st.markdown("---")
    
    # CANH BAO BAO QUAN SAN PHAM HET HAN
    co_canh_bao = False
    for item in st.session_state.kho_hang:
        try:
            days_left = (datetime.strptime(item.get("ngay_hh", "2099-12-31"), "%Y-%m-%d") - datetime.now()).days + 1
            if days_left <= 7:
                co_canh_bao = True
                if days_left < 0:
                    st.error(f"CANH BAO - DA QUA HAN {abs(days_left)} NGAY: {item['ten'].upper()} | Ke: {item['vi_tri']}")
                else:
                    st.warning(f"CANH BAO - SAP HET HAN (Con {days_left} ngay): {item['ten'].upper()} | Ke: {item['vi_tri']}")
        except:
            pass
    if not co_canh_bao:
        st.success("He thong an toan. Tat ca vat lieu deu co han su dung an toan.")
    st.markdown("---")
    
    # CHUC NANG SMART-SEARCH GO CHU CAI TU DONG THA GOI Y TU THI (NO ENTER)
    st.markdown("### TIM KIEM THONG MINH (Go chu cai goi y rut xuong ngay lap tuc)")
    with st.popover("BAM VAO DAY DE GO CHU CAI / XEM GOI Y ABC", use_container_width=True):
        chu_cai_nhap = st.text_input("Go chu cai dau, ten hang hoac quet ma vach (Danh sach ABC tu dong cap nhat):", value="", key="inst_search").strip()
        chu_cai_clean = loai_bo_dau_tieng_viet(chu_cai_nhap)
        start_with = []
        contain_with = []
        for sp in st.session_state.kho_hang:
            t_clean = loai_bo_dau_tieng_viet(sp["ten"])
            m_clean = sp["ma_vach"].lower()
            if chu_cai_clean in t_clean or chu_cai_clean in m_clean:
                if t_clean.startswith(chu_cai_clean) or m_clean.startswith(chu_cai_clean):
                    start_with.append(sp)
                else:
                    contain_with.append(sp)
        start_with.sort(key=lambda x: x["ten"])
        contain_with.sort(key=lambda x: x["ten"])
        ket_qua_goi_y = start_with + contain_with
        if chu_cai_nhap:
            st.markdown(f"Goi y khop cho tu khoa '{chu_cai_nhap}':")
        else:
            st.markdown("Toan bo danh sach kho hang (Xep theo thu tu ABC):")
        for item_goi_y in ket_qua_goi_y:
            st.markdown(f"Spham: {item_goi_y['ten'].upper()}")
            st.markdown(f"Vi tri ke: {item_goi_y['vi_tri']} | Ma vach: {item_goi_y['ma_vach']} | HSD: {item_goi_y['ngay_hh']}")
            st.markdown("---")
    st.markdown("---")

    # ==========================================
    # KHU VUR QUAN TRI PHANG TUYET DOI
    # ==========================================
    is_admin_up = role_now in ["1_creator", "2_owner", "3_admin"]
    
    # 3.1 CHUC NANG: NHAP VAT TU MOI
    if is_admin_up:
        st.markdown("### MANAGEMENT ZONE (Khu vur quan tri danh cho Ban Quan Ly)")
        st.markdown("#### Nhap them vat tu hang hoa moi")
        col_a1, col_a2, col_a3, col_a4, col_a5 = st.columns(5)
        with col_a1:
            add_name = st.text_input("Ten hang hoa:", key="w_add_name").strip()
        with col_a2:
            add_barcode = st.text_input("Ma vach dinh danh:", key="w_add_bar").strip()
        with col_a3:
            add_nsx = st.date_input("Ngay san xuat:", value=date.today(), key="w_add_nsx").strftime("%Y-%m-%d")
        with col_a4:
            add_nhh = st.date_input("Han su dung:", value=date.today(), key="w_add_nhh").strftime("%Y-%m-%d")
        with col_a5:
            add_loc = st.text_input("Vi tri ke kho chi tiet:", key="w_add_loc").strip()
        
        if st.button("XAC NHAN GHI SO NHAP KHO", type="primary", use_container_width=True):
            if not add_name or not add_barcode or not add_loc:
                st.error("Vui long nhap day du thong tin!")
            elif any(x["ma_vach"] == add_barcode for x in st.session_state.kho_hang):
                st.error("Ma vach nay da ton tai san!")
            else:
                st.session_state.kho_hang.append({"ten": add_name.upper(), "ma_vach": add_barcode, "ngay_sx": add_nsx, "ngay_hh": add_nhh, "vi_tri": add_loc})
                luu_du_lieu_he_thong()
                st.success(f"Da cap nhat thanh con san pham {add_name.upper()}!")
                st.rerun()
        st.markdown("---")

    # 3.2 CHUC NANG: SUA HOAC XOA VAT TU
    if is_admin_up and st.session_state.kho_hang:
        st.markdown("#### Sua doi thong tin chi tiet / Xoa bo vat tu")
        ds_ten_kho = [f"{x['ten']} [Ma vach: {x['ma_vach']}]" for x in st.session_state.kho_hang]
        sp_chon_de_sua = st.selectbox("Chon san pham ban muon sua doi hoac xoa bo:", options=ds_ten_kho, key="sb_edit_product_flat")
        idx_sua = ds_ten_kho.index(sp_chon_de_sua)
        item_sua = st.session_state.kho_hang[idx_sua]
        
        e_name = st.text_input("Dieu chinh ten hang hoa moi:", value=item_sua["ten"], key="txt_edit_flat_name").strip()
        e_bar = st.text_input("Dieu chinh ma vach moi:", value=item_sua["ma_vach"], key="txt_edit_flat_bar").strip()
        e_loc = st.text_input("Dieu chinh vi tri ke hang moi:", value=item_sua["vi_tri"], key="txt_edit_flat_loc").strip()
        
        if st.button("XAC NHAN LUU THAY DOI VAT TU", type="primary", use_container_width=True):
