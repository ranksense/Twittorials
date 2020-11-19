import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import requests
import base64
import ast #convert string to dictionary

####################################


c30, c31, c32, c33, c34 = st.beta_columns(5)

with c30:
  st.header('')
  st.image('logo.png', width = 725 )

with c34:
  st.header('')
  st.header('')
  st.markdown('###### &nbsp &nbsp &nbsp &nbsp &nbsp Made in [![this is an image link](https://i.imgur.com/iIOA6kU.png)](https://www.streamlit.io/)&nbsp, with :heart: by [@DataChaz](https://twitter.com/DataChaz)')

def _max_width_():
    max_width_str = f"max-width: 1400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

_max_width_()

####################################


with st.beta_expander("🛠️ Code for boilerplate", expanded=False):

        code_text_area = '''c30, c31, c32, c33, c34 = st.beta_columns(5)

with c30:
  st.header('')
  st.image('logo.png', width = 725 )

with c34:
  st.header('')
  st.header('')
  st.markdown('###### &nbsp &nbsp &nbsp &nbsp &nbsp Made in [![this is an image link](https://i.imgur.com/iIOA6kU.png)](https://www.streamlit.io/)&nbsp, with :heart: by [@DataChaz](https://twitter.com/DataChaz)')

        '''

        st.code(code_text_area, language='python')

options = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0"

headers = "{'user-agent' : '" + options + "'}"
Dict = ast.literal_eval(headers)

CodeList = []

st.markdown('## **Paste a list of URLs ▼**') ### https://docs.streamlit.io/api.html#streamlit.file_uploader #########

c29, c30, c31 = st.beta_columns([1,4,1])

with c30:

    MAX_LINES = 20

    text = st.text_area("One URL per line (max 20)", 
"https://httpbin.org/status/200", height=300)
    lines = text.split("\n")  # A list of lines

    if not text:
        st.stop()

    if len(lines) > MAX_LINES:
        st.warning(f"Maximum number of lines reached. Only the first {MAX_LINES} will be processed.")
        lines = lines[:MAX_LINES]

    for line in lines:
        # Process line here
        data = pd.DataFrame({'url':lines})

    #drop_duplicates
    data = data.drop_duplicates(subset ="url")
    #contains https or http
    data = data[data["url"].str.contains('http://|https://')]
    #At least 8 characters
    data = data[data['url'].map(len) > 8]

c70, c71 = st.beta_columns(2)

with c70:

    with st.beta_expander("🛠️ Code for text_area", expanded=False):

        code_text_area = '''MAX_LINES = 20

        text = st.text_area("URLs, one per line.", height=200)
        lines = text.split("\n")

        if len(lines) > MAX_LINES:
            st.warning(f"Maximum number of lines reached. Only the first {MAX_LINES} will be processed.")
            lines = lines[:MAX_LINES]

        for line in lines:
            # Process line here
            data = pd.DataFrame({'url':lines})

        #drop_duplicates
        data = data.drop_duplicates(subset ="url")
        #contains https or http
        data = data[data["url"].str.contains('http://|https://')]
        #At least 8 characters
        data = data[data['url'].map(len) > 8]
        #st.dataframe(data)
        '''

        st.code(code_text_area, language='python')

with c71:

    with st.beta_expander("🛠️ Code for cached functions", expanded=False):

        code_text_area = '''@st.cache(suppress_st_warning=True)
def _extract_status(row):
  return {
    "code": row["no_redirects_response"].status_code,
    "redirects": len(row["redirects_response"].history),
    "last_code": row["redirects_response"].status_code,
    "last_url_in_chain": row["redirects_response"].url
    }

@st.cache(suppress_st_warning=True)
def fetching_URL_statuses(urls):
  df = pd.DataFrame({"url": urls})
  df["no_redirects_response"] = df.url.apply(lambda url: requests.get(url, allow_redirects=False, headers=Dict))
  df["redirects_response"] = df.url.apply(lambda url: requests.get(url, headers=Dict))
  return {k: _extract_status(v) for k,v in df.set_index("url").to_dict("index").items()}

dict1 = fetching_URL_statuses(data.url.tolist()[:100])
dfFromDict = pd.DataFrame.from_dict(dict1, orient='index')
dfFromDict.reset_index(inplace=True)
dfFromDict = dfFromDict.rename(columns={'index': 'url'})
dfFromDict = dfFromDict.astype(str)


        '''

        st.code(code_text_area, language='python')

#st.header('')

#endregion ##########################################################################################

@st.cache(suppress_st_warning=True)
def _extract_status(row):
  return {
    "code": row["no_redirects_response"].status_code,
    "redirects": len(row["redirects_response"].history),
    "last_code": row["redirects_response"].status_code,
    "last_url_in_chain": row["redirects_response"].url
    }

@st.cache(suppress_st_warning=True)
def fetching_URL_statuses(urls):
  df = pd.DataFrame({"url": urls})
  df["no_redirects_response"] = df.url.apply(lambda url: requests.get(url, allow_redirects=False, headers=Dict))
  df["redirects_response"] = df.url.apply(lambda url: requests.get(url, headers=Dict))
  return {k: _extract_status(v) for k,v in df.set_index("url").to_dict("index").items()}

dict1 = fetching_URL_statuses(data.url.tolist()[:100])
dfFromDict = pd.DataFrame.from_dict(dict1, orient='index')
dfFromDict.reset_index(inplace=True)
dfFromDict = dfFromDict.rename(columns={'index': 'url'})
dfFromDict = dfFromDict.astype(str)

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_data(nrows):

    dfFromDict["code_class"] = pd.np.where(
        dfFromDict.code.str.contains("^1.*"),
        "(1XX)",
        pd.np.where(
            dfFromDict.code.str.contains("^2.*"),
            "(2XX)",
            pd.np.where(
                dfFromDict.code.str.contains("^3.*"),
                "(3XX)",
                pd.np.where(
                    dfFromDict.code.str.contains("^4.*"),
                    "(4XX)",
                    "(5XX)",
                ),
            ),
        ),
)

    return dfFromDict

dfFromDict2 = load_data(100)
dfFromDict2 = dfFromDict2.sort_values(by='code')
DfPivotCodes = dfFromDict2.groupby(['code_class']).agg({'code_class': ['count']})
DfPivotCodes.columns = ['_'.join(multi_index) for multi_index in DfPivotCodes.columns.ravel()]
DfPivotCodes = DfPivotCodes.reset_index()

dfPivotFiltered = DfPivotCodes[DfPivotCodes['code_class'].isin(["(2XX)","(3XX)","(4XX)","(5XX)"])]

c = st.beta_container()

##################################

code_types_fromDF = dfPivotFiltered['code_class'].to_list()
code_countfromDF = dfPivotFiltered['code_class_count'].to_list()

st.header('')

try:
    csv = dfFromDict2.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown('## **▼ List view**')
    st.subheader("")
    href = f'<a href="data:file/csv;base64,{b64}" download="listViewExport.csv">** - Download link 🎁 **</a>'
    st.markdown(href, unsafe_allow_html=True)

except NameError:
    print ('wait')

codeClass =["(2XX)","(3XX)","(4XX)","(5XX)"]

Code01 = codeClass[0]
Code02 = codeClass[1]
Code03 = codeClass[2]
Code04 = codeClass[3]

code_count_Origin = [0,0,0,0]

# 4 code types in dataframe
if len(code_countfromDF) == 4:
    code_count_Origin = code_countfromDF
# 3 code types in dataframe
if code_types_fromDF == ["(2XX)","(3XX)","(4XX)"]:
    code_count_Origin[0] = code_countfromDF[0]
    code_count_Origin[1] = code_countfromDF[1]
    code_count_Origin[2] = code_countfromDF[2]
if code_types_fromDF == ["(3XX)","(4XX)","(5XX)"]:
    code_count_Origin[1] = code_countfromDF[0]
    code_count_Origin[2] = code_countfromDF[1]
    code_count_Origin[3] = code_countfromDF[2]
if code_types_fromDF == ["(2XX)","(3XX)","(5XX)"]:
    code_count_Origin[0] = code_countfromDF[0]
    code_count_Origin[1] = code_countfromDF[1]
    code_count_Origin[3] = code_countfromDF[2]
if code_types_fromDF == ["(2XX)","(4XX)","(5XX)"]:
    code_count_Origin[0] = code_countfromDF[0]
    code_count_Origin[2] = code_countfromDF[1]
    code_count_Origin[3] = code_countfromDF[2]
# 2 code types in dataframe
if code_types_fromDF == ["(2XX)","(3XX)"]:
    code_count_Origin[0] = code_countfromDF[0]
    code_count_Origin[1] = code_countfromDF[1]
if code_types_fromDF == ["(2XX)","(4XX)"]:
    code_count_Origin[0] = code_countfromDF[0]
    code_count_Origin[2] = code_countfromDF[1]
if code_types_fromDF == ["(2XX)","(5XX)"]:
    code_count_Origin[0] = code_countfromDF[0]
    code_count_Origin[3] = code_countfromDF[1]
if code_types_fromDF == ["(3XX)","(4XX)"]:
    code_count_Origin[1] = code_countfromDF[0]
    code_count_Origin[2] = code_countfromDF[1]
if code_types_fromDF == ["(3XX)","(5XX)"]:
    code_count_Origin[1] = code_countfromDF[0]
    code_count_Origin[3] = code_countfromDF[1]
# 1 code type in dataframe
if code_types_fromDF == ["(2XX)"]:
    code_count_Origin[0] = code_countfromDF[0]
if code_types_fromDF == ["(3XX)"]:
    code_count_Origin[1] = code_countfromDF[0]
if code_types_fromDF == ["(4XX)"]:
    code_count_Origin[2] = code_countfromDF[0]
if code_types_fromDF == ["(5XX)"]:
    code_count_Origin[3] = code_countfromDF[0]

pie_options = {
    "tooltip": {
        "trigger": 'item',
        "formatter": '{a} <br/>{b}: {c} ({d}%)'
    },
    "color":['#57904b','#fb8649','#ae1029', '#0065c2'],

    "legend": {
        "orient": 'vertical',
        #"orient": 'vertical',
        "size": 150,
        "bottom": 2,
        #"center": 10,
        "left": 3,
        "data": codeClass
    },
    "series": [
        {
            "name": 'Code',
            "type": 'scroll',
            "type": 'pie',
            "radius": ['50%', '70%'],
            "avoidLabelOverlap": True,
            "label": {
                "bleedMargin": 50
            },
            "emphasis": {
                "label": {
                    "show": True,
                    "fontSize": '30',
                    "fontWeight": 'bold'
                }
            },
            "labelLine": {
                "show": True
            },
            "data": [
                {"value": code_count_Origin[0], "name": Code01},
                {"value": code_count_Origin[1], "name": Code02},
                {"value": code_count_Origin[2], "name": Code03},
                {"value": code_count_Origin[3], "name": Code04},
            ]
        }
    ]
};

c1, c2 = c.beta_columns(2)

with c1:
    st.markdown('## **▼ Chart Overview **')   
    st_echarts(options=pie_options)

    
with c2:
    st.markdown('## **▼ Pivot Overview **')

    st.write("")
    st.write("")
    st.table(dfPivotFiltered)


c3, c4 = c.beta_columns(2)

with c3:

    with st.beta_expander("🛠️ Code for chart", expanded=False):
        
    #st.table(dfPivotFiltered)
            #st.header('')
        code_text_table = '''pie_options = {
    "tooltip": {
        "trigger": 'item',
        "formatter": '{a} <br/>{b}: {c} ({d}%)'
    },
    "color":['#57904b','#fb8649','#ae1029', '#0065c2'],

    "legend": {
        "orient": 'vertical',
        #"orient": 'vertical',
        "size": 150,
        "bottom": 2,
        #"center": 10,
        "left": 3,
        "data": codeClass
    },
    "series": [
        {
            "name": 'Code',
            "type": 'scroll',
            "type": 'pie',
            "radius": ['50%', '70%'],
            "avoidLabelOverlap": False,
            "label": {
                "bleedMargin": 50
            },
            "emphasis": {
                "label": {
                    "show": True,
                    "fontSize": '30',
                    "fontWeight": 'bold'
                }
            },
            "labelLine": {
                "show": True
            },
            "data": [
                {"value": code_count_Origin[0], "name": Code01},
                {"value": code_count_Origin[1], "name": Code02},
                {"value": code_count_Origin[2], "name": Code03},
                {"value": code_count_Origin[3], "name": Code04},
            ]
        }
    ]
 };


 st.markdown('## **▼ Chart Overview **')
 st_echarts(options=pie_options)

            '''

        st.code(code_text_table, language='python')


with c4:

    with st.beta_expander("🛠️ Code for pivot table", expanded=False):
        
    #st.table(dfPivotFiltered)
            #st.header('')
        code_text_table = '''
dfFromDict2["code"] = pd.to_numeric(dfFromDict2["code"])
dfFromDict2["last_code"] = pd.to_numeric(dfFromDict2["last_code"])
dfFromDict2.reset_index(inplace=True)

dfFromDict2 = dfFromDict2[["url", "code", "code_class", "redirects", "last_url_in_chain", "last_code"]]
dfFromDict2 = dfFromDict2.style.applymap(colors, subset=['code', "last_code"])

st.table(dfFromDict2)


            '''

        st.code(code_text_table, language='python')

c2 = st.beta_container()

def colors(value):
  if value == 200:
    color = 'green'
  elif value == 301:
    color = 'orange'
  elif value == 302:
    color = 'orange'
  elif value == 400:
    color = 'red'
  elif value == 404:
    color = 'red'
  elif value == 403:
    color = 'red'
  elif value == 500:
    color = 'red'
  else:
    color = 'black'

  return 'color: %s' % color

dfFromDict2["code"] = pd.to_numeric(dfFromDict2["code"])
dfFromDict2["last_code"] = pd.to_numeric(dfFromDict2["last_code"])
dfFromDict2.reset_index(inplace=True)

dfFromDict2 = dfFromDict2[["url", "code", "code_class", "redirects", "last_url_in_chain", "last_code"]]
dfFromDict2 = dfFromDict2.style.applymap(colors, subset=['code', "last_code"])

st.table(dfFromDict2)

c30, c31 = st.beta_columns(2)

with c31:

    with st.beta_expander("🛠️ Code for download module", expanded=False):
        
            #st.header('')
            code_text_table = '''try:
    csv = dfFromDict2.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown('## **▼ List view**')
    st.subheader("")
    href = f'<a href="data:file/csv;base64,{b64}" download="listViewExport.csv">** - Download link 🎁 **</a>'
    st.markdown(href, unsafe_allow_html=True)

except NameError:
    print ('wait')


            '''

            st.code(code_text_table, language='python')

with c30:

    with st.beta_expander("🛠️ Code for list view", expanded=False):
        
            #st.header('')
            code_text_table = '''
            
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_data(nrows):

    dfFromDict["code_class"] = pd.np.where(
        dfFromDict.code.str.contains("^1.*"),
        "(1XX)",
        pd.np.where(
            dfFromDict.code.str.contains("^2.*"),
            "(2XX)",
            pd.np.where(
                dfFromDict.code.str.contains("^3.*"),
                "(3XX)",
                pd.np.where(
                    dfFromDict.code.str.contains("^4.*"),
                    "(4XX)",
                    "(5XX)",
                ),
            ),
        ),
)

    return dfFromDict

dfFromDict2 = load_data(100)

def colors(value):
  if value == 200:
    color = 'green'
  elif value == 301:
    color = 'orange'
  elif value == 302:
    color = 'orange'
  elif value == 400:
    color = 'red'
  elif value == 404:
    color = 'red'
  elif value == 403:
    color = 'red'
  elif value == 500:
    color = 'red'
  else:
    color = 'black'

  return 'color: %s' % color

dfFromDict2["code"] = pd.to_numeric(dfFromDict2["code"])
dfFromDict2["last_code"] = pd.to_numeric(dfFromDict2["last_code"])
dfFromDict2.reset_index(inplace=True)

dfFromDict2 = dfFromDict2[["url", "code", "code_class", "redirects", "last_url_in_chain", "last_code"]]
dfFromDict2 = dfFromDict2.style.applymap(colors, subset=['code', "last_code"])

st.table(dfFromDict2)

            
            '''

            st.code(code_text_table, language='python')

    
