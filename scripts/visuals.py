import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import pandas as pd
import ast

sns.set(style="whitegrid")

def plot_sentiment_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='sentiment_label', hue='bank')
    plt.title("Sentiment Distribution per Bank")
    plt.xlabel("Sentiment")
    plt.ylabel("Review Count")
    plt.legend(title="Bank")
    plt.tight_layout()
    plt.show()

def plot_rating_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='rating', hue='bank')
    plt.title("Rating Distribution per Bank")
    plt.xlabel("Rating (1–5 Stars)")
    plt.ylabel("Count")
    plt.legend(title="Bank")
    plt.tight_layout()
    plt.show()

def plot_theme_counts(df):
    df['themes'] = df['themes'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    exploded = df.explode('themes')
    exploded = exploded[exploded['themes'] != 'Other']

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=exploded.groupby(['bank', 'themes']).size().reset_index(name='count'),
        x='themes', y='count', hue='bank'
    )
    plt.title("Theme Mentions per Bank (Excluding 'Other')")
    plt.xlabel("Theme")
    plt.ylabel("Mentions")
    plt.legend(title="Bank")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

def generate_wordcloud(df, column="keywords", title="Word Cloud"):
    text = " ".join(
        kw for kw_list in df[column].dropna()
        for kw in (ast.literal_eval(kw_list) if isinstance(kw_list, str) and kw_list.startswith("[") else [])
    )
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(title)
    plt.tight_layout()
    plt.show()

def theme_counts_table(df):
    df['themes'] = df['themes'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    exploded = df.explode('themes')
    exploded = exploded[exploded['themes'] != 'Other']

    theme_counts = (
        exploded.groupby(['bank', 'themes'])
        .size()
        .reset_index(name='count')
    )

    pivot_table = pd.pivot_table(
        theme_counts,
        values='count',
        index='themes',
        columns='bank',
        fill_value=0
    )

    pivot_table.columns.name = 'Themes'  
    pivot_table.index.name = None    

    pivot_table['Total'] = pivot_table.sum(axis=1)
    pivot_table = pivot_table.sort_values('Total', ascending=False)

    styled_table = (
        pivot_table
        .style
        .background_gradient(cmap='Blues', subset=pivot_table.columns[:-1])
        .format("{:.0f}", subset=pivot_table.columns)
        .set_caption("Theme Mentions by Bank (Excluding 'Other')")
        .set_table_styles([
            {'selector': 'caption',
             'props': [('font-size', '16px'),
                       ('font-weight', 'bold'),
                       ('text-align', 'center')]}
        ])
    )

    return styled_table