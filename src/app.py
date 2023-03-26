import os
import pathlib

import dash
# import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import dash_daq as daq

import pandas as pd
import pickle


import webbrowser
from threading import Timer


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Text-based Financial Indices Hub!"
server = app.server
app.config["suppress_callback_exceptions"] = True

APP_PATH = os.getcwd() #str(pathlib.Path(__file__).parent.resolve())
df = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "spc_data.csv")))



#========================================================

# from src.analyst_report_py37 import *
from src.dash_graphs_py37_public import *

# AR = AnalystReport(beg_date='20221201', end_date='20221212')
# # AR.tokenizing(load=True)
# # AR.predictLabs(load=True)
# # AR.connectToPastDat(past_dat_sents_labs_files=['dat_sents_labs_20190101_20221031.pkl',
# #                                                'dat_sents_labs_20221101_20221130.pkl'])

AR = AnalystReportShell()
DG = DashGraphs(AR)

# MA = MarketAnalysis(AR)
# MA.period = 'quarter'


#========================================================


periods = ['quarter','month']
KRXfields = ['코스피','전기전자','화학','금융업','의약품','운수장비','음식료품','전기가스업','건설업','기계']
KRXfields_ENG = ['KOSPI','Electrical & Electronic Equip.','Chemicals','Finance','Medical Supplies','Transport Equipment','Foods & Beverages','Electricity & Gas','Construction','Machinery']
ARfields = ['전체','전자/영상/통신장비등','화학물질/제품','금융','의료물질/의약품',['자동차', '조선/기타운수'],'식료품','전기/가스/증기','건설업','기타기계/장비']
ARfields_ENG = ['All-industry','Electronic components, computer, radio, television and communication equipment and apparatuses','Chemicals and chemical products','Finance','Pharmaceuticals, medicinal chemicals and botanical products','Motor vehicles, trailers and semitrailers & Other transport equipment','Food products','Electricity, gas, steam and air conditioning supply','Construction','Other machinery and equipment']
fieldtypes = [3,1,1,1,1,2,1,1,1,1]

TFItopics = ['생산','선박','자동차','반도체','설비투자','건설투자','실업','채용','구직','도소매','정부지출','물가','주가','주택가격','세계교역']
TFItopics_LONG = ['생산','선박','자동차','반도체','설비투자','건설투자','실업','채용','구직','도소매','정부지출','물가전망','주가전망','주택가격전망','세계교역']
TFItopics_ENG = ['Production','Shipbuilding','Automobile','Semiconductor','Facilities Investment','Construction','Unemployment','Recruitment','Job Search','Wholesale and Retail','Government Expendition','Inflation','Stock Price','Housing Price','World Trade']


FAfields = ['전자/영상/통신장비등', '정보통신업', '화학물질/제품', '의료물질/의약품', '금융', '전문/과학/기술',
               '도매/소매', '기타기계/장비', '자동차', '의료/정밀기기', '식료품', '운수/창고업', '1차금속',
               '예술/스포츠/여가', '조선/기타운수']#, '건설업', '전기장비', '인쇄/기록매체복제', '고무/플라스틱', '기타제조업',
               # '석유정제/코크스', '의복/모피', '전기/가스/증기', '부동산업', '비금속광물', '음료', '사업시설/사업지원/임대업',
               # '가구', '펄프/종이', '금속가공', '하수/폐기물처리업', '숙박업', '목재/나무', '교육서비스', '섬유',
               # '가죽/가방/신발', '기타개인서비스', '농업', '어업']

FAfields_ENG = ['Electronic, video, and communication equipment', 'Information and communication industry', 'Chemicals', 'Medical substances and medicine', 'Finance', 'Specialized, scientific, and technical services',
               'Wholesale and retail', 'Other machines and equipment', 'Automobile', 'Medical and precision equipment', 'Groceries', 'Transportation and warehouse', 'Primary metal',
               'Art, sports, and leisure services', 'Shipbuilding and other transportation']#, 'Construction', '전기장비', '인쇄/기록매체복제', '고무/플라스틱', '기타제조업',
               # '석유정제/코크스', '의복/모피', '전기/가스/증기', '부동산업', '비금속광물', '음료', '사업시설/사업지원/임대업',
               # '가구', '펄프/종이', '금속가공', '하수/폐기물처리업', '숙박업', '목재/나무', '교육서비스', '섬유',
               # '가죽/가방/신발', '기타개인서비스', '농업', '어업']

FAfields_ALL = ['전자/영상/통신장비등', '정보통신업', '화학물질/제품', '의료물질/의약품', '금융', '전문/과학/기술',
               '도매/소매', '기타기계/장비', '자동차', '의료/정밀기기', '식료품', '운수/창고업', '1차금속',
               '예술/스포츠/여가', '조선/기타운수', '건설업', '전기장비', '인쇄/기록매체복제', '고무/플라스틱', '기타제조업',
               '석유정제/코크스', '의복/모피', '전기/가스/증기', '부동산업', '비금속광물', '음료', '사업시설/사업지원/임대업',
               '가구', '펄프/종이', '금속가공', '하수/폐기물처리업', '숙박업', '목재/나무', '교육서비스', '섬유',
               '가죽/가방/신발', '기타개인서비스', '농업', '어업']

FAfields_ALL_ENG = ['Electronic, video, and communication equipment', 'Information and communication industry', 'Chemicals', 'Medical substances and medicine', 'Finance', 'Specialized, scientific, and technical services',
               'Wholesale and retail', 'Other machines and equipment', 'Automobile', 'Medical and precision equipment', 'Groceries', 'Transportation and warehouse', 'Primary metal',
               'Art, sports, and leisure services', 'Shipbuilding and other transportation', 'Construction', 'Electrical equipment', 'Printing and record media manufacturing', 'Rubber and plastic', 'Other manufacturing',
               'Petroleum refining and coke', 'Clothes and fur', 'Electric, gas, and steam ', 'Real estate', 'Nonmetallic minerals', 'Beverage', 'Facility management and supporting services',
               'Furniture', 'Pulp and paper', 'Metalworking', 'Sewage and waste disposal', 'Accommodation', 'Lumber and wood', 'Education', 'Textile',
               'Leather, bag and footwear', 'Other personal services', 'Agriculture', 'Fishing']


EAevents = ['코로나','러우전쟁','환율','금리']
EAevents_ENG = ['Covid 19', 'Russia-Ukraine War', 'Exchange Rate', 'Interest Rate']
#========================================================


params = list(df)
max_length = len(df)

suffix_row = "_row"
suffix_button_id = "_button"
suffix_sparkline_graph = "_sparkline_graph"
suffix_count = "_count"
suffix_ooc_n = "_OOC_number"
suffix_ooc_g = "_OOC_graph"
suffix_indicator = "_indicator"


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Text-based Financial Indices Hub"),
                    html.H6("By Beomseok Seo"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.A(
                        html.Button(children="GitHub"),
                        href="https://seo-beomseok.github.io",
                    ),
                    html.Button(
                        id="learn-more-button", children="LEARN MORE", n_clicks=0
                    ),
                    html.A(
                        html.Img(id="logo", src=app.get_asset_url("dash-logo-new.png")),
                        href="javascript:void(0);",
                    ),
                ],
            ),
        ],
    )


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="tab-1",
                        label="News Analysis",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),                
                    dcc.Tab(
                        id="tab-2",
                        label="Market Analysis",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="tab-3",
                        label="Factor Analysis",
                        value="tab3",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="tab-4",
                        label="Event Analysis",
                        value="tab4",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    # dcc.Tab(
                    #     id="tab-5",
                    #     label="Regional Analysis",
                    #     value="tab5",
                    #     className="custom-tab",
                    #     selected_className="custom-tab--selected",
                    # ),
                ],
            )
        ],
    )

def build_tab_1():
    return [
        # Manually select metrics
        html.Div(
            id="news-analysis-intro-container",
            className='analysis-intro-container',
            children=dcc.Markdown('''
                News analysis provides Theme Frequency in News Indices (TFNI) that address information about 15 important fields in economy. 
                The TFIs are computed based on about 4,000 economic news articles every day that are scrapped from the internet. 
                The total number of news articles used for this analysis is about 18 million.
                $$
                TFNI_{t}=\\sum\\limits_{i=1}^{N_t} \\hat{A}_i^{(t)} / N_t,\\qquad
                \\hat{A}_i^{(t)} = \\bigvee\\limits_{m=1}^{M_i} C_{im}^{(t)},\\qquad
                C_{im}^{(t)} = \\prod\\limits_{k=1}^{K}\\bigvee\\limits_{l=1}^{L_k} I_{S_{im}^{(t)}}(w_l^{[k]}),
                $$
                where $\\Omega_t=\\{A_1^{(t)},\\cdots,A_{N_t}^{(t)}\\}$ is the set of news articles, $A_i^{(t)}$, $i=1,\\cdots,N_t$, at time $t$ for the number of news articles, $N_t$, 
                and $A_i^{(t)}=\\{S_{i1}^{(t)},\\cdots,S_{iM_i}^{(t)}\\}$ is the set of news sentences, $S_{im}^{(t)}$, $m=1,\\cdots,M_i$, 
                and $W^{[k]} = \\{w_1^{[k]},\\cdots,w_{L_k}^{[k]}\\}$, $k=1,\\cdots,K$ is the $K$ groups of different synonyms describing a speicific field of economy, e.g. production, inflation, etc. 
                $I_S(w)=\\begin{cases} 1 & \\text{if} w\\in S \\\\ 0 & \\text{o.w.}\\end{cases}$ is an indicator function and $\\bigvee\\limits_{m=1}^{M} C_m = max(C_1,\\cdots,C_M)$ is an elementwise max function.
                ''',
                mathjax=True
            )
        ),
        html.Br(),        
        html.Div(
            id="news-analysis-container",
            className="analysis-container",
            children=[
                html.Div(
                    id="news-value-setter-menu",
                    className='value-setter-menu',
                    children=[
                        html.Div(
                            id="news-value-setter-panel",
                            className="value-setter-panel",
                            children=[
                            html.Div(
                                className="value-setter-panel-header row",
                                children=[
                                    html.Label("Period", className="three columns"),
                                    html.Label("Field", className="three columns"),
                                ],
                                # className="row",
                            ),
                            html.Div(
                                className="value-setter-panel-data row",
                                children=[
                                    html.Div(
                                        dcc.Dropdown(id="news-period-select-dropdown",
                                            options=list({"label": period, "value": period} for period in ['month','week']),
                                            value='month',
                                            clearable=False), 
                                        className="three columns"
                                    ),
                                    html.Div(
                                        dcc.Dropdown(id="news-field-select-dropdown",
                                            options=list({"label": field, "value": TFItopics[i]} for i,field in enumerate(TFItopics_ENG)),
                                            value='생산',
                                            clearable=False), 
                                        className="three columns"
                                    ),
                                    html.Div(
                                        html.Button("Update", id='news-set-btn', className="value-setter-set-btn"),
                                        className="three columns"
                                    ),
                                ],
                                # className="row",
                            ),
                            
                            ]
                        ),
                        
                    ],
                ),
            ],
        ),
        html.Br(),
        html.Div(className="analysis-graph-container", children=[generate_NA_graph()]),
        html.Br(),
        html.Div(
            id="news-analysis-outro-container",
            className="analysis-outro-container",
            children=dcc.Markdown('''
                    - [Economic Forecasting Using News Texts: The Compilation and Usage of Text-based Economic Field Indicators \\[뉴스 텍스트를 이용한 경기 예측: 경제부문별 텍스트 지표의 작성과 활용\\]](https://www.bok.or.kr/portal/bbs/P0002353/view.do?nttId=10070554&menuNo=200433&pageIndex=1). (2022) Seo, Beomseok., BOK Issue Note. 2022-(18).
                    - Econometric Forecasting Using Ubiquitous News Texts: Text-enhanced Factor Model. (2023+) Seo, Beomseok., (Forthcoming)
                    '''
            ),
        ),
        html.Br(),
    ]




def build_tab_2():
    return [
        # Manually select metrics
        html.Div(
            id="market-analysis-intro-container",
            className='analysis-intro-container',
            children=dcc.Markdown('''
                Market analysis compares the Text-based Business Confidence Indicators (TBCI) to the corresponding KOSPI indices by field.
                TBCIs are computed based on about 2,000 analyst reports per month that are generated from about 50 investment banks in Korea.
                The total number of analyst reports used for this analysis is about 130 thousand.
                $$
                TBCI_{i,t}=\\frac{X_{i,t}-\\bar{X}_{i,.}}{s_{i,.}}*10+100
                $$
                where $X_{i,t}=\\frac{\\sum_{s\\in S_{i,t}} I(s\\in \\mathcal{P})-I(s\\in \\mathcal{N})}{\\sum_{s\\in S_{i,t}} I(s\\in \\mathcal{P})+I(s\\in \\mathcal{N})},\\,$ 
                $\\bar{X}_{i,.} = \\frac{\\sum_{t}^T X_{i,t}}{T},\\,$ 
                $s_{i,.} = \\sqrt{\\frac{\\sum_{t}^T(X_{i,t}-\\bar{X}_{i,t})^2}{(T-1)}}\\,$
                and $\\mathcal{P}$ and $\\mathcal{N}$ are respectively the set of all positive and negative sentences, and $S_{i,t}$ is the multiset of the sentences in the sample for the field $i$ and time point $t$.
                
                ''',
                mathjax=True
            )
        ),
        html.Br(),
        html.Div(
            className="analysis-container",
            children=[
                html.Div(
                    className='value-setter-menu',
                    children=[
                        html.Div(
                            className="value-setter-panel",
                            children=[
                            html.Div(
                                className="value-setter-panel-header row",
                                children=[
                                    html.Label("Period", className="three columns"),
                                    html.Label("Field", className="three columns"),
                                ],
                                # className="row",
                            ),
                            html.Div(
                                className="value-setter-panel-data row",
                                children=[
                                    html.Div(
                                        dcc.Dropdown(id="market-period-select-dropdown",
                                            options=list({"label": period, "value": period} for period in ['quarter']),
                                            value='quarter',
                                            clearable=False), 
                                        className="three columns"
                                    ),
                                    html.Div(
                                        dcc.Dropdown(id="market-field-select-dropdown",
                                            options=list({"label": field, "value": field} for field in KRXfields_ENG),
                                            value='KOSPI',
                                            clearable=False), 
                                        className="three columns"
                                    ),
                                    html.Div(
                                        html.Button("Update", id='market-set-btn', className="value-setter-set-btn"),
                                        className="three columns"
                                    ),
                                ],
                                # className="row",
                            ),
                            
                            ]
                        ),
                        
                    ],
                ),
            ],
        ),
        html.Br(),
        html.Div(className="analysis-graph-container", children=[generate_MA_graph()]),
        html.Div(className="analysis-mid-container", children=dcc.Markdown(
            '''
            ''')
        ),
        html.Br(),
        html.Div(
            id="market-analysis-outro-container",
            className="analysis-outro-container",
            children=dcc.Markdown('''
                    - [Industrial Monitoring Using AI Algorithm: Analyst Report Text Mining \\[AI를 이용한 산업 모니터링: 증권사 리포트 텍스트 분석\\]](https://www.bok.or.kr/portal/bbs/P0002353/view.do?nttId=10075584&menuNo=200433&pageIndex=1). (2023) Seo, Beomseok, BOK Issue Note. 2023-(5).
                    '''
            ),
        ),
        html.Br(),        
    ]


def build_tab_3():
    return [
        # Manually select metrics
        html.Div(
            id="factor-analysis-intro-container",
            className='analysis-intro-container', # \\sum\\limits_{u\\in U_{i,t}\\setminus W} I(w=u)
            children=dcc.Markdown('''
                Factor analysis provides the Text-based Business Condition Factors (BC-factors) that show the top 5 issues in 40 industries that affect on their business condition.
                BC-factors are computed based on about 2,000 analyst reports per month that are generated from about 50 investment banks in Korea.  

                $$
                BC-factors_{i,t}^5 = \\{(w^{[K]},\\cdots,w^{[K-4]})\\, |\\, w^{[k]} = f(v_{(k)}),\\, v = m_{U_{i,t}\\setminus W}(w),\\, v_{(k)} \\text{ is the $k^{th}$ order statistic of }v \\}
                $$  

                where $U_{i,t}$ is the multiset of the trigram patterns appearing in the analyst reports of a field $i$ at time $t$, 
                and $m_A(w)$ is the multiplicity function of the multiset $A$ which is equivalent to the count of the element $w$ appearing in the multiset $A$, 
                and $W$ is the set of stopwords, and $K=|Supp(U_{i,t}\\setminus W)|$ is the cardinality of the support of the multiset $U_{i,t}\\setminus W$.
                
                ''',
                mathjax=True
            )
        ),
        html.Br(),
        html.Div(
            className="analysis-container",
            children=[
                html.Div(
                    className='value-setter-menu',
                    children=[
                        html.Div(
                            className="value-setter-panel",
                            children=[
                            html.Div(
                                className="value-setter-panel-header row",
                                children=[
                                    html.Label("Field", className="three columns"),
                                ],
                                # className="row",
                            ),
                            html.Div(
                                className="value-setter-panel-data row",
                                children=[
                                    html.Div(
                                        dcc.Dropdown(id="factor-field-select-dropdown",
                                            options=list({"label": field, "value": field} for field in FAfields_ENG),
                                            value="Electronic, video, and communication equipment",
                                            clearable=False,
                                            optionHeight=60), 
                                        className="three columns"
                                    ),
                                    html.Div(
                                        html.Button("Update", id='factor-set-btn', className="value-setter-set-btn"),
                                        className="three columns"
                                    ),
                                ],
                                # className="row",
                            ),
                            
                            ]
                        ),
                        
                    ],
                ),
            ],
        ),
        html.Br(),
        html.Div(className="analysis-graph-container", children=[generate_FA_graph()]),
        html.Div(
            className="analysis-footnote-container",
            children=dcc.Markdown('''
                    N: the number of sentences analyzed / C: the number of companies analyzed / A: the number of IBs that wrote the reports for the corresponding company, field, and time.
                    '''
            ),
        ),
        html.Br(),
        html.Div(
            className="analysis-container",
            children=[
                html.Div(
                    className='value-setter-menu',
                    children=[
                        html.Div(
                            className="value-setter-panel",
                            children=[
                            html.Div(
                                className="value-setter-panel-header row",
                                children=[
                                    html.Label("Max depth", className="three columns"),
                                ],
                                # className="row",
                            ),
                            html.Div(
                                className="value-setter-panel-data row",
                                children=[
                                    html.Div(
                                        dcc.Slider(2,4,1,value=2,id="treemap-slider"),
                                        className="two columns"
                                    ),
                                ],
                                # className="row",
                            ),
                            
                            ]
                        ),
                        
                    ],
                ),
            ],
        ),
        html.Div(className="analysis-graph-container", children=[generate_FA_treemap_graph()]),
        html.Br(),
        html.Br(),
        html.Div(
            id="factor-analysis-outro-container",
            className="analysis-outro-container",
            children=dcc.Markdown('''
                    - [Industrial Monitoring Using AI Algorithm: Analyst Report Text Mining \\[AI를 이용한 산업 모니터링: 증권사 리포트 텍스트 분석\\]](https://www.bok.or.kr/portal/bbs/P0002353/view.do?nttId=10075584&menuNo=200433&pageIndex=1). (2023) Seo, Beomseok, BOK Issue Note. 2023-(5).
                    '''
            ),
        ),
        html.Br(),                
    ]


def build_tab_4():
    return [
        # Manually select metrics
        html.Div(
            id="event-analysis-intro-container",
            className='analysis-intro-container',
            children=dcc.Markdown('''
                Event analysis provides the examples of Text-based Impact of an Event Indicators (TIEI) and Text-based Evaluation of an Event Indicators (TEEI) for a couple of events selected for their importance in economy.
                
                $$
                TIEI^{\\mathcal{A}_w}_{i,t} = \\frac{\\sum_{s\\in S_{i,t} } I(s\\in \\mathcal{A}_w)}{|S_{i,t}|}*100,
                $$
                
                where $\\mathcal{A}_w$ is the set of all sentences that include a word group $w$,
                $S_{i,t}$ is the multiset of the sentences in the sample for the field $i$ and time point $t$.

                $$
                TEEI^A_{i,t}=\\frac{X_{i,t}-\\bar{X}_{i,.}}{s_{i,.}}*10+100
                $$
                
                where $X_{i,t}=\\frac{\\sum_{s\\in S_{i,t}} I(s\\in \\mathcal{P} \\bigcap s\\in \\mathcal{A}_w )-I(s\\in \\mathcal{N} \\bigcap s\\in \\mathcal{A}_w)}{\\sum_{s\\in S_{i,t}} I(s\\in \\mathcal{P} \\bigcap s\\in \\mathcal{A}_w)+I(s\\in \\mathcal{N} \\bigcap s\\in \\mathcal{A}_w)},\\,$ 
                $\\bar{X}_{i,.} = \\frac{\\sum_{t}^T X_{i,t}}{T},\\,$ 
                $s_{i,.} = \\sqrt{\\frac{\\sum_{t}^T(X_{i,t}-\\bar{X}_{i,t})^2}{(T-1)}}\\,$
                and $\\mathcal{P}$ and $\\mathcal{N}$ are respectively the set of all positive and negative sentences.
                
                ''',
                mathjax=True
            )
        ),
        html.Br(),
        html.Div(
            className="analysis-container",
            children=[
                html.Div(
                    className='value-setter-menu',
                    children=[
                        html.Div(
                            className="value-setter-panel",
                            children=[
                            html.Div(
                                className="value-setter-panel-header row",
                                children=[
                                    html.Label("Period", className="three columns"),
                                    html.Label("Field", className="three columns"),
                                ],
                                # className="row",
                            ),
                            html.Div(
                                className="value-setter-panel-data row",
                                children=[
                                    html.Div(
                                        dcc.Dropdown(id="event-select-dropdown",
                                            options=list({"label": event, "value": EAevents[i]} for i,event in enumerate(EAevents_ENG)),
                                            value='코로나',
                                            clearable=False), 
                                        className="three columns"
                                    ),
                                    html.Div(
                                        dcc.Dropdown(id="event-item-select-dropdown",
                                            options=list({"label": item, "value": item} for item in ['Impact','Evaluation']),
                                            value='Impact',
                                            clearable=False), 
                                        className="three columns"
                                    ),
                                    html.Div(
                                        html.Button("Update", id='event-set-btn', className="value-setter-set-btn"),
                                        className="three columns"
                                    ),
                                ],
                                # className="row",
                            ),
                            
                            ]
                        ),
                        
                    ],
                ),
            ],
        ),
        html.Br(),
        html.Div(className="analysis-graph-container", children=[generate_EA_graph()]),
        html.Br(),
        html.Div(className="analysis-mid-container", children=dcc.Markdown(
            '''

            ...  

            ''')
        ),
        html.Br(),
        html.Div(
            id="event-analysis-outro-container",
            className="analysis-outro-container",
            children=dcc.Markdown('''
                    - [Industrial Monitoring Using AI Algorithm: Analyst Report Text Mining \\[AI를 이용한 산업 모니터링: 증권사 리포트 텍스트 분석\\]](https://www.bok.or.kr/portal/bbs/P0002353/view.do?nttId=10075584&menuNo=200433&pageIndex=1). (2023) Seo, Beomseok, BOK Issue Note. 2023-(5).
                    '''
            ),
        ),
        html.Br(),                
    ]



def generate_NA_graph():
    NA_period = 'month'
    fig = DG.plotNewsPlotly(NA_period,'생산_20050101_20230129','', show=False)
    fig.for_each_trace(lambda f: f.update(name = 'Production' if f.name=='생산' else f.name,))    
    fig.update_layout(legend=dict(orientation="h",
                                  yanchor="top",
                                  y=1.2,
                                  xanchor="left",x=0))
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            # type="-"
        )
    )
    return dcc.Graph(id="news-analysis-graph",figure=fig)


def generate_MA_graph():
    MA = MarketAnalysisShell(AR)
    MA.getMarketDat('quarter')
    if MA.period == 'month':
        beg='201901'
        end='202301'
    elif MA.period == 'quarter':
        beg='2019q1'
        end='2023q1'
    fig = DG.plotKospiPlotly(MA,'','코스피',beg=beg,end=end,type=3, load_csv=True, show=False)
    fig.update_layout(legend=dict(orientation="h",
                                  yanchor="top",
                                  y=1.05,
                                  xanchor="left",x=1))
    return dcc.Graph(id="market-analysis-graph",figure=fig)


def generate_FA_graph():
    fig = DG.plotTableDash(dat='', title='전자/영상/통신장비등', load_csv=True, show=False)
    return html.Div(id="factor-analysis-graph",children=fig)


def generate_FA_treemap_graph():
    fig = DG.plotTreemap(quarter='2022q4', load_csv=True, show=False)
    return dcc.Graph(id="factor-analysis-treemap-graph",figure=fig)


def generate_EA_graph():
    EA = EventAnalysisShell(AR)
    EA.eventImpact('러우전쟁')
    fig = DG.plotEventImpact(EA, show=False)
    return dcc.Graph(id="event-analysis-graph",figure=fig)




def generate_modal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                        """
                        ###### What is this app about?

                        This dashboard replicates the text-based financial indicators proposed in Beomseok Seo (2022, 2023). Please keep in mind that the presented data may not be completely accurate and could potentially be outdated. Therefore, it is recommended to use the information provided with caution and at your own risk.

                        
                        """
                            )
                        ),
                    ),
                ],
            )
        ),
    )





app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=50,  # start at batch 50
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        # dcc.Store(id="value-setter-store", data=init_value_setter_store()),
        dcc.Store(id="n-interval-stage", data=50),
        generate_modal(),
    ],
)


@app.callback(
    [Output("app-content", "children"), Output("interval-component", "n_intervals")],
    [Input("app-tabs", "value")],
    [State("n-interval-stage", "data")],
)
def render_tab_content(tab_switch, stopped_interval):
    if tab_switch == "tab1":
        return build_tab_1(), stopped_interval
    elif tab_switch == "tab2":
        return build_tab_2(), stopped_interval
    elif tab_switch == "tab3":
        return build_tab_3(), stopped_interval     
    elif tab_switch == "tab4":
        return build_tab_4(), stopped_interval 
    elif tab_switch == "tab5":
        return build_tab_4(), stopped_interval 


# Update interval
@app.callback(
    Output("n-interval-stage", "data"),
    [Input("app-tabs", "value")],
    [
        State("interval-component", "n_intervals"),
        State("interval-component", "disabled"),
        State("n-interval-stage", "data"),
    ],
)
def update_interval_state(tab_switch, cur_interval, disabled, cur_stage):
    if disabled:
        return cur_interval

    if tab_switch == "tab1":
        return cur_interval
    return cur_stage


# ======= Callbacks for modal popup =======
@app.callback(
    Output("markdown", "style"),
    [Input("learn-more-button", "n_clicks"), Input("markdown_close", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "learn-more-button":
            return {"display": "block"}

    return {"display": "none"}



# ====== Callbacks to update stored data via click =====

@app.callback(
    output=Output("news-analysis-graph", "figure"),
    inputs=[Input("news-set-btn", "n_clicks")],
    state=[
        State("news-period-select-dropdown", "value"),
        State("news-field-select-dropdown", "value"),
    ],
)
def update_NA_graph(set_btn, period, field):
    field_ = TFItopics_LONG[np.where([x==field for x in TFItopics])[0][0]]
    NA_period = period
    fig = DG.plotNewsPlotly(NA_period,field_+'_20050101_20230129','', show=False)
    fig.for_each_trace(lambda f: f.update(name = TFItopics_ENG[np.where([x==field for x in TFItopics])[0][0]] if f.name in TFItopics_LONG else f.name,))    
    fig.update_layout(legend=dict(orientation="h",
                                  yanchor="top",
                                  y=1.2,
                                  xanchor="left",x=0))
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            # type="-"
        ),
        height=500,
    )
    return fig


@app.callback(
    output=Output("market-analysis-graph", "figure"),
    inputs=[Input("market-set-btn", "n_clicks")],
    state=[
        State("market-period-select-dropdown", "value"),
        State("market-field-select-dropdown", "value"),
    ],
)
def update_MA_graph(set_btn, period, KRXfield):
    MA = MarketAnalysisShell(AR)
    MA.getMarketDat(period)
    j = np.where([i==KRXfield for i in KRXfields_ENG])[0][0]
    ARfield = ARfields[j]
    type_ = fieldtypes[j]
    
    if period == 'month':
        beg='201901'
        end='202301'
    elif period == 'quarter':
        beg='2019q1'
        end='2023q1'

    KRXfield_ = KRXfields[np.where([x==KRXfield for x in KRXfields_ENG])[0][0]]
    ARfield_ = ARfields_ENG[np.where([x==ARfield for x in ARfields])[0][0]]
    fig = DG.plotKospiPlotly(MA,ARfield,KRXfield_,beg=beg,end=end,type=type_, load_csv=True, show=False)
    fig.for_each_trace(lambda f: f.update(name = 'TBCI '+KRXfield if f.name[:4]=='TBCI' else 'KOSPI '+ARfield_,))    
    fig.update_layout(legend=dict(orientation="h",
                              yanchor="top",
                              y=1.05,
                              xanchor="left",x=0))
    return fig
    #"period:{}, field:{}".format(period,field)


@app.callback(
    output=Output("factor-analysis-graph", "children"),
    inputs=[Input("factor-set-btn", "n_clicks")],
    state=[
        State("factor-field-select-dropdown", "value"),
    ],
)
def update_FA_graph(set_btn, field):
    field_ = FAfields[np.where([x==field for x in FAfields_ENG])[0][0]]
    fig = DG.plotTableDash(dat='', title=field_, load_csv=True, show=False)
    return fig


@app.callback(
    output=Output("factor-analysis-treemap-graph", "figure"),
    inputs=[Input("treemap-slider", "value")],
)
def update_FA_treemap_graph(slider):
    fig = DG.plotTreemap(quarter='2022q4', load_csv=True, show=False)
    fig.update_traces(maxdepth=slider)
    return fig


@app.callback(
    output=Output("event-analysis-graph", "figure"),
    inputs=[Input("event-set-btn", "n_clicks")],
    state=[
        State("event-select-dropdown", "value"),
        State("event-item-select-dropdown", "value"),
    ],
)
def update_EA_graph(set_btn, event, item):
    EA = EventAnalysisShell(AR)
    if item=='Impact':
        EA.eventImpact(event)
        fig = DG.plotEventImpact(EA, show=False)
        fig.for_each_trace(lambda f: f.update(name = FAfields_ALL_ENG[np.where([f.name==x for x in FAfields_ALL])[0][0]]))    
    elif item=='Evaluation':
        EA.eventEval(event)
        fig = DG.plotEventEval(EA, show=False)
        fig.for_each_trace(lambda f: f.update(name = FAfields_ALL_ENG[np.where([f.name==x for x in FAfields_ALL])[0][0]]))
    return fig






def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))

# Running the server
if __name__ == "__main__":
    port = 8050 # or simply open on the default `8050` port
    # Timer(1, open_browser).start()    
    app.run_server(debug=True, port=8050)
    open_browser()
