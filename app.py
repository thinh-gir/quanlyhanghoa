import streamlit as st
import json
import os
from datetime import datetime, date

# ==========================================
# 1. CẤU HÌNH & KHỞI TẠO HỆ THỐNG SMART-HUB HỒNG PHÁT
# ==========================================
st.set_page_config(page_title="Hệ thống Quản lý Smart-Hub Hồng Phát", layout="wide", page_icon="🏭")

DB_FILE = "dulieu_kho_hongphat_smarthub.json"

ROLE_LABELS = {
    "1_creator": "👑 CREATOR (ĐỒNG SÁNG LẬP)",
    "2_owner": "💼 BOSS (CHỦ CHỢ)",
    "3_admin": "🛠️ ADMIN (QUẢN LÝ)",
    "4_staff": "👁️ STAFF (NHÂN VIÊN)"
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
        "users": {"Zeroizerd": {"name": "Đồng Sáng Lập Zeroizerd", "password": "13723@", "active": True, "role": "1_creator"}},
        "kho_hang": [
            {"ten": "CHOCOMONT BÁNH GẤU", "ma_vach": "1111", "ngay_sx": "2026-01-01", "ngay_hh": "2026-06-30", "vi_tri": "Khu A - Kệ 01 - Tầng 2"},
            {"ten": "CHẢO CHỐNG DÍNH", "ma_vach": "2222", "ngay_sx": "2026-01-01", "ngay_hh": "2028-01-01", "vi_tri": "Khu A - Kệ 02 - Tầng 1"},
            {"ten": "BÁNH MÌ SỮA", "ma_vach": "3333", "ngay_sx": "2026-01-01", "ngay_hh": "2026-02-01", "vi_tri": "Khu B - Kệ 01 - Tầng 1"}
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

# Khởi tạo khóa lưu trữ sản phẩm đang chọn bằng ngón tay
if 'mobile_selected_mv' not in st.session_state:
    st.session_state.mobile_selected_mv = None

# ==========================================
# 2. GIAO DIỆN ĐĂNG NHẬP (TỐI ƯU MOBILE)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #0088cc;'>🏭 SMART-HUB HỒNG PHÁT</h2>", unsafe_allow_html=True)
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.subheader("🔑 ĐĂNG NHẬP")
        u_in = st.text_input("Tên tài khoản:", key="u_in").strip()
        p_in = st.text_input("Mật khẩu bảo mật:", type="password", key="p_in")
        if st.button("ĐĂNG NHẬP SYSTEM", type="primary", use_container_width=True):
            if u_in in st.session_state.users:
                u_info = st.session_state.users[u_in]
                if u_info["password"] == p_in:
                    if u_info["active"]:
                        st.session_state.logged_in = True
                        st.session_state.current_user = u_in
                        st.rerun()
                    else: st.error("Tài khoản chưa được kích hoạt quyền!")
                else: st.error("Mật khẩu không chính xác!")
            else: st.error("Tài khoản không tồn tại!")
    with col_l2:
        st.subheader("📝 ĐĂNG KÝ MỚI")
        r_user = st.text_input("Tên đăng nhập mới (viết liền):", key="r_user").strip()
        r_name = st.text_input("Họ và tên thật nhân sự:", key="r_name").strip()
        r_pass = st.text_input("Tạo mật khẩu truy cập:", type="password", key="r_pass")
        if st.button("GỬI YÊU CẦU ĐĂNG KÝ", use_container_width=True):
            if not r_user or not r_name or not r_pass: st.error("Vui lòng điền đầy đủ thông tin!")
            elif r_user in st.session_state.users: st.error("Tên tài khoản này đã có người sử dụng!")
            else:
                st.session_state.users[r_user] = {"name": r_name, "password": r_pass, "active": False, "role": "4_staff"}
                luu_du_lieu_he_thong()
                st.success("Đăng ký thành công! Hãy chờ cấp trên phê duyệt.")

# ==========================================
# 3. DASHBOARD ĐIỀU HÀNH CHÍNH THỨC (GIAO DIỆN PHẲNG DI ĐỘNG)
# ==========================================
else:
    u_now = st.session_state.users[st.session_state.current_user]
    role_now = u_now["role"]
    col_hd1, col_hd2 = st.columns(2)
    with col_hd1:
        st.markdown(f"<h2 style='color: #0088cc; margin:0;'>🏭 SMART-HUB — HỒNG PHÁT</h2>", unsafe_allow_html=True)
        st.write(f"👤 Trực: **{u_now['name']}** | `{ROLE_LABELS[role_now]}`")
    with col_hd2:
        if st.button("🚪 ĐĂNG XUẤT", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.mobile_selected_mv = None
            st.rerun()
    st.markdown("---")
    
    # CẢNH BÁO BẢO QUẢN SẢN PHẨM HẾT HẠN
    co_canh_bao = False
    for item in st.session_state.kho_hang:
        try:
            days_left = (datetime.strptime(item.get("ngay_hh", "2099-12-31"), "%Y-%m-%d") - datetime.now()).days + 1
            if days_left <= 7:
                co_canh_bao = True
                if days_left < 0: st.error(f"🚨 **💥 QUÁ HẠN {abs(days_left)} NGÀY**: {item['ten'].upper()} | Kệ: {item['vi_tri']}")
                else: st.warning(f"⚠️ **⏳ SẮP HẾT HẠN (Còn {days_left} ngày)**: {item['ten'].upper()} | Kệ: {item['vi_tri']}")
        except: pass
    if not co_canh_bao: st.success("✅ Toàn bộ vật liệu kho nằm trong hạn sử dụng an toàn.")
    st.markdown("---")
    
    # ==========================================
    # CHỨC NĂNG SMART-SEARCH GÕ CHỮ CÁI THẢ PHÍM GỢI Ý ĐỘNG CHO MOBILE
    # ==========================================
    st.markdown("### 🔍 MOBILE SMART SEARCH (Tìm kiếm chạm gợi ý siêu tốc trên điện thoại)")
    
    # Ô gõ chữ thuần tương thích 100% bàn phím ảo điện thoại di động
    chu_cai_nhap = st.text_input("Gõ chữ cái đầu, tên sản phẩm hoặc quét mã vạch:", value="", key="mobile_keyboard_search").strip()
    chu_cai_clean = loai_bo_dau_tieng_viet(chu_cai_nhap)
    
    if chu_cai_nhap:
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
        
        if ket_qua_goi_y:
            st.markdown("👇 *Chạm ngón tay vào tên hàng hóa dưới đây để định vị kệ:*")
            
            # Xuất kết quả thành các nút bấm Tag to, dễ bấm bằng ngón tay trên điện thoại
            for item_goi_y in ket_qua_goi_y[:8]: # Hiển thị tối đa 8 gợi ý ABC tốt nhất phù hợp màn hình dọc di động
                if st.button(f"📦 {item_goi_y['ten'].upper()} [MV: {item_goi_y['ma_vach']}]", key=f"mob_btn_{item_goi_y['ma_vach']}", use_container_width=True):
                    st.session_state.mobile_selected_mv = item_goi_y['ma_vach']
        else:
            st.error("❌ Không tìm thấy hàng hóa nào khớp với chữ cái sếp gõ.")
            
    # Hiển thị bảng định vị mục tiêu khi chạm ngón tay chọn sản phẩm gợi ý
    if st.session_state.mobile_selected_mv:
        for sp in st.session_state.kho_hang:
            if sp["ma_vach"] == st.session_state.mobile_selected_mv:
                st.markdown("---")
                st.markdown("<h4 style='color: #0088cc;'>📍 ĐỊNH VỊ VỊ TRÍ THÀNH CÔNG:</h4>", unsafe_allow_html=True)
                st.info(f"📍 **VỊ TRÍ TRÊN KỆ KHO:** {sp['vi_tri']}\n\n🔹 **Tên mặt hàng:** {sp['ten'].upper()}\n\n🔹 **Mã vạch:** `{sp['ma_vach']}` | **Hạn bảo quản:** {sp['ngay_hh']}")
                break
    else:
        st.info("💡 Mẹo di động: Chỉ cần nhập 1 vài chữ cái đầu (ví dụ: c, ch, b), hệ thống sẽ rớt nút bấm gợi ý ra ngay cho sếp chạm chọn.")

    st.markdown("---")

    # KHU VỰC THAO TÁC CỦA QUẢN LÝ (THÊM / SỬA / XÓA)
    if role_now in ["1_creator", "2_owner", "3_admin"]:
        st.markdown("### ⚙️ MANAGEMENT ZONE (Khu vực quản trị dành cho Ban Quản Lý Chợ)")
        st.markdown("#### ➕ Nhập thêm vật tư hàng hóa mới")
        col_a1, col_a2, col_a3, col_a4, col_a5 = st.columns(5)
        with col_a1: add_name = st.text_input("Tên hàng hóa:", key="w_add_name").strip()
        with col_a2: add_barcode = st.text_input("Mã vạch định danh:", key="w_add_bar").strip()
        with col_a3: add_nsx = st.date_input("Ngày sản xuất:", value=date.today(), key="w_add_nsx").strftime("%Y-%m-%d")
        with col_a4: add_nhh = st.date_input("Hạn sử dụng:", value=date.today(), key="w_add_nhh").strftime("%Y-%m-%d")
        with col_a5: add_loc = st.text_input("Vị trí kệ kho chi tiết:", key="w_add_loc").strip()
        if st.button("➕ XÁC NHẬN GHI SỔ NHẬP KHO", type="primary", use_container_width=True):
            if not add_name or not add_barcode or not add_loc: st.error("Vui lòng nhập đầy đủ thông tin!")
            elif any(x["ma_vach"] == add_barcode for x in st.session_state.kho_hang): st.error("Mã vạch này đã tồn tại sẵn!")
            else:
                st.session_state.kho_hang.append({"ten": add_name.upper(), "ma_vach": add_barcode, "ngay_sx": add_nsx, "ngay_hh": add_nhh, "vi_tri": add_loc})
                luu_du_lieu_he_thong()
