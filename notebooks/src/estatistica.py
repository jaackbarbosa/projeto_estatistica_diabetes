from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
from scipy.stats import (
    levene, 
    ttest_ind, 
    mannwhitneyu,
)

sns.set_theme(style='dark') 

#-----------------------------------------------------------------------------------------------------------------------------------------------     

def analise_levene(dataframe, alfa=0.05, centro='mean'):
    ''' Teste de Levene, verifica se as variâncias das variáveis são iguais ou se pelo menos uma variância é diferente.

    Parâmetros
    ----------------------------------
    dataframe : pd.DataFrame
        Base de dados.
    alfa : float
        Nível de significância. Por padrão é 0.05. 
    center : str
        Selecionar o tipo de distribuição dos dados para fazer o teste. Verifique as três possibilidades de dados na documentação da função levene.

    Obs.: Se o DataFrame seguir uma distribuição normal, no parâmetro center é usada a média para o cálculo, se a hipótese nula da distribuição normal for rejeitada, no parâmetro center é usado a mediana para o cálculo.
    '''
    print("Teste de Levene")
    
    estatistica_levene, valor_p_levene = levene(
        *[dataframe[coluna] for coluna in dataframe.columns],
        center=centro, 
        nan_policy="omit"
    )
    
    print(f"estatistia_levene: {estatistica_levene:.3f}")
    if valor_p_levene > alfa :
        print(f"Variâncias iguais (valor p: {valor_p_levene:.3f})")
    else:
        print(f"Ao menos uma variância é diferente (valor p: {valor_p_levene:.3f})")        
#------------------------------------------------------------------------------------------------------------------------------------------------

def analise_ttest_ind(dataframe, alfa=0.05, variancias_iguais=True, alternativa="two-sided"):
    ''' Teste Ttest_ind, Calcule o teste T para as médias de duas amostras independentes de pontuações.

    Este é um teste para a hipótese nula de que 2 amostras independentes têm valores médios (esperados) idênticos. Este teste assume que as populações têm variâncias idênticas por padrão..

    Parâmetros
    ----------------------------------
    dataframe : pd.DataFrame
        Base de dados.
    alfa : float
        Nível de significância. Por padrão é 0.05. 
    equal_var : boo
        Realiza um cálculo a partir da afirmação (True) que as variâncias são iguais, se as variâncias forem diferentes o cálculo será feito de uma forma diferente, teste as variâncias antes de usar essa função. Por padrão é True
    alternative : str
        O parâmetro 'alternativa' define a hipótese alternativa. As seguintes opções estão disponíveis (o padrão é 'two-sided'):
         'two-sided (bilateral)': as médias das distribuições subjacentes às amostras são desiguais.
         'less (menos)': a média da distribuição subjacente à primeira amostra é menor que a média da distribuição subjacente à segunda amostra.
         'greater (maior)': a média da distribuição subjacente à primeira amostra é maior que a média da distribuição subjacente à segunda amostra.
    '''
    print("Teste Ttest_ind")
    
    estatistica_ttest_ind, valor_p_ttest_ind = ttest_ind(
        *[dataframe[coluna] for coluna in dataframe.columns],
        equal_var=variancias_iguais, 
        alternative=alternativa,
        nan_policy="omit"
    )
    
    print(f"{estatistica_ttest_ind=:.3f}")
    if valor_p_ttest_ind > alfa :
        print(f"Não rejeita a hipótese nula (valor p: {valor_p_ttest_ind:.3f})")
    else:
        print(f"Rejeita a hipótese nula (valor p: {valor_p_ttest_ind:.3f})")   


#------------------------------------------------------------------------------------------------------------------------------------------------

def analise_mannwhitneyu(dataframe, alfa=0.05, alternativa="two-sided"):
    ''' Teste U de Mann-Whitney .
        Execute o teste de classificação U de Mann-Whitney em duas amostras independentes.
        
        O teste U de Mann-Whitney é um teste não paramétrico da hipótese nula de que a distribuição subjacente à amostra x é a mesma que a distribuição subjacente à amostra y . É frequentemente usado como um teste de diferença de localização entre distribuições.

    Parâmetros
    ----------------------------------
    dataframe : pd.DataFrame
        Base de dados.
    alfa : float
        Nível de significância. Por padrão é 0.05. 
    alternativa : str
        O parâmetro 'alternativa' define a hipótese alternativa. As seguintes opções estão disponíveis (o padrão é 'two-sided'):
         'two-sided (bilateral)': as médias das distribuições subjacentes às amostras são desiguais.
         'less (menos)': a média da distribuição subjacente à primeira amostra é menor que a média da distribuição subjacente à segunda amostra.
         'greater (maior)': a média da distribuição subjacente à primeira amostra é maior que a média da distribuição subjacente à segunda amostra.
    ''' 
    print("Teste U de Mann-Whitney")
    estatistica_mw, valor_p_mw = mannwhitneyu(
        *[dataframe[coluna] for coluna in dataframe.columns],
        nan_policy="omit",
        alternative=alternativa
    )
    
    print(f"{estatistica_mw=:.3f}")
    if valor_p_mw > alfa :
        print(f"Não rejeita a hipótese nula (valor p: {valor_p_mw:.3f})")
    else:
        print(f"Rejeita a hipótese nula (valor p: {valor_p_mw:.3f})")


#------------------------------------------------------------------------------------------------------------------------------------------------

def remove_outliers(dados, largura_bigodes=1.5):
    ''' Removendo os outliers de variáveis numéricas com base no cálculo por trás do boxplot.
    
    Parâmetros
    -------------------------------
    dados : pd.DataFrame, pd.Series ou np.array
        Base contendo apenas dados numéricos.
    largura_bigodes : float
        Largura dos bigodes, que por padrão é de 1.5, mas dependendo da área de aplicação ela pode ser alterada conforme sua utilização.

    Return
    ------------------------------
    pd.DataFrame, pd.Series ou np.array
        Um filtro é para remover os outliers com base no cálculo por trás de um boxplot.
    
    '''
    q1 = dados.quantile(0.25)
    q3 = dados.quantile(0.75)
    iqr = q3 - q1
    return dados[(dados >= q1 - largura_bigodes * iqr) & (dados <= q3 + largura_bigodes * iqr)]


#------------------------------------------------------------------------------------------------------------------------------------------------
def grafico_variaveis_categoricas(
    dataframe, 
    coluna_analise, 
    coluna_alvo=None, 
    numero_linhas=4, 
    numero_colunas=1, 
    tamanho_figura=(14,16),
    compartilhar_eixoy=False,
    espacamento_entre_linhas=0.4, 
    espacamento_entre_colunas=0.4,
    analise_padrao=True
):
    '''Gráfico para avaliar a relação entre a coluna alvo e as variáveis categóricas. Ele exibe a proporção da relação de entre cada categoria da coluna alvo e as categorias das variáveis.

    
    Parametros
    -------------------------------------------------------------
    dataframe : pd.DataFrame
        Base de dados.s
    coluna_analise : list ou np.array
        Variável com as colunas categóricas.
    coluna_alvo : string
        O nome da variável que será incluída no parâmetro hue, por padrão ela suporta uma coluna alvo binária (duas categorias). Quando o parâmetro analise_padrao=False, suporta uma coluna alvo com três ou mais categorias. 
    numero_linhas : int
        Quantidade de linhas para os gráficos da figura. O valor padrão do parâmetro é 4.
    numero_colunas : int
        Quantidade de colunas para os gráficos da figura.  O valor padrão do parâmetro é 1.
    tamanho_figura : tuple e float
        Uma tupa composta por dois floats, o primeiro é a largura e o segundo a altura da figura. O valor padrão do parâmetro é (14,16).
    compartilhar_eixo_y : boo
        Remove os eixos individuais de cada gráfico e compartilha o eixo y com todas os gráficos da mesma linha. O valor padrão do parâmetro é True.
    espacamento_entre_colunas : float
        Altera o espaçamento entre as colunas das categorias dos gráficos na figura. O valor padrão do parâmetro é 0.4
    espacamento_entre_linhas : float
        Altera o espaçamento entre as linhas das categorias dos gráficos na figura. O valor padrão do parâmetro é 0.4
    analise_padrao : boo
        Altera a quantidade de categorias suportadas para comparação. Por padrão é True.
            Quando False, suporta uma coluna alvo com três ou mais categorias. 
            Quando True, suporta uma coluna_alvo com categorias binárias (duas categorias).
    '''
    fig, axs = plt.subplots(nrows=numero_linhas, ncols=numero_colunas, figsize=tamanho_figura, sharey=compartilhar_eixoy)

    if analise_padrao:
        for i, coluna in enumerate(coluna_analise):
            h = sns.histplot(x=coluna, 
                             hue=coluna_alvo, 
                             data=dataframe, 
                             multiple='fill', 
                             ax=axs.flat[i], 
                             stat='percent',
                             shrink=0.8)
            h.tick_params(axis='x', labelrotation=45)
            h.grid(False)
        
            h.yaxis.set_major_formatter(PercentFormatter(1))
            h.set_ylabel('')
        
            for bar in h.containers:
                h.bar_label(bar, label_type='center', labels=[f'{b.get_height():.1%}' for b in bar], color='white', weight='bold', fontsize=11)
        
            legend = h.get_legend()
            legend.remove()
        
        labels = [text.get_text() for text in legend.get_texts()]
        
        fig.legend(handles=legend.legend_handles, labels=labels, loc='upper center', ncols=2, title=coluna_alvo, bbox_to_anchor=(0.5, 0.965))
        fig.suptitle(f'{coluna_alvo} por variável categórica', fontsize=16)
        
        fig.align_labels()
        
        plt.subplots_adjust(wspace=espacamento_entre_colunas, hspace=espacamento_entre_linhas, top=0.925)
    
    else:
        # para pegar cada sistema de eixo individualmente, vamos usar o método flatten() na variável axs e zipar com a nossa variável com as colunas para análise
        for ax, coluna in zip(axs.flatten(), coluna_analise): 
            h = sns.histplot(x=coluna_alvo, 
                             hue=coluna, # vamos usar cada loop para criar uma coluna alvo diferente
                             data=dataframe, 
                             multiple='fill', 
                             ax=ax, # vamos pegar o sistema de eixo diretamente
                             stat='percent',
                             shrink=0.8)
            h.tick_params(axis='x', labelrotation=45)
        
            h.yaxis.set_major_formatter(PercentFormatter(1))
            h.set_ylabel('')
        
            for bar in h.containers:
                h.bar_label(
                    bar, label_type='center', 
                    labels=[f'{b.get_height():.1%}' for b in bar], 
                    color='white', 
                    weight='bold', 
                    fontsize=11)
        
            # vamos selecionar a legenda
            legend = h.get_legend()
        
            labels = [text.get_text() for text in legend.get_texts()]
        
            # verificando a quantidade de categorias em cada variável a cada loop
            numero_itens = len(dataframe[coluna].cat.categories)
        
            # padrinizando a apresentação das legendas
            ax.legend(
                handles=legend.legend_handles, # incluindo as bandeiras na legenda
                labels=labels, # colocando rótulo nas bandeiras
                loc="upper center", # centralizando as categorias na parte superior do gráfico 
                ncols=numero_itens if numero_itens <= 6 else min(4, numero_itens), # criando condição para se a legenda for igual ou inferior a 6, exiba todas as categorias em um alinha, se tiver mais, as categorias serão quebradas em 4 por linha no máximo
                bbox_to_anchor=(0.5, 1.15) # primeiro centralizando a legenda (0.5) e colocando em uma altura superior ao gráfico (0.15)
            )
        
            # incluindo o título por cada categoria da variável de análise referente a coluna alvo
            ax.set_title(f"Distribuição de {coluna} por nível de {coluna_alvo}.", fontsize=14, pad=55)
        
            # ajustes para espaçamento entre as categorias
            
        plt.subplots_adjust(wspace=espacamento_entre_colunas, hspace=espacamento_entre_linhas, top=0.925)
    
        plt.show()
