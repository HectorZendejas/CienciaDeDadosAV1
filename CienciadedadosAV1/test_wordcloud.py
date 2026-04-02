try:
    import wordcloud
    print('wordcloud ok', wordcloud.__version__)
except Exception as e:
    print('wordcloud faltando', e)