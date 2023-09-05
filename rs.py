import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

user_id = st.text_input( "您要向哪位用户进行推荐？请输入用户编号(0-999)： 👇")

if user_id:

    @st.cache(hash_funcs={"MyUnhashableClass": lambda _: None}, allow_output_mutation=True)
    def load():
        rules = pd.read_csv('Rules.csv')
        rules['antecedents'] = rules['antecedents'].map(eval)
        rules['consequents'] = rules['consequents'].map(eval)
        return np.load("predicts.npy"), np.load("user_sim_matrix_all.npy"), pd.read_csv('Processed_Item_Info.csv'), pd.read_csv('Processed_User_Info.csv'), rules

    predicts, user_sim_matrix_all, df_meta_GC_3, df_GC_5, rules = load()

    sortedResult = predicts[:, int(user_id)].argsort()[::-1]

    recommended_num = 20
    
    idx = 0  # 保存已经推荐了多少部电影
    st.write()
    st.markdown('### 为该用户推荐的评分最高的20个Gift Card商品是:')

    reco_item_list = []
    for i in sortedResult:
        reco_item = df_meta_GC_3.iloc[i]['asin']
        st.write('预测评分：%.2f, 商品ID：%s' % (predicts[i, int(user_id)], reco_item))
        img_path = "./images/" + reco_item + ".jpg"
        img = Image.open(img_path)
        cap = "商品ID: " + reco_item
        st.image(img, caption=cap, width=200)
        reco_item_list.append(reco_item)
        idx += 1
        if idx == recommended_num: break

    st.write()
    num = 5
    num_idx = 0
    for item in reco_item_list:
        for j in range(rules.shape[0]):
            if item in rules['antecedents'][j]:
                rule_list = rules['antecedents'][j]
                st.markdown('### 根据关联规则分析')
                s = "、".join(rule_list)
                st.write('对于商品', item, '您可以进一步购买: ', s)
                for rule_item in rule_list:
                    img_path = "./images/" + rule_item + ".jpg"
                    img = Image.open(img_path)
                    cap = "商品ID: " + reco_item
                    st.image(img, caption=cap, width=200)


                st.write('Support:', rules['support'][j])
                st.write('Confidence:', rules['confidence'][j])
                st.write('Lift:', rules['lift'][j])
                st.write()
                num_idx += 1
                if num_idx == num: break

    st.write()
    st.markdown('### 此外，您可能感兴趣的用户有:')
    sortedResult = user_sim_matrix_all[:, int(user_id)].argsort()[::-1]

    recommended_user_num = 10
    idx2 = 0

    for i in sortedResult:
        st.write('相似度：%.2f, 用户ID：%s' % (user_sim_matrix_all[i, int(user_id)], df_GC_5.iloc[i]['reviewerID']))
        idx2 += 1
        if idx2 == recommended_user_num: break