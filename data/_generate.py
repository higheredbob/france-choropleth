from pandas import *
from numpy import *

# Cantons data from ‘code officiel geographique’ database
cog = read_csv("_tmp/comsimp2015.txt", sep="\t", encoding="iso-8859-1", dtype=str)
cog = DataFrame(data={'canton':cog.DEP+"-"+cog.CT,'insee':cog.DEP+cog.COM}).set_index('insee')

# Load cantons names
can = read_csv("_tmp/can.txt", sep="\t", encoding="iso-8859-1", dtype=str)
can = DataFrame(data={'name':can.NCCENR,'canton':can.DEP+"-"+can.CANTON}).set_index('canton')

# Load ‘chiffres clefs’ database
cc = read_excel("_tmp/base-cc-resume-15.xls", sheetname=[0,1], header=5, index_col=[0])
cc = concat([cc[0],cc[1]]).rename(columns = {'LIBGEO':'name'})

# Link communes to cantons
cc = concat([cc, cog[cog.canton.str[-2:].fillna("99").astype('int') < 50]], axis=1).dropna(subset=["name"])
cc.canton[(cc.P12_POP/cc.SUPERF > 75) | (cc.P12_POP > 1000)] = nan
cc.dropna(subset=['canton']).to_csv('_tmp/cog.csv', columns = ['canton'], index_label = 'insee')

# Density and opacity
df = concat([cc,concat([cc.groupby('canton').sum(),can],axis=1).dropna(subset=["name","P12_POP"])])
df['opacity'] = qcut(df.P12_POP/df.SUPERF,100, labels=False)*.75+5
df.to_csv('geo/data.csv', columns = ['name','opacity'], index_label='insee', float_format='%.0f')
