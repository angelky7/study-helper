import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False
from datetime import datetime, timedelta
import json
import os

st.set_page_config(
    page_title="学涯助手 - 大学生效率工具",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .tagline {
        font-size: 1.1rem;
        color: #888;
        margin-bottom: 2rem;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }
    .feature-box {
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        margin-bottom: 0.8rem;
        transition: all 0.2s;
    }
    .feature-box:hover {
        border-color: #667eea;
        box-shadow: 0 2px 8px rgba(102,126,234,0.15);
    }
</style>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.markdown("## 🎓 学涯助手")
    st.markdown("大学生效率工具箱")
    st.divider()

    # 用户信息
    name = st.text_input("你的名字", value="同学")

    st.divider()
    st.markdown("""
    **2026 Qoder 高校创造力大赛**
    - 赛道：StudyHack 学习科研
    - 郑州轻工业大学
    """)

# 数据持久化
DATA_FILE = "study_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"courses": [], "tasks": [], "exams": [], "logs": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# 主标题
st.markdown('<h1 class="main-header">🎓 学涯助手</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">选课不纠结 · 考试不慌张 · 时间不浪费</p>', unsafe_allow_html=True)

# 主标签页
tab1, tab2, tab3, tab4 = st.tabs([
    "📅 考试倒计时",
    "📋 课程管理",
    "✅ 任务规划",
    "📊 学习统计"
])

# ============ 考试倒计时 ============
with tab1:
    st.header("📅 考试倒计时")
    st.markdown("添加考试日期，自动生成倒计时和备考计划")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("添加考试")
        exam_name = st.text_input("考试名称", placeholder="如：高等数学期末考试")
        exam_date = st.date_input("考试日期", value=datetime.now() + timedelta(days=30))
        exam_priority = st.selectbox("重要程度", ["⭐ 普通", "⭐⭐ 重要", "⭐⭐⭐ 关键"])

        if st.button("➕ 添加考试", use_container_width=True):
            if exam_name:
                data["exams"].append({
                    "name": exam_name,
                    "date": str(exam_date),
                    "priority": exam_priority,
                    "created": str(datetime.now())
                })
                save_data(data)
                st.success(f"已添加：{exam_name}")
                st.rerun()

    with col2:
        st.subheader("即将考试")

        if data["exams"]:
            # 按日期排序
            sorted_exams = sorted(data["exams"], key=lambda x: x["date"])

            for i, exam in enumerate(sorted_exams):
                exam_dt = datetime.strptime(exam["date"], "%Y-%m-%d")
                days_left = (exam_dt - datetime.now()).days

                if days_left < 0:
                    status = "✅ 已结束"
                    color = "green"
                elif days_left <= 7:
                    status = f"🔴 仅剩 {days_left} 天！"
                    color = "red"
                elif days_left <= 14:
                    status = f"🟡 还有 {days_left} 天"
                    color = "orange"
                else:
                    status = f"🟢 还有 {days_left} 天"
                    color = "blue"

                with st.container():
                    st.markdown(f"""
                    <div style="padding: 1rem; border-left: 4px solid {color}; background: #f8f9fa; margin-bottom: 0.8rem; border-radius: 0 8px 8px 0;">
                        <strong>{exam['name']}</strong> &nbsp; {exam['priority']}<br>
                        <span style="color: {color}; font-weight: bold;">{status}</span>
                        &nbsp;|&nbsp; 📅 {exam['date']}
                    </div>
                    """, unsafe_allow_html=True)

            # 生成备考建议
            nearest = sorted_exams[0]
            days_left = (datetime.strptime(nearest["date"], "%Y-%m-%d") - datetime.now()).days
            if 0 <= days_left <= 30:
                st.markdown(f"### 💡 {nearest['name']} 备考建议")

                if days_left <= 3:
                    st.markdown("""
                    - **最后冲刺**：只看重点公式和错题
                    - 保证睡眠，不要熬夜
                    - 准备考试用品（证件、笔、计算器）
                    """)
                elif days_left <= 7:
                    st.markdown("""
                    - **一周计划**：每天复习2-3个章节
                    - 做往年真题，找出薄弱环节
                    - 整理错题本，重点突破
                    """)
                elif days_left <= 14:
                    st.markdown("""
                    - **两周计划**：系统过一遍知识点
                    - 每天学习2-3小时，保持节奏
                    - 标记难点，留时间集中攻克
                    """)
                else:
                    st.markdown("""
                    - **提前规划**：了解考试范围和题型
                    - 每周投入5-8小时预习
                    - 做好课堂笔记，考前不慌
                    """)
        else:
            st.info("还没有添加考试，左侧添加你的第一个考试吧！")

# ============ 课程管理 ============
with tab2:
    st.header("📋 课程管理")
    st.markdown("管理你的课程表，追踪课程进度")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("添加课程")
        course_name = st.text_input("课程名称", placeholder="如：电化学原理")
        course_teacher = st.text_input("任课老师")
        course_time = st.text_input("上课时间", placeholder="如：周一 3-4节")
        course_location = st.text_input("上课地点", placeholder="如：A305")
        course_credits = st.number_input("学分", min_value=0.5, max_value=10.0, step=0.5, value=2.0)

        if st.button("➕ 添加课程", use_container_width=True):
            if course_name:
                data["courses"].append({
                    "name": course_name,
                    "teacher": course_teacher,
                    "time": course_time,
                    "location": course_location,
                    "credits": course_credits,
                    "created": str(datetime.now())
                })
                save_data(data)
                st.success(f"已添加：{course_name}")
                st.rerun()

    with col2:
        if data["courses"]:
            # 课程列表
            st.subheader("我的课程")

            df_courses = pd.DataFrame(data["courses"])

            # 按星期排列
            st.dataframe(
                df_courses[["name", "teacher", "time", "location", "credits"]].rename(
                    columns={"name": "课程", "teacher": "老师", "time": "时间", "location": "地点", "credits": "学分"}
                ),
                use_container_width=True,
                hide_index=True
            )

            # 统计
            total_credits = df_courses["credits"].sum()
            st.metric("总学分", f"{total_credits}")

            # 删除课程
            st.subheader("管理课程")
            selected = st.selectbox("选择要删除的课程", df_courses["name"].tolist())
            if st.button("🗑️ 删除选中课程"):
                data["courses"] = [c for c in data["courses"] if c["name"] != selected]
                save_data(data)
                st.rerun()
        else:
            st.info("还没有添加课程")

        # 课程推荐
        st.subheader("🔔 本周课程提醒")
        if data["courses"]:
            weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
            today = datetime.now().weekday()

            for day_idx in range(7):
                day_name = weekdays[day_idx]
                day_courses = [c for c in data["courses"] if day_name in c.get("time", "")]
                if day_courses:
                    label = f"📌 {day_name}" if day_idx == today else day_name
                    with st.expander(f"{label}（{len(day_courses)}门课）"):
                        for c in day_courses:
                            st.markdown(f"- **{c['name']}** {c.get('time', '')} {c.get('location', '')}")
        else:
            st.markdown("添加课程后自动显示")

# ============ 任务规划 ============
with tab3:
    st.header("✅ 任务规划")
    st.markdown("管理作业、实验报告、小组任务等")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("新建任务")
        task_name = st.text_input("任务内容", placeholder="如：完成电化学实验报告")
        task_deadline = st.date_input("截止日期", value=datetime.now() + timedelta(days=7))
        task_type = st.selectbox("任务类型", ["📝 作业", "🔬 实验报告", "📖 预习/复习", "👥 小组任务", "📄 论文/报告", "其他"])
        task_difficulty = st.slider("预计耗时（小时）", 0.5, 20.0, 2.0, 0.5)

        if st.button("➕ 添加任务", use_container_width=True):
            if task_name:
                data["tasks"].append({
                    "name": task_name,
                    "deadline": str(task_deadline),
                    "type": task_type,
                    "hours": task_difficulty,
                    "done": False,
                    "created": str(datetime.now())
                })
                save_data(data)
                st.success("已添加！")
                st.rerun()

    with col2:
        # 任务统计
        pending = [t for t in data["tasks"] if not t["done"]]
        done = [t for t in data["tasks"] if t["done"]]

        mcol1, mcol2, mcol3 = st.columns(3)
        mcol1.metric("待完成", len(pending))
        mcol2.metric("已完成", len(done))
        total_hours = sum(t["hours"] for t in pending)
        mcol3.metric("预计总耗时", f"{total_hours:.1f}h")

        st.subheader("📌 待办任务")

        if pending:
            # 按截止日期排序
            pending_sorted = sorted(pending, key=lambda x: x["deadline"])

            for i, task in enumerate(pending_sorted):
                deadline = datetime.strptime(task["deadline"], "%Y-%m-%d")
                days_left = (deadline - datetime.now()).days

                if days_left < 0:
                    urgency = "🔴 已逾期"
                elif days_left <= 2:
                    urgency = f"🔴 {days_left}天后截止"
                elif days_left <= 5:
                    urgency = f"🟡 {days_left}天后截止"
                else:
                    urgency = f"🟢 {days_left}天后截止"

                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(f"""
                    **{task['type']}** {task['name']}<br>
                    <small>{urgency} · 截止 {task['deadline']} · 预计 {task['hours']}h</small>
                    """, unsafe_allow_html=True)
                with col_b:
                    if st.button("✅", key=f"done_{i}"):
                        task["done"] = True
                        save_data(data)
                        st.rerun()
        else:
            st.success("太棒了！没有待办任务 🎉")

        # 已完成任务
        if done:
            with st.expander(f"已完成（{len(done)}项）"):
                for task in done:
                    st.markdown(f"~~{task['name']}~~ ✅")

        # 清空已完成
        if done and st.button("🗑️ 清空已完成任务"):
            data["tasks"] = [t for t in data["tasks"] if not t["done"]]
            save_data(data)
            st.rerun()

# ============ 学习统计 ============
with tab4:
    st.header("📊 学习统计")
    st.markdown("记录每日学习情况，追踪学习趋势")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("记录今天的学习")
        log_date = st.date_input("日期", value=datetime.now())
        log_hours = st.slider("学习时长（小时）", 0.0, 16.0, 3.0, 0.5)
        log_subject = st.text_input("学习内容", placeholder="如：复习电化学第三章")
        log_mood = st.select_slider("今天状态", options=["😫 很累", "😐 一般", "🙂 不错", "🔥 充满动力"])

        if st.button("💾 保存记录", use_container_width=True):
            data["logs"].append({
                "date": str(log_date),
                "hours": log_hours,
                "subject": log_subject,
                "mood": log_mood,
                "created": str(datetime.now())
            })
            save_data(data)
            st.success("已记录！")
            st.rerun()

    with col2:
        if data["logs"]:
            df_logs = pd.DataFrame(data["logs"])
            df_logs["date"] = pd.to_datetime(df_logs["date"])
            df_logs = df_logs.sort_values("date")

            # 总览指标
            total_hours = df_logs["hours"].sum()
            avg_hours = df_logs["hours"].mean()
            days_recorded = df_logs["date"].nunique()

            m1, m2, m3 = st.columns(3)
            m1.metric("累计学习", f"{total_hours:.1f}h")
            m2.metric("日均时长", f"{avg_hours:.1f}h")
            m3.metric("打卡天数", days_recorded)

            # 学习趋势图
            st.subheader("📈 学习趋势")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(df_logs["date"].dt.strftime("%m-%d"), df_logs["hours"], color="#667eea", alpha=0.7)
            ax.set_xlabel("日期")
            ax.set_ylabel("学习时长(h)")
            ax.set_title("每日学习时长")
            ax.grid(True, alpha=0.2, axis='y')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

            # 周统计
            st.subheader("📅 本周统计")
            this_week = df_logs[df_logs["date"] >= datetime.now() - timedelta(days=7)]
            if len(this_week) > 0:
                week_hours = this_week["hours"].sum()
                st.markdown(f"本周学习 **{week_hours:.1f}** 小时")

                # 进度条
                goal = 20  # 周目标
                progress = min(week_hours / goal, 1.0)
                st.progress(progress, text=f"周目标 {goal}h · 完成 {progress*100:.0f}%")
            else:
                st.info("本周还没有记录")

            # 状态分布
            st.subheader("😊 学习状态分布")
            mood_counts = df_logs["mood"].value_counts()
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            colors = ['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3']
            ax2.pie(mood_counts.values, labels=mood_counts.index, autopct='%1.0f%%', colors=colors)
            ax2.set_title("学习状态占比")
            st.pyplot(fig2)
        else:
            st.info("还没有学习记录，在左侧记录今天的学习吧！")

# 页脚
st.divider()
st.markdown("""
<div style='text-align: center; color: #999; padding: 1rem;'>
    <p>🎓 学涯助手 · 2026 Qoder 高校创造力大赛 · StudyHack 赛道</p>
    <p>用 Qoder 开发 | 郑州轻工业大学</p>
</div>
""", unsafe_allow_html=True)
