# -*- coding: utf-8 -*-
"""
CrossBorder Insight —— 出海竞品情报与行业洞察分析平台
=====================================================
适用场景：出海咨询 / 竞品情报分析
运行方式：
    pip install streamlit pandas plotly openpyxl
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ========== 新增：自定义导航栏样式 ==========
st.markdown("""
<style>
    /* 侧边栏整体加宽，给中英文留空间 */
    [data-testid="stSidebar"] {
        min-width: 300px !important;
        max-width: 300px !important;
    }

    /* radio 每个选项的 label：放大字体、支持换行、增加间距 */
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label {
        font-size: 16px !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
        white-space: pre-line !important;   /* 让 \n 生效 */
        padding: 10px 0px !important;
        margin-bottom: 4px !important;
        border-radius: 6px !important;
    }

    /* 鼠标悬停高亮 */
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label:hover {
        background-color: #f0f2f6;
    }

    /* 去掉 radio 自带的小圆圈和文字的间隙过大的问题 */
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label > div:first-child {
        align-self: flex-start !important;
        margin-top: 6px !important;
    }
</style>
""", unsafe_allow_html=True)
# ===========================================
# ----------------------------------------------------------------------------
# 一、数据初始化（直接定义 DataFrame，无需外部 CSV 文件）
# ----------------------------------------------------------------------------

# 30 家中国出海企业的公开数据
# 字段顺序：name, sector, target_markets, founded_year, funding_stage,
#           total_funding_usd, core_product, product_maturity, team_score, localization
companies_raw = [
    ["SHEIN",       "跨境电商",   "欧美/中东/拉美",      2008, "E轮+",  2000, "快时尚电商",   5, 4, 5],
    ["Anker",       "跨境电商",   "北美/欧洲/日本",      2011, "已上市",  500, "消费电子",     5, 4, 5],
    ["PatPat",      "跨境电商",   "北美/欧洲",           2014, "D轮",    700, "母婴电商",     4, 3, 4],
    ["Cider",       "跨境电商",   "欧美/东南亚",         2020, "B轮",    400, "快时尚电商",   4, 3, 4],
    ["米哈游",      "游戏出海",   "全球",               2012, "未上市",    0, "游戏研发发行", 5, 5, 4],
    ["莉莉丝游戏",  "游戏出海",   "全球",               2013, "未上市",    0, "游戏研发发行", 5, 4, 4],
    ["三七互娱",    "游戏出海",   "东南亚/日韩/欧美",    2011, "已上市",    0, "游戏发行",     4, 4, 3],
    ["沐瞳科技",    "游戏出海",   "东南亚/中东/拉美",    2014, "被收购",    0, "MOBA游戏",     4, 4, 5],
    ["汇量科技",    "SaaS/企业服务", "全球",            2013, "已上市",  300, "移动广告平台", 4, 4, 4],
    ["声网Agora",   "SaaS/企业服务", "全球",            2014, "已上市",  200, "实时音视频云", 4, 5, 4],
    ["涂鸦智能",    "SaaS/企业服务", "全球",            2014, "已上市",  900, "IoT云平台",   4, 4, 4],
    ["有赞",        "SaaS/企业服务", "东南亚",          2012, "已上市",  400, "电商SaaS",     4, 3, 3],
    ["蚂蚁国际",    "金融科技",   "东南亚/南亚/欧洲",    2015, "未上市",    0, "跨境支付",     5, 5, 5],
    ["连连数字",    "金融科技",   "全球",               2009, "已上市",  300, "跨境支付",     4, 4, 4],
    ["Airwallex",   "金融科技",   "全球",               2015, "E轮+",    900, "跨境支付",     4, 4, 5],
    ["TikTok",      "社交内容",   "全球",               2016, "未上市",    0, "短视频社交",   5, 5, 5],
    ["欢聚集团",    "社交内容",   "东南亚/中东/拉美",    2005, "已上市",    0, "直播社交",     4, 4, 4],
    ["赤子城科技",  "社交内容",   "中东/东南亚/欧美",    2009, "已上市",  200, "社交应用",     4, 3, 4],
    ["传音控股",    "硬件/IoT",   "非洲/南亚/拉美",      2006, "已上市",    0, "智能手机",     5, 4, 5],
    ["大疆创新",    "硬件/IoT",   "全球",               2006, "未上市",    0, "无人机",       5, 5, 5],
    ["九号公司",    "硬件/IoT",   "欧美/亚太",           2012, "已上市",  300, "智能出行",     4, 4, 4],
    ["极兔速递",    "物流/供应链", "东南亚/中东/拉美",   2015, "E轮+",  2000, "跨境物流",     5, 4, 4],
    ["菜鸟国际",    "物流/供应链", "全球",              2013, "未上市",    0, "跨境物流",     5, 5, 4],
    ["纵腾集团",    "物流/供应链", "欧美",              2007, "D轮",   1000, "海外仓物流",   4, 3, 4],
    ["名创优品",    "新零售",     "全球",               2013, "已上市",    0, "生活家居零售", 5, 4, 5],
    ["泡泡玛特",    "新零售",     "亚太/欧美",           2010, "已上市",    0, "潮流玩具",     5, 4, 4],
    ["瑞幸咖啡",    "新零售",     "东南亚",             2017, "已上市",    0, "咖啡连锁",     4, 4, 3],
    ["晶科能源",    "新能源",     "全球",               2006, "已上市",    0, "光伏组件",     5, 4, 4],
    ["宁德时代",    "新能源",     "全球",               2011, "已上市",    0, "动力电池",     5, 5, 4],
    ["比亚迪",      "新能源",     "全球",               1995, "已上市",    0, "新能源汽车",   5, 5, 4],
]

# 组建企业 DataFrame
df = pd.DataFrame(
    companies_raw,
    columns=[
        "name", "sector", "target_markets", "founded_year", "funding_stage",
        "total_funding_usd", "core_product", "product_maturity", "team_score", "localization",
    ],
)

# 融资记录 DataFrame（用于融资趋势图），至少 10 条
funding_rounds = pd.DataFrame(
    [
        ["SHEIN",     "E轮", 1000, 2022, "General Atlantic"],
        ["Anker",     "D轮", 300,  2020, "红杉资本"],
        ["PatPat",    "D轮", 400,  2021, "泛大西洋投资"],
        ["Cider",     "B轮", 100,  2021, "DST Global"],
        ["涂鸦智能",  "C轮", 200,  2020, "NEA"],
        ["Airwallex", "E轮", 300,  2022, "Lone Pine Capital"],
        ["极兔速递",  "E轮", 600,  2021, "高瓴资本"],
        ["纵腾集团",  "D轮", 500,  2021, "华兴资本"],
        ["声网Agora", "D轮", 150,  2019, "经纬中国"],
        ["汇量科技",  "C轮", 100,  2019, "摩根士丹利"],
    ],
    columns=["company", "round", "amount_usd", "year", "investor"],
)

# 目标市场列表（用于页面下拉框）
MARKET_OPTIONS = ["东南亚", "中东", "欧美", "拉美", "非洲", "日韩", "南亚"]

# ----------------------------------------------------------------------------
# 二、通用工具函数（含中文注释）
# ----------------------------------------------------------------------------

def split_markets(target_markets: str):
    """把用 '/' 分隔的目标市场字符串拆成列表，例如 '欧美/中东' -> ['欧美', '中东']"""
    return [m.strip() for m in target_markets.split("/") if m.strip()]


def funding_score(funding_usd: float):
    """根据累计融资额（百万美元）把融资能力映射为 1-5 分"""
    if funding_usd >= 1000:
        return 5
    elif funding_usd >= 500:
        return 4
    elif funding_usd >= 200:
        return 3
    elif funding_usd >= 100:
        return 2
    else:
        return 1


def market_coverage_score(target_markets: str):
    """根据目标市场数量（覆盖国家/地区数）映射为 1-5 分"""
    count = len(split_markets(target_markets))
    if count >= 3:
        return 5
    elif count == 2:
        return 3
    else:
        return 1


# ----------------------------------------------------------------------------
# 三、页面配置与侧边栏导航
# ----------------------------------------------------------------------------

st.set_page_config(page_title="CrossBorder Insight", layout="wide")

# 页面标题与副标题
# st.title("🌍 CrossBorder Insight")
# st.caption("出海竞品情报与行业洞察分析平台")

# 侧边栏导航（5 个页面切换）
# page = st.sidebar.radio(
#     "导航菜单",
#     ["行业概览", "竞品情报库", "竞品对标分析", "市场进入策略", "报告中心"],
# )
with st.sidebar:
    st.title("CrossBorder Insight")
    st.caption("出海竞品情报与行业洞察分析平台")
    st.markdown("---")

    # 中英文导航选项（\n 会在 CSS 作用下变成换行）
    menu_options = [
        "行业概览\nIndustry Overview",
        "竞品情报库\nCompany Intelligence",
        "竞品对标分析\nCompetitive Benchmark",
        "市场进入策略\nMarket Entry Strategy",
        "报告中心\nReport Center"
    ]

    # label_visibility="collapsed" 隐藏默认的"导航菜单"小标题，更干净
    selected = st.sidebar.radio(
        "导航菜单",
        menu_options,
        label_visibility="collapsed"
    )

    # 把选中的中文部分提取出来，用于后续 if 判断
    page = selected.split("\n")[0].replace("📊 ", "").replace("🏢 ", "").replace("⚔️ ", "").replace("🌏 ", "").replace(
        "📄 ", "")

# 侧边栏底部预留 screenshots 目录引用（后续可放截图）
st.sidebar.markdown("---")
st.sidebar.caption("截图存放目录：`screenshots/`（项目根目录下）")


# ----------------------------------------------------------------------------
# 四、页面 1：行业概览 Dashboard
# ----------------------------------------------------------------------------
if page == "行业概览":
    st.subheader("📊 行业概览")
    st.caption("基于 30 家中国出海企业公开数据，辅助市场进入决策")

    # 4 个 KPI 指标卡片
    total_companies = len(df)                                  # 企业总数
    total_funding_bw = df["total_funding_usd"].sum() / 100     # 总融资额（亿美元）
    avg_funding_m = df["total_funding_usd"].mean()             # 平均融资额（百万美元）
    sector_count = df["sector"].nunique()                      # 赛道数量

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("企业总数", f"{total_companies} 家")
    col2.metric("总融资额", f"{total_funding_bw:.1f} 亿美元")
    col3.metric("平均融资额", f"{avg_funding_m:.1f} 百万美元")
    col4.metric("赛道数量", f"{sector_count} 个")

    st.divider()

    # 赛道分布：饼图
    sector_counts = df["sector"].value_counts().reset_index()
    sector_counts.columns = ["sector", "count"]

    # 计算一条过质心、按占比切分的饼图
    fig_pie = px.pie(sector_counts, names="sector", values="count",
                     title="赛道分布")
    st.plotly_chart(fig_pie, use_container_width=True)

    # 目标市场热度：横向柱状图（拆分 target_markets，统计市场出现次数 Top 10）
    market_count = {}
    for markets in df["target_markets"]:
        for m in split_markets(markets):
            market_count[m] = market_count.get(m, 0) + 1
    market_df = pd.DataFrame(
        sorted(market_count.items(), key=lambda x: x[1], reverse=True)[:10],
        columns=["market", "count"],
    )
    fig_bar = px.bar(market_df, x="count", y="market", orientation="h",
                     title="目标市场热度 Top 10")
    st.plotly_chart(fig_bar, use_container_width=True)

    # 融资趋势：折线图（按年份聚合 funding_rounds 的金额）
    trend_df = funding_rounds.groupby("year")["amount_usd"].sum().reset_index()
    fig_line = px.line(trend_df, x="year", y="amount_usd", markers=True,
                       title="融资趋势（按年份融资总额，百万美元）")
    fig_line.update_xaxes(tickformat="d")
    st.plotly_chart(fig_line, use_container_width=True)


# ----------------------------------------------------------------------------
# 五、页面 2：竞品情报库
# ----------------------------------------------------------------------------
elif page == "竞品情报库":
    st.subheader("🔎 竞品情报库")
    st.caption("筛选并查看 30 家中国出海企业的竞品情报")

    # 顶部 3 个筛选器
    filter_sector = st.multiselect("赛道", df["sector"].unique().tolist())
    filter_market = st.multiselect("目标市场", MARKET_OPTIONS)
    filter_stage = st.selectbox("融资阶段", ["全部"] + df["funding_stage"].unique().tolist())

    # 应用筛选
    filtered = df.copy()
    if filter_sector:
        filtered = filtered[filtered["sector"].isin(filter_sector)]
    if filter_market:
        filtered = filtered[
            filtered["target_markets"].apply(
                lambda x: any(m in split_markets(x) for m in filter_market)
            )
        ]
    if filter_stage != "全部":
        filtered = filtered[filtered["funding_stage"] == filter_stage]

    st.caption(f"共筛选出 {len(filtered)} 家企业")

    # 企业表格（含基础字段）
    st.dataframe(
        filtered[["name", "sector", "target_markets", "funding_stage", "total_funding_usd"]],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.markdown("#### 点击下方企业查看详情")

    # 每家企业一个 expander 展开详情
    for _, row in filtered.iterrows():
        with st.expander(f"{row['name']} ｜ {row['sector']}"):
            st.write(f"**成立年：** {row['founded_year']}")
            st.write(f"**核心产品：** {row['core_product']}")

            # 三维度评分（用 st.progress 展示 0-5 分）
            st.write("**三维度评分：**")
            st.write(f"产品成熟度：{row['product_maturity']} / 5")
            st.progress(int(row["product_maturity"]) / 5)
            st.write(f"团队背景：{row['team_score']} / 5")
            st.progress(int(row["team_score"]) / 5)
            st.write(f"本地化程度：{row['localization']} / 5")
            st.progress(int(row["localization"]) / 5)


# ----------------------------------------------------------------------------
# 六、页面 3：竞品对标分析（核心功能）
# ----------------------------------------------------------------------------
elif page == "竞品对标分析":
    st.subheader("⚔️ 竞品对标分析")
    st.caption("选择两家企业，用雷达图对比 5 个维度，自动生成文字结论")

    company_names = df["name"].tolist()
    col_a, col_b = st.columns(2)
    company_a = col_a.selectbox("企业 A", company_names)
    company_b = col_b.selectbox("企业 B", company_names, index=1)

    # 取出两家的数据
    a = df[df["name"] == company_a].iloc[0]
    b = df[df["name"] == company_b].iloc[0]

    # 5 个维度得分（融资能力、市场覆盖度用函数换算成 1-5 分）
    dims = ["产品成熟度", "团队背景", "本地化程度", "融资能力", "市场覆盖度"]
    a_scores = [
        a["product_maturity"],
        a["team_score"],
        a["localization"],
        funding_score(a["total_funding_usd"]),
        market_coverage_score(a["target_markets"]),
    ]
    b_scores = [
        b["product_maturity"],
        b["team_score"],
        b["localization"],
        funding_score(b["total_funding_usd"]),
        market_coverage_score(b["target_markets"]),
    ]

    # 雷达图
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=a_scores + [a_scores[0]], theta=dims + [dims[0]],
        fill="toself", name=company_a,
    ))
    fig.add_trace(go.Scatterpolar(
        r=b_scores + [b_scores[0]], theta=dims + [dims[0]],
        fill="toself", name=company_b,
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        title=f"{company_a} vs {company_b} 五维对标",
        showlegend=True,
    )
    st.plotly_chart(fig, use_container_width=True)

    # 自动生成文字结论（if-else 逻辑拼接）
    conclusion = ""
    if a_scores[0] > b_scores[0]:
        conclusion += f"{company_a} 在产品成熟度上领先，"
    else:
        conclusion += f"{company_b} 在产品成熟度上领先，"
    if a_scores[2] > b_scores[2]:
        conclusion += f"但 {company_b} 在本地化程度方面更弱，其本地化得分为 {b_scores[2]}。"
    else:
        conclusion += f"而 {company_b} 本地化程度更高（{b_scores[2]} 分）。"
    if a_scores[3] > b_scores[3]:
        conclusion += f"融资能力上 {company_a} 更强，资金储备更充足。"
    else:
        conclusion += f"融资能力上 {company_b} 更强，资金储备更充足。"
    conclusion += "建议结合目标市场的具体需求，差异化定位，取长补短。"
    st.markdown("#### 💡 分析结论")
    st.success(conclusion)


# ----------------------------------------------------------------------------
# 七、页面 4：市场进入策略（核心功能）
# ----------------------------------------------------------------------------
elif page == "市场进入策略":
    st.subheader("🏙️ 市场进入策略")
    st.caption("选择目标市场，输出结构化洞察与进入建议")

    market = st.selectbox("目标市场", MARKET_OPTIONS)

    # 筛选进入该市场的企业
    in_market = df[df["target_markets"].apply(lambda x: market in split_markets(x))]
    cnt = len(in_market)

    if cnt == 0:
        st.warning(f"当前数据集中没有企业明确标注进入「{market}」市场。")
    else:
        avg_funding = in_market["total_funding_usd"].mean()
        # 主要赛道分布
        sector_dist = in_market["sector"].value_counts().reset_index()
        sector_dist.columns = ["sector", "count"]

        # 融资热度：统计涉及该市场企业的融资事件数量
        funding_hot = funding_rounds[
            funding_rounds["company"].isin(in_market["name"].tolist())
        ].shape[0]

        # 卡片式布局
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("进入企业数", f"{cnt} 家")
        col2.metric("平均融资额", f"{avg_funding:.1f} 百万美元")
        col3.metric("融资事件数", f"{funding_hot} 起")
        col4.metric("主要赛道数", f"{in_market['sector'].nunique()} 个")

        st.divider()

        # 主要赛道分布（饼图）
        fig_market_pie = px.pie(sector_dist, names="sector", values="count",
                                title=f"「{market}」主要赛道分布")
        st.plotly_chart(fig_market_pie, use_container_width=True)

        # 详细赛道列表
        st.markdown("#### 赛道明细")
        for _, r in sector_dist.iterrows():
            st.write(f"- **{r['sector']}**：{r['count']} 家")

        st.divider()

        # 进入建议（根据数据自动生成）
        st.markdown("#### 💡 进入建议")
        ecom_cnt = in_market[in_market["sector"].str.contains("电商")].shape[0]
        if ecom_cnt > 0:
            advice = (f"该市场已有 {ecom_cnt} 家电商类企业，竞争较为激烈，"
                      f"建议在定位上差异化（如更细分的品类或本地化服务）。")
        elif cnt >= 5:
            advice = f"该市场已有 {cnt} 家中国企业进入，建议避开红海，寻找细分赛道切入。"
        else:
            advice = (f"该市场中国企业进入较少（{cnt} 家），存在一定空白机会，"
                      f"可考虑先发卡位。")
        st.info(advice)


# ----------------------------------------------------------------------------
# 八、页面 5：报告中心
# ----------------------------------------------------------------------------
elif page == "报告中心":
    st.title("🌍 CrossBorder Insight")
    st.caption("出海竞品情报与行业洞察分析平台")
    st.subheader("📄 报告中心")
    st.caption("一键生成 Markdown 格式的竞品分析报告并下载")

    if st.button("生成报告"):
        # 基础统计
        total = len(df)
        sectors = df["sector"].nunique()
        total_funding = df["total_funding_usd"].sum() / 100

        # 按赛道聚合融资 Top 5
        sector_funding = (
            df.groupby("sector")["total_funding_usd"].sum()
            .sort_values(ascending=False).head(5)
        ).reset_index()

        # 融资最多的前 3 家企业
        top_funded = (
            df.sort_values("total_funding_usd", ascending=False).head(3)
        )[["name", "sector", "total_funding_usd"]]

        # 用字符串拼接生成 Markdown 报告
        report = f"""# 中国出海企业竞品分析报告

> 由 CrossBorder Insight 自动生成

## 一、执行摘要
本报告基于 {total} 家中国出海企业的公开数据，覆盖 {sectors} 个赛道，"
累计融资约 {total_funding:.1f} 亿美元。整体来看，中国企业在跨境电商、"
游戏出海、新能源、硬件等赛道已形成较强的全球竞争力。

## 二、行业概况
- 企业总数：{total}
- 赛道数量：{sectors}
- 总融资额：{total_funding:.1f} 亿美元

### 主要赛道融资分布
"""
        for _, r in sector_funding.iterrows():
            report += f"- {r['sector']}：{r['total_funding_usd']} 百万美元\n"

        report += "\n## 三、重点竞品分析\n"
        for _, r in top_funded.iterrows():
            report += (
                f"- **{r['name']}**（{r['sector']}）："
                f"累计融资 {r['total_funding_usd']} 百万美元\n"
            )

        report += "\n## 四、市场进入建议\n"
        report += (
            "- 已进入全球市场（标注为“全球”）的企业较多，说明这些赛道已高度国际化。\n"
            "- 对新兴市场（东南亚、中东、拉美）投放资源的企业，多为电商、游戏、物流等赛道，"
            "本地化程度较高。\n"
            "- 建议结合目标市场的监管、文化与消费习惯，选择差异化定位，避免同质化竞争。\n"
        )

        report += "\n## 五、结论\n"
        report += (
            "中国出海企业在产品成熟度、团队背景、本地化等方面整体表现优秀。"
            "未来应进一步深耕本地化服务，同时关注新兴市场的先发机遇。\n"
        )

        # 展示报告并下载
        st.markdown(report)
        st.download_button(
            "下载 Markdown 报告",
            data=report,
            file_name="crossborder_insight_report.md",
            mime="text/markdown",
        )
