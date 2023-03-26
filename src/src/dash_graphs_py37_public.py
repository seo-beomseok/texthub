import pandas as pd
import numpy as np
import datetime as dt
import os
from collections import OrderedDict

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash import Dash, dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from jupyter_dash import JupyterDash

######################################################################################
### Dash Graphs
######################################################################################

class DashGraphs():
	def __init__(self, AR):
		self.AR = AR

	@staticmethod
	def plotTableDash(dat, figsize=(13,3), color_cell_list = [], title='', show=True, load_csv=True):
		# public

		title = title.replace('/','')
		
		if load_csv:
			color_cell_list = pd.read_csv('./out'+'/FA_colorcell_'+title+'.csv',index_col=0).to_numpy()
			dat = pd.read_csv('./out'+'/FA_table_'+title+'.csv',index_col=0).to_numpy()

		H = dat.shape[0]
		W = dat.shape[1]

		matrix_dat = np.empty((H,W),dtype=object)
		matrix_col = np.empty((H,W),dtype=object)
		for i in range(H):
			for j in range(W):
				matrix_col[i,j] = 'rgb(150, 150, 150)'

		for (i, j), value in np.ndenumerate(dat.T):   
			if j==0:
				matrix_dat[j, i]=value
			else:
				matrix_dat[j, i]=value
			
		  
		matrix_pd = pd.DataFrame(matrix_dat[1:,:], columns=matrix_dat[0,:])
		
		fig = dash_table.DataTable(
			# fill_width=False,
			data=matrix_pd.to_dict('records'),
			columns=[{'id': c, 'name': c} for c in matrix_pd.columns],
			style_table={'overflowX': 'auto'},
		    style_cell={'overflow': 'hidden',
				        'textOverflow': 'ellipsis',
				        'maxWidth': '70px',},			
			style_header={'backgroundColor': px.colors.qualitative.G10[4], #'#ab63fa',
						  'color': 'white',
						  # 'font-weight': 'bold',
						  'font-family': 'Open Sans Bold',
						  'font-size': '1.2rem',
						  'border': '1px solid black',
						  'textAlign': 'center'},
			style_data={'backgroundColor': 'rgb(150, 150, 150)',
						'color': 'black',
						'width': '70px',
						'maxWidth': '70px',
						'minWidth': '70px',
						'font-weight': 'lighter',
		                'font-family': 'Open Sans',
		                'font-size': '1.2rem',
		                'border': '1px solid grey',
						'textAlign': 'center'},
			style_data_conditional=[{'if': {'row_index': c[1]-1, 'column_id': matrix_pd.columns[c[0]]}, 
									 'background-color': px.colors.qualitative.Plotly[c[2]], 
									 'color': 'black'} for c in color_cell_list],)

		if show:
			pass

		return fig


	@staticmethod
	def plotEventImpact(EA, num_fields=5, threshold_ratio=0, legend_loc='best', beg='2019q1', end='2023q1', show=True):
		# public
		pd.options.plotting.backend = "plotly"

		ids = EA.pd_interest.max(axis=1)[EA.pd_interest.max(axis=1)>threshold_ratio].sort_values(ascending=False)[:num_fields]

		fig = EA.pd_interest.loc[ids.index,beg:end].transpose().fillna(0).plot(template='plotly_dark')

		fig.update_layout(legend_title_text = 'Field')
		fig.update_xaxes(title_text='Quarter', tickangle=270)
		fig.update_yaxes(title_text='TIEI')

		if show:
			fig.show()

		return fig


	@staticmethod
	def plotEventEval(EA, num_fields=5, legend_loc='best', beg='2019q1', end='2023q1', show=True):
		# public
		pd.options.plotting.backend = "plotly"

		ids_ = list(EA.pd_rank.sum(axis=1).sort_values(ascending=False).index[:num_fields])

		fig = EA.pd_interest.loc[ids_,beg:end].transpose().plot(template='plotly_dark')
		
		fig.update_traces(connectgaps=True)
		fig.update_layout(legend_title_text = 'Field')
		fig.update_xaxes(title_text='Quarter', tickangle=270)
		fig.update_yaxes(title_text='TEEI')
		fig.add_hline(y=100, line_width=1, line_dash='dash', line_color='red')

		if show:
			fig.show()

		return fig		


	@staticmethod
	def plotKospiPlotly(MA, field, krxfield, type=1, return_dat=False, return_corr=False, diff=False, rescale=True, show=True,
				  beg='2019q1', end='2023q1', load_csv=True):
		# public

		
		fig = make_subplots(specs=[[{"secondary_y": True}]])
			
		ibeg = np.where([i==beg for i in MA.timepoints])[0][0]
		try:
			iend = np.where([i==end for i in MA.timepoints])[0][0]
		except:
			iend = len(MA.timepoints)


		if type==1:
			if load_csv:
				temp_dat = pd.read_csv(MA.AR.out_dir+'/MA_temp_dat_t1_'+MA.period+'.csv',index_col=0, header=[0,1]).iloc[:,ibeg:iend].transpose()[[field]]
			else:
				temp_dat = MA.AR.dat_sents_labs.loc[MA.AR.dat_sents_labs['BOK업종']==field,['lab','BOK업종',MA.period]].groupby(['BOK업종',MA.period]).apply(lambda x: x.sum()/x.abs().sum()).unstack().iloc[:,ibeg:iend].transpose()
			temp_dat.index = [x[1] for x in temp_dat.index]
			temp_dat.columns = ['TBCI '+field]
		elif type==2:
			if load_csv:
				temp_dat = pd.read_csv(MA.AR.out_dir+'/MA_temp_dat_t2_'+MA.period+'.csv',index_col=0, header=0).iloc[:,ibeg:iend].transpose()
			else:
				temp_dat = MA.AR.dat_sents_labs.loc[[x in field for x in MA.AR.dat_sents_labs['BOK업종']],['lab',MA.period]].groupby([MA.period]).apply(lambda x: x.sum()/x.abs().sum()).transpose().iloc[:,ibeg:iend].transpose()
			temp_dat.columns = ['TBCI '+' + '.join(field)]
			temp_dat.index.name = None
		elif type==3:
			if load_csv:
				temp_dat = pd.read_csv(MA.AR.out_dir+'/MA_temp_dat_t3_'+MA.period+'.csv',index_col=[0,1], header=0)
			else:
				temp_dat = MA.AR.dat_sents_labs.loc[:,['lab',MA.period]].groupby([MA.period]).apply(lambda x: x.sum()/x.abs().sum()).unstack().to_frame('증권사')
			temp_dat.index = [str(x[1]) for x in temp_dat.index]
			temp_dat.columns = ['TBCI 전산업 업황']

		if rescale:
			temp_dat = 10*((temp_dat - np.nanmean(temp_dat))/np.nanstd(temp_dat))+100			

	
		if diff:
			fig.add_trace(go.Scatter(x=temp_dat.index, y=temp_dat.iloc[:,0].diff(), name=temp_dat.columns[0], mode='lines', ), secondary_y=False,)
		else:
			fig.add_trace(go.Scatter(x=temp_dat.index, y=temp_dat.iloc[:,0], name=temp_dat.columns[0], mode='lines', line=dict()), secondary_y=False,) #color='#ab63fa'


		if load_csv:
			krx_temp_dat = pd.read_csv(MA.AR.out_dir+'/MA_krx_dat_'+MA.period+'.csv',index_col=0, header=0)[krxfield]
		else:
			krx_temp_dat = MA.krx_dat_[krxfield]
	
		if type==1 or type==2:
			krx_temp_dat.name = '코스피 '+krxfield
		elif type==3:
			pass
			

		if diff:
			fig.add_trace(go.Scatter(x=krx_temp_dat.index, y=krx_temp_dat.diff(), name=krx_temp_dat.name, mode='lines', line=dict(dash='dash')), secondary_y=True,)
		else:
			fig.add_trace(go.Scatter(x=krx_temp_dat.index, y=krx_temp_dat, name=krx_temp_dat.name, mode='lines', line=dict(dash='dash',)), secondary_y=True,) #color='#fecb52'
				
		fig.update_xaxes(title_text=MA.period.capitalize(), tickangle=270)
		fig.update_yaxes(title_text='TBCI', secondary_y=False)
		fig.update_yaxes(title_text='Points in KRX', secondary_y=True)
		fig.update_layout(template='plotly_dark')
		fig.update_layout(legend_title_text = 'Field',margin=dict(t=50, b=50, r=20),)

		if show:
			fig.show()
		
		return fig

	@staticmethod
	def plotNewsPlotly(period, field, relfield, add_stat=True, return_dat=False, return_corr=False, diff=False, rescale=True, show=True):
		# public
		
		fig = make_subplots(specs=[[{"secondary_y": True}]])

		temp_dat = pd.read_csv('./out'+'/TFI_'+period+'_'+field+'.csv',index_col=0, header=[0])
		temp_dat.index = [str(x) for x in temp_dat.index]
		temp_dat.columns = [field.split('_')[0]]

		temp_dat = temp_dat.iloc[np.where([str(x)=='200601' for x in temp_dat.index])[0][0]:,:]

		if rescale:
			temp_dat = 10*((temp_dat - np.nanmean(temp_dat))/np.nanstd(temp_dat))+100

	
		if diff:
			fig.add_trace(go.Scatter(x=temp_dat.index, y=temp_dat.iloc[:,0].diff(), name=temp_dat.columns[0], mode='lines', ), secondary_y=False,)
		else:
			fig.add_trace(go.Scatter(x=temp_dat.index, y=temp_dat.iloc[:,0], name=temp_dat.columns[0], mode='lines', line=dict()), secondary_y=False,) #color='#ab63fa'
				
		fig.update_xaxes(title_text=period.capitalize(), tickangle=270)
		fig.update_yaxes(title_text='TFNI', secondary_y=False)
		# fig.update_yaxes(title_text='Points in KRX', secondary_y=True)
		fig.update_layout(template='plotly_dark')
		fig.update_layout(legend_title_text = 'Field',margin=dict(t=50, b=50, r=20),)

		if show:
			fig.show()
		
		if add_stat:
			try:
				df_stat = pd.read_csv('./out'+'/SI_month_'+field+'.csv', index_col=0)
				if period=='month':
					fig.add_trace(go.Scatter(x=df_stat.index, y=df_stat.iloc[:,0], name=df_stat.columns[0], mode='lines', line=dict(), visible='legendonly'), secondary_y=True)
				elif period=='week':
					temp_index = [y[0]*100+y[1] for y in [dt.date(int(str(x)[:4]),int(str(x)[4:]),15).isocalendar() for x in df_stat.index]]
					fig.add_trace(go.Scatter(x=temp_index, y=df_stat.iloc[:,0], name=df_stat.columns[0], mode='lines', line=dict(), visible='legendonly'), secondary_y=True)
			except:
				pass

		return fig

	def plotTreemap(self, quarter='2022q4', show=True, load_csv=True):
		# public

		if load_csv:
			treemap_dat = pd.read_csv('./out'+'/Treemap_dat_'+quarter+'.csv')
		else:
			if quarter[5]=='1':
				quarter_prev = str(int(quarter[:4])-1)+'q4'
			else:
				quarter_prev = quarter[:5]+str(int(quarter[5])-1)

			treemap_dat = pd.DataFrame(columns=['names','parents','values','color'])

			for item in ['BOK업종','업종','topic']:
			    values = AR.dat_sents_labs.loc[(AR.dat_sents_labs['quarter']==quarter) & (~AR.dat_sents_labs[item_parent].isnull())][[item,'sents']].groupby(item).count().sort_values('sents',ascending=False)
			    ids = values.index.values
			    
			    if item=='BOK업종':
			        parents = ['전산업']*len(ids)
			    else:
			        if item=='업종':
			            item_parent = 'BOK업종'
			        elif item=='topic':
			            item_parent = '업종'
			            
			        parents = AR.dat_sents_labs.loc[AR.dat_sents_labs['quarter']==quarter][[item,item_parent]].groupby([item,item_parent]).count().reset_index(1).loc[ids,item_parent].values
			    
			    color_crnt = AR.dat_sents_labs.loc[AR.dat_sents_labs['quarter']==quarter][[item,'lab']].groupby(item).mean()
			    color_past = AR.dat_sents_labs.loc[AR.dat_sents_labs['quarter']==quarter_prev][[item,'lab']].groupby(item).mean()
			    color_crnt = color_crnt.merge(color_past, left_index=True, right_index=True, how='left')
			    color_crnt = color_crnt['lab_x']/color_crnt['lab_y']*100-100
			    color_crnt = np.sign(color_crnt)*np.log(np.abs(color_crnt))
			    color_crnt = color_crnt[ids]
			    
			    temp = pd.DataFrame({'names':ids, 'parents':parents, 'values':values.to_numpy().flatten(), 'color':color_crnt.to_numpy().flatten()})
			    treemap_dat = pd.concat([treemap_dat,temp])
		
		fig = px.treemap(
		    names = treemap_dat['names'],
		    parents = treemap_dat['parents'],
		    values = treemap_dat['values'],
		    color = treemap_dat['color'],
		    maxdepth = 2,
		)
		fig.update_traces(root_color="lightgrey")
		fig.update_layout(template='plotly_dark')
		fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
		
		if show:
			fig.show()
		
		return fig

class AnalystReportShell():
	# public
    def __init__(self, curr_dir=os.getcwd(), beg_date=None, end_date=None):
        self.curr_dir = curr_dir
        self.dat_dir = curr_dir + '/data'
        self.res_dir = curr_dir + '/res'
        self.src_dir = curr_dir + '/src'
        self.out_dir = curr_dir + '/out'
        self.fig_dir = curr_dir + '/fig'
        self.txt_dir = curr_dir + '/selenium/texted'
        
        self.beg_date = beg_date
        self.end_date = end_date	


class MarketAnalysisShell():
	# public
    def __init__(self, AnalystReport):
        self.AR = AnalystReport

    def getMarketDat(self, period='quarter'):
        self.period = period        
        self.timepoints = pd.read_csv(self.AR.out_dir+'/MA_timepoints_'+self.period+'.csv',index_col=0,dtype=object)['0']


class EventAnalysisShell():
	# public
	def __init__(self, AnalystReport):
		self.AR = AnalystReport

	def eventImpact(self, interest):
		self.pd_interest = pd.read_csv(self.AR.out_dir+'/EA_impact_'+interest+'.csv',index_col=0, header=0)

	def eventEval(self, interest):
		self.pd_interest = pd.read_csv(self.AR.out_dir+'/EA_eval_interest_'+interest+'.csv',index_col=0, header=0)
		self.pd_rank = pd.read_csv(self.AR.out_dir+'/EA_eval_rank_'+interest+'.csv',index_col=0, header=0)		