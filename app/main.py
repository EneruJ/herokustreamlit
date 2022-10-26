import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

st.write('# Analyse de données : Tiers stratégiques sur Pokémon ')  #st.title('Avocado Prices dashboard')
st.markdown('''
L'objectif de cette analyse est de déterminer les différentes caractéristiques qui définissent les tiers stratégiques sur le jeu Pokémon.
Pour cela, nous allons analyser les caractéristiques principales des Pokémon présents dans chacun des tiers et définir ce qui fait qu'un Pokémon sera dans un tier en particulier.
''')

df = pd.read_csv('Données//pokemon-data.csv', delimiter=';')
mdf = pd.read_csv('Données//move-data.csv', delimiter=',')
pdf = pd.read_csv('Données//pokemon.csv', delimiter=',')


st.write('Tout d\'abord, après avoir importé les librairies essentiels ainsi que les dataset utiles au projet, quelques éléments du dataset principal **df** ont été modifiés afin de faciliter leur analyse. Pour cette analyse, seuls les tiers principaux en stratégie seront utilisés, on modifie donc le dataset afin de garder les 6 tiers principaux. On crée ensuite une nouvelle colonne *"bst"* qui contiendra le total des statistiques de base des pokémons, puis une colonne *"tier_rank"* qui sera une adaptation de l\'ordre des tiers en chiffre afin de générer plus facilement certains graphiques.')

df.columns = ['name', 'types', 'abilities', 'tier', 'hp', 'atk', 'def', 'spa', 'spd', 'spe', 'next_evos','moves']
df.loc[df.tier == 'OUBL','tier'] = 'Uber'
df.loc[df.tier == 'UUBL','tier'] = 'OU'
df.loc[df.tier == 'RUBL','tier'] = 'UU'
df.loc[df.tier == 'NUBL','tier'] = 'RU'
df.loc[df.tier == 'PUBL','tier'] = 'NU'
df = df[df['tier'].isin(['Uber', 'OU', 'UU', 'NU', 'RU', 'PU'])]
df['bst'] = df['hp'] + df['atk'] + df['def'] + df['spa'] + df['spd'] + df['spe']
tiers = ['Uber', 'OU', 'UU', 'RU', 'NU', 'PU']                                                                      
df.loc[df['tier'] == "Uber", "tier_rank"] = 0
df.loc[df['tier'] == "OU", "tier_rank"] = 1
df.loc[df['tier'] == "UU", "tier_rank"] = 2
df.loc[df['tier'] == "RU", "tier_rank"] = 3
df.loc[df['tier'] == "NU", "tier_rank"] = 4
df.loc[df['tier'] == "PU", "tier_rank"] = 5
df = df.astype({'tier_rank': int})
df['moves'] = df.apply(lambda x: set(x.moves), axis=1)


# Suite à cela, on fusionne les 2 dataset principaux, en se basant sur le nom anglais des pokémons. L'ajout du dataset **pdf** permettra d'avoir plus d'élements à analyser afin de répondre à notre problématique.



final_df = pd.merge(df, pdf, on='name')
final_df.head()

AgGrid(final_df, height=400)
# Nous obtenons donc le dataset **final_df**, jeu de données qui contient les caracteristiques principales de chaque Pokémon disponible, ainsi que leur tier. Grâce à ce dataset, nous allons pouvoir répondre à notre problématique, et déterminer **comment les tiers stratégiques sont définis.**
# 
# Tout d'abord, nous allons analyser le pourcentage de Pokémon présent dans chaque tier.


fig, ax= plt.subplots()
#c = sns.color_palette('muted')
#c = [c[5], c[1], c[3], c[4], c[2], c[0]]
#ax = df.tier.value_counts().plot(kind='pie', autopct='%1.1f%%', colors=c, title='Pourcentage de Pokemon par tier')
explode = (0, 0.1, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
ax.pie(df.tier.value_counts(), labels=df.tier.value_counts(), autopct='%1.1f%%',
        shadow=True, startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig)

# Après avoir analysé le pourcentage de pokémons présent dans chaque tier, nous pouvons pour chaque tier avoir une moyenne du **bst** des pokémons, qui correspond au total de leurs statistiques. Comme ce graphique le démontre, on peut facilement observer que plus on s'éloigne des tiers élevés, plus la moyenne de statistiques baisse.


df.bst[df['tier'] == "OU"].describe()


fig, ax = plt.subplots(figsize=(15,8))
g2 = sns.boxplot(data=df, x='tier', y='bst', order=tiers, palette="muted")
# ax[1].set(xlabel='Tier', ylabel='Moyenne des statistiques', title='Moyenne des statistiques selon le tier')
st.pyplot(fig)

# On peut aussi observer sur le tier **PU** de nombreuses valeurs aberrantes, correspondant à des pokémons ayant de très bonnes statistiques, mais un point faible rendant leur montée dans le classement impossible.

df.bst[(df['tier'] == "PU")].describe()

# Pour la suite de cette analyse, nous allons observer pour chaque tier la moyenne des capacités qu'un pokemon peut apprendre. En effet, un grand nombre de capacités permettrait de rendre un pokémon beaucoup plus intéressant, du fait qu'il soit moins prévisible d'évaluer ce qu'il peut utiliser lors d'un combat stratégique.


# Comme on peut le constater, le nombre de capacités n'est pas un élément significatif permettant de définir le tier stratégique d'un pokémon. Pour tous les tiers, les moyennes sont assez égales et les écart-types sont très faibles. 

# Nous allons maintenant analyser une autre caractérisque des pokémons : le fait qu'un pokémon soit légendaire ou non. En effet, pour la majorité des pokémons, être légendaire implique d'avoir une base de statistique plus élevée que la moyenne.


fig, ax = plt.subplots(figsize=(15,5))
ax = sns.kdeplot(data=final_df, y="bst", x="is_legendary")
st.pyplot(fig)

# Grâce à ce graphique, on peut effectivement confirmer que les pokémons légendaires ont une moyenne de statistiques bien plus élevée que les pokémons "normaux". On pourrait donc conclure de façon pûrement théorique que les pokémons légendaires sont forcément dans des tiers élevés, mais nous allons utiliser un nouveau graphique pour prouver cela.


fig, ax = plt.subplots()
df_leg = final_df[final_df["is_legendary"] == 1]
ax = sns.countplot(data=df_leg, x="is_legendary", hue="tier", hue_order=tiers)
st.pyplot(fig)

# Comme évoquer sur le graphique précédent, on retrouve effectivement dans ce graphique les pokémons légendaires étant principalement dans les tiers les plus élevés. Ce graphique nous permettrait donc d'accentuer le fait qu'avoir une base de statistique élevée permet à un pokémon d'être dans les tiers les plus hauts (sans prendre en compte les éventuelles exceptions provoquées par un talent propre au pokémon (aptitude innée au pokémon et pouvant le rendre extrêmement fort comme extrêmement mauvais, mais il serait trop long de démontrer ce point dans cette analyse de données))

# En conclusion, cette analyse de données a permis de démontrer que plusieurs critères peuvent permettre à un pokémon d'être haut placé dans les tiers stratégiques. Tout d'abord, avoir une bonne base de statistiques serait un élément significatif dans le choix du tier d'un pokémon, les pokémons légendaires étant un bon exemple de par leur moyenne de statistiques très élevée et leurs places majoritaires dans les tiers élevés. Cependant, d'autres aspects sont moins significatifs, comme le nombre de capacités d'un pokémon, qui ne varie pas vraiment entre les pokémons de différents tiers.
