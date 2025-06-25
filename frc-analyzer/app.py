import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import re

st.title("Анализ .frc файла")

uploaded_file = st.file_uploader("Загрузите .frc файл", type=["frc", "txt"])
if uploaded_file:
    lines = uploaded_file.read().decode("latin1").splitlines()

    st.write("📄 Пример первых строк файла:")
    st.code("\n".join(lines[:10]))

    data = []
    for line in lines:
        line = line.strip().replace(",", ".")
        # Ищем числа с научной нотацией или обычные
        matches = re.findall(r"[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", line)
        if len(matches) >= 2:
            try:
                x = float(matches[0])
                y = float(matches[1])
                data.append((x, y))
            except ValueError:
                continue

    if data:
        x_vals, y_vals = zip(*data)
        x_vals = np.array(x_vals)
        y_vals = np.array(y_vals)

        sign_changes = np.where(np.diff(np.sign(y_vals)))[0]
        roots = []
        for i in sign_changes:
            x0, x1 = x_vals[i], x_vals[i + 1]
            y0, y1 = y_vals[i], y_vals[i + 1]
            if y1 - y0 == 0:
                continue
            root = x0 - y0 * (x1 - x0) / (y1 - y0)
            roots.append(root)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label="График")
        ax.axhline(0, color='gray', linestyle='--')
        for r in roots:
            ax.plot(r, 0, 'ro')
            ax.annotate(f"{r:.2f}", (r, 0), textcoords="offset points", xytext=(0, 10), ha='center')
        ax.set_xlabel("Поле (X)")
        ax.set_ylabel("Момент (Y)")
        ax.legend()
        st.pyplot(fig)

        st.subheader("📌 Найденные корни (X-пересечения):")
        for r in roots:
            st.write(f"{r:.4f}")
    else:
        st.warning("⚠️ Файл не содержит подходящих данных.")
else:
    st.info("⏳ Загрузите .frc файл, чтобы начать.")
    