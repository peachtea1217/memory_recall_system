import urllib
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# 设置页面宽度为wide
st.set_page_config(layout="wide")

# 文件上传
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='utf-8')


def page_home():
    st.title('記憶想起支援システム')


    # 自定义CSS样式来调整容器宽度
    custom_style = """
    <style>
        body {
            max-width: 100%; /* 移除最大宽度限制 */
            margin: 0; /* 去除边距 */
            padding: 0; /* 去除内边距 */
            overflow-x: hidden; /* 隐藏水平滚动条 */
        }
    </style>
    """

    # 使用st.markdown嵌入自定义CSS样式
    st.markdown(custom_style, unsafe_allow_html=True)

    if uploaded_file is not None:
        # 创建一个控制器,来显示時系列
        container = st.container()
        container.write("時系列")

        time_series_columns = ['number', 'event', 'start_day', 'end_day', 'start_time', 'end_time', 'tag', 'person',
                               'SNS', 'place', 'num_photo']
        # 获取指定列的数据
        df_time_series = df[time_series_columns]
        # 将DataFrame的索引设置为一个不可见的列
        df_selected = df_time_series.reset_index(drop=True)

        # 修改索引，使序号从1开始
        df_selected.index = range(1, len(df) + 1)

        # 显示数据表
        st.dataframe(data=df_selected, column_config=None, width=700)

        # 形成词云

        # # 提取所需的文本数据
        # text_data = df.iloc[:3][['event', 'person', 'place']].values.tolist()  # 将"文本列名"替换为实际的列名
        #
        # # 将多行文本合并为一个字符串
        # combined_text = ' '.join([' '.join(row) for row in text_data])
        #
        # # MeCabのTaggerクラスのインスタンスを作成
        # tagger = MeCab.Tagger("-Owakati")
        #
        # # 使用 MeCab 分词
        # words = tagger.parse(combined_text).split()
        #
        # # 生成词云
        # wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))
        #
        # # 绘制词云图像
        # plt.figure(figsize=(10, 5))
        # plt.imshow(wordcloud, interpolation='bilinear')
        # plt.axis('off')
        # plt.tight_layout()
        #
        # # 显示词云图像
        # st.pyplot()

        # # 提取指定列的文本内容
        # columns_to_extract = ['event', 'person', 'place']  # 用您的实际列名替代
        # extracted_text = ""  # 创建空数据串用于承接文本
        # # 将所有文本连接起来
        # for column in columns_to_extract:
        #     extracted_text += ' '.join(df[column].astype(str))
        #
        # # 指定支持的 TrueType 字体路径
        # font_path = "/Users/wangsihan/Downloads/851H-kktt_004.ttf"
        #
        # wc = WordCloud(
        #     # font_path=st.selectbox("请选择一种字体", (ziti)),
        #     background_color='white',  # 背景颜色
        #     width=1000,
        #     height=1000,
        #     max_font_size=80,  # 字体大小
        #     min_font_size=1,
        #     # mask=plt.imread(st.selectbox("请选择一种轮廓图", (lunkuo))),  # 背景图片
        #     max_words=10000
        # )
        # wc.generate(" ".join(extracted_text))
        # wc.to_file('ciyun.png')
        #
        # # 生成词云
        # wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(extracted_text))
        #
        # # 使用 Matplotlib 绘制词云图像
        # plt.figure(figsize=(10, 5))
        # plt.imshow(wordcloud, interpolation='bilinear')
        # plt.axis('off')  # 不显示坐标轴
        # plt.tight_layout()
        #
        # # 将词云图像显示在 Streamlit 应用中
        # st.pyplot()


        # 提取所需的三列日语文本数据
        text_data = df[['event', 'person', 'place']].astype(str).values.flatten()

        # 使用Janome进行形态素解析，并只保留名词
        def extract_nouns(text):
            t = Tokenizer()
            nouns = [token.surface for token in t.tokenize(text) if token.part_of_speech.startswith('名詞')]
            return ' '.join(nouns)

        processed_text = [extract_nouns(text) for text in text_data]

        # 将名词文本数据合并为一个字符串
        combined_text = ' '.join(processed_text)

        # 指定TrueType字体文件路径，替换为你自己的字体文件路径
        font_path = '/Users/wangsihan/Downloads/851H-kktt_004.ttf'

        # 使用WordCloud生成词云，指定字体路径
        wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(
            combined_text)

        # 显示词云图
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()


def sorted(sort_column, output_columns):
    # 执行从大到小的排序
    if isinstance(sort_column, list) and len(sort_column) == 3:
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=[False, True, True])

    elif isinstance(sort_column, list) and len(sort_column) == 2:
        # 按照指定列的数据大小重新排列
        df_sorted = df.sort_values(by=sort_column, ascending=[False, False])

    # 获取指定列的数据
    df_select = df_sorted[output_columns]
    # 将DataFrame的索引设置为一个不可见的列
    df_ranking = df_select.reset_index(drop=True)

    # 修改索引，使序号从1开始
    df_ranking.index = range(1, len(df) + 1)

    # 显示数据表
    st.dataframe(data=df_ranking, width=700)


def line_chart(predicted_score, actual_score):
    # 创建 Matplotlib 折线图
    fig, ax = plt.subplots()
    ax.plot(df["number"], df[predicted_score], label="Predicted Score")
    ax.plot(df["number"], df[actual_score], label="Actual Score")
    ax.set_xlabel("event number")
    ax.set_ylabel("Score")
    ax.set_title("Event Scores")
    ax.legend()

    # 将 Matplotlib 图表显示在 Streamlit 中
    st.pyplot(fig)

    # 直接用本来带的line chart功能
    st.line_chart(
        data=df,  # 数据来源
        x='event',
        y=[predicted_score, actual_score],
        width=700,
        height=500
    )

    # 创建 Plotly 折线图
    fig = px.line(df, x="event", y=[predicted_score, actual_score], title="Event Scores")
    fig.update_layout(xaxis_title="Event Name", yaxis_title="Score", width=700, height=700)

    # 将 Plotly 图表显示在 Streamlit 中
    st.plotly_chart(fig)

    # 创建 Plotly 折线图2

    # 获取事件名称的唯一值并按照表格数据的顺序排列
    unique_events = list(dict.fromkeys(df['event']))

    # 创建两个折线对象
    line1 = go.Scatter(x=df['event'], y=df[predicted_score], mode='lines+markers', name='Line 1')
    line2 = go.Scatter(x=df['event'], y=df[actual_score], mode='lines+markers', name='Line 2')

    # 创建图表布局
    layout = go.Layout(
        title='Two Lines Chart',
        xaxis_title='Event Name',
        yaxis_title='Score',
        xaxis=dict(rangeslider=dict(visible=True)),  # 添加 x 轴的范围滑块
        width=700,
        height=700
    )

    # 创建图表
    fig = go.Figure(data=[line1, line2], layout=layout)

    # 设置 x 轴的唯一值顺序
    fig.update_xaxes(categoryorder='array', categoryarray=unique_events)

    # 在 Streamlit 中显示 Plotly 图表
    st.plotly_chart(fig)

def page_ranking():
    # ランキング
    option_ranking = st.selectbox(
        'ランキング方式を選んでください',
        ('人物のランキング', '場所のランキング', 'イベントのランキング'))

    st.write('You selected:', option_ranking)

    # 将用户选择的排序方式，转化为文件中的列名
    if option_ranking == '人物のランキング':
        # 指定人物のランキング出现的列
        sort_column = ['weight_person', 'person', 'number']
        person_ranking_columns = ['number', 'event', 'start_day', 'end_day', 'start_time', 'end_time', 'tag', 'person',
                               'SNS', 'place', 'num_photo']
        sorted(sort_column, person_ranking_columns)

    elif option_ranking == '場所のランキング':
        sort_column = ['weight_place', 'place', 'number']
        place_ranking_columns = ['number', 'event', 'start_day', 'end_day', 'start_time', 'end_time', 'tag', 'person',
                               'SNS', 'place', 'num_photo']
        sorted(sort_column, place_ranking_columns)

    else:
        sort_column = ['weight_event', 'number']
        event_ranking_columns = ['number', 'event', 'start_day', 'end_day', 'start_time', 'end_time', 'tag', 'person',
                               'SNS', 'place', 'num_photo']
        sorted(sort_column, event_ranking_columns)



def page_sequence():
    # 想起に役に立つ順
    option_sequence = st.selectbox(
        '想起に役に立つ順',
        ('「思い出したい」順', '「重要」順', '「幸せな気分」順'))

    st.write('You selected:', option_sequence)

    # 将用户选择的排序方式，转化为文件中的列名
    if option_sequence == '「思い出したい」順':
        # 指定人物のランキング出现的列
        sort_column = 'weight_remember'
        person_ranking_columns = ['number', 'event', 'start_day', 'end_day', 'person', 'place']
        # 折线图
        predicted_score = 'weight_remember'
        actual_score = 'remember'
        sorted(sort_column, person_ranking_columns)
        line_chart(predicted_score, actual_score)


    # elif option_sequence == '「重要」順':
    #     sort_column = 'weight_important'
    #     place_ranking_columns = ['number', 'event', 'start_day', 'end_day', 'person', 'place']
    #     # 折线图
    #     predicted_score = 'weight_important'
    #     actual_score = 'important'
    #     sorted(sort_column, place_ranking_columns)
    #     line_chart(predicted_score, actual_score)
    #
    # elif option_sequence == '「幸せな気分」順':
    #     sort_column = 'weight_happy'
    #     event_ranking_columns = ['number', 'event', 'start_day', 'end_day', 'person', 'place']
    #     # 折线图
    #     predicted_score = 'weight_happy'
    #     actual_score = 'happy'
    #     sorted(sort_column, event_ranking_columns)
    #     line_chart(predicted_score, actual_score)



# 在边栏中添加导航链接
add_selectbox = st.sidebar.selectbox(
    "記憶想起支援システム",
    ("ホームページ", "ランキング", "想起に役に立つ順")
)

# 根据导航选择展示不同页面内容
if add_selectbox == "ホームページ":
    page_home()
elif add_selectbox == "ランキング":
    page_ranking()
elif add_selectbox == "想起に役に立つ順":
    page_sequence()


# 创建一个文本框用于输入搜索词，放在边栏中
search_term = st.sidebar.text_input("キーワード検索：", "")

# 选择需要搜索的列
search_columns = ['event', 'person', 'place']

def page_search(search_results):
    st.write("搜索结果：")
    st.write(search_results)

# 检查用户是否输入了搜索词
if search_term:
    # 初始化一个空的DataFrame，用于存储搜索结果
    search_results = pd.DataFrame()

    # 在选择的列中搜索关键词
    for column in search_columns:
        results = df[df[column].str.contains(search_term, case=False, na=False)]
        print(f"results:{results}\n")
        search_results = pd.concat([search_results, results])

    # 如果找到了匹配的结果
    if not search_results.empty:
        page_search(search_results)
    else:
        st.warning("没有找到对应关键词的数据")

        # 在没有结果的情况下，显示“没有找到对应关键词的数据”，并提供一个返回按钮
        if st.button("返回"):
            # 构建新页面的URL参数，这里没有任何参数，只是跳回到原始页面
            new_page_params = {}
            new_page_url = st.experimental_get_query_params()
            new_page_url.update(new_page_params)

            # 构建新页面的URL
            new_page_url_encoded = urllib.parse.urlencode(new_page_url)
            new_url = f"current_page?{new_page_url_encoded}"
            st.experimental_set_query_params(**new_page_url)
            st.markdown(f"正在跳转到新页面：[返回原页面]({new_url})")