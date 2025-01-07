import streamlit as st
import subprocess

# Tiêu đề ứng dụng
st.title("Run SSHX Script with Real-Time Logging")

# Mô tả ứng dụng
st.write("Nhấn nút bên dưới để chạy lệnh `curl -sSf https://sshx.io/get | sh -s run` với log thời gian thực.")

# Placeholder để hiển thị log
log_container = st.empty()

# Nút chạy lệnh
if st.button("Chạy lệnh"):
    # Biến để lưu trữ log liên tục
    log_data = ""
    try:
        # Thực thi lệnh và đọc log theo thời gian thực
        with subprocess.Popen(
            "stdbuf -oL curl -sSf https://sshx.io/get | sh -s run",
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1  # Không buffer hóa
        ) as process:
            for line in iter(process.stdout.readline, ''):
                log_data += line  # Lưu log mới vào biến
                log_container.text(log_data)  # Hiển thị toàn bộ log
            process.stdout.close()
            process.wait()  # Đợi quá trình hoàn thành

        if process.returncode == 0:
            st.success("Lệnh đã chạy thành công!")
        else:
            st.error(f"Lệnh thất bại với mã lỗi {process.returncode}.")
    except Exception as e:
        # Hiển thị lỗi nếu có
        st.error(f"Đã xảy ra lỗi: {e}")