import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ===============================
# 页面配置必须在最前面
# ===============================
st.set_page_config(
    layout="wide",
    page_title="有机固废理化性质数据库",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ===============================
# 自定义CSS样式 - 增大字体
# ===============================
st.markdown("""
<style>
    /* 全局字体大小调整 */
    html, body, [class*="css"] {
        font-size: 16px !important;
        font-family: 'Arial', 'Helvetica', sans-serif;
    }

    /* 主标题样式 */
    .main-title {
        text-align: center;
        color: #2C3E50;
        padding: 15px;
        background: linear-gradient(90deg, #F5F7FA, #E4E7ED);
        border-radius: 10px;
        margin-bottom: 25px;
        border-left: 5px solid #34495E;
        font-size: 32px !important;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* 副标题 */
    h2 {
        font-size: 24px !important;
        color: #2C3E50;
        margin-top: 20px;
        margin-bottom: 15px;
        font-weight: bold;
    }

    h3 {
        font-size: 20px !important;
        color: #34495E;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    h4 {
        font-size: 18px !important;
        color: #2C3E50;
        margin-top: 10px;
        margin-bottom: 8px;
        font-weight: 600;
    }

    /* 模块分隔样式 */
    .module-divider {
        border: 2px solid #D5DBDB;
        border-radius: 10px;
        padding: 15px;
        margin: 20px 0;
        background-color: #F8F9F9;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* 侧边栏字体 */
    .sidebar .sidebar-content {
        background-color: #ECF0F1;
        font-size: 16px !important;
    }

    .sidebar .sidebar-content label {
        font-size: 16px !important;
        font-weight: 500;
        color: #2C3E50;
    }

    .sidebar .sidebar-content .stSelectbox, 
    .sidebar .sidebar-content .stNumberInput,
    .sidebar .sidebar-content .stSlider {
        font-size: 16px !important;
    }

    /* 卡片样式 */
    .metric-card {
        background-color: #F8F9F9;
        padding: 18px;
        border-radius: 10px;
        border-left: 5px solid #3498DB;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        font-size: 16px !important;
        border-top: 1px solid #EAEDED;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
        background-color: #FFFFFF;
    }

    .metric-card h4 {
        font-size: 18px !important;
        margin-bottom: 8px;
        color: #2C3E50;
    }

    .metric-card h3 {
        font-size: 22px !important;
        margin-top: 5px;
        color: #2980B9;
    }

    /* 表格字体 */
    .stDataFrame {
        font-size: 16px !important;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .stDataFrame th {
        font-size: 16px !important;
        font-weight: bold;
        background-color: #34495E !important;
        color: white !important;
    }

    .stDataFrame td {
        font-size: 16px !important;
        background-color: #F8F9F9 !important;
    }

    /* 标签页字体 */
    .stTabs [data-baseweb="tab"] {
        background-color: #ECF0F1;
        border-radius: 8px 8px 0px 0px;
        padding: 12px 24px;
        font-size: 16px !important;
        font-weight: 500;
        color: #2C3E50;
        border: 1px solid #D5DBDB;
        margin-right: 4px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #3498DB;
        color: white !important;
        font-size: 16px !important;
        font-weight: bold;
        border-bottom: 3px solid #2980B9;
    }

    /* 指标字体 */
    .stMetric {
        background-color: #F8F9F9;
        padding: 18px;
        border-radius: 10px;
        border-left: 5px solid #3498DB;
        font-size: 16px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-top: 1px solid #EAEDED;
    }

    .stMetric label {
        font-size: 16px !important;
        font-weight: 500;
        color: #2C3E50;
    }

    .stMetric div[data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: bold;
        color: #2980B9;
    }

    .stMetric div[data-testid="stMetricLabel"] {
        font-size: 16px !important;
        opacity: 0.8;
        color: #566573;
    }

    /* 警告和信息框字体 */
    .stAlert {
        font-size: 16px !important;
        border-radius: 8px;
    }

    /* 按钮字体 */
    .stButton button {
        font-size: 16px !important;
        font-weight: 500;
        background-color: #3498DB;
        color: white;
        border-radius: 8px;
        border: none;
        transition: background-color 0.3s ease;
    }

    .stButton button:hover {
        background-color: #2980B9;
    }

    /* 单选按钮和多选框字体 */
    .stRadio label, .stCheckbox label {
        font-size: 16px !important;
        color: #2C3E50;
    }

    /* 滑块字体 */
    .stSlider label {
        font-size: 16px !important;
        color: #2C3E50;
    }

    /* 下载按钮 */
    .stDownloadButton button {
        font-size: 16px !important;
        background-color: #27AE60;
    }

    .stDownloadButton button:hover {
        background-color: #229954;
    }

    /* 页脚字体 */
    .footer {
        font-size: 16px !important;
    }

    /* 模块标题样式 - 大地色系 */
    .module-title {
        background: linear-gradient(90deg, #A67C52, #8B7355);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        font-size: 20px !important;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 4px 8px rgba(139, 115, 85, 0.3);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        letter-spacing: 0.5px;
    }

    /* 物质名称显示样式 */
    .material-name-display {
        background: linear-gradient(90deg, #3498DB, #2980B9);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        font-size: 22px !important;
        font-weight: bold;
        box-shadow: 0 6px 12px rgba(52, 152, 219, 0.2);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    /* 横线分隔样式 */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, #A67C52, #8B7355, #D7CCC8);
        margin: 30px 0;
        border-radius: 1px;
        border: none;
        opacity: 0.7;
    }

    /* 选择框样式 */
    .stSelectbox, .stMultiselect {
        border-radius: 8px;
    }

    /* 调整图表容器的阴影 */
    .js-plotly-plot {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)


# ===============================
# 加载数据函数
# ===============================
@st.cache_data
def load_data():
    df = pd.read_excel(
        "data.xls",
        na_values=["—", "-", "–", "nan", "NaN", ""]
    )

    # 规范分类字段
    if "分类" in df.columns:
        df["分类"] = df["分类"].astype("string").str.strip()

    # 删除分类为空的脏行
    df = df.dropna(subset=["分类"])

    # 处理数值数据
    def clean_numeric(x):
        if pd.isna(x):
            return np.nan
        x = str(x).strip()
        if x in ["—", "-", "–"]:
            return np.nan
        if "±" in x:
            return float(x.split("±")[0].strip())
        if x.startswith("<"):
            return float(x[1:])
        try:
            return float(x)
        except ValueError:
            return np.nan

    # 确定数值列（排除分类列和物质名称列）
    categorical_cols = ["分类", "物质名称"]
    numeric_cols = [c for c in df.columns if c not in categorical_cols]

    for col in numeric_cols:
        df[col] = df[col].apply(clean_numeric)

    return df


# ===============================
# 辅助函数
# ===============================
def create_element_radar_chart(material_data, category_data, selected_material, selected_category):
    """创建元素分析雷达图对比"""
    categories = ['C', 'H', 'O', 'N', 'S']

    # 获取当前物质数据
    current_values = [material_data.get(cat, 0) for cat in categories]

    # 获取同类别的平均值
    avg_values = []
    for cat in categories:
        avg = category_data[cat].mean()
        avg_values.append(avg if not pd.isna(avg) else 0)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=current_values,
        theta=categories,
        fill='toself',
        name=selected_material,
        line_color='#E74C3C',
        fillcolor='rgba(231, 76, 60, 0.2)',
        line=dict(width=2.5)
    ))

    fig.add_trace(go.Scatterpolar(
        r=avg_values,
        theta=categories,
        fill='toself',
        name=f'{selected_category}平均值',
        line_color='#3498DB',
        fillcolor='rgba(52, 152, 219, 0.2)',
        line=dict(width=2.5)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(current_values), max(avg_values)) * 1.2],
                tickfont=dict(size=14, color='#2C3E50'),
                linecolor='#BDC3C7',
                gridcolor='#ECF0F1'
            ),
            angularaxis=dict(
                tickfont=dict(size=14, color='#2C3E50'),
                linecolor='#BDC3C7',
                gridcolor='#ECF0F1'
            ),
            bgcolor='rgba(248, 249, 249, 0.5)'
        ),
        showlegend=True,
        title=dict(
            text="元素分析雷达图对比",
            font=dict(size=18, color='#2C3E50', family='Arial')
        ),
        height=400,
        font=dict(size=14, family='Arial'),
        legend=dict(
            font=dict(size=14),
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='#BDC3C7',
            borderwidth=1
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig


def create_proximate_radar_chart(material_data, category_data, selected_material, selected_category):
    """创建工业分析雷达图对比"""
    categories = ['固定碳', '挥发分', '水分', '灰分']

    # 获取当前物质数据
    current_values = [material_data.get(cat, 0) for cat in categories]

    # 获取同类别的平均值
    avg_values = []
    for cat in categories:
        avg = category_data[cat].mean()
        avg_values.append(avg if not pd.isna(avg) else 0)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=current_values,
        theta=categories,
        fill='toself',
        name=selected_material,
        line_color='#9B59B6',
        fillcolor='rgba(155, 89, 182, 0.2)',
        line=dict(width=2.5)
    ))

    fig.add_trace(go.Scatterpolar(
        r=avg_values,
        theta=categories,
        fill='toself',
        name=f'{selected_category}平均值',
        line_color='#2ECC71',
        fillcolor='rgba(46, 204, 113, 0.2)',
        line=dict(width=2.5)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(current_values), max(avg_values)) * 1.2],
                tickfont=dict(size=14, color='#2C3E50'),
                linecolor='#BDC3C7',
                gridcolor='#ECF0F1'
            ),
            angularaxis=dict(
                tickfont=dict(size=14, color='#2C3E50'),
                linecolor='#BDC3C7',
                gridcolor='#ECF0F1'
            ),
            bgcolor='rgba(248, 249, 249, 0.5)'
        ),
        showlegend=True,
        title=dict(
            text="工业分析雷达图对比",
            font=dict(size=18, color='#2C3E50', family='Arial')
        ),
        height=400,
        font=dict(size=14, family='Arial'),
        legend=dict(
            font=dict(size=14),
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='#BDC3C7',
            borderwidth=1
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig


def create_heatmap(df_category):
    """创建热力图"""
    # 选择要显示的数值列
    heatmap_data = df_category[['C', 'H', 'O', 'N', '固定碳', '挥发分', '灰分', '水分']]

    fig = px.imshow(
        heatmap_data.T,
        labels=dict(x="物质", y="指标", color="值"),
        x=df_category['物质名称'].tolist(),
        y=heatmap_data.columns.tolist(),
        color_continuous_scale='Viridis',
        aspect="auto"
    )

    fig.update_layout(
        title=dict(
            text=f"{selected_category} 热力图分析",
            font=dict(size=16, color='#2C3E50')
        ),
        height=400,
        font=dict(size=14),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig


# ===============================
# 顶刊论文配色方案
# ===============================
# Nature/Science 风格的配色方案
JOURNAL_COLORS = [
    '#1F77B4',  # 蓝色
    '#FF7F0E',  # 橙色
    '#2CA02C',  # 绿色
    '#D62728',  # 红色
    '#9467BD',  # 紫色
    '#8C564B',  # 棕色
    '#E377C2',  # 粉色
    '#7F7F7F',  # 灰色
    '#BCBD22',  # 黄绿色
    '#17BECF',  # 青色
]

# 高级配色方案 - 改为用户指定的配色
PIE_COLORS = [
    '#BED2ED',  # 浅蓝色
    '#DCE8BA',  # 浅绿色
    '#C3B3D0',  # 浅紫色
    '#E6C6C4',  # 浅粉色
    '#E6C48F',  # 浅橙色
    '#FCF8B9',  # 浅黄色
    '#A6D0DD',  # 补充：天空蓝
    '#FF9A8B',  # 补充：珊瑚粉
    '#C7E9B0',  # 补充：淡绿色
    '#B5B8D1',  # 补充：淡紫色
]

# 顶刊渐变色配色方案
JOURNAL_GRADIENTS = [
    'Viridis',  # Nature常用
    'Plasma',  # Science常用
    'Cividis',  # 色盲友好，Nature推荐
    'Turbo',  # Google Research开发
    'Rainbow',  # 彩虹色
    'Portland',  # 地质学常用
    'Electric',  # 电气风格
]

# 顶刊单色渐变色
JOURNAL_SEQUENTIAL = [
    'Blues',  # 蓝色系
    'Greens',  # 绿色系
    'Reds',  # 红色系
    'Oranges',  # 橙色系
    'Purples',  # 紫色系
    'Greys',  # 灰色系
    'YlOrRd',  # 黄-橙-红
    'YlGnBu',  # 黄-绿-蓝
    'Inferno',  # 地狱火风格
    'Magma',  # 岩浆风格
]

# ===============================
# 主程序开始
# ===============================
# 加载数据
df = load_data()

# ===============================
# 页面标题 - 使用更大字体
# ===============================
st.markdown('<h1 class="main-title">📊 有机固废理化性质数据库</h1>', unsafe_allow_html=True)

# ===============================
# 侧边栏 - 增大字体
# ===============================
with st.sidebar:
    st.markdown('<h2 style="font-size: 22px !important;">🔧 数据选择</h2>', unsafe_allow_html=True)

    # 选择分类
    categories = sorted(df["分类"].unique())
    selected_category = st.selectbox(
        "选择固废分类",
        categories,
        help="选择要分析的固废类型"
    )

    # 根据选择的分类筛选数据
    df_category = df[df["分类"] == selected_category]

    # 选择物质
    materials = sorted(df_category["物质名称"].unique())
    selected_material = st.selectbox(
        "选择具体物质",
        materials,
        help="选择要详细分析的具体物质"
    )

    st.divider()

    # 快速统计
    st.markdown('<h3 style="font-size: 20px !important;">📈 快速统计</h3>', unsafe_allow_html=True)
    st.metric("该分类物质数量", len(materials))
    st.metric("数据库总条目数", len(df))

    # 渐变色选择
    st.divider()
    st.markdown('<h3 style="font-size: 20px !important;">🎨 配色设置</h3>', unsafe_allow_html=True)

    # 选择热力图的渐变色
    selected_gradient = st.selectbox(
        "热力图渐变色方案",
        JOURNAL_GRADIENTS,
        index=0,
        help="选择顶刊论文常用的渐变色方案"
    )

    # 选择柱状图配色
    selected_sequential = st.selectbox(
        "柱状图渐变色方案",
        JOURNAL_SEQUENTIAL,
        index=0,
        help="选择顶刊论文常用的单色渐变色方案"
    )

    # 选择数据库概览柱状图配色
    selected_overview_gradient = st.selectbox(
        "数据库概览柱状图渐变色方案",
        JOURNAL_GRADIENTS,
        index=1,  # 默认选择 Plasma
        help="选择数据库概览柱状图的渐变色方案"
    )

    # 数据下载按钮
    st.divider()
    st.markdown('<h3 style="font-size: 20px !important;">💾 数据导出</h3>', unsafe_allow_html=True)

    # 导出当前分类数据
    csv = df_category.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"导出 {selected_category} 数据",
        data=csv,
        file_name=f"{selected_category}_数据.csv",
        mime="text/csv",
        help="下载当前分类的所有数据"
    )

# ===============================
# 顶部信息栏 - 添加更多平均指标
# ===============================
st.markdown('<h3 style="font-size: 20px !important;">📊 关键指标概览</h3>', unsafe_allow_html=True)

# 第一行：基础统计信息
col_info1, col_info2, col_info3, col_info4 = st.columns(4)
with col_info1:
    st.metric("📁 分类数量", len(categories))
with col_info2:
    st.metric("📦 物质数量", len(materials))
with col_info3:
    avg_hhv = df_category["高位热值"].mean()
    st.metric("🔥 平均高位热值", f"{avg_hhv:.2f} MJ/kg" if not pd.isna(avg_hhv) else "N/A")
with col_info4:
    avg_lhv = df_category["低位热值"].mean()
    st.metric("🌡️ 平均低位热值", f"{avg_lhv:.2f} MJ/kg" if not pd.isna(avg_lhv) else "N/A")

# 第二行：工业分析平均指标
col_info5, col_info6, col_info7, col_info8 = st.columns(4)
with col_info5:
    avg_volatile = df_category["挥发分"].mean()
    st.metric("⚡ 平均挥发分", f"{avg_volatile:.2f}%" if not pd.isna(avg_volatile) else "N/A")
with col_info6:
    avg_ash = df_category["灰分"].mean()
    st.metric("⚫ 平均灰分含量", f"{avg_ash:.2f}%" if not pd.isna(avg_ash) else "N/A")
with col_info7:
    avg_moisture = df_category["水分"].mean()
    st.metric("💧 平均水分", f"{avg_moisture:.2f}%" if not pd.isna(avg_moisture) else "N/A")
with col_info8:
    avg_fc = df_category["固定碳"].mean()
    st.metric("🏭 平均固定碳", f"{avg_fc:.2f}%" if not pd.isna(avg_fc) else "N/A")

# ===============================
# 添加横线分隔
# ===============================
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ===============================
# 获取选中的物质数据
# ===============================
material_data = df_category[df_category["物质名称"] == selected_material].iloc[0]

# ===============================
# 创建两列布局 - 左右并排
# ===============================
col_left, col_right = st.columns([1.2, 1])

# ===============================
# 左列：物质详细分析模块
# ===============================
with col_left:
    # 显示当前选中的物质名称
    st.markdown(f'<div class="material-name-display">📋 当前分析物质: {selected_material}</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-title">物质详细分析模块</div>', unsafe_allow_html=True)

    # 使用标签页组织内容
    tab1, tab2, tab3, tab4 = st.tabs(["📊 综合分析", "⚛️ 元素分析", "🏭 工业分析", "🔥 热值分析"])

    with tab1:
        # 创建小卡片展示关键指标
        st.markdown('<h4 style="font-size: 18px !important;">🎯 关键指标</h4>', unsafe_allow_html=True)

        col_card1, col_card2, col_card3, col_card4 = st.columns(4)
        with col_card1:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #3498DB; font-size: 18px !important;">🌡️ 高位热值</h4>
                <h3 style="font-size: 22px !important;">{material_data.get('高位热值', 'N/A'):.2f} MJ/kg</h3>
            </div>
            """, unsafe_allow_html=True)

        with col_card2:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #E74C3C; font-size: 18px !important;">⚡ 挥发分</h4>
                <h3 style="font-size: 22px !important;">{material_data.get('挥发分', 'N/A'):.2f} %</h3>
            </div>
            """, unsafe_allow_html=True)

        with col_card3:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #2ECC71; font-size: 18px !important;">⚫ 灰分</h4>
                <h3 style="font-size: 22px !important;">{material_data.get('灰分', 'N/A'):.2f} %</h3>
            </div>
            """, unsafe_allow_html=True)

        with col_card4:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #9B59B6; font-size: 18px !important;">💧 水分</h4>
                <h3 style="font-size: 22px !important;">{material_data.get('水分', 'N/A'):.2f} %</h3>
            </div>
            """, unsafe_allow_html=True)

        # 添加雷达图
        st.markdown('<h4 style="font-size: 18px !important;">📡 元素分析雷达图</h4>', unsafe_allow_html=True)
        radar_fig = create_element_radar_chart(material_data, df_category, selected_material, selected_category)
        st.plotly_chart(radar_fig, use_container_width=True)

    with tab2:
        st.markdown('<h4 style="font-size: 20px !important;">⚛️ 元素分析组成 (wt%)</h4>', unsafe_allow_html=True)
        element_data = {
            "元素": ["C", "H", "O", "N", "S", "Cl", "Br"],
            "含量": [
                material_data.get("C", np.nan),
                material_data.get("H", np.nan),
                material_data.get("O", np.nan),
                material_data.get("N", np.nan),
                material_data.get("S", np.nan),
                material_data.get("Cl", np.nan),
                material_data.get("Br", np.nan)
            ]
        }
        element_df = pd.DataFrame(element_data)
        element_df["含量"] = element_df["含量"].round(3)

        # 使用表格和柱状图并排显示
        col_table, col_chart = st.columns([1, 1])

        with col_table:
            st.dataframe(element_df, use_container_width=True, hide_index=True)

        with col_chart:
            # 元素分布柱状图 - 使用用户指定的配色
            fig_elements = px.bar(
                element_df,
                x='元素',
                y='含量',
                title='元素分布',
                color='元素',
                text='含量',
                color_discrete_sequence=PIE_COLORS[:7]  # 使用用户指定的配色
            )
            fig_elements.update_traces(
                texttemplate='%{text:.2f}%',
                textposition='outside',
                marker=dict(line=dict(width=1, color='#2C3E50'))
            )
            fig_elements.update_layout(
                height=300,
                font=dict(size=14, family='Arial'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    title=dict(font=dict(size=14, color='#2C3E50')),
                    tickfont=dict(size=12, color='#2C3E50')
                ),
                yaxis=dict(
                    title=dict(font=dict(size=14, color='#2C3E50')),
                    tickfont=dict(size=12, color='#2C3E50')
                )
            )
            st.plotly_chart(fig_elements, use_container_width=True)

        # 添加元素选择饼图
        st.markdown('<h4 style="font-size: 18px !important;">🔍 自定义元素饼图</h4>', unsafe_allow_html=True)

        # 元素选择多选框
        all_elements = ["C", "H", "O", "N", "S", "Cl", "Br"]
        selected_elements = st.multiselect(
            "选择要在饼图中显示的元素",
            all_elements,
            default=["C", "H", "O", "N", "S"],
            help="勾选要显示的元素，饼图会实时更新"
        )

        if selected_elements:
            # 准备选中的元素数据
            selected_values = [material_data.get(e, 0) for e in selected_elements]
            selected_labels = []

            # 过滤掉值为0或NaN的元素
            valid_data = []
            for e, v in zip(selected_elements, selected_values):
                if not pd.isna(v) and v > 0:
                    valid_data.append((e, v))
                    selected_labels.append(f"{e}: {v:.2f}%")

            if valid_data:
                element_names, element_values = zip(*valid_data)

                # 创建饼图 - 使用用户指定的配色和立体效果
                fig_custom_pie = go.Figure(data=[go.Pie(
                    labels=selected_labels,
                    values=element_values,
                    hole=0.4,  # 更大的孔洞，更现代
                    marker=dict(
                        colors=PIE_COLORS[:len(valid_data)],
                        line=dict(color='#2C3E50', width=1.5)
                    ),
                    textinfo='label+percent',
                    textposition='inside',
                    hovertemplate="<b>%{label}</b><br>含量: %{value:.2f} wt%<br>占比: %{percent}",
                    pull=[0.05 for _ in range(len(valid_data))],  # 轻微分离效果
                    rotation=45,  # 旋转角度
                    direction='clockwise'  # 顺时针方向
                )])

                fig_custom_pie.update_layout(
                    title=dict(
                        text=f'{selected_material} 元素组成 (自定义)',
                        font=dict(size=16, color='#2C3E50', family='Arial')
                    ),
                    showlegend=False,
                    height=400,
                    font=dict(size=14, family='Arial'),
                    annotations=[dict(
                        text='元素组成',
                        x=0.5, y=0.5,
                        font=dict(size=16, color='#2C3E50'),
                        showarrow=False
                    )] if len(selected_elements) > 0 else None,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )

                st.plotly_chart(fig_custom_pie, use_container_width=True)
            else:
                st.warning("选择的元素没有有效数据")
        else:
            st.warning("请至少选择一个元素")

    with tab3:
        st.markdown('<h4 style="font-size: 20px !important;">🏭 工业分析组成 (wt%)</h4>', unsafe_allow_html=True)
        proximate_data = {
            "指标": ["固定碳", "挥发分", "水分", "灰分"],
            "含量": [
                material_data.get("固定碳", np.nan),
                material_data.get("挥发分", np.nan),
                material_data.get("水分", np.nan),
                material_data.get("灰分", np.nan)
            ]
        }
        proximate_df = pd.DataFrame(proximate_data)
        proximate_df["含量"] = proximate_df["含量"].round(3)

        # 并排显示表格和饼图
        col_table2, col_pie = st.columns([1, 1])

        with col_table2:
            st.dataframe(proximate_df, use_container_width=True, hide_index=True)

        with col_pie:
            if not proximate_df["含量"].isna().all():
                fig_proximate = px.pie(
                    proximate_df,
                    values='含量',
                    names='指标',
                    title='工业分析组成分布',
                    hole=0.4,
                    color_discrete_sequence=PIE_COLORS[:4]  # 使用用户指定的配色
                )
                fig_proximate.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    hovertemplate="<b>%{label}</b><br>含量: %{value:.2f}%<br>占比: %{percent}",
                    marker=dict(line=dict(color='#2C3E50', width=1.5)),
                    pull=[0.05, 0.05, 0.05, 0.05],
                    rotation=30
                )
                fig_proximate.update_layout(
                    height=300,
                    font=dict(size=14, family='Arial'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_proximate, use_container_width=True)

        # 添加工业分析雷达图
        st.markdown('<h4 style="font-size: 18px !important;">📡 工业分析雷达图</h4>', unsafe_allow_html=True)
        proximate_radar_fig = create_proximate_radar_chart(material_data, df_category, selected_material,
                                                           selected_category)
        st.plotly_chart(proximate_radar_fig, use_container_width=True)

    with tab4:
        st.markdown('<h4 style="font-size: 20px !important;">🔥 热值分析</h4>', unsafe_allow_html=True)
        heat_data = {
            "指标": ["高位热值", "低位热值"],
            "热值 (MJ/kg)": [
                material_data.get("高位热值", np.nan),
                material_data.get("低位热值", np.nan)
            ]
        }
        heat_df = pd.DataFrame(heat_data)
        heat_df["热值 (MJ/kg)"] = heat_df["热值 (MJ/kg)"].round(3)

        col_table3, col_chart2 = st.columns([1, 1])

        with col_table3:
            st.dataframe(heat_df, use_container_width=True, hide_index=True)

        with col_chart2:
            if not heat_df["热值 (MJ/kg)"].isna().all():
                fig_heat = px.bar(
                    heat_df,
                    x='指标',
                    y='热值 (MJ/kg)',
                    title='热值对比',
                    color='指标',
                    text='热值 (MJ/kg)',
                    color_discrete_sequence=['#BED2ED', '#DCE8BA']  # 使用用户指定的配色中的两种颜色
                )
                fig_heat.update_traces(
                    texttemplate='%{text:.2f} MJ/kg',
                    textposition='outside',
                    marker=dict(line=dict(width=1, color='#2C3E50'))
                )
                fig_heat.update_layout(
                    height=300,
                    font=dict(size=14, family='Arial'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(
                        title=dict(font=dict(size=14, color='#2C3E50')),
                        tickfont=dict(size=12, color='#2C3E50')
                    ),
                    yaxis=dict(
                        title=dict(font=dict(size=14, color='#2C3E50')),
                        tickfont=dict(size=12, color='#2C3E50')
                    )
                )
                st.plotly_chart(fig_heat, use_container_width=True)

# ===============================
# 右列：元素组成可视化模块
# ===============================
with col_right:
    # 显示当前选中的物质名称（右列也显示） - 修改图标为试管⚗️
    st.markdown(f'<div class="material-name-display">⚗️ 元素组成分析: {selected_material}</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="module-title">元素组成可视化模块</div>', unsafe_allow_html=True)

    # 准备元素数据
    elements = ["C", "H", "O", "N", "S", "Cl", "Br"]
    element_values = [material_data.get(e, 0) for e in elements]
    element_labels = []

    # 过滤掉值为0或NaN的元素
    for e, v in zip(elements, element_values):
        if not pd.isna(v) and v > 0:
            element_labels.append(f"{e}: {v:.2f}%")

    if element_labels:
        # 创建更美观的饼图 - 使用用户指定的配色和立体效果
        fig_pie = go.Figure(data=[go.Pie(
            labels=element_labels,
            values=[v for v in element_values if not pd.isna(v) and v > 0],
            hole=0.4,  # 更大的孔洞，更现代
            marker=dict(
                colors=PIE_COLORS[:len(element_labels)],
                line=dict(color='#2C3E50', width=1.5)
            ),
            textinfo='label+percent',
            textposition='inside',
            hovertemplate="<b>%{label}</b><br>含量: %{value:.2f} wt%<br>占比: %{percent}",
            pull=[0.05 for _ in range(len(element_labels))],  # 轻微分离效果，增加立体感
            rotation=45,  # 旋转角度
            direction='clockwise',  # 顺时针方向
            sort=False  # 不自动排序，保持原始顺序
        )])

        fig_pie.update_layout(
            title=dict(
                text=f'{selected_material} 元素组成',
                font=dict(size=18, color='#2C3E50', family='Arial')
            ),
            showlegend=False,
            height=400,
            font=dict(size=14, family='Arial'),
            annotations=[dict(
                text='元素组成',
                x=0.5, y=0.5,
                font=dict(size=16, color='#2C3E50'),
                showarrow=False
            )],
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("该物质缺少元素分析数据")

    # 添加元素组成表格
    st.markdown('<h4 style="font-size: 18px !important;">📝 元素组成明细</h4>', unsafe_allow_html=True)
    element_detail_df = pd.DataFrame({
        '元素': elements,
        '含量(%)': element_values
    })
    element_detail_df = element_detail_df[element_detail_df['含量(%)'] > 0]

    if not element_detail_df.empty:
        # 应用样式到表格
        styled_df = element_detail_df.style.format({'含量(%)': '{:.2f}'}) \
            .set_properties(**{
            'background-color': '#F8F9F9',
            'color': '#2C3E50',
            'border': '1px solid #D5DBDB'
        }) \
            .set_table_styles([{
            'selector': 'th',
            'props': [('background-color', '#34495E'),
                      ('color', 'white'),
                      ('font-weight', 'bold'),
                      ('border', '1px solid #2C3E50')]
        }])

        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )

# ===============================
# 添加横线分隔（全宽）
# ===============================
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ===============================
# 全宽模块：类别对比分析
# ===============================
st.markdown('<div class="module-title">📊 类别对比分析模块</div>', unsafe_allow_html=True)

st.markdown(f'<h2 style="font-size: 24px !important;">📊 {selected_category} 类别物质对比分析</h2>',
            unsafe_allow_html=True)

# 创建对比模块的选项卡
tab_comparison1, tab_comparison2, tab_comparison3 = st.tabs(["柱状图对比", "热力图分析", "散点图分析"])

with tab_comparison1:
    col_control, col_chart = st.columns([1, 3])

    with col_control:
        st.markdown('<h4 style="font-size: 18px !important;">⚙️ 对比设置</h4>', unsafe_allow_html=True)

        # 选择要对比的特性
        comparison_options = ["挥发分", "灰分", "水分", "固定碳", "C", "H", "O", "N", "高位热值"]
        selected_comparison = st.selectbox(
            "选择对比指标",
            comparison_options,
            index=0
        )

        # 选择排序方式
        sort_order = st.radio(
            "排序方式",
            ["降序", "升序"],
            horizontal=True
        )

        # 选择要突出显示的物质（多选）
        st.markdown('<h4 style="font-size: 18px !important;">🎯 突出显示物质</h4>', unsafe_allow_html=True)
        highlight_materials = st.multiselect(
            "选择要突出显示的物质",
            materials,
            default=[selected_material] if selected_material in materials else []
        )

        # 显示数量限制
        max_display = st.slider(
            "显示最大数量",
            min_value=5,
            max_value=min(30, len(materials)),
            value=15
        )

    with col_chart:
        # 准备对比数据
        comparison_data = df_category[["物质名称", selected_comparison]].copy()
        comparison_data = comparison_data.dropna(subset=[selected_comparison])

        if not comparison_data.empty:
            # 排序数据
            ascending = sort_order == "升序"
            comparison_data = comparison_data.sort_values(
                by=selected_comparison,
                ascending=ascending
            ).head(max_display)

            # 创建柱状图 - 使用顶刊渐变色
            fig_comparison = go.Figure()

            # 创建渐变色
            colorscale = selected_sequential
            norm_values = (comparison_data[selected_comparison] - comparison_data[selected_comparison].min()) / (
                        comparison_data[selected_comparison].max() - comparison_data[selected_comparison].min())

            # 添加所有物质的柱状图，使用渐变色
            colors = []
            for i, (_, row) in enumerate(comparison_data.iterrows()):
                if row["物质名称"] in highlight_materials:
                    colors.append('#E74C3C')  # 使用红色突出显示
                else:
                    # 使用渐变色
                    colors.append(px.colors.sequential.__dict__[colorscale][int(norm_values.iloc[i] * 7)])

            fig_comparison.add_trace(go.Bar(
                x=comparison_data["物质名称"],
                y=comparison_data[selected_comparison],
                name=selected_comparison,
                marker_color=colors,
                marker_line=dict(color='#2C3E50', width=1),
                hovertemplate="<b>%{x}</b><br>" + selected_comparison + ": %{y:.2f}<extra></extra>",
                text=comparison_data[selected_comparison].round(2),
                textposition='outside',
                textfont=dict(color='#2C3E50', size=12)
            ))

            # 更新图表布局
            fig_comparison.update_layout(
                title=dict(
                    text=f"{selected_category} - {selected_comparison} 对比",
                    font=dict(size=18, color='#2C3E50')
                ),
                xaxis_title=dict(
                    text="物质名称",
                    font=dict(size=14, color='#2C3E50')
                ),
                yaxis_title=dict(
                    text=f"{selected_comparison}" + (
                        " (wt%)" if selected_comparison not in ["高位热值"] else " (MJ/kg)"),
                    font=dict(size=14, color='#2C3E50')
                ),
                hovermode='x unified',
                showlegend=False,
                height=500,
                xaxis=dict(
                    tickangle=-45,
                    tickfont=dict(size=12, color='#2C3E50'),
                    gridcolor='#ECF0F1'
                ),
                yaxis=dict(
                    tickfont=dict(size=12, color='#2C3E50'),
                    gridcolor='#ECF0F1'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            # 添加平均值线
            avg_value = comparison_data[selected_comparison].mean()
            fig_comparison.add_hline(
                y=avg_value,
                line_dash="dash",
                line_color="#8B7355",  # 大地色
                line_width=2,
                annotation_text=f"平均值: {avg_value:.2f}",
                annotation_font=dict(size=12, color='#2C3E50'),
                annotation_bgcolor='rgba(255, 255, 255, 0.8)',
                annotation_bordercolor='#BDC3C7'
            )

            st.plotly_chart(fig_comparison, use_container_width=True)

            # 显示统计数据
            col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
            with col_stats1:
                st.metric("最大值", f"{comparison_data[selected_comparison].max():.2f}")
            with col_stats2:
                st.metric("最小值", f"{comparison_data[selected_comparison].min():.2f}")
            with col_stats3:
                st.metric("平均值", f"{avg_value:.2f}")
            with col_stats4:
                st.metric("标准差", f"{comparison_data[selected_comparison].std():.2f}")
        else:
            st.warning(f"该分类下没有足够的{selected_comparison}数据用于对比")

with tab_comparison2:
    st.markdown('<h4 style="font-size: 20px !important;">热力图分析</h4>', unsafe_allow_html=True)
    # 修改热力图的渐变色方案
    heatmap_data = df_category[['C', 'H', 'O', 'N', '固定碳', '挥发分', '灰分', '水分']]

    fig = px.imshow(
        heatmap_data.T,
        labels=dict(x="物质", y="指标", color="值"),
        x=df_category['物质名称'].tolist(),
        y=heatmap_data.columns.tolist(),
        color_continuous_scale=selected_gradient,  # 使用用户选择的渐变色
        aspect="auto"
    )

    fig.update_layout(
        title=dict(
            text=f"{selected_category} 热力图分析",
            font=dict(size=16, color='#2C3E50')
        ),
        height=400,
        font=dict(size=14),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "💡 热力图可以直观展示不同物质在各个指标上的数值分布，颜色越深表示数值越大。当前使用的渐变色方案为顶级期刊常用配色。")

with tab_comparison3:
    st.markdown('<h4 style="font-size: 20px !important;">散点图分析</h4>', unsafe_allow_html=True)

    col_scatter1, col_scatter2 = st.columns(2)

    with col_scatter1:
        x_axis = st.selectbox(
            "X轴指标",
            ["C", "H", "O", "固定碳", "挥发分"],
            key="x_axis"
        )

    with col_scatter2:
        y_axis = st.selectbox(
            "Y轴指标",
            ["高位热值", "灰分", "水分", "N", "S"],
            key="y_axis"
        )

    # 创建散点图
    scatter_data = df_category.dropna(subset=[x_axis, y_axis])

    if not scatter_data.empty:
        fig_scatter = px.scatter(
            scatter_data,
            x=x_axis,
            y=y_axis,
            color="物质名称",
            size="高位热值",
            hover_name="物质名称",
            title=f"{x_axis} vs {y_axis} 关系图",
            size_max=30,
            color_discrete_sequence=PIE_COLORS[:10]  # 使用用户指定的配色
        )

        # 添加趋势线
        fig_scatter.update_traces(
            marker=dict(
                line=dict(width=1, color='#2C3E50'),
                opacity=0.8
            )
        )

        # 计算相关系数
        correlation = scatter_data[x_axis].corr(scatter_data[y_axis])

        fig_scatter.update_layout(
            font=dict(size=14, family='Arial'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title=dict(font=dict(size=14, color='#2C3E50')),
                tickfont=dict(size=12, color='#2C3E50'),
                gridcolor='#ECF0F1'
            ),
            yaxis=dict(
                title=dict(font=dict(size=14, color='#2C3E50')),
                tickfont=dict(size=12, color='#2C3E50'),
                gridcolor='#ECF0F1'
            ),
            legend=dict(
                font=dict(size=12),
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='#BDC3C7'
            )
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.metric("相关系数", f"{correlation:.3f}")

        if abs(correlation) > 0.7:
            st.success(f"📈 {x_axis} 和 {y_axis} 有较强的相关性")
        elif abs(correlation) > 0.3:
            st.info(f"📊 {x_axis} 和 {y_axis} 有中等程度的相关性")
        else:
            st.warning(f"📉 {x_axis} 和 {y_axis} 相关性较弱")
    else:
        st.warning("没有足够的数据创建散点图")

# ===============================
# 添加横线分隔（全宽）
# ===============================
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ===============================
# 底部数据概览（简化版）
# ===============================
st.markdown('<div class="module-title">📈 数据库概览模块</div>', unsafe_allow_html=True)

st.markdown('<h2 style="font-size: 24px !important;">📈 数据库概览</h2>', unsafe_allow_html=True)

# 创建概览图表 - 只保留分类数量统计图
st.markdown('<h4 style="font-size: 20px !important;">各分类物质数量统计</h4>', unsafe_allow_html=True)

# 分类数量统计
category_counts = df["分类"].value_counts()
fig_categories = px.bar(
    x=category_counts.index,
    y=category_counts.values,
    title="各分类物质数量",
    labels={'x': '分类', 'y': '数量'},
    color=category_counts.values,
    color_continuous_scale=selected_overview_gradient  # 使用用户选择的数据库概览渐变色
)
fig_categories.update_layout(
    height=400,
    font=dict(size=14, family='Arial'),
    xaxis_tickangle=-45,
    xaxis=dict(
        tickfont=dict(size=12, color='#2C3E50'),
        title=dict(font=dict(size=14, color='#2C3E50'))
    ),
    yaxis=dict(
        tickfont=dict(size=12, color='#2C3E50'),
        title=dict(font=dict(size=14, color='#2C3E50'))
    ),
    coloraxis_colorbar=dict(
        title="物质数量",
        title_font=dict(size=12, color='#2C3E50'),
        tickfont=dict(size=11, color='#2C3E50')
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# 添加颜色条说明
st.markdown(
    f'<p style="font-size: 14px !important; color: #566573; text-align: center;">当前使用的渐变色方案: <b>{selected_overview_gradient}</b></p>',
    unsafe_allow_html=True)

st.plotly_chart(fig_categories, use_container_width=True)

# 添加一些统计数据
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
with col_stat1:
    st.metric("📁 总分类数", len(category_counts))
with col_stat2:
    st.metric("📦 总物质数", len(df))
with col_stat3:
    avg_hhv_all = df["高位热值"].mean()
    st.metric("🔥 全库平均高位热值", f"{avg_hhv_all:.2f} MJ/kg" if not pd.isna(avg_hhv_all) else "N/A")
with col_stat4:
    avg_ash_all = df["灰分"].mean()
    st.metric("⚫ 全库平均灰分", f"{avg_ash_all:.2f}%" if not pd.isna(avg_ash_all) else "N/A")

# ===============================
# 页脚
# ===============================
st.divider()
st.markdown("""
<div class="footer" style="text-align: center; color: #566573; padding: 20px;">
    <p style="font-size: 16px !important;">📚 <b>有机固废理化性质数据库</b> | 版本 1.0 
    <p style="font-size: 16px !important;">🎨 饼图配色: #BED2ED #DCE8BA #C3B3D0 #E6C6C4 #E6C48F #FCF8B9</p>
    <p style="font-size: 16px !important;">📊 数据库概览柱状图配色: <b>{selected_overview_gradient}</b></p>
    <p style="font-size: 16px !important;">💡 数据仅供参考，实际应用请结合具体实验验证</p>
</div>
""".format(selected_overview_gradient=selected_overview_gradient), unsafe_allow_html=True)
# 显示原始数据（可选）
with st.expander("📁 查看原始数据"):
    st.dataframe(df, use_container_width=True)